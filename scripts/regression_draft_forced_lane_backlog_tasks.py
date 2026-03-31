#!/usr/bin/env python3
"""Regression guardrail for forced-lane backlog template copy-pack alias schema."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "draft_forced_lane_backlog_tasks.py"
FIXTURE = ROOT / "logs" / "weekly_lane_coverage_guardrail_over_cap_fixture.json"


def run_once(json_out: Path, md_out: Path, include_compat_row: bool = False) -> dict:
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--guardrail-json",
        str(FIXTURE),
        "--json-out",
        str(json_out),
        "--md-out",
        str(md_out),
    ]
    if include_compat_row:
        cmd.append("--include-copy-pack-compat-row")
    subprocess.run(cmd, check=True, cwd=ROOT)
    return json.loads(json_out.read_text(encoding="utf-8"))


def assert_schema(payload: dict) -> None:
    assert payload["status"] == "over-cap", "expected over-cap fixture"
    assert payload["gameplayCopyPack"] in {"steady", "spike"}
    assert payload["gameplayCopyPackAlias"] in {"ST", "SP"}

    templates = payload.get("templates", [])
    assert templates, "expected at least one forced-lane template"

    gameplay_template = next((t for t in templates if t.get("copyPack")), None)
    assert gameplay_template is not None, "expected gameplay template with copy pack"
    assert gameplay_template["copyPack"] in {"steady", "spike"}
    assert gameplay_template["copyPackAlias"] in {"ST", "SP"}

    expected_alias = {"steady": "ST", "spike": "SP"}[gameplay_template["copyPack"]]
    assert gameplay_template["copyPackAlias"] == expected_alias

    payload_alias = {"steady": "ST", "spike": "SP"}[payload["gameplayCopyPack"]]
    assert payload["gameplayCopyPackAlias"] == payload_alias


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="regression_draft_forced_lane_") as tmp:
        tmp_path = Path(tmp)

        first_json = tmp_path / "first.json"
        first_md = tmp_path / "first.md"
        second_json = tmp_path / "second.json"
        second_md = tmp_path / "second.md"

        first_payload = run_once(first_json, first_md)
        second_payload = run_once(second_json, second_md)

        compat_json = tmp_path / "compat.json"
        compat_md = tmp_path / "compat.md"
        compat_payload = run_once(compat_json, compat_md, include_compat_row=True)

        assert_schema(first_payload)
        assert_schema(second_payload)

        assert first_payload == second_payload, "payload must be deterministic across repeated runs"
        assert first_md.read_text(encoding="utf-8") == second_md.read_text(encoding="utf-8"), (
            "markdown output must be deterministic across repeated runs"
        )
        assert compat_payload == first_payload, "compat markdown row must not mutate payload schema"

        compat_text = compat_md.read_text(encoding="utf-8")
        assert "COPY PACK COMPAT:STEADY=ST|SPIKE=SP" in compat_text, (
            "expected compatibility row when compat flag enabled"
        )
        assert "COPY PACK COMPAT LEGEND:ST=STEADY|SP=SPIKE" in compat_text, (
            "expected compatibility legend row when compat flag enabled"
        )
        assert "COPY PACK COMPAT:STEADY=ST|SPIKE=SP" not in first_md.read_text(encoding="utf-8"), (
            "compatibility row must stay gated behind flag"
        )
        assert "COPY PACK COMPAT LEGEND:ST=STEADY|SP=SPIKE" not in first_md.read_text(
            encoding="utf-8"
        ), "compatibility legend row must stay gated behind flag"

    print("PASS: regression_draft_forced_lane_backlog_tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
