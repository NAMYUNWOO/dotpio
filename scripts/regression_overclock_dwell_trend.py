#!/usr/bin/env python3
"""Regression checks for overclock multi-run dwell trend combiner."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "overclock_dwell_trend.py"


def write_sample(path: Path, generated_at: str, low: int, mid: int, high: int) -> None:
    payload = {
        "generatedAt": generated_at,
        "map": "map_03",
        "totalExposureSeconds": low + mid + high,
        "dwellBuckets": {"LOW": low, "MID": mid, "HIGH": high},
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="overclock-dwell-trend-reg-") as td:
        root = Path(td)
        inp = root / "playtests"
        out_json = root / "trend.json"
        out_md = root / "trend.md"
        inp.mkdir(parents=True, exist_ok=True)

        write_sample(inp / "overclock_dwell_buckets_run_20260320_100000.json", "2026-03-20T10:00:00Z", 3, 6, 9)
        write_sample(inp / "overclock_dwell_buckets_run_20260320_110000.json", "2026-03-20T11:00:00Z", 4, 8, 10)
        write_sample(inp / "overclock_dwell_buckets_run_20260320_120000.json", "2026-03-20T12:00:00Z", 7, 9, 12)

        subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--input-dir",
                str(inp),
                "--runs",
                "2",
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )

        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["status"] == "ok", payload
        assert payload["windowRuns"] == 2, payload
        assert payload["medians"]["LOW"] == 6, payload
        assert payload["medians"]["MID"] == 8, payload
        assert payload["medians"]["HIGH"] == 11, payload
        assert payload["medians"]["TOTAL"] == 25, payload
        assert len(payload["runs"]) == 2, payload
        assert payload["volatility"]["level"] == "STEADY", payload
        assert payload["volatility"]["token"] == "VOL:STEADY", payload

        md_text = out_md.read_text(encoding="utf-8")
        assert "Window runs: 2/2" in md_text
        assert "Median LOW/MID/HIGH/TOTAL: 6 / 8 / 11 / 25" in md_text
        assert "Volatility: VOL:STEADY" in md_text

        write_sample(inp / "overclock_dwell_buckets_run_20260320_130000.json", "2026-03-20T13:00:00Z", 2, 2, 40)
        subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--input-dir",
                str(inp),
                "--runs",
                "2",
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )

        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["volatility"]["level"] == "SWING", payload
        assert payload["volatility"]["token"] == "VOL:SWING", payload

        md_text = out_md.read_text(encoding="utf-8")
        assert "Volatility: VOL:SWING" in md_text

    print("[PASS] overclock dwell trend regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
