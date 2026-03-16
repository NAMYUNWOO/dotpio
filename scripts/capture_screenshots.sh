#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT_DIR/screenshots}"
SAVE_DIR="${LOVE_SAVE_DIR:-$HOME/.local/share/love/dotpio}"

mkdir -p "$OUT_DIR"
mkdir -p "$SAVE_DIR"

run_capture() {
  local name="$1"
  shift
  local tmpShot="__auto_${name}"
  echo "[capture] $name"
  (
    cd "$ROOT_DIR"
    rm -f "$SAVE_DIR/$tmpShot"
    env "$@" AUTO_SCREENSHOT="$tmpShot" love . >/tmp/dotpio-shot-${name}.log 2>&1
    mv "$SAVE_DIR/$tmpShot" "$OUT_DIR/$name"
  )
  echo "  -> $OUT_DIR/$name"
}

run_capture "screenshot-map04.png" \
  AUTO_START_MAP=04 \
  AUTO_START_PORTAL=03

run_capture "screenshot-inventory-dos.png" \
  AUTO_START_MAP=04 \
  AUTO_START_PORTAL=03 \
  AUTO_OPEN_INVENTORY=1

echo "Done. Screenshots written to: $OUT_DIR"
