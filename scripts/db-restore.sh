#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# db-restore.sh — Restore a PostgreSQL dump into the decoupled WCOA Docker DB.
#
# Usage:
#   ./scripts/db-restore.sh <dump.sql>
#   ./scripts/db-restore.sh --drop <dump.sql>                    # drop & recreate DB first
#   ./scripts/db-restore.sh --env-file <path> <dump.sql>
#   ./scripts/db-restore.sh --core-compose <path> <dump.sql>
#   ./scripts/db-restore.sh --project-compose <path> <dump.sql>
#
# Run from anywhere — this script always operates relative to madrona-apps/wcoa/.
#
# Prerequisites:
#   1. Docker Compose stack is running with both decoupled compose files:
#        docker compose \
#          -f ../../madrona-portal/docker/compose.base.yml \
#          -f docker/compose.yml \
#          --env-file docker/.env up -d
#   2. wcoa/docker/.env exists and contains DB_NAME, DB_USER, DB_PASSWORD.
#
# Options:
#   --drop              Terminate all active connections, drop, and recreate the
#                       target database before restoring. Required for a clean
#                       import from prod. Without this flag the dump is applied
#                       on top of existing data.
#   --env-file <path>   Path to the .env file (default: ./docker/.env).
#   --core-compose <path>
#                       Path to compose.base.yml
#                       (default: ../../madrona-portal/docker/compose.base.yml).
#   --project-compose <path>
#                       Path to wcoa compose overlay
#                       (default: ./docker/compose.yml).
#
# Notes:
#   - The dump is streamed directly into the db container (no temp files).
#   - psql warnings (e.g. "already exists") are normal when importing a dump
#     produced on a different Postgres version (12 → 16) and are not fatal.
#   - After a --drop restore, run migrations to pick up any schema drift:
#       docker compose -f <core-compose> -f <project-compose> --env-file <env-file> \
#         exec app python marco/manage.py migrate
# -----------------------------------------------------------------------------
set -euo pipefail

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
die()  { echo "[db-restore] ERROR: $*" >&2; exit 1; }
info() { echo "[db-restore] $*"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DEFAULT_ENV_FILE="$PROJECT_ROOT/docker/.env"
DEFAULT_CORE_COMPOSE="$PROJECT_ROOT/../../madrona-portal/docker/compose.base.yml"
DEFAULT_PROJECT_COMPOSE="$PROJECT_ROOT/docker/compose.yml"

resolve_to_abs() {
  local path="$1"
  [[ -n "$path" ]] || return 1
  if [[ "$path" == ~* ]]; then
    path="${path/#\~/$HOME}"
  fi
  echo "$(cd "$(dirname "$path")" && pwd)/$(basename "$path")"
}

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
DROP_FIRST=false
DUMP_FILE=""
ENV_FILE="$DEFAULT_ENV_FILE"
CORE_COMPOSE_FILE="$DEFAULT_CORE_COMPOSE"
PROJECT_COMPOSE_FILE="$DEFAULT_PROJECT_COMPOSE"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --drop)     DROP_FIRST=true; shift ;;
    --env-file) [[ -n "${2:-}" ]] || die "--env-file requires a path argument"
                ENV_FILE="$2"; shift 2 ;;
    --core-compose)
                [[ -n "${2:-}" ]] || die "--core-compose requires a path argument"
                CORE_COMPOSE_FILE="$2"; shift 2 ;;
    --project-compose)
                [[ -n "${2:-}" ]] || die "--project-compose requires a path argument"
                PROJECT_COMPOSE_FILE="$2"; shift 2 ;;
    -*)         die "Unknown option: '$1'. Usage: $0 [--drop] [--env-file <path>] [--core-compose <path>] [--project-compose <path>] <dump.sql>" ;;
    *)          [[ -z "$DUMP_FILE" ]] || die "Unexpected argument: '$1'"
                DUMP_FILE="$1"; shift ;;
  esac
done

[[ -n "$DUMP_FILE" ]] || die "Usage: $0 [--drop] [--env-file <path>] [--core-compose <path>] [--project-compose <path>] <dump.sql>"

