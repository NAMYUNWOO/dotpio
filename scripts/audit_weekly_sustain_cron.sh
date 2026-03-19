#!/usr/bin/env bash
set -euo pipefail

MARKER="# DOTPIO_WEEKLY_SUSTAIN"
CRONTAB_BIN="${CRONTAB_BIN:-crontab}"
OUTPUT_FORMAT="text"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/audit_weekly_sustain_cron.sh [--crontab-bin PATH] [--format text|json]

Reads current crontab, locates the managed DOTPIO weekly sustain entry,
and prints parsed schedule + log-rotation policy fields.

Environment override:
  CRONTAB_BIN
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --crontab-bin)
      CRONTAB_BIN="$2"
      shift 2
      ;;
    --format)
      OUTPUT_FORMAT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown arg: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "[ERROR] --format must be one of: text, json" >&2
  exit 1
fi

if ! command -v "$CRONTAB_BIN" >/dev/null 2>&1; then
  echo "[ERROR] crontab binary not found: $CRONTAB_BIN" >&2
  exit 1
fi

CURRENT_CRON="$($CRONTAB_BIN -l 2>/dev/null || true)"
MATCHES="$(printf '%s\n' "$CURRENT_CRON" | grep -F "$MARKER" || true)"

if [[ -z "$MATCHES" ]]; then
  echo "[ERROR] Managed weekly sustain entry not found (${MARKER})." >&2
  exit 2
fi

match_count="$(printf '%s\n' "$MATCHES" | sed '/^$/d' | wc -l | tr -d ' ')"
if [[ "$match_count" -ne 1 ]]; then
  echo "[ERROR] Expected exactly one managed entry, found ${match_count}." >&2
  printf '%s\n' "$MATCHES" >&2
  exit 3
fi

ENTRY="$(printf '%s\n' "$MATCHES" | head -n 1)"

if [[ ! "$ENTRY" =~ ^CRON_TZ=([^[:space:]]+)[[:space:]]+([0-9]+)[[:space:]]+([0-9]+)[[:space:]]+\*[[:space:]]+\*[[:space:]]+([0-7])[[:space:]]+(.+)[[:space:]]+\#[[:space:]]DOTPIO_WEEKLY_SUSTAIN[[:space:]]*$ ]]; then
  echo "[ERROR] Managed entry format is unexpected; cannot parse schedule." >&2
  echo "entry=${ENTRY}" >&2
  exit 4
fi

TZ_VALUE="${BASH_REMATCH[1]}"
SCHEDULE_MINUTE="${BASH_REMATCH[2]}"
SCHEDULE_HOUR="${BASH_REMATCH[3]}"
SCHEDULE_DOW="${BASH_REMATCH[4]}"
CRON_CMD="${BASH_REMATCH[5]}"

if [[ ! "$CRON_CMD" =~ bash[[:space:]]+scripts/rotate_log_if_needed\.sh[[:space:]]+([^[:space:]]+)[[:space:]]+([0-9]+)[[:space:]]+([0-9]+)[[:space:]]+([0-9]+)[[:space:]]+\&\&[[:space:]]+bash[[:space:]]+scripts/run_weekly_sustain\.sh[[:space:]]+\>\>[[:space:]]+([^[:space:]]+) ]]; then
  echo "[ERROR] Managed entry found but rotate/sustain command shape is unexpected." >&2
  echo "entry=${ENTRY}" >&2
  exit 5
fi

LOG_PATH="${BASH_REMATCH[1]}"
MAX_LOG_SIZE_MB="${BASH_REMATCH[2]}"
RETAIN_ROTATED_LOGS="${BASH_REMATCH[3]}"
MAX_ROTATED_AGE_DAYS="${BASH_REMATCH[4]}"
RUNNER_LOG_PATH="${BASH_REMATCH[5]}"

if [[ "$OUTPUT_FORMAT" == "json" ]]; then
  MARKER="$MARKER" \
  TZ_VALUE="$TZ_VALUE" \
  SCHEDULE_MINUTE="$SCHEDULE_MINUTE" \
  SCHEDULE_HOUR="$SCHEDULE_HOUR" \
  SCHEDULE_DOW="$SCHEDULE_DOW" \
  LOG_PATH="$LOG_PATH" \
  MAX_LOG_SIZE_MB="$MAX_LOG_SIZE_MB" \
  RETAIN_ROTATED_LOGS="$RETAIN_ROTATED_LOGS" \
  MAX_ROTATED_AGE_DAYS="$MAX_ROTATED_AGE_DAYS" \
  RUNNER_LOG_PATH="$RUNNER_LOG_PATH" \
  ENTRY="$ENTRY" \
  python3 - <<'PY'
import json
import os

payload = {
    "status": "ok",
    "marker": os.environ["MARKER"],
    "tz": os.environ["TZ_VALUE"],
    "minute": int(os.environ["SCHEDULE_MINUTE"]),
    "hour": int(os.environ["SCHEDULE_HOUR"]),
    "dow": int(os.environ["SCHEDULE_DOW"]),
    "log_path": os.environ["LOG_PATH"],
    "max_log_size_mb": int(os.environ["MAX_LOG_SIZE_MB"]),
    "retain_rotated_logs": int(os.environ["RETAIN_ROTATED_LOGS"]),
    "max_rotated_age_days": int(os.environ["MAX_ROTATED_AGE_DAYS"]),
    "runner_log_path": os.environ["RUNNER_LOG_PATH"],
    "entry": os.environ["ENTRY"],
}
print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
PY
  exit 0
fi

echo "[OK] Managed weekly sustain entry found."
echo "tz=${TZ_VALUE}"
echo "minute=${SCHEDULE_MINUTE}"
echo "hour=${SCHEDULE_HOUR}"
echo "dow=${SCHEDULE_DOW}"
echo "log_path=${LOG_PATH}"
echo "max_log_size_mb=${MAX_LOG_SIZE_MB}"
echo "retain_rotated_logs=${RETAIN_ROTATED_LOGS}"
echo "max_rotated_age_days=${MAX_ROTATED_AGE_DAYS}"
echo "runner_log_path=${RUNNER_LOG_PATH}"
echo "entry=${ENTRY}"
