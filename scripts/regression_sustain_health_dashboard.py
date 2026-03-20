#!/usr/bin/env python3
"""Regression check for sustain health dashboard markdown/json generation."""
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
        out_json = tmp / "dashboard.json"

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
        required_md = [
            "# DOTPIO Sustain Health Dashboard",
            "Overall: **GREEN**",
            "Trend: **stable**",
            "## Regression Risk",
            "Score: **5 / 100**",
            "Threshold alert: **OK**",
            "Top drivers:",
            "trendStable: +5 (Trend classification is stable)",
            "decision=NO_CURVE_CHANGE",
            "weeklyEvents=42",
            "CRON_TZ: Asia/Seoul",
            "Delta events: 3",
        ]
        for token in required_md:
            if token not in text:
                raise AssertionError(f"Missing expected dashboard token: {token}")

        subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--format",
                "json",
                "--pretty",
                "--snapshot-json",
                str(snapshot),
                "--anti-exploit-json",
                str(anti),
                "--audit-json",
                str(audit),
                "--out-json",
                str(out_json),
            ],
            check=True,
            cwd=ROOT,
        )
        json_text = out_json.read_text(encoding="utf-8")
        if "\n  \"overall\"" not in json_text:
            raise AssertionError("Pretty JSON indentation missing from dashboard output")
        payload = json.loads(json_text)
        if payload.get("overall", {}).get("tier") != "GREEN":
            raise AssertionError("Unexpected overall tier in JSON dashboard output")
        if payload.get("overall", {}).get("trend") != "stable":
            raise AssertionError("Unexpected trend classification in JSON dashboard output")
        if payload.get("schedulerPolicy", {}).get("tz") != "Asia/Seoul":
            raise AssertionError("Scheduler policy fields missing from JSON dashboard output")
        risk = payload.get("regressionRisk", {})
        if risk.get("score") != 5 or risk.get("level") != "LOW" or risk.get("alert") != "OK":
            raise AssertionError("Regression risk score payload mismatch")
        top_drivers = risk.get("topDrivers", [])
        if not top_drivers or top_drivers[0].get("name") != "trendStable" or top_drivers[0].get("points") != 5:
            raise AssertionError("Expected trendStable top driver in regression risk payload")

        bad = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--pretty",
                "--snapshot-json",
                str(snapshot),
                "--anti-exploit-json",
                str(anti),
                "--audit-json",
                str(audit),
                "--out-md",
                str(out_md),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if bad.returncode == 0:
            raise AssertionError("Expected --pretty without --format json to fail")

    print("[PASS] sustain health dashboard regression validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
