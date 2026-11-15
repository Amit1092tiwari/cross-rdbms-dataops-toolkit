#!/usr/bin/env bash
# ==============================================================================
# Data Validation Framework (DVF) Bash Runner
# Lightweight runner for CI/CD and Batch pipelines using standard database CLIs.
# Returns: 0 on PASS, 1 on FAIL
# ==============================================================================
set -euo pipefail

PLATFORM="${1:-}"
SQL_FILE="${2:-}"
DB_NAME="${3:-${DB_NAME:-}}"
DB_HOST="${4:-${DB_HOST:-localhost}}"
DB_USER="${5:-${DB_USER:-}}"

if [[ -z "$PLATFORM" || -z "$SQL_FILE" || -z "$DB_NAME" ]]; then
  echo "Usage: $0 <postgresql|mysql|mssql> <path/to/sql_file> <db_name> [db_host] [db_user]"
  exit 1
fi

if [[ ! -f "$SQL_FILE" ]]; then
  echo "[ERROR] SQL file not found: $SQL_FILE" >&2
  exit 1
fi

TMP_OUT=$(mktemp)
trap 'rm -f "$TMP_OUT"' EXIT

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Executing $SQL_FILE against $PLATFORM database '$DB_NAME'..."

case "$PLATFORM" in
  postgresql)
    psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f "$SQL_FILE" -A -F $'\t' > "$TMP_OUT" 2>&1
    ;;
  mysql)
    mysql -h "$DB_HOST" -u "$DB_USER" "$DB_NAME" --batch < "$SQL_FILE" > "$TMP_OUT" 2>&1
    ;;
  mssql)
    sqlcmd -S "$DB_HOST" -d "$DB_NAME" -U "$DB_USER" -i "$SQL_FILE" -s $'\t' -W > "$TMP_OUT" 2>&1
    ;;
  *)
    echo "[ERROR] Unsupported platform: $PLATFORM" >&2
    exit 1
    ;;
esac

# Evaluate Results
FAIL_COUNT=$(grep -cE $'\tFAIL\t|  FAIL  ' "$TMP_OUT" || true)
PASS_COUNT=$(grep -cE $'\tP\t|  P  ' "$TMP_OUT" || true)
WARN_COUNT=$(grep -cE $'\tWARN\t|  WARN  ' "$TMP_OUT" || true)

echo "=================================================="
echo "DVF EXECUTION SUMMARY"
echo "=================================================="
echo "Passed   : $PASS_COUNT"
echo "Failed   : $FAIL_COUNT"
echo "Warnings : $WARN_COUNT"
echo "=================================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  echo "❌ FAILED TESTS DETECTED:"
  grep -E $'\tFAIL\t|  FAIL  ' "$TMP_OUT"
  echo ">>> PIPELINE RESULT: FAILED <<<"
  exit 1
else
  echo ">>> PIPELINE RESULT: PASSED <<<"
  exit 0
fi
