#!/usr/bin/env python3
"""Regression check for weekly snapshot schema + delta fields."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_SCRIPT = ROOT / "scripts" / "economy_weekly_snapshot.py"
TELEMETRY = ROOT / "logs" / "economy_telemetry.ndjson"
ANTI = ROOT / "logs" / "economy_anti_exploit_report.json"


def run_once(out_md: Path, out_json: Path) -> dict:
    subprocess.run(
        [
            "python3",
            str(SNAPSHOT_SCRIPT),
            "--telemetry",
            str(TELEMETRY),
            "--anti-exploit",
            str(ANTI),
            "--out-md",
            str(out_md),
            "--out-json",
            str(out_json),
        ],
        check=True,
        cwd=ROOT,
    )
    return json.loads(out_json.read_text(encoding="utf-8"))


def assert_has_keys(payload: dict) -> None:
    required = [
        "telemetryEventCount",
        "totalSrlSpent",
        "deltaFromPrevious",
        "comparedToPrevious",
        "decision",
        "laneCadence",
    ]
    for key in required:
        if key not in payload:
            raise AssertionError(f"Missing key: {key}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="weekly-snapshot-regression-") as tmpdir:
        tmp = Path(tmpdir)
        out_md = tmp / "snapshot.md"
        out_json = tmp / "snapshot.json"

        first = run_once(out_md, out_json)
        assert_has_keys(first)
        if first["comparedToPrevious"] is not False:
            raise AssertionError("First run should be baseline (comparedToPrevious=false)")
        if first["deltaFromPrevious"]["telemetryEventCount"] is not None:
            raise AssertionError("First run delta telemetryEventCount should be null")
        if first["deltaFromPrevious"]["totalSrlSpent"] is not None:
            raise AssertionError("First run delta totalSrlSpent should be null")

        second = run_once(out_md, out_json)
        assert_has_keys(second)
        if second["comparedToPrevious"] is not True:
            raise AssertionError("Second run should compare against previous snapshot")

        lane_cadence = second["laneCadence"]
        if lane_cadence.get("status") not in {"OK", "GAP"}:
            raise AssertionError(f"Unexpected lane cadence status: {lane_cadence.get('status')}")
        if lane_cadence.get("token") not in {"LANE CADENCE:OK", "LANE CADENCE:GAP"}:
            raise AssertionError(f"Unexpected lane cadence token: {lane_cadence.get('token')}")
        buckets = lane_cadence.get("bucketCoverage", {})
        for expected in ("combat-vfx", "design-world", "systems-ops"):
            if expected not in buckets:
                raise AssertionError(f"Missing lane cadence bucket: {expected}")
        lane_gap_detail = lane_cadence.get("laneGapDetail")
        if not isinstance(lane_gap_detail, str) or "combat/vfx" not in lane_gap_detail:
            raise AssertionError(f"Unexpected lane gap detail: {lane_gap_detail}")
        if "combatVfxLastTouchAgeHours" not in lane_cadence:
            raise AssertionError("Missing combatVfxLastTouchAgeHours in lane cadence payload")
        if "sourceLatestAgeHours" not in lane_cadence:
            raise AssertionError("Missing sourceLatestAgeHours in lane cadence payload")

        md_text = out_md.read_text(encoding="utf-8")
        if "LANE GAP DETAIL:" not in md_text:
            raise AssertionError("Missing LANE GAP DETAIL line in markdown snapshot")

        delta = second["deltaFromPrevious"]
        if delta["telemetryEventCount"] != 0:
            raise AssertionError(f"Expected zero telemetryEventCount delta, got {delta['telemetryEventCount']}")
        if delta["totalSrlSpent"] != 0:
            raise AssertionError(f"Expected zero totalSrlSpent delta, got {delta['totalSrlSpent']}")

    print("[PASS] weekly snapshot regression validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
