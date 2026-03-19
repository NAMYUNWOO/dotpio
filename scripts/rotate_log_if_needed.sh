#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/rotate_log_if_needed.sh <log-path> [max-size-mb]" >&2
  exit 1
fi

LOG_PATH="$1"
MAX_SIZE_MB="${2:-20}"

if ! [[ "$MAX_SIZE_MB" =~ ^[0-9]+$ ]] || [[ "$MAX_SIZE_MB" -le 0 ]]; then
  echo "[ERROR] max-size-mb must be a positive integer" >&2
  exit 1
fi

if [[ ! -f "$LOG_PATH" ]]; then
  exit 0
fi

MAX_BYTES=$((MAX_SIZE_MB * 1024 * 1024))
CURRENT_BYTES=$(wc -c < "$LOG_PATH")

if (( CURRENT_BYTES < MAX_BYTES )); then
  exit 0
fi

TS="$(date '+%Y%m%d_%H%M%S')"
ROTATED_PATH="${LOG_PATH}.${TS}"

mv "$LOG_PATH" "$ROTATED_PATH"
: > "$LOG_PATH"

echo "[log-rotate] rotated ${LOG_PATH} -> ${ROTATED_PATH} (size=${CURRENT_BYTES} bytes, threshold=${MAX_BYTES} bytes)"
