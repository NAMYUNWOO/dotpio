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


def run_fixture_case(
    *,
    tmp_path: Path,
    name: str,
    rows: list[str],
    expected_snapshot: dict[str, int],
    expected_dispatch_hint: str,
    expected_dispatch_hint_alias: str,
    expected_dispatch_pressure: str,
    expected_dispatch_pressure_alias: str,
    expected_dispatch_pressure_momentum: int,
    expected_dispatch_pressure_momentum_band: str,
    expected_dispatch_pressure_momentum_band_alias: str,
    expected_dispatch_pressure_momentum_fx_cue: str,
    expected_dispatch_pressure_momentum_fx_cue_alias: str,
    expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation: str,
) -> None:
    backlog = tmp_path / f"{name}_backlog.md"
    json_out = tmp_path / f"{name}_guardrail.json"
    md_out = tmp_path / f"{name}_guardrail.md"

    backlog.write_text("\n".join(["# fixture", *rows]) + "\n", encoding="utf-8")

    report = run_guardrail(backlog, json_out, md_out)
    snapshot = report.get("trendScoreBandSnapshot")
    assert snapshot == expected_snapshot, (
        f"{name}: trendScoreBandSnapshot counts must include alias/full-token matches"
    )

    alias = report.get("trendScoreBandSnapshotAlias")
    assert alias == expected_alias(snapshot), (
        f"{name}: trendScoreBandSnapshotAlias must match canonical C{{CALM}}E{{EDGE}}H{{HEATED}} mapping"
    )
    assert report.get("trendScoreBandDispatchHint") == expected_dispatch_hint, (
        f"{name}: trendScoreBandDispatchHint must match expected dominant/tie mapping"
    )
    assert report.get("trendScoreBandDispatchHintAlias") == expected_dispatch_hint_alias, (
        f"{name}: trendScoreBandDispatchHintAlias must match compact dispatch-hint alias"
    )
    assert report.get("trendScoreBandDispatchPressure") == expected_dispatch_pressure, (
        f"{name}: trendScoreBandDispatchPressure must match cadence+distribution pressure mapping"
    )
    assert report.get("trendScoreBandDispatchPressureAlias") == expected_dispatch_pressure_alias, (
        f"{name}: trendScoreBandDispatchPressureAlias must match compact dispatch-pressure alias"
    )
    assert report.get("trendScoreBandDispatchPressureMomentum") == expected_dispatch_pressure_momentum, (
        f"{name}: trendScoreBandDispatchPressureMomentum must match deterministic drift-window momentum score"
    )
    assert report.get("trendScoreBandDispatchPressureMomentumBand") == expected_dispatch_pressure_momentum_band, (
        f"{name}: trendScoreBandDispatchPressureMomentumBand must map from momentum score domain"
    )
    assert (
        report.get("trendScoreBandDispatchPressureMomentumBandAlias")
        == expected_dispatch_pressure_momentum_band_alias
    ), f"{name}: trendScoreBandDispatchPressureMomentumBandAlias must match compact momentum-band alias"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxCue")
        == expected_dispatch_pressure_momentum_fx_cue
    ), f"{name}: trendScoreBandDispatchPressureMomentumFxCue must map deterministic combat/vfx cue from momentum band"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxCueAlias")
        == expected_dispatch_pressure_momentum_fx_cue_alias
    ), f"{name}: trendScoreBandDispatchPressureMomentumFxCueAlias must match compact combat/vfx cue alias"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxCueMicrocopyRecommendation")
        == expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation
    ), f"{name}: trendScoreBandDispatchPressureMomentumFxCueMicrocopyRecommendation must map deterministic ai-content/design recommendation from momentum fx cue"

    md_text = md_out.read_text(encoding="utf-8")
    assert f"TSSB:{alias}" in md_text, f"{name}: markdown output must render canonical TSSB alias"
    assert "TSSB legend (C=calm, E=edge, H=heated)" in md_text, (
        f"{name}: markdown output must include compact TSSB decode microcopy row"
    )
    assert f"trend-score dispatch hint (offline): **{expected_dispatch_hint}**" in md_text, (
        f"{name}: markdown output must include deterministic offline dispatch hint row"
    )
    assert f"trend-score dispatch hint alias: **TSDH:{expected_dispatch_hint_alias}**" in md_text, (
        f"{name}: markdown output must include compact dispatch-hint alias row"
    )
    assert f"trend-score dispatch pressure (offline): **{expected_dispatch_pressure}**" in md_text, (
        f"{name}: markdown output must include offline dispatch-pressure row"
    )
    assert f"trend-score dispatch pressure alias: **TSDP:{expected_dispatch_pressure_alias}**" in md_text, (
        f"{name}: markdown output must include compact dispatch-pressure alias row"
    )
    assert (
        f"trend-score dispatch-pressure momentum (offline): **{expected_dispatch_pressure_momentum}**"
        in md_text
    ), f"{name}: markdown output must include offline dispatch-pressure momentum row"
    assert (
        f"trend-score dispatch-pressure momentum band (offline): **{expected_dispatch_pressure_momentum_band}**"
        in md_text
    ), f"{name}: markdown output must include offline momentum-band row"
    assert (
        f"trend-score dispatch-pressure momentum band alias: **TSDPM:{expected_dispatch_pressure_momentum_band_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact momentum-band alias row"
    assert (
        f"trend-score dispatch-pressure momentum fx cue (combat/vfx): **{expected_dispatch_pressure_momentum_fx_cue}**"
        in md_text
    ), f"{name}: markdown output must include combat/vfx momentum fx-cue row"
    assert (
        f"trend-score dispatch-pressure momentum fx cue alias: **TSDPMFX:{expected_dispatch_pressure_momentum_fx_cue_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact combat/vfx momentum fx-cue alias row"
    assert (
        "trend-score dispatch-pressure momentum fx cue cadence decode (design/world): "
        "**SOFT=CALM cadence, EDGE=EDGE cadence, HARD=HEATED cadence**"
        in md_text
    ), f"{name}: markdown output must include design/world momentum fx-cue cadence decode row"
    assert (
        "trend-score dispatch-pressure momentum fx cue microcopy rec (ai-content/design): "
        f"**{expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation}**"
        in md_text
    ), f"{name}: markdown output must include ai-content/design momentum fx-cue microcopy recommendation row"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="regression_check_lane_guardrail_") as tmp:
        tmp_path = Path(tmp)

        run_fixture_case(
            tmp_path=tmp_path,
            name="balanced_tie",
            rows=[
                "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C and compatRowPolicySourceConfidenceTrendScoreBand:CALM",
                "- [x] Design/World Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E and compatRowPolicySourceConfidenceTrendScoreBand:EDGE",
                "- [x] Combat/VFX Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:H and compatRowPolicySourceConfidenceTrendScoreBand:HEATED",
                "- [x] AI Content/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                "- [x] UX/Systems Team: compatRowPolicySourceConfidenceTrendScoreBand:EDGE",
            ],
            expected_snapshot={"CALM": 3, "EDGE": 3, "HEATED": 2},
            expected_dispatch_hint="BALANCED",
            expected_dispatch_hint_alias="B",
            expected_dispatch_pressure="LIGHT",
            expected_dispatch_pressure_alias="L",
            expected_dispatch_pressure_momentum=100,
            expected_dispatch_pressure_momentum_band="HIGH",
            expected_dispatch_pressure_momentum_band_alias="H",
            expected_dispatch_pressure_momentum_fx_cue="HARD",
            expected_dispatch_pressure_momentum_fx_cue_alias="H",
            expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="surge pressure; triage hottest lane first",
        )

        run_fixture_case(
            tmp_path=tmp_path,
            name="ready_mix",
            rows=[
                "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                "- [x] Design/World Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                "- [x] UX/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E",
                "- [x] Combat/VFX Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:H",
                "- [x] AI Content/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E",
                "- [x] World Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
            ],
            expected_snapshot={"CALM": 3, "EDGE": 2, "HEATED": 1},
            expected_dispatch_hint="CALM_FOCUS",
            expected_dispatch_hint_alias="C",
            expected_dispatch_pressure="READY",
            expected_dispatch_pressure_alias="R",
            expected_dispatch_pressure_momentum=88,
            expected_dispatch_pressure_momentum_band="HIGH",
            expected_dispatch_pressure_momentum_band_alias="H",
            expected_dispatch_pressure_momentum_fx_cue="HARD",
            expected_dispatch_pressure_momentum_fx_cue_alias="H",
            expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="surge pressure; triage hottest lane first",
        )

        run_fixture_case(
            tmp_path=tmp_path,
            name="calm_focus",
            rows=[
                "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBand:CALM",
                "- [x] Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                "- [x] UX/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                "- [x] Design/World Team: compatRowPolicySourceConfidenceTrendScoreBand:EDGE",
                "- [x] Combat/VFX Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:H",
            ],
            expected_snapshot={"CALM": 3, "EDGE": 1, "HEATED": 1},
            expected_dispatch_hint="CALM_FOCUS",
            expected_dispatch_hint_alias="C",
            expected_dispatch_pressure="HOT",
            expected_dispatch_pressure_alias="H",
            expected_dispatch_pressure_momentum=64,
            expected_dispatch_pressure_momentum_band="MID",
            expected_dispatch_pressure_momentum_band_alias="M",
            expected_dispatch_pressure_momentum_fx_cue="EDGE",
            expected_dispatch_pressure_momentum_fx_cue_alias="E",
            expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="pressure rising; prep focused dispatch",
        )

        run_fixture_case(
            tmp_path=tmp_path,
            name="edge_focus",
            rows=[
                "- [x] Design/World Team: compatRowPolicySourceConfidenceTrendScoreBand:EDGE",
                "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E",
                "- [x] UX Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E",
                "- [x] AI Content/Systems Team: compatRowPolicySourceConfidenceTrendScoreBand:CALM",
                "- [x] Combat/VFX Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:H",
            ],
            expected_snapshot={"CALM": 1, "EDGE": 3, "HEATED": 1},
            expected_dispatch_hint="EDGE_FOCUS",
            expected_dispatch_hint_alias="E",
            expected_dispatch_pressure="HOT",
            expected_dispatch_pressure_alias="H",
            expected_dispatch_pressure_momentum=64,
            expected_dispatch_pressure_momentum_band="MID",
            expected_dispatch_pressure_momentum_band_alias="M",
            expected_dispatch_pressure_momentum_fx_cue="EDGE",
            expected_dispatch_pressure_momentum_fx_cue_alias="E",
            expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="pressure rising; prep focused dispatch",
        )

        run_fixture_case(
            tmp_path=tmp_path,
            name="heated_focus",
            rows=[
                "- [x] Combat/VFX Team: compatRowPolicySourceConfidenceTrendScoreBand:HEATED",
                "- [x] Combat Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:H",
                "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:H",
                "- [x] Design/World Team: compatRowPolicySourceConfidenceTrendScoreBand:EDGE",
                "- [x] UX/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
            ],
            expected_snapshot={"CALM": 1, "EDGE": 1, "HEATED": 3},
            expected_dispatch_hint="HEATED_FOCUS",
            expected_dispatch_hint_alias="H",
            expected_dispatch_pressure="HOT",
            expected_dispatch_pressure_alias="H",
            expected_dispatch_pressure_momentum=64,
            expected_dispatch_pressure_momentum_band="MID",
            expected_dispatch_pressure_momentum_band_alias="M",
            expected_dispatch_pressure_momentum_fx_cue="EDGE",
            expected_dispatch_pressure_momentum_fx_cue_alias="E",
            expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="pressure rising; prep focused dispatch",
        )

        run_fixture_case(
            tmp_path=tmp_path,
            name="low_momentum_band",
            rows=[
                "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBand:CALM",
                "- [x] Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                "- [x] UX/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                "- [x] AI Content/Systems Team: compatRowPolicySourceConfidenceTrendScoreBand:CALM",
                "- [x] Design/Systems Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
            ],
            expected_snapshot={"CALM": 5, "EDGE": 0, "HEATED": 0},
            expected_dispatch_hint="CALM_FOCUS",
            expected_dispatch_hint_alias="C",
            expected_dispatch_pressure="HOT",
            expected_dispatch_pressure_alias="H",
            expected_dispatch_pressure_momentum=5,
            expected_dispatch_pressure_momentum_band="LOW",
            expected_dispatch_pressure_momentum_band_alias="L",
            expected_dispatch_pressure_momentum_fx_cue="SOFT",
            expected_dispatch_pressure_momentum_fx_cue_alias="S",
            expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="steady pace; hold broad scan",
        )

    print("ok: trendScoreBand dispatch-hint/momentum-band regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
