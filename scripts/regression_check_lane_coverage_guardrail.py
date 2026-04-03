#!/usr/bin/env python3
"""Regression checks for lane-coverage guardrail trend-score alias mapping."""

from __future__ import annotations

import json
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_lane_coverage_guardrail.py"


def load_guardrail_module():
    spec = importlib.util.spec_from_file_location("check_lane_coverage_guardrail", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load check_lane_coverage_guardrail module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_guardrail(
    backlog: Path,
    json_out: Path,
    md_out: Path,
    *,
    include_trend_family_why: bool = False,
    include_combat_callout_compact_legend: bool = False,
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
    if include_combat_callout_compact_legend:
        cmd.append("--include-combat-callout-compact-legend")
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
    expected_dispatch_pressure_base_class: str,
    expected_dispatch_pressure_cadence_override_state: str,
    expected_dispatch_pressure_cadence_override_alias: str,
    expected_dispatch_pressure_cadence_override_streak: int,
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
    expected_dispatch_pressure_momentum_fx_cue_combat_callout: str,
    expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias: str,
    expected_recommendation_family_trend: str | None = None,
) -> dict[str, int | str]:
    backlog = tmp_path / f"{name}_backlog.md"
    json_out = tmp_path / f"{name}_guardrail.json"
    md_out = tmp_path / f"{name}_guardrail.md"

    backlog.write_text("\n".join(["# fixture", *rows]) + "\n", encoding="utf-8")

    report = run_guardrail(
        backlog,
        json_out,
        md_out,
        include_trend_family_why=True,
        include_combat_callout_compact_legend=True,
    )
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
    assert (
        report.get("trendScoreBandDispatchPressureBaseClass")
        == expected_dispatch_pressure_base_class
    ), f"{name}: trendScoreBandDispatchPressureBaseClass must expose deterministic pre-override pressure class"
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideState")
        == expected_dispatch_pressure_cadence_override_state
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideState must reflect deterministic combat-or-vfx consecutive-missing override state"
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideAlias")
        == expected_dispatch_pressure_cadence_override_alias
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideAlias must mirror compact BASE/ESCALATE alias"
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideStreak")
        == expected_dispatch_pressure_cadence_override_streak
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideStreak must stay deterministic (0|1|2) from current/prior combat-or-vfx missing windows"
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideBucket")
        == "combat-or-vfx"
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideBucket must remain deterministic on combat-or-vfx cadence gate"
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
    why_copy_budget_token = report.get(
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudget"
    )
    assert why_copy_budget_token == "TSDPMSRFTWHYLEN:E24|H21|C21|MAX24/32", (
        f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudget must mirror canonical WHY copy-budget token"
    )
    why_copy_budget_signals = report.get(
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudgetSignals"
    )
    assert why_copy_budget_signals == {
        "copyMap": {
            "E": "escalate pressure checks",
            "H": "hold pressure cadence",
            "C": "cool pressure posture",
        },
        "lengths": {"E": 24, "H": 21, "C": 21},
        "threshold": 32,
        "maxLen": 24,
    }, (
        f"{name}: trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudgetSignals must expose deterministic copyMap/lengths/threshold/maxLen payload mirror"
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
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxCueCombatCallout")
        == expected_dispatch_pressure_momentum_fx_cue_combat_callout
    ), f"{name}: trendScoreBandDispatchPressureMomentumFxCueCombatCallout must map deterministic combat/vfx callout from momentum fx cue"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxCueCombatCalloutAlias")
        == expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias
    ), f"{name}: trendScoreBandDispatchPressureMomentumFxCueCombatCalloutAlias must match compact combat/vfx callout alias"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeBaseline")
        == "HL=hold line, PE=press edge, BC=burst clear"
    ), f"{name}: baseline combat-callout decode row must remain deterministic"
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeCompact")
        == "HL=hold lane, PE=push edge, BC=burst clear"
    ), f"{name}: compact combat-callout decode variant must remain deterministic"
    assert report.get("trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeEvaluation") == {
        "baseline": "HL=hold line, PE=press edge, BC=burst clear",
        "compact": "HL=hold lane, PE=push edge, BC=burst clear",
        "baselineLen": 43,
        "compactLen": 42,
        "dosWidthLimit": 72,
        "preferred": "COMPACT",
        "status": "PASS",
    }, f"{name}: combat-callout decode evaluation payload must include deterministic DOS-width/readability signals"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasDecodeEvaluation"
    ) == {
        "baseline": "PH=push now/hard crack, HP=hold lane/pressure poke, ES=ease lane/steady nudge",
        "compact": "PH|HP|ES",
        "baselineLen": 77,
        "compactLen": 8,
        "dosWidthLimit": 72,
        "preferred": "COMPACT",
        "status": "WARN",
    }, f"{name}: adaptive-focus alias decode evaluation payload must keep deterministic baseline/compact shape + DOS-width signal contract"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasPreferenceToken"
    ) in {"PH", "HP", "ES"}, f"{name}: adaptive-focus alias preference token must stay within PH|HP|ES"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasPreferenceAbSweep"
    ) == "A=PH|B=HP|C=ES", f"{name}: adaptive-focus alias A/B sweep seed must remain deterministic"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasPreferenceAbLabelPilot"
    ) == "A=PN|B=HL|C=EZ", f"{name}: adaptive-focus alias A/B pilot labels must remain deterministic"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasPreferenceAbWinner"
    ) in {"A", "B", "C"}, f"{name}: adaptive-focus alias A/B winning-slot token must stay within A|B|C"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasPreferenceAbWinnerLegend"
    ) == "A=PH|B=HP|C=ES", f"{name}: adaptive-focus alias A/B winning-slot decode legend must remain deterministic"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasPreferenceAbWinnerPilotLabel"
    ) in {"PN", "HL", "EZ"}, f"{name}: adaptive-focus alias A/B winning-slot pilot label must stay within PN|HL|EZ"
    assert report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyUltraCompactShortlistAdaptiveFocusAliasPreferenceAbWinnerPilotLegend"
    ) == "A=PN|B=HL|C=EZ", f"{name}: adaptive-focus alias A/B winning-slot pilot decode legend must remain deterministic"

    md_text = md_out.read_text(encoding="utf-8")
    cadence_24h_health = report.get("cadence24hHealth")
    cadence_24h_health_alias = report.get("cadence24hHealthAlias")
    assert cadence_24h_health in {"OK", "WATCH", "ALERT"}, (
        f"{name}: cadence24hHealth must stay within OK|WATCH|ALERT domain"
    )
    assert cadence_24h_health_alias in {"O", "W", "A"}, (
        f"{name}: cadence24hHealthAlias must stay within O|W|A domain"
    )
    assert cadence_24h_health_alias == {"OK": "O", "WATCH": "W", "ALERT": "A"}[cadence_24h_health], (
        f"{name}: cadence24hHealthAlias must deterministically mirror cadence24hHealth"
    )
    assert report.get("cadence24hLegendBaseline") == "O=OK, W=WATCH, A=ALERT", (
        f"{name}: cadence24hLegendBaseline must remain deterministic"
    )
    assert report.get("cadence24hLegendCompact") == "O=ok, W=watch, A=alert", (
        f"{name}: cadence24hLegendCompact must remain deterministic compact decode copy"
    )
    assert report.get("cadence24hLegendEvaluation") == {
        "baseline": "O=OK, W=WATCH, A=ALERT",
        "compact": "O=ok, W=watch, A=alert",
        "baselineLen": 22,
        "compactLen": 22,
        "dosWidthLimit": 72,
        "preferred": "COMPACT",
        "status": "PASS",
    }, f"{name}: cadence24hLegendEvaluation must expose deterministic DOS-width/readability payload"
    assert (
        f"TSDCAD24:{cadence_24h_health_alias}** ({cadence_24h_health})" in md_text
    ), f"{name}: markdown output must include cadence-24h token row with alias/value parity"
    assert (
        "cadence 24h health compact decode (design/world): **O=ok, W=watch, A=alert**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-24h decode row"
    assert (
        "cadence 24h health decode dos-width eval (design/world): **TSDCAD24LEN:B22|C22|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include cadence-24h DOS-width/readability evaluation row"
    cadence_24h_token_rows = md_text.count("**TSDCAD24:")
    cadence_24h_legend_rows = md_text.count("**TSDCAD24 legend (O=OK, W=WATCH, A=ALERT)**")
    cadence_24h_compact_rows = md_text.count("**O=ok, W=watch, A=alert**")
    cadence_24h_eval_rows = md_text.count("**TSDCAD24LEN:")
    assert cadence_24h_token_rows >= 1, (
        f"{name}: markdown output must include at least one cadence-24h token row"
    )
    assert cadence_24h_legend_rows == cadence_24h_token_rows, (
        f"{name}: TSDCAD24 legend row count must match TSDCAD24 token row count across sections"
    )
    assert cadence_24h_compact_rows == cadence_24h_token_rows, (
        f"{name}: TSDCAD24 compact decode row count must match TSDCAD24 token row count across sections"
    )
    assert cadence_24h_eval_rows == cadence_24h_token_rows, (
        f"{name}: TSDCAD24LEN row count must match TSDCAD24 token row count across sections"
    )
    assert report.get("cadence24hRecoveryTriadPulsePaletteAlias") == "CV=SPARK|DW=ANCHOR|SO=LOCK", (
        f"{name}: cadence24hRecoveryTriadPulsePaletteAlias must stay deterministic"
    )
    expected_cadence_24h_coverage_alias = (
        f"CV{report.get('bucketCadence', {}).get('combat-or-vfx', {}).get('count', 0)}|"
        f"DW{report.get('bucketCadence', {}).get('design-or-world', {}).get('count', 0)}|"
        f"SO{report.get('bucketCadence', {}).get('systems-or-ops', {}).get('count', 0)}"
    )
    expected_cadence_24h_bucket_hit_counts_row = (
        "- cadence 24h bucket hit counts (forced-next rationale): "
        f"**combat-or-vfx={report.get('bucketCadence', {}).get('combat-or-vfx', {}).get('count', 0)} | "
        f"design-or-world={report.get('bucketCadence', {}).get('design-or-world', {}).get('count', 0)} | "
        f"systems-or-ops={report.get('bucketCadence', {}).get('systems-or-ops', {}).get('count', 0)}**"
    )
    assert expected_cadence_24h_bucket_hit_counts_row in md_text, (
        f"{name}: markdown output must include explicit cadence 24h bucket hit counts alongside forced-next rationale"
    )
    expected_cadence_24h_coverage_pressure_alias = (
        "GAP"
        if min(
            int(report.get('bucketCadence', {}).get('combat-or-vfx', {}).get('count', 0)),
            int(report.get('bucketCadence', {}).get('design-or-world', {}).get('count', 0)),
            int(report.get('bucketCadence', {}).get('systems-or-ops', {}).get('count', 0)),
        )
        <= 0
        else (
            "THIN"
            if min(
                int(report.get('bucketCadence', {}).get('combat-or-vfx', {}).get('count', 0)),
                int(report.get('bucketCadence', {}).get('design-or-world', {}).get('count', 0)),
                int(report.get('bucketCadence', {}).get('systems-or-ops', {}).get('count', 0)),
            )
            == 1
            else "SOLID"
        )
    )
    cadence_counts = [
        int(report.get('bucketCadence', {}).get('combat-or-vfx', {}).get('count', 0)),
        int(report.get('bucketCadence', {}).get('design-or-world', {}).get('count', 0)),
        int(report.get('bucketCadence', {}).get('systems-or-ops', {}).get('count', 0)),
    ]
    cadence_spread = max(cadence_counts) - min(cadence_counts)
    expected_cadence_24h_coverage_spread_alias = (
        "STABLE" if cadence_spread <= 1 else ("SHIFT" if cadence_spread == 2 else "WIDE")
    )
    cadence_24h_coverage_spread_trend = report.get("cadence24hRecoveryTriadCoverageSpreadTrend")
    cadence_24h_coverage_spread_trend_alias = report.get("cadence24hRecoveryTriadCoverageSpreadTrendAlias")
    cadence_24h_coverage_spread_trend_confidence = report.get(
        "cadence24hRecoveryTriadCoverageSpreadTrendConfidence"
    )
    cadence_24h_coverage_spread_trend_confidence_alias = report.get(
        "cadence24hRecoveryTriadCoverageSpreadTrendConfidenceAlias"
    )
    cadence_24h_coverage_spread_trend_confidence_momentum = report.get(
        "cadence24hRecoveryTriadCoverageSpreadTrendConfidenceMomentum"
    )
    cadence_24h_coverage_spread_trend_confidence_momentum_alias = report.get(
        "cadence24hRecoveryTriadCoverageSpreadTrendConfidenceMomentumAlias"
    )
    cadence_24h_coverage_spread_trend_confidence_momentum_score = int(
        report.get("cadence24hRecoveryTriadCoverageSpreadTrendConfidenceMomentumScore", 50)
    )
    assert report.get("cadence24hRecoveryTriadCoverageAlias") == expected_cadence_24h_coverage_alias, (
        f"{name}: cadence24hRecoveryTriadCoverageAlias must deterministically mirror cadence bucket counts"
    )
    assert report.get("cadence24hRecoveryTriadCoveragePressureAlias") == expected_cadence_24h_coverage_pressure_alias, (
        f"{name}: cadence24hRecoveryTriadCoveragePressureAlias must deterministically mirror minimum bucket coverage pressure"
    )
    assert report.get("cadence24hRecoveryTriadCoverageSpreadAlias") == expected_cadence_24h_coverage_spread_alias, (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadAlias must deterministically mirror cadence bucket count spread"
    )
    assert cadence_24h_coverage_spread_trend in {"UP", "FLAT", "DOWN"}, (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadTrend must stay within UP|FLAT|DOWN domain"
    )
    assert cadence_24h_coverage_spread_trend_alias == {"UP": "U", "FLAT": "F", "DOWN": "D"}[cadence_24h_coverage_spread_trend], (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadTrendAlias must deterministically mirror spread-trend alias map"
    )
    assert cadence_24h_coverage_spread_trend_confidence in {"LOW", "MID", "HIGH"}, (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadTrendConfidence must stay within LOW|MID|HIGH domain"
    )
    assert cadence_24h_coverage_spread_trend_confidence_alias == {
        "LOW": "L",
        "MID": "M",
        "HIGH": "H",
    }[cadence_24h_coverage_spread_trend_confidence], (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadTrendConfidenceAlias must deterministically mirror confidence alias map"
    )
    assert cadence_24h_coverage_spread_trend_confidence_momentum in {"UP", "FLAT", "DOWN"}, (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadTrendConfidenceMomentum must stay within UP|FLAT|DOWN domain"
    )
    assert cadence_24h_coverage_spread_trend_confidence_momentum_alias == {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }[cadence_24h_coverage_spread_trend_confidence_momentum], (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadTrendConfidenceMomentumAlias must deterministically mirror momentum alias map"
    )
    assert 0 <= cadence_24h_coverage_spread_trend_confidence_momentum_score <= 100, (
        f"{name}: cadence24hRecoveryTriadCoverageSpreadTrendConfidenceMomentumScore must stay within 0..100 domain"
    )
    assert (
        "cadence 24h recovery triad pulse palette alias (combat/vfx): "
        "**TSDCAD24TRIP:CV=SPARK|DW=ANCHOR|SO=LOCK**"
        in md_text
    ), f"{name}: markdown output must include compact triad pulse palette alias row"
    assert (
        "cadence 24h recovery triad bucket coverage alias (systems/ops): "
        f"**TSDCAD24TRICOV:{expected_cadence_24h_coverage_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad bucket coverage alias row"
    assert (
        "cadence 24h recovery triad coverage pressure alias (systems/ops): "
        f"**TSDCAD24TRICOVP:{expected_cadence_24h_coverage_pressure_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-pressure alias row"
    assert (
        "cadence 24h recovery triad coverage spread alias (design/world): "
        f"**TSDCAD24TRICOVS:{expected_cadence_24h_coverage_spread_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread alias row"
    assert (
        "cadence 24h recovery triad coverage spread trend (ai-content/combat): "
        f"**TSDCAD24TRICOVST:{cadence_24h_coverage_spread_trend}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend row"
    assert (
        "cadence 24h recovery triad coverage spread trend alias (systems/qa): "
        f"**TSDCAD24TRICOVSTA:{cadence_24h_coverage_spread_trend_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend alias row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence (ai-content/combat): "
        f"**TSDCAD24TRICOVSTC:{cadence_24h_coverage_spread_trend_confidence}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence alias (systems/qa): "
        f"**TSDCAD24TRICOVSTCA:{cadence_24h_coverage_spread_trend_confidence_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence alias row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum (ai-content/combat): "
        f"**TSDCAD24TRICOVSTCM:{cadence_24h_coverage_spread_trend_confidence_momentum}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum alias (systems/qa): "
        f"**TSDCAD24TRICOVSTCMA:{cadence_24h_coverage_spread_trend_confidence_momentum_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum alias row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score (ai-content/combat): "
        f"**TSDCAD24TRICOVSTCMS:{cadence_24h_coverage_spread_trend_confidence_momentum_score}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum score row"
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue(
            cadence_24h_coverage_spread_trend_confidence_momentum_score
        )
    )
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias(
            expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue
        )
    )
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory(
            rows
        )
    )
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory_alias = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory_alias(
            expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory
        )
    )
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band(
            rows
        )
    )
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score(
            rows
        )
    )
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias(
            expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score
        )
    )
    expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_trend = (
        load_guardrail_module().resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_trend(
            rows
        )
    )
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue (combat/vfx): "
        f"**TSDCAD24TRICOVSTCMSV:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum score vfx cue row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue alias (systems/qa): "
        f"**TSDCAD24TRICOVSTCMSVA:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum score vfx cue alias row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis advisory (ai-content/combat): "
        f"**TSDCAD24TRICOVSTCMSVH:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis advisory row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis advisory alias (systems/qa): "
        f"**TSDCAD24TRICOVSTCMSVHA:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis advisory alias row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence band (ai-content/combat): "
        f"**TSDCAD24TRICOVSTCMSVHC:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence-band row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence drift score (ai-content/combat): "
        f"**TSDCAD24TRICOVSTCMSVHCS:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence drift-score row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence drift score alias (systems/qa): "
        f"**TSDCAD24TRICOVSTCMSVHCSA:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence drift-score alias row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence drift-score trend (ai-content/combat): "
        f"**TSDCAD24TRICOVSTCMSVHCST:{expected_cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_trend}**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence drift-score trend row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score ladder decode (design/world): "
        "**TSDCAD24TRICOVSTCMS legend (80=surge confidence, 50=hold confidence, 20=cool confidence)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad momentum-score ladder decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score ladder dos-width eval (design/world): "
        "**TSDCAD24TRICOVSTCMSLEN:B59|C26|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad momentum-score ladder dos-width eval row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum decode (design/world): "
        "**TSDCAD24TRICOVSTCMA legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue decode (design/world): "
        "**TSDCAD24TRICOVSTCMSV legend (GLINT=calm flicker, PULSE=steady pressure, BLAST=full commit)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum score vfx cue decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue alias decode (design/world): "
        "**TSDCAD24TRICOVSTCMSVA legend (G=GLINT, P=PULSE, B=BLAST)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence momentum score vfx cue alias decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis advisory decode (design/world): "
        "**TSDCAD24TRICOVSTCMSVH legend (STEADY=stable cue, SWING=cue churn)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis advisory decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis advisory alias decode (design/world): "
        "**TSDCAD24TRICOVSTCMSVHA legend (S=stable cue, W=cue churn)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis advisory alias decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence band decode (design/world): "
        "**TSDCAD24TRICOVSTCMSVHC legend (LOW=high flip churn, MID=mixed flips, HIGH=stable cues)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence-band decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence drift score alias decode (design/world): "
        "**TSDCAD24TRICOVSTCMSVHCSA legend (L=<50 stability, M=50-79, H>=80)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence drift-score alias decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence drift-score trend decode (design/world): "
        "**TSDCAD24TRICOVSTCMSVHCST legend (UP=stabilizing, FLAT=holding, DOWN=destabilizing)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence drift-score trend decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue dual-hysteresis decode helper (design/world): "
        "**TSDCAD24TRICOVSTCMSVHD:VH=STEADY|SWING, VHA=S|W**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad dual-hysteresis decode helper row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue dual-hysteresis decode helper dos-width eval (design/world): "
        "**TSDCAD24TRICOVSTCMSVHDLEN:B24|C24|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad dual-hysteresis decode helper dos-width eval row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue confidence-band dual decode helper (design/world): "
        "**TSDCAD24TRICOVSTCMSVHCD:VHC=LOW|MID|HIGH, VHCA=L|M|H**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad confidence-band dual decode helper row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue confidence-band dual decode helper dos-width eval (design/world): "
        "**TSDCAD24TRICOVSTCMSVHCDLEN:B28|C28|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad confidence-band dual decode helper dos-width eval row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence momentum score vfx cue hysteresis confidence-band alias decode dos-width eval (design/world): "
        "**TSDCAD24TRICOVSTCMSVHCALEN:B42|C42|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad vfx-cue hysteresis confidence-band alias decode dos-width eval row"
    assert (
        "cadence 24h recovery triad coverage spread trend confidence decode (design/world): "
        "**TSDCAD24TRICOVSTCA legend (L=LOW, M=MID, H=HIGH)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend confidence decode row"
    assert (
        "cadence 24h recovery triad coverage spread trend decode (design/world): "
        "**TSDCAD24TRICOVSTA legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include cadence-triad coverage-spread trend decode row"
    cadence_24h_triad_rows = md_text.count("**TSDCAD24TRI:")
    cadence_24h_triad_palette_rows = md_text.count("**TSDCAD24TRIP:CV=SPARK|DW=ANCHOR|SO=LOCK**")
    cadence_24h_triad_coverage_rows = md_text.count("**TSDCAD24TRICOV:")
    cadence_24h_triad_coverage_pressure_rows = md_text.count("**TSDCAD24TRICOVP:")
    cadence_24h_triad_coverage_spread_rows = md_text.count("**TSDCAD24TRICOVS:")
    cadence_24h_triad_coverage_spread_trend_rows = md_text.count("**TSDCAD24TRICOVST:")
    cadence_24h_triad_coverage_spread_trend_alias_rows = md_text.count("**TSDCAD24TRICOVSTA:")
    cadence_24h_triad_coverage_spread_trend_confidence_rows = md_text.count("**TSDCAD24TRICOVSTC:")
    cadence_24h_triad_coverage_spread_trend_confidence_alias_rows = md_text.count("**TSDCAD24TRICOVSTCA:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_rows = md_text.count("**TSDCAD24TRICOVSTCM:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_alias_rows = md_text.count("**TSDCAD24TRICOVSTCMA:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_rows = md_text.count("**TSDCAD24TRICOVSTCMS:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_rows = md_text.count("**TSDCAD24TRICOVSTCMSV:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_rows = md_text.count("**TSDCAD24TRICOVSTCMSVA:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_rows = md_text.count("**TSDCAD24TRICOVSTCMSVH:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHA:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHC:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHCS:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHCSA:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHD:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_eval_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHDLEN:B24|C24|LIM72|PREF:COMPACT|PASS**")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHCD:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_eval_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHCDLEN:B28|C28|LIM72|PREF:COMPACT|PASS**")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHCA:")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_eval_rows = md_text.count("**TSDCAD24TRICOVSTCMSVHCALEN:B42|C42|LIM72|PREF:COMPACT|PASS**")
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_alias_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMA legend (U=UP, F=FLAT, D=DOWN)**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_ladder_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMS legend (80=surge confidence, 50=hold confidence, 20=cool confidence)**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_ladder_eval_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMSLEN:B59|C26|LIM72|PREF:COMPACT|PASS**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMSV legend (GLINT=calm flicker, PULSE=steady pressure, BLAST=full commit)**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMSVA legend (G=GLINT, P=PULSE, B=BLAST)**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMSVH legend (STEADY=stable cue, SWING=cue churn)**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMSVHA legend (S=stable cue, W=cue churn)**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCMSVHC legend (LOW=high flip churn, MID=mixed flips, HIGH=stable cues)**"
    )
    cadence_24h_triad_coverage_spread_trend_confidence_alias_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTCA legend (L=LOW, M=MID, H=HIGH)**"
    )
    cadence_24h_triad_coverage_spread_trend_alias_legend_rows = md_text.count(
        "**TSDCAD24TRICOVSTA legend (U=UP, F=FLAT, D=DOWN)**"
    )
    assert cadence_24h_triad_palette_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRIP row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOV row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_pressure_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVP row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVS row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVST row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_alias_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTA row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTC row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_alias_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCA row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCM row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_alias_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMA row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMS row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSV row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVA row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVH row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHA row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_rows == cadence_24h_triad_rows, (
        f"{name}: regression row-count parity assertion requires TSDCAD24TRICOVSTCMSVHCA to mirror TSDCAD24TRI across summary/token sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHC row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHCS row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHCSA row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHD row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_eval_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHDLEN row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHCD row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_eval_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHCDLEN row count must match TSDCAD24TRI row count across sections"
    )
    assert cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_eval_rows == cadence_24h_triad_rows, (
        f"{name}: TSDCAD24TRICOVSTCMSVHCALEN row count must match TSDCAD24TRI row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_eval_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCALEN row count must mirror TSDCAD24TRICOVSTCMSVHCA across summary/token sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_ladder_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMS legend row count must match TSDCAD24TRICOVSTCMS row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_ladder_eval_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSLEN row count must match TSDCAD24TRICOVSTCMS row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSV legend row count must match TSDCAD24TRICOVSTCMSV row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVA legend row count must match TSDCAD24TRICOVSTCMSVA row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_rows
    ), (
        f"{name}: fixture-level explicit parity assertion requires TSDCAD24TRICOVSTCMSVA legend row count to mirror TSDCAD24TRICOVSTCMSVA across summary/token sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVH legend row count must match TSDCAD24TRICOVSTCMSVH row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVHA legend row count must match TSDCAD24TRICOVSTCMSVHA row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVHC legend row count must match TSDCAD24TRICOVSTCMSVHC row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_alias_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_alias_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCMA legend row count must match TSDCAD24TRICOVSTCMA row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_momentum_alias_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_momentum_alias_rows
    ), (
        f"{name}: fixture-level explicit parity assertion requires TSDCAD24TRICOVSTCMA legend row count to mirror TSDCAD24TRICOVSTCMA across summary/token sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_confidence_alias_legend_rows
        == cadence_24h_triad_coverage_spread_trend_confidence_alias_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTCA legend row count must match TSDCAD24TRICOVSTCA row count across sections"
    )
    assert (
        cadence_24h_triad_coverage_spread_trend_alias_legend_rows
        == cadence_24h_triad_coverage_spread_trend_alias_rows
    ), (
        f"{name}: TSDCAD24TRICOVSTA legend row count must match TSDCAD24TRICOVSTA row count across sections"
    )
    cadence_24h_lines = md_text.splitlines()
    cadence_24h_triad_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRI:" in line
    ]
    cadence_24h_token_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24:" in line
    ]
    cadence_24h_coverage_pressure_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVP:" in line
    ]
    cadence_24h_coverage_spread_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVS:" in line
    ]
    cadence_24h_coverage_spread_trend_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVST:" in line
    ]
    cadence_24h_coverage_spread_trend_alias_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTA:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTC:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_alias_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCA:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCM:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_alias_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMA:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMS:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSV:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVA:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVH:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHA:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHC:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHCS:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHCSA:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHD:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_eval_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHDLEN:B24|C24|LIM72|PREF:COMPACT|PASS**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHCD:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_eval_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHCDLEN:B28|C28|LIM72|PREF:COMPACT|PASS**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHCA:" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_eval_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSVHCALEN:B42|C42|LIM72|PREF:COMPACT|PASS**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_legend_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "**TSDCAD24TRICOVSTCMS legend (80=surge confidence, 50=hold confidence, 20=cool confidence)**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_eval_indexes = [
        i for i, line in enumerate(cadence_24h_lines) if "**TSDCAD24TRICOVSTCMSLEN:B59|C26|LIM72|PREF:COMPACT|PASS**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_legend_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "**TSDCAD24TRICOVSTCMSV legend (GLINT=calm flicker, PULSE=steady pressure, BLAST=full commit)**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_legend_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "**TSDCAD24TRICOVSTCMSVA legend (G=GLINT, P=PULSE, B=BLAST)**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "**TSDCAD24TRICOVSTCMSVH legend (STEADY=stable cue, SWING=cue churn)**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_lines = [
        cadence_24h_lines[i]
        for i in cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_indexes
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "**TSDCAD24TRICOVSTCMSVHA legend (S=stable cue, W=cue churn)**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_legend_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "**TSDCAD24TRICOVSTCMSVHC legend (LOW=high flip churn, MID=mixed flips, HIGH=stable cues)**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_legend_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "**TSDCAD24TRICOVSTCMSVHCSA legend (L=<50 stability, M=50-79, H>=80)**" in line
    ]
    cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_lines = [
        cadence_24h_lines[i]
        for i in cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes
    ]
    cadence_24h_triad_plan_indexes = [
        i
        for i, line in enumerate(cadence_24h_lines)
        if "cadence 24h recovery triad plan (design/world): **" in line
    ]
    assert len(cadence_24h_triad_indexes) == len(cadence_24h_token_indexes), (
        f"{name}: TSDCAD24TRI row count must match TSDCAD24 row count across sections"
    )
    assert len(cadence_24h_coverage_pressure_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVP row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVS row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVST row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_alias_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTA row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTC row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_alias_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCA row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCM row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_alias_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMA row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMS row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSV row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVH row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHA row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHC row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCS row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHD row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_eval_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHDLEN row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCD row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_eval_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCDLEN row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCA row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_eval_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCALEN row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_eval_indexes) == len(
        cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCALEN row count must mirror TSDCAD24TRICOVSTCMSVHCA across summary/token sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_legend_indexes) == len(
        cadence_24h_triad_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMS legend row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_eval_indexes) == len(
        cadence_24h_triad_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSLEN row count must match TSDCAD24TRI row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_legend_indexes) == len(
        cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSV legend row count must match TSDCAD24TRICOVSTCMSV row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_indexes) == len(
        cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVH legend row count must match TSDCAD24TRICOVSTCMSVH row count across sections"
    )
    for legend_line in cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_lines:
        legend_token = legend_line.split("**", 2)[1]
        assert len(legend_token) <= 72, (
            f"{name}: TSDCAD24TRICOVSTCMSVH legend must stay <=72 chars in both summary/token sections"
        )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes) == len(
        cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVHA legend row count must match TSDCAD24TRICOVSTCMSVHA row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_legend_indexes) == len(
        cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVHC legend row count must match TSDCAD24TRICOVSTCMSVHC row count across sections"
    )
    assert len(cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_legend_indexes) == len(
        cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_indexes
    ), (
        f"{name}: TSDCAD24TRICOVSTCMSVHCSA legend row count must match TSDCAD24TRICOVSTCMSVHCSA row count across sections"
    )
    for legend_line in cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_lines:
        legend_token = legend_line.split("**", 2)[1]
        assert len(legend_token) <= 72, (
            f"{name}: TSDCAD24TRICOVSTCMSVHA legend must stay <=72 chars in both summary/token sections"
        )
    assert len(cadence_24h_triad_plan_indexes) == len(cadence_24h_triad_indexes), (
        f"{name}: cadence 24h recovery triad plan row count must match TSDCAD24TRI row count across sections"
    )
    for cluster_i in range(len(cadence_24h_triad_indexes)):
        assert cadence_24h_token_indexes[cluster_i] == cadence_24h_triad_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRI immediately before TSDCAD24 in both sections"
        )
        assert cadence_24h_coverage_spread_indexes[cluster_i] == cadence_24h_coverage_pressure_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVS immediately after TSDCAD24TRICOVP in both sections"
        )
        assert cadence_24h_coverage_spread_trend_indexes[cluster_i] == cadence_24h_coverage_spread_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVST immediately after TSDCAD24TRICOVS in both sections"
        )
        assert cadence_24h_coverage_spread_trend_alias_indexes[cluster_i] == cadence_24h_coverage_spread_trend_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTA immediately after TSDCAD24TRICOVST in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_indexes[cluster_i] == cadence_24h_coverage_spread_trend_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTC immediately after TSDCAD24TRICOVSTA in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_alias_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCA immediately after TSDCAD24TRICOVSTC in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCM immediately after TSDCAD24TRICOVSTCA in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_alias_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMA immediately after TSDCAD24TRICOVSTCM in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMS immediately after TSDCAD24TRICOVSTCMA in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSV immediately after TSDCAD24TRICOVSTCMS in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVA immediately after TSDCAD24TRICOVSTCMSV in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVH immediately after TSDCAD24TRICOVSTCMSVA in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHA immediately after TSDCAD24TRICOVSTCMSVH in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHC immediately after TSDCAD24TRICOVSTCMSVHA in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHCS immediately after TSDCAD24TRICOVSTCMSVHC in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHCSA immediately after TSDCAD24TRICOVSTCMSVHCS in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_legend_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_indexes[cluster_i] + 2, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMS legend two rows after TSDCAD24TRICOVSTCMSVHCS in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_eval_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSLEN immediately after TSDCAD24TRICOVSTCMS legend in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_legend_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_ladder_eval_indexes[cluster_i] + 4, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSV legend after cadence decode cluster in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_legend_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVA legend immediately after TSDCAD24TRICOVSTCMSV legend in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVH legend immediately after TSDCAD24TRICOVSTCMSVA legend in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHA legend immediately after TSDCAD24TRICOVSTCMSVH legend in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_legend_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHC legend immediately after TSDCAD24TRICOVSTCMSVHA legend in both sections"
        )
        assert cadence_24h_triad_plan_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes[cluster_i] + 7, (
            f"{name}: cadence order must keep triad plan row immediately after TSDCAD24TRICOVSTCMS decode rows in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_indexes[cluster_i] == cadence_24h_triad_plan_indexes[cluster_i] + 1, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHCA immediately after cadence 24h triad plan in both sections"
        )
        assert cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_eval_indexes[cluster_i] == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_alias_indexes[cluster_i] + 2, (
            f"{name}: cadence order must keep TSDCAD24TRICOVSTCMSVHCALEN two rows after TSDCAD24TRICOVSTCMSVHCA in both sections"
        )
        assert (
            cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_alias_legend_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_legend_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_alias_legend_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_legend_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_legend_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_legend_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_drift_score_alias_legend_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_eval_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_dual_helper_eval_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_indexes[cluster_i] + 1
            == cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_eval_indexes[cluster_i]
            and cadence_24h_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band_dual_helper_eval_indexes[cluster_i] + 1
            == cadence_24h_triad_plan_indexes[cluster_i]
        ), (
            f"{name}: cadence order must keep hysteresis decode legends + dual helper rows adjacent and directly before triad plan row in both sections"
        )

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
        "trend-score dispatch pressure base class (pre-cadence override): "
        f"**{expected_dispatch_pressure_base_class}**"
        in md_text
    ), f"{name}: markdown output must include deterministic pre-override dispatch-pressure class row"
    assert (
        "trend-score dispatch pressure cadence override: "
        f"**TSDPCO:{expected_dispatch_pressure_cadence_override_alias}** "
        f"({expected_dispatch_pressure_cadence_override_state}, bucket=combat-or-vfx)"
        in md_text
    ), f"{name}: markdown output must include deterministic cadence-override contract row"
    assert (
        "trend-score dispatch pressure cadence override streak: "
        f"**TSDPCOS:{expected_dispatch_pressure_cadence_override_streak}**"
        in md_text
    ), f"{name}: markdown output must include deterministic cadence-override streak row"
    expected_cadence_note = (
        "PUSH"
        if expected_dispatch_pressure_cadence_override_streak >= 2
        or expected_dispatch_pressure_momentum_slope == "SURGING"
        else "WATCH"
        if expected_dispatch_pressure_cadence_override_streak == 1
        or expected_dispatch_pressure_momentum_slope == "RISING"
        else "HOLD"
    )
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideNote")
        == expected_cadence_note
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideNote must map deterministic HOLD/WATCH/PUSH note from streak+slope"
    expected_cadence_note_alias = {"HOLD": "H", "WATCH": "W", "PUSH": "P"}[expected_cadence_note]
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideNoteAlias")
        == expected_cadence_note_alias
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteAlias must mirror deterministic compact HOLD/WATCH/PUSH alias"
    assert (
        "trend-score dispatch pressure cadence override note (ai-content/design, offline): "
        f"**TSDPCO NOTE:{expected_cadence_note}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-override note row"
    assert (
        "trend-score dispatch pressure cadence override note alias: "
        f"**TSDPCON:{expected_cadence_note_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-override note alias row"
    expected_cadence_note_rationale = (
        "push"
        if expected_cadence_note == "PUSH"
        or expected_dispatch_pressure_momentum_slope == "SURGING"
        else "watch"
        if expected_cadence_note == "WATCH"
        or expected_dispatch_pressure_momentum_slope == "RISING"
        else "steady"
    )
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideNoteRationale")
        == expected_cadence_note_rationale
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationale must map deterministic steady/watch/push rationale from note+slope"
    expected_cadence_note_rationale_alias = {
        "steady": "S",
        "watch": "W",
        "push": "P",
    }[expected_cadence_note_rationale]
    assert (
        report.get("trendScoreBandDispatchPressureCadenceOverrideNoteRationaleAlias")
        == expected_cadence_note_rationale_alias
    ), f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleAlias must mirror deterministic compact rationale alias"
    assert (
        "trend-score dispatch pressure cadence override note rationale (ai-content/design, offline): "
        f"**TSDPCON WHY:{expected_cadence_note_rationale}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-note rationale row"
    confidence_value = report.get("trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidence")
    assert confidence_value in {"LOW", "MID", "HIGH"}, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidence must stay within LOW|MID|HIGH"
    )
    confidence_alias_value = report.get("trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceAlias")
    expected_confidence_alias = {"LOW": "L", "MID": "M", "HIGH": "H"}[confidence_value]
    assert confidence_alias_value == expected_confidence_alias, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceAlias must mirror LOW|MID|HIGH alias"
    )
    confidence_trend_value = report.get("trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrend")
    assert confidence_trend_value in {"UP", "FLAT", "DOWN"}, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrend must stay within UP|FLAT|DOWN"
    )
    confidence_trend_alias_value = report.get("trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendAlias")
    expected_confidence_trend_alias = {"UP": "U", "FLAT": "F", "DOWN": "D"}[confidence_trend_value]
    assert confidence_trend_alias_value == expected_confidence_trend_alias, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendAlias must mirror UP|FLAT|DOWN alias"
    )
    confidence_trend_momentum_score = report.get(
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumScore"
    )
    assert isinstance(confidence_trend_momentum_score, int) and 0 <= confidence_trend_momentum_score <= 100, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumScore must stay in 0..100"
    )
    confidence_trend_momentum_band = report.get(
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBand"
    )
    assert confidence_trend_momentum_band in {"LOW", "MID", "HIGH"}, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBand must stay within LOW|MID|HIGH"
    )
    confidence_trend_momentum_band_alias = report.get(
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandAlias"
    )
    expected_confidence_trend_momentum_band_alias = {"LOW": "L", "MID": "M", "HIGH": "H"}[confidence_trend_momentum_band]
    assert confidence_trend_momentum_band_alias == expected_confidence_trend_momentum_band_alias, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandAlias must mirror LOW|MID|HIGH alias"
    )
    confidence_trend_momentum_band_trend = report.get(
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrend"
    )
    assert confidence_trend_momentum_band_trend in {"UP", "FLAT", "DOWN"}, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrend must stay within UP|FLAT|DOWN"
    )
    confidence_trend_momentum_band_trend_alias = report.get(
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrendAlias"
    )
    expected_confidence_trend_momentum_band_trend_alias = {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }[confidence_trend_momentum_band_trend]
    assert confidence_trend_momentum_band_trend_alias == expected_confidence_trend_momentum_band_trend_alias, (
        f"{name}: trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrendAlias must mirror UP|FLAT|DOWN alias"
    )
    expected_fx_urgency_cue = {
        "DOWN": "SOFT",
        "FLAT": "SURGE",
        "UP": "SPIKE",
    }[confidence_trend_momentum_band_trend]
    expected_fx_urgency_cue_alias = {
        "SOFT": "S",
        "SURGE": "U",
        "SPIKE": "P",
    }[expected_fx_urgency_cue]
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxUrgencyCue")
        == expected_fx_urgency_cue
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCue must deterministically map from TSDPCONWCTSBT"
    )
    assert (
        report.get("trendScoreBandDispatchPressureMomentumFxUrgencyCueAlias")
        == expected_fx_urgency_cue_alias
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueAlias must mirror SOFT|SURGE|SPIKE alias"
    )
    urgency_confidence_value = report.get("trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidence")
    assert urgency_confidence_value in {"LOW", "MID", "HIGH"}, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidence must stay within LOW|MID|HIGH"
    )
    expected_urgency_confidence_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence(rows)
    )
    assert urgency_confidence_value == expected_urgency_confidence_value, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidence must deterministically map from recent TSDPCONWCTSBT churn"
    )
    urgency_confidence_trend_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrend"
    )
    assert urgency_confidence_trend_value in {"UP", "FLAT", "DOWN"}, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrend must stay within UP|FLAT|DOWN"
    )
    expected_urgency_confidence_trend_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend(rows)
    )
    assert urgency_confidence_trend_value == expected_urgency_confidence_trend_value, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrend must deterministically map from consecutive TSDPMFXUC windows"
    )
    urgency_confidence_trend_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendAlias"
    )
    expected_urgency_confidence_trend_alias_value = {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }[urgency_confidence_trend_value]
    assert urgency_confidence_trend_alias_value == expected_urgency_confidence_trend_alias_value, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendAlias must mirror UP|FLAT|DOWN alias"
    )
    urgency_confidence_trend_momentum_score_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumScore"
    )
    assert isinstance(urgency_confidence_trend_momentum_score_value, int), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumScore must be an int"
    )
    assert 0 <= urgency_confidence_trend_momentum_score_value <= 100, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumScore must stay within 0..100"
    )
    expected_urgency_confidence_trend_momentum_score_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score(rows)
    )
    assert (
        urgency_confidence_trend_momentum_score_value
        == expected_urgency_confidence_trend_momentum_score_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumScore must deterministically map from weighted TSDPMFXUCT drift"
    )
    urgency_confidence_trend_momentum_band_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBand"
    )
    assert urgency_confidence_trend_momentum_band_value in {"LOW", "MID", "HIGH"}, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBand must stay within LOW|MID|HIGH"
    )
    expected_urgency_confidence_trend_momentum_band_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band(
            urgency_confidence_trend_momentum_score_value
        )
    )
    assert (
        urgency_confidence_trend_momentum_band_value
        == expected_urgency_confidence_trend_momentum_band_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBand must deterministically map from TSDPMFXUCTS buckets"
    )
    urgency_confidence_trend_momentum_band_trend_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrend"
    )
    assert urgency_confidence_trend_momentum_band_trend_value in {"UP", "FLAT", "DOWN"}, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrend must stay within UP|FLAT|DOWN"
    )
    prior_urgency_confidence_trend_momentum_score_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score(
            rows[:-1] if len(rows) > 1 else rows
        )
    )
    prior_urgency_confidence_trend_momentum_band_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band(
            prior_urgency_confidence_trend_momentum_score_value
        )
    )
    expected_urgency_confidence_trend_momentum_band_trend_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend(
            urgency_confidence_trend_momentum_band_value,
            prior_urgency_confidence_trend_momentum_band_value,
        )
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_value
        == expected_urgency_confidence_trend_momentum_band_trend_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrend must deterministically map from consecutive TSDPMFXUCTSB windows"
    )
    urgency_confidence_trend_momentum_band_trend_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendAlias"
    )
    expected_urgency_confidence_trend_momentum_band_trend_alias_value = {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }[urgency_confidence_trend_momentum_band_trend_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_alias_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendAlias must mirror UP|FLAT|DOWN alias"
    )
    urgency_confidence_trend_momentum_band_trend_confidence_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendConfidence"
    )
    assert urgency_confidence_trend_momentum_band_trend_confidence_value in {"LOW", "MID", "HIGH"}, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendConfidence must stay within LOW|MID|HIGH"
    )
    prior_urgency_confidence_trend_momentum_band_trend_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend(
            prior_urgency_confidence_trend_momentum_band_value,
            load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band(
                load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score(
                    rows[:-2] if len(rows) > 2 else rows[:-1] if len(rows) > 1 else rows
                )
            ),
        )
    )
    expected_urgency_confidence_trend_momentum_band_trend_confidence_value = (
        load_guardrail_module().resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_confidence(
            urgency_confidence_trend_momentum_band_trend_value,
            prior_urgency_confidence_trend_momentum_band_trend_value,
        )
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_confidence_value
        == expected_urgency_confidence_trend_momentum_band_trend_confidence_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendConfidence must deterministically map from consecutive TSDPMFXUCTSBTA stability windows"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulse"
    )
    assert urgency_confidence_trend_momentum_band_trend_vfx_pulse_value in {"CALM", "PULSE", "BLAST"}, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulse must stay within CALM|PULSE|BLAST"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_value = {
        "UP": "BLAST",
        "FLAT": "PULSE",
        "DOWN": "CALM",
    }[urgency_confidence_trend_momentum_band_trend_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulse must deterministically map from TSDPMFXUCTSBT"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseAlias"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_value = {
        "CALM": "C",
        "PULSE": "P",
        "BLAST": "B",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseAlias must mirror CALM|PULSE|BLAST alias"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidance"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_value = {
        "CALM": "steady sweep",
        "PULSE": "brace lanes",
        "BLAST": "commit burst",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidance must map deterministically from TSDPMFXV"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidence"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value = {
        "steady sweep": "HIGH",
        "brace lanes": "MID",
        "commit burst": "LOW",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidence must map deterministically from TSDPMFXVW"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceAlias"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_value = {
        "LOW": "L",
        "MID": "M",
        "HIGH": "H",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceAlias must mirror LOW|MID|HIGH alias"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendation"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value = {
        "HIGH": "lock sweep",
        "MID": "brace check",
        "LOW": "burst triage",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendation must map deterministically from TSDPMFXVWC"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationAlias"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_value = {
        "lock sweep": "LS",
        "brace check": "BC",
        "burst triage": "BT",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationAlias must mirror recommendation alias map"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensity"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_value = {
        "lock sweep": "HARD",
        "brace check": "EDGE",
        "burst triage": "SOFT",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensity must map deterministically from TSDPMFXVWCR"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityAlias"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_value = {
        "SOFT": "S",
        "EDGE": "E",
        "HARD": "H",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityAlias must mirror intensity alias map"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrend"
    )
    assert urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_value in {
        "UP",
        "FLAT",
        "DOWN",
    }, (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrend must stay in UP|FLAT|DOWN"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendAlias"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_value = {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendAlias must mirror trend alias map"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScore"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePosture"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureAlias"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureMicrocopy"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureMicrocopyAlias"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value = {
        "UP": 80,
        "FLAT": 50,
        "DOWN": 20,
    }[urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_value]
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value = (
        "SURGE"
        if urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value >= 70
        else "HOLD"
        if urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value >= 40
        else "COOL"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_value = {
        "COOL": "C",
        "HOLD": "H",
        "SURGE": "S",
    }[expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value]
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_value = {
        "SURGE": "push now",
        "HOLD": "hold lane",
        "COOL": "ease lane",
    }[expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value]
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_value = {
        "SURGE": "PN",
        "HOLD": "HL",
        "COOL": "EL",
    }[expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value]
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScoreBeat"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value = (
        "SHATTER"
        if urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value >= 70
        else "PULSE"
        if urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value >= 40
        else "GLIDE"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScoreBeatAlias"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScoreBeatMicrocopy"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopy"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyAlias"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_value = report.get(
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScorePostureBeatBridgeMicrocopyCompactSummary"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_value = {
        "GLIDE": "G",
        "PULSE": "P",
        "SHATTER": "S",
    }[expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value]
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_value = {
        "GLIDE": "steady nudge",
        "PULSE": "pressure poke",
        "SHATTER": "hard crack",
    }[expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value]
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_value = (
        f"{expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_value}"
        f" / {expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_value}"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_alias_value = {
        "GLIDE": "SN",
        "PULSE": "PP",
        "SHATTER": "HC",
    }[expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value]
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_value = (
        f"{expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_value}"
        f"/{expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_alias_value}"
    )
    expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_value = {
        "push now / hard crack": "PNHC",
        "push now / pressure poke": "PNPP",
        "push now / steady nudge": "PNSN",
        "hold lane / hard crack": "HLHC",
        "hold lane / pressure poke": "HLPP",
        "hold lane / steady nudge": "HLSN",
        "ease lane / hard crack": "ELHC",
        "ease lane / pressure poke": "ELPP",
        "ease lane / steady nudge": "ELSN",
    }[expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_value]
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value
    ), (
        f"{name}: trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendScore must mirror intensity-trend score map"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value
    ), (
        f"{name}: ...IntensityTrendScorePosture must mirror trend-score posture buckets"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_value
    ), (
        f"{name}: ...IntensityTrendScorePostureAlias must mirror posture alias map"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_value
    ), (
        f"{name}: ...IntensityTrendScorePostureMicrocopy must mirror posture microcopy map"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_value
    ), (
        f"{name}: ...IntensityTrendScorePostureMicrocopyAlias must mirror posture microcopy alias map"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value
    ), (
        f"{name}: ...IntensityTrendScoreBeat must map score to GLIDE|PULSE|SHATTER deterministically"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_value
    ), (
        f"{name}: ...IntensityTrendScoreBeatAlias must mirror beat alias map"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_value
    ), (
        f"{name}: ...IntensityTrendScoreBeatMicrocopy must mirror beat microcopy map"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_value
    ), (
        f"{name}: ...IntensityTrendScorePostureBeatBridgeMicrocopy must concatenate posture + beat microcopy deterministically"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_value
    ), (
        f"{name}: ...IntensityTrendScorePostureBeatBridgeMicrocopyAlias must concatenate posture + beat alias deterministically"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_value
        == expected_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_value
    ), (
        f"{name}: ...IntensityTrendScorePostureBeatBridgeMicrocopyCompactSummary must map bridge microcopy to compact digest token deterministically"
    )
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence (ai-content/systems, offline): "
        f"**TSDPCON WHY CONF:{confidence_value}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-note rationale confidence row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence alias: "
        f"**TSDPCONWC:{confidence_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-note rationale confidence-alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation (ai-content/systems, offline): "
        f"**TSDPMFXVWCR:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias: "
        f"**TSDPMFXVWCRA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity (combat/vfx, offline): "
        f"**TSDPMFXVWCRI:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias: "
        f"**TSDPMFXVWCRIA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend (ai-content/systems, offline): "
        f"**TSDPMFXVWCRIT:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend alias: "
        f"**TSDPMFXVWCRITA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score (ai-content/systems, offline): "
        f"**TSDPMFXVWCRITS:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend score row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture (combat/vfx, offline): "
        f"**TSDPMFXVWCRITSP:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value}**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture alias: "
        f"**TSDPMFXVWCRITSPA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy (ai-content/systems, offline): "
        f"**TSDPMFXVWCRITSPM:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_value}**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture microcopy row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy alias: "
        f"**TSDPMFXVWCRITSPMA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture microcopy alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat (combat/vfx, offline): "
        f"**TSDPMFXVWCRITSB:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend beat row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat alias: "
        f"**TSDPMFXVWCRITSBA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend beat alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat microcopy (ai-content/systems, offline): "
        f"**TSDPMFXVWCRITSBM:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_value}**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend beat microcopy row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy (ai-content/systems, offline): "
        f"**TSDPMFXVWCRITSPMB:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_value}**"
        in md_text
    ), f"{name}: markdown output must include posture-beat bridge microcopy row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy alias: "
        f"**TSDPMFXVWCRITSPMBA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include posture-beat bridge microcopy alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat compact bridge-summary token (ai-content/design, offline): "
        f"**TSDPMFXVWCRITSPMBS:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_value}**"
        in md_text
    ), f"{name}: markdown output must include compact bridge-summary token row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat compact bridge-summary decode (design/world): "
        "**TSDPMFXVWCRITSPMBS legend (PNHC=push now/hard crack, HLPP=hold lane/pressure poke, ELSN=ease lane/steady nudge)**"
        in md_text
    ), f"{name}: markdown output must include compact bridge-summary decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation decode (design/world): "
        "**TSDPMFXVWCR legend (HIGH=lock sweep, MID=brace check, LOW=burst triage)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias decode (design/world): "
        "**TSDPMFXVWCRA legend (LS=lock sweep, BC=brace check, BT=burst triage)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity decode (design/world): "
        "**TSDPMFXVWCRI legend (SOFT=burst triage, EDGE=brace check, HARD=lock sweep)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias decode (design/world): "
        "**TSDPMFXVWCRIA legend (S=SOFT, E=EDGE, H=HARD)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend decode (design/world): "
        "**TSDPMFXVWCRIT legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend alias decode (design/world): "
        "**TSDPMFXVWCRITA legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score helper (design/world, dos-width): "
        "**TSDPMFXVWCRITSH helper (80=surge, 50=hold, 20=cool)**"
        in md_text
    ), f"{name}: markdown output must include compact trend-score helper row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture decode (design/world): "
        "**TSDPMFXVWCRITSP legend (SURGE=push tempo, HOLD=hold tempo, COOL=ease tempo)**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture alias decode (design/world): "
        "**TSDPMFXVWCRITSPA legend (S=SURGE, H=HOLD, C=COOL)**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy decode (design/world): "
        "**TSDPMFXVWCRITSPM legend (SURGE=push now, HOLD=hold lane, COOL=ease lane)**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture microcopy decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy alias decode (design/world): "
        "**TSDPMFXVWCRITSPMA legend (PN=push now, HL=hold lane, EL=ease lane)**"
        in md_text
    ), f"{name}: markdown output must include trend-score posture microcopy alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy decode dos-width eval (design/world): "
        "**TSDPMFXVWCRITSPMLEN:B46|C39|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include posture-microcopy decode DOS-width/readability evaluation row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy decode preference alias (design/world): "
        "**TSDPMFXVWCRITSPMP:C**"
        in md_text
    ), f"{name}: markdown output must include posture-microcopy decode preference alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat decode (design/world): "
        "**TSDPMFXVWCRITSB legend (GLIDE=stable drift, PULSE=active drift, SHATTER=hard pivot)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend beat decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat alias decode (design/world): "
        "**TSDPMFXVWCRITSBA legend (G=GLIDE, P=PULSE, S=SHATTER)**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation intensity trend beat alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat microcopy decode (design/world): "
        "**TSDPMFXVWCRITSBM legend (GLIDE=steady nudge, PULSE=pressure poke, SHATTER=hard crack)**"
        in md_text
    ), f"{name}: markdown output must include beat-microcopy decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy decode (design/world): "
        "**TSDPMFXVWCRITSPMB legend (SURGE/HOLD/COOL + SHATTER/PULSE/GLIDE => push now|hold lane|ease lane / hard crack|pressure poke|steady nudge)**"
        in md_text
    ), f"{name}: markdown output must include posture-beat bridge microcopy decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy alias decode (design/world): "
        "**TSDPMFXVWCRITSPMBA legend (PN|HL|EL / HC|PP|SN)**"
        in md_text
    ), f"{name}: markdown output must include posture-beat bridge microcopy alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy decode dos-width eval (design/world): "
        "**TSDPMFXVWCRITSPMBLEN:B109|C19|LIM72|PREF:COMPACT|WARN**"
        in md_text
    ), f"{name}: markdown output must include posture-beat bridge microcopy DOS-width/readability evaluation row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat ladder helper (design/world, dos-width): "
        "**TSDPMFXVWCRITSB helper (80=SHATTER, 50=PULSE, 20=GLIDE)**"
        in md_text
    ), f"{name}: markdown output must include beat-ladder helper row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat ladder helper dos-width eval (design/world): "
        "**TSDPMFXVWCRITSBLEN:B30|C16|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include beat-ladder helper DOS-width/readability evaluation row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias decode dos-width eval (design/world): "
        "**TSDPMFXVWCRALEN:B45|C43|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include guidance-confidence recommendation alias decode DOS-width/readability evaluation row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias decode dos-width eval (design/world): "
        "**TSDPMFXVWCRIALEN:F52|C22|LIM72|PREF:CONCISE|PASS**"
        in md_text
    ), f"{name}: markdown output must include concise intensity decode DOS-width/readability evaluation row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence trend (ai-content/systems, offline): "
        f"**TSDPCONWCT:{confidence_trend_value}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-note rationale confidence-trend row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence trend alias: "
        f"**TSDPCONWCTA:{confidence_trend_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-note rationale confidence-trend alias row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence trend momentum score (ai-content/systems, offline): "
        f"**TSDPCONWCTS:{confidence_trend_momentum_score}**"
        in md_text
    ), f"{name}: markdown output must include cadence-note rationale confidence-trend momentum score row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence trend momentum band (ai-content/systems, offline): "
        f"**TSDPCONWCTSB:{confidence_trend_momentum_band}**"
        in md_text
    ), f"{name}: markdown output must include cadence-note rationale confidence-trend momentum band row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence trend momentum band alias: "
        f"**TSDPCONWCTSBA:{confidence_trend_momentum_band_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-note rationale confidence-trend momentum band alias row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence trend momentum band trend (ai-content/systems, offline): "
        f"**TSDPCONWCTSBT:{confidence_trend_momentum_band_trend}**"
        in md_text
    ), f"{name}: markdown output must include cadence-note rationale confidence-trend momentum band trend row"
    assert (
        "trend-score dispatch pressure cadence override note rationale confidence trend momentum band trend alias: "
        f"**TSDPCONWCTSBTA:{confidence_trend_momentum_band_trend_alias}**"
        in md_text
    ), f"{name}: markdown output must include cadence-note rationale confidence-trend momentum band trend alias row"
    assert (
        "trend-score dispatch pressure cadence override note rationale alias: "
        f"**TSDPCONW:{expected_cadence_note_rationale_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact cadence-note rationale alias row"
    assert (
        "trend-score dispatch pressure cadence override note decode: "
        "**TSDPCON legend (H=HOLD, W=WATCH, P=PUSH)**"
        in md_text
    ), f"{name}: markdown output must include cadence-override note decode row"
    cadence_cluster_lines = md_text.splitlines()
    cadence_cluster_streak_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCOS:" in line
    ]
    cadence_cluster_note_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCO NOTE:" in line
    ]
    cadence_cluster_note_alias_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCON:" in line and "TSDPCON legend" not in line
    ]
    cadence_cluster_rationale_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCON WHY:" in line
    ]
    cadence_cluster_rationale_conf_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCON WHY CONF:" in line
    ]
    cadence_cluster_rationale_conf_alias_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWC:" in line
    ]
    cadence_cluster_rationale_conf_trend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCT:" in line
    ]
    cadence_cluster_rationale_conf_trend_alias_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTA:" in line
    ]
    cadence_cluster_rationale_conf_trend_momentum_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTS:" in line
    ]
    cadence_cluster_rationale_conf_trend_momentum_band_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTSB:" in line
    ]
    cadence_cluster_rationale_conf_trend_momentum_band_alias_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTSBA:" in line
    ]
    cadence_cluster_rationale_conf_trend_momentum_band_trend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTSBT:" in line
    ]
    cadence_cluster_rationale_conf_trend_momentum_band_trend_alias_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTSBTA:" in line
    ]
    cadence_cluster_rationale_alias_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONW:" in line
    ]
    cadence_cluster_note_legend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCON legend (H=HOLD, W=WATCH, P=PUSH)**" in line
    ]
    cadence_cluster_conf_legend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWC legend (L=LOW, M=MID, H=HIGH)**" in line
    ]
    cadence_cluster_conf_trend_legend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCT legend (U=UP, F=FLAT, D=DOWN)**" in line
    ]
    cadence_cluster_conf_trend_alias_legend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTA legend (U=UP, F=FLAT, D=DOWN)**" in line
    ]
    cadence_cluster_conf_trend_momentum_band_trend_legend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTSBT legend (U=UP, F=FLAT, D=DOWN)**" in line
    ]
    cadence_cluster_conf_trend_momentum_band_trend_alias_legend_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTSBTA legend (U=UP, F=FLAT, D=DOWN)**" in line
    ]
    cadence_cluster_trend_fx_pair_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPPAIR:TSDPCONWCTSBT=" in line
    ]
    cadence_cluster_trend_fx_pair_decode_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPCONWCTSBT U/F/D => TSDPMFXU SPIKE/SURGE/SOFT**" in line
    ]
    cadence_cluster_trend_fx_pair_alias_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPPAIRA:" in line
    ]
    cadence_cluster_trend_fx_pair_alias_decode_indexes = [
        i for i, line in enumerate(cadence_cluster_lines)
        if "**TSDPPAIRA legend (S=SOFT, U=SURGE, P=SPIKE)**" in line
    ]
    assert len(cadence_cluster_streak_indexes) >= 1, (
        f"{name}: cadence cluster streak row must appear in markdown summary"
    )
    assert len(cadence_cluster_note_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster note row count must match streak row count"
    )
    assert len(cadence_cluster_note_alias_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster note-alias row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_alias_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-alias row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_alias_indexes) == len(cadence_cluster_rationale_conf_indexes), (
        f"{name}: cadence cluster rationale-confidence-alias row count must mirror TSDPCON WHY CONF row count in both sections"
    )
    assert len(cadence_cluster_rationale_conf_trend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_indexes) == len(cadence_cluster_rationale_conf_alias_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend row count must mirror TSDPCONWC row count in both sections"
    )
    assert len(cadence_cluster_rationale_conf_trend_alias_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-alias row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_alias_indexes) == len(cadence_cluster_rationale_conf_trend_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-alias row count must mirror TSDPCONWCT row count in both sections"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-momentum row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_indexes) == len(cadence_cluster_rationale_conf_trend_alias_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-momentum row count must mirror TSDPCONWCTA row count in both sections"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-momentum-band row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_indexes) == len(cadence_cluster_rationale_conf_trend_momentum_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-momentum-band row count must mirror TSDPCONWCTS row count in both sections"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_alias_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-momentum-band-alias row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_trend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-momentum-band-trend row count must match streak row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_trend_alias_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-confidence-trend-momentum-band-trend-alias row count must match streak row count"
    )
    expected_cadence_cluster_rows = len(cadence_cluster_streak_indexes)
    assert expected_cadence_cluster_rows >= 1, (
        f"{name}: fixture-level cadence cluster must render at least one markdown section row"
    )
    assert len(cadence_cluster_rationale_conf_trend_indexes) == expected_cadence_cluster_rows, (
        f"{name}: fixture-level TSDPCONWCT row count must deterministically mirror cadence-cluster section row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_alias_indexes) == expected_cadence_cluster_rows, (
        f"{name}: fixture-level TSDPCONWCTA row count must deterministically mirror cadence-cluster section row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_indexes) == expected_cadence_cluster_rows, (
        f"{name}: fixture-level TSDPCONWCTS row count must deterministically mirror cadence-cluster section row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_indexes) == expected_cadence_cluster_rows, (
        f"{name}: fixture-level TSDPCONWCTSB row count must deterministically mirror cadence-cluster section row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_indexes) == len(cadence_cluster_rationale_conf_trend_momentum_indexes), (
        f"{name}: fixture-level TSDPCONWCTSB row count must deterministically mirror TSDPCONWCTS row count in both sections"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_alias_indexes) == expected_cadence_cluster_rows, (
        f"{name}: fixture-level TSDPCONWCTSBA row count must deterministically mirror cadence-cluster section row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_trend_indexes) == expected_cadence_cluster_rows, (
        f"{name}: fixture-level TSDPCONWCTSBT row count must deterministically mirror cadence-cluster section row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_trend_alias_indexes) == expected_cadence_cluster_rows, (
        f"{name}: fixture-level TSDPCONWCTSBTA row count must deterministically mirror cadence-cluster section row count"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_trend_indexes) == len(
        cadence_cluster_rationale_conf_trend_momentum_band_trend_alias_indexes
    ), (
        f"{name}: fixture-level TSDPCONWCTSBT row count must deterministically mirror TSDPCONWCTSBTA row count in both sections"
    )
    assert len(cadence_cluster_rationale_conf_trend_momentum_band_trend_indexes) == expected_cadence_cluster_rows and len(
        cadence_cluster_rationale_conf_trend_momentum_band_trend_alias_indexes
    ) == expected_cadence_cluster_rows, (
        f"{name}: mixed-cadence fixture matrix must keep TSDPCONWCTSBT/TSDPCONWCTSBTA row-count parity across summary + token sections"
    )
    assert len(cadence_cluster_rationale_alias_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster rationale-alias row count must match streak row count"
    )
    assert len(cadence_cluster_note_legend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster legend row count must match streak row count"
    )
    assert len(cadence_cluster_conf_legend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster confidence-legend row count must match streak row count"
    )
    assert len(cadence_cluster_conf_trend_legend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster confidence-trend-legend row count must match streak row count"
    )
    assert len(cadence_cluster_conf_trend_alias_legend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster confidence-trend-alias-legend row count must match streak row count"
    )
    assert len(cadence_cluster_conf_trend_momentum_band_trend_legend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster confidence-trend-momentum-band-trend-legend row count must match streak row count"
    )
    assert len(cadence_cluster_conf_trend_momentum_band_trend_alias_legend_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster confidence-trend-momentum-band-trend-alias-legend row count must match streak row count"
    )
    assert len(cadence_cluster_trend_fx_pair_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster trend->fx urgency pair row count must match streak row count"
    )
    assert len(cadence_cluster_trend_fx_pair_decode_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster trend->fx urgency pair-decode row count must match streak row count"
    )
    assert len(cadence_cluster_trend_fx_pair_alias_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster trend->fx urgency compact-alias row count must match streak row count"
    )
    assert len(cadence_cluster_trend_fx_pair_indexes) == len(cadence_cluster_trend_fx_pair_alias_indexes), (
        f"{name}: fixture-level TSDPPAIR row count must deterministically mirror TSDPPAIRA row count in both sections"
    )
    assert len(cadence_cluster_trend_fx_pair_indexes) == expected_cadence_cluster_rows and len(
        cadence_cluster_trend_fx_pair_alias_indexes
    ) == expected_cadence_cluster_rows, (
        f"{name}: mixed-cadence fixture matrix must keep TSDPPAIR/TSDPPAIRA row-count parity across summary + token sections"
    )
    assert len(cadence_cluster_trend_fx_pair_alias_decode_indexes) == len(cadence_cluster_streak_indexes), (
        f"{name}: cadence cluster trend->fx urgency compact-alias decode row count must match streak row count"
    )
    for cluster_i in range(len(cadence_cluster_streak_indexes)):
        assert cadence_cluster_note_indexes[cluster_i] == cadence_cluster_streak_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCOS immediately before TSDPCO NOTE in both sections"
        )
        assert cadence_cluster_note_alias_indexes[cluster_i] == cadence_cluster_note_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCO NOTE immediately before TSDPCON in both sections"
        )
        assert cadence_cluster_rationale_indexes[cluster_i] == cadence_cluster_note_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCON immediately before TSDPCON WHY in both sections"
        )
        assert cadence_cluster_rationale_conf_indexes[cluster_i] == cadence_cluster_rationale_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCON WHY immediately before TSDPCON WHY CONF in both sections"
        )
        assert cadence_cluster_rationale_conf_alias_indexes[cluster_i] == cadence_cluster_rationale_conf_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCON WHY CONF immediately before TSDPCONWC in both sections"
        )
        assert cadence_cluster_rationale_conf_trend_indexes[cluster_i] == cadence_cluster_rationale_conf_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWC immediately before TSDPCONWCT in both sections"
        )
        assert cadence_cluster_rationale_conf_trend_alias_indexes[cluster_i] == cadence_cluster_rationale_conf_trend_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCT immediately before TSDPCONWCTA in both sections"
        )
        assert cadence_cluster_rationale_conf_trend_momentum_indexes[cluster_i] == cadence_cluster_rationale_conf_trend_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTA immediately before TSDPCONWCTS in both sections"
        )
        assert cadence_cluster_rationale_conf_trend_momentum_band_indexes[cluster_i] == cadence_cluster_rationale_conf_trend_momentum_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTS immediately before TSDPCONWCTSB in both sections"
        )
        assert cadence_cluster_rationale_conf_trend_momentum_band_alias_indexes[cluster_i] == cadence_cluster_rationale_conf_trend_momentum_band_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTSB immediately before TSDPCONWCTSBA in both sections"
        )
        assert cadence_cluster_rationale_conf_trend_momentum_band_trend_indexes[cluster_i] == cadence_cluster_rationale_conf_trend_momentum_band_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTSBA immediately before TSDPCONWCTSBT in both sections"
        )
        assert cadence_cluster_rationale_conf_trend_momentum_band_trend_alias_indexes[cluster_i] == cadence_cluster_rationale_conf_trend_momentum_band_trend_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTSBT immediately before TSDPCONWCTSBTA in both sections"
        )
        assert cadence_cluster_rationale_alias_indexes[cluster_i] == cadence_cluster_rationale_conf_trend_momentum_band_trend_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTSBTA immediately before TSDPCONW in both sections"
        )
        assert cadence_cluster_conf_legend_indexes[cluster_i] == cadence_cluster_rationale_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONW immediately before TSDPCONWC legend in both sections"
        )
        assert cadence_cluster_conf_trend_legend_indexes[cluster_i] == cadence_cluster_conf_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWC legend immediately before TSDPCONWCT legend in both sections"
        )
        assert cadence_cluster_conf_trend_alias_legend_indexes[cluster_i] == cadence_cluster_conf_trend_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCT legend immediately before TSDPCONWCTA legend in both sections"
        )
        assert cadence_cluster_conf_trend_momentum_band_trend_legend_indexes[cluster_i] == cadence_cluster_conf_trend_alias_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTA legend immediately before TSDPCONWCTSBT legend in both sections"
        )
        assert cadence_cluster_conf_trend_momentum_band_trend_alias_legend_indexes[cluster_i] == cadence_cluster_conf_trend_momentum_band_trend_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTSBT legend immediately before TSDPCONWCTSBTA legend in both sections"
        )
        assert cadence_cluster_trend_fx_pair_indexes[cluster_i] == cadence_cluster_conf_trend_momentum_band_trend_alias_legend_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPCONWCTSBTA legend immediately before TSDPPAIR row in both sections"
        )
        assert cadence_cluster_trend_fx_pair_alias_indexes[cluster_i] == cadence_cluster_trend_fx_pair_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPPAIR row immediately before TSDPPAIRA row in both sections"
        )
        assert cadence_cluster_trend_fx_pair_decode_indexes[cluster_i] == cadence_cluster_trend_fx_pair_alias_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPPAIRA row immediately before trend->fx decode row in both sections"
        )
        assert cadence_cluster_trend_fx_pair_alias_decode_indexes[cluster_i] == cadence_cluster_trend_fx_pair_decode_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep trend->fx decode row immediately before TSDPPAIRA legend row in both sections"
        )
        assert cadence_cluster_note_legend_indexes[cluster_i] == cadence_cluster_trend_fx_pair_alias_decode_indexes[cluster_i] + 1, (
            f"{name}: cadence cluster order must keep TSDPPAIRA legend row immediately before TSDPCON legend in both sections"
        )
    assert "trend-score dispatch pressure cadence override decode: **TSDPCO legend (B=BASE, E=ESCALATE)**" in md_text, (
        f"{name}: markdown output must include cadence-override alias decode row"
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
        "UP": "escalate pressure checks",
        "FLAT": "hold pressure cadence",
        "DOWN": "cool pressure posture",
    }.get(family_trend, "hold pressure cadence")
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
    assert (
        "trend-score momentum-slope rec family trend why copy budget (design/ux): "
        "**TSDPMSRFTWHYLEN:E24|H21|C21|MAX24/32**"
        in md_text
    ), f"{name}: markdown output must include optional design/ux WHY copy-budget audit row when flag enabled"

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
        "trend-score dispatch-pressure momentum fx urgency cue from momentum-band trend (combat/vfx): "
        f"**TSDPMFXU:{expected_fx_urgency_cue}**"
        in md_text
    ), f"{name}: markdown output must include trend->urgency momentum fx cue row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency cue alias: "
        f"**TSDPMFXUA:{expected_fx_urgency_cue_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact trend->urgency momentum fx cue alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence (ai-content/combat, offline): "
        f"**TSDPMFXUC:{urgency_confidence_value}**"
        in md_text
    ), f"{name}: markdown output must include offline urgency-confidence row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend (ai-content/combat, offline): "
        f"**TSDPMFXUCT:{urgency_confidence_trend_value}**"
        in md_text
    ), f"{name}: markdown output must include offline urgency-confidence trend row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend alias: "
        f"**TSDPMFXUCTA:{urgency_confidence_trend_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include compact urgency-confidence trend alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum score (ai-content/systems, offline): "
        f"**TSDPMFXUCTS:{urgency_confidence_trend_momentum_score_value}**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence trend momentum score row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band (ux/ai-content, offline): "
        f"**TSDPMFXUCTSB:{urgency_confidence_trend_momentum_band_value}**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence trend momentum-band row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend (ai-content/systems, offline): "
        f"**TSDPMFXUCTSBT:{urgency_confidence_trend_momentum_band_trend_value}**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence trend momentum-band-trend row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend alias: "
        f"**TSDPMFXUCTSBTA:{urgency_confidence_trend_momentum_band_trend_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence trend momentum-band-trend alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend confidence (ai-content/systems, offline): "
        f"**TSDPMFXUCTSBTC:{urgency_confidence_trend_momentum_band_trend_confidence_value}**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence trend momentum-band-trend confidence row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend vfx pulse (combat/vfx, offline): "
        f"**TSDPMFXV:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_value}**"
        in md_text
    ), f"{name}: markdown output must include combat/vfx urgency-trend vfx pulse row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend vfx pulse alias: "
        f"**TSDPMFXVA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include combat/vfx urgency-trend vfx pulse alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band pulse guidance (ai-content/systems, offline): "
        f"**TSDPMFXVW:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_value}**"
        in md_text
    ), f"{name}: markdown output must include offline pulse-guidance microcopy row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence (ai-content/systems, offline): "
        f"**TSDPMFXVWC:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value}**"
        in md_text
    ), f"{name}: markdown output must include pulse-guidance confidence row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence alias: "
        f"**TSDPMFXVWCA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_value}**"
        in md_text
    ), f"{name}: markdown output must include pulse-guidance confidence alias row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency guidance confidence decode (design/world): "
        "**TSDPMFXVWC legend (L=LOW, M=MID, H=HIGH)**"
        in md_text
    ), f"{name}: markdown output must include pulse-guidance confidence decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence decode (design/world): "
        "**TSDPMFXUC legend (LOW=volatile churn, MID=mixed churn, HIGH=steady churn)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend decode (design/world): "
        "**TSDPMFXUCT legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence trend decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend alias decode (design/world): "
        "**TSDPMFXUCTA legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence trend alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend decode (design/world): "
        "**TSDPMFXUCTSBT legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence momentum-band-trend decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend alias decode (design/world): "
        "**TSDPMFXUCTSBTA legend (U=UP, F=FLAT, D=DOWN)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence momentum-band-trend alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend confidence decode (design/world): "
        "**TSDPMFXUCTSBTC legend (LOW=flip, MID=one-side flat, HIGH=stable)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence momentum-band-trend confidence decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band vfx pulse decode (design/world): "
        "**TSDPMFXV legend (C=CALM, P=PULSE, B=BLAST)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence vfx pulse decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band vfx pulse alias decode (design/world): "
        "**TSDPMFXVA legend (C=CALM, P=PULSE, B=BLAST)**"
        in md_text
    ), f"{name}: markdown output must include urgency-confidence vfx pulse alias decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band pulse guidance decode (design/world): "
        "**TSDPMFXVW legend (CALM=steady sweep, PULSE=brace lanes, BLAST=commit burst)**"
        in md_text
    ), f"{name}: markdown output must include pulse-guidance decode row"
    urgency_confidence_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence (ai-content/combat, offline): "
        f"**TSDPMFXUC:{urgency_confidence_value}**"
    )
    urgency_confidence_trend_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend (ai-content/combat, offline): "
        f"**TSDPMFXUCT:{urgency_confidence_trend_value}**"
    )
    urgency_confidence_trend_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend alias: "
        f"**TSDPMFXUCTA:{urgency_confidence_trend_alias_value}**"
    )
    urgency_confidence_trend_momentum_score_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum score (ai-content/systems, offline): "
        f"**TSDPMFXUCTS:{urgency_confidence_trend_momentum_score_value}**"
    )
    urgency_confidence_trend_momentum_band_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band (ux/ai-content, offline): "
        f"**TSDPMFXUCTSB:{urgency_confidence_trend_momentum_band_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend (ai-content/systems, offline): "
        f"**TSDPMFXUCTSBT:{urgency_confidence_trend_momentum_band_trend_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend alias: "
        f"**TSDPMFXUCTSBTA:{urgency_confidence_trend_momentum_band_trend_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_confidence_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend confidence (ai-content/systems, offline): "
        f"**TSDPMFXUCTSBTC:{urgency_confidence_trend_momentum_band_trend_confidence_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend vfx pulse (combat/vfx, offline): "
        f"**TSDPMFXV:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend vfx pulse alias: "
        f"**TSDPMFXVA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band pulse guidance (ai-content/systems, offline): "
        f"**TSDPMFXVW:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence (ai-content/systems, offline): "
        f"**TSDPMFXVWC:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence alias: "
        f"**TSDPMFXVWCA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation (ai-content/systems, offline): "
        f"**TSDPMFXVWCR:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias: "
        f"**TSDPMFXVWCRA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity (combat/vfx, offline): "
        f"**TSDPMFXVWCRI:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias: "
        f"**TSDPMFXVWCRIA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend (ai-content/systems, offline): "
        f"**TSDPMFXVWCRIT:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend alias: "
        f"**TSDPMFXVWCRITA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score (ai-content/systems, offline): "
        f"**TSDPMFXVWCRITS:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture (combat/vfx, offline): "
        f"**TSDPMFXVWCRITSP:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture alias: "
        f"**TSDPMFXVWCRITSPA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy (ai-content/systems, offline): "
        f"**TSDPMFXVWCRITSPM:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy alias: "
        f"**TSDPMFXVWCRITSPMA:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_eval_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy decode dos-width eval (design/world): "
        "**TSDPMFXVWCRITSPMLEN:B46|C39|LIM72|PREF:COMPACT|PASS**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_preference_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend score posture microcopy decode preference alias (design/world): "
        "**TSDPMFXVWCRITSPMP:C**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy decode (design/world): "
        "**TSDPMFXVWCRITSPMB legend (SURGE/HOLD/COOL + SHATTER/PULSE/GLIDE => push now|hold lane|ease lane / hard crack|pressure poke|steady nudge)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy alias decode (design/world): "
        "**TSDPMFXVWCRITSPMBA legend (PN|HL|EL / HC|PP|SN)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_decode_eval_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat bridge microcopy decode dos-width eval (design/world): "
        "**TSDPMFXVWCRITSPMBLEN:B109|C19|LIM72|PREF:COMPACT|WARN**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat compact bridge-summary token (ai-content/design, offline): "
        f"**TSDPMFXVWCRITSPMBS:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat compact bridge-summary decode (design/world): "
        "**TSDPMFXVWCRITSPMBS legend (PNHC=push now/hard crack, HLPP=hold lane/pressure poke, ELSN=ease lane/steady nudge)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_candidates_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat ultra-compact bridge-summary alias candidates (ai-content/design, offline): "
        "**TSDPMFXVWCRITSPMBSA table (PNHC->PH, PNPP->PP, PNSN->PS, HLHC->HH, HLPP->HP, HLSN->HS, ELHC->EH, ELPP->EP, ELSN->ES)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat ultra-compact bridge-summary alias shortlist (ux/design, offline): "
        "**TSDPMFXVWCRITSPMBSAP shortlist (PH=push now/hard crack, HP=hold lane/pressure poke, ES=ease lane/steady nudge)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive note (ai-content/combat, offline): "
        "**TSDPMFXVWCRITSPMBSAPN:"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive-note transition helper (design/world, dos-width): "
        "**TSDPMFXVWCRITSPMBSAPN helper (SURGE->PH, HOLD->HP, COOL->ES)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_eval_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive-note transition helper dos-width eval (design/world): "
        "**TSDPMFXVWCRITSPMBSAPNLEN:B57|C41|LIM72|PREF:COMPACT|PASS**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias (combat/vfx, dos-width): "
        "**TSDPMFXVWCRITSPMBSAPF:"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias decode (design/world): "
        "**TSDPMFXVWCRITSPMBSAPF legend (PH=push now/hard crack, HP=hold lane/pressure poke, ES=ease lane/steady nudge)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_token_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias preference token (ai-content/design, offline): "
        "**TSDPMFXVWCRITSPMBSAPFP:"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_sweep_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias A/B sweep seed (ai-content/design, offline): "
        "**TSDPMFXVWCRITSPMBSAPFPAB:A=PH|B=HP|C=ES**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_label_pilot_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias A/B pilot labels (design/ux, offline): "
        "**TSDPMFXVWCRITSPMBSAPFPABL:A=PN|B=HL|C=EZ**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias A/B winning slot (systems/qa, offline): "
        "**TSDPMFXVWCRITSPMBSAPFPABW:"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_legend_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias A/B winning-slot decode legend (design/world, offline): "
        "**TSDPMFXVWCRITSPMBSAPFPABWLEG:A=PH|B=HP|C=ES**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_label_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias A/B winning-slot pilot label (ux/design, offline): "
        "**TSDPMFXVWCRITSPMBSAPFPABWP:"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_legend_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias A/B winning-slot pilot decode legend (design/ux, offline): "
        "**TSDPMFXVWCRITSPMBSAPFPABWPLEG:A=PN|B=HL|C=EZ**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_eval_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend posture-beat shortlist adaptive focus alias decode dos-width eval (design/world): "
        "**TSDPMFXVWCRITSPMBSAPFLEN:"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_ladder_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat ladder helper (design/world, dos-width): "
        "**TSDPMFXVWCRITSB helper (80=SHATTER, 50=PULSE, 20=GLIDE)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat decode (design/world): "
        "**TSDPMFXVWCRITSB legend (GLIDE=stable drift, PULSE=active drift, SHATTER=hard pivot)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend beat (combat/vfx, offline): "
        f"**TSDPMFXVWCRITSB:{urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_value}**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence decode (design/world): "
        "**TSDPMFXVWC legend (L=LOW, M=MID, H=HIGH)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation decode (design/world): "
        "**TSDPMFXVWCR legend (HIGH=lock sweep, MID=brace check, LOW=burst triage)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias decode (design/world): "
        "**TSDPMFXVWCRA legend (LS=lock sweep, BC=brace check, BT=burst triage)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity decode (design/world): "
        "**TSDPMFXVWCRI legend (SOFT=burst triage, EDGE=brace check, HARD=lock sweep)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias decode (design/world): "
        "**TSDPMFXVWCRIA legend (S=SOFT, E=EDGE, H=HARD)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend decode (design/world): "
        "**TSDPMFXVWCRIT legend (U=UP, F=FLAT, D=DOWN)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend alias decode (design/world): "
        "**TSDPMFXVWCRITA legend (U=UP, F=FLAT, D=DOWN)**"
    )
    urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_decode_eval_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias decode dos-width eval (design/world): "
        "**TSDPMFXVWCRIALEN:F52|C22|LIM72|PREF:CONCISE|PASS**"
    )
    urgency_confidence_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence decode (design/world): "
        "**TSDPMFXUC legend (LOW=volatile churn, MID=mixed churn, HIGH=steady churn)**"
    )
    urgency_confidence_trend_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend decode (design/world): "
        "**TSDPMFXUCT legend (U=UP, F=FLAT, D=DOWN)**"
    )
    urgency_confidence_trend_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend alias decode (design/world): "
        "**TSDPMFXUCTA legend (U=UP, F=FLAT, D=DOWN)**"
    )
    urgency_confidence_trend_momentum_band_trend_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend decode (design/world): "
        "**TSDPMFXUCTSBT legend (U=UP, F=FLAT, D=DOWN)**"
    )
    urgency_confidence_trend_momentum_band_trend_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend alias decode (design/world): "
        "**TSDPMFXUCTSBTA legend (U=UP, F=FLAT, D=DOWN)**"
    )
    urgency_confidence_trend_momentum_band_trend_confidence_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend confidence decode (design/world): "
        "**TSDPMFXUCTSBTC legend (LOW=flip, MID=one-side flat, HIGH=stable)**"
    )
    urgency_confidence_trend_momentum_band_vfx_pulse_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band vfx pulse decode (design/world): "
        "**TSDPMFXV legend (C=CALM, P=PULSE, B=BLAST)**"
    )
    urgency_confidence_trend_momentum_band_vfx_pulse_alias_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band vfx pulse alias decode (design/world): "
        "**TSDPMFXVA legend (C=CALM, P=PULSE, B=BLAST)**"
    )
    urgency_confidence_trend_momentum_band_vfx_pulse_guidance_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency confidence trend momentum band pulse guidance decode (design/world): "
        "**TSDPMFXVW legend (CALM=steady sweep, PULSE=brace lanes, BLAST=commit burst)**"
    )
    pulse_callout_pair_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx pulse->callout pairing decode (design/world, dos-width): "
        "**TSDPMFXV C/P/B => TSDPMFXC HL/PE/BC**"
    )
    urgency_decode_idx = md_text.find(
        "trend-score dispatch-pressure momentum fx urgency cue decode (design/world): "
        "**SOFT=trend cooling (DOWN), SURGE=trend stable (FLAT), SPIKE=trend rising (UP)**"
    )
    assert (
        urgency_confidence_idx
        < urgency_confidence_trend_idx
        < urgency_confidence_trend_alias_idx
        < urgency_confidence_trend_momentum_score_idx
        < urgency_confidence_trend_momentum_band_idx
        < urgency_confidence_trend_momentum_band_trend_idx
        < urgency_confidence_trend_momentum_band_trend_alias_idx
        < urgency_confidence_trend_momentum_band_trend_confidence_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_decode_eval_idx
        < urgency_confidence_decode_idx
        < urgency_confidence_trend_decode_idx
        < urgency_confidence_trend_alias_decode_idx
        < urgency_confidence_trend_momentum_band_trend_decode_idx
        < urgency_confidence_trend_momentum_band_trend_alias_decode_idx
        < urgency_confidence_trend_momentum_band_trend_confidence_decode_idx
        < urgency_confidence_trend_momentum_band_vfx_pulse_decode_idx
        < urgency_confidence_trend_momentum_band_vfx_pulse_alias_decode_idx
        < urgency_confidence_trend_momentum_band_vfx_pulse_guidance_decode_idx
        < pulse_callout_pair_decode_idx
        < urgency_decode_idx
    ), (
        f"{name}: urgency cluster order must keep `TSDPMFXUC -> TSDPMFXUCT -> TSDPMFXUCTA -> TSDPMFXUCTS -> TSDPMFXUCTSB -> TSDPMFXUCTSBT -> TSDPMFXUCTSBTA -> TSDPMFXUCTSBTC -> TSDPMFXV -> TSDPMFXVA -> TSDPMFXVW -> TSDPMFXVWC -> TSDPMFXVWCA -> TSDPMFXVWCR -> TSDPMFXVWCRA -> TSDPMFXVWCRI -> TSDPMFXVWCRIA -> TSDPMFXVWCRIT -> TSDPMFXVWCRITA -> TSDPMFXVWCRITS -> TSDPMFXVWCRITSP -> TSDPMFXVWCRITSPA -> TSDPMFXVWCRITSPM -> TSDPMFXVWCRITSPMA -> TSDPMFXVWCRITSB -> TSDPMFXVWC legend -> TSDPMFXVWCR legend -> TSDPMFXVWCRA legend -> TSDPMFXVWCRI legend -> TSDPMFXVWCRIA legend -> TSDPMFXVWCRIT legend -> TSDPMFXVWCRITA legend -> TSDPMFXVWCRIALEN -> TSDPMFXUC legend -> TSDPMFXUCT legend -> TSDPMFXUCTA legend -> TSDPMFXUCTSBT legend -> TSDPMFXUCTSBTA legend -> TSDPMFXUCTSBTC legend -> TSDPMFXV legend -> TSDPMFXVA legend -> TSDPMFXVW legend -> TSDPMFXV->TSDPMFXC pair decode -> TSDPMFXU decode`"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_eval_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_preference_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_decode_idx
    ), (
        f"{name}: urgency cluster decode order must keep `TSDPMFXVWCRITSPMLEN -> TSDPMFXVWCRITSPMP` adjacent before `TSDPMFXVWCRITSB legend`"
    )
    assert (
        urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_decode_eval_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_candidates_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_eval_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_token_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_sweep_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_label_pilot_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_legend_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_label_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_legend_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_eval_idx
        < urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_ladder_decode_idx
    ), (
        f"{name}: urgency cluster decode order must keep `TSDPMFXVWCRITSPMB -> TSDPMFXVWCRITSPMBA -> TSDPMFXVWCRITSPMBLEN -> TSDPMFXVWCRITSPMBS -> TSDPMFXVWCRITSPMBS legend -> TSDPMFXVWCRITSPMBSA table -> TSDPMFXVWCRITSPMBSAP shortlist -> TSDPMFXVWCRITSPMBSAPN -> TSDPMFXVWCRITSPMBSAPN helper -> TSDPMFXVWCRITSPMBSAPNLEN -> TSDPMFXVWCRITSPMBSAPF -> TSDPMFXVWCRITSPMBSAPF legend -> TSDPMFXVWCRITSPMBSAPFP -> TSDPMFXVWCRITSPMBSAPFPAB -> TSDPMFXVWCRITSPMBSAPFPABL -> TSDPMFXVWCRITSPMBSAPFPABW -> TSDPMFXVWCRITSPMBSAPFPABWLEG -> TSDPMFXVWCRITSPMBSAPFPABWP -> TSDPMFXVWCRITSPMBSAPFPABWPLEG -> TSDPMFXVWCRITSPMBSAPFLEN` before `TSDPMFXVWCRITSB helper`"
    )
    fx_urgency_row_count = md_text.count("**TSDPMFXU:")
    fx_urgency_confidence_row_count = md_text.count("**TSDPMFXUC:")
    assert fx_urgency_confidence_row_count == fx_urgency_row_count, (
        f"{name}: `TSDPMFXUC` row count ({fx_urgency_confidence_row_count}) must mirror "
        f"`TSDPMFXU` row count ({fx_urgency_row_count}) across summary + token sections"
    )
    fx_urgency_confidence_trend_row_count = md_text.count("**TSDPMFXUCT:")
    fx_urgency_confidence_trend_alias_row_count = md_text.count("**TSDPMFXUCTA:")
    fx_urgency_confidence_trend_momentum_score_row_count = md_text.count("**TSDPMFXUCTS:")
    fx_urgency_confidence_trend_momentum_band_row_count = md_text.count("**TSDPMFXUCTSB:")
    fx_urgency_confidence_trend_momentum_band_trend_row_count = md_text.count("**TSDPMFXUCTSBT:")
    fx_urgency_confidence_trend_momentum_band_trend_alias_row_count = md_text.count("**TSDPMFXUCTSBTA:")
    fx_urgency_confidence_trend_momentum_band_trend_confidence_row_count = md_text.count("**TSDPMFXUCTSBTC:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_row_count = md_text.count("**TSDPMFXV:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_row_count = md_text.count("**TSDPMFXVA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_row_count = md_text.count("**TSDPMFXVW:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_row_count = md_text.count("**TSDPMFXVWC:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_row_count = md_text.count("**TSDPMFXVWCA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_row_count = md_text.count("**TSDPMFXVWCR:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_row_count = md_text.count("**TSDPMFXVWCRA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_row_count = md_text.count("**TSDPMFXVWCRI:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_row_count = md_text.count("**TSDPMFXVWCRIA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_row_count = md_text.count("**TSDPMFXVWCRIT:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_row_count = md_text.count("**TSDPMFXVWCRITA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count = md_text.count("**TSDPMFXVWCRITS:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count = md_text.count("**TSDPMFXVWCRITSP:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_row_count = md_text.count("**TSDPMFXVWCRITSPA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count = md_text.count("**TSDPMFXVWCRITSPM:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_row_count = md_text.count("**TSDPMFXVWCRITSPMA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_eval_row_count = md_text.count("**TSDPMFXVWCRITSPMLEN:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_preference_alias_row_count = md_text.count("**TSDPMFXVWCRITSPMP:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_helper_row_count = md_text.count("**TSDPMFXVWCRITSH helper")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count = md_text.count("**TSDPMFXVWCRITSB:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_row_count = md_text.count("**TSDPMFXVWCRITSBA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_row_count = md_text.count("**TSDPMFXVWCRITSBM:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count = md_text.count("**TSDPMFXVWCRITSPMB:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_row_count = md_text.count("**TSDPMFXVWCRITSPMBA:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_decode_eval_row_count = md_text.count("**TSDPMFXVWCRITSPMBLEN:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_row_count = md_text.count("**TSDPMFXVWCRITSPMBS:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_candidates_row_count = md_text.count("**TSDPMFXVWCRITSPMBSA table")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAP shortlist")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPN:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPN helper")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_eval_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPNLEN:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPF:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPF legend")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_token_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFP:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_sweep_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFPAB:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_label_pilot_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFPABL:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFPABW:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_legend_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFPABWLEG:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFPABWP:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_legend_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFPABWPLEG:")
    fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_eval_row_count = md_text.count("**TSDPMFXVWCRITSPMBSAPFLEN:")
    adaptive_focus_alias_matches = re.findall(r"\*\*TSDPMFXVWCRITSPMBSAPF:([A-Z]+)\*\*", md_text)
    adaptive_focus_alias_preference_matches = re.findall(r"\*\*TSDPMFXVWCRITSPMBSAPFP:([A-Z]+)\*\*", md_text)
    assert adaptive_focus_alias_matches and all(
        alias in {"PH", "HP", "ES"} for alias in adaptive_focus_alias_matches
    ), f"{name}: `TSDPMFXVWCRITSPMBSAPF` domain must stay within PH|HP|ES"
    assert adaptive_focus_alias_preference_matches and all(
        alias in {"PH", "HP", "ES"} for alias in adaptive_focus_alias_preference_matches
    ), f"{name}: `TSDPMFXVWCRITSPMBSAPFP` domain must stay within PH|HP|ES"
    assert fx_urgency_confidence_trend_alias_row_count == fx_urgency_confidence_trend_row_count, (
        f"{name}: `TSDPMFXUCTA` row count ({fx_urgency_confidence_trend_alias_row_count}) must mirror "
        f"`TSDPMFXUCT` row count ({fx_urgency_confidence_trend_row_count}) across summary + token sections"
    )
    assert fx_urgency_confidence_trend_momentum_score_row_count == fx_urgency_confidence_trend_row_count, (
        f"{name}: `TSDPMFXUCTS` row count ({fx_urgency_confidence_trend_momentum_score_row_count}) must mirror "
        f"`TSDPMFXUCT` row count ({fx_urgency_confidence_trend_row_count}) across summary + token sections"
    )
    assert fx_urgency_confidence_trend_momentum_band_row_count == fx_urgency_confidence_trend_momentum_score_row_count, (
        f"{name}: `TSDPMFXUCTSB` row count ({fx_urgency_confidence_trend_momentum_band_row_count}) must mirror "
        f"`TSDPMFXUCTS` row count ({fx_urgency_confidence_trend_momentum_score_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_row_count
        == fx_urgency_confidence_trend_momentum_band_row_count
    ), (
        f"{name}: `TSDPMFXUCTSBT` row count ({fx_urgency_confidence_trend_momentum_band_trend_row_count}) must mirror "
        f"`TSDPMFXUCTSB` row count ({fx_urgency_confidence_trend_momentum_band_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_row_count
    ), (
        f"{name}: `TSDPMFXUCTSBTA` row count ({fx_urgency_confidence_trend_momentum_band_trend_alias_row_count}) must mirror "
        f"`TSDPMFXUCTSBT` row count ({fx_urgency_confidence_trend_momentum_band_trend_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_confidence_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_alias_row_count
    ), (
        f"{name}: `TSDPMFXUCTSBTC` row count ({fx_urgency_confidence_trend_momentum_band_trend_confidence_row_count}) must mirror "
        f"`TSDPMFXUCTSBTA` row count ({fx_urgency_confidence_trend_momentum_band_trend_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_confidence_row_count
    ), (
        f"{name}: `TSDPMFXV` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_row_count}) must mirror "
        f"`TSDPMFXUCTSBTC` row count ({fx_urgency_confidence_trend_momentum_band_trend_confidence_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_row_count
    ), (
        f"{name}: `TSDPMFXVA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_row_count}) must mirror "
        f"`TSDPMFXV` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_row_count
    ), (
        f"{name}: `TSDPMFXVW` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_row_count}) must mirror "
        f"`TSDPMFXVA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_row_count
    ), (
        f"{name}: `TSDPMFXVWC` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_row_count}) must mirror "
        f"`TSDPMFXVW` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_row_count
    ), (
        f"{name}: `TSDPMFXVWCA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_row_count}) must mirror "
        f"`TSDPMFXVWC` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCR` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_row_count}) must mirror "
        f"`TSDPMFXVWCA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_row_count
    ), (
        f"{name}: `TSDPMFXVWCRA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_row_count}) must mirror "
        f"`TSDPMFXVWCR` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRI` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_row_count}) must mirror "
        f"`TSDPMFXVWCRA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_row_count
    ), (
        f"{name}: `TSDPMFXVWCRIA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRI` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRIT` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_row_count}) must mirror "
        f"`TSDPMFXVWCRIA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRIT` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITS` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count}) must mirror "
        f"`TSDPMFXVWCRITA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSP` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count}) must mirror "
        f"`TSDPMFXVWCRITS` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRITSP` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPM` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count}) must mirror "
        f"`TSDPMFXVWCRITSP` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPM` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_eval_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMLEN` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_eval_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPM` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_preference_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMP` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_decode_preference_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPM` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count}) must mirror "
        f"`TSDPMFXVWCRITS` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_helper_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSH helper` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_helper_row_count}) must mirror "
        f"`TSDPMFXVWCRITS` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSBA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRITSB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSBM` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_microcopy_row_count}) must mirror "
        f"`TSDPMFXVWCRITSB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count}) must mirror "
        f"`TSDPMFXVWCRITSB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBA` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_decode_eval_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBLEN` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_decode_eval_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBS` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_candidates_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSA table` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_candidates_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAP shortlist` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAP shortlist` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBS` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPN` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAP shortlist` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPN helper` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPN` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_eval_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPNLEN` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_eval_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPN helper` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_helper_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPN` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPF legend` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_token_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFP` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_token_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_sweep_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFPAB` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_sweep_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_label_pilot_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFPABL` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_label_pilot_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFPABW` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_legend_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFPABWLEG` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_legend_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFPABWP` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_legend_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFPABWPLEG` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_winner_pilot_legend_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_eval_row_count
        == fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count
    ), (
        f"{name}: `TSDPMFXVWCRITSPMBSAPFLEN` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_decode_eval_row_count}) must mirror "
        f"`TSDPMFXVWCRITSPMBSAPF` row count ({fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count}) across summary + token sections"
    )
    assert (
        "trend-score dispatch-pressure momentum fx pulse->callout pairing decode (design/world, dos-width): "
        "**TSDPMFXV C/P/B => TSDPMFXC HL/PE/BC**"
        in md_text
    ), f"{name}: markdown output must include compact pulse-state to combat-callout pair decode row"
    assert (
        "trend-score dispatch-pressure momentum fx urgency cue decode (design/world): "
        "**SOFT=trend cooling (DOWN), SURGE=trend stable (FLAT), SPIKE=trend rising (UP)**"
        in md_text
    ), f"{name}: markdown output must include trend->urgency decode row"
    assert (
        "trend-score dispatch pressure trend->fx urgency pair (design/world, dos-width): "
        f"**TSDPPAIR:TSDPCONWCTSBT={confidence_trend_momentum_band_trend}|TSDPMFXU={expected_fx_urgency_cue}**"
        in md_text
    ), f"{name}: markdown output must include compact trend->fx urgency pair row for one-scan intent"
    assert (
        "trend-score dispatch pressure trend->fx urgency pair decode (design/world): "
        "**TSDPCONWCTSBT U/F/D => TSDPMFXU SPIKE/SURGE/SOFT**"
        in md_text
    ), f"{name}: markdown output must include compact trend->fx urgency pair decode row"
    assert (
        "trend-score dispatch pressure trend->fx urgency compact alias (design/world, dos-width): "
        f"**TSDPPAIRA:{expected_fx_urgency_cue_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact trend->fx urgency alias row"
    assert (
        "trend-score dispatch pressure trend->fx urgency compact alias decode (design/world): "
        "**TSDPPAIRA legend (S=SOFT, U=SURGE, P=SPIKE)**"
        in md_text
    ), f"{name}: markdown output must include compact trend->fx urgency alias decode row"
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
    assert (
        "trend-score dispatch-pressure momentum fx combat callout (combat/vfx): "
        f"**{expected_dispatch_pressure_momentum_fx_cue_combat_callout}**"
        in md_text
    ), f"{name}: markdown output must include combat/vfx momentum fx combat-callout row"
    assert (
        "trend-score dispatch-pressure momentum fx combat callout alias: "
        f"**TSDPMFXC:{expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias}**"
        in md_text
    ), f"{name}: markdown output must include compact combat/vfx momentum fx combat-callout alias row"
    assert (
        "trend-score dispatch-pressure momentum fx combat callout decode (design/world): "
        "**HL=hold line, PE=press edge, BC=burst clear**"
        in md_text
    ), f"{name}: markdown output must include design/world combat-callout decode row"
    assert (
        "trend-score dispatch-pressure momentum fx combat callout compact decode (design/world): "
        "**HL=hold lane, PE=push edge, BC=burst clear**"
        in md_text
    ), f"{name}: markdown output must include optional compact combat-callout decode variant row"
    assert (
        "trend-score dispatch-pressure momentum fx combat callout decode dos-width eval (design/world): "
        "**TSDPMFXCLEN:B43|C42|LIM72|PREF:COMPACT|PASS**"
        in md_text
    ), f"{name}: markdown output must include compact combat-callout DOS-width/readability evaluation row"

    return {
        "familyTrend": family_trend,
        "tsdpmfxuctsbtRowCount": fx_urgency_confidence_trend_momentum_band_trend_row_count,
        "tsdpmfxuctsbtaRowCount": fx_urgency_confidence_trend_momentum_band_trend_alias_row_count,
        "tsdpmfxuctsbtcRowCount": fx_urgency_confidence_trend_momentum_band_trend_confidence_row_count,
        "tsdpmfxvRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_row_count,
        "tsdpmfxvaRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias_row_count,
        "tsdpmfxvwcrRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_row_count,
        "tsdpmfxvwcraRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias_row_count,
        "tsdpmfxvwcriRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_row_count,
        "tsdpmfxvwcriaRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias_row_count,
        "tsdpmfxvwcritRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_row_count,
        "tsdpmfxvwcritaRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias_row_count,
        "tsdpmfxvwcritsRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_row_count,
        "tsdpmfxvwcritspRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_row_count,
        "tsdpmfxvwcritspaRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_alias_row_count,
        "tsdpmfxvwcritspmbRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_row_count,
        "tsdpmfxvwcritspmbsRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_compact_summary_row_count,
        "tsdpmfxvwcritspmbsapnRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_note_row_count,
        "tsdpmfxvwcritspmbsapfRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_row_count,
        "tsdpmfxvwcritspmbsapfpRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_token_row_count,
        "tsdpmfxvwcritspmbsapfpabRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_sweep_row_count,
        "tsdpmfxvwcritspmbsapfpablRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_beat_bridge_microcopy_ultra_compact_shortlist_adaptive_focus_alias_preference_ab_label_pilot_row_count,
        "tsdpmfxvwcritspmRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_row_count,
        "tsdpmfxvwcritspmaRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_posture_microcopy_alias_row_count,
        "tsdpmfxvwcritsbRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_row_count,
        "tsdpmfxvwcritsbaRowCount": fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_score_beat_alias_row_count,
    }


def main() -> int:
    guardrail_module = load_guardrail_module()
    assert (
        guardrail_module.resolve_cadence_override_streak(["combat-or-vfx"], []) == 1
    ), "fixture: cadence override streak must include intermediate TSDPCOS:1 domain"
    assert (
        guardrail_module.resolve_cadence_24h_ops_action(
            "ALERT",
            ["combat-or-vfx", "design-or-world", "systems-or-ops"],
        )
        == "force combat-or-vfx bucket next"
    ), "fixture: cadence24hOpsAction must prioritize combat-or-vfx bucket dispatch when multiple cadence buckets are missing"
    assert (
        guardrail_module.resolve_cadence_24h_ops_action("ALERT", ["design-or-world"])
        == "force design-or-world bucket next"
    ), "fixture: cadence24hOpsAction must route to design-or-world bucket dispatch when combat-or-vfx is already covered"
    assert (
        guardrail_module.resolve_cadence_24h_ops_action("WATCH", ["systems-or-ops"])
        == "force systems-or-ops bucket next"
    ), "fixture: cadence24hOpsAction must route to systems-or-ops bucket dispatch when it is the remaining missing bucket"
    assert (
        guardrail_module.resolve_cadence_24h_ops_action("WATCH", [])
        == "schedule missing bucket"
    ), "fixture: cadence24hOpsAction must preserve deterministic health-based fallback contract when no cadence buckets are missing"
    with tempfile.TemporaryDirectory(prefix="regression_check_lane_guardrail_") as tmp:
        tmp_path = Path(tmp)
        observed_family_trends: list[str] = []
        mixed_window_tsdpmfx_pulse_parity: list[
            tuple[str, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
        ] = []

        balanced_tie_result = run_fixture_case(
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
            expected_dispatch_pressure_base_class="LIGHT",
            expected_dispatch_pressure_cadence_override_state="BASE",
            expected_dispatch_pressure_cadence_override_alias="B",
            expected_dispatch_pressure_cadence_override_streak=0,
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
            expected_dispatch_pressure_momentum_fx_cue_combat_callout="BURST_CLEAR",
            expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="BC",
        )
        mixed_window_tsdpmfx_pulse_parity.append(
            (
                "balanced_tie",
                int(balanced_tie_result["tsdpmfxuctsbtRowCount"]),
                int(balanced_tie_result["tsdpmfxuctsbtaRowCount"]),
                int(balanced_tie_result["tsdpmfxuctsbtcRowCount"]),
                int(balanced_tie_result["tsdpmfxvRowCount"]),
                int(balanced_tie_result["tsdpmfxvaRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcrRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcraRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcriRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcriaRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritaRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritsRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspaRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspmbRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspmbsRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspmbsapnRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspmbsapfRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspmbsapfpRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspmbsapfpabRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritspmbsapfpablRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritsbRowCount"]),
                int(balanced_tie_result["tsdpmfxvwcritsbaRowCount"]),
            )
        )

        ready_mix_result = run_fixture_case(
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
            expected_dispatch_pressure_base_class="READY",
            expected_dispatch_pressure_cadence_override_state="BASE",
            expected_dispatch_pressure_cadence_override_alias="B",
            expected_dispatch_pressure_cadence_override_streak=0,
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
            expected_dispatch_pressure_momentum_fx_cue_combat_callout="BURST_CLEAR",
            expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="BC",
        )
        mixed_window_tsdpmfx_pulse_parity.append(
            (
                "ready_mix",
                int(ready_mix_result["tsdpmfxuctsbtRowCount"]),
                int(ready_mix_result["tsdpmfxuctsbtaRowCount"]),
                int(ready_mix_result["tsdpmfxuctsbtcRowCount"]),
                int(ready_mix_result["tsdpmfxvRowCount"]),
                int(ready_mix_result["tsdpmfxvaRowCount"]),
                int(ready_mix_result["tsdpmfxvwcrRowCount"]),
                int(ready_mix_result["tsdpmfxvwcraRowCount"]),
                int(ready_mix_result["tsdpmfxvwcriRowCount"]),
                int(ready_mix_result["tsdpmfxvwcriaRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritaRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritsRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspaRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspmbRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspmbsRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspmbsapnRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspmbsapfRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspmbsapfpRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspmbsapfpabRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritspmbsapfpablRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritsbRowCount"]),
                int(ready_mix_result["tsdpmfxvwcritsbaRowCount"]),
            )
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
            expected_dispatch_pressure_base_class="HOT",
            expected_dispatch_pressure_cadence_override_state="BASE",
            expected_dispatch_pressure_cadence_override_alias="B",
            expected_dispatch_pressure_cadence_override_streak=0,
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
            expected_dispatch_pressure_momentum_fx_cue_combat_callout="PRESS_EDGE",
            expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="PE",
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
            expected_dispatch_pressure_base_class="HOT",
            expected_dispatch_pressure_cadence_override_state="BASE",
            expected_dispatch_pressure_cadence_override_alias="B",
            expected_dispatch_pressure_cadence_override_streak=0,
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
            expected_dispatch_pressure_momentum_fx_cue_combat_callout="PRESS_EDGE",
            expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="PE",
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
            expected_dispatch_pressure_base_class="HOT",
            expected_dispatch_pressure_cadence_override_state="BASE",
            expected_dispatch_pressure_cadence_override_alias="B",
            expected_dispatch_pressure_cadence_override_streak=0,
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
            expected_dispatch_pressure_momentum_fx_cue_combat_callout="PRESS_EDGE",
            expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="PE",
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
            expected_dispatch_pressure_base_class="HOT",
            expected_dispatch_pressure_cadence_override_state="ESCALATE",
            expected_dispatch_pressure_cadence_override_alias="E",
            expected_dispatch_pressure_cadence_override_streak=2,
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
            expected_dispatch_pressure_momentum_fx_cue_combat_callout="HOLD_LINE",
            expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="HL",
        )

        prior_window_trend_up_result = run_fixture_case(
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
                expected_dispatch_pressure_base_class="HOT",
                expected_dispatch_pressure_cadence_override_state="ESCALATE",
                expected_dispatch_pressure_cadence_override_alias="E",
                expected_dispatch_pressure_cadence_override_streak=2,
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
                expected_dispatch_pressure_momentum_fx_cue_combat_callout="PRESS_EDGE",
                expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="PE",
                expected_recommendation_family_trend="UP",
            )
        observed_family_trends.append(str(prior_window_trend_up_result["familyTrend"]))
        mixed_window_tsdpmfx_pulse_parity.append(
            (
                "prior_window_trend_up",
                int(prior_window_trend_up_result["tsdpmfxuctsbtRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxuctsbtaRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxuctsbtcRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvaRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcrRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcraRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcriRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcriaRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritaRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritsRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspaRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspmbRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspmbsRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspmbsapnRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspmbsapfRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspmbsapfpRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspmbsapfpabRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritspmbsapfpablRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritsbRowCount"]),
                int(prior_window_trend_up_result["tsdpmfxvwcritsbaRowCount"]),
            )
        )
        prior_window_trend_down_result = run_fixture_case(
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
                expected_dispatch_pressure_base_class="HOT",
                expected_dispatch_pressure_cadence_override_state="ESCALATE",
                expected_dispatch_pressure_cadence_override_alias="E",
                expected_dispatch_pressure_cadence_override_streak=2,
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
                expected_dispatch_pressure_momentum_fx_cue_combat_callout="PRESS_EDGE",
                expected_dispatch_pressure_momentum_fx_cue_combat_callout_alias="PE",
                expected_recommendation_family_trend="DOWN",
            )
        observed_family_trends.append(str(prior_window_trend_down_result["familyTrend"]))
        mixed_window_tsdpmfx_pulse_parity.append(
            (
                "prior_window_trend_down",
                int(prior_window_trend_down_result["tsdpmfxuctsbtRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxuctsbtaRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxuctsbtcRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvaRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcrRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcraRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcriRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcriaRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritaRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritsRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspaRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspmbRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspmbsRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspmbsapnRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspmbsapfRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspmbsapfpRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspmbsapfpabRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritspmbsapfpablRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritsbRowCount"]),
                int(prior_window_trend_down_result["tsdpmfxvwcritsbaRowCount"]),
            )
        )

        assert "UP" in observed_family_trends and "DOWN" in observed_family_trends, (
            "fixture matrix must include explicit prior-window recommendation-family trend transitions for both UP and DOWN"
        )
        assert all(
            tsdpmfxuctsbt_count
            == tsdpmfxuctsbta_count
            == tsdpmfxuctsbtc_count
            == tsdpmfxv_count
            == tsdpmfxva_count
            == tsdpmfxvwcr_count
            == tsdpmfxvwcra_count
            == tsdpmfxvwcri_count
            == tsdpmfxvwcria_count
            == tsdpmfxvwcrit_count
            == tsdpmfxvwcrita_count
            == tsdpmfxvwcrits_count
            == tsdpmfxvwcritsp_count
            == tsdpmfxvwcritspa_count
            == tsdpmfxvwcritspmbsapn_count
            == tsdpmfxvwcritspmbsapf_count
            == tsdpmfxvwcritspmbsapfp_count
            == tsdpmfxvwcritspmbsapfpab_count
            == tsdpmfxvwcritspmbsapfpabl_count
            == tsdpmfxvwcritsb_count
            == tsdpmfxvwcritsba_count
            for (
                _,
                tsdpmfxuctsbt_count,
                tsdpmfxuctsbta_count,
                tsdpmfxuctsbtc_count,
                tsdpmfxv_count,
                tsdpmfxva_count,
                tsdpmfxvwcr_count,
                tsdpmfxvwcra_count,
                tsdpmfxvwcri_count,
                tsdpmfxvwcria_count,
                tsdpmfxvwcrit_count,
                tsdpmfxvwcrita_count,
                tsdpmfxvwcrits_count,
                tsdpmfxvwcritsp_count,
                tsdpmfxvwcritspa_count,
                tsdpmfxvwcritspmb_count,
                tsdpmfxvwcritspmbs_count,
                tsdpmfxvwcritspmbsapn_count,
                tsdpmfxvwcritspmbsapf_count,
                tsdpmfxvwcritspmbsapfp_count,
                tsdpmfxvwcritspmbsapfpab_count,
                tsdpmfxvwcritspmbsapfpabl_count,
                tsdpmfxvwcritsb_count,
                tsdpmfxvwcritsba_count,
            )
            in mixed_window_tsdpmfx_pulse_parity
        ), (
            "mixed-window fixture matrix must keep TSDPMFXUCTSBT/TSDPMFXUCTSBTA/TSDPMFXUCTSBTC/TSDPMFXV/TSDPMFXVA/TSDPMFXVWCR/TSDPMFXVWCRA/TSDPMFXVWCRI/TSDPMFXVWCRIA/TSDPMFXVWCRIT/TSDPMFXVWCRITA/TSDPMFXVWCRITS/TSDPMFXVWCRITSP/TSDPMFXVWCRITSPA/TSDPMFXVWCRITSPMB/TSDPMFXVWCRITSPMBS/TSDPMFXVWCRITSPMBSAPN/TSDPMFXVWCRITSPMBSAPF/TSDPMFXVWCRITSPMBSAPFP/TSDPMFXVWCRITSPMBSAPFPAB/TSDPMFXVWCRITSPMBSAPFPABL/TSDPMFXVWCRITSB/TSDPMFXVWCRITSBA row-count parity across summary + token sections"
        )

    cadence_24h_confidence_delta_ramp_rows = {
        "up": [
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Design/World Team: synthetic monotonic ramp seed",
            "Combat/VFX Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
        ],
        "flat": [
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
        ],
        "down": [
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Design/World Team: synthetic monotonic ramp seed",
            "Combat/VFX Team: synthetic monotonic ramp seed",
            "Systems/QA Team: synthetic monotonic ramp seed",
            "Design/World Team: synthetic monotonic ramp seed",
            "Design/World Team: synthetic monotonic ramp seed",
        ],
    }
    cadence_24h_confidence_delta_ramp_scores = {
        name: int(
            guardrail_module.resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score(
                rows
            )
        )
        for name, rows in cadence_24h_confidence_delta_ramp_rows.items()
    }
    cadence_24h_confidence_delta_ramp_momentum = {
        name: guardrail_module.resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum(
            rows
        )
        for name, rows in cadence_24h_confidence_delta_ramp_rows.items()
    }
    assert cadence_24h_confidence_delta_ramp_momentum == {
        "up": "UP",
        "flat": "FLAT",
        "down": "DOWN",
    }, (
        "mixed-window fixture invariant requires synthetic confidence-delta ramps to preserve explicit momentum-domain mapping UP|FLAT|DOWN"
    )
    assert (
        cadence_24h_confidence_delta_ramp_scores["up"]
        > cadence_24h_confidence_delta_ramp_scores["flat"]
        > cadence_24h_confidence_delta_ramp_scores["down"]
    ), (
        "mixed-window fixture invariant requires TSDCAD24TRICOVSTCMS monotonic response for synthetic confidence-delta ramps (up > flat > down)"
    )
    cadence_24h_confidence_delta_ramp_vfx_cues = {
        name: guardrail_module.resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue(
            score
        )
        for name, score in cadence_24h_confidence_delta_ramp_scores.items()
    }
    assert set(cadence_24h_confidence_delta_ramp_vfx_cues.values()).issubset({"GLINT", "PULSE", "BLAST"}), (
        "mixed-window fixture invariant requires TSDCAD24TRICOVSTCMSV domain lock (GLINT|PULSE|BLAST)"
    )
    assert (
        cadence_24h_confidence_delta_ramp_scores["up"] >= cadence_24h_confidence_delta_ramp_scores["flat"] >= cadence_24h_confidence_delta_ramp_scores["down"]
    ), (
        "mixed-window fixture invariant requires TSDCAD24TRICOVSTCMSV source-score ordering compatibility (up >= flat >= down)"
    )

    cadence_24h_hysteresis_three_window_fixture = [
        ("steady_a", cadence_24h_confidence_delta_ramp_rows["flat"]),
        ("swing", cadence_24h_confidence_delta_ramp_rows["up"]),
        ("steady_b", cadence_24h_confidence_delta_ramp_rows["down"]),
    ]
    cadence_24h_hysteresis_three_window_scores = [
        int(
            guardrail_module.resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score(
                rows
            )
        )
        for _, rows in cadence_24h_hysteresis_three_window_fixture
    ]
    cadence_24h_hysteresis_three_window_advisories = [
        guardrail_module.resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_advisory(
            rows
        )
        for _, rows in cadence_24h_hysteresis_three_window_fixture
    ]
    cadence_24h_hysteresis_three_window_confidence_bands = [
        guardrail_module.resolve_cadence_24h_recovery_triad_coverage_spread_trend_confidence_momentum_score_vfx_cue_hysteresis_confidence_band(
            rows
        )
        for _, rows in cadence_24h_hysteresis_three_window_fixture
    ]
    assert cadence_24h_hysteresis_three_window_advisories == ["STEADY", "SWING", "STEADY"], (
        "synthetic three-window cue-transition fixture must prove deterministic advisory toggle STEADY -> SWING -> STEADY"
    )
    assert cadence_24h_hysteresis_three_window_confidence_bands == ["HIGH", "LOW", "HIGH"], (
        "synthetic three-window cue-transition fixture must map confidence bands HIGH -> LOW -> HIGH from stability-window flips"
    )
    assert set(cadence_24h_hysteresis_three_window_confidence_bands).issubset({"LOW", "MID", "HIGH"}), (
        "synthetic three-window cue-transition fixture requires TSDCAD24TRICOVSTCMSVHC domain lock (LOW|MID|HIGH)"
    )
    assert cadence_24h_hysteresis_three_window_scores[1] > cadence_24h_hysteresis_three_window_scores[0] > cadence_24h_hysteresis_three_window_scores[2], (
        "synthetic three-window cue-transition fixture requires deterministic score ladder ordering (window2 > window1 > window3)"
    )

    print("ok: trendScoreBand dispatch-hint/momentum-band regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
