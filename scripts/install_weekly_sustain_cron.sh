#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNNER_REL="scripts/run_weekly_sustain.sh"
RUNNER_PATH="${REPO_ROOT}/${RUNNER_REL}"
DEFAULT_LOG_PATH="${REPO_ROOT}/logs/weekly_sustain_cron.log"
LOG_PATH="${SUSTAIN_CRON_LOG_PATH:-$DEFAULT_LOG_PATH}"
MAX_LOG_SIZE_MB="${SUSTAIN_CRON_MAX_LOG_SIZE_MB:-20}"
RETAIN_ROTATED_LOGS="${SUSTAIN_CRON_RETAIN_ROTATED_LOGS:-5}"
MAX_ROTATED_AGE_DAYS="${SUSTAIN_CRON_MAX_ROTATED_AGE_DAYS:-0}"

SCHEDULE_MINUTE="${SUSTAIN_CRON_MINUTE:-0}"
SCHEDULE_HOUR="${SUSTAIN_CRON_HOUR:-9}"
SCHEDULE_DOW="${SUSTAIN_CRON_DOW:-1}" # 1 = Monday
TZ_VALUE="${SUSTAIN_CRON_TZ:-Asia/Seoul}"
APPLY=0
CRONTAB_BIN="${CRONTAB_BIN:-crontab}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/install_weekly_sustain_cron.sh [--apply] [--minute N] [--hour N] [--dow N] [--tz Zone] [--log-path Path] [--max-log-size-mb N] [--retain-rotated-logs N] [--max-rotated-age-days N]

Default schedule:
  Every Monday 09:00 (Asia/Seoul)

Behavior:
  - Without --apply: prints the cron line and current matching entries only (dry-run).
  - With --apply: upserts one managed cron entry for scripts/run_weekly_sustain.sh.

Environment override (optional):
  SUSTAIN_CRON_MINUTE, SUSTAIN_CRON_HOUR, SUSTAIN_CRON_DOW, SUSTAIN_CRON_TZ,
  SUSTAIN_CRON_LOG_PATH, SUSTAIN_CRON_MAX_LOG_SIZE_MB, SUSTAIN_CRON_RETAIN_ROTATED_LOGS,
  SUSTAIN_CRON_MAX_ROTATED_AGE_DAYS, CRONTAB_BIN
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      APPLY=1
      shift
      ;;
    --minute)
      SCHEDULE_MINUTE="$2"
      shift 2
      ;;
    --hour)
      SCHEDULE_HOUR="$2"
      shift 2
      ;;
    --dow)
      SCHEDULE_DOW="$2"
      shift 2
      ;;
    --tz)
      TZ_VALUE="$2"
      shift 2
      ;;
    --log-path)
      LOG_PATH="$2"
      shift 2
      ;;
    --max-log-size-mb)
      MAX_LOG_SIZE_MB="$2"
      shift 2
      ;;
    --retain-rotated-logs)
      RETAIN_ROTATED_LOGS="$2"
      shift 2
      ;;
    --max-rotated-age-days)
      MAX_ROTATED_AGE_DAYS="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ! -x "$RUNNER_PATH" ]]; then
  echo "[ERROR] Missing executable runner: $RUNNER_PATH" >&2
  echo "Run: chmod +x $RUNNER_REL" >&2
  exit 1
fi

ROTATE_PATH="${REPO_ROOT}/scripts/rotate_log_if_needed.sh"
if [[ ! -x "$ROTATE_PATH" ]]; then
  echo "[ERROR] Missing executable log rotate helper: $ROTATE_PATH" >&2
  echo "Run: chmod +x scripts/rotate_log_if_needed.sh" >&2
  exit 1
fi

if ! [[ "$SCHEDULE_MINUTE" =~ ^([0-5]?[0-9])$ ]]; then
  echo "[ERROR] --minute must be 0-59" >&2
  exit 1
fi
if ! [[ "$SCHEDULE_HOUR" =~ ^([01]?[0-9]|2[0-3])$ ]]; then
  echo "[ERROR] --hour must be 0-23" >&2
  exit 1
fi
if ! [[ "$SCHEDULE_DOW" =~ ^[0-7]$ ]]; then
  echo "[ERROR] --dow must be 0-7 (0/7=Sunday, 1=Monday)" >&2
  exit 1
fi

if [[ -z "$LOG_PATH" ]]; then
  echo "[ERROR] --log-path must be non-empty" >&2
  exit 1
fi
if ! [[ "$MAX_LOG_SIZE_MB" =~ ^[0-9]+$ ]] || [[ "$MAX_LOG_SIZE_MB" -le 0 ]]; then
  echo "[ERROR] --max-log-size-mb must be a positive integer" >&2
  exit 1
fi
if ! [[ "$RETAIN_ROTATED_LOGS" =~ ^[0-9]+$ ]]; then
  echo "[ERROR] --retain-rotated-logs must be a non-negative integer" >&2
  exit 1
fi
if ! [[ "$MAX_ROTATED_AGE_DAYS" =~ ^[0-9]+$ ]]; then
  echo "[ERROR] --max-rotated-age-days must be a non-negative integer" >&2
  exit 1
fi

if ! command -v "$CRONTAB_BIN" >/dev/null 2>&1; then
  echo "[ERROR] crontab binary not found: $CRONTAB_BIN" >&2
  exit 1
fi

MARKER="# DOTPIO_WEEKLY_SUSTAIN"
ROTATE_REL="scripts/rotate_log_if_needed.sh"
CRON_CMD="cd ${REPO_ROOT} && bash ${ROTATE_REL} ${LOG_PATH} ${MAX_LOG_SIZE_MB} ${RETAIN_ROTATED_LOGS} ${MAX_ROTATED_AGE_DAYS} && bash ${RUNNER_REL} >> ${LOG_PATH} 2>&1"
CRON_LINE="CRON_TZ=${TZ_VALUE} ${SCHEDULE_MINUTE} ${SCHEDULE_HOUR} * * ${SCHEDULE_DOW} ${CRON_CMD} ${MARKER}"

CURRENT_CRON="$($CRONTAB_BIN -l 2>/dev/null || true)"
EXISTING_MATCH="$(printf '%s\n' "$CURRENT_CRON" | grep -F "$MARKER" || true)"

echo "[INFO] Proposed managed cron entry:"
echo "$CRON_LINE"

if [[ -n "$EXISTING_MATCH" ]]; then
  echo "[INFO] Existing managed entries:"
  printf '%s\n' "$EXISTING_MATCH"
else
  echo "[INFO] Existing managed entries: none"
fi

if [[ "$APPLY" -eq 0 ]]; then
  echo "[DRY-RUN] No changes applied. Re-run with --apply to upsert."
  exit 0
fi

UPDATED_CRON="$(printf '%s\n' "$CURRENT_CRON" | grep -vF "$MARKER" || true)"
UPDATED_CRON="${UPDATED_CRON}"$'\n'"${CRON_LINE}"$'\n'

printf '%s' "$UPDATED_CRON" | "$CRONTAB_BIN" -

echo "[OK] Managed weekly sustain cron upserted."
"$CRONTAB_BIN" -l | grep -F "$MARKER" || true
