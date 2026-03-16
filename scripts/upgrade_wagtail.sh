#!/usr/bin/env bash
# =============================================================================
# upgrade_wagtail.sh
# Scripted upgrade from Wagtail 6.1.3 → 7.0
#
# Usage:
#   ./upgrade_wagtail.sh [OPTIONS]
#
# Options:
#   --dry-run           Show what would happen without making changes
#   --skip-tests        Skip test suite at each step (faster, less safe)
#   --start-from VER    Resume from a specific version (6.2 | 6.3 | 7.0)
#   --python PATH       Python executable to use (default: python)
#   --pip PATH          Pip executable to use (default: pip)
#   -h, --help          Show this help message
#
# Examples:
#   ./upgrade_wagtail.sh
#   ./upgrade_wagtail.sh --dry-run
#   ./upgrade_wagtail.sh --start-from 6.3
#   ./upgrade_wagtail.sh --skip-tests --python python3
# =============================================================================

set -euo pipefail

# ── Colour output ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# ── Defaults ──────────────────────────────────────────────────────────────────
DRY_RUN=false
SKIP_TESTS=true
START_FROM=""
PYTHON_BIN="/usr/local/apps/env/bin/python3"
PIP_BIN="pip"
MP_PROJECT_CONFIG="MP_PROJECT_CONFIG='config.wcoa.ini'"
MANAGE_PATH="/usr/local/apps/madrona_portal/marco/manage.py"

# ── Helpers ───────────────────────────────────────────────────────────────────
log()   { echo -e "$*"; }
info()  { log "${BLUE}[INFO]${NC}  $*"; }
ok()    { log "${GREEN}[OK]${NC}    $*"; }
warn()  { log "${YELLOW}[WARN]${NC}  $*"; }
error() { log "${RED}[ERROR]${NC} $*"; }
step()  { log "\n${BOLD}${BLUE}══ $* ${NC}"; }
hr()    { log "────────────────────────────────────────────────────────────"; }

run() {
    log "${YELLOW}▶ $*${NC}"
    if [[ "$DRY_RUN" == true ]]; then
        log "  (dry-run — skipped)"
    else
        "$@" 2>&1
    fi
}

die() { error "$*"; exit 1; }

usage() {
    grep '^#' "$0" | grep -v '#!/' | sed 's/^# \?//' | head -30
    exit 0
}

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)       DRY_RUN=true ;;
        --skip-tests)    SKIP_TESTS=true ;;
        --start-from)    START_FROM="$2"; shift ;;
        --python)        PYTHON_BIN="$2"; shift ;;
        --pip)           PIP_BIN="$2"; shift ;;
        -h|--help)       usage ;;
        *) die "Unknown option: $1 — run with --help for usage" ;;
    esac
    shift
done

manage() {
    MP_PROJECT_CONFIG='config.wcoa.ini' "$PYTHON_BIN" "$MANAGE_PATH" "$@"
}

# ── Track whether each major section passed ───────────────────────────────────
PREFLIGHT_OK=true
UPGRADE_OK=true
AUDIT_ISSUES=()

# =============================================================================
# SECTION 1 — PREFLIGHT CHECKS
# =============================================================================
step "PREFLIGHT CHECKS"

# Verify we're in a Django project root
if [[ ! -f "$MANAGE_PATH" ]]; then
    die "manage.py not found. Run this script from your Django project root."
fi

# Verify Python is available
if ! command -v "$PYTHON_BIN" &>/dev/null; then
    die "Python executable not found: $PYTHON_BIN"
fi
PYTHON_VERSION=$("$PYTHON_BIN" --version 2>&1)
info "Python: $PYTHON_VERSION"

# Verify pip is available
if ! command -v "$PIP_BIN" &>/dev/null; then
    die "Pip executable not found: $PIP_BIN"
fi

# Check current Wagtail version
CURRENT_WAGTAIL=$("$PIP_BIN" freeze 2>/dev/null | grep -i '^wagtail==' | head -n1 | cut -d'=' -f3 || true)
CURRENT_WAGTAIL="${CURRENT_WAGTAIL:-unknown}"
info "Current Wagtail: $CURRENT_WAGTAIL"

# Warn if not starting from expected version and no --start-from provided
if [[ "$CURRENT_WAGTAIL" != "6.1"* && -z "$START_FROM" ]]; then
    warn "Expected Wagtail 6.1.x but found $CURRENT_WAGTAIL."
    warn "If you have already partially upgraded, use --start-from to resume."
    warn "Continuing anyway — but verify this is intentional."
