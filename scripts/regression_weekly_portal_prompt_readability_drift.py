#!/usr/bin/env python3
"""Regression checks for weekly_portal_prompt_readability_drift.py."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from weekly_portal_prompt_readability_drift import (
    action_pace_alt_window_confidence_from_signals,
    action_pace_alt_window_fit_from_signals,
    action_pace_alt_window_why_from_signals,
    action_pace_alt_window_urgency_from_signals,
    action_pace_alt_window_urgency_drift_from_prior,
    action_pace_alt_window_step_from_signals,
    action_pace_alt_window_step_drift_from_prior,
    alt_step_confidence_drift_from_prior,
    action_pace_alt_window_step_glyph_from_signals,
    action_pace_alt_window_pulse_drift_from_prior,
    action_pace_alt_window_from_signals,
    route_pulse_link_streak_from_prior,
    route_pulse_link_mode_from_signals,
    route_pulse_link_mode_drift_from_prior,
    route_pulse_link_mode_stability_streak_from_prior,
    route_pulse_link_mode_fit_from_signals,
    route_pulse_link_mode_fit_drift_from_prior,
    action_pace_window_confidence_from_signals,
    pace_drift_from_prior,
    sandbox_cooloff_from_prior,
    what_if_split_cooloff_from_prior,
    what_if_split_escalate_cooloff_from_prior,
    what_if_split_escalate_recover_plan_from_signals,
    what_if_split_escalate_recover_why_from_signals,
    what_if_split_escalate_recover_tempo_from_signals,
    what_if_split_escalate_recover_veto_from_signals,
    what_if_split_escalate_recover_veto_confidence_from_signals,
    what_if_split_escalate_recover_veto_why_from_signals,
    what_if_split_escalate_recover_veto_cooloff_from_prior,
    what_if_split_escalate_recover_veto_state_from_signals,
    what_if_split_escalate_recover_veto_dwell_from_prior,
    what_if_split_escalate_recover_veto_release_from_prior,
    what_if_split_escalate_recover_veto_release_confidence_from_signals,
    what_if_split_escalate_recover_veto_release_route_from_signals,
    what_if_split_escalate_recover_veto_release_tick_from_prior,
    what_if_split_escalate_recover_veto_release_tick_phase_from_signals,
    what_if_split_escalate_recover_veto_release_tick_cadence_from_signals,
    what_if_split_escalate_recover_veto_rearm_from_signals,
    what_if_split_escalate_recover_veto_rearm_confidence_from_signals,
    what_if_split_escalate_recover_veto_rearm_why_from_signals,
    what_if_split_escalate_recover_veto_rearm_cooloff_from_prior,
    what_if_split_escalate_recover_veto_rearm_cooloff_state_from_signals,
    what_if_split_escalate_recover_veto_rearm_fit_from_signals,
    what_if_split_escalate_recover_veto_rearm_nudge_from_signals,
    what_if_split_escalate_recover_veto_rearm_nudge_window_from_signals,
    what_if_split_escalate_recover_veto_rearm_nudge_confidence_from_signals,
    what_if_split_escalate_recover_veto_rearm_nudge_drift_from_prior,
    what_if_split_escalate_recover_veto_rearm_coach_mode_from_signals,
    what_if_split_escalate_recover_veto_rearm_coach_why_from_signals,
    what_if_split_escalate_recover_veto_rearm_coach_handoff_from_signals,
    what_if_split_escalate_recover_veto_rearm_coach_handoff_fit_from_signals,
    what_if_split_escalate_recover_veto_rearm_coach_handoff_why_from_signals,
    what_if_split_escalate_recover_confidence_delta_from_prior,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly_portal_prompt_readability_drift.py"


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def run_output(cmd: list[str], cwd: Path) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True)


def commit_all(repo: Path, message: str) -> None:
    run(["git", "add", "-A"], repo)
    run(["git", "commit", "-m", message], repo)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="portal-prompt-drift-reg-") as td:
        repo = Path(td)
        run(["git", "init"], repo)
        run(["git", "config", "user.email", "reg@example.com"], repo)
        run(["git", "config", "user.name", "Regression Bot"], repo)

        (repo / "src").mkdir(parents=True, exist_ok=True)
        (repo / "src" / "portal.lua").write_text(
            'return "PORTAL READY -> ENTER:JUMP  NEXT ROUTE:SAFE  COACH:LOW PRESSURE  PRESSURE:1"\n',
            encoding="utf-8",
        )
        commit_all(repo, "feat: add detailed portal prompt")

        (repo / "src" / "portal.lua").write_text(
            'return "PORTAL READY -> ENTER:JUMP  NEXT:SAFE  COACH:LOW  P:1  ALT:RISK  ADEL:-1  AP:LOW  VIBE:E"\n',
            encoding="utf-8",
        )
        commit_all(repo, "feat: compact portal prompt")

        out_json = repo / "out.json"
        out_md = repo / "out.md"
        out_fx_candidates_json = repo / "out_fx_candidates.json"
        out_fx_candidates_md = repo / "out_fx_candidates.md"
        out_ambient_auto_remap_json = repo / "out_ambient_auto_remap.json"
        out_ambient_auto_remap_md = repo / "out_ambient_auto_remap.md"

        run_output(
            [
                "python3",
                str(SCRIPT),
                "--since-days",
                "3650",
                "--max-commits",
                "20",
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
                "--out-fx-remap-candidates-json",
                str(out_fx_candidates_json),
                "--out-fx-remap-candidates-md",
                str(out_fx_candidates_md),
                "--out-ambient-why-auto-remap-plan-json",
                str(out_ambient_auto_remap_json),
                "--out-ambient-why-auto-remap-plan-md",
                str(out_ambient_auto_remap_md),
            ],
            repo,
        )

        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["checkedCommits"] >= 2, payload
        assert payload["portalPromptCommits"] >= 2, payload
        assert payload["totals"]["added"]["compact"] > 0, payload
        assert payload["totals"]["added"]["detailed"] > 0, payload
        assert payload["modeTrend"] in {"COMPACT", "DETAILED", "BALANCED"}, payload
        assert payload["pressureBand"] in {"LOW", "MID", "HIGH"}, payload
        assert payload["driftRisk"] in {"LOW", "MID", "HIGH"}, payload
        assert set(payload["driftRiskSignals"].keys()) == {"score", "imbalance", "pressureChurn"}, payload
        assert payload.get("rgfxwriWhyConfPolicyRecommendation") in {"FREEZE", "GUARDED", "RELAXED"}, payload
        assert set(payload.get("rgfxwriWhyConfPolicyRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "familyChurn",
            "familyNet",
            "familyCoverage",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("ambientRampConfidenceRecommendation") in {"PIN_HIGH_CONF", "GUARD_HIGH_CONF", "ALLOW_BALANCED_CONF"}, payload
        assert set(payload.get("ambientRampConfidenceRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "pressureBand",
            "ambientRampConfidenceChurn",
            "ambientRampConfidenceNet",
            "ambientRampConfidenceCoverage",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("ambientRampWhyRecommendation") in {"HOLD_SAFE_WHY", "PRESSURE_GATED_WHY", "OPEN_CONTEXTUAL_WHY"}, payload
        assert set(payload.get("ambientRampWhyRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "pressureBand",
            "ambientRampWhyChurn",
            "ambientRampWhyNet",
            "ambientRampWhyCoverage",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("ambientRampWhyRecommendationConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("ambientRampWhyRecommendationConfidenceSignals", {}).keys()) == {
            "recommendation",
            "driftRisk",
            "pressureBand",
            "ambientRampWhyChurn",
            "rationale",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("ambientRampWhyRecommendationConfidenceStreak"), int), payload
        assert set(payload.get("ambientRampWhyRecommendationConfidenceStreakSignals", {}).keys()) == {
            "currentConfidence",
            "priorConfidence",
            "priorStreak",
            "priorLoaded",
            "threshold",
            "suppress",
            "reason",
        }, payload
        assert payload.get("urgencyStackPruningOrderRecommendation") in {"PARITY>FX>DETAIL", "FX>PARITY>DETAIL"}, payload
        assert set(payload.get("urgencyStackPruningOrderRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "parityCompactChurn",
            "urgencyFxChurn",
            "urgencyDetailedChurn",
            "parityCompactNet",
            "urgencyFxNet",
            "urgencyDetailedNet",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("urgencyStackRailRecommendation") in {"STEADY-FIRST", "SPIKE-WHEN-CONFIRMED", "BALANCED"}, payload
        assert set(payload.get("urgencyStackRailRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "urgencyStackRailChurn",
            "urgencyStackRailNet",
            "urgencyStackRailCoverage",
            "urgencyStackTierChurn",
            "urgencyStackTierNet",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("dmgGlyphShapeRemapRecommendation") in {"PIN_BANDS", "RAIL_SYNC", "MICRO_TUNE"}, payload
        assert set(payload.get("dmgGlyphShapeRemapRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "dmgGlyphChurn",
            "dmgGlyphNet",
            "dmgGlyphCoverage",
            "urgencyStackRailChurn",
            "urgencyStackRailNet",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("dmgGlyphFxRemapRecommendation") in {"HOLD_FX", "SYNC_WITH_GLYPH", "MICRO_TUNE_FX"}, payload
        assert set(payload.get("dmgGlyphFxRemapRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "dmgGlyphFxLiveChurn",
            "dmgGlyphFxLiveNet",
            "dmgGlyphFxLiveCoverage",
            "dmgGlyphChurn",
            "dmgGlyphNet",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("dmgGlyphFxRemapConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("dmgGlyphFxRemapConfidenceSignals", {}).keys()) == {
            "driftRisk",
            "dmgGlyphFxLiveChurn",
            "dmgGlyphChurn",
            "churnScore",
            "rationale",
        }, payload
        assert payload.get("dmgnumLifeTrendFxPulseRemapRecommendation") in {"HOLD_PULSE_CONF", "MICRO_TUNE_PULSE_CONF", "SYNC_WITH_TREND"}, payload
        assert set(payload.get("dmgnumLifeTrendFxPulseRemapRecommendationSignals", {}).keys()) == {
            "driftRisk",
            "pressureBand",
            "laneCadenceRecency",
            "dmgnumLifeTrendFxPulseChurn",
            "dmgnumLifeTrendFxPulseNet",
            "dmgnumLifeTrendFxPulseCoverage",
            "dmgnumLifeTrendFxPulseConfChurn",
            "dmgnumLifeTrendFxPulseConfNet",
            "dmgnumLifeTrendFxPulseConfCoverage",
            "rationale",
            "offlineOnly",
            "guidance",
        }, payload
        assert payload.get("pulseRemapMomentumRecommendation") in {"FREEZE", "WATCH", "ALLOW"}, payload
        assert set(payload.get("pulseRemapMomentumRecommendationSignals", {}).keys()) == {
            "recommendation",
            "driftRisk",
            "pressureBand",
            "laneCadenceRecency",
            "planChurn",
            "planNet",
            "planCoverage",
            "freezeBias",
            "rationale",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("pulseRemapMomentumDrift"), int), payload
        assert set(payload.get("pulseRemapMomentumDriftSignals", {}).keys()) == {
            "currentMomentum",
            "currentScore",
            "priorMomentum",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("pulseRemapMomentumSuppression") in {"SUPPRESS", "ARM", "OFF"}, payload
        assert set(payload.get("pulseRemapMomentumSuppressionSignals", {}).keys()) == {
            "currentMomentum",
            "priorMomentum",
            "priorLoaded",
            "priorFreezeStreak",
            "freezeStreak",
            "threshold",
            "suppress",
            "offlineOnly",
            "reason",
        }, payload
        assert isinstance(payload.get("pulseRemapMomentumFreezeStreak"), int) and payload["pulseRemapMomentumFreezeStreak"] >= 0, payload
        assert isinstance(payload.get("pulseRemapMomentumSuppressionAlias"), str) and payload["pulseRemapMomentumSuppressionAlias"].startswith("PRMS:"), payload
        assert set(payload.get("pulseRemapMomentumSuppressionAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert isinstance(payload.get("pulseRemapSuppressionFamilyTrendDrift"), int), payload
        assert set(payload.get("pulseRemapSuppressionFamilyTrendSignals", {}).keys()) == {
            "trend",
            "currentNet",
            "priorNet",
            "priorLoaded",
            "reason",
        }, payload
        assert payload["pulseRemapSuppressionFamilyTrendSignals"]["trend"] in {"UP", "DOWN", "FLAT"}, payload
        assert isinstance(payload.get("pulseRemapSuppressionPlanFamilyTrendDrift"), int), payload
        assert set(payload.get("pulseRemapSuppressionPlanFamilyTrendSignals", {}).keys()) == {
            "trend",
            "currentNet",
            "priorNet",
            "priorLoaded",
            "reason",
        }, payload
        assert payload["pulseRemapSuppressionPlanFamilyTrendSignals"]["trend"] in {"UP", "DOWN", "FLAT"}, payload
        assert payload.get("pulseRemapSuppressionEscalationPlan") in {"HOLD", "ARM", "LOCK"}, payload
        assert set(payload.get("pulseRemapSuppressionEscalationPlanSignals", {}).keys()) == {
            "suppression",
            "momentum",
            "freezeStreak",
            "driftRisk",
            "laneCadenceRecency",
            "offlineOnly",
            "reason",
        }, payload
        assert isinstance(payload.get("pulseRemapSuppressionEscalationPlanAlias"), str) and payload["pulseRemapSuppressionEscalationPlanAlias"].startswith("PRSP:"), payload
        assert set(payload.get("pulseRemapSuppressionEscalationPlanAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert payload.get("pulseRemapSuppressionSceneFlavor") in {"CALM", "BRACE", "LOCK"}, payload
        assert set(payload.get("pulseRemapSuppressionSceneFlavorSignals", {}).keys()) == {
            "suppressionPlan",
            "driftRisk",
            "pressureBand",
            "laneCadenceRecency",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("pulseRemapSceneConfidence") in {"LOW", "MED", "HIGH"}, payload
        assert set(payload.get("pulseRemapSceneConfidenceSignals", {}).keys()) == {
            "suppressionPlan",
            "driftRisk",
            "pressureBand",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("pulseRemapSuppressionSceneMicroline"), str) and len(payload["pulseRemapSuppressionSceneMicroline"]) > 0, payload
        assert set(payload.get("pulseRemapSuppressionSceneMicrolineSignals", {}).keys()) == {
            "suppressionPlan",
            "sceneFlavor",
            "sceneConfidence",
            "laneCadenceRecency",
            "cadenceTrend",
            "cadenceMemory",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("pulseRemapSuppressionPostureWarning") in {"STEADY", "CAUTION", "ALERT"}, payload
        assert set(payload.get("pulseRemapSuppressionPostureWarningSignals", {}).keys()) == {
            "suppressionPlan",
            "suppression",
            "sceneConfidence",
            "driftRisk",
            "pressureBand",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("pulseRemapSuppressionPostureWarningAlias"), str) and payload["pulseRemapSuppressionPostureWarningAlias"].startswith("PRPW:"), payload
        assert set(payload.get("pulseRemapSuppressionPostureWarningAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert isinstance(payload.get("pulseRemapMomentumAlias"), str) and payload["pulseRemapMomentumAlias"].startswith("PRM:"), payload
        assert set(payload.get("pulseRemapMomentumAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert set(payload.get("routeVibeTotals", {}).keys()) == {"added", "removed", "net"}, payload
        assert set(payload["routeVibeTotals"]["added"].keys()) == {"CALM", "EDGE", "DOOM"}, payload
        assert payload["routeVibeTotals"]["added"]["EDGE"] >= 1, payload
        assert payload["laneFocus"] in {"PORTAL", "ALT", "PRESSURE", "MIXED"}, payload
        assert set(payload["laneFocusScores"].keys()) == {"portal", "alt", "pressure"}, payload
        assert isinstance(payload.get("focusStreak"), int) and payload["focusStreak"] >= 0, payload
        assert isinstance(payload.get("focusShift"), str) and "->" in payload["focusShift"], payload
        assert payload.get("focusVolatility") in {"STEADY", "SWING"}, payload
        assert set(payload.get("focusVolatilitySignals", {}).keys()) == {"switches", "edges", "switchRatio"}, payload
        assert payload["routeAction"] in {"PORTAL_AUDIT", "ALT_TUNE", "PRESSURE_REBASE", "BALANCE_PASS", "WATCH"}, payload
        assert isinstance(payload["routeActionReason"], str) and payload["routeActionReason"], payload
        assert payload.get("routeActionConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("routeActionConfidenceSignals", {}).keys()) == {
            "topScore",
            "secondScore",
            "totalScore",
            "dominanceRatio",
            "focusSpread",
            "driftSpread",
        }, payload
        assert isinstance(payload.get("focusBalance"), str) and payload["focusBalance"].endswith("%"), payload
        assert set(payload.get("focusBalanceSignals", {}).keys()) == {
            "topScore",
            "totalScore",
            "dominanceRatio",
            "percent",
        }, payload
        assert payload.get("focusEntropy") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("focusEntropySignals", {}).keys()) == {
            "raw",
            "normalized",
            "maxEntropy",
            "totalScore",
        }, payload
        assert payload.get("actionGuard") in {"LOCK", "SOFT"}, payload
        assert set(payload.get("actionGuardSignals", {}).keys()) == {
            "armed",
            "reason",
            "driftRisk",
            "actionConfidence",
        }, payload
        assert isinstance(payload.get("laneLock"), str), payload
        assert set(payload.get("laneLockSignals", {}).keys()) == {"threshold", "armed", "lane", "streak"}, payload
        assert isinstance(payload.get("laneBucketAge"), str), payload
        assert payload.get("laneBucketAgeStatus") in {"OK", "GAP"}, payload
        assert isinstance(payload.get("laneBucketAgeHours"), dict), payload
        assert isinstance(payload.get("laneBucketAgeDrift"), int), payload
        assert set(payload.get("laneBucketAgeDriftSignals", {}).keys()) == {"currentMaxAgeHours", "priorMaxAgeHours", "priorLoaded"}, payload
        assert payload.get("laneCadenceRecency") in {"LANE CADENCE RECENCY:ok", "LANE CADENCE RECENCY:warn"}, payload
        assert set(payload.get("laneCadenceRecencySignals", {}).keys()) == {"status", "maxAgeHours", "deltaHours", "windowHours", "reason"}, payload
        assert isinstance(payload.get("laneBucketAgeCompactAlias"), str), payload
        assert set(payload.get("laneBucketAgeCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "systemsOpsHours",
            "designWorldHours",
            "combatVfxHours",
        }, payload
        assert payload.get("lanePriorityRecommendation") in {"BALANCED", "SYSTEMS/OPS", "DESIGN/WORLD", "COMBAT/VFX"}, payload
        assert set(payload.get("lanePriorityRecommendationSignals", {}).keys()) == {
            "offlineOnly",
            "priorLoaded",
            "priorRecommendation",
            "rawRecommendation",
            "hysteresisApplied",
            "hysteresisThreshold",
            "hysteresisScoreGap",
            "hysteresisReason",
            "currentAgeHours",
            "priorAgeHours",
            "momentumHours",
            "momentumBoost",
            "priorityScores",
            "staleLanes",
            "worstAgeHours",
            "reason",
        }, payload
        assert payload.get("lanePriorityRecommendationConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("lanePriorityRecommendationConfidenceSignals", {}).keys()) == {
            "recommendation",
            "worstAgeHours",
            "momentumGapHours",
            "maxMomentumHours",
            "reason",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationCompactAlias"), str), payload
        assert set(payload.get("lanePriorityRecommendationCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "recommendation",
            "alias",
        }, payload
        assert isinstance(payload.get("lanePriorityHysteresisCompactAlias"), str), payload
        assert set(payload.get("lanePriorityHysteresisCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "hysteresisApplied",
            "alias",
        }, payload
        assert payload.get("lanePriorityHysteresisRail") in {"OFF", "LPR HYS RAIL:STEADY", "LPR HYS RAIL:SPIKE"}, payload
        assert set(payload.get("lanePriorityHysteresisRailSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "confidence",
            "hysteresisApplied",
            "scoreGap",
            "threshold",
            "closeGapThreshold",
            "rail",
            "reason",
        }, payload
        assert payload.get("lanePriorityHysteresisThresholdTuning") in {
            "LPR HYS THRESH REC:LOWER",
            "LPR HYS THRESH REC:HOLD",
            "LPR HYS THRESH REC:RAISE",
        }, payload
        assert set(payload.get("lanePriorityHysteresisThresholdTuningSignals", {}).keys()) == {
            "offlineOnly",
            "baseThreshold",
            "recommendedThreshold",
            "mode",
            "maxAbsMomentumHours",
            "momentumVolatilitySpanHours",
            "ageSpreadHours",
            "adaptiveFloor",
            "adaptiveCeiling",
            "priorAdaptiveWindowLoaded",
            "volatilityRegime",
            "priorVolatilityRegime",
            "volatilityRegimeMemory",
            "volatilityRegimeReason",
            "stepSizes",
            "learningReason",
            "reason",
        }, payload
        assert payload.get("lanePriorityVolatilityRegimeMemory") in {"LPR VOL REGIME:CALM", "LPR VOL REGIME:SWING", "LPR VOL REGIME:SPIKE"}, payload
        assert set(payload.get("lanePriorityVolatilityRegimeMemorySignals", {}).keys()) == {
            "currentRegime",
            "priorRegime",
            "memoryRegime",
            "reason",
            "stepSizes",
        }, payload
        assert payload.get("lanePriorityHysteresisThresholdCompactAlias") in {"OFF", "LPR HYS THR:L", "LPR HYS THR:H", "LPR HYS THR:R"}, payload
        assert set(payload.get("lanePriorityHysteresisThresholdCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "recommendation",
            "alias",
        }, payload
        assert payload.get("lanePriorityHysteresisWindowBand") in {"LPR HYS WINDOW:TIGHT", "LPR HYS WINDOW:BASE", "LPR HYS WINDOW:WIDE"}, payload
        assert set(payload.get("lanePriorityHysteresisWindowBandSignals", {}).keys()) == {
            "adaptiveFloor",
            "adaptiveCeiling",
            "span",
            "band",
            "reason",
        }, payload
        assert payload.get("lanePriorityHysteresisWindowDelta") in {"LPR HYS WINDOW Δ:-2", "LPR HYS WINDOW Δ:-1", "LPR HYS WINDOW Δ:+0", "LPR HYS WINDOW Δ:+1", "LPR HYS WINDOW Δ:+2"}, payload
        assert payload.get("lanePriorityHysteresisWindowDeltaValue") in {-2, -1, 0, 1, 2}, payload
        assert set(payload.get("lanePriorityHysteresisWindowDeltaSignals", {}).keys()) == {
            "currentBand",
            "priorBand",
            "currentScore",
            "priorScore",
            "delta",
            "priorLoaded",
        }, payload
        assert payload.get("routeSandbox") in {"ON", "OFF"}, payload
        assert set(payload.get("routeSandboxSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "laneLockArmed",
            "laneLock",
            "laneLockStreak",
            "threshold",
            "reason",
        }, payload
        assert payload.get("routeSandboxPlan") in {"SIMULATE", "PROBE", "PREPARE", "HOLD"}, payload
        assert set(payload.get("routeSandboxPlanSignals", {}).keys()) == {
            "routeSandbox",
            "actionGuard",
            "driftRisk",
            "reason",
        }, payload
        assert payload.get("sandboxTarget") in {"PORTAL", "ALT", "PRESSURE", "MIXED", "NONE"}, payload
        assert set(payload.get("sandboxTargetSignals", {}).keys()) == {
            "routeSandbox",
            "lane",
            "laneLockArmed",
            "laneLockStreak",
            "targetSource",
            "reason",
        }, payload
        assert payload.get("sandboxTargetSource") in {"LOCK", "MIXED", "NONE"}, payload
        assert payload.get("sandboxTargetConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("sandboxTargetConfidenceSignals", {}).keys()) == {
            "sandboxTarget",
            "routeActionConfidence",
            "laneLockArmed",
            "laneLockStreak",
            "reason",
        }, payload
        assert payload.get("sandboxReadiness") in {"IDLE", "PRIMED", "ARMED"}, payload
        assert set(payload.get("sandboxReadinessSignals", {}).keys()) == {
            "routeSandbox",
            "sandboxTargetConfidence",
            "actionGuard",
            "laneLockArmed",
            "laneLockStreak",
            "reason",
        }, payload
        assert isinstance(payload.get("sandboxTargetShift"), str) and "->" in payload["sandboxTargetShift"], payload
        assert set(payload.get("sandboxTargetShiftSignals", {}).keys()) == {
            "priorTarget",
            "currentTarget",
            "changed",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("sandboxCooloff"), int) and payload["sandboxCooloff"] >= 0, payload
        assert set(payload.get("sandboxCooloffSignals", {}).keys()) == {
            "active",
            "currentSandbox",
            "priorSandbox",
            "priorCooloff",
            "priorLoaded",
            "reason",
        }, payload
        assert payload["sandboxCooloffSignals"]["currentSandbox"] in {"ON", "OFF"}, payload
        assert payload.get("driftMomentum") in {"RISING", "COOLING", "FLAT"}, payload
        assert set(payload.get("driftMomentumSignals", {}).keys()) == {"recentAvg", "olderAvg", "delta", "recentCount", "olderCount"}, payload
        assert payload.get("actionStability") in {"LOCKED", "WATCH"}, payload
        assert set(payload.get("actionStabilitySignals", {}).keys()) == {
            "routeActionConfidence",
            "focusVolatility",
            "driftMomentum",
            "stableConfidence",
            "steadyFocus",
            "stableMomentum",
            "reason",
        }, payload
        assert payload.get("pressureLag") in {"FAST", "STABLE", "SLOW"}, payload
        assert set(payload.get("pressureLagSignals", {}).keys()) == {
            "pressureChurn",
            "driftMomentum",
            "driftDelta",
            "absDriftDelta",
        }, payload
        assert isinstance(payload.get("whatIfAlt"), str), payload
        assert set(payload.get("whatIfAltSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "currentLane",
            "altLane",
            "baselineRisk",
            "imbalance",
            "pressureChurn",
            "projectedRisk",
            "deltaRisk",
            "reason",
        }, payload
        assert payload.get("whatIfConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfConfidenceSignals", {}).keys()) == {
            "flagEnabled",
            "deltaRisk",
            "currentLane",
            "altLane",
            "routeActionConfidence",
            "reason",
        }, payload
        assert payload.get("whatIfAlign") in {"ALIGNED", "DIVERGED"}, payload
        assert set(payload.get("whatIfAlignSignals", {}).keys()) == {
            "flagEnabled",
            "routeAction",
            "routeActionLane",
            "altLane",
            "reason",
        }, payload
        assert payload.get("whatIfBand") in {"GAIN", "NEUTRAL", "LOSS"}, payload
        assert set(payload.get("whatIfBandSignals", {}).keys()) == {
            "flagEnabled",
            "deltaRisk",
            "currentLane",
            "altLane",
            "reason",
        }, payload
        assert payload.get("whatIfMagnitude") in {"SMALL", "MED", "LARGE"}, payload
        assert set(payload.get("whatIfMagnitudeSignals", {}).keys()) == {
            "flagEnabled",
            "deltaRisk",
            "absDeltaRisk",
            "reason",
        }, payload
        assert payload.get("whatIfFit") in {"SAFE", "EVEN", "TENSE"}, payload
        assert set(payload.get("whatIfFitSignals", {}).keys()) == {
            "flagEnabled",
            "pressureBand",
            "projectedRisk",
            "projectedBand",
            "reason",
        }, payload
        assert payload.get("whatIfFallback") in {"OFF", "NONE", "PORTAL", "ALT", "PRESSURE"}, payload
        assert set(payload.get("whatIfFallbackSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "whatIfAlign",
            "altLane",
            "routeAction",
            "routeActionLane",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfFallbackConfidenceSignals", {}).keys()) == {
            "flagEnabled",
            "fallback",
            "whatIfAlign",
            "deltaRisk",
            "routeActionConfidence",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackFit") in {"SAFE", "EVEN", "TENSE"}, payload
        assert set(payload.get("whatIfFallbackFitSignals", {}).keys()) == {
            "flagEnabled",
            "fallback",
            "pressureBand",
            "baselineRisk",
            "projectedRisk",
            "projectedBand",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfFallbackWhy"), str), payload
        assert set(payload.get("whatIfFallbackWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "fallback",
            "fallbackConfidence",
            "fallbackFit",
            "pressureBand",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackAlign") in {"SYNC", "ASYNC"}, payload
        assert set(payload.get("whatIfFallbackAlignSignals", {}).keys()) == {
            "fallback",
            "laneFocus",
            "actionable",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackMagnitude") in {"SMALL", "MED", "LARGE"}, payload
        assert set(payload.get("whatIfFallbackMagnitudeSignals", {}).keys()) == {
            "flagEnabled",
            "fallback",
            "deltaRisk",
            "absDeltaRisk",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfFallbackAlt2"), str), payload
        assert set(payload.get("whatIfFallbackAlt2Signals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "fallback",
            "fallbackLane",
            "portalScore",
            "altScore",
            "pressureScore",
            "topScore",
            "secondScore",
            "minTopScore",
            "minGap",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackAlt2Confidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfFallbackAlt2ConfidenceSignals", {}).keys()) == {
            "flagEnabled",
            "alt2",
            "fallbackLane",
            "topScore",
            "secondScore",
            "scoreGap",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackPlan") in {"PRIMARY", "SECONDARY", "HOLD"}, payload
        assert set(payload.get("whatIfFallbackPlanSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "fallback",
            "fallbackConfidence",
            "fallbackAlt2",
            "fallbackAlt2Confidence",
            "primaryActionable",
            "secondaryActionable",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackPlanFit") in {"SAFE", "EVEN", "TENSE"}, payload
        assert set(payload.get("whatIfFallbackPlanFitSignals", {}).keys()) == {
            "plan",
            "planLane",
            "pressureBand",
            "projectedBand",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfFallbackPlanWhy"), str), payload
        assert set(payload.get("whatIfFallbackPlanWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "plan",
            "planFit",
            "planReason",
            "reason",
        }, payload
        assert payload.get("whatIfSplit") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "primaryLane",
            "secondaryLane",
            "primaryConfidence",
            "secondaryConfidence",
            "lanesDiverged",
            "absDeltaRisk",
            "strongDelta",
            "strongConfidence",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitLanes"), str), payload
        assert set(payload.get("whatIfSplitLanesSignals", {}).keys()) == {
            "primaryActionable",
            "secondaryActionable",
            "reason",
        }, payload
        assert payload.get("whatIfSplitConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitConfidenceSignals", {}).keys()) == {
            "split",
            "flagEnabled",
            "primaryConfidence",
            "secondaryConfidence",
            "strongConfidence",
            "strongDelta",
            "reason",
        }, payload
        assert payload.get("whatIfSplitSafe") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitSafeSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "split",
            "primaryConfidence",
            "secondaryConfidence",
            "primaryFit",
            "secondaryConfidenceGate",
            "splitArmed",
            "primarySafe",
            "secondarySafe",
            "reason",
        }, payload
        assert payload.get("whatIfSplitPosture") in {"SAFE", "WATCH", "HOLD"}, payload
        assert set(payload.get("whatIfSplitPostureSignals", {}).keys()) == {
            "split",
            "splitSafe",
            "splitConfidence",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitCooloff"), int), payload
        assert set(payload.get("whatIfSplitCooloffSignals", {}).keys()) == {
            "active",
            "currentSplit",
            "priorSplit",
            "priorCooloff",
            "reason",
            "priorLoaded",
        }, payload
        assert payload.get("whatIfSplitEscalate") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitEscalateSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "split",
            "splitArmed",
            "lanesDiverged",
            "planFit",
            "tenseFit",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscalateConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscalateConfidenceSignals", {}).keys()) == {
            "splitEscalate",
            "splitConfidence",
            "planFit",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscLanes"), str), payload
        assert set(payload.get("whatIfSplitEscLanesSignals", {}).keys()) == {
            "splitEscalate",
            "primaryActionable",
            "secondaryActionable",
            "lanesDiverged",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscCool"), int), payload
        assert set(payload.get("whatIfSplitEscCoolSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "active",
            "currentSplitEscalate",
            "priorSplitEscalate",
            "priorCooloff",
            "reason",
            "priorLoaded",
        }, payload
        assert payload.get("whatIfSplitEscState") in {"ARMED", "COOLING", "IDLE"}, payload
        assert set(payload.get("whatIfSplitEscStateSignals", {}).keys()) == {
            "splitEscalate",
            "splitEscCool",
            "cooling",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscPressure") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscPressureSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscState",
            "splitEscCool",
            "pressureBand",
            "baseRank",
            "adjustedRank",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecover"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscState",
            "splitEscLanes",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverConfidenceSignals", {}).keys()) == {
            "splitEscRecover",
            "splitEscState",
            "splitEscPressure",
            "splitEscLanes",
            "laneDivergence",
            "laneCount",
            "pressureRank",
            "stateEasing",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverAlt"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverAltSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecover",
            "splitEscState",
            "splitEscLanes",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverAltConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverAltConfidenceSignals", {}).keys()) == {
            "splitEscRecoverAlt",
            "splitEscState",
            "splitEscPressure",
            "splitEscLanes",
            "laneDivergence",
            "laneCount",
            "pressureRank",
            "stateEasing",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverPlan") in {"PRIMARY", "ALT", "HOLD"}, payload
        assert set(payload.get("whatIfSplitEscRecoverPlanSignals", {}).keys()) == {
            "splitEscRecover",
            "splitEscRecoverAlt",
            "hasPrimary",
            "hasAlt",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverWhy") in {
            "FLAG OFF",
            "PRIMARY RELIEF",
            "PRIMARY STABILIZE",
            "PRIMARY STEADY",
            "ALT SAFETY NET",
            "ALT CONTINGENCY",
            "HOLD FOR SIGNAL",
        }, payload
        assert set(payload.get("whatIfSplitEscRecoverWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecoverPlan",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverTempo") in {"FAST", "STEADY", "DEFER"}, payload
        assert set(payload.get("whatIfSplitEscRecoverTempoSignals", {}).keys()) == {
            "splitEscRecoverPlan",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVeto") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "splitEscRecoverPlan",
            "confidenceLow",
            "pressureHigh",
            "planActionable",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoConfidenceSignals", {}).keys()) == {
            "splitEscRecoverVeto",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "splitEscRecoverPlan",
            "confidenceLow",
            "pressureHigh",
            "planActionable",
            "vetoOn",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverVetoDwell"), int) and payload["whatIfSplitEscRecoverVetoDwell"] >= 0, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoDwellSignals", {}).keys()) == {
            "currentState",
            "priorState",
            "priorDwell",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoReleaseRoute") in {"PORTAL", "ALT", "PRESSURE", "HOLD", "NONE"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoReleaseRouteSignals", {}).keys()) == {
            "splitEscRecoverVetoRelease",
            "splitEscRecoverVetoState",
            "splitEscRecover",
            "splitEscRecoverAlt",
            "splitEscRecoverPlan",
            "primaryActionable",
            "altActionable",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoReleaseCadence") in {"ACCEL", "STEADY", "DECAY", "FLAG OFF"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoReleaseCadenceSignals", {}).keys()) == {
            "tick",
            "priorTick",
            "delta",
            "numeric",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearm") in {"WATCH", "OFF"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "releaseTickPhase",
            "splitEscPressure",
            "releaseCadence",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmConfidenceSignals", {}).keys()) == {
            "splitEscRecoverVetoRearm",
            "flagEnabled",
            "releaseTickPhase",
            "splitEscPressure",
            "releaseCadence",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverVetoRearmWhy"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecoverVetoRearm",
            "splitEscRecoverVetoRearmConfidence",
            "splitEscPressure",
            "releaseTickPhase",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverVetoRearmCooloff"), int) and payload["whatIfSplitEscRecoverVetoRearmCooloff"] >= 0, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmCooloffSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "active",
            "currentRearm",
            "priorRearm",
            "priorCooloff",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmCooloffState") in {"ACTIVE", "IDLE"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmCooloffStateSignals", {}).keys()) == {
            "splitEscRecoverVetoRearm",
            "splitEscRecoverVetoRearmCooloff",
            "active",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmFit") in {"RELIEF", "EVEN", "TENSE"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmFitSignals", {}).keys()) == {
            "splitEscRecoverVetoRearmCooloffState",
            "splitEscRecoverVetoRearmCooloff",
            "splitEscPressure",
            "reason",
        }, payload
        assert set(payload["pressureEdits"].keys()) == {"added", "removed", "net"}, payload
        assert "tokenTotals" in payload, payload
        assert "VIBE TRAIL CONF:" in payload["tokenTotals"]["net"], payload
        assert "VIBE TRAIL CONF RAIL:" in payload["tokenTotals"]["net"], payload
        assert "VTC:" in payload["tokenTotals"]["net"], payload
        assert "VTCR:" in payload["tokenTotals"]["net"], payload
        assert "VIBE TRAIL WHY CONF:" in payload["tokenTotals"]["net"], payload
        assert "VTWC:" in payload["tokenTotals"]["net"], payload
        assert "VIBE TRAIL WHY CONF WHY:" in payload["tokenTotals"]["net"], payload
        assert "VTCW:" in payload["tokenTotals"]["net"], payload
        assert "ROUTE GLOW CONF:" in payload["tokenTotals"]["net"], payload
        assert "RGC:" in payload["tokenTotals"]["net"], payload
        assert "ROUTE GLOW FX CONF:" in payload["tokenTotals"]["net"], payload
        assert "RGFXC:" in payload["tokenTotals"]["net"], payload
        assert "ROUTE GLOW FX CONF WHY:" in payload["tokenTotals"]["net"], payload
        assert "RGFXW:" in payload["tokenTotals"]["net"], payload
        assert "ROUTE GLOW FX CONF WHY RAIL:" in payload["tokenTotals"]["net"], payload
        assert "RGFXWR:" in payload["tokenTotals"]["net"], payload
        assert "RGFXWRM:" in payload["tokenTotals"]["net"], payload
        assert "RGFXWRIUFX:" in payload["tokenTotals"]["net"], payload
        assert "DMGNUM STACK CAP:" in payload["tokenTotals"]["net"], payload
        assert "DMGNUM LIFE:" in payload["tokenTotals"]["net"], payload
        assert "DMGNUM LIFE CONF:" in payload["tokenTotals"]["net"], payload
        assert "DMGNUM LIFE CONF Δ:" in payload["tokenTotals"]["net"], payload
        assert "DMGNUM LIFE TREND:" in payload["tokenTotals"]["net"], payload
        assert "DMGNUM LIFE TREND FX PULSE:" in payload["tokenTotals"]["net"], payload
        assert "DMGNUM LIFE TREND FX PULSE CONF:" in payload["tokenTotals"]["net"], payload
        assert "DMG GLYPH:" in payload["tokenTotals"]["net"], payload
        assert "DMG GLYPH FX LIVE:" in payload["tokenTotals"]["net"], payload
        assert "LPR HYS THR:" in payload["tokenTotals"]["net"], payload
        assert "LPR HYS WINDOW Δ:" in payload["tokenTotals"]["net"], payload
        assert "tokenFamilyTotals" in payload, payload
        assert "vibeTrailWhyAlias" in payload["tokenFamilyTotals"], payload
        assert "vibeTrailWhyConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "vibeTrailWhyConfidenceWhyAlias" in payload["tokenFamilyTotals"], payload
        assert "vibeTrailWhyConfidenceWhyConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "vibeTrailArcAlias" in payload["tokenFamilyTotals"], payload
        assert "ambientRampConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "pulseHeatFxAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailMode" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailIntensity" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailIntensityWhy" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias" in payload["tokenFamilyTotals"], payload
        assert "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias" in payload["tokenFamilyTotals"], payload
        assert "urgencyStackTierAlias" in payload["tokenFamilyTotals"], payload
        assert "urgencyStackRailAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumStackCapAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumLifeAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumLifeConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumLifeConfidenceDeltaAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumLifeTrendAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumLifeTrendFxPulseAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumLifeTrendFxPulseConfidenceAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgnumLifeTrendFxPulseRemapPlanAlias" in payload["tokenFamilyTotals"], payload
        assert "pulseRemapMomentumAlias" in payload["tokenFamilyTotals"], payload
        assert "pulseRemapMomentumSuppressionAlias" in payload["tokenFamilyTotals"], payload
        assert "pulseRemapSuppressionPlanAlias" in payload["tokenFamilyTotals"], payload
        assert "pulseRemapSuppressionPostureWarningAlias" in payload["tokenFamilyTotals"], payload
        assert "dmgGlyphFxLiveAlias" in payload["tokenFamilyTotals"], payload
        assert "lanePriorityHysteresisThresholdAlias" in payload["tokenFamilyTotals"], payload
        assert "lanePriorityHysteresisWindowDeltaAlias" in payload["tokenFamilyTotals"], payload
        assert set(payload["tokenFamilyTotals"]["vibeTrailWhyAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["vibeTrailWhyConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["vibeTrailWhyConfidenceWhyAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["vibeTrailWhyConfidenceWhyConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["vibeTrailArcAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["ambientRampConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["pulseHeatFxAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxConfidenceWhyAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxConfidenceWhyRailAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxConfidenceWhyRailMode"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxConfidenceWhyRailIntensity"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxConfidenceWhyRailIntensityWhy"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["urgencyStackTierAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["urgencyStackRailAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumStackCapAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumLifeAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumLifeConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumLifeConfidenceDeltaAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumLifeTrendAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumLifeTrendFxPulseAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumLifeTrendFxPulseConfidenceAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgnumLifeTrendFxPulseRemapPlanAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["pulseRemapMomentumAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["pulseRemapMomentumSuppressionAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["pulseRemapSuppressionPlanAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["pulseRemapSuppressionPostureWarningAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["dmgGlyphFxLiveAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["lanePriorityHysteresisThresholdAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert set(payload["tokenFamilyTotals"]["lanePriorityHysteresisWindowDeltaAlias"].keys()) == {
            "aliases",
            "aliasesTouched",
            "aliasesTouchedCount",
            "added",
            "removed",
            "net",
            "churn",
            "coverage",
        }, payload
        assert payload.get("pulseHeatFxCompactBudgetDrift") in {"STABLE", "WATCH", "SPIKE"}, payload
        assert set(payload.get("pulseHeatFxCompactBudgetDriftSignals", {}).keys()) == {
            "reason",
            "compactNet",
            "familyNet",
            "familyChurn",
            "absFamilyNet",
            "absCompactNet",
        }, payload
        assert payload.get("routeGlowFxCompactBudgetDrift") in {"STABLE", "WATCH", "SPIKE"}, payload
        assert set(payload.get("routeGlowFxCompactBudgetDriftSignals", {}).keys()) == {
            "reason",
            "compactNet",
            "familyNet",
            "familyChurn",
            "absFamilyNet",
            "absCompactNet",
        }, payload
        assert payload.get("routeGlowFxConfWhyRailModeCompactBudgetDrift") in {"STABLE", "WATCH", "SPIKE"}, payload
        assert set(payload.get("routeGlowFxConfWhyRailModeCompactBudgetDriftSignals", {}).keys()) == {
            "reason",
            "compactNet",
            "familyNet",
            "familyChurn",
            "absFamilyNet",
            "absCompactNet",
        }, payload
        assert "stickyTokens" in payload, payload
        assert set(payload["stickyTokens"].keys()) == {"count", "tokens"}, payload
        assert payload["stickyTokens"]["count"] == len(payload["stickyTokens"]["tokens"]), payload
        assert payload.get("anomalyPulse") in {"ON", "OFF"}, payload
        assert payload.get("anomalyConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("anomalyPulseSignals", {}).keys()) == {
            "stickyCount",
            "stickyThreshold",
            "pressureChurn",
            "pressureThreshold",
            "stickyMet",
            "pressureMet",
            "triggerCount",
            "stickyGap",
            "pressureGap",
            "combinedGap",
            "spike",
        }, payload
        assert isinstance(payload.get("topTokenMovers"), list), payload
        if payload["topTokenMovers"]:
            assert {"token", "net", "added", "removed"}.issubset(payload["topTokenMovers"][0].keys()), payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmNudgeWindow") in {"ARMED", "COOLING", "IDLE"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmNudgeWindowSignals", {}).keys()) == {
            "splitEscRecoverVetoRearm",
            "splitEscRecoverVetoRearmCooloffState",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverVetoRearmNudgeWhy"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmNudgeWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecoverVetoRearmNudge",
            "splitEscRecoverVetoRearmNudgeConfidence",
            "splitEscRecoverVetoRearmNudgeWindow",
            "splitEscRecoverVetoRearmFit",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmNudgeImpact") in {"DEFENSIVE", "CAUTIOUS", "NEUTRAL"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmNudgeImpactSignals", {}).keys()) == {
            "splitEscRecoverVetoRearmNudge",
            "splitEscRecoverVetoRearmNudgeWindow",
            "splitEscRecoverVetoRearmFit",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmNudgeDrift") in {"STABLE", "SHIFTING"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmNudgeDriftSignals", {}).keys()) == {
            "currentNudgeWhy",
            "priorNudgeWhy",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverVetoRearmCoach"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmCoachSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecover",
            "splitEscRecoverAlt",
            "splitEscRecoverPlan",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmCoachConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmCoachConfidenceSignals", {}).keys()) == {
            "splitEscRecoverVetoRearmCoach",
            "splitEscRecoverVetoRearmNudgeConfidence",
            "splitEscRecoverVetoRearmFit",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmCoachHandoff") in {"LOCKED", "FLEX", "NONE"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmCoachHandoffSignals", {}).keys()) == {
            "splitEscRecoverVetoRearmCoach",
            "splitEscRecoverVetoRearmCoachMode",
            "splitEscRecoverVetoRearmCoachConfidence",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmCoachHandoffFit") in {"SAFE", "EVEN", "TENSE"}, payload
        assert payload.get("actionPace") in {"ACCEL", "STEADY", "BRAKE"}, payload
        assert set(payload.get("actionPaceSignals", {}).keys()) == {
            "actionGuard",
            "actionStability",
            "pressureLag",
            "reason",
        }, payload
        assert isinstance(payload.get("paceDrift"), int), payload
        assert set(payload.get("paceDriftSignals", {}).keys()) == {
            "currentPace",
            "currentScore",
            "priorPace",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("actionPaceWindow") in {"OPEN", "HOLD", "CLOSE"}, payload
        assert set(payload.get("actionPaceWindowSignals", {}).keys()) == {
            "actionPace",
            "actionGuard",
            "paceDrift",
            "reason",
        }, payload
        assert payload.get("actionPaceWindowConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("actionPaceWindowConfidenceSignals", {}).keys()) == {
            "actionPaceWindow",
            "actionStability",
            "paceDrift",
            "driftContinuity",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("actionPaceAltWindow"), str), payload
        assert set(payload.get("actionPaceAltWindowSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceWindow",
            "routeSandbox",
            "sandboxTarget",
            "sandboxReadiness",
            "reason",
        }, payload
        assert payload.get("actionPaceAltWindowConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("actionPaceAltWindowConfidenceSignals", {}).keys()) == {
            "actionPaceAltWindow",
            "actionPaceWindowConfidence",
            "flagEnabled",
            "routeSandbox",
            "sandboxTarget",
            "sandboxReadiness",
            "reason",
        }, payload
        assert isinstance(payload.get("actionPaceAltWindowFit"), str), payload
        assert set(payload.get("actionPaceAltWindowFitSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceAltWindow",
            "routeSandbox",
            "sandboxTarget",
            "sandboxReadiness",
            "pressureBand",
            "reason",
        }, payload
        assert isinstance(payload.get("actionPaceAltWindowWhy"), str), payload
        assert set(payload.get("actionPaceAltWindowWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceAltWindow",
            "actionPaceAltWindowConfidence",
            "actionPaceAltWindowFit",
            "routeSandbox",
            "sandboxTarget",
            "sandboxReadiness",
            "reason",
        }, payload
        assert isinstance(payload.get("altStepWhyConfidenceDrift"), int), payload
        assert set(payload.get("altStepWhyConfidenceDriftSignals", {}).keys()) == {
            "currentAltStepWhy",
            "currentAltStepWhyConfidence",
            "currentScore",
            "priorAltStepWhyConfidence",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("altWhyGlyphDrift"), int), payload
        assert set(payload.get("altWhyGlyphDriftSignals", {}).keys()) == {
            "currentAltWhyGlyphNet",
            "priorAltWhyGlyphNet",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("altWhyGlyphModeDrift"), int), payload
        assert set(payload.get("altWhyGlyphModeDriftSignals", {}).keys()) == {
            "currentAltWhyGlyphModeNet",
            "priorAltWhyGlyphModeNet",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("altWhyGlyphModeConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("altWhyGlyphModeConfidenceSignals", {}).keys()) == {
            "altWhyGlyphModeDrift",
            "absAltWhyGlyphModeDrift",
            "currentAltWhyGlyphModeNet",
            "priorAltWhyGlyphModeNet",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("altWhyGlyphModeConfidenceDrift"), int), payload
        assert set(payload.get("altWhyGlyphModeConfidenceDriftSignals", {}).keys()) == {
            "currentAltWhyGlyphModeConfidence",
            "currentScore",
            "priorAltWhyGlyphModeConfidence",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("altWhyGlyphModeConfidenceWhy"), str), payload
        assert set(payload.get("altWhyGlyphModeConfidenceWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "altWhyGlyphModeConfidence",
            "altWhyGlyphModeConfidenceDrift",
            "absAltWhyGlyphModeDrift",
            "currentAltWhyGlyphModeNet",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("actionPaceAltWindowUrgency") in {"OFF", "NOW", "SOON", "LATER"}, payload
        assert set(payload.get("actionPaceAltWindowUrgencySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceAltWindow",
            "actionPaceAltWindowConfidence",
            "actionPaceAltWindowFit",
            "actionPaceAltWindowWhy",
            "reason",
        }, payload
        assert isinstance(payload.get("actionPaceAltWindowStep"), str), payload
        assert set(payload.get("actionPaceAltWindowStepSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceAltWindow",
            "actionPaceAltWindowConfidence",
            "actionPaceAltWindowFit",
            "actionPaceAltWindowUrgency",
            "routeSandbox",
            "sandboxTarget",
            "sandboxReadiness",
            "reason",
        }, payload
        assert isinstance(payload.get("actionPaceAltWindowStepGlyph"), str), payload
        assert set(payload.get("actionPaceAltWindowStepGlyphSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceAltWindowStep",
            "actionPaceAltWindowUrgency",
            "actionPaceAltWindowFit",
            "reason",
        }, payload
        assert payload.get("actionPaceAltWindowPulse") in {"OFF", "COOL", "LIVE", "HOT"}, payload
        assert set(payload.get("actionPaceAltWindowPulseSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceAltWindowUrgency",
            "actionPaceAltWindowFit",
            "actionPaceAltWindowConfidence",
            "reason",
        }, payload
        assert isinstance(payload.get("actionPaceAltWindowPulseDrift"), int), payload
        assert set(payload.get("actionPaceAltWindowPulseDriftSignals", {}).keys()) == {
            "currentPulse",
            "currentScore",
            "priorPulse",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("routePulseLink") in {"OFF", "SOFT", "SHARP"}, payload
        assert set(payload.get("routePulseLinkSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPaceAltWindowPulse",
            "actionPaceAltWindowPulseDrift",
            "actionPaceAltWindowFit",
            "reason",
        }, payload
        assert payload.get("routePulseLinkConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("routePulseLinkConfidenceSignals", {}).keys()) == {
            "routePulseLink",
            "actionPaceAltWindowPulse",
            "actionPaceAltWindowPulseDrift",
            "actionPaceAltWindowFit",
            "actionPaceAltWindowConfidence",
            "reason",
        }, payload
        assert isinstance(payload.get("routePulseLinkStreak"), int), payload
        assert set(payload.get("routePulseLinkStreakSignals", {}).keys()) == {
            "currentRoutePulseLink",
            "priorRoutePulseLink",
            "priorStreak",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("routePulseLinkMode") in {"IDLE", "SUSTAIN", "SURGE"}, payload
        assert set(payload.get("routePulseLinkModeSignals", {}).keys()) == {
            "routePulseLink",
            "routePulseLinkStreak",
            "actionPaceAltWindowPulseDrift",
            "reason",
        }, payload
        assert isinstance(payload.get("routePulseLinkModeDrift"), int), payload
        assert set(payload.get("routePulseLinkModeDriftSignals", {}).keys()) == {
            "currentMode",
            "currentScore",
            "priorMode",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("routePulseLinkModeStabilityStreak"), int), payload
        assert set(payload.get("routePulseLinkModeStabilityStreakSignals", {}).keys()) == {
            "currentMode",
            "priorMode",
            "priorStreak",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("routePulseLinkModeWhy"), str), payload
        assert set(payload.get("routePulseLinkModeWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "routePulseLinkMode",
            "routePulseLink",
            "routePulseLinkModeDrift",
            "routePulseLinkStreak",
            "reason",
        }, payload
        assert payload.get("routePulseLinkModeFit") in {"SYNC", "WATCH", "BREAK", "RESET"}, payload
        assert set(payload.get("routePulseLinkModeFitSignals", {}).keys()) == {
            "routePulseLinkMode",
            "routePulseLinkModeDrift",
            "routePulseLinkModeStabilityStreak",
            "reason",
        }, payload
        assert isinstance(payload.get("routePulseLinkModeFitDrift"), int), payload
        assert set(payload.get("routePulseLinkModeFitDriftSignals", {}).keys()) == {
            "currentFit",
            "currentScore",
            "priorFit",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("routePulseTokenPriority") in {"FIT-FIRST", "MODE-FIRST", "OFF"}, payload
        assert set(payload.get("routePulseTokenPrioritySignals", {}).keys()) == {
            "envName",
            "configuredMode",
            "routePulseLinkModeFitDrift",
            "priorMode",
            "priorLoaded",
            "guardHeld",
            "reason",
        }, payload
        assert isinstance(payload.get("actionPaceWhy"), str), payload
        assert set(payload.get("actionPaceWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionPace",
            "actionGuard",
            "actionStability",
            "pressureLag",
            "paceDrift",
            "reason",
        }, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmCoachHandoffFitSignals", {}).keys()) == {
            "splitEscRecoverVetoRearmCoachHandoff",
            "splitEscPressure",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverVetoRearmCoachHandoffWhy"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmCoachHandoffWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecoverVetoRearmCoachHandoff",
            "splitEscRecoverVetoRearmCoachHandoffFit",
            "splitEscRecoverVetoRearmCoachConfidence",
            "reason",
        }, payload
        assert isinstance(payload.get("ambientRampWhyAutoRemapPlan"), str), payload
        assert isinstance(payload.get("ambientRampWhyAutoRemapPlanCompact"), str), payload
        assert isinstance(payload.get("ambientRampWhyAutoRemapWhyCompact"), str), payload
        assert set(payload.get("ambientRampWhyAutoRemapPlanSignals", {}).keys()) == {
            "recommendation",
            "confidence",
            "parity",
            "driftRisk",
            "pressureBand",
            "ambientRampWhyChurn",
            "ambientRampWhyNet",
            "offlineOnly",
            "rationale",
            "nextAction",
            "rerankPolicy",
            "candidateCount",
            "confidenceStreak",
            "candidateSuppressed",
        }, payload
        assert isinstance(payload.get("ambientRampWhyAutoRemapPlanDrift"), int), payload
        assert set(payload.get("ambientRampWhyAutoRemapPlanDriftSignals", {}).keys()) == {
            "currentPlan",
            "currentScore",
            "priorPlan",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("ambientRampWhyAutoRemapPlanConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("ambientRampWhyAutoRemapPlanConfidenceSignals", {}).keys()) == {
            "selectedPlan",
            "recommendationConfidence",
            "parity",
            "driftRisk",
            "pressureBand",
            "planDrift",
            "priorLoaded",
            "rationale",
        }, payload
        assert isinstance(payload.get("ambientRampWhyAutoRemapPlanConfidenceDrift"), int), payload
        assert set(payload.get("ambientRampWhyAutoRemapPlanConfidenceDriftSignals", {}).keys()) == {
            "currentConfidence",
            "currentScore",
            "priorConfidence",
            "priorScore",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("ambientRampWhyAutoRemapConfidenceBandAlias") in {"L", "M", "H"}, payload
        assert set(payload.get("ambientRampWhyAutoRemapConfidenceBandAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert payload.get("ambientRampWhyAutoRemapConfidenceMomentumFreezeRecommendation") in {"FREEZE", "WATCH", "ALLOW"}, payload
        assert set(payload.get("ambientRampWhyAutoRemapConfidenceMomentumFreezeRecommendationSignals", {}).keys()) == {
            "currentConfidence",
            "confidenceDrift",
            "confidenceStreak",
            "planDrift",
            "parity",
            "driftRisk",
            "candidateSuppressed",
            "oscillating",
            "offlineOnly",
            "reason",
        }, payload
        assert payload.get("ambientRampWhyAutoRemapConfidenceMomentumAlias") in {"F", "W", "A"}, payload
        assert set(payload.get("ambientRampWhyAutoRemapConfidenceMomentumAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert isinstance(payload.get("ambientRampWhyAutoRemapConfidenceMomentumScore"), int), payload
        assert 0 <= payload.get("ambientRampWhyAutoRemapConfidenceMomentumScore") <= 100, payload
        assert set(payload.get("ambientRampWhyAutoRemapConfidenceMomentumScoreSignals", {}).keys()) == {
            "recommendation",
            "base",
            "confidenceDrift",
            "confidenceStreak",
            "planDrift",
            "driftRisk",
            "parity",
            "candidateSuppressed",
        }, payload
        assert out_ambient_auto_remap_json.exists()
        assert out_ambient_auto_remap_md.exists()
        md_text = out_md.read_text(encoding="utf-8")
        assert "Token Totals" in md_text
        assert "Top Token Movers" in md_text
        assert "Token Family Coverage" in md_text
        assert "VTA + VIBE TRAIL ARC" in md_text
        assert "ARC + AMBIENT RAMP CONF" in md_text
        assert "ARW + AMBIENT RAMP WHY" in md_text
        assert "ARW REC PARITY:" in md_text
        assert "PULSE HEAT FX:" in md_text
        assert "VTW FAMILY CHURN" in md_text
        assert "VTWC FAMILY CHURN" in md_text
        assert "VTCW FAMILY CHURN" in md_text
        assert "VTCWC FAMILY CHURN" in md_text
        assert "VTA FAMILY CHURN" in md_text
        assert "AMBIENT RAMP CONF FAMILY CHURN" in md_text
        assert "PULSE HEAT FX FAMILY CHURN" in md_text
        assert "ROUTE GLOW FX FAMILY CHURN" in md_text
        assert "ROUTE GLOW CONF FAMILY CHURN" in md_text
        assert "ROUTE GLOW FX CONF FAMILY CHURN" in md_text
        assert "ROUTE GLOW FX CONF WHY FAMILY CHURN" in md_text
        assert "ROUTE GLOW FX CONF WHY RAIL FAMILY CHURN" in md_text
        assert "ROUTE GLOW FX CONF WHY RAIL MODE FAMILY CHURN" in md_text
        assert "ROUTE GLOW FX CONF WHY RAIL INTENSITY FAMILY CHURN" in md_text
        assert "RGFXWRI WHY FAMILY CHURN" in md_text
        assert "RGFXWRI WHY CONF FAMILY CHURN" in md_text
        assert "RGFXWRIU URGENCY FAMILY CHURN" in md_text
        assert "RGFXWRIUP URGENCY PARITY COMPACT FAMILY CHURN" in md_text
        assert "URGENCY PARITY LABEL FAMILY CHURN" in md_text
        assert "RGFXWRIUFX URGENCY FX FAMILY CHURN" in md_text
        assert "URG STACK FAMILY CHURN" in md_text
        assert "URG STACK RAIL FAMILY CHURN" in md_text
        assert "DMGNUM STACK CAP FAMILY CHURN" in md_text
        assert "DMGNUM LIFE FAMILY CHURN" in md_text
        assert "DMGNUM LIFE CONF FAMILY CHURN" in md_text
        assert "DMGNUM LIFE CONF Δ FAMILY CHURN" in md_text
        assert "DMGNUM LIFE TREND FAMILY CHURN" in md_text
        assert "DMGNUM LIFE TREND FX PULSE FAMILY CHURN" in md_text
        assert "DMGNUM LIFE TREND FX PULSE CONF FAMILY CHURN" in md_text
        assert "DMGNUM LIFE TREND FX PULSE REMAP PLAN FAMILY CHURN" in md_text
        assert "PULSE REMAP MOMENTUM FAMILY CHURN" in md_text
        assert "PULSE REMAP SUPPRESS FAMILY CHURN" in md_text
        assert "PULSE REMAP SUPPRESS PLAN FAMILY CHURN" in md_text
        assert "DMG GLYPH FAMILY CHURN" in md_text
        assert "DMG GLYPH FX LIVE FAMILY CHURN" in md_text
        assert "LPR HYS THR FAMILY CHURN" in md_text
        assert "LPR HYS WINDOW Δ FAMILY CHURN" in md_text
        assert "LANE CADENCE SUMMARY" in md_text
        assert "LBA:" in md_text
        assert "LANE BUCKET AGE:" in md_text
        assert "LANE BUCKET AGE Δ:" in md_text
        assert "LANE CADENCE RECENCY:" in md_text
        assert "LANE PRIORITY REC:" in md_text
        assert "LPR:" in md_text
        assert "LPR HYS:" in md_text
        assert "LPR HYS RAIL:" in md_text
        assert "LPR HYS THRESH REC:" in md_text
        assert "LPR VOL REGIME:" in md_text
        assert "LPR HYS THR:" in md_text
        assert "LPR HYS WINDOW:" in md_text
        assert "LPR HYS WINDOW Δ:" in md_text
        assert "LANE PRIORITY REC CONF:" in md_text
        assert "LANE PRIORITY REC HYSTERESIS:" in md_text
        assert "ROUTE GLOW FX + RGFX:" in md_text
        assert "ROUTE GLOW CONF:" in md_text
        assert "ROUTE GLOW FX CONF + RGFXC:" in md_text
        assert "ROUTE GLOW FX CONF WHY + RGFXW:" in md_text
        assert "ROUTE GLOW FX CONF WHY RAIL + RGFXWR:" in md_text
        assert "RGFXWRM RAIL MODE:" in md_text
        assert "RGFXWRI RAIL INTENSITY:" in md_text
        assert "RGFXWRI WHY:" in md_text
        assert "RGFXWRIWC + RGFXWRI WHY CONF:" in md_text
        assert "RGFXWRIU + ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:" in md_text
        assert "RGFXWRIUP URGENCY PARITY COMPACT:" in md_text
        assert "ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY PARITY:" in md_text
        assert "RGFXWRIUFX URGENCY FX:" in md_text
        assert "URG STACK:" in md_text
        assert "URG STACK RAIL:" in md_text
        assert "DMGNUM STACK CAP:" in md_text
        assert "DMGNUM LIFE:" in md_text
        assert "DMGNUM LIFE CONF:" in md_text
        assert "DMGNUM LIFE CONF Δ:" in md_text
        assert "DMGNUM LIFE TREND:" in md_text
        assert "DMGNUM LIFE TREND FX PULSE:" in md_text
        assert "DMGNUM LIFE TREND FX PULSE CONF:" in md_text
        assert "DMGNUM LIFE TREND FX PULSE REMAP PLAN:" in md_text
        assert "PULSE REMAP MOMENTUM Δ:" in md_text
        assert "PULSE REMAP MOMENTUM SUPPRESS:" in md_text
        assert "PULSE REMAP SUPPRESS PLAN:" in md_text
        assert "PULSE REMAP SCENE:" in md_text
        assert "PULSE REMAP SCENE CONF:" in md_text
        assert "PULSE REMAP SCENE MICROLINE:" in md_text
        assert "PRMS:" in md_text
        assert "PRSP:" in md_text
        assert "PRPW:" in md_text
        assert "PRM + PULSE REMAP MOMENTUM:" in md_text
        assert "PRMS + PULSE REMAP MOMENTUM SUPPRESS:" in md_text
        assert "PRSP + PULSE REMAP SUPPRESS PLAN:" in md_text
        assert "PRMS FAMILY TREND:" in md_text
        assert "PRSP FAMILY TREND:" in md_text
        assert "DMG GLYPH:" in md_text
        assert "DMG GLYPH FX LIVE:" in md_text
        assert "LPR HYS THR:" in md_text
        assert "LPR VOL REGIME:" in md_text
        assert "LPR HYS WINDOW:" in md_text
        assert "LPR HYS WINDOW Δ:" in md_text
        assert "LANE CADENCE SUMMARY: SYSTEMS/OPS" in md_text
        assert "PULSE HEAT FX COMPACT-BUDGET DRIFT" in md_text
        assert "ROUTE GLOW FX COMPACT-BUDGET DRIFT" in md_text
        assert "ROUTE GLOW FX CONF WHY RAIL MODE COMPACT-BUDGET DRIFT" in md_text
        assert "MODE TREND" in md_text
        assert "PRESSURE BAND" in md_text
        assert "DRIFT RISK" in md_text
        assert "RGFXWRI WHY CONF POLICY REC" in md_text
        assert "AMBIENT RAMP CONF REC" in md_text
        assert "AMBIENT RAMP WHY REC" in md_text
        assert "AMBIENT RAMP WHY REC CONF" in md_text
        assert "AMBIENT RAMP WHY REC PARITY" in md_text
        assert "AMBIENT RAMP WHY AUTO-REMAP PLAN" in md_text
        assert "ARW AUTO PLAN" in md_text
        assert "ARW AUTO WHY" in md_text
        assert "ARW AUTO PLAN Δ" in md_text
        assert "ARW AUTO PLAN CONF" in md_text
        assert "ARW AUTO PLAN CONF Δ" in md_text
        assert "AMBIENT RAMP WHY REC CONF STREAK" in md_text
        assert "ARW AUTO PLAN FAMILY CHURN" in md_text
        assert "ARW APC FAMILY CHURN" in md_text
        assert "ARW AUTO PLAN CONF MOMENTUM FAMILY CHURN" in md_text
        assert "ARW MOMENTUM" in md_text
        assert "ARW MOMENTUM SCORE" in md_text
        assert "ARW MOMENTUM ARC" in md_text
        assert "ARW ARC PULSE" in md_text
        assert "ARW MOMENTUM FAMILY CHURN" in md_text
        assert "ARW MOMENTUM ARC FAMILY CHURN" in md_text
        assert "ARW ARC PULSE FAMILY CHURN" in md_text
        assert "ARW AUTO PLAN CANDIDATE SUPPRESS" in md_text
        assert "URGENCY STACK PRUNING REC" in md_text
        assert "URGENCY STACK RAIL REC" in md_text
        assert "DMG GLYPH SHAPE REMAP REC" in md_text
        assert "DMG GLYPH FX REMAP REC" in md_text
        assert "DMG GLYPH FX REMAP CONF" in md_text
        assert "DMGNUM LIFE TREND FX PULSE CONF REMAP REC" in md_text
        assert "PULSE REMAP MOMENTUM" in md_text
        assert "PRM:" in md_text
        assert "ROUTE VIBE DRIFT" in md_text
        assert "Route Vibe Drift (added/removed/net)" in md_text
        assert "FOCUS" in md_text
        assert "FOCUS STREAK" in md_text
        assert "FOCUS SHIFT" in md_text
        assert "FOCUS VOL" in md_text
        assert "ROUTE ACTION" in md_text
        assert "ACTION CONF" in md_text
        assert "FOCUS BAL" in md_text
        assert "FOCUS ENTROPY" in md_text
        assert "ACTION GUARD" in md_text
        assert "LANE LOCK" in md_text
        assert "ROUTE SANDBOX" in md_text
        assert "SANDBOX PLAN" in md_text
        assert "SANDBOX TARGET" in md_text
        assert "TARGET SRC" in md_text
        assert "SANDBOX TARGET CONF" in md_text
        assert "SANDBOX READY" in md_text
        assert "TARGET SHIFT" in md_text
        assert "SANDBOX COOLOFF" in md_text
        assert "DRIFT MOMENTUM" in md_text
        assert "ACTION STABILITY" in md_text
        assert "PRESSURE LAG" in md_text
        assert "ACTION PACE" in md_text
        assert "PACE DRIFT" in md_text
        assert "ACTION PACE WINDOW" in md_text
        assert "ACTION PACE WINDOW CONF" in md_text
        assert "ACTION PACE ALT WINDOW" in md_text
        assert "ACTION PACE ALT WINDOW CONF" in md_text
        assert "ALT STEP CONF Δ" in md_text
        assert "ALT STEP WHY CONF Δ" in md_text
        assert "ALT WHY GLYPH Δ" in md_text
        assert "ALT WHY GLYPH MODE Δ" in md_text
        assert "ALT WHY GLYPH MODE CONF" in md_text
        assert "ALT WHY GLYPH MODE CONF Δ" in md_text
        assert "ALT WHY GLYPH MODE CONF WHY" in md_text
        assert "ACTION PACE ALT WINDOW FIT" in md_text
        assert "ACTION PACE ALT WINDOW WHY" in md_text
        assert "ACTION PACE ALT WINDOW URGENCY" in md_text
        assert "ACTION PACE ALT WINDOW URGENCY Δ" in md_text
        assert "ACTION PACE ALT WINDOW STEP" in md_text
        assert "ACTION PACE ALT WINDOW STEP Δ" in md_text
        assert "ACTION PACE ALT WINDOW STEP GLYPH" in md_text
        assert "ACTION PACE ALT WINDOW PULSE" in md_text
        assert "ACTION PACE ALT WINDOW PULSE Δ" in md_text
        assert "ROUTE PULSE LINK" in md_text
        assert "ROUTE PULSE LINK CONF" in md_text
        assert "ROUTE PULSE LINK STREAK" in md_text
        assert "ROUTE PULSE LINK MODE" in md_text
        assert "ROUTE PULSE LINK MODE Δ" in md_text
        assert "ROUTE PULSE LINK MODE STREAK" in md_text
        assert "ROUTE PULSE LINK MODE WHY" in md_text
        assert "ROUTE PULSE LINK MODE FIT" in md_text
        assert "ROUTE PULSE LINK MODE FIT Δ" in md_text
        assert "ROUTE PULSE TOKEN PRIORITY" in md_text
        assert "ACTION PACE WHY" in md_text
        assert "WHAT-IF" in md_text
        assert "WHAT-IF CONF" in md_text
        assert "WHAT-IF ALIGN" in md_text
        assert "WHAT-IF BAND" in md_text
        assert "WHAT-IF MAG" in md_text
        assert "WHAT-IF FIT" in md_text
        assert "WHAT-IF FALLBACK" in md_text
        assert "WHAT-IF FALLBACK CONF" in md_text
        assert "WHAT-IF FALLBACK FIT" in md_text
        assert "WHAT-IF FALLBACK WHY" in md_text
        assert "WHAT-IF FALLBACK ALIGN" in md_text
        assert "WHAT-IF FALLBACK MAG" in md_text
        assert "WHAT-IF FALLBACK ALT2" in md_text
        assert "WHAT-IF FALLBACK ALT2 CONF" in md_text
        assert "WHAT-IF FALLBACK PLAN" in md_text
        assert "WHAT-IF PLAN FIT" in md_text
        assert "WHAT-IF PLAN WHY" in md_text
        assert "WHAT-IF SPLIT" in md_text
        assert "WHAT-IF SPLIT LANES" in md_text
        assert "WHAT-IF SPLIT CONF" in md_text
        assert "WHAT-IF SPLIT SAFE" in md_text
        assert "WHAT-IF SPLIT POSTURE" in md_text
        assert "WHAT-IF SPLIT COOLOFF" in md_text
        assert "WHAT-IF SPLIT ESCALATE" in md_text
        assert "WHAT-IF SPLIT ESC CONF" in md_text
        assert "WHAT-IF SPLIT ESC LANES" in md_text
        assert "WHAT-IF SPLIT ESC COOL" in md_text
        assert "WHAT-IF SPLIT ESC STATE" in md_text
        assert "WHAT-IF SPLIT ESC PRESSURE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER ALT" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER ALT CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER PLAN" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER WHY" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER TEMPO" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO WHY" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO COOLOFF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO STATE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO DWELL" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE TICK" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM WHY" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF STATE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM FIT" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WINDOW" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WHY" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE IMPACT" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE DRIFT" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COACH" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COACH CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COACH MODE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COACH WHY" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF FIT" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF WHY" in md_text
        assert "STICKY TOKENS" in md_text
        assert "ANOMALY" in md_text
        assert "ANOMALY CONF" in md_text
        assert "Sticky Tokens" in md_text

        cooloff_zero, signals_zero = sandbox_cooloff_from_prior(
            current_sandbox="OFF",
            prior_json_path=repo / "missing-prior.json",
        )
        assert cooloff_zero == 0, (cooloff_zero, signals_zero)
        assert signals_zero["reason"] == "no-prior-on-cycle", signals_zero

        prior_on = repo / "prior-on.json"
        prior_on.write_text(json.dumps({"routeSandbox": "ON", "sandboxCooloff": 0}), encoding="utf-8")
        cooloff_one, signals_one = sandbox_cooloff_from_prior(
            current_sandbox="OFF",
            prior_json_path=prior_on,
        )
        assert cooloff_one == 1, (cooloff_one, signals_one)
        assert signals_one["reason"] == "sandbox-just-disarmed", signals_one

        pace_drift_zero, pace_drift_zero_signals = pace_drift_from_prior(
            current_pace="STEADY",
            prior_json_path=repo / "missing-pace-prior.json",
        )
        assert pace_drift_zero == 0, (pace_drift_zero, pace_drift_zero_signals)
        assert pace_drift_zero_signals["reason"] == "no-prior-pace", pace_drift_zero_signals

        pace_prior = repo / "prior-pace.json"
        pace_prior.write_text(json.dumps({"actionPace": "BRAKE"}), encoding="utf-8")
        pace_drift_up, pace_drift_up_signals = pace_drift_from_prior(
            current_pace="ACCEL",
            prior_json_path=pace_prior,
        )
        assert pace_drift_up == 2, (pace_drift_up, pace_drift_up_signals)
        assert pace_drift_up_signals["reason"] == "pace-accelerated", pace_drift_up_signals

        route_pulse_streak_reset, route_pulse_streak_reset_signals = route_pulse_link_streak_from_prior(
            current_route_pulse_link="OFF",
            prior_json_path=repo / "missing-route-pulse-prior.json",
        )
        assert route_pulse_streak_reset == 0, (route_pulse_streak_reset, route_pulse_streak_reset_signals)
        assert route_pulse_streak_reset_signals["reason"] == "link-off-reset", route_pulse_streak_reset_signals

        route_pulse_prior = repo / "prior-route-pulse.json"
        route_pulse_prior.write_text(
            json.dumps({"routePulseLink": "SHARP", "routePulseLinkStreak": 2}),
            encoding="utf-8",
        )
        route_pulse_streak_up, route_pulse_streak_up_signals = route_pulse_link_streak_from_prior(
            current_route_pulse_link="SHARP",
            prior_json_path=route_pulse_prior,
        )
        assert route_pulse_streak_up == 3, (route_pulse_streak_up, route_pulse_streak_up_signals)
        assert route_pulse_streak_up_signals["reason"] == "link-persistence-extended", route_pulse_streak_up_signals

        route_pulse_mode_surge, route_pulse_mode_surge_signals = route_pulse_link_mode_from_signals(
            route_pulse_link="SHARP",
            route_pulse_link_streak=3,
            action_pace_alt_window_pulse_drift=1,
        )
        assert route_pulse_mode_surge == "SURGE", (route_pulse_mode_surge, route_pulse_mode_surge_signals)
        assert route_pulse_mode_surge_signals["reason"] == "sharp-link-escalating-or-persistent", route_pulse_mode_surge_signals

        route_pulse_mode_sustain, route_pulse_mode_sustain_signals = route_pulse_link_mode_from_signals(
            route_pulse_link="SOFT",
            route_pulse_link_streak=2,
            action_pace_alt_window_pulse_drift=0,
        )
        assert route_pulse_mode_sustain == "SUSTAIN", (route_pulse_mode_sustain, route_pulse_mode_sustain_signals)
        assert route_pulse_mode_sustain_signals["reason"] == "link-persistence-building", route_pulse_mode_sustain_signals

        route_pulse_mode_drift_zero, route_pulse_mode_drift_zero_signals = route_pulse_link_mode_drift_from_prior(
            current_route_pulse_link_mode="IDLE",
            prior_json_path=repo / "missing-route-pulse-mode-prior.json",
        )
        assert route_pulse_mode_drift_zero == 0, (route_pulse_mode_drift_zero, route_pulse_mode_drift_zero_signals)
        assert route_pulse_mode_drift_zero_signals["reason"] == "no-prior-mode", route_pulse_mode_drift_zero_signals

        route_pulse_mode_prior = repo / "prior-route-pulse-mode.json"
        route_pulse_mode_prior.write_text(json.dumps({"routePulseLinkMode": "SUSTAIN"}), encoding="utf-8")
        route_pulse_mode_drift_up, route_pulse_mode_drift_up_signals = route_pulse_link_mode_drift_from_prior(
            current_route_pulse_link_mode="SURGE",
            prior_json_path=route_pulse_mode_prior,
        )
        assert route_pulse_mode_drift_up == 1, (route_pulse_mode_drift_up, route_pulse_mode_drift_up_signals)
        assert route_pulse_mode_drift_up_signals["reason"] == "mode-intensified", route_pulse_mode_drift_up_signals

        route_pulse_mode_streak_fresh, route_pulse_mode_streak_fresh_signals = route_pulse_link_mode_stability_streak_from_prior(
            current_route_pulse_link_mode="IDLE",
            prior_json_path=repo / "missing-route-pulse-mode-streak-prior.json",
        )
        assert route_pulse_mode_streak_fresh == 1, (route_pulse_mode_streak_fresh, route_pulse_mode_streak_fresh_signals)
        assert route_pulse_mode_streak_fresh_signals["reason"] == "no-prior-mode", route_pulse_mode_streak_fresh_signals

        route_pulse_mode_streak_prior = repo / "prior-route-pulse-mode-streak.json"
        route_pulse_mode_streak_prior.write_text(
            json.dumps({"routePulseLinkMode": "SURGE", "routePulseLinkModeStabilityStreak": 4}),
            encoding="utf-8",
        )
        route_pulse_mode_streak_up, route_pulse_mode_streak_up_signals = route_pulse_link_mode_stability_streak_from_prior(
            current_route_pulse_link_mode="SURGE",
            prior_json_path=route_pulse_mode_streak_prior,
        )
        assert route_pulse_mode_streak_up == 5, (route_pulse_mode_streak_up, route_pulse_mode_streak_up_signals)
        assert route_pulse_mode_streak_up_signals["reason"] == "mode-stable-extended", route_pulse_mode_streak_up_signals

        route_pulse_mode_fit_sync, route_pulse_mode_fit_sync_signals = route_pulse_link_mode_fit_from_signals(
            route_pulse_link_mode="SUSTAIN",
            route_pulse_link_mode_drift=0,
            route_pulse_link_mode_stability_streak=4,
        )
        assert route_pulse_mode_fit_sync == "SYNC", (route_pulse_mode_fit_sync, route_pulse_mode_fit_sync_signals)
        assert route_pulse_mode_fit_sync_signals["reason"] == "mode-stable-multi-window", route_pulse_mode_fit_sync_signals

        route_pulse_mode_fit_break, route_pulse_mode_fit_break_signals = route_pulse_link_mode_fit_from_signals(
            route_pulse_link_mode="SURGE",
            route_pulse_link_mode_drift=1,
            route_pulse_link_mode_stability_streak=1,
        )
        assert route_pulse_mode_fit_break == "BREAK", (route_pulse_mode_fit_break, route_pulse_mode_fit_break_signals)
        assert route_pulse_mode_fit_break_signals["reason"] == "surge-intensifying", route_pulse_mode_fit_break_signals

        route_pulse_mode_fit_drift_zero, route_pulse_mode_fit_drift_zero_signals = route_pulse_link_mode_fit_drift_from_prior(
            current_route_pulse_link_mode_fit="WATCH",
            prior_json_path=repo / "missing-route-pulse-mode-fit-prior.json",
        )
        assert route_pulse_mode_fit_drift_zero == 0, (route_pulse_mode_fit_drift_zero, route_pulse_mode_fit_drift_zero_signals)
        assert route_pulse_mode_fit_drift_zero_signals["reason"] == "no-prior-fit", route_pulse_mode_fit_drift_zero_signals

        route_pulse_mode_fit_prior = repo / "prior-route-pulse-mode-fit.json"
        route_pulse_mode_fit_prior.write_text(json.dumps({"routePulseLinkModeFit": "WATCH"}), encoding="utf-8")
        route_pulse_mode_fit_drift_up, route_pulse_mode_fit_drift_up_signals = route_pulse_link_mode_fit_drift_from_prior(
            current_route_pulse_link_mode_fit="BREAK",
            prior_json_path=route_pulse_mode_fit_prior,
        )
        assert route_pulse_mode_fit_drift_up == 2, (route_pulse_mode_fit_drift_up, route_pulse_mode_fit_drift_up_signals)
        assert route_pulse_mode_fit_drift_up_signals["reason"] == "fit-intensified", route_pulse_mode_fit_drift_up_signals

        pace_conf_high, pace_conf_high_signals = action_pace_window_confidence_from_signals(
            action_pace_window="HOLD",
            action_stability="LOCKED",
            pace_drift=0,
            pace_drift_signals={"priorLoaded": True},
        )
        assert pace_conf_high == "HIGH", (pace_conf_high, pace_conf_high_signals)
        assert pace_conf_high_signals["reason"] == "locked-stability-and-stable-drift", pace_conf_high_signals

        pace_conf_low, pace_conf_low_signals = action_pace_window_confidence_from_signals(
            action_pace_window="OPEN",
            action_stability="WATCH",
            pace_drift=2,
            pace_drift_signals={"priorLoaded": True},
        )
        assert pace_conf_low == "LOW", (pace_conf_low, pace_conf_low_signals)
        assert pace_conf_low_signals["reason"] == "watch-stability-with-drift-swing", pace_conf_low_signals

        alt_window_flag_off, alt_window_flag_off_signals = action_pace_alt_window_from_signals(
            action_pace_window="CLOSE",
            route_sandbox="ON",
            sandbox_target="PRESSURE",
            sandbox_readiness="ARMED",
        )
        assert alt_window_flag_off == "FLAG OFF", (alt_window_flag_off, alt_window_flag_off_signals)
        assert alt_window_flag_off_signals["reason"] == "flag-disabled", alt_window_flag_off_signals

        prior_alt_flag = os.environ.get("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW")
        prior_alt_fit_flag = os.environ.get("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT")
        try:
            os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW"] = "1"
            os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT"] = "1"
            alt_window_probe, alt_window_probe_signals = action_pace_alt_window_from_signals(
                action_pace_window="CLOSE",
                route_sandbox="ON",
                sandbox_target="ALT",
                sandbox_readiness="ARMED",
            )
            assert alt_window_probe == "PROBE ALT", (alt_window_probe, alt_window_probe_signals)
            assert alt_window_probe_signals["reason"] == "closed-primary-with-armed-sandbox-lane", alt_window_probe_signals

            alt_window_wait, alt_window_wait_signals = action_pace_alt_window_from_signals(
                action_pace_window="CLOSE",
                route_sandbox="OFF",
                sandbox_target="ALT",
                sandbox_readiness="IDLE",
            )
            assert alt_window_wait == "WAIT SANDBOX", (alt_window_wait, alt_window_wait_signals)
            assert alt_window_wait_signals["reason"] == "sandbox-not-armed", alt_window_wait_signals

            alt_conf_high, alt_conf_high_signals = action_pace_alt_window_confidence_from_signals(
                action_pace_alt_window=alt_window_probe,
                action_pace_alt_window_signals=alt_window_probe_signals,
                action_pace_window_confidence="MID",
            )
            assert alt_conf_high == "HIGH", (alt_conf_high, alt_conf_high_signals)
            assert alt_conf_high_signals["reason"] == "armed-actionable-sandbox-target", alt_conf_high_signals

            alt_conf_low, alt_conf_low_signals = action_pace_alt_window_confidence_from_signals(
                action_pace_alt_window=alt_window_wait,
                action_pace_alt_window_signals=alt_window_wait_signals,
                action_pace_window_confidence="HIGH",
            )
            assert alt_conf_low == "LOW", (alt_conf_low, alt_conf_low_signals)
            assert alt_conf_low_signals["reason"] == "fallback-not-actionable", alt_conf_low_signals

            alt_conf_drift_zero, alt_conf_drift_zero_signals = alt_step_confidence_drift_from_prior(
                current_alt_step_confidence="MID",
                prior_json_path=repo / "missing-alt-step-conf-prior.json",
            )
            assert alt_conf_drift_zero == 0, (alt_conf_drift_zero, alt_conf_drift_zero_signals)
            assert alt_conf_drift_zero_signals["reason"] == "no-prior-alt-step-confidence", alt_conf_drift_zero_signals

            alt_conf_prior = repo / "prior-alt-step-conf.json"
            alt_conf_prior.write_text(json.dumps({"altStepConfidence": "LOW"}), encoding="utf-8")
            alt_conf_drift_up, alt_conf_drift_up_signals = alt_step_confidence_drift_from_prior(
                current_alt_step_confidence="HIGH",
                prior_json_path=alt_conf_prior,
            )
            assert alt_conf_drift_up == 2, (alt_conf_drift_up, alt_conf_drift_up_signals)
            assert alt_conf_drift_up_signals["reason"] == "alt-step-confidence-increased", alt_conf_drift_up_signals

            alt_fit_safe, alt_fit_safe_signals = action_pace_alt_window_fit_from_signals(
                action_pace_alt_window=alt_window_probe,
                action_pace_alt_window_signals=alt_window_probe_signals,
                pressure_band="MID",
            )
            assert alt_fit_safe == "SAFE", (alt_fit_safe, alt_fit_safe_signals)
            assert alt_fit_safe_signals["reason"] == "armed-fallback-absorbs-mid-pressure", alt_fit_safe_signals

            alt_fit_tense, alt_fit_tense_signals = action_pace_alt_window_fit_from_signals(
                action_pace_alt_window=alt_window_wait,
                action_pace_alt_window_signals=alt_window_wait_signals,
                pressure_band="HIGH",
            )
            assert alt_fit_tense == "TENSE", (alt_fit_tense, alt_fit_tense_signals)
            assert alt_fit_tense_signals["reason"] == "fallback-lane-not-actionable", alt_fit_tense_signals

            prior_alt_why_flag = os.environ.get("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY")
            os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY"] = "1"
            alt_why_probe, alt_why_probe_signals = action_pace_alt_window_why_from_signals(
                action_pace_alt_window=alt_window_probe,
                action_pace_alt_window_confidence=alt_conf_high,
                action_pace_alt_window_fit=alt_fit_safe,
                action_pace_alt_window_signals=alt_window_probe_signals,
            )
            assert alt_why_probe == "PROBE NOW", (alt_why_probe, alt_why_probe_signals)
            assert alt_why_probe_signals["reason"] == "high-confidence-safe-probe", alt_why_probe_signals

            alt_why_wait, alt_why_wait_signals = action_pace_alt_window_why_from_signals(
                action_pace_alt_window=alt_window_wait,
                action_pace_alt_window_confidence=alt_conf_low,
                action_pace_alt_window_fit=alt_fit_tense,
                action_pace_alt_window_signals=alt_window_wait_signals,
            )
            assert alt_why_wait == "ARM SANDBOX", (alt_why_wait, alt_why_wait_signals)
            assert alt_why_wait_signals["reason"] == "sandbox-not-armed", alt_why_wait_signals

            prior_alt_urgency_flag = os.environ.get("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_URGENCY")
            os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_URGENCY"] = "1"
            alt_urgency_now, alt_urgency_now_signals = action_pace_alt_window_urgency_from_signals(
                action_pace_alt_window=alt_window_probe,
                action_pace_alt_window_confidence=alt_conf_high,
                action_pace_alt_window_fit=alt_fit_safe,
                action_pace_alt_window_why=alt_why_probe,
            )
            assert alt_urgency_now == "NOW", (alt_urgency_now, alt_urgency_now_signals)
            assert alt_urgency_now_signals["reason"] == "high-confidence-safe-probe-window", alt_urgency_now_signals

            alt_urgency_later, alt_urgency_later_signals = action_pace_alt_window_urgency_from_signals(
                action_pace_alt_window=alt_window_wait,
                action_pace_alt_window_confidence=alt_conf_low,
                action_pace_alt_window_fit=alt_fit_tense,
                action_pace_alt_window_why=alt_why_wait,
            )
            assert alt_urgency_later == "LATER", (alt_urgency_later, alt_urgency_later_signals)
            assert alt_urgency_later_signals["reason"] == "fallback-not-actionable-yet", alt_urgency_later_signals

            urgency_drift_zero, urgency_drift_zero_signals = action_pace_alt_window_urgency_drift_from_prior(
                current_action_pace_alt_window_urgency="SOON",
                prior_json_path=repo / "missing-urgency-prior.json",
            )
            assert urgency_drift_zero == 0, (urgency_drift_zero, urgency_drift_zero_signals)
            assert urgency_drift_zero_signals["reason"] == "no-prior-urgency-band", urgency_drift_zero_signals

            urgency_prior = repo / "prior-alt-urgency.json"
            urgency_prior.write_text(json.dumps({"actionPaceAltWindowUrgency": "LATER"}), encoding="utf-8")
            urgency_drift_up, urgency_drift_up_signals = action_pace_alt_window_urgency_drift_from_prior(
                current_action_pace_alt_window_urgency="NOW",
                prior_json_path=urgency_prior,
            )
            assert urgency_drift_up == 2, (urgency_drift_up, urgency_drift_up_signals)
            assert urgency_drift_up_signals["reason"] == "urgency-escalated", urgency_drift_up_signals

            prior_alt_step_flag = os.environ.get("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP")
            os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP"] = "1"
            alt_step_probe, alt_step_probe_signals = action_pace_alt_window_step_from_signals(
                action_pace_alt_window=alt_window_probe,
                action_pace_alt_window_confidence=alt_conf_high,
                action_pace_alt_window_fit=alt_fit_safe,
                action_pace_alt_window_urgency=alt_urgency_now,
                action_pace_alt_window_signals=alt_window_probe_signals,
            )
            assert alt_step_probe == "PROBE", (alt_step_probe, alt_step_probe_signals)
            assert alt_step_probe_signals["reason"] == "safe-immediate-probe-window", alt_step_probe_signals

            alt_step_wait, alt_step_wait_signals = action_pace_alt_window_step_from_signals(
                action_pace_alt_window=alt_window_wait,
                action_pace_alt_window_confidence=alt_conf_low,
                action_pace_alt_window_fit=alt_fit_tense,
                action_pace_alt_window_urgency=alt_urgency_later,
                action_pace_alt_window_signals=alt_window_wait_signals,
            )
            assert alt_step_wait == "ARM", (alt_step_wait, alt_step_wait_signals)
            assert alt_step_wait_signals["reason"] == "sandbox-not-armed", alt_step_wait_signals

            step_drift_zero, step_drift_zero_signals = action_pace_alt_window_step_drift_from_prior(
                current_action_pace_alt_window_step="WATCH",
                prior_json_path=repo / "missing-alt-step-prior.json",
            )
            assert step_drift_zero == 0, (step_drift_zero, step_drift_zero_signals)
            assert step_drift_zero_signals["reason"] == "no-prior-step-token", step_drift_zero_signals

            step_prior = repo / "prior-alt-step.json"
            step_prior.write_text(json.dumps({"actionPaceAltWindowStep": "ARM"}), encoding="utf-8")
            step_drift_up, step_drift_up_signals = action_pace_alt_window_step_drift_from_prior(
                current_action_pace_alt_window_step="PROBE",
                prior_json_path=step_prior,
            )
            assert step_drift_up == 6, (step_drift_up, step_drift_up_signals)
            assert step_drift_up_signals["reason"] == "step-escalated", step_drift_up_signals

            prior_alt_step_glyph_flag = os.environ.get("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP_GLYPH")
            os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP_GLYPH"] = "1"
            step_glyph_probe, step_glyph_probe_signals = action_pace_alt_window_step_glyph_from_signals(
                action_pace_alt_window_step=alt_step_probe,
                action_pace_alt_window_urgency=alt_urgency_now,
                action_pace_alt_window_fit=alt_fit_safe,
            )
            assert step_glyph_probe == "✦", (step_glyph_probe, step_glyph_probe_signals)
            assert step_glyph_probe_signals["reason"] == "immediate-safe-action", step_glyph_probe_signals

            step_glyph_wait, step_glyph_wait_signals = action_pace_alt_window_step_glyph_from_signals(
                action_pace_alt_window_step="WAIT",
                action_pace_alt_window_urgency=alt_urgency_later,
                action_pace_alt_window_fit=alt_fit_tense,
            )
            assert step_glyph_wait == "◇", (step_glyph_wait, step_glyph_wait_signals)
            assert step_glyph_wait_signals["reason"] == "hold-pattern-guidance", step_glyph_wait_signals

            if prior_alt_why_flag is None:
                os.environ.pop("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY"] = prior_alt_why_flag
            if prior_alt_urgency_flag is None:
                os.environ.pop("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_URGENCY", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_URGENCY"] = prior_alt_urgency_flag
            if prior_alt_step_flag is None:
                os.environ.pop("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP"] = prior_alt_step_flag
            if prior_alt_step_glyph_flag is None:
                os.environ.pop("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP_GLYPH", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP_GLYPH"] = prior_alt_step_glyph_flag
        finally:
            if prior_alt_flag is None:
                os.environ.pop("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW"] = prior_alt_flag
            if prior_alt_fit_flag is None:
                os.environ.pop("DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT"] = prior_alt_fit_flag

        prior_cooling = repo / "prior-cooloff.json"
        prior_cooling.write_text(json.dumps({"routeSandbox": "OFF", "sandboxCooloff": 2}), encoding="utf-8")
        cooloff_three, signals_three = sandbox_cooloff_from_prior(
            current_sandbox="OFF",
            prior_json_path=prior_cooling,
        )
        assert cooloff_three == 3, (cooloff_three, signals_three)
        assert signals_three["reason"] == "cooloff-continuing", signals_three

        split_cooloff_zero, split_signals_zero = what_if_split_cooloff_from_prior(
            current_split="OFF",
            prior_json_path=repo / "missing-split-prior.json",
        )
        assert split_cooloff_zero == 0, (split_cooloff_zero, split_signals_zero)
        assert split_signals_zero["reason"] == "no-prior-on-cycle", split_signals_zero

        split_prior_on = repo / "split-prior-on.json"
        split_prior_on.write_text(json.dumps({"whatIfSplit": "ON", "whatIfSplitCooloff": 0}), encoding="utf-8")
        split_cooloff_one, split_signals_one = what_if_split_cooloff_from_prior(
            current_split="OFF",
            prior_json_path=split_prior_on,
        )
        assert split_cooloff_one == 1, (split_cooloff_one, split_signals_one)
        assert split_signals_one["reason"] == "split-just-disarmed", split_signals_one

        split_prior_cooling = repo / "split-prior-cooloff.json"
        split_prior_cooling.write_text(json.dumps({"whatIfSplit": "OFF", "whatIfSplitCooloff": 2}), encoding="utf-8")
        split_cooloff_three, split_signals_three = what_if_split_cooloff_from_prior(
            current_split="OFF",
            prior_json_path=split_prior_cooling,
        )
        assert split_cooloff_three == 3, (split_cooloff_three, split_signals_three)
        assert split_signals_three["reason"] == "cooloff-continuing", split_signals_three

        prior_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL")
        try:
            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL"] = "0"
            esc_cool_disabled, esc_signals_disabled = what_if_split_escalate_cooloff_from_prior(
                current_split_escalate="OFF",
                prior_json_path=repo / "missing-esc-prior.json",
            )
            assert esc_cool_disabled == 0, (esc_cool_disabled, esc_signals_disabled)
            assert esc_signals_disabled["reason"] == "flag-disabled", esc_signals_disabled

            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL"] = "1"
            esc_prior_on = repo / "esc-prior-on.json"
            esc_prior_on.write_text(json.dumps({"whatIfSplitEscalate": "ON", "whatIfSplitEscCool": 0}), encoding="utf-8")
            esc_cool_one, esc_signals_one = what_if_split_escalate_cooloff_from_prior(
                current_split_escalate="OFF",
                prior_json_path=esc_prior_on,
            )
            assert esc_cool_one == 1, (esc_cool_one, esc_signals_one)
            assert esc_signals_one["reason"] == "split-escalation-just-disarmed", esc_signals_one

            esc_prior_cooling = repo / "esc-prior-cooloff.json"
            esc_prior_cooling.write_text(json.dumps({"whatIfSplitEscalate": "OFF", "whatIfSplitEscCool": 2}), encoding="utf-8")
            esc_cool_three, esc_signals_three = what_if_split_escalate_cooloff_from_prior(
                current_split_escalate="OFF",
                prior_json_path=esc_prior_cooling,
            )
            assert esc_cool_three == 3, (esc_cool_three, esc_signals_three)
            assert esc_signals_three["reason"] == "split-escalation-cooloff-continuing", esc_signals_three
        finally:
            if prior_env is None:
                os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL"] = prior_env

        plan_primary, plan_primary_signals = what_if_split_escalate_recover_plan_from_signals(
            what_if_split_esc_recover="PORTAL",
            what_if_split_esc_recover_alt="ALT",
        )
        assert plan_primary == "PRIMARY", (plan_primary, plan_primary_signals)
        assert plan_primary_signals["reason"] == "primary-recovery-lane-available", plan_primary_signals

        plan_hold, plan_hold_signals = what_if_split_escalate_recover_plan_from_signals(
            what_if_split_esc_recover="NONE",
            what_if_split_esc_recover_alt="NONE",
        )
        assert plan_hold == "HOLD", (plan_hold, plan_hold_signals)
        assert plan_hold_signals["reason"] == "no-actionable-recovery-lanes", plan_hold_signals

        prior_recover_why_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY")
        try:
            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY"] = "0"
            why_off, why_off_signals = what_if_split_escalate_recover_why_from_signals(
                what_if_split_esc_recover_plan="PRIMARY",
                what_if_split_esc_recover_confidence="HIGH",
                what_if_split_esc_pressure="LOW",
            )
            assert why_off == "FLAG OFF", (why_off, why_off_signals)
            assert why_off_signals["reason"] == "flag-disabled", why_off_signals

            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY"] = "1"
            why_primary_relief, why_primary_relief_signals = what_if_split_escalate_recover_why_from_signals(
                what_if_split_esc_recover_plan="PRIMARY",
                what_if_split_esc_recover_confidence="HIGH",
                what_if_split_esc_pressure="LOW",
            )
            assert why_primary_relief == "PRIMARY RELIEF", (why_primary_relief, why_primary_relief_signals)
            assert why_primary_relief_signals["reason"] == "high-confidence-primary-lane-with-low-pressure", why_primary_relief_signals

            why_hold, why_hold_signals = what_if_split_escalate_recover_why_from_signals(
                what_if_split_esc_recover_plan="HOLD",
                what_if_split_esc_recover_confidence="LOW",
                what_if_split_esc_pressure="MID",
            )
            assert why_hold == "HOLD FOR SIGNAL", (why_hold, why_hold_signals)
            assert why_hold_signals["reason"] == "no-actionable-recovery-lane", why_hold_signals

            tempo_fast, tempo_fast_signals = what_if_split_escalate_recover_tempo_from_signals(
                what_if_split_esc_recover_plan="PRIMARY",
                what_if_split_esc_recover_confidence="HIGH",
                what_if_split_esc_pressure="LOW",
            )
            assert tempo_fast == "FAST", (tempo_fast, tempo_fast_signals)
            assert tempo_fast_signals["reason"] == "high-confidence-low-pressure-recovery", tempo_fast_signals

            tempo_defer, tempo_defer_signals = what_if_split_escalate_recover_tempo_from_signals(
                what_if_split_esc_recover_plan="HOLD",
                what_if_split_esc_recover_confidence="LOW",
                what_if_split_esc_pressure="MID",
            )
            assert tempo_defer == "DEFER", (tempo_defer, tempo_defer_signals)
            assert tempo_defer_signals["reason"] == "no-actionable-recovery-plan", tempo_defer_signals

            prior_veto_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO")
            try:
                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO"] = "0"
                veto_off, veto_off_signals = what_if_split_escalate_recover_veto_from_signals(
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="PRIMARY",
                )
                assert veto_off == "OFF", (veto_off, veto_off_signals)
                assert veto_off_signals["reason"] == "flag-disabled", veto_off_signals

                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO"] = "1"
                veto_on, veto_on_signals = what_if_split_escalate_recover_veto_from_signals(
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="ALT",
                )
                assert veto_on == "ON", (veto_on, veto_on_signals)
                assert veto_on_signals["reason"] == "low-confidence-under-high-pressure-with-actionable-plan", veto_on_signals

                veto_hold, veto_hold_signals = what_if_split_escalate_recover_veto_from_signals(
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="HOLD",
                )
                assert veto_hold == "OFF", (veto_hold, veto_hold_signals)
                assert veto_hold_signals["reason"] == "low-confidence-high-pressure-but-no-actionable-plan", veto_hold_signals

                veto_conf_high, veto_conf_high_signals = what_if_split_escalate_recover_veto_confidence_from_signals(
                    what_if_split_esc_recover_veto="ON",
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="PRIMARY",
                )
                assert veto_conf_high == "HIGH", (veto_conf_high, veto_conf_high_signals)
                assert veto_conf_high_signals["reason"] == "all-veto-guard-signals-aligned", veto_conf_high_signals

                veto_conf_mid, veto_conf_mid_signals = what_if_split_escalate_recover_veto_confidence_from_signals(
                    what_if_split_esc_recover_veto="OFF",
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="HOLD",
                )
                assert veto_conf_mid == "MID", (veto_conf_mid, veto_conf_mid_signals)
                assert veto_conf_mid_signals["reason"] == "pressure-and-confidence-trigger-with-plan-gap", veto_conf_mid_signals

                prior_veto_why_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY")
                try:
                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY"] = "0"
                    veto_why_off, veto_why_off_signals = what_if_split_escalate_recover_veto_why_from_signals(
                        what_if_split_esc_recover_veto="ON",
                        what_if_split_esc_recover_veto_confidence="HIGH",
                        what_if_split_esc_pressure="HIGH",
                        what_if_split_esc_recover_plan="PRIMARY",
                    )
                    assert veto_why_off == "FLAG OFF", (veto_why_off, veto_why_off_signals)
                    assert veto_why_off_signals["reason"] == "flag-disabled", veto_why_off_signals

                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY"] = "1"
                    veto_why_on, veto_why_on_signals = what_if_split_escalate_recover_veto_why_from_signals(
                        what_if_split_esc_recover_veto="ON",
                        what_if_split_esc_recover_veto_confidence="HIGH",
                        what_if_split_esc_pressure="HIGH",
                        what_if_split_esc_recover_plan="ALT",
                    )
                    assert veto_why_on == "HIGH PRESSURE LOCK", (veto_why_on, veto_why_on_signals)
                    assert veto_why_on_signals["reason"] == "veto-armed-under-high-pressure-actionable-plan", veto_why_on_signals
                finally:
                    if prior_veto_why_env is None:
                        os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY", None)
                    else:
                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY"] = prior_veto_why_env

                prior_veto_cooloff_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF")
                try:
                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF"] = "1"
                    veto_cooloff_prior = repo / "veto-cooloff-prior.json"
                    veto_cooloff_prior.write_text(json.dumps({"whatIfSplitEscRecoverVeto": "ON", "whatIfSplitEscRecoverVetoCooloff": 0}), encoding="utf-8")
                    veto_cooloff_one, veto_cooloff_one_signals = what_if_split_escalate_recover_veto_cooloff_from_prior(
                        current_split_esc_recover_veto="OFF",
                        prior_json_path=veto_cooloff_prior,
                    )
                    assert veto_cooloff_one == 1, (veto_cooloff_one, veto_cooloff_one_signals)
                    assert veto_cooloff_one_signals["reason"] == "veto-just-disarmed", veto_cooloff_one_signals

                    veto_cooloff_prior.write_text(json.dumps({"whatIfSplitEscRecoverVeto": "OFF", "whatIfSplitEscRecoverVetoCooloff": 2}), encoding="utf-8")
                    veto_cooloff_roll, veto_cooloff_roll_signals = what_if_split_escalate_recover_veto_cooloff_from_prior(
                        current_split_esc_recover_veto="OFF",
                        prior_json_path=veto_cooloff_prior,
                    )
                    assert veto_cooloff_roll == 3, (veto_cooloff_roll, veto_cooloff_roll_signals)
                    assert veto_cooloff_roll_signals["reason"] == "veto-remains-disarmed-in-cooloff-window", veto_cooloff_roll_signals

                    veto_state_armed, veto_state_armed_signals = what_if_split_escalate_recover_veto_state_from_signals(
                        what_if_split_esc_recover_veto="ON",
                        what_if_split_esc_recover_veto_cooloff=0,
                    )
                    assert veto_state_armed == "ARMED", (veto_state_armed, veto_state_armed_signals)

                    veto_state_cooling, veto_state_cooling_signals = what_if_split_escalate_recover_veto_state_from_signals(
                        what_if_split_esc_recover_veto="OFF",
                        what_if_split_esc_recover_veto_cooloff=2,
                    )
                    assert veto_state_cooling == "COOLING", (veto_state_cooling, veto_state_cooling_signals)
                    assert veto_state_cooling_signals["reason"] == "veto-disarmed-in-cooloff-window", veto_state_cooling_signals

                    veto_dwell_prior = repo / "veto-dwell-prior.json"
                    veto_dwell_prior.write_text(
                        json.dumps({"whatIfSplitEscRecoverVetoState": "ARMED", "whatIfSplitEscRecoverVetoDwell": 2}),
                        encoding="utf-8",
                    )
                    veto_dwell_roll, veto_dwell_roll_signals = what_if_split_escalate_recover_veto_dwell_from_prior(
                        current_split_esc_recover_veto_state="ARMED",
                        prior_json_path=veto_dwell_prior,
                    )
                    assert veto_dwell_roll == 3, (veto_dwell_roll, veto_dwell_roll_signals)
                    assert veto_dwell_roll_signals["reason"] == "veto-remains-armed", veto_dwell_roll_signals

                    veto_dwell_new, veto_dwell_new_signals = what_if_split_escalate_recover_veto_dwell_from_prior(
                        current_split_esc_recover_veto_state="ARMED",
                        prior_json_path=repo / "missing-veto-dwell-prior.json",
                    )
                    assert veto_dwell_new == 1, (veto_dwell_new, veto_dwell_new_signals)
                    assert veto_dwell_new_signals["priorLoaded"] is False, veto_dwell_new_signals
                    assert veto_dwell_new_signals["reason"] == "veto-armed-new-streak", veto_dwell_new_signals

                    veto_dwell_reset, veto_dwell_reset_signals = what_if_split_escalate_recover_veto_dwell_from_prior(
                        current_split_esc_recover_veto_state="COOLING",
                        prior_json_path=veto_dwell_prior,
                    )
                    assert veto_dwell_reset == 0, (veto_dwell_reset, veto_dwell_reset_signals)
                    assert veto_dwell_reset_signals["reason"] == "veto-not-armed", veto_dwell_reset_signals

                    prior_veto_release_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE")
                    try:
                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE"] = "0"
                        veto_release_flag_off, veto_release_flag_off_signals = what_if_split_escalate_recover_veto_release_from_prior(
                            current_split_esc_recover_veto_state="IDLE",
                            prior_json_path=veto_dwell_prior,
                        )
                        assert veto_release_flag_off == "FLAG OFF", (veto_release_flag_off, veto_release_flag_off_signals)
                        assert veto_release_flag_off_signals["reason"] == "flag-disabled", veto_release_flag_off_signals

                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE"] = "1"
                        veto_release_prior = repo / "veto-release-prior.json"
                        veto_release_prior.write_text(
                            json.dumps({"whatIfSplitEscRecoverVetoState": "COOLING"}),
                            encoding="utf-8",
                        )
                        veto_release_clear, veto_release_clear_signals = what_if_split_escalate_recover_veto_release_from_prior(
                            current_split_esc_recover_veto_state="IDLE",
                            prior_json_path=veto_release_prior,
                        )
                        assert veto_release_clear == "COOLING CLEAR", (veto_release_clear, veto_release_clear_signals)
                        assert veto_release_clear_signals["reason"] == "veto-state-transitioned-cooling-to-idle", veto_release_clear_signals

                        veto_release_cooling, veto_release_cooling_signals = what_if_split_escalate_recover_veto_release_from_prior(
                            current_split_esc_recover_veto_state="COOLING",
                            prior_json_path=veto_release_prior,
                        )
                        assert veto_release_cooling == "COOLING", (veto_release_cooling, veto_release_cooling_signals)
                        assert veto_release_cooling_signals["reason"] == "veto-state-still-cooling", veto_release_cooling_signals

                        veto_release_conf_high, veto_release_conf_high_signals = what_if_split_escalate_recover_veto_release_confidence_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING CLEAR",
                            what_if_split_esc_recover_veto_state="IDLE",
                            what_if_split_esc_recover_veto_dwell=0,
                        )
                        assert veto_release_conf_high == "HIGH", (veto_release_conf_high, veto_release_conf_high_signals)
                        assert veto_release_conf_high_signals["reason"] == "clean-cooling-to-idle-release-transition", veto_release_conf_high_signals

                        veto_release_conf_mid, veto_release_conf_mid_signals = what_if_split_escalate_recover_veto_release_confidence_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING",
                            what_if_split_esc_recover_veto_state="COOLING",
                            what_if_split_esc_recover_veto_dwell=0,
                        )
                        assert veto_release_conf_mid == "MID", (veto_release_conf_mid, veto_release_conf_mid_signals)
                        assert veto_release_conf_mid_signals["reason"] == "release-pending-while-cooling", veto_release_conf_mid_signals

                        veto_release_route_primary, veto_release_route_primary_signals = what_if_split_escalate_recover_veto_release_route_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING CLEAR",
                            what_if_split_esc_recover_veto_state="IDLE",
                            what_if_split_esc_recover="PORTAL",
                            what_if_split_esc_recover_alt="ALT",
                            what_if_split_esc_recover_plan="PRIMARY",
                        )
                        assert veto_release_route_primary == "PORTAL", (veto_release_route_primary, veto_release_route_primary_signals)
                        assert veto_release_route_primary_signals["reason"] == "release-cleared-follow-primary-recovery-lane", veto_release_route_primary_signals

                        veto_release_route_hold, veto_release_route_hold_signals = what_if_split_escalate_recover_veto_release_route_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING",
                            what_if_split_esc_recover_veto_state="COOLING",
                            what_if_split_esc_recover="PORTAL",
                            what_if_split_esc_recover_alt="ALT",
                            what_if_split_esc_recover_plan="PRIMARY",
                        )
                        assert veto_release_route_hold == "HOLD", (veto_release_route_hold, veto_release_route_hold_signals)
                        assert veto_release_route_hold_signals["reason"] == "release-route-held-while-cooling", veto_release_route_hold_signals

                        prior_veto_release_tick_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK")
                        try:
                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK"] = "0"
                            veto_release_tick_flag_off, veto_release_tick_flag_off_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="COOLING CLEAR",
                                current_split_esc_recover_veto_state="IDLE",
                                prior_json_path=veto_release_prior,
                            )
                            assert veto_release_tick_flag_off == "FLAG OFF", (veto_release_tick_flag_off, veto_release_tick_flag_off_signals)
                            assert veto_release_tick_flag_off_signals["reason"] == "flag-disabled", veto_release_tick_flag_off_signals

                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK"] = "1"
                            veto_release_tick_start, veto_release_tick_start_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="COOLING CLEAR",
                                current_split_esc_recover_veto_state="IDLE",
                                prior_json_path=veto_release_prior,
                            )
                            assert veto_release_tick_start == 1, (veto_release_tick_start, veto_release_tick_start_signals)
                            assert veto_release_tick_start_signals["reason"] == "release-cleared-idle-window-started", veto_release_tick_start_signals

                            veto_release_tick_prior = repo / "veto-release-tick-prior.json"
                            veto_release_tick_prior.write_text(
                                json.dumps(
                                    {
                                        "whatIfSplitEscRecoverVetoReleaseTick": 2,
                                        "whatIfSplitEscRecoverVetoRelease": "STABLE",
                                        "whatIfSplitEscRecoverVetoState": "IDLE",
                                    }
                                ),
                                encoding="utf-8",
                            )
                            veto_release_tick_continue, veto_release_tick_continue_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="STABLE",
                                current_split_esc_recover_veto_state="IDLE",
                                prior_json_path=veto_release_tick_prior,
                            )
                            assert veto_release_tick_continue == 3, (veto_release_tick_continue, veto_release_tick_continue_signals)
                            assert veto_release_tick_continue_signals["reason"] == "release-idle-window-continuing", veto_release_tick_continue_signals

                            veto_release_tick_reset, veto_release_tick_reset_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="HOLD",
                                current_split_esc_recover_veto_state="ARMED",
                                prior_json_path=veto_release_tick_prior,
                            )
                            assert veto_release_tick_reset == 0, (veto_release_tick_reset, veto_release_tick_reset_signals)
                            assert veto_release_tick_reset_signals["reason"] == "no-active-release-idle-window", veto_release_tick_reset_signals

                            veto_release_phase_idle, veto_release_phase_idle_signals = what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
                                what_if_split_esc_recover_veto_release_tick=0,
                            )
                            assert veto_release_phase_idle == "IDLE", (veto_release_phase_idle, veto_release_phase_idle_signals)
                            assert veto_release_phase_idle_signals["reason"] == "no-active-release-tick-window", veto_release_phase_idle_signals

                            veto_release_phase_mid, veto_release_phase_mid_signals = what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
                                what_if_split_esc_recover_veto_release_tick=3,
                            )
                            assert veto_release_phase_mid == "MID", (veto_release_phase_mid, veto_release_phase_mid_signals)
                            assert veto_release_phase_mid_signals["reason"] == "release-window-mid-pacing", veto_release_phase_mid_signals

                            veto_release_phase_flag_off, veto_release_phase_flag_off_signals = what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
                                what_if_split_esc_recover_veto_release_tick="FLAG OFF",
                            )
                            assert veto_release_phase_flag_off == "FLAG OFF", (veto_release_phase_flag_off, veto_release_phase_flag_off_signals)
                            assert veto_release_phase_flag_off_signals["reason"] == "non-numeric-tick-token-forwarded", veto_release_phase_flag_off_signals

                            veto_release_cadence_accel, veto_release_cadence_accel_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick=4,
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 1},
                            )
                            assert veto_release_cadence_accel == "ACCEL", (veto_release_cadence_accel, veto_release_cadence_accel_signals)
                            assert veto_release_cadence_accel_signals["reason"] == "tick-growth-jump-vs-prior-window", veto_release_cadence_accel_signals

                            veto_release_cadence_steady, veto_release_cadence_steady_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick=3,
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 2},
                            )
                            assert veto_release_cadence_steady == "STEADY", (veto_release_cadence_steady, veto_release_cadence_steady_signals)
                            assert veto_release_cadence_steady_signals["reason"] == "tick-growth-linear-vs-prior-window", veto_release_cadence_steady_signals

                            veto_release_cadence_decay, veto_release_cadence_decay_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick=2,
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 3},
                            )
                            assert veto_release_cadence_decay == "DECAY", (veto_release_cadence_decay, veto_release_cadence_decay_signals)
                            assert veto_release_cadence_decay_signals["reason"] == "tick-stalled-or-regressed-vs-prior-window", veto_release_cadence_decay_signals

                            veto_release_cadence_flag_off, veto_release_cadence_flag_off_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick="FLAG OFF",
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 7},
                            )
                            assert veto_release_cadence_flag_off == "FLAG OFF", (veto_release_cadence_flag_off, veto_release_cadence_flag_off_signals)
                            assert veto_release_cadence_flag_off_signals["reason"] == "non-numeric-tick-token-forwarded", veto_release_cadence_flag_off_signals

                            prior_veto_rearm_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM")
                            try:
                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM"] = "0"
                                veto_rearm_off, veto_rearm_off_signals = what_if_split_escalate_recover_veto_rearm_from_signals(
                                    what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    what_if_split_esc_pressure="HIGH",
                                    what_if_split_esc_recover_veto_release_cadence="STEADY",
                                )
                                assert veto_rearm_off == "OFF", (veto_rearm_off, veto_rearm_off_signals)
                                assert veto_rearm_off_signals["reason"] == "flag-disabled", veto_rearm_off_signals

                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM"] = "1"
                                veto_rearm_watch, veto_rearm_watch_signals = what_if_split_escalate_recover_veto_rearm_from_signals(
                                    what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    what_if_split_esc_pressure="HIGH",
                                    what_if_split_esc_recover_veto_release_cadence="STEADY",
                                )
                                assert veto_rearm_watch == "WATCH", (veto_rearm_watch, veto_rearm_watch_signals)
                                assert veto_rearm_watch_signals["reason"] == "late-release-window-under-high-pressure", veto_rearm_watch_signals

                                veto_rearm_decay, veto_rearm_decay_signals = what_if_split_escalate_recover_veto_rearm_from_signals(
                                    what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    what_if_split_esc_pressure="HIGH",
                                    what_if_split_esc_recover_veto_release_cadence="DECAY",
                                )
                                assert veto_rearm_decay == "OFF", (veto_rearm_decay, veto_rearm_decay_signals)
                                assert veto_rearm_decay_signals["reason"] == "release-cadence-not-rearm-prone", veto_rearm_decay_signals

                                veto_rearm_conf_high, veto_rearm_conf_high_signals = what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
                                    what_if_split_esc_recover_veto_rearm=veto_rearm_watch,
                                    what_if_split_esc_recover_veto_rearm_signals=veto_rearm_watch_signals,
                                )
                                assert veto_rearm_conf_high == "HIGH", (veto_rearm_conf_high, veto_rearm_conf_high_signals)
                                assert veto_rearm_conf_high_signals["reason"] == "watch-cue-aligned-with-late-high-pressure-steady-cadence", veto_rearm_conf_high_signals

                                veto_rearm_conf_mid, veto_rearm_conf_mid_signals = what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
                                    what_if_split_esc_recover_veto_rearm=veto_rearm_decay,
                                    what_if_split_esc_recover_veto_rearm_signals=veto_rearm_decay_signals,
                                )
                                assert veto_rearm_conf_mid == "MID", (veto_rearm_conf_mid, veto_rearm_conf_mid_signals)
                                assert veto_rearm_conf_mid_signals["reason"] == "watch-cue-suppressed-by-cadence-guard", veto_rearm_conf_mid_signals

                                veto_rearm_conf_low, veto_rearm_conf_low_signals = what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
                                    what_if_split_esc_recover_veto_rearm=veto_rearm_off,
                                    what_if_split_esc_recover_veto_rearm_signals=veto_rearm_off_signals,
                                )
                                assert veto_rearm_conf_low == "LOW", (veto_rearm_conf_low, veto_rearm_conf_low_signals)
                                assert veto_rearm_conf_low_signals["reason"] == "flag-disabled", veto_rearm_conf_low_signals

                                prior_veto_rearm_why_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_WHY")
                                try:
                                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_WHY"] = "0"
                                    veto_rearm_why_off, veto_rearm_why_off_signals = what_if_split_escalate_recover_veto_rearm_why_from_signals(
                                        what_if_split_esc_recover_veto_rearm=veto_rearm_watch,
                                        what_if_split_esc_recover_veto_rearm_confidence=veto_rearm_conf_high,
                                        what_if_split_esc_pressure="HIGH",
                                        what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    )
                                    assert veto_rearm_why_off == "FLAG OFF", (veto_rearm_why_off, veto_rearm_why_off_signals)
                                    assert veto_rearm_why_off_signals["reason"] == "flag-disabled", veto_rearm_why_off_signals

                                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_WHY"] = "1"
                                    veto_rearm_why_on, veto_rearm_why_on_signals = what_if_split_escalate_recover_veto_rearm_why_from_signals(
                                        what_if_split_esc_recover_veto_rearm=veto_rearm_watch,
                                        what_if_split_esc_recover_veto_rearm_confidence=veto_rearm_conf_high,
                                        what_if_split_esc_pressure="HIGH",
                                        what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    )
                                    assert veto_rearm_why_on == "HIGH PRESSURE REARM", (veto_rearm_why_on, veto_rearm_why_on_signals)
                                    assert veto_rearm_why_on_signals["reason"] == "watch-cue-confirmed-under-high-pressure", veto_rearm_why_on_signals

                                    veto_rearm_why_nowatch, veto_rearm_why_nowatch_signals = what_if_split_escalate_recover_veto_rearm_why_from_signals(
                                        what_if_split_esc_recover_veto_rearm=veto_rearm_decay,
                                        what_if_split_esc_recover_veto_rearm_confidence=veto_rearm_conf_mid,
                                        what_if_split_esc_pressure="HIGH",
                                        what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    )
                                    assert veto_rearm_why_nowatch == "NO WATCH CUE", (veto_rearm_why_nowatch, veto_rearm_why_nowatch_signals)
                                    assert veto_rearm_why_nowatch_signals["reason"] == "rearm-watch-not-active", veto_rearm_why_nowatch_signals
                                finally:
                                    if prior_veto_rearm_why_env is None:
                                        os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_WHY", None)
                                    else:
                                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_WHY"] = prior_veto_rearm_why_env

                                prior_veto_rearm_cooloff_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF")
                                try:
                                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF"] = "0"
                                    rearm_cooloff_off, rearm_cooloff_off_signals = what_if_split_escalate_recover_veto_rearm_cooloff_from_prior(
                                        current_split_esc_recover_veto_rearm="OFF",
                                        prior_json_path=repo / "missing-rearm-cooloff-prior.json",
                                    )
                                    assert rearm_cooloff_off == 0, (rearm_cooloff_off, rearm_cooloff_off_signals)
                                    assert rearm_cooloff_off_signals["reason"] == "flag-disabled", rearm_cooloff_off_signals

                                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF"] = "1"
                                    rearm_cooloff_prior = repo / "rearm-cooloff-prior.json"
                                    rearm_cooloff_prior.write_text(
                                        json.dumps({"whatIfSplitEscRecoverVetoRearm": "WATCH", "whatIfSplitEscRecoverVetoRearmCooloff": 0}),
                                        encoding="utf-8",
                                    )
                                    rearm_cooloff_one, rearm_cooloff_one_signals = what_if_split_escalate_recover_veto_rearm_cooloff_from_prior(
                                        current_split_esc_recover_veto_rearm="OFF",
                                        prior_json_path=rearm_cooloff_prior,
                                    )
                                    assert rearm_cooloff_one == 1, (rearm_cooloff_one, rearm_cooloff_one_signals)
                                    assert rearm_cooloff_one_signals["reason"] == "rearm-watch-just-disarmed", rearm_cooloff_one_signals

                                    rearm_cooloff_prior.write_text(
                                        json.dumps({"whatIfSplitEscRecoverVetoRearm": "OFF", "whatIfSplitEscRecoverVetoRearmCooloff": 2}),
                                        encoding="utf-8",
                                    )
                                    rearm_cooloff_roll, rearm_cooloff_roll_signals = what_if_split_escalate_recover_veto_rearm_cooloff_from_prior(
                                        current_split_esc_recover_veto_rearm="OFF",
                                        prior_json_path=rearm_cooloff_prior,
                                    )
                                    assert rearm_cooloff_roll == 3, (rearm_cooloff_roll, rearm_cooloff_roll_signals)
                                    assert rearm_cooloff_roll_signals["reason"] == "rearm-watch-remains-disarmed-in-cooloff-window", rearm_cooloff_roll_signals
                                    rearm_cooloff_state_active, rearm_cooloff_state_active_signals = what_if_split_escalate_recover_veto_rearm_cooloff_state_from_signals(
                                        what_if_split_esc_recover_veto_rearm="OFF",
                                        what_if_split_esc_recover_veto_rearm_cooloff=rearm_cooloff_roll,
                                    )
                                    assert rearm_cooloff_state_active == "ACTIVE", (rearm_cooloff_state_active, rearm_cooloff_state_active_signals)
                                    assert rearm_cooloff_state_active_signals["reason"] == "watch-armed-or-cooloff-running", rearm_cooloff_state_active_signals

                                    rearm_cooloff_state_idle, rearm_cooloff_state_idle_signals = what_if_split_escalate_recover_veto_rearm_cooloff_state_from_signals(
                                        what_if_split_esc_recover_veto_rearm="OFF",
                                        what_if_split_esc_recover_veto_rearm_cooloff=0,
                                    )
                                    assert rearm_cooloff_state_idle == "IDLE", (rearm_cooloff_state_idle, rearm_cooloff_state_idle_signals)
                                    assert rearm_cooloff_state_idle_signals["reason"] == "no-watch-and-no-cooloff", rearm_cooloff_state_idle_signals
                                    rearm_fit_relief, rearm_fit_relief_signals = what_if_split_escalate_recover_veto_rearm_fit_from_signals(
                                        what_if_split_esc_recover_veto_rearm_cooloff_state="ACTIVE",
                                        what_if_split_esc_recover_veto_rearm_cooloff=2,
                                        what_if_split_esc_pressure="LOW",
                                    )
                                    assert rearm_fit_relief == "RELIEF", (rearm_fit_relief, rearm_fit_relief_signals)
                                    assert rearm_fit_relief_signals["reason"] == "active-cooloff-with-low-pressure", rearm_fit_relief_signals

                                    rearm_fit_even, rearm_fit_even_signals = what_if_split_escalate_recover_veto_rearm_fit_from_signals(
                                        what_if_split_esc_recover_veto_rearm_cooloff_state="ACTIVE",
                                        what_if_split_esc_recover_veto_rearm_cooloff=1,
                                        what_if_split_esc_pressure="MID",
                                    )
                                    assert rearm_fit_even == "EVEN", (rearm_fit_even, rearm_fit_even_signals)
                                    assert rearm_fit_even_signals["reason"] == "active-cooloff-with-mid-pressure", rearm_fit_even_signals

                                    rearm_fit_tense, rearm_fit_tense_signals = what_if_split_escalate_recover_veto_rearm_fit_from_signals(
                                        what_if_split_esc_recover_veto_rearm_cooloff_state="IDLE",
                                        what_if_split_esc_recover_veto_rearm_cooloff=0,
                                        what_if_split_esc_pressure="HIGH",
                                    )
                                    assert rearm_fit_tense == "TENSE", (rearm_fit_tense, rearm_fit_tense_signals)
                                    assert rearm_fit_tense_signals["reason"] == "pressure-high-without-relief-window", rearm_fit_tense_signals

                                    prior_veto_rearm_nudge_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE")
                                    try:
                                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE"] = "0"
                                        nudge_off, nudge_off_signals = what_if_split_escalate_recover_veto_rearm_nudge_from_signals(
                                            what_if_split_esc_recover_veto_rearm="WATCH",
                                            what_if_split_esc_recover_veto_rearm_confidence="HIGH",
                                            what_if_split_esc_recover_veto_rearm_fit="TENSE",
                                            what_if_split_esc_recover_veto_rearm_cooloff_state="ACTIVE",
                                        )
                                        assert nudge_off == "FLAG OFF", (nudge_off, nudge_off_signals)
                                        assert nudge_off_signals["reason"] == "flag-disabled", nudge_off_signals

                                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE"] = "1"
                                        nudge_hold, nudge_hold_signals = what_if_split_escalate_recover_veto_rearm_nudge_from_signals(
                                            what_if_split_esc_recover_veto_rearm="WATCH",
                                            what_if_split_esc_recover_veto_rearm_confidence="HIGH",
                                            what_if_split_esc_recover_veto_rearm_fit="TENSE",
                                            what_if_split_esc_recover_veto_rearm_cooloff_state="ACTIVE",
                                        )
                                        assert nudge_hold == "HOLD DEFENSE", (nudge_hold, nudge_hold_signals)
                                        assert nudge_hold_signals["reason"] == "watch-armed-high-confidence-tense-fit", nudge_hold_signals

                                        nudge_relief, nudge_relief_signals = what_if_split_escalate_recover_veto_rearm_nudge_from_signals(
                                            what_if_split_esc_recover_veto_rearm="OFF",
                                            what_if_split_esc_recover_veto_rearm_confidence="LOW",
                                            what_if_split_esc_recover_veto_rearm_fit="RELIEF",
                                            what_if_split_esc_recover_veto_rearm_cooloff_state="ACTIVE",
                                        )
                                        assert nudge_relief == "RESET READY", (nudge_relief, nudge_relief_signals)
                                        assert nudge_relief_signals["reason"] == "cooloff-active-with-relief-fit", nudge_relief_signals

                                        nudge_window_armed, nudge_window_armed_signals = what_if_split_escalate_recover_veto_rearm_nudge_window_from_signals(
                                            what_if_split_esc_recover_veto_rearm="WATCH",
                                            what_if_split_esc_recover_veto_rearm_cooloff_state="ACTIVE",
                                        )
                                        assert nudge_window_armed == "ARMED", (nudge_window_armed, nudge_window_armed_signals)
                                        assert nudge_window_armed_signals["reason"] == "watch-cue-active", nudge_window_armed_signals

                                        nudge_window_cooling, nudge_window_cooling_signals = what_if_split_escalate_recover_veto_rearm_nudge_window_from_signals(
                                            what_if_split_esc_recover_veto_rearm="OFF",
                                            what_if_split_esc_recover_veto_rearm_cooloff_state="ACTIVE",
                                        )
                                        assert nudge_window_cooling == "COOLING", (nudge_window_cooling, nudge_window_cooling_signals)
                                        assert nudge_window_cooling_signals["reason"] == "watch-disarmed-in-cooloff-window", nudge_window_cooling_signals

                                        nudge_window_idle, nudge_window_idle_signals = what_if_split_escalate_recover_veto_rearm_nudge_window_from_signals(
                                            what_if_split_esc_recover_veto_rearm="OFF",
                                            what_if_split_esc_recover_veto_rearm_cooloff_state="IDLE",
                                        )
                                        assert nudge_window_idle == "IDLE", (nudge_window_idle, nudge_window_idle_signals)
                                        assert nudge_window_idle_signals["reason"] == "no-watch-or-cooloff-window", nudge_window_idle_signals

                                        nudge_conf_high, nudge_conf_high_signals = what_if_split_escalate_recover_veto_rearm_nudge_confidence_from_signals(
                                            what_if_split_esc_recover_veto_rearm_nudge="HOLD DEFENSE",
                                            what_if_split_esc_recover_veto_rearm_confidence="HIGH",
                                            what_if_split_esc_recover_veto_rearm_fit="TENSE",
                                        )
                                        assert nudge_conf_high == "HIGH", (nudge_conf_high, nudge_conf_high_signals)
                                        assert nudge_conf_high_signals["reason"] == "high-urgency-nudge-backed-by-high-rearm-confidence", nudge_conf_high_signals

                                        nudge_conf_mid, nudge_conf_mid_signals = what_if_split_escalate_recover_veto_rearm_nudge_confidence_from_signals(
                                            what_if_split_esc_recover_veto_rearm_nudge="PROBE CAREFUL",
                                            what_if_split_esc_recover_veto_rearm_confidence="MID",
                                            what_if_split_esc_recover_veto_rearm_fit="EVEN",
                                        )
                                        assert nudge_conf_mid == "MID", (nudge_conf_mid, nudge_conf_mid_signals)
                                        assert nudge_conf_mid_signals["reason"] == "actionable-nudge-with-mid-confidence-context", nudge_conf_mid_signals

                                        drift_stable, drift_stable_signals = what_if_split_escalate_recover_veto_rearm_nudge_drift_from_prior(
                                            current_nudge_why="WATCH REARM",
                                            prior_json_path=repo / "missing-nudge-drift-prior.json",
                                        )
                                        assert drift_stable == "STABLE", (drift_stable, drift_stable_signals)
                                        assert drift_stable_signals["reason"] == "nudge-rationale-unchanged-vs-prior-window", drift_stable_signals

                                        prior_nudge_drift = repo / "prior-nudge-drift.json"
                                        prior_nudge_drift.write_text(
                                            json.dumps({"whatIfSplitEscRecoverVetoRearmNudgeWhy": "LANE MONITOR"}),
                                            encoding="utf-8",
                                        )
                                        drift_shifting, drift_shifting_signals = what_if_split_escalate_recover_veto_rearm_nudge_drift_from_prior(
                                            current_nudge_why="WATCH REARM",
                                            prior_json_path=prior_nudge_drift,
                                        )
                                        assert drift_shifting == "SHIFTING", (drift_shifting, drift_shifting_signals)
                                        assert drift_shifting_signals["reason"] == "nudge-rationale-changed-vs-prior-window", drift_shifting_signals


                                        coach_mode_balanced, coach_mode_balanced_signals = what_if_split_escalate_recover_veto_rearm_coach_mode_from_signals(
                                            what_if_split_esc_recover_veto_rearm_coach="PORTAL|ALT",
                                        )
                                        assert coach_mode_balanced == "BALANCED", (coach_mode_balanced, coach_mode_balanced_signals)
                                        assert coach_mode_balanced_signals["reason"] == "coach-includes-distinct-primary-and-backup-lanes", coach_mode_balanced_signals

                                        coach_mode_primary, coach_mode_primary_signals = what_if_split_escalate_recover_veto_rearm_coach_mode_from_signals(
                                            what_if_split_esc_recover_veto_rearm_coach="PORTAL|NONE",
                                        )
                                        assert coach_mode_primary == "PRIMARY", (coach_mode_primary, coach_mode_primary_signals)
                                        assert coach_mode_primary_signals["reason"] == "coach-primary-lane-drives-guidance", coach_mode_primary_signals

                                        coach_mode_backup, coach_mode_backup_signals = what_if_split_escalate_recover_veto_rearm_coach_mode_from_signals(
                                            what_if_split_esc_recover_veto_rearm_coach="NONE|ALT",
                                        )
                                        assert coach_mode_backup == "BACKUP", (coach_mode_backup, coach_mode_backup_signals)
                                        assert coach_mode_backup_signals["reason"] == "coach-primary-missing-but-backup-actionable", coach_mode_backup_signals

                                        prior_coach_why_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_WHY")
                                        try:
                                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_WHY"] = "0"
                                            coach_why_off, coach_why_off_signals = what_if_split_escalate_recover_veto_rearm_coach_why_from_signals(
                                                what_if_split_esc_recover_veto_rearm_coach="PORTAL|ALT",
                                                what_if_split_esc_recover_veto_rearm_coach_mode="BALANCED",
                                                what_if_split_esc_recover_veto_rearm_coach_confidence="HIGH",
                                            )
                                            assert coach_why_off == "FLAG OFF", (coach_why_off, coach_why_off_signals)
                                            assert coach_why_off_signals["reason"] == "flag-disabled", coach_why_off_signals

                                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_WHY"] = "1"
                                            coach_why_dual, coach_why_dual_signals = what_if_split_escalate_recover_veto_rearm_coach_why_from_signals(
                                                what_if_split_esc_recover_veto_rearm_coach="PORTAL|ALT",
                                                what_if_split_esc_recover_veto_rearm_coach_mode="BALANCED",
                                                what_if_split_esc_recover_veto_rearm_coach_confidence="HIGH",
                                            )
                                            assert coach_why_dual == "DUAL COVER", (coach_why_dual, coach_why_dual_signals)
                                            assert coach_why_dual_signals["reason"] == "balanced-coach-with-high-confidence", coach_why_dual_signals

                                            coach_why_backup, coach_why_backup_signals = what_if_split_escalate_recover_veto_rearm_coach_why_from_signals(
                                                what_if_split_esc_recover_veto_rearm_coach="NONE|ALT",
                                                what_if_split_esc_recover_veto_rearm_coach_mode="BACKUP",
                                                what_if_split_esc_recover_veto_rearm_coach_confidence="MID",
                                            )
                                            assert coach_why_backup == "NO ACTION", (coach_why_backup, coach_why_backup_signals)
                                            assert coach_why_backup_signals["reason"] == "coach-primary-not-actionable", coach_why_backup_signals


                                            coach_handoff_locked, coach_handoff_locked_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_from_signals(
                                                what_if_split_esc_recover_veto_rearm_coach="PORTAL|NONE",
                                                what_if_split_esc_recover_veto_rearm_coach_mode="PRIMARY",
                                                what_if_split_esc_recover_veto_rearm_coach_confidence="HIGH",
                                            )
                                            assert coach_handoff_locked == "LOCKED", (coach_handoff_locked, coach_handoff_locked_signals)
                                            assert coach_handoff_locked_signals["reason"] == "single-lane-coach-ready-for-locked-handoff", coach_handoff_locked_signals

                                            coach_handoff_fit_safe, coach_handoff_fit_safe_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_fit_from_signals(
                                                what_if_split_esc_recover_veto_rearm_coach_handoff="LOCKED",
                                                what_if_split_esc_pressure="LOW",
                                            )
                                            assert coach_handoff_fit_safe == "SAFE", (coach_handoff_fit_safe, coach_handoff_fit_safe_signals)
                                            assert coach_handoff_fit_safe_signals["reason"] == "locked-handoff-with-low-pressure", coach_handoff_fit_safe_signals

                                            coach_handoff_fit_tense, coach_handoff_fit_tense_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_fit_from_signals(
                                                what_if_split_esc_recover_veto_rearm_coach_handoff="NONE",
                                                what_if_split_esc_pressure="HIGH",
                                            )
                                            assert coach_handoff_fit_tense == "TENSE", (coach_handoff_fit_tense, coach_handoff_fit_tense_signals)
                                            assert coach_handoff_fit_tense_signals["reason"] == "no-handoff-under-high-pressure", coach_handoff_fit_tense_signals

                                            prior_coach_handoff_why_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_HANDOFF_WHY")
                                            try:
                                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_HANDOFF_WHY"] = "0"
                                                handoff_why_off, handoff_why_off_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_why_from_signals(
                                                    what_if_split_esc_recover_veto_rearm_coach_handoff="LOCKED",
                                                    what_if_split_esc_recover_veto_rearm_coach_handoff_fit="SAFE",
                                                    what_if_split_esc_recover_veto_rearm_coach_confidence="HIGH",
                                                )
                                                assert handoff_why_off == "FLAG OFF", (handoff_why_off, handoff_why_off_signals)
                                                assert handoff_why_off_signals["reason"] == "flag-disabled", handoff_why_off_signals

                                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_HANDOFF_WHY"] = "1"
                                                handoff_why_commit, handoff_why_commit_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_why_from_signals(
                                                    what_if_split_esc_recover_veto_rearm_coach_handoff="LOCKED",
                                                    what_if_split_esc_recover_veto_rearm_coach_handoff_fit="SAFE",
                                                    what_if_split_esc_recover_veto_rearm_coach_confidence="HIGH",
                                                )
                                                assert handoff_why_commit == "COMMIT", (handoff_why_commit, handoff_why_commit_signals)
                                                assert handoff_why_commit_signals["reason"] == "locked-handoff-with-actionable-confidence", handoff_why_commit_signals

                                                handoff_why_hold, handoff_why_hold_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_why_from_signals(
                                                    what_if_split_esc_recover_veto_rearm_coach_handoff="NONE",
                                                    what_if_split_esc_recover_veto_rearm_coach_handoff_fit="TENSE",
                                                    what_if_split_esc_recover_veto_rearm_coach_confidence="LOW",
                                                )
                                                assert handoff_why_hold == "HOLD LINE", (handoff_why_hold, handoff_why_hold_signals)
                                                assert handoff_why_hold_signals["reason"] == "no-coach-handoff-available", handoff_why_hold_signals
                                            finally:
                                                if prior_coach_handoff_why_env is None:
                                                    os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_HANDOFF_WHY", None)
                                                else:
                                                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_HANDOFF_WHY"] = prior_coach_handoff_why_env
                                        finally:
                                            if prior_coach_why_env is None:
                                                os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_WHY", None)
                                            else:
                                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_WHY"] = prior_coach_why_env
                                    finally:
                                        if prior_veto_rearm_nudge_env is None:
                                            os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE", None)
                                        else:
                                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE"] = prior_veto_rearm_nudge_env
                                finally:
                                    if prior_veto_rearm_cooloff_env is None:
                                        os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF", None)
                                    else:
                                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF"] = prior_veto_rearm_cooloff_env
                            finally:
                                if prior_veto_rearm_env is None:
                                    os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM", None)
                                else:
                                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM"] = prior_veto_rearm_env
                        finally:
                            if prior_veto_release_tick_env is None:
                                os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK", None)
                            else:
                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK"] = prior_veto_release_tick_env
                    finally:
                        if prior_veto_release_env is None:
                            os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE", None)
                        else:
                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE"] = prior_veto_release_env
                finally:
                    if prior_veto_cooloff_env is None:
                        os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF", None)
                    else:
                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF"] = prior_veto_cooloff_env
            finally:
                if prior_veto_env is None:
                    os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO", None)
                else:
                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO"] = prior_veto_env

            recover_prior = repo / "recover-prior.json"
            recover_prior.write_text(json.dumps({"whatIfSplitEscRecoverConfidence": "LOW"}), encoding="utf-8")
            delta_up, delta_up_signals = what_if_split_escalate_recover_confidence_delta_from_prior(
                current_confidence="HIGH",
                prior_json_path=recover_prior,
            )
            assert delta_up == "+2", (delta_up, delta_up_signals)
            assert delta_up_signals["reason"] == "confidence-increased-vs-prior-window", delta_up_signals

            recover_prior.write_text(json.dumps({"whatIfSplitEscRecoverConfidence": "HIGH"}), encoding="utf-8")
            delta_down, delta_down_signals = what_if_split_escalate_recover_confidence_delta_from_prior(
                current_confidence="LOW",
                prior_json_path=recover_prior,
            )
            assert delta_down == "-2", (delta_down, delta_down_signals)
            assert delta_down_signals["reason"] == "confidence-decreased-vs-prior-window", delta_down_signals

            delta_flat, delta_flat_signals = what_if_split_escalate_recover_confidence_delta_from_prior(
                current_confidence="MID",
                prior_json_path=repo / "missing-recover-prior.json",
            )
            assert delta_flat == "+0", (delta_flat, delta_flat_signals)
            assert delta_flat_signals["priorLoaded"] is False, delta_flat_signals
            assert delta_flat_signals["reason"] == "confidence-unchanged-vs-prior-window", delta_flat_signals
        finally:
            if prior_recover_why_env is None:
                os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY"] = prior_recover_why_env

    print("[PASS] weekly portal prompt readability drift regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
