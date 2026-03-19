#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 4 ]]; then
  echo "Usage: bash scripts/rotate_log_if_needed.sh <log-path> [max-size-mb] [retain-rotated] [max-age-days]" >&2
  exit 1
fi

LOG_PATH="$1"
MAX_SIZE_MB="${2:-20}"
RETAIN_ROTATED="${3:-5}"
MAX_AGE_DAYS="${4:-0}"

if ! [[ "$MAX_SIZE_MB" =~ ^[0-9]+$ ]] || [[ "$MAX_SIZE_MB" -le 0 ]]; then
  echo "[ERROR] max-size-mb must be a positive integer" >&2
  exit 1
fi
if ! [[ "$RETAIN_ROTATED" =~ ^[0-9]+$ ]]; then
  echo "[ERROR] retain-rotated must be a non-negative integer" >&2
  exit 1
fi
if ! [[ "$MAX_AGE_DAYS" =~ ^[0-9]+$ ]]; then
  echo "[ERROR] max-age-days must be a non-negative integer" >&2
  exit 1
fi

if [[ ! -f "$LOG_PATH" ]]; then
  exit 0
fi

MAX_BYTES=$((MAX_SIZE_MB * 1024 * 1024))
CURRENT_BYTES=$(wc -c < "$LOG_PATH")

if (( CURRENT_BYTES >= MAX_BYTES )); then
  TS="$(date '+%Y%m%d_%H%M%S')"
  ROTATED_PATH="${LOG_PATH}.${TS}"

  mv "$LOG_PATH" "$ROTATED_PATH"
  : > "$LOG_PATH"

  echo "[log-rotate] rotated ${LOG_PATH} -> ${ROTATED_PATH} (size=${CURRENT_BYTES} bytes, threshold=${MAX_BYTES} bytes)"
fi

shopt -s nullglob
rotated_logs=("${LOG_PATH}".*)
shopt -u nullglob

if (( ${#rotated_logs[@]} == 0 )); then
  exit 0
fi

pruned_by_age=0
if (( MAX_AGE_DAYS > 0 )); then
  age_minutes=$((MAX_AGE_DAYS * 24 * 60))
  while IFS= read -r aged_file; do
    [[ -z "${aged_file}" ]] && continue
    rm -f -- "${aged_file}"
    ((pruned_by_age+=1))
  done < <(find "$(dirname "$LOG_PATH")" -maxdepth 1 -type f -name "$(basename "$LOG_PATH").*" -mmin +"${age_minutes}" -print 2>/dev/null)

  if (( pruned_by_age > 0 )); then
    echo "[log-rotate] pruned ${pruned_by_age} rotated logs by age (max-age-days=${MAX_AGE_DAYS})"
  fi

  shopt -s nullglob
  rotated_logs=("${LOG_PATH}".*)
  shopt -u nullglob
  if (( ${#rotated_logs[@]} == 0 )); then
    exit 0
  fi
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