fi

# Check Django version compatibility
DJANGO_VERSION=$("$PYTHON_BIN" -c "import django; print(django.__version__)" 2>/dev/null || echo "unknown")
info "Django: $DJANGO_VERSION"
DJANGO_MAJOR=$(echo "$DJANGO_VERSION" | cut -d. -f1)
DJANGO_MINOR=$(echo "$DJANGO_VERSION" | cut -d. -f2)
if [[ "$DJANGO_MAJOR" -lt 4 ]] || [[ "$DJANGO_MAJOR" -eq 4 && "$DJANGO_MINOR" -lt 2 ]]; then
    die "Wagtail 7.0 requires Django 4.2+. Current: $DJANGO_VERSION — upgrade Django first."
fi
ok "Django version is compatible ($DJANGO_VERSION)"

# Check for a virtual environment (advisory)
if [[ -z "${VIRTUAL_ENV:-}" && -z "${CONDA_DEFAULT_ENV:-}" ]]; then
    warn "No active virtual environment detected. It is strongly recommended to upgrade inside a venv."
fi

# Check for pending migrations before we start
info "Checking for unapplied migrations..."
PENDING=$(manage showmigrations --plan 2>/dev/null | grep -c "\[ \]" || true)
PENDING=${PENDING:-0}
if [[ "$PENDING" -gt 0 ]]; then
    die "There are $PENDING unapplied migrations. Run 'python manage.py migrate' before upgrading."
fi
ok "No pending migrations"

# Check git status (advisory)
if command -v git &>/dev/null && git rev-parse --is-inside-work-tree &>/dev/null; then
    DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$DIRTY" -gt 0 ]]; then
        warn "Working tree has $DIRTY uncommitted change(s). Consider committing or stashing before proceeding."
    else
        ok "Git working tree is clean"
    fi
else
    warn "Not a git repository (or git not installed) — cannot verify clean state"
fi

hr

# =============================================================================
# SECTION 2 — DEPRECATION WARNING BASELINE
# =============================================================================
step "DEPRECATION WARNING SCAN (current codebase)"

info "Running test suite with deprecation warnings as errors..."
if [[ "$SKIP_TESTS" == true ]]; then
    warn "--skip-tests is set. Skipping deprecation scan. This is not recommended for the initial check."
elif [[ "$DRY_RUN" == true ]]; then
    info "(dry-run) Would run: MP_PROJECT_CONFIG=config.wcoa.ini $PYTHON_BIN -W error::DeprecationWarning $MANAGE_PATH test"
else
    set +e
    MP_PROJECT_CONFIG='config.wcoa.ini' "$PYTHON_BIN" -W error::DeprecationWarning "$MANAGE_PATH" test 2>&1
    DEP_STATUS=$?
    set -e
    if [[ $DEP_STATUS -ne 0 ]]; then
        warn "Deprecation warnings detected (exit code $DEP_STATUS)."
        warn "It is strongly recommended to resolve these before continuing."
        warn "Press Enter to continue anyway, or Ctrl+C to abort and fix them first."
        read -r
    else
        ok "No deprecation warnings found"
    fi
fi

hr

# =============================================================================
# SECTION 3 — STEP-THROUGH UPGRADE LOOP
# =============================================================================
# Wagtail recommends upgrading one feature version at a time so that
# deprecation warnings surface before they become hard errors.

declare -a VERSIONS=("6.2" "6.3" "7.0")
declare -a CONSTRAINTS=(">=6.2,<6.3" ">=6.3,<7.0" ">=7.0,<7.1")
declare -a MESSAGES=(
    "Upgrade to 6.2 — surfaces deprecations from 6.0/6.1"
    "Upgrade to 6.3 — surfaces deprecations from 6.2, last before major"
    "Upgrade to 7.0 (LTS) — final target"
)

START_IDX=0
if [[ -n "$START_FROM" ]]; then
    found=false
    for i in "${!VERSIONS[@]}"; do
        if [[ "${VERSIONS[$i]}" == "$START_FROM" ]]; then
            START_IDX=$i
            found=true
            break
        fi
    done
    if [[ "$found" == false ]]; then
        die "--start-from value '$START_FROM' is not valid. Choose from: 6.2, 6.3, 7.0"
    fi
    info "Resuming from Wagtail $START_FROM (skipping earlier steps)"
fi