# Resolve dump path before we cd away.
DUMP_ABS="$(resolve_to_abs "$DUMP_FILE")"
[[ -f "$DUMP_ABS" ]] || die "Dump file not found: $DUMP_FILE"

ENV_FILE_ABS="$(resolve_to_abs "$ENV_FILE")"
[[ -f "$ENV_FILE_ABS" ]] || die "Env file not found: $ENV_FILE"

CORE_COMPOSE_ABS="$(resolve_to_abs "$CORE_COMPOSE_FILE")"
[[ -f "$CORE_COMPOSE_ABS" ]] || die "Core compose file not found: $CORE_COMPOSE_FILE"

PROJECT_COMPOSE_ABS="$(resolve_to_abs "$PROJECT_COMPOSE_FILE")"
[[ -f "$PROJECT_COMPOSE_ABS" ]] || die "Project compose file not found: $PROJECT_COMPOSE_FILE"

# ---------------------------------------------------------------------------
# Always operate from the wcoa repo regardless of where the script is called
# ---------------------------------------------------------------------------
cd "$PROJECT_ROOT"

# ---------------------------------------------------------------------------
# Load .env for DB credentials and DJANGO_ENV
# ---------------------------------------------------------------------------
set -a
# shellcheck source=/dev/null
source "$ENV_FILE_ABS"
set +a

DB_NAME="${DB_NAME:-wcoa_docker_db}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:?DB_PASSWORD must be set in .env}"

# ---------------------------------------------------------------------------
# Compose command helpers
# ---------------------------------------------------------------------------
compose() {
  docker compose -f "$CORE_COMPOSE_ABS" -f "$PROJECT_COMPOSE_ABS" --env-file "$ENV_FILE_ABS" "$@"
}

psql_exec() {
  compose exec -T -e "PGPASSWORD=$DB_PASSWORD" db psql -U "$DB_USER" "$@"
}

info "Using core compose:    $CORE_COMPOSE_ABS"
info "Using project compose: $PROJECT_COMPOSE_ABS"
info "Using env file:        $ENV_FILE_ABS"

# ---------------------------------------------------------------------------
# Verify the db container is healthy before doing anything
# ---------------------------------------------------------------------------
info "Checking db service health..."
compose ps db | grep -q "healthy" \
  || die "db container is not healthy. Is the stack running? Try: docker compose -f $CORE_COMPOSE_ABS -f $PROJECT_COMPOSE_ABS --env-file $ENV_FILE_ABS up -d"

# ---------------------------------------------------------------------------
# Optional: terminate connections, drop, and recreate the database
# ---------------------------------------------------------------------------
if [[ "$DROP_FIRST" == true ]]; then
  info "Terminating active connections to '$DB_NAME'..."
  psql_exec -d postgres -c \
    "SELECT pg_terminate_backend(pid)
     FROM pg_stat_activity
     WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();" \
    > /dev/null

  info "Dropping database '$DB_NAME'..."
  psql_exec -d postgres -c "DROP DATABASE IF EXISTS \"$DB_NAME\";"

  info "Creating database '$DB_NAME'..."
  psql_exec -d postgres -c "CREATE DATABASE \"$DB_NAME\";"

  info "Enabling PostGIS extension..."
  psql_exec -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
fi

# ---------------------------------------------------------------------------
# Stream the dump into the database
# ---------------------------------------------------------------------------
DUMP_SIZE="$(du -sh "$DUMP_ABS" | cut -f1)"
info "Restoring '$DUMP_FILE' (${DUMP_SIZE}) → '$DB_NAME'..."
info "psql warnings about existing objects are expected and non-fatal."

psql_exec -d "$DB_NAME" \
  --set ON_ERROR_STOP=off \
  < "$DUMP_ABS"

info "Restore complete."
info ""
info "Next steps:"
info "  Apply any pending migrations:"
info "    docker compose -f $CORE_COMPOSE_ABS -f $PROJECT_COMPOSE_ABS --env-file $ENV_FILE_ABS exec app python marco/manage.py migrate"
