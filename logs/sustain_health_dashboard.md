# DOTPIO Sustain Health Dashboard

- GeneratedAt(UTC): 2026-03-19T16:58:34.853704Z
- Overall: **YELLOW** (2/3 checks green)

## Signals
- ✅ Economy safety: decision=NO_CURVE_CHANGE, suspiciousWindows=0
- ✅ Telemetry freshness: weeklyEvents=41, totalSrlSpent=68
- ⚠️ Scheduler policy audit: status=missing

## Weekly Snapshot
- Window: 2026-03-12T13:29:45Z ~ 2026-03-19T13:29:45Z
- Decision: **NO_CURVE_CHANGE**
- Rationale: No suspicious net-positive exploit windows detected in the latest anti-exploit report.
- Delta events: 9
- Delta total SRL spent: 20

## Scheduler Policy
- Managed weekly sustain cron entry not found or audit artifact missing.

## Action
- If overall is YELLOW/ORANGE/RED: run `bash scripts/run_weekly_sustain.sh` and investigate the failing signal before next RC cut.