for i in "${!VERSIONS[@]}"; do
    if [[ $i -lt $START_IDX ]]; then
        continue
    fi

    VER="${VERSIONS[$i]}"
    CONSTRAINT="${CONSTRAINTS[$i]}"
    MSG="${MESSAGES[$i]}"

    step "$MSG"

    # Install
    info "Installing wagtail$CONSTRAINT ..."
    run "$PIP_BIN" install "wagtail$CONSTRAINT"

    # Verify installed version
    if [[ "$DRY_RUN" == false ]]; then
        INSTALLED=$("$PYTHON_BIN" -c "import wagtail; print(wagtail.VERSION_STRING)" 2>/dev/null || echo "unknown")
        info "Installed: wagtail $INSTALLED"
    fi

    # Run system check
    info "Running Django system checks..."
    run manage check

    # Run migrations
    info "Applying migrations..."
    run manage migrate

    # Make migrations (in case Wagtail added new ones you need to account for)
    info "Checking for required new migrations..."
    if [[ "$DRY_RUN" == false ]]; then
        NEW_MIGRATIONS=$(manage makemigrations --check --dry-run 2>&1 || true)
        if echo "$NEW_MIGRATIONS" | grep -q "No changes detected"; then
            ok "No new migrations needed"
        else
            warn "New migrations detected — you may need to run makemigrations:"
            echo "$NEW_MIGRATIONS"
        fi
    fi

    # Run tests
    if [[ "$SKIP_TESTS" == true ]]; then
        warn "Skipping test suite (--skip-tests)"
    else
        info "Running test suite..."
        set +e
        run env MP_PROJECT_CONFIG='config.wcoa.ini' "$PYTHON_BIN" -W error::DeprecationWarning "$MANAGE_PATH" test
        TEST_STATUS=$?
        set -e
        if [[ $TEST_STATUS -ne 0 ]]; then
            error "Tests failed after upgrading to $VER (exit code $TEST_STATUS)."
            error "Fix the failures before proceeding to the next version."
            UPGRADE_OK=false
            die "Stopping upgrade at $VER due to test failures."
        fi
        ok "Tests passed on wagtail $VER"
    fi

    # Checkpoint
    ok "Wagtail $VER step complete"
    if command -v git &>/dev/null && git rev-parse --is-inside-work-tree &>/dev/null; then
        if [[ "$DRY_RUN" == false ]]; then
            info "Suggestion: git add requirements*.txt && git commit -m 'chore: upgrade wagtail to $VER'"
        fi
    fi

    hr
done

# =============================================================================
# SECTION 4 — BREAKING CHANGES AUDIT
# Only relevant once we're at 7.0 (or resuming from there)
# =============================================================================
step "BREAKING CHANGES AUDIT (Wagtail 6.1 → 7.0)"

info "Scanning codebase for known deprecated/removed patterns..."

# Helper: search and record findings
check_pattern() {
    local LABEL="$1"
    local PATTERN="$2"
    local NOTE="$3"
    local EXTRA_ARGS="${4:---include=*.py}"

    MATCHES=$(grep -r "$PATTERN" . \
        --exclude-dir=.git \
        --exclude-dir=__pycache__ \
        --exclude-dir=node_modules \
        --exclude-dir=".venv" \
        --exclude-dir="venv" \
        $EXTRA_ARGS \
        -l 2>/dev/null || true)

    if [[ -n "$MATCHES" ]]; then
        warn "[$LABEL] Found in:"
        echo "$MATCHES" | while read -r f; do
            log "    $f"
            grep -n "$PATTERN" "$f" | while read -r line; do
                log "      $line"
            done
        done
        warn "  → $NOTE"
        AUDIT_ISSUES+=("$LABEL")
    else
        ok "[$LABEL] Not found — nothing to do"
    fi
}

# ── Removed settings ──────────────────────────────────────────────────────────
check_pattern \
    "WAGTAIL_AUTO_UPDATE_PREVIEW" \
    "WAGTAIL_AUTO_UPDATE_PREVIEW\b" \
    "Replace with: WAGTAIL_AUTO_UPDATE_PREVIEW_INTERVAL = 0 (to disable)"

check_pattern \
    "PASSWORD_REQUIRED_TEMPLATE (bare)" \
    "^PASSWORD_REQUIRED_TEMPLATE\s*=" \
    "Replace with: WAGTAIL_PASSWORD_REQUIRED_TEMPLATE" \
    "--include=*.py"

check_pattern \
    "DOCUMENT_PASSWORD_REQUIRED_TEMPLATE (bare)" \
    "^DOCUMENT_PASSWORD_REQUIRED_TEMPLATE\s*=" \
    "Replace with: WAGTAILDOCS_PASSWORD_REQUIRED_TEMPLATE" \
    "--include=*.py"

