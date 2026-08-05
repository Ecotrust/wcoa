#!/usr/bin/env bash

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ROOT_DIR="$(cd "$DIR/.." >/dev/null 2>&1 && pwd)"

COMPOSE_FILE="$ROOT_DIR/docker/compose.prod.yml"
ENV_FILE="$ROOT_DIR/docker/.env"
SERVICE_NAME="db"

DBNAME=""
DBOWNER=""
DBPASSWORD=""
OUTDIR="$ROOT_DIR/docker/backups/sql"
OUTFILE=""

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

Options:
  -n <db_name>         Database name (default: DB_NAME from env file)
  -o <db_owner>        Database user (default: DB_USER from env file)
  -p <db_password>     Database password (default: DB_PASSWORD from env file)
  -d <output_dir>      Output directory (default: docker/backups/sql)
  -f <output_file>     Output filename (default: <db_name>_dump_<timestamp>.sql)
  -c <compose_file>    Docker compose file path
  -e <env_file>        Environment file path
  -s <service_name>    Docker service name (default: db)
  -h                   Show this help
EOF
}

while getopts ":n:o:p:d:f:c:e:s:h" flag; do
  case "$flag" in
    n) DBNAME="$OPTARG" ;;
    o) DBOWNER="$OPTARG" ;;
    p) DBPASSWORD="$OPTARG" ;;
    d) OUTDIR="$OPTARG" ;;
    f) OUTFILE="$OPTARG" ;;
    c) COMPOSE_FILE="$OPTARG" ;;
    e) ENV_FILE="$OPTARG" ;;
    s) SERVICE_NAME="$OPTARG" ;;
    h)
      usage
      exit 0
      ;;
    :) echo "Error: Option -$OPTARG requires an argument." >&2; usage; exit 1 ;;
    \?) echo "Error: Invalid option -$OPTARG" >&2; usage; exit 1 ;;
  esac
done

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "Error: Docker compose file not found at $COMPOSE_FILE" >&2
  exit 1
fi

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

DBNAME="${DBNAME:-${DB_NAME:-}}"
DBOWNER="${DBOWNER:-${DB_USER:-}}"
DBPASSWORD="${DBPASSWORD:-${DB_PASSWORD:-}}"

if [[ -z "$DBNAME" || -z "$DBOWNER" || -z "$DBPASSWORD" ]]; then
  echo "Error: DB credentials are incomplete. Provide -n/-o/-p or set DB_NAME/DB_USER/DB_PASSWORD in env file." >&2
  exit 1
fi

mkdir -p "$OUTDIR"

if [[ -z "$OUTFILE" ]]; then
  OUTFILE="${DBNAME}_dump_$(date +%F_%H-%M-%S).sql"
fi

OUTPATH="$OUTDIR/$OUTFILE"

compose_cmd=(docker compose -f "$COMPOSE_FILE")
if [[ -f "$ENV_FILE" ]]; then
  compose_cmd+=(--env-file "$ENV_FILE")
fi

CONTAINER_ID="$(${compose_cmd[@]} ps -q "$SERVICE_NAME")"

if [[ -z "$CONTAINER_ID" ]]; then
  echo "Error: Service '$SERVICE_NAME' is not running." >&2
  exit 1
fi

${compose_cmd[@]} exec -T \
  -e PGPASSWORD="$DBPASSWORD" \
  "$SERVICE_NAME" \
  pg_dump -b -c -n public -O --quote-all-identifiers --no-acl -w -U "$DBOWNER" -d "$DBNAME" > "$OUTPATH"

echo "Database dump created: $OUTPATH"
