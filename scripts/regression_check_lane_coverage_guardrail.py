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


def run_guardrail(
    backlog: Path,
    json_out: Path,
    md_out: Path,
    *,
    include_trend_family_why: bool = False,
) -> dict:
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
    if include_trend_family_why:
        cmd.append("--include-trend-family-why")
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
    expected_dispatch_pressure_momentum_band_sparkline: str,
    expected_dispatch_pressure_momentum_slope: str,
    expected_dispatch_pressure_momentum_slope_alias: str,
    expected_dispatch_pressure_momentum_slope_recommendation: str,
    expected_dispatch_pressure_momentum_fx_cue: str,
    expected_dispatch_pressure_momentum_fx_cue_alias: str,
    expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation: str,
    expected_recommendation_family_trend: str | None = None,
) -> str:
    backlog = tmp_path / f"{name}_backlog.md"
    json_out = tmp_path / f"{name}_guardrail.json"
    md_out = tmp_path / f"{name}_guardrail.md"

    backlog.write_text("\n".join(["# fixture", *rows]) + "\n", encoding="utf-8")

    report = run_guardrail(backlog, json_out, md_out, include_trend_family_why=True)
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
        report.get("trendScoreBandDispatchPressureMomentumBandSparkline")
        == expected_dispatch_pressure_momentum_band_sparkline
    ), f"{name}: trendScoreBandDispatchPressureMomentumBandSparkline must match deterministic rolling momentum-band progression"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumSlope")
        == expected_dispatch_pressure_momentum_slope
    ), f"{name}: trendScoreBandDispatchPressureMomentumSlope must map deterministic prior-window momentum deltas"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumSlopeAlias")
        == expected_dispatch_pressure_momentum_slope_alias
    ), f"{name}: trendScoreBandDispatchPressureMomentumSlopeAlias must match compact momentum-slope alias"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumSlopeRecommendation")
        == expected_dispatch_pressure_momentum_slope_recommendation
    ), f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendation must map deterministic ai-content/systems recommendation from momentum slope"
    expected_recommendation_state = {
        "COOLING": "HOLD",
        "RISING": "PREP",
        "SURGING": "CLAMP",
    }.get(expected_dispatch_pressure_momentum_slope, "HOLD")
    expected_recommendation_alias = {
        "HOLD": "H",
        "PREP": "P",
        "CLAMP": "C",
    }.get(expected_recommendation_state, "H")
    assert (
        report.get("trendScoreBandDispatchPressureMomentumSlopeRecommendationState")
        == expected_recommendation_state
    ), f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationState must map deterministic HOLD/PREP/CLAMP state from momentum slope"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumSlopeRecommendationAlias")
        == expected_recommendation_alias
    ), f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationAlias must map deterministic compact alias from recommendation state"
    expected_recommendation_family = {
        "HOLD": "STABLE",
        "PREP": "READY",
        "CLAMP": "TRIAGE",
    }.get(expected_recommendation_state, "STABLE")
    expected_recommendation_family_alias = {
        "STABLE": "S",
        "READY": "R",
        "TRIAGE": "T",
    }.get(expected_recommendation_family, "S")
    assert (
        report.get("trendScoreBandDispatchPressureMomentumSlopeRecommendationFamily")
        == expected_recommendation_family
    ), f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationFamily must map deterministic STABLE/READY/TRIAGE family from recommendation state"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyAlias")
        == expected_recommendation_family_alias
    ), f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyAlias must map deterministic compact alias from recommendation family"
    family_trend = report.get("trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrend")
    assert family_trend in {"UP", "FLAT", "DOWN"}, (
        f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrend must stay in UP/FLAT/DOWN domain"
    )
    if expected_recommendation_family_trend is not None:
        assert family_trend == expected_recommendation_family_trend, (
            f"{name}: expected explicit prior-window family trend {expected_recommendation_family_trend}, got {family_trend}"
        )
    family_trend_alias = report.get("trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendAlias")
    assert family_trend_alias == {"UP": "U", "FLAT": "F", "DOWN": "D"}.get(family_trend), (
        f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendAlias must deterministically mirror family trend alias"
    )
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
        "trend-score dispatch-pressure momentum band progression (last-10 rolling): "
        f"**TSDPM-SPARK:{expected_dispatch_pressure_momentum_band_sparkline}**"
        in md_text
    ), f"{name}: markdown output must include compact momentum-band sparkline row"
    assert "trend-score momentum sparkline legend: **L=LOW, M=MID, H=HIGH (older->newer)**" in md_text, (
        f"{name}: markdown output must include momentum sparkline legend row"
    )
    assert (
        "trend-score dispatch-pressure momentum slope (ai-content/systems): "
        f"**{expected_dispatch_pressure_momentum_slope}**"
        in md_text
    ), f"{name}: markdown output must include deterministic offline momentum-slope row"
    assert (
        f"trend-score dispatch-pressure momentum slope alias: **TSDPMS:{expected_dispatch_pressure_momentum_slope_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact momentum-slope alias row"
    assert (
        "trend-score momentum-slope rec state alias: "
        f"**TSDPMSR:{expected_recommendation_alias}** ({expected_recommendation_state})"
        in md_text
    ), f"{name}: markdown output must include compact momentum-slope recommendation-state alias row"
    assert "trend-score momentum-slope rec decode: **TSDPMSR legend (H=HOLD, P=PREP, C=CLAMP)**" in md_text, (
        f"{name}: markdown output must include TSDPMSR decode row"
    )
    assert (
        "trend-score momentum-slope rec family alias: "
        f"**TSDPMSRF:{expected_recommendation_family_alias}** ({expected_recommendation_family})"
        in md_text
    ), f"{name}: markdown output must include compact momentum-slope recommendation-family alias row"
    assert "trend-score momentum-slope rec family decode: **TSDPMSRF legend (S=STABLE, R=READY, T=TRIAGE)**" in md_text, (
        f"{name}: markdown output must include TSDPMSRF decode row"
    )
    assert (
        "trend-score momentum-slope rec family trend alias: "
        f"**TSDPMSRFT:{family_trend_alias}** ({family_trend})"
        in md_text
    ), f"{name}: markdown output must include compact momentum-slope recommendation-family trend alias row"
    assert "trend-score momentum-slope rec family trend decode: **TSDPMSRFT legend (U=UP, F=FLAT, D=DOWN)**" in md_text, (
        f"{name}: markdown output must include TSDPMSRFT decode row"
    )
    expected_family_trend_why = {
        "UP": "escalate lane pressure checks",
        "FLAT": "hold lane pressure cadence",
        "DOWN": "cool lane pressure posture",
    }.get(family_trend, "hold lane pressure cadence")
    expected_family_trend_why_alias = {
        "UP": "E",
        "FLAT": "H",
        "DOWN": "C",
    }.get(family_trend, "H")
    assert (
        "trend-score momentum-slope rec family trend decode variant (design/world): "
        "**TSDPMSRFT legend (U=escalate, F=hold, D=cool)**"
        in md_text
    ), f"{name}: markdown output must include optional design/world trend decode variant when flag enabled"
    assert (
        "trend-score momentum-slope rec family trend why alias: "
        f"**TSDPMSRFTWHYA:{expected_family_trend_why_alias}**"
        in md_text
    ), f"{name}: markdown output must include optional trend-rationale alias row when flag enabled"
    assert (
        "trend-score momentum-slope rec family trend why alias decode: "
        "**TSDPMSRFTWHYA legend (E=escalate, H=hold, C=cool)**"
        in md_text
    ), f"{name}: markdown output must include optional trend-rationale alias decode row when flag enabled"
    assert (
        "trend-score momentum-slope rec family trend why (ai-content/systems): "
        f"**TSDPMSRFT WHY:{expected_family_trend_why}**"
        in md_text
    ), f"{name}: markdown output must include optional ai-content/systems trend rationale microcopy when flag enabled"

    optional_decode_variant_row = (
        "trend-score momentum-slope rec family trend decode variant (design/world): "
        "**TSDPMSRFT legend (U=escalate, F=hold, D=cool)**"
    )
    optional_why_alias_row = (
        "trend-score momentum-slope rec family trend why alias: "
        f"**TSDPMSRFTWHYA:{expected_family_trend_why_alias}**"
    )
    optional_why_alias_decode_row = (
        "trend-score momentum-slope rec family trend why alias decode: "
        "**TSDPMSRFTWHYA legend (E=escalate, H=hold, C=cool)**"
    )
    optional_why_row = (
        "trend-score momentum-slope rec family trend why (ai-content/systems): "
        f"**TSDPMSRFT WHY:{expected_family_trend_why}**"
    )
    optional_decode_variant_idx = md_text.find(optional_decode_variant_row)
    optional_why_alias_idx = md_text.find(optional_why_alias_row)
    optional_why_alias_decode_idx = md_text.find(optional_why_alias_decode_row)
    optional_why_idx = md_text.find(optional_why_row)
    assert (
        optional_decode_variant_idx
        < optional_why_alias_idx
        < optional_why_alias_decode_idx
        < optional_why_idx
    ), (
        f"{name}: optional trend rows must preserve order "
        "`TSDPMSRFT decode variant -> TSDPMSRFTWHYA -> TSDPMSRFTWHYA decode -> TSDPMSRFT WHY`"
    )

    assert (
        "trend-score dispatch-pressure momentum slope rec (ai-content/systems): "
        f"**{expected_dispatch_pressure_momentum_slope_recommendation}**"
        in md_text
    ), f"{name}: markdown output must include ai-content/systems momentum-slope recommendation row"
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

    return family_trend


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="regression_check_lane_guardrail_") as tmp:
        tmp_path = Path(tmp)
        observed_family_trends: list[str] = []

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
            expected_dispatch_pressure_momentum_band_sparkline="HHHH",
            expected_dispatch_pressure_momentum_slope="COOLING",
            expected_dispatch_pressure_momentum_slope_alias="C",
            expected_dispatch_pressure_momentum_slope_recommendation="hold steady; validate calm-lane continuity",
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
            expected_dispatch_pressure_momentum_band_sparkline="LMHHH",
            expected_dispatch_pressure_momentum_slope="RISING",
            expected_dispatch_pressure_momentum_slope_alias="R",
            expected_dispatch_pressure_momentum_slope_recommendation="prep focused sweeps; stage next-lane handoff",
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
            expected_dispatch_pressure_momentum_band_sparkline="LLMM",
            expected_dispatch_pressure_momentum_slope="SURGING",
            expected_dispatch_pressure_momentum_slope_alias="S",
            expected_dispatch_pressure_momentum_slope_recommendation="escalate triage; clamp hottest-lane drift",
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
            expected_dispatch_pressure_momentum_band_sparkline="LLMM",
            expected_dispatch_pressure_momentum_slope="SURGING",
            expected_dispatch_pressure_momentum_slope_alias="S",
            expected_dispatch_pressure_momentum_slope_recommendation="escalate triage; clamp hottest-lane drift",
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
            expected_dispatch_pressure_momentum_band_sparkline="LLMM",
            expected_dispatch_pressure_momentum_slope="SURGING",
            expected_dispatch_pressure_momentum_slope_alias="S",
            expected_dispatch_pressure_momentum_slope_recommendation="escalate triage; clamp hottest-lane drift",
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
            expected_dispatch_pressure_momentum_band_sparkline="LLLL",
            expected_dispatch_pressure_momentum_slope="COOLING",
            expected_dispatch_pressure_momentum_slope_alias="C",
            expected_dispatch_pressure_momentum_slope_recommendation="hold steady; validate calm-lane continuity",
            expected_dispatch_pressure_momentum_fx_cue="SOFT",
            expected_dispatch_pressure_momentum_fx_cue_alias="S",
            expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="steady pace; hold broad scan",
        )

        observed_family_trends.append(
            run_fixture_case(
                tmp_path=tmp_path,
                name="prior_window_trend_up",
                rows=[
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E",
                ],
                expected_snapshot={"CALM": 2, "EDGE": 1, "HEATED": 0},
                expected_dispatch_hint="CALM_FOCUS",
                expected_dispatch_hint_alias="C",
                expected_dispatch_pressure="HOT",
                expected_dispatch_pressure_alias="H",
                expected_dispatch_pressure_momentum=58,
                expected_dispatch_pressure_momentum_band="MID",
                expected_dispatch_pressure_momentum_band_alias="M",
                expected_dispatch_pressure_momentum_band_sparkline="LM",
                expected_dispatch_pressure_momentum_slope="SURGING",
                expected_dispatch_pressure_momentum_slope_alias="S",
                expected_dispatch_pressure_momentum_slope_recommendation="escalate triage; clamp hottest-lane drift",
                expected_dispatch_pressure_momentum_fx_cue="EDGE",
                expected_dispatch_pressure_momentum_fx_cue_alias="E",
                expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="pressure rising; prep focused dispatch",
                expected_recommendation_family_trend="UP",
            )
        )
        observed_family_trends.append(
            run_fixture_case(
                tmp_path=tmp_path,
                name="prior_window_trend_down",
                rows=[
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:C",
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E",
                    "- [x] Systems/QA Team: compatRowPolicySourceConfidenceTrendScoreBandAlias:E",
                ],
                expected_snapshot={"CALM": 2, "EDGE": 2, "HEATED": 0},
                expected_dispatch_hint="BALANCED",
                expected_dispatch_hint_alias="B",
                expected_dispatch_pressure="HOT",
                expected_dispatch_pressure_alias="H",
                expected_dispatch_pressure_momentum=38,
                expected_dispatch_pressure_momentum_band="MID",
                expected_dispatch_pressure_momentum_band_alias="M",
                expected_dispatch_pressure_momentum_band_sparkline="LMM",
                expected_dispatch_pressure_momentum_slope="COOLING",
                expected_dispatch_pressure_momentum_slope_alias="C",
                expected_dispatch_pressure_momentum_slope_recommendation="hold steady; validate calm-lane continuity",
                expected_dispatch_pressure_momentum_fx_cue="EDGE",
                expected_dispatch_pressure_momentum_fx_cue_alias="E",
                expected_dispatch_pressure_momentum_fx_cue_microcopy_recommendation="pressure rising; prep focused dispatch",
                expected_recommendation_family_trend="DOWN",
            )
        )

        assert "UP" in observed_family_trends and "DOWN" in observed_family_trends, (
            "fixture matrix must include explicit prior-window recommendation-family trend transitions for both UP and DOWN"
        )

    print("ok: trendScoreBand dispatch-hint/momentum-band regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
