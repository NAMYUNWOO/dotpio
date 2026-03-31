#!/usr/bin/env python3
"""Regression checks for lane-coverage guardrail trend-score alias mapping."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_lane_coverage_guardrail.py"


def run_guardrail(backlog: Path, json_out: Path, md_out: Path) -> dict:
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--backlog",
        str(backlog),
        "--max-items",
        "10",
        "--cap-ratio",
        "0.40",
        "--json-out",
        str(json_out),
        "--md-out",
        str(md_out),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)
    return json.loads(json_out.read_text(encoding="utf-8"))


def expected_alias(snapshot: dict[str, int]) -> str:
    return f"C{snapshot['CALM']}E{snapshot['EDGE']}H{snapshot['HEATED']}"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="regression_check_lane_guardrail_") as tmp:
        tmp_path = Path(tmp)
        backlog = tmp_path / "backlog.md"
        json_out = tmp_path / "guardrail.json"
        md_out = tmp_path / "guardrail.md"

        backlog.write_text(
            "\n".join(
                [
                    "# fixture",
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C and compatRowPolicySourceConfidenceTrendScoreBand:CALM",
                    "- [x] Design/World Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E and compatRowPolicySourceConfidenceTrendScoreBand:EDGE",
                    "- [x] Combat/VFX Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:H and compatRowPolicySourceConfidenceTrendScoreBand:HEATED",
                    "- [x] AI Content/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                    "- [x] UX/Systems Team: compatRowPolicySourceConfidenceTrendScoreBand:EDGE",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        report = run_guardrail(backlog, json_out, md_out)
        snapshot = report.get("trendScoreBandSnapshot")
        assert snapshot == {"CALM": 3, "EDGE": 3, "HEATED": 2}, (
            "trendScoreBandSnapshot counts must include alias/full-token matches"
        )

        alias = report.get("trendScoreBandSnapshotAlias")
        assert alias == expected_alias(snapshot), (
            "trendScoreBandSnapshotAlias must match canonical C{CALM}E{EDGE}H{HEATED} mapping"
        )

        md_text = md_out.read_text(encoding="utf-8")
        assert f"TSSB:{alias}" in md_text, "markdown output must render canonical TSSB alias"
        assert "TSSB legend (C=calm, E=edge, H=heated)" in md_text, (
            "markdown output must include compact TSSB decode microcopy row"
        )

    print("ok: trendScoreBandSnapshotAlias regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
