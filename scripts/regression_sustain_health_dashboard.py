#!/usr/bin/env python3
"""Regression check for sustain health dashboard markdown generation."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sustain_health_dashboard.py"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="sustain-dashboard-regression-") as tmpdir:
        tmp = Path(tmpdir)

        snapshot = tmp / "snapshot.json"
        anti = tmp / "anti.json"
        audit = tmp / "audit.json"
        out_md = tmp / "dashboard.md"

        snapshot.write_text(
            json.dumps(
                {
                    "windowStart": "2026-03-12T00:00:00Z",
                    "windowEnd": "2026-03-19T00:00:00Z",
                    "telemetryEventCount": 42,
                    "totalSrlSpent": 128,
                    "suspiciousCount": 0,
                    "decision": "NO_CURVE_CHANGE",
                    "decisionRationale": "No suspicious windows",
                    "deltaFromPrevious": {"telemetryEventCount": 3, "totalSrlSpent": -10},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        anti.write_text(json.dumps({"suspiciousCount": 0}), encoding="utf-8")
        audit.write_text(
            json.dumps(
                {
                    "status": "ok",
                    "tz": "Asia/Seoul",
                    "minute": 30,
                    "hour": 9,
                    "dow": 1,
                    "log_path": "logs/weekly_sustain.log",
                    "max_log_size_mb": 20,
                    "retain_rotated_logs": 6,
                    "max_rotated_age_days": 21,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--snapshot-json",
                str(snapshot),
                "--anti-exploit-json",
                str(anti),
                "--audit-json",
                str(audit),
                "--out-md",
                str(out_md),
            ],
            check=True,
            cwd=ROOT,
        )

        text = out_md.read_text(encoding="utf-8")
        required = [
            "# DOTPIO Sustain Health Dashboard",
            "Overall: **GREEN**",
            "decision=NO_CURVE_CHANGE",
            "weeklyEvents=42",
            "CRON_TZ: Asia/Seoul",
            "Delta events: 3",
        ]
        for token in required:
            if token not in text:
                raise AssertionError(f"Missing expected dashboard token: {token}")

    print("[PASS] sustain health dashboard regression validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
