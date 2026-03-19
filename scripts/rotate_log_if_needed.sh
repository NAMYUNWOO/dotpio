#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 3 ]]; then
  echo "Usage: bash scripts/rotate_log_if_needed.sh <log-path> [max-size-mb] [retain-rotated]" >&2
  exit 1
fi

LOG_PATH="$1"
MAX_SIZE_MB="${2:-20}"
RETAIN_ROTATED="${3:-5}"

if ! [[ "$MAX_SIZE_MB" =~ ^[0-9]+$ ]] || [[ "$MAX_SIZE_MB" -le 0 ]]; then
  echo "[ERROR] max-size-mb must be a positive integer" >&2
  exit 1
fi
if ! [[ "$RETAIN_ROTATED" =~ ^[0-9]+$ ]]; then
  echo "[ERROR] retain-rotated must be a non-negative integer" >&2
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

shopt -s nullglob
rotated_logs=("${LOG_PATH}".*)
shopt -u nullglob

if (( ${#rotated_logs[@]} == 0 )); then
  exit 0
fi

IFS=$'\n' sorted_rotated_logs=($(ls -1t -- "${rotated_logs[@]}" 2>/dev/null || true))
unset IFS

if (( ${#sorted_rotated_logs[@]} <= RETAIN_ROTATED )); then
  exit 0
fi

pruned=0
for (( idx=RETAIN_ROTATED; idx<${#sorted_rotated_logs[@]}; idx++ )); do
  rm -f -- "${sorted_rotated_logs[$idx]}"
  ((pruned+=1))
done

if (( pruned > 0 )); then
  echo "[log-rotate] pruned ${pruned} rotated logs (retain=${RETAIN_ROTATED})"
fi
