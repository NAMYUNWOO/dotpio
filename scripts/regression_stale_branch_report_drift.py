#!/usr/bin/env python3
"""Regression checks for stale branch/report drift checker."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "stale_branch_report_drift_check.py"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="stale-drift-reg-") as td:
        tmp = Path(td)
        good_json = tmp / "good.json"
        good_json.write_text(json.dumps({"generatedAt": "2099-01-01T00:00:00Z"}), encoding="utf-8")

        out_json = tmp / "out.json"
        out_md = tmp / "out.md"
        run(
            [
                "python3",
                str(SCRIPT),
                "--branch-max-age-days",
                "9999",
                "--report-max-age-days",
                "9999",
                "--report-path",
                str(good_json),
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ]
        )

        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["status"] == "ok", payload
        assert payload["branch"]["ok"] is True
        assert payload["reports"][0]["ok"] is True

        old_json = tmp / "old.json"
        old_json.write_text(json.dumps({"generatedAt": "2000-01-01T00:00:00Z"}), encoding="utf-8")
        run(
            [
                "python3",
                str(SCRIPT),
                "--branch-max-age-days",
                "9999",
                "--report-max-age-days",
                "1",
                "--report-path",
                str(old_json),
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ]
        )
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["status"] == "warn", payload
        assert payload["reports"][0]["ok"] is False

    print("[PASS] stale branch/report drift regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
