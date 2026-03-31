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
CHECKED_IN_JSON_FIXTURE = ROOT / "logs" / "forced_lane_task_templates_over_cap_fixture.json"
CHECKED_IN_MD_FIXTURE = ROOT / "logs" / "forced_lane_task_templates_over_cap_fixture.md"


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
    assert payload["compatRowPolicy"] in {"ALWAYS", "SPIKE_ONLY"}
    assert payload["compatRowPolicySource"] in {"COPY_PACK", "VOLATILITY_MEMORY"}
    assert payload["compatRowPolicySourceAlias"] in {"C", "V"}
    assert payload["compatRowPolicySourceConfidence"] in {"LOW", "MID", "HIGH"}
    assert payload["compatRowPolicySourceConfidenceAlias"] in {"L", "M", "H"}
    assert payload["compatRowPolicyAlias"] in {"A", "S"}

    signals = payload.get("compatRowPolicySignals", {})
    assert signals.get("volatilityBand") in {"steady", "spike"}
    assert signals.get("source") == "gameplayCopyPack"
    assert signals.get("policySource") in {"COPY_PACK", "VOLATILITY_MEMORY"}
    assert signals.get("policySourceAlias") in {"C", "V"}
    assert signals.get("policySourceConfidence") in {"LOW", "MID", "HIGH"}
    assert signals.get("policySourceConfidenceAlias") in {"L", "M", "H"}
    assert signals.get("policyAlias") in {"A", "S"}
    assert signals.get("reason") in {
        "steady-pack-recommends-always-onboarding",
        "spike-pack-recommends-gated-onboarding",
    }

    if payload["gameplayCopyPack"] == "spike":
        assert payload["compatRowPolicy"] == "SPIKE_ONLY"
        assert payload["compatRowPolicyAlias"] == "S"
        assert signals.get("volatilityBand") == "spike"
        assert signals.get("policyAlias") == "S"
        assert signals.get("reason") == "spike-pack-recommends-gated-onboarding"
    else:
        assert payload["compatRowPolicy"] == "ALWAYS"
        assert payload["compatRowPolicyAlias"] == "A"
        assert signals.get("volatilityBand") == "steady"
        assert signals.get("policyAlias") == "A"
        assert signals.get("reason") == "steady-pack-recommends-always-onboarding"

    assert signals.get("policySource") == payload["compatRowPolicySource"]
    assert signals.get("policySourceAlias") == payload["compatRowPolicySourceAlias"]
    assert signals.get("policySourceConfidence") == payload["compatRowPolicySourceConfidence"]
    assert signals.get("policySourceConfidenceAlias") == payload["compatRowPolicySourceConfidenceAlias"]

    expected_confidence_alias = {"LOW": "L", "MID": "M", "HIGH": "H"}[
        payload["compatRowPolicySourceConfidence"]
    ]
    assert payload["compatRowPolicySourceConfidenceAlias"] == expected_confidence_alias

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
        compat_lines = compat_text.splitlines()
        compat_row = "- COPY PACK COMPAT:STEADY=ST|SPIKE=SP"
        compat_legend_row = "- COPY PACK COMPAT LEGEND:ST=STEADY|SP=SPIKE"
        contract_row = (
            "- CONTRACT CHECKLIST: compatRowPolicyAlias in {A,S} and compatRowPolicySignals.policyAlias mirrors compatRowPolicyAlias"
        )
        source_contract_row = (
            "- CONTRACT CHECKLIST: compatRowPolicySourceAlias in {C,V} and compatRowPolicySignals.policySourceAlias mirrors compatRowPolicySourceAlias"
        )
        source_confidence_contract_row = (
            "- CONTRACT CHECKLIST: compatRowPolicySourceConfidence in {LOW,MID,HIGH} and compatRowPolicySignals.policySourceConfidence mirrors compatRowPolicySourceConfidence"
        )
        source_confidence_mirror_contract_row = (
            "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidence mirrors compatRowPolicySourceConfidence exactly"
        )
        source_confidence_alias_contract_row = (
            "- CONTRACT CHECKLIST: compatRowPolicySourceConfidenceAlias in {L,M,H} and compatRowPolicySignals.policySourceConfidenceAlias mirrors compatRowPolicySourceConfidenceAlias"
        )
        source_confidence_alias_mirror_contract_row = (
            "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidenceAlias mirrors compatRowPolicySourceConfidenceAlias exactly"
        )

        assert "COPY PACK COMPAT:STEADY=ST|SPIKE=SP" in compat_text, (
            "expected compatibility row when compat flag enabled"
        )
        assert "COPY PACK COMPAT LEGEND:ST=STEADY|SP=SPIKE" in compat_text, (
            "expected compatibility legend row when compat flag enabled"
        )
        assert compat_lines.count(compat_row) == 1, (
            "compatibility row must appear exactly once when compat flag enabled"
        )
        assert compat_lines.count(compat_legend_row) == 1, (
            "compatibility legend row must appear exactly once when compat flag enabled"
        )
        assert compat_lines.count(contract_row) == 1, "contract checklist row must appear exactly once"
        assert compat_lines.count(source_contract_row) == 1, (
            "policy-source contract checklist row must appear exactly once"
        )
        assert compat_lines.count(source_confidence_contract_row) == 1, (
            "policy-source confidence contract checklist row must appear exactly once"
        )
        assert compat_lines.count(source_confidence_mirror_contract_row) == 1, (
            "policy-source confidence mirror contract checklist row must appear exactly once"
        )
        assert compat_lines.count(source_confidence_alias_contract_row) == 1, (
            "policy-source confidence alias contract checklist row must appear exactly once"
        )
        assert compat_lines.count(source_confidence_alias_mirror_contract_row) == 1, (
            "policy-source confidence alias mirror contract checklist row must appear exactly once"
        )
        compat_index = compat_lines.index(compat_row)
        legend_index = compat_lines.index(compat_legend_row)
        assert legend_index == compat_index + 1, (
            "compatibility legend row must immediately follow compatibility row"
        )
        assert contract_row in first_md.read_text(encoding="utf-8"), (
            "contract checklist row should be present in baseline markdown output"
        )
        assert source_contract_row in first_md.read_text(encoding="utf-8"), (
            "policy-source contract checklist row should be present in baseline markdown output"
        )
        assert source_confidence_contract_row in first_md.read_text(encoding="utf-8"), (
            "policy-source confidence contract checklist row should be present in baseline markdown output"
        )
        assert source_confidence_mirror_contract_row in first_md.read_text(encoding="utf-8"), (
            "policy-source confidence mirror contract checklist row should be present in baseline markdown output"
        )
        assert source_confidence_alias_contract_row in first_md.read_text(encoding="utf-8"), (
            "policy-source confidence alias contract checklist row should be present in baseline markdown output"
        )
        assert source_confidence_alias_mirror_contract_row in first_md.read_text(encoding="utf-8"), (
            "policy-source confidence alias mirror contract checklist row should be present in baseline markdown output"
        )
        assert "COPY PACK COMPAT:STEADY=ST|SPIKE=SP" not in first_md.read_text(encoding="utf-8"), (
            "compatibility row must stay gated behind flag"
        )
        assert "COPY PACK COMPAT LEGEND:ST=STEADY|SP=SPIKE" not in first_md.read_text(
            encoding="utf-8"
        ), "compatibility legend row must stay gated behind flag"

        checked_in_payload = json.loads(CHECKED_IN_JSON_FIXTURE.read_text(encoding="utf-8"))
        assert_schema(checked_in_payload)
        checked_in_markdown = CHECKED_IN_MD_FIXTURE.read_text(encoding="utf-8")
        assert source_contract_row in checked_in_markdown, (
            "checked-in fixture markdown must include policy-source alias contract checklist row"
        )
        assert source_confidence_contract_row in checked_in_markdown, (
            "checked-in fixture markdown must include policy-source confidence contract checklist row"
        )
        assert source_confidence_mirror_contract_row in checked_in_markdown, (
            "checked-in fixture markdown must include policy-source confidence mirror contract checklist row"
        )
        assert source_confidence_alias_contract_row in checked_in_markdown, (
            "checked-in fixture markdown must include policy-source confidence alias contract checklist row"
        )
        assert source_confidence_alias_mirror_contract_row in checked_in_markdown, (
            "checked-in fixture markdown must include policy-source confidence alias mirror contract checklist row"
        )

    print("PASS: regression_draft_forced_lane_backlog_tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