# ── Removed user form settings ────────────────────────────────────────────────
check_pattern \
    "WAGTAIL_USER_EDIT_FORM" \
    "WAGTAIL_USER_EDIT_FORM" \
    "Removed — override UserViewSet.get_form_class() instead"

check_pattern \
    "WAGTAIL_USER_CREATION_FORM" \
    "WAGTAIL_USER_CREATION_FORM" \
    "Removed — override UserViewSet.get_form_class() instead"

check_pattern \
    "WAGTAIL_USER_CUSTOM_FIELDS" \
    "WAGTAIL_USER_CUSTOM_FIELDS" \
    "Removed — override UserViewSet.get_form_class() instead"

# ── Renamed tag settings (soft-deprecated but flag them) ─────────────────────
check_pattern \
    "TAG_LIMIT (bare, should be WAGTAIL_TAG_LIMIT)" \
    "^TAG_LIMIT\s*=" \
    "Rename to: WAGTAIL_TAG_LIMIT (old name works for now, but will be removed)"

check_pattern \
    "TAG_SPACES_ALLOWED (bare, should be WAGTAIL_TAG_SPACES_ALLOWED)" \
    "^TAG_SPACES_ALLOWED\s*=" \
    "Rename to: WAGTAIL_TAG_SPACES_ALLOWED (old name works for now, but will be removed)"

# ── classnames kwarg ─────────────────────────────────────────────────────────
check_pattern \
    "classnames= kwarg" \
    "classnames=" \
    "Rename to: classname= (without the 's')"

# ── Non-nullable non-text fields that may block draft saves ──────────────────
info ""
info "Checking for non-nullable non-text fields (may block draft saving in 7.0)..."
info "The following field types require null=True to allow blank draft saves:"
info "  IntegerField, FloatField, DecimalField, DateField, DateTimeField, TimeField,"
info "  BooleanField, ForeignKey, OneToOneField, ManyToManyField"
info ""

NON_TEXT_FIELDS=$(grep -rn \
    -e "models\.IntegerField\|models\.FloatField\|models\.DecimalField" \
    -e "models\.DateField\|models\.DateTimeField\|models\.TimeField" \
    -e "models\.ForeignKey\|models\.OneToOneField" \
    --include="*.py" \
    --exclude-dir=.git \
    --exclude-dir=migrations \
    --exclude-dir=__pycache__ \
    . 2>/dev/null | grep -v "null=True" | grep -v "#" || true)

if [[ -n "$NON_TEXT_FIELDS" ]]; then
    warn "[NON-TEXT FIELDS WITHOUT null=True] These may block draft saves if they are required on publish:"
    echo "$NON_TEXT_FIELDS" | while read -r line; do
        log "    $line"
    done
    warn "  → Review each field: add null=True if you want drafts to be saveable with a blank value."
    warn "  → Add blank=True alongside null=True to control publish-time validation separately."
    AUDIT_ISSUES+=("Non-nullable non-text fields — manual review required")
else
    ok "[NON-TEXT FIELDS] No obvious cases found (review your Page/Snippet models manually to be sure)"
fi

hr

# =============================================================================
# SECTION 5 — FINAL SUMMARY
# =============================================================================
step "SUMMARY"

log ""
if [[ "$UPGRADE_OK" == true ]]; then
    ok "All version steps completed successfully"
else
    error "Upgrade encountered errors — check the log above"
fi

log ""
if [[ ${#AUDIT_ISSUES[@]} -eq 0 ]]; then
    ok "Breaking changes audit: no issues found"
else
    warn "Breaking changes audit: ${#AUDIT_ISSUES[@]} area(s) need attention:"
    for issue in "${AUDIT_ISSUES[@]}"; do
        warn "  • $issue"
    done
fi

log ""
log "${BOLD}Recommended next steps:${NC}"
log "  1. Review any audit warnings above and update your code"
log "  2. If any models needed null=True added, run: python manage.py makemigrations"
log "  3. Run the full test suite one final time: python manage.py test"
log "  4. Deploy to staging with a copy of production data and test manually"
log "  5. Check the Wagtail admin: draft saves, snippet menus, user management flows"
log ""
log "${BOLD}References:${NC}"
log "  Release notes:  https://docs.wagtail.org/en/stable/releases/7.0.html"
log "  Upgrade guide:  https://docs.wagtail.org/en/stable/releases/upgrading.html"
log ""

if [[ "$DRY_RUN" == true ]]; then
    warn "This was a DRY RUN — no changes were made to your environment."
fi
