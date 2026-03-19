#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[weekly-sustain] $(date '+%Y-%m-%d %H:%M:%S %Z') starting"

lua scripts/economy_anti_exploit_report.lua
python3 scripts/economy_weekly_snapshot.py
python3 scripts/regression_weekly_snapshot.py

echo "[weekly-sustain] done"
echo "- logs/economy_anti_exploit_report.md"
echo "- logs/economy_anti_exploit_report.json"
echo "- logs/economy_weekly_snapshot.md"
echo "- logs/economy_weekly_snapshot.json"
