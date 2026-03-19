#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[weekly-sustain] $(date '+%Y-%m-%d %H:%M:%S %Z') starting"

lua scripts/economy_anti_exploit_report.lua
python3 scripts/economy_weekly_snapshot.py
python3 scripts/regression_weekly_snapshot.py

AUDIT_JSON="logs/weekly_sustain_cron_audit.json"
if bash scripts/audit_weekly_sustain_cron.sh --format json >"$AUDIT_JSON" 2>/dev/null; then
  echo "[weekly-sustain] cron audit captured: $AUDIT_JSON"
else
  rm -f "$AUDIT_JSON"
  echo "[weekly-sustain] cron audit unavailable (managed entry missing); dashboard will mark scheduler signal as warning"
fi

python3 scripts/sustain_health_dashboard.py --audit-json "$AUDIT_JSON"
python3 scripts/regression_sustain_health_dashboard.py

echo "[weekly-sustain] done"
echo "- logs/economy_anti_exploit_report.md"
echo "- logs/economy_anti_exploit_report.json"
echo "- logs/economy_weekly_snapshot.md"
echo "- logs/economy_weekly_snapshot.json"
echo "- logs/sustain_health_dashboard.md"
