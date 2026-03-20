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
python3 scripts/sustain_health_dashboard.py --format json --pretty --audit-json "$AUDIT_JSON"
python3 scripts/regression_sustain_health_dashboard.py
python3 scripts/stale_branch_report_drift_check.py
python3 scripts/regression_stale_branch_report_drift.py
python3 scripts/weekly_changelog_drift_check.py
python3 scripts/regression_weekly_changelog_drift.py
python3 scripts/weekly_portal_prompt_readability_drift.py
python3 scripts/regression_weekly_portal_prompt_readability_drift.py
python3 scripts/overclock_dwell_trend.py --runs 7
python3 scripts/regression_overclock_dwell_trend.py

echo "[weekly-sustain] done"
echo "- logs/economy_anti_exploit_report.md"
echo "- logs/economy_anti_exploit_report.json"
echo "- logs/economy_weekly_snapshot.md"
echo "- logs/economy_weekly_snapshot.json"
echo "- logs/sustain_health_dashboard.md"
echo "- logs/sustain_health_dashboard.json"
echo "- logs/stale_branch_report_drift.md"
echo "- logs/stale_branch_report_drift.json"
echo "- logs/weekly_changelog_drift.md"
echo "- logs/weekly_changelog_drift.json"
echo "- logs/weekly_portal_prompt_readability_drift.md"
echo "- logs/weekly_portal_prompt_readability_drift.json"
echo "- logs/playtests/overclock_dwell_trend.md"
echo "- logs/playtests/overclock_dwell_trend.json"
