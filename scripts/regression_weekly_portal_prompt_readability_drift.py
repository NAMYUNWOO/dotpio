#!/usr/bin/env python3
"""Regression checks for weekly_portal_prompt_readability_drift.py."""
from __future__ import annotations

import hashlib
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
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_fx_pressure_alias,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy,
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
    combo_confidence_fx_accent_from_signals,
    combo_confidence_fx_accent_family_trend_from_prior,
    combo_confidence_coach_copy_swap_recommendation_family_trend_from_prior,
    lane_priority_recommendation_confidence_guard,
    lane_cadence_24h_check,
    lane_underrepresented_watchdog,
    combat_vfx_cadence_coach_why,
    combat_vfx_cadence_coach_why_hysteresis_confidence_floor_fx_pulse_family_trend_from_prior,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_threshold_policy_ops_window_profiler,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_threshold_policy_ops_window_dominant_compact_alias,
    resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly_portal_prompt_readability_drift.py"

# Deterministic markdown adjacency lock for coherence-arc coach compact alias rows.
COHERENCE_ARC_COACH_ORDER_LOCK_SCAFFOLD = {
    "summary": ("- COHERENCE ARC COACH:", "- CVARC:", "- CBGCFXWAC:", "- CBGCFXWAC LEGEND:"),
    "tokenCoverage": ("- COHERENCE ARC COACH:", "- CVARC:", "- CBGCFXWAC:", "- CBGCFXWAC LEGEND:"),
    "enabled": True,
}


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

        def _run_report_with_env(out_json_path: Path, out_md_path: Path, env_overrides: dict[str, str]) -> tuple[dict[str, object], str]:
            env = os.environ.copy()
            env.update(env_overrides)
            subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--since-days",
                    "3650",
                    "--max-commits",
                    "20",
                    "--out-json",
                    str(out_json_path),
                    "--out-md",
                    str(out_md_path),
                    "--out-fx-remap-candidates-json",
                    str(out_fx_candidates_json),
                    "--out-fx-remap-candidates-md",
                    str(out_fx_candidates_md),
                    "--out-ambient-why-auto-remap-plan-json",
                    str(out_ambient_auto_remap_json),
                    "--out-ambient-why-auto-remap-plan-md",
                    str(out_ambient_auto_remap_md),
                ],
                cwd=repo,
                check=True,
                text=True,
                env=env,
                stdout=subprocess.DEVNULL,
            )
            return (
                json.loads(out_json_path.read_text(encoding="utf-8")),
                out_md_path.read_text(encoding="utf-8"),
            )

        def _count_lines(md_text: str, prefix: str) -> int:
            return sum(1 for line in md_text.splitlines() if line.startswith(prefix))

        # Deterministic carryover fixture: narration compact aliases must always map
        # to stable Combat/VFX cue aliases regardless of prior-window token history.
        narration_cue_flag = (
            "DOTPIO_EXPERIMENT_CADENCE_BRIDGE_GLYPH_CONF_FX_PULSE_MICROCOPY_WORLD_TONE_COHERENCE_ARC_"
            "STORYBEAT_PHASE_FX_CUE_INTENSITY_PULSE_LANGUAGE_VARIANT_PACK_PHASE_INTENT_NARRATION_"
            "COMPACT_ALIAS_COMBAT_VFX_FX_CUE"
        )
        prior_narration_cue_flag = os.environ.get(narration_cue_flag)
        os.environ[narration_cue_flag] = "1"
        try:
            drift_streak_fixture = [
                ("A", "ANCHOR", "SOFT", "S"),
                ("R", "RECOVER", "EDGE", "E"),
                ("S", "SURGE", "HARD", "H"),
            ]
            prior_token_alias: str | None = None
            for alias, narration, expected_cue, expected_token_alias in drift_streak_fixture:
                prior_window_payload = {"priorTokenAlias": prior_token_alias} if prior_token_alias is not None else {}
                _, cue_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue(
                    intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_signals={
                        "narration": narration,
                        "alias": alias,
                        "token": f"CBGCFXWSBPFXPIN:{alias}",
                        "priorWindow": prior_window_payload,
                    }
                )
                assert cue_signals["alias"] == alias, cue_signals
                assert cue_signals["cue"] == expected_cue, cue_signals
                assert cue_signals["tokenAlias"] == expected_token_alias, cue_signals
                assert cue_signals["token"] == f"CBGCFXWSBPFXPINF:{expected_token_alias}", cue_signals
                prior_token_alias = expected_token_alias
        finally:
            if prior_narration_cue_flag is None:
                os.environ.pop(narration_cue_flag, None)
            else:
                os.environ[narration_cue_flag] = prior_narration_cue_flag

        fxpde_echo_flag = (
            "DOTPIO_EXPERIMENT_CADENCE_BRIDGE_GLYPH_CONF_FX_PULSE_MICROCOPY_WORLD_TONE_COHERENCE_ARC_"
            "STORYBEAT_PHASE_INTENT_REHEARSAL_PHASE_ECHO_MUTATION"
        )
        fxpde_alias_flag = (
            "DOTPIO_EXPERIMENT_CADENCE_BRIDGE_GLYPH_CONF_FX_PULSE_MICROCOPY_WORLD_TONE_COHERENCE_ARC_"
            "STORYBEAT_PHASE_INTENT_REHEARSAL_PHASE_ECHO_MUTATION_COMPACT_ALIAS"
        )

        fxpde_matrix = {
            "echo_off_alias_off": {
                "env": {fxpde_echo_flag: "0", fxpde_alias_flag: "0"},
                "echo_enabled": False,
                "alias_enabled": False,
            },
            "echo_on_alias_off": {
                "env": {fxpde_echo_flag: "1", fxpde_alias_flag: "0"},
                "echo_enabled": True,
                "alias_enabled": False,
            },
            "echo_off_alias_on": {
                "env": {fxpde_echo_flag: "0", fxpde_alias_flag: "1"},
                "echo_enabled": False,
                "alias_enabled": True,
            },
            "echo_on_alias_on": {
                "env": {fxpde_echo_flag: "1", fxpde_alias_flag: "1"},
                "echo_enabled": True,
                "alias_enabled": True,
            },
        }

        for matrix_name, matrix_case in fxpde_matrix.items():
            matrix_out_json = repo / f"out_{matrix_name}.json"
            matrix_out_md = repo / f"out_{matrix_name}.md"
            matrix_payload, matrix_md = _run_report_with_env(
                out_json_path=matrix_out_json,
                out_md_path=matrix_out_md,
                env_overrides=matrix_case["env"],
            )
            assert matrix_payload.get("checkedCommits", 0) >= 2, matrix_payload
            expected_matrix_key = f"E{1 if matrix_case['echo_enabled'] else 0}A{1 if matrix_case['alias_enabled'] else 0}"
            assert matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrix"
            ) == expected_matrix_key, matrix_payload
            assert matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDrift"
            ) == f"CBGCFXWSBPFXPDE MATRIX DRIFT:{expected_matrix_key}>{expected_matrix_key}", matrix_payload
            drift_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftSignals",
                {},
            )
            assert set(drift_signals.keys()) == {
                "current",
                "prior",
                "changed",
                "streak",
                "priorLoaded",
                "reason",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert drift_signals.get("current") == expected_matrix_key, matrix_payload
            assert drift_signals.get("prior") == expected_matrix_key, matrix_payload
            assert drift_signals.get("changed") is False, matrix_payload
            assert drift_signals.get("streak") == 0, matrix_payload
            assert drift_signals.get("priorLoaded") is False, matrix_payload
            assert drift_signals.get("reason") == "no-prior-window", matrix_payload
            assert drift_signals.get("token") == f"CBGCFXWSBPFXPDE MATRIX DRIFT:{expected_matrix_key}>{expected_matrix_key}", matrix_payload
            assert drift_signals.get("offlineOnly") is True, matrix_payload
            assert matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftChanged"
            ) is False, matrix_payload
            assert matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftStreak"
            ) == 0, matrix_payload
            assert matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftTrendBand"
            ) == f"CBGCFXWSBPFXPDE MATRIX DRIFT TREND:STABLE", matrix_payload
            trend_band_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftTrendBandSignals",
                {},
            )
            assert set(trend_band_signals.keys()) == {
                "band",
                "reason",
                "changed",
                "streak",
                "priorLoaded",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert trend_band_signals.get("band") == "STABLE", matrix_payload
            assert trend_band_signals.get("reason") == "no-prior-window", matrix_payload
            assert trend_band_signals.get("priorLoaded") is False, matrix_payload
            assert trend_band_signals.get("offlineOnly") is True, matrix_payload
            combat_vfx_cue = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyCombatVfxCue"
            )
            assert combat_vfx_cue == "CBGCFXWSBPFXPDE POLICY FX CUE:SOFT", matrix_payload
            combat_vfx_cue_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyCombatVfxCueSignals",
                {},
            )
            assert set(combat_vfx_cue_signals.keys()) == {
                "thresholdPolicy",
                "cue",
                "cueMap",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert combat_vfx_cue_signals.get("thresholdPolicy") == "BASELINE_ONLY", matrix_payload
            assert combat_vfx_cue_signals.get("cue") == "SOFT", matrix_payload
            assert combat_vfx_cue_signals.get("token") == "CBGCFXWSBPFXPDE POLICY FX CUE:SOFT", matrix_payload
            assert combat_vfx_cue_signals.get("offlineOnly") is True, matrix_payload
            threshold_policy_alias = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyCompactAlias"
            )
            assert threshold_policy_alias == "CBGCFXWSBPFXPDP:B", matrix_payload
            threshold_policy_alias_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyCompactAliasSignals",
                {},
            )
            assert set(threshold_policy_alias_signals.keys()) == {
                "thresholdPolicy",
                "alias",
                "aliasMap",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert threshold_policy_alias_signals.get("thresholdPolicy") == "BASELINE_ONLY", matrix_payload
            assert threshold_policy_alias_signals.get("alias") == "B", matrix_payload
            assert threshold_policy_alias_signals.get("token") == "CBGCFXWSBPFXPDP:B", matrix_payload
            assert threshold_policy_alias_signals.get("offlineOnly") is True, matrix_payload
            threshold_policy_copy_pack = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyCopyPack"
            )
            assert threshold_policy_copy_pack == "FLAG OFF", matrix_payload
            threshold_policy_copy_pack_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyCopyPackSignals",
                {},
            )
            assert set(threshold_policy_copy_pack_signals.keys()) == {
                "flagName",
                "flagEnabled",
                "thresholdPolicy",
                "recommendation",
                "copyPack",
                "copyMap",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert threshold_policy_copy_pack_signals.get("flagEnabled") is False, matrix_payload
            assert threshold_policy_copy_pack_signals.get("thresholdPolicy") == "BASELINE_ONLY", matrix_payload
            assert threshold_policy_copy_pack_signals.get("recommendation") == "ESTABLISH_BASELINE", matrix_payload
            assert threshold_policy_copy_pack_signals.get("copyPack") == "CALM_WATCH", matrix_payload
            assert threshold_policy_copy_pack_signals.get("token") == "CBGCFXWSBPFXPDE POLICY COPY:CALM_WATCH", matrix_payload
            assert threshold_policy_copy_pack_signals.get("offlineOnly") is True, matrix_payload
            threshold_policy_world_copyline = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyWorldCopyline"
            )
            assert threshold_policy_world_copyline == "FLAG OFF", matrix_payload
            threshold_policy_world_copyline_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyWorldCopylineSignals",
                {},
            )
            assert set(threshold_policy_world_copyline_signals.keys()) == {
                "flagName",
                "flagEnabled",
                "thresholdPolicy",
                "recommendation",
                "copyline",
                "copylineMap",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert threshold_policy_world_copyline_signals.get("flagEnabled") is False, matrix_payload
            assert threshold_policy_world_copyline_signals.get("thresholdPolicy") == "BASELINE_ONLY", matrix_payload
            assert threshold_policy_world_copyline_signals.get("recommendation") == "ESTABLISH_BASELINE", matrix_payload
            assert threshold_policy_world_copyline_signals.get("copyline") == "HOLD_LINE", matrix_payload
            assert threshold_policy_world_copyline_signals.get("token") == "CBGCFXWSBPFXPDE WORLD COPYLINE:HOLD_LINE", matrix_payload
            assert threshold_policy_world_copyline_signals.get("offlineOnly") is True, matrix_payload
            threshold_policy_ops_window_profiler = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyOpsWindowProfiler"
            )
            assert isinstance(threshold_policy_ops_window_profiler, str) and threshold_policy_ops_window_profiler.startswith(
                "CBGCFXWSBPFXPDE POLICY OPS WINDOW:"
            ), matrix_payload
            threshold_policy_ops_window_profiler_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyOpsWindowProfilerSignals",
                {},
            )
            assert set(threshold_policy_ops_window_profiler_signals.keys()) == {
                "thresholdPolicy",
                "alias",
                "windowSize",
                "windowPolicies",
                "windowAliases",
                "counts",
                "dominantPolicy",
                "changed",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert threshold_policy_ops_window_profiler_signals.get("thresholdPolicy") == "BASELINE_ONLY", matrix_payload
            assert threshold_policy_ops_window_profiler_signals.get("alias") == "B", matrix_payload
            assert threshold_policy_ops_window_profiler_signals.get("offlineOnly") is True, matrix_payload
            threshold_policy_ops_window_dominant_alias = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyOpsWindowDominantCompactAlias"
            )
            assert threshold_policy_ops_window_dominant_alias == "CBGCFXWSBPFXPDE POLICY OPS DOMINANT:B", matrix_payload
            threshold_policy_ops_window_dominant_alias_signals = matrix_payload.get(
                "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyOpsWindowDominantCompactAliasSignals",
                {},
            )
            assert set(threshold_policy_ops_window_dominant_alias_signals.keys()) == {
                "dominantPolicy",
                "alias",
                "aliasMap",
                "token",
                "offlineOnly",
            }, matrix_payload
            assert threshold_policy_ops_window_dominant_alias_signals.get("dominantPolicy") == "BASELINE_ONLY", matrix_payload
            assert threshold_policy_ops_window_dominant_alias_signals.get("alias") == "B", matrix_payload
            assert threshold_policy_ops_window_dominant_alias_signals.get("offlineOnly") is True, matrix_payload

            # Multi-window dominant-policy flip fixture: verify deterministic alias transitions as
            # rolling composition changes.
            fixture_a_prior_path = repo / "fixture_ops_window_a.json"
            fixture_a_prior_path.write_text(
                json.dumps(
                    {
                        "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyOpsWindowProfilerSignals": {
                            "windowPolicies": ["BASELINE_ONLY", "BASELINE_ONLY", "WATCH"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            fixture_a_token, fixture_a_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_threshold_policy_ops_window_profiler(
                snapshot_signals={"thresholdPolicy": "WATCH"},
                prior_json_path=fixture_a_prior_path,
            )
            fixture_a_alias, fixture_a_alias_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_threshold_policy_ops_window_dominant_compact_alias(
                ops_window_profiler_signals=fixture_a_signals
            )
            assert fixture_a_token.startswith("CBGCFXWSBPFXPDE POLICY OPS WINDOW:"), fixture_a_token
            assert fixture_a_signals.get("windowPolicies") == ["BASELINE_ONLY", "BASELINE_ONLY", "WATCH", "WATCH"], fixture_a_signals
            assert fixture_a_signals.get("dominantPolicy") == "WATCH", fixture_a_signals
            assert fixture_a_alias == "CBGCFXWSBPFXPDE POLICY OPS DOMINANT:W", fixture_a_alias
            assert fixture_a_alias_signals.get("alias") == "W", fixture_a_alias_signals

            fixture_b_prior_path = repo / "fixture_ops_window_b.json"
            fixture_b_prior_path.write_text(
                json.dumps(
                    {
                        "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintPhaseEchoMutationFlagMatrixDriftPlaytestSnapshotThresholdPolicyOpsWindowProfilerSignals": {
                            "windowPolicies": ["BASELINE_ONLY", "MANUAL", "MANUAL"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            fixture_b_token, fixture_b_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_threshold_policy_ops_window_profiler(
                snapshot_signals={"thresholdPolicy": "MANUAL"},
                prior_json_path=fixture_b_prior_path,
            )
            fixture_b_alias, fixture_b_alias_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_threshold_policy_ops_window_dominant_compact_alias(
                ops_window_profiler_signals=fixture_b_signals
            )
            assert fixture_b_token.startswith("CBGCFXWSBPFXPDE POLICY OPS WINDOW:"), fixture_b_token
            assert fixture_b_signals.get("windowPolicies") == ["BASELINE_ONLY", "MANUAL", "MANUAL", "MANUAL"], fixture_b_signals
            assert fixture_b_signals.get("dominantPolicy") == "MANUAL", fixture_b_signals
            assert fixture_b_alias == "CBGCFXWSBPFXPDE POLICY OPS DOMINANT:M", fixture_b_alias
            assert fixture_b_alias_signals.get("alias") == "M", fixture_b_alias_signals
            for row_prefix in (
                "- CBGCFXWSBPFXPD ECHO:",
                "- CBGCFXWSBPFXPDE:",
                "- CBGCFXWSBPFXPDE LEGEND:",
                "- CBGCFXWSBPFXPDE MATRIX:",
                "- CBGCFXWSBPFXPDE MATRIX DRIFT TREND:",
                "- CBGCFXWSBPFXPDE POLICY OPS DOMINANT:",
                "- CBGCFXWSBPFXPDE POLICY OPS DOMINANT LEGEND:",
            ):
                observed_count = _count_lines(matrix_md, row_prefix)
                assert observed_count == 2, (
                    f"FXPDE flag matrix mismatch for {matrix_name}: expected 2 instances of "
                    f"{row_prefix}, observed {observed_count}"
                )
            echo_lines = [line for line in matrix_md.splitlines() if line.startswith("- CBGCFXWSBPFXPD ECHO:")]
            alias_lines = [line for line in matrix_md.splitlines() if line.startswith("- CBGCFXWSBPFXPDE:")]
            expected_echo_enabled = str(matrix_case["echo_enabled"])
            expected_alias_enabled = str(matrix_case["alias_enabled"])
            assert all(f"enabled={expected_echo_enabled}" in line for line in echo_lines), (
                f"FXPDE flag matrix mismatch for {matrix_name}: expected ECHO rows to include enabled={expected_echo_enabled}"
            )
            assert all(f"enabled={expected_alias_enabled}" in line for line in alias_lines), (
                f"FXPDE flag matrix mismatch for {matrix_name}: expected alias rows to include enabled={expected_alias_enabled}"
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

        hysteresis_prior = repo / "hysteresis_prior.json"
        hysteresis_prior.write_text(json.dumps({"comboConfidenceFxAccent": "EMBER"}), encoding="utf-8")
        hysteresis_accent, hysteresis_signals = combo_confidence_fx_accent_from_signals(
            scene_arc="IRON",
            fallback_narrative_signals={"volatilityRegime": "SWING", "recommendation": "STEADY"},
            prior_json_path=hysteresis_prior,
        )
        assert hysteresis_accent == "EMBER", hysteresis_signals
        assert hysteresis_signals["hysteresisApplied"] is True, hysteresis_signals
        assert hysteresis_signals["priorAccent"] == "EMBER", hysteresis_signals

        dccfxt_prior = repo / "dccfxt_prior.json"
        dccfxt_prior.write_text(
            json.dumps(
                {
                    "tokenFamilyTotals": {
                        "dmgComboConfidenceFxAccentAlias": {"net": 8}
                    },
                    "comboConfidenceFxAccentFamilyTrendSignals": {"trend": "UP"},
                }
            ),
            encoding="utf-8",
        )
        dccfxt_drift, dccfxt_signals = combo_confidence_fx_accent_family_trend_from_prior(
            current_family_totals={"net": 6},
            prior_json_path=dccfxt_prior,
            volatility_regime="SWING",
        )
        assert dccfxt_drift == -2, dccfxt_signals
        assert dccfxt_signals["hysteresisApplied"] is True, dccfxt_signals
        assert dccfxt_signals["trend"] == "FLAT", dccfxt_signals
        assert dccfxt_signals["trendHysteresisRecommendation"] == "HOLD", dccfxt_signals
        assert dccfxt_signals["trendHysteresisConfidence"] in {"MID", "HIGH"}, dccfxt_signals

        copy_swap_prior = repo / "copy_swap_prior.json"
        copy_swap_prior.write_text(
            json.dumps(
                {
                    "tokenFamilyTotals": {
                        "dmgComboConfidenceCoachCopySwapRecommendationAlias": {"net": 10}
                    },
                    "comboConfidenceCoachCopySwapRecommendationFamilyTrendSignals": {"trend": "DOWN"},
                }
            ),
            encoding="utf-8",
        )
        copy_swap_drift, copy_swap_signals = combo_confidence_coach_copy_swap_recommendation_family_trend_from_prior(
            current_family_totals={"net": 11},
            prior_json_path=copy_swap_prior,
        )
        assert copy_swap_drift == 1, copy_swap_signals
        assert copy_swap_signals["trend"] == "FLAT", copy_swap_signals
        assert copy_swap_signals["hysteresisApplied"] is True, copy_swap_signals

        lprcg_prior = repo / "lprcg_prior.json"
        lprcg_prior.write_text(
            json.dumps({"lanePriorityRecommendationConfidenceGuardSignals": {"divergenceStreak": 2}}),
            encoding="utf-8",
        )
        swing_guard_conf, swing_guard_signals = lane_priority_recommendation_confidence_guard(
            confidence="HIGH",
            floor_family_trend_signals={"trend": "UP"},
            lane_priority_hysteresis_threshold_tuning_signals={
                "volatilityRegimeMemory": "SWING",
                "volatilityRegimeReason": "memory-hold-from-prior-regime",
            },
            prior_json_path=lprcg_prior,
        )
        assert swing_guard_conf == "MID", swing_guard_signals
        assert swing_guard_signals["divergenceThreshold"] == 3, swing_guard_signals
        assert swing_guard_signals["thresholdPolicy"] == "SWING_MEMORY_GUARD_RAISED", swing_guard_signals
        assert swing_guard_signals["guardApplied"] is True, swing_guard_signals

        baseline_guard_conf, baseline_guard_signals = lane_priority_recommendation_confidence_guard(
            confidence="MID",
            floor_family_trend_signals={"trend": "UP"},
            lane_priority_hysteresis_threshold_tuning_signals={
                "volatilityRegimeMemory": "CALM",
                "volatilityRegimeReason": "fresh-calm-regime",
            },
            prior_json_path=repo / "missing_lprcg_prior.json",
        )
        assert baseline_guard_conf == "MID", baseline_guard_signals
        assert baseline_guard_signals["divergenceThreshold"] == 2, baseline_guard_signals
        assert baseline_guard_signals["thresholdPolicy"] == "BASELINE", baseline_guard_signals
        assert baseline_guard_signals["guardApplied"] is False, baseline_guard_signals

        coach_why_prior = repo / "coach_why_prior.json"
        coach_why_prior.write_text(
            json.dumps({"combatVfxCadenceCoachWhy": "COMBAT/VFX CADENCE COACH WHY:RED HOLD"}),
            encoding="utf-8",
        )
        coach_why_token, coach_why_signals = combat_vfx_cadence_coach_why(
            combat_vfx_cadence_watchdog_streak_signals={"streak": 4, "priorStreak": 3},
            lane_cadence_miss_risk_signals={"risk": "MID", "deltaHours": -2.0},
            prior_json_path=coach_why_prior,
        )
        assert coach_why_token == "COMBAT/VFX CADENCE COACH WHY:RED HOLD", coach_why_signals
        assert coach_why_signals["hysteresisApplied"] is True, coach_why_signals
        assert coach_why_signals["priorShort"] == "RED HOLD", coach_why_signals
        assert coach_why_signals["watchdogStreakTrendVolatility"] == "SWING", coach_why_signals

        vfx_fresh_token, vfx_fresh_signals = lane_cadence_24h_check(
            lane_bucket_age={
                "ageHours": {"systems/ops": 3, "design/world": 7, "combat/vfx": 24},
                "windowHours": 24,
            }
        )
        assert vfx_fresh_token == "LANE CADENCE 24H CHECK:PASS", vfx_fresh_signals
        assert vfx_fresh_signals["vfxTouchedWithin24h"] is True, vfx_fresh_signals

        vfx_stale_token, vfx_stale_signals = lane_cadence_24h_check(
            lane_bucket_age={
                "ageHours": {"systems/ops": 3, "design/world": 7, "combat/vfx": 25},
                "windowHours": 24,
            }
        )
        assert vfx_stale_token == "LANE CADENCE 24H CHECK:FAIL", vfx_stale_signals
        assert vfx_stale_signals["vfxTouchedWithin24h"] is False, vfx_stale_signals

        underrep_ok_token, underrep_ok_signals = lane_underrepresented_watchdog(
            lane_bucket_age={
                "ageHours": {"systems/ops": 2, "design/world": 6, "combat/vfx": 12},
                "windowHours": 24,
            }
        )
        assert underrep_ok_token == "LANE UNDERREP WATCHDOG:OK", underrep_ok_signals
        assert underrep_ok_signals["underrepresentedLanes"] == [], underrep_ok_signals

        underrep_warn_token, underrep_warn_signals = lane_underrepresented_watchdog(
            lane_bucket_age={
                "ageHours": {"systems/ops": 1000, "design/world": 28, "combat/vfx": 3},
                "windowHours": 24,
            }
        )
        assert underrep_warn_token == "LANE UNDERREP WATCHDOG:WARN", underrep_warn_signals
        assert "systems/ops" in underrep_warn_signals["untouchedLanes"], underrep_warn_signals
        assert "design/world" in underrep_warn_signals["staleLanes"], underrep_warn_signals

        assert payload.get("comboConfidenceFxAccentTrendHysteresisRecommendation") in {"HOLD", "ALLOW"}, payload
        assert payload.get("comboConfidenceFxAccentTrendHysteresisConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert payload.get("comboConfidenceFxAccentTrendHysteresisAlias") in {"FLAG OFF", "DCCFXH:HL", "DCCFXH:HM", "DCCFXH:HH", "DCCFXH:AL", "DCCFXH:AM", "DCCFXH:AH"}, payload
        assert payload.get("comboConfidenceFxAccentVolatilityAlias") in {"FLAG OFF", "DCCFXV:C", "DCCFXV:S", "DCCFXV:P"}, payload
        assert payload.get("dmgComboConfidenceFxCoachCueAlias") in {"DCCFXC:H", "DCCFXC:T", "DCCFXC:M"}, payload
        assert payload.get("dmgComboConfidenceFxCoachCueWhyAlias") in {"DCCFXCW:R", "DCCFXCW:S", "DCCFXCW:F", "DCCFXCW:B"}, payload
        assert payload.get("comboConfidenceFxCoachCueWhyScenePaletteHint") in {"FLAG OFF", "DCCFXCW SCENE PALETTE:COOL", "DCCFXCW SCENE PALETTE:ASH", "DCCFXCW SCENE PALETTE:SCAR"}, payload
        assert payload.get("comboConfidenceFxCoachCueWhyScenePulse") in {"FLAG OFF", "DCCFXCW SCENE PULSE:SOFT", "DCCFXCW SCENE PULSE:HARD", "DCCFXCW SCENE PULSE:SURGE"}, payload
        assert payload.get("comboConfidenceFxCoachCueWhyScenePulseArc") in {"FLAG OFF", "DCCFXCW SCENE PULSE ARC:RECOVER", "DCCFXCW SCENE PULSE ARC:BRACE", "DCCFXCW SCENE PULSE ARC:ERUPT"}, payload
        assert payload.get("comboConfidenceFxCoachCueWhyScenePulseArcAlias") in {"FLAG OFF", "DCCFXCPA:R", "DCCFXCPA:B", "DCCFXCPA:E"}, payload
        assert set(payload.get("comboConfidenceFxCoachCueWhyScenePulseArcSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "pulse",
            "trend",
            "volatilityRegime",
            "arc",
            "reason",
            "offlineOnly",
        }, payload
        assert set(payload.get("comboConfidenceFxCoachCueWhyScenePulseArcAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "arc",
            "alias",
            "offlineOnly",
        }, payload
        assert set(payload.get("comboConfidenceFxAccentTrendHysteresisAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "recommendation",
            "confidence",
            "alias",
        }, payload
        assert set(payload.get("comboConfidenceFxAccentVolatilityAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "volatilityRegime",
            "alias",
        }, payload
        assert set(payload.get("comboConfidenceFxAccentTrendHysteresisRecommendationSignals", {}).keys()) == {
            "recommendation",
            "reason",
            "volatilityRegime",
            "hysteresisThreshold",
            "hysteresisApplied",
            "rawDrift",
            "offlineOnly",
        }, payload
        assert set(payload.get("comboConfidenceFxAccentTrendHysteresisConfidenceSignals", {}).keys()) == {
            "confidence",
            "reason",
            "hysteresisThreshold",
            "rawDrift",
            "offlineOnly",
        }, payload
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
        assert isinstance(payload.get("pulseRemapSceneMicrolineCadenceFamilyTrendDrift"), int), payload
        assert set(payload.get("pulseRemapSceneMicrolineCadenceFamilyTrendSignals", {}).keys()) == {
            "trend",
            "currentNet",
            "priorNet",
            "priorLoaded",
            "reason",
        }, payload
        assert payload["pulseRemapSceneMicrolineCadenceFamilyTrendSignals"]["trend"] in {"UP", "DOWN", "FLAT"}, payload
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
        assert set(payload.get("pulseRemapSceneMicrolineVariantPack", {}).keys()) == {
            "primary",
            "alternate",
            "fallback",
            "selected",
            "selectedMode",
        }, payload
        assert payload["pulseRemapSceneMicrolineVariantPack"]["selectedMode"] in {"PRIMARY", "ALTERNATE", "FALLBACK"}, payload
        assert set(payload.get("pulseRemapSceneMicrolineVariantPackSignals", {}).keys()) == {
            "suppressionPlan",
            "sceneFlavor",
            "sceneConfidence",
            "laneCadenceRecency",
            "cadenceTrend",
            "selectedMode",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("pulseRemapSceneMicrolineVariantPackSelectionAlias"), str) and payload["pulseRemapSceneMicrolineVariantPackSelectionAlias"].startswith("PRSMV:"), payload
        assert set(payload.get("pulseRemapSceneMicrolineVariantPackSelectionAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert payload.get("pulseRemapSceneMicrolineStyleDiversificationPolicy") in {"ANCHOR", "BLEND", "DIVERSIFY"}, payload
        assert set(payload.get("pulseRemapSceneMicrolineStyleDiversificationPolicySignals", {}).keys()) == {
            "suppressionPlan",
            "sceneConfidence",
            "laneCadenceRecency",
            "cadenceTrend",
            "priorNet",
            "currentNet",
            "cadenceVolatility",
            "priorLoaded",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("pulseRemapSceneMicrolineStylePolicySmoothed") in {"ANCHOR", "BLEND", "DIVERSIFY"}, payload
        assert set(payload.get("pulseRemapSceneMicrolineStylePolicySmoothedSignals", {}).keys()) == {
            "currentPolicy",
            "priorPolicy",
            "priorLoaded",
            "cadenceVolatility",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("pulseRemapSceneMicrolineStylePolicyPostureHook") in {"CALM", "WARN", "ALERT"}, payload
        assert set(payload.get("pulseRemapSceneMicrolineStylePolicyPostureHookSignals", {}).keys()) == {
            "smoothedPolicy",
            "styleTrend",
            "currentNet",
            "priorNet",
            "laneCadenceRecency",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("pulseRemapSceneMicrolineStylePolicyAlias"), str) and payload["pulseRemapSceneMicrolineStylePolicyAlias"].startswith("PRSMP:"), payload
        assert set(payload.get("pulseRemapSceneMicrolineStylePolicyAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert isinstance(payload.get("pulseRemapSceneMicrolineStylePostureAlias"), str) and payload["pulseRemapSceneMicrolineStylePostureAlias"].startswith("PRSMPP:"), payload
        assert set(payload.get("pulseRemapSceneMicrolineStylePostureAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert payload.get("pulseRemapSceneFxGlint") in {"SOFT", "VOID", "SPIKE"}, payload
        assert set(payload.get("pulseRemapSceneFxGlintSignals", {}).keys()) == {
            "stylePosture",
            "suppressionWarning",
            "sceneConfidence",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("pulseRemapSceneFxGlintAlias"), str) and payload["pulseRemapSceneFxGlintAlias"].startswith("PRSFX:"), payload
        assert set(payload.get("pulseRemapSceneFxGlintAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
        assert payload.get("pulseRemapSceneCopyPaletteRecommendation") in {"COOL", "ASH", "SCAR"}, payload
        assert set(payload.get("pulseRemapSceneCopyPaletteRecommendationSignals", {}).keys()) == {
            "sceneFlavor",
            "sceneConfidence",
            "sceneFxGlint",
            "stylePosture",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("pulseRemapSceneMicrolineCadence") in {"RISE", "HOLD", "COOL"}, payload
        assert set(payload.get("pulseRemapSceneMicrolineCadenceSignals", {}).keys()) == {
            "suppressionPlan",
            "sceneConfidence",
            "laneCadenceRecency",
            "cadenceTrend",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("pulseRemapSceneMicrolineStylePolicyFamilyTrendDrift"), int), payload
        assert set(payload.get("pulseRemapSceneMicrolineStylePolicyFamilyTrendSignals", {}).keys()) == {
            "trend",
            "currentNet",
            "priorNet",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("pulseRemapSceneFxGlintFamilyTrendDrift"), int), payload
        assert set(payload.get("pulseRemapSceneFxGlintFamilyTrendSignals", {}).keys()) == {
            "trend",
            "currentNet",
            "priorNet",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("pulseRemapSceneCopyPaletteRecommendationFamilyTrendDrift"), int), payload
        assert set(payload.get("pulseRemapSceneCopyPaletteRecommendationFamilyTrendSignals", {}).keys()) == {
            "trend",
            "currentNet",
            "priorNet",
            "priorLoaded",
            "reason",
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
        assert isinstance(payload.get("pulseRemapSceneCopyPaletteRecommendationAlias"), str) and payload["pulseRemapSceneCopyPaletteRecommendationAlias"].startswith("PRSCP:"), payload
        assert set(payload.get("pulseRemapSceneCopyPaletteRecommendationAliasSignals", {}).keys()) == {"flagName", "flagEnabled"}, payload
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
        assert payload.get("laneCadence24hCheck") in {"LANE CADENCE 24H CHECK:PASS", "LANE CADENCE 24H CHECK:FAIL"}, payload
        assert set(payload.get("laneCadence24hCheckSignals", {}).keys()) == {
            "status",
            "windowHours",
            "systemsOpsAgeHours",
            "designWorldAgeHours",
            "combatVfxAgeHours",
            "vfxTouchedWithin24h",
            "reason",
        }, payload
        assert isinstance(payload.get("vfxTouchedWithin24h"), bool), payload
        assert payload.get("vfxTouchedWithin24h") == (
            payload.get("laneCadence24hCheckSignals", {}).get("vfxTouchedWithin24h")
        ), payload
        assert payload.get("laneUnderrepresentedWatchdog") in {"LANE UNDERREP WATCHDOG:OK", "LANE UNDERREP WATCHDOG:WARN"}, payload
        assert set(payload.get("laneUnderrepresentedWatchdogSignals", {}).keys()) == {
            "status",
            "windowHours",
            "staleLanes",
            "untouchedLanes",
            "underrepresentedLanes",
            "reason",
        }, payload
        assert payload.get("laneUnderrepresentedWatchdogSignals", {}).get("status") in {"OK", "WARN"}, payload
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
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardSignals", {}).keys()) == {
            "baseConfidence",
            "guardedConfidence",
            "trend",
            "volatilityRegime",
            "diverged",
            "priorStreak",
            "divergenceStreak",
            "divergenceThreshold",
            "thresholdPolicy",
            "guardApplied",
            "priorLoaded",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardAlias"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "action",
            "alias",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardThreshold"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardThresholdSignals", {}).keys()) == {
            "threshold",
            "policy",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoach"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachSignals", {}).keys()) == {
            "guardAction",
            "priorConsecutiveApplyWindows",
            "consecutiveApplyWindows",
            "triggered",
            "priorLoaded",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachAlias"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "coachToken",
            "alias",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPack"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPackSignals", {}).keys()) == {
            "pack",
            "priorPack",
            "guardAction",
            "consecutiveApplyWindows",
            "volatilityRegime",
            "priorVolatilityRegime",
            "regimeChanged",
            "priorLoaded",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPackAlias"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPackAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "packToken",
            "alias",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyNarrative"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyNarrativeSignals", {}).keys()) == {
            "pack",
            "guardAction",
            "volatilityRegime",
            "priorVolatilityRegime",
            "regimeChanged",
            "consecutiveApplyWindows",
            "divergenceStreak",
            "reason",
            "offlineOnly",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyAlias"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "coachCopyToken",
            "alias",
        }, payload
        assert isinstance(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyWhy"), str), payload
        assert set(payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "reason",
            "short",
            "offlineOnly",
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
        assert "lanePriorityHysteresisFloorRecommendationAlias" in payload["tokenFamilyTotals"], payload
        assert "lanePriorityHysteresisFloorFamilyTrendAlias" in payload["tokenFamilyTotals"], payload
        assert "lanePriorityHysteresisFloorFamilyTrendDrift" in payload, payload
        assert "lanePriorityHysteresisFloorFamilyTrendSignals" in payload, payload
        assert "lanePriorityHysteresisFloorFamilyTrendAlias" in payload, payload
        assert "lanePriorityHysteresisFloorFamilyTrendAliasSignals" in payload, payload
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
        assert "lanePriorityRecommendationConfidenceGuardThresholdAlias" in payload["tokenFamilyTotals"], payload
        assert "lanePriorityRecommendationConfidenceGuardCoachPackAlias" in payload["tokenFamilyTotals"], payload
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
        assert "DMG COMBO FAMILY CHURN" in md_text
        assert "DMG COMBO CONF FAMILY CHURN" in md_text
        assert "DMG COMBO RETUNE + DCR FAMILY CHURN" in md_text
        assert "DMG COMBO RETUNE CONF + DCRC FAMILY CHURN" in md_text
        assert "DMG COMBO CHAIN COACH FAMILY CHURN" in md_text
        assert "PULSE REMAP MOMENTUM FAMILY CHURN" in md_text
        assert "PULSE REMAP SUPPRESS FAMILY CHURN" in md_text
        assert "PULSE REMAP SUPPRESS PLAN FAMILY CHURN" in md_text
        assert "PULSE REMAP SCENE MICROLINE VARIANT PACK FAMILY CHURN" in md_text
        assert "PULSE REMAP SCENE MICROLINE STYLE POLICY + PRSMP FAMILY CHURN" in md_text
        assert "DMG GLYPH FAMILY CHURN" in md_text
        assert "DMG GLYPH FX LIVE FAMILY CHURN" in md_text
        assert "LPR HYS THR FAMILY CHURN" in md_text
        assert "LPR HYS WINDOW Δ FAMILY CHURN" in md_text
        assert "LPR HYS FLOOR REC + LPR HYS FLOOR FAMILY CHURN" in md_text
        assert "LPR HYS FLOOR FAMILY TREND" in md_text
        assert "LANE CADENCE SUMMARY" in md_text
        assert "LBA:" in md_text
        assert "LANE BUCKET AGE:" in md_text
        assert "LANE BUCKET AGE Δ:" in md_text
        assert "LANE CADENCE RECENCY:" in md_text
        assert "LANE CADENCE MISS RISK:" in md_text
        assert "LANE CADENCE 24H CHECK:" in md_text
        assert "COMBAT/VFX CADENCE WATCHDOG:" in md_text
        assert "COMBAT/VFX CADENCE WATCHDOG STREAK:" in md_text
        assert "COMBAT/VFX CADENCE COACH:" in md_text
        assert "COMBAT/VFX CADENCE COACH WHY:" in md_text
        assert "CVCW:" in md_text
        assert "CVCWH:" in md_text
        assert "CVCWHR:" in md_text
        assert "CVCWHR CONF:" in md_text
        assert "CVCWHRC:" in md_text
        assert "CVCWHR CONF FLOOR REC:" in md_text
        assert "CVCWHRF:" in md_text
        assert "CVCWHR FX PULSE:" in md_text
        assert "CVCWHR FX PULSE LEGEND:" in md_text
        assert "CVCWHR FX LEGEND REC:" in md_text
        assert "CVCWHR FX LEGEND REC CONF:" in md_text
        assert "CVCWHR FX LEGEND CP:" in md_text
        assert "CVCWHR FX LEGEND COPY PACK TREND:" in md_text
        assert "CVCWHR FX LEGEND CPT:" in md_text
        assert "CVCWHR FX LEGEND COPY PACK TREND CONF:" in md_text
        assert "CVCWHR FX LEGEND CPTC:" in md_text
        assert "CVCWHR FX LEGEND CPTC LEGEND:" in md_text
        assert "CVCWHR FX LEGEND CPTC OVERRIDE:" in md_text
        assert "CADENCE BRIDGE:" in md_text
        assert "CADENCE BRIDGE GLYPH:" in md_text
        assert "CVCWHR CONF FLOOR + CVCWHRF FAMILY CHURN:" in md_text
        assert "CADENCE BRIDGE FAMILY CHURN:" in md_text
        assert "CVCWH FAMILY CHURN:" in md_text
        assert "CVCWHR FAMILY CHURN:" in md_text
        assert "CVCWHR CONF + CVCWHRC FAMILY CHURN:" in md_text
        assert "COMBAT/VFX CADENCE COACH WHY + CVCW FAMILY CHURN:" in md_text
        assert "CVCC:" in md_text
        assert "COMBAT/VFX CADENCE WATCHDOG LEGEND:" in md_text
        assert "LCMR:" in md_text
        assert "LANE PRIORITY REC:" in md_text
        assert "LPR:" in md_text
        assert "LPR HYS:" in md_text
        assert "LPR HYS RAIL:" in md_text
        assert "LPR HYS THRESH REC:" in md_text
        assert "LPR VOL REGIME:" in md_text
        assert "LPR HYS THR:" in md_text
        assert "LPR HYS WINDOW:" in md_text
        assert "LPR HYS WINDOW Δ:" in md_text
        assert "LPR HYS FLOOR REC:" in md_text
        assert "LPR HYS FLOOR:" in md_text
        assert "LANE PRIORITY REC CONF:" in md_text
        assert "LANE PRIORITY REC CONF GUARD:" in md_text
        assert "LPRCG:" in md_text
        assert "LPRCG THRESH:" in md_text
        assert "LPRCG COACH:" in md_text
        assert "LPRCGC:" in md_text
        assert "LPRCG COACH PACK:" in md_text
        assert "LPRCGCP:" in md_text
        assert "LPRCG COACH COPY:" in md_text
        assert "LPRCGCN:" in md_text
        assert "LPRCG COACH COPY WHY:" in md_text
        assert "LPRCG THRESH FAMILY CHURN" in md_text
        assert "LPRCG COACH + LPRCGC FAMILY CHURN" in md_text
        assert "LPRCG COACH PACK + LPRCGCP FAMILY CHURN" in md_text
        assert "LPRCG COACH COPY + LPRCGCN FAMILY CHURN" in md_text
        assert payload.get("combatVfxCadenceCoach") in {
            "COMBAT/VFX CADENCE COACH:NUDGE",
            "COMBAT/VFX CADENCE COACH:ARM",
            "COMBAT/VFX CADENCE COACH:ESCALATE",
        }, payload
        assert set(payload.get("combatVfxCadenceCoachSignals", {}).keys()) == {
            "coach",
            "watchdogStatus",
            "watchdogStreak",
            "laneCadenceMissRisk",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("combatVfxCadenceCoachWhy", "").startswith("COMBAT/VFX CADENCE COACH WHY:"), payload
        assert set(payload.get("combatVfxCadenceCoachWhySignals", {}).keys()) == {
            "short",
            "reason",
            "laneCadenceMissRisk",
            "laneCadenceDeltaHours",
            "watchdogStreak",
            "priorWatchdogStreak",
            "watchdogStreakDelta",
            "watchdogStreakTrend",
            "watchdogStreakTrendVolatility",
            "priorShort",
            "priorLoaded",
            "hysteresisApplied",
            "offlineOnly",
        }, payload
        assert payload.get("combatVfxCadenceCoachWhyAlias") in {"FLAG OFF", "CVCW:R", "CVCW:H", "CVCW:P", "CVCW:C", "CVCW:B"}, payload
        assert set(payload.get("combatVfxCadenceCoachWhyAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "coachWhyToken",
            "alias",
        }, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisAlias") in {"FLAG OFF", "CVCWH:H", "CVCWH:S"}, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisRecommendationAlias") in {"CVCWHR:HOLD", "CVCWHR:RELAX"}, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisRecommendationConfidence") in {"CVCWHR CONF:LOW", "CVCWHR CONF:MID", "CVCWHR CONF:HIGH"}, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisRecommendationConfidenceAlias") in {"FLAG OFF", "CVCWHRC:L", "CVCWHRC:M", "CVCWHRC:H"}, payload
        assert isinstance(payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseFamilyTrendDrift"), int), payload
        assert set(payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseFamilyTrendSignals", {}).keys()) == {
            "trend",
            "currentNet",
            "priorNet",
            "priorLoaded",
            "reason",
        }, payload
        assert payload["combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseFamilyTrendSignals"]["trend"] in {"UP", "DOWN", "FLAT"}, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackAlias") in {"FLAG OFF", "CVCWHR FX LEGEND CP:T", "CVCWHR FX LEGEND CP:D", "CVCWHR FX LEGEND CP:N"}, payload
        assert set(payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "copyPackToken",
            "alias",
        }, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrend") in {"COPY PACK TREND:STABLE", "COPY PACK TREND:SHIFTING"}, payload
        assert set(payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrendSignals", {}).keys()) == {
            "trend",
            "copyPack",
            "priorCopyPack",
            "deltaHours",
            "priorDeltaHours",
            "momentumShiftHours",
            "priorLoaded",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrendAlias") in {"FLAG OFF", "CVCWHR FX LEGEND CPT:S", "CVCWHR FX LEGEND CPT:H"}, payload
        assert set(payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrendAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "trendToken",
            "trend",
            "alias",
        }, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrendConfidence") in {
            "CVCWHR FX LEGEND COPY PACK TREND CONF:LOW",
            "CVCWHR FX LEGEND COPY PACK TREND CONF:MID",
            "CVCWHR FX LEGEND COPY PACK TREND CONF:HIGH",
        }, payload
        assert set(payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrendConfidenceSignals", {}).keys()) == {
            "confidence",
            "trend",
            "priorLoaded",
            "momentumShiftHours",
            "reason",
            "offlineOnly",
            "aliasToken",
            "alias",
            "flagName",
            "flagEnabled",
        }, payload
        assert payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrendConfidenceOverride") in {
            "CVCWHR FX LEGEND CPTC OVERRIDE:ON",
            "CVCWHR FX LEGEND CPTC OVERRIDE:OFF",
        }, payload
        assert set(payload.get("combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseLegendCopyPackTrendConfidenceOverrideSignals", {}).keys()) == {
            "override",
            "trend",
            "confidence",
            "expectedConfidence",
            "diverged",
            "mismatchStreak",
            "priorMismatchStreak",
            "priorLoaded",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackVariants") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCW COPY PACK:PACE_HOLD",
            "CBGCFXWSBPFXPDCW COPY PACK:PACE_PIVOT",
            "CBGCFXWSBPFXPDCW COPY PACK:PACE_COVER",
            "CBGCFXWSBPFXPDCW COPY PACK:PUNCH_HOLD",
            "CBGCFXWSBPFXPDCW COPY PACK:PUNCH_FEINT",
            "CBGCFXWSBPFXPDCW COPY PACK:PUNCH_BURST",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackVariantsSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "alias",
            "family",
            "familyMap",
            "writerTooltipVariants",
            "writerTooltipVariantsMap",
            "sourceToken",
            "compactToken",
            "token",
            "offlineOnly",
        }, payload
        copy_pack_variants_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackVariantsSignals", {})
        assert copy_pack_variants_signals.get("alias") in {"A", "B", "C", "D", "E", "F"}, payload
        assert copy_pack_variants_signals.get("family") in {
            "PACE_HOLD",
            "PACE_PIVOT",
            "PACE_COVER",
            "PUNCH_HOLD",
            "PUNCH_FEINT",
            "PUNCH_BURST",
        }, payload
        assert copy_pack_variants_signals.get("compactToken", "").startswith("CW PACK:"), payload
        tooltip_variants = copy_pack_variants_signals.get("writerTooltipVariants")
        assert isinstance(tooltip_variants, list), payload
        assert len(tooltip_variants) == 2, payload
        assert all(isinstance(v, str) and v.strip() for v in tooltip_variants), payload
        tooltip_variants_map = copy_pack_variants_signals.get("writerTooltipVariantsMap")
        assert isinstance(tooltip_variants_map, dict), payload
        assert set(tooltip_variants_map.keys()) == {"A", "B", "C", "D", "E", "F"}, payload
        assert all(isinstance(entries, list) and len(entries) == 2 for entries in tooltip_variants_map.values()), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadence") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCW COPY PACK CADENCE:STEADY",
            "CBGCFXWSBPFXPDCW COPY PACK CADENCE:PIVOT",
            "CBGCFXWSBPFXPDCW COPY PACK CADENCE:BURST",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "family",
            "cadence",
            "cadenceMap",
            "sourceToken",
            "token",
            "offlineOnly",
        }, payload
        copy_pack_cadence_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceSignals", {})
        assert copy_pack_cadence_signals.get("family") in {
            "PACE_HOLD",
            "PACE_PIVOT",
            "PACE_COVER",
            "PUNCH_HOLD",
            "PUNCH_FEINT",
            "PUNCH_BURST",
        }, payload
        assert copy_pack_cadence_signals.get("cadence") in {"STEADY", "PIVOT", "BURST"}, payload
        cadence_map = copy_pack_cadence_signals.get("cadenceMap")
        assert isinstance(cadence_map, dict), payload
        assert set(cadence_map.keys()) == {"PACE_HOLD", "PACE_PIVOT", "PACE_COVER", "PUNCH_HOLD", "PUNCH_FEINT", "PUNCH_BURST"}, payload
        assert set(cadence_map.values()) <= {"STEADY", "PIVOT", "BURST"}, payload
        assert cadence_map == {
            "PACE_HOLD": "STEADY",
            "PACE_PIVOT": "PIVOT",
            "PACE_COVER": "STEADY",
            "PUNCH_HOLD": "STEADY",
            "PUNCH_FEINT": "PIVOT",
            "PUNCH_BURST": "BURST",
        }, payload
        assert cadence_map.get(copy_pack_cadence_signals.get("family")) == copy_pack_cadence_signals.get("cadence"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCompactAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWC:S",
            "CBGCFXWSBPFXPDCWC:P",
            "CBGCFXWSBPFXPDCWC:B",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "cadence",
            "alias",
            "aliasMap",
            "sourceToken",
            "token",
            "offlineOnly",
        }, payload
        copy_pack_cadence_compact_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCompactAliasSignals", {})
        assert copy_pack_cadence_compact_alias_signals.get("cadence") in {"STEADY", "PIVOT", "BURST"}, payload
        assert copy_pack_cadence_compact_alias_signals.get("alias") in {"S", "P", "B"}, payload
        assert copy_pack_cadence_compact_alias_signals.get("aliasMap") == {"STEADY": "S", "PIVOT": "P", "BURST": "B"}, payload
        assert copy_pack_cadence_compact_alias_signals.get("aliasMap", {}).get(copy_pack_cadence_compact_alias_signals.get("cadence")) == copy_pack_cadence_compact_alias_signals.get("alias"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCue") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCW FX CUE:SOFT",
            "CBGCFXWSBPFXPDCW FX CUE:EDGE",
            "CBGCFXWSBPFXPDCW FX CUE:HARD",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "cadence",
            "fxCue",
            "fxCueMap",
            "sourceToken",
            "token",
            "offlineOnly",
        }, payload
        copy_pack_cadence_combat_vfx_fx_cue_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueSignals", {})
        assert copy_pack_cadence_combat_vfx_fx_cue_signals.get("cadence") in {"STEADY", "PIVOT", "BURST"}, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_signals.get("fxCue") in {"SOFT", "EDGE", "HARD"}, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_signals.get("fxCueMap") == {"STEADY": "SOFT", "PIVOT": "EDGE", "BURST": "HARD"}, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_signals.get("fxCueMap", {}).get(copy_pack_cadence_combat_vfx_fx_cue_signals.get("cadence")) == copy_pack_cadence_combat_vfx_fx_cue_signals.get("fxCue"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWF:S",
            "CBGCFXWSBPFXPDCWF:E",
            "CBGCFXWSBPFXPDCWF:H",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "fxCue",
            "alias",
            "aliasMap",
            "sourceToken",
            "token",
            "offlineOnly",
        }, payload
        copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasSignals", {})
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals.get("fxCue") in {"SOFT", "EDGE", "HARD"}, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals.get("alias") in {"S", "E", "H"}, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals.get("aliasMap") == {"SOFT": "S", "EDGE": "E", "HARD": "H"}, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals.get("aliasMap", {}).get(copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals.get("fxCue")) == copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals.get("alias"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherence") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWF COHERENCE:OK",
            "CBGCFXWSBPFXPDCWF COHERENCE:DRIFT",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "alias",
            "sourceToken",
            "expectedSourceToken",
            "status",
            "token",
            "offlineOnly",
        }, payload
        copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceSignals", {})
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("alias") in {"S", "E", "H"}, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("status") in {"OK", "DRIFT"}, payload
        expected_source_map = {
            "S": "CBGCFXWSBPFXPDCW FX CUE:SOFT",
            "E": "CBGCFXWSBPFXPDCW FX CUE:EDGE",
            "H": "CBGCFXWSBPFXPDCW FX CUE:HARD",
        }
        expected_source_from_alias = expected_source_map[copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("alias")]
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("expectedSourceToken") == expected_source_from_alias, payload
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("sourceToken") == copy_pack_cadence_combat_vfx_fx_cue_compact_alias_signals.get("sourceToken"), payload
        assert copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("status") == (
            "OK"
            if copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("sourceToken")
            == copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_signals.get("expectedSourceToken")
            else "DRIFT"
        ), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceMicrolinePair") in {
            "FLAG OFF",
            "COHERENCE COPY:LOCKED LANE|digest alias/source aligned",
            "COHERENCE COPY:DRIFT WATCH|digest alias/source mismatch",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceMicrolinePairSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "status",
            "pairMap",
            "selected",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFC:O",
            "CBGCFXWSBPFXPDCWFC:D",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "status",
            "alias",
            "aliasMap",
            "tooltipMap",
            "tooltip",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCT:L",
            "CBGCFXWSBPFXPDCWFCT:R",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "alias",
            "tooltipAlias",
            "tooltipAliasMap",
            "microlineMap",
            "microline",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCTA:S",
            "CBGCFXWSBPFXPDCWFCTA:R",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "tooltipAlias",
            "actionAlias",
            "actionAliasMap",
            "microlineMap",
            "microline",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopy") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCTA RFALL:NONE",
            "CBGCFXWSBPFXPDCWFCTA RFALL:V1",
            "CBGCFXWSBPFXPDCWFCTA RFALL:V2",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionAlias",
            "rStreak",
            "selectedVariant",
            "variantMap",
            "selectedCopy",
            "reason",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopySignals", {}).get("actionAlias") in {"S", "R"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopySignals", {}).get("selectedVariant") in {"NONE", "V1", "V2"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopySignals", {}).get("reason") in {
            "steady-window",
            "single-review-window",
            "repeated-review-window",
            "repeated-review-window-escalated",
        }, payload
        assert int(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopyRStreak", -1)) >= 0, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNote") in {
            "FLAG OFF",
            "CTA REVIEW CADENCE NOTE:steady-scan",
            "CTA REVIEW CADENCE NOTE:repeat-once",
            "CTA REVIEW CADENCE NOTE:repeat-escalate",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "selectedVariant",
            "note",
            "noteMap",
            "reason",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteSignals", {}).get("selectedVariant") in {"NONE", "V1", "V2"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteSignals", {}).get("note") in {"steady-scan", "repeat-once", "repeat-escalate"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteSignals", {}).get("reason") == "aligned-with-rfall-selection", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCTAN:S",
            "CBGCFXWSBPFXPDCWFCTAN:O",
            "CBGCFXWSBPFXPDCWFCTAN:E",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "note",
            "alias",
            "noteAliasMap",
            "aliasDecode",
            "operatorDecodeMicrolineMap",
            "operatorDecodeMicroline",
            "cadence",
            "reason",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasSignals", {}).get("note") in {
            "steady-scan",
            "repeat-once",
            "repeat-escalate",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasSignals", {}).get("alias") in {
            "S",
            "O",
            "E",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasSignals", {}).get("cadence") in {
            "STEADY_SCAN",
            "REPEAT_ONCE",
            "REPEAT_ESCALATE",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasSignals", {}).get("operatorDecodeMicroline", "").startswith((
            "STEADY_SCAN=",
            "REPEAT_ONCE=",
            "REPEAT_ESCALATE=",
        )), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasSignals", {}).get("reason") == "compact-rfall-aligned-cadence-route", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasOperatorPostureAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCTAP:H",
            "CBGCFXWSBPFXPDCWFCTAP:O",
            "CBGCFXWSBPFXPDCWFCTAP:T",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasOperatorPostureAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "cadenceNoteAlias",
            "cadenceAliasDomain",
            "posture",
            "postureMap",
            "postureDomain",
            "compactAlias",
            "compactAliasMap",
            "compactAliasDomain",
            "transitionPath",
            "transitionPathAliases",
            "transitionMap",
            "reason",
            "token",
            "offlineOnly",
        }, payload
        operator_posture_alias_signals = payload.get(
            "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasOperatorPostureAliasSignals",
            {},
        )
        assert operator_posture_alias_signals.get("cadenceNoteAlias") in {"S", "O", "E"}, payload
        assert operator_posture_alias_signals.get("cadenceAliasDomain") == ["S", "O", "E"], payload
        assert operator_posture_alias_signals.get("posture") in {"HOLD", "REPLAY_ONCE", "TRIAGE_REPLAY"}, payload
        assert operator_posture_alias_signals.get("postureDomain") == ["HOLD", "REPLAY_ONCE", "TRIAGE_REPLAY"], payload
        assert operator_posture_alias_signals.get("compactAlias") in {"H", "O", "T"}, payload
        assert operator_posture_alias_signals.get("compactAliasDomain") == ["H", "O", "T"], payload
        assert operator_posture_alias_signals.get("transitionPath") == "S->O->E", payload
        assert operator_posture_alias_signals.get("transitionPathAliases") == ["H", "O", "T"], payload
        assert operator_posture_alias_signals.get("transitionMap") == {"S": "H", "O": "O", "E": "T"}, payload
        assert operator_posture_alias_signals.get("reason") == "cadence-note-operator-posture-route", payload

        # Deterministic fixture (Cycle HY follow-up): verify schema/domain contract and
        # transition aliases stay stable across explicit S->O->E cadence alias progression.
        for cadence_alias, expected_posture, expected_compact_alias in (
            ("S", "HOLD", "H"),
            ("O", "REPLAY_ONCE", "O"),
            ("E", "TRIAGE_REPLAY", "T"),
        ):
            fixture_token, fixture_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias(
                {"alias": cadence_alias}
            )
            assert fixture_token in {"FLAG OFF", f"CBGCFXWSBPFXPDCWFCTAP:{expected_compact_alias}"}, fixture_token
            assert fixture_signals.get("cadenceNoteAlias") == cadence_alias, fixture_signals
            assert fixture_signals.get("cadenceAliasDomain") == ["S", "O", "E"], fixture_signals
            assert fixture_signals.get("posture") == expected_posture, fixture_signals
            assert fixture_signals.get("postureDomain") == ["HOLD", "REPLAY_ONCE", "TRIAGE_REPLAY"], fixture_signals
            assert fixture_signals.get("compactAlias") == expected_compact_alias, fixture_signals
            assert fixture_signals.get("compactAliasDomain") == ["H", "O", "T"], fixture_signals
            assert fixture_signals.get("transitionPath") == "S->O->E", fixture_signals
            assert fixture_signals.get("transitionPathAliases") == ["H", "O", "T"], fixture_signals
            assert fixture_signals.get("transitionMap") == {"S": "H", "O": "O", "E": "T"}, fixture_signals

        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasOperatorPostureTransitionStageAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCTAS:H",
            "CBGCFXWSBPFXPDCWFCTAS:R",
            "CBGCFXWSBPFXPDCWFCTAS:T",
        }, payload
        transition_stage_signals = payload.get(
            "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasOperatorPostureTransitionStageAliasSignals",
            {},
        )
        assert set(transition_stage_signals.keys()) == {
            "flagName",
            "flagEnabled",
            "cadenceNoteAlias",
            "cadenceAliasDomain",
            "transitionPath",
            "stage",
            "stageMap",
            "stageAlias",
            "stageAliasMap",
            "token",
            "offlineOnly",
        }, payload
        assert transition_stage_signals.get("cadenceAliasDomain") == ["S", "O", "E"], payload
        assert transition_stage_signals.get("transitionPath") == "S->O->E", payload
        assert transition_stage_signals.get("stage") in {"HOLD_STEP", "REPLAY_STEP", "TRIAGE_STEP"}, payload
        assert transition_stage_signals.get("stageAlias") in {"H", "R", "T"}, payload

        for cadence_alias, expected_stage, expected_stage_alias in (
            ("S", "HOLD_STEP", "H"),
            ("O", "REPLAY_STEP", "R"),
            ("E", "TRIAGE_STEP", "T"),
        ):
            transition_stage_token, transition_fixture_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias(
                {"cadenceNoteAlias": cadence_alias}
            )
            assert transition_stage_token in {"FLAG OFF", f"CBGCFXWSBPFXPDCWFCTAS:{expected_stage_alias}"}, transition_stage_token
            assert transition_fixture_signals.get("cadenceNoteAlias") == cadence_alias, transition_fixture_signals
            assert transition_fixture_signals.get("stage") == expected_stage, transition_fixture_signals
            assert transition_fixture_signals.get("stageAlias") == expected_stage_alias, transition_fixture_signals
            assert transition_fixture_signals.get("transitionPath") == "S->O->E", transition_fixture_signals
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasOperatorPostureTransitionStageAliasCopyPackFxPressureAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCTASF:S",
            "CBGCFXWSBPFXPDCWFCTASF:E",
            "CBGCFXWSBPFXPDCWFCTASF:H",
        }, payload
        fx_pressure_signals = payload.get(
            "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewCadenceNoteCompactAliasOperatorPostureTransitionStageAliasCopyPackFxPressureAliasSignals",
            {},
        )
        assert set(fx_pressure_signals.keys()) == {
            "flagName",
            "flagEnabled",
            "resolvedAlias",
            "resolvedAliasDomain",
            "pressureAliasMap",
            "pressureAlias",
            "pressureAliasDomain",
            "pressureMap",
            "pressure",
            "token",
            "offlineOnly",
        }, payload
        assert fx_pressure_signals.get("resolvedAlias") in {"H", "R", "T"}, payload
        assert fx_pressure_signals.get("pressureAlias") in {"S", "E", "H"}, payload
        assert fx_pressure_signals.get("pressure") in {"SOFT", "EDGE", "HARD"}, payload

        for resolved_alias, expected_pressure_alias, expected_pressure in (
            ("H", "S", "SOFT"),
            ("R", "E", "EDGE"),
            ("T", "H", "HARD"),
        ):
            pressure_token, pressure_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_fx_pressure_alias(
                {"resolvedAlias": resolved_alias}
            )
            assert pressure_token in {"FLAG OFF", f"CBGCFXWSBPFXPDCWFCTASF:{expected_pressure_alias}"}, pressure_token
            assert pressure_signals.get("resolvedAlias") == resolved_alias, pressure_signals
            assert pressure_signals.get("pressureAlias") == expected_pressure_alias, pressure_signals
            assert pressure_signals.get("pressure") == expected_pressure, pressure_signals
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionEscalationAlias") in {
            "FLAG OFF",
            "CBGCFXWSBPFXPDCWFCTAE:H",
            "CBGCFXWSBPFXPDCWFCTAE:T",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionEscalationAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "actionAlias",
            "escalationAlias",
            "escalationAliasMap",
            "escalationMap",
            "escalation",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionEscalationAliasSignals", {}).get("actionAlias") in {"S", "R"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionEscalationAliasSignals", {}).get("escalationAlias") in {"H", "T"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionEscalationAliasSignals", {}).get("escalation") in {"HOLD", "TRIAGE"}, payload
        assert payload.get("cadenceBridge") in {"CADENCE BRIDGE:SCOUT", "CADENCE BRIDGE:PRESS", "CADENCE BRIDGE:HOLD"}, payload
        assert set(payload.get("cadenceBridgeSignals", {}).keys()) == {"bridge", "confidenceFloorRecommendation", "designWorldAgeHours", "systemsOpsAgeHours", "combatVfxAgeHours", "windowHours", "reason", "offlineOnly"}, payload
        assert payload.get("cadenceBridgeGlyph") in {"FLAG OFF", "CADENCE BRIDGE GLYPH:CALM", "CADENCE BRIDGE GLYPH:TENSE"}, payload
        assert set(payload.get("cadenceBridgeGlyphSignals", {}).keys()) == {"flagName", "flagEnabled", "bridge", "glyph", "designWorldAgeHours", "systemsOpsAgeHours", "combatVfxAgeHours", "freshestOtherAgeHours", "designWorldGapHours", "reason", "offlineOnly"}, payload
        assert payload.get("cadenceBridgeGlyphConfidence") in {"FLAG OFF", "CADENCE BRIDGE GLYPH CONF:LOW", "CADENCE BRIDGE GLYPH CONF:MID", "CADENCE BRIDGE GLYPH CONF:HIGH"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceSignals", {}).keys()) == {"flagName", "flagEnabled", "confidence", "currentGapHours", "priorGapHours", "gapDriftHours", "gapVolatilityHours", "priorGapVolatilityHours", "currentSpike", "spikeMemoryWindows", "priorSpikeMemoryWindows", "volatilityRegime", "priorLoaded", "priorGlyphToken", "reason", "offlineOnly"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceSignals", {}).get("volatilityRegime") in {"CALM", "SWING", "SPIKE"}, payload
        assert int(payload.get("cadenceBridgeGlyphConfidenceSignals", {}).get("spikeMemoryWindows", -1)) in {0, 1, 2}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceCompactAlias") in {"FLAG OFF", "CBGC:L", "CBGC:M", "CBGC:H"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceCompactAliasSignals", {}).keys()) == {"flagName", "flagEnabled", "confidence", "alias", "aliasToken"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceLegendCompactAlias") in {"FLAG OFF", "CBGCL:LMH"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceLegendCompactAliasSignals", {}).keys()) == {"flagName", "flagEnabled", "alias", "aliasToken"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrative") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentCue") in {"H", "P", "T", "U"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePack") == "CBGC INTENT ALT PACK:hold|anchor/prep|brace/triage|stabilize", payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackCompactAlias") in {"FLAG OFF", "CBGCI:HPTU"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackCompactAliasSignals", {}).keys()) == {"flagName", "flagEnabled", "alias", "aliasToken", "cue", "current"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackCompactAliasSignals", {}).get("alias") == "HPTU", payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackCompactAliasSignals", {}).get("aliasToken") == "CBGCI:HPTU", payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackCompactAliasSignals", {}).get("cue") in {"H", "P", "T", "U"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackCompactAliasSignals", {}).get("current") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackActiveAlias") in {"FLAG OFF", "CBGCIA:H", "CBGCIA:P", "CBGCIA:T", "CBGCIA:U"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackActiveAliasSignals", {}).keys()) == {"flagName", "flagEnabled", "cue", "current", "aliasToken"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackActiveAliasSignals", {}).get("cue") in {"H", "P", "T", "U"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackActiveAliasSignals", {}).get("current") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackActiveAliasSignals", {}).get("aliasToken") in {"FLAG OFF", "CBGCIA:H", "CBGCIA:P", "CBGCIA:T", "CBGCIA:U"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackLegendCompactAlias") in {"FLAG OFF", "CBGCIL:HPTU"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackLegendCompactAliasSignals", {}).keys()) == {"flagName", "flagEnabled", "alias", "aliasToken"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackLegendCompactAliasSignals", {}).get("alias") == "HPTU", payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackLegendCompactAliasSignals", {}).get("aliasToken") == "CBGCIL:HPTU", payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).keys()) == {"map", "current", "confidence", "intentCueMap", "intentCue", "intentTonePackMap", "intentTonePack", "flagName", "flagEnabled"}, payload
        intent_cue_map = payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("intentCueMap")
        assert isinstance(intent_cue_map, dict), payload
        assert set(intent_cue_map.keys()) == {"steady", "swing", "spike", "unknown"}, payload
        assert set(intent_cue_map.values()) == {"H", "P", "T", "U"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("intentCue") == payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentCue"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("current") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("current") in intent_cue_map, payload
        assert intent_cue_map[payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("current")] == payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentCue"), payload
        active_alias = payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackActiveAlias")
        active_alias_signals = payload.get("cadenceBridgeGlyphConfidenceNarrativeIntentTonePackActiveAliasSignals", {})
        if active_alias != "FLAG OFF":
            assert active_alias == f"CBGCIA:{payload.get('cadenceBridgeGlyphConfidenceNarrativeIntentCue')}", payload
            assert active_alias_signals.get("aliasToken") == active_alias, payload
        # Contract lock (Cycle GC follow-up): keep deterministic key order and value-domain for
        # intentTonePackMap, then ensure the active `current` narrative selects the coherent tone-pack.
        intent_tone_pack_map = payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("intentTonePackMap")
        assert isinstance(intent_tone_pack_map, dict), payload
        assert list(intent_tone_pack_map.keys()) == ["steady", "swing", "spike", "unknown"], payload
        assert set(intent_tone_pack_map.values()) == {"hold|anchor", "prep|brace", "triage|stabilize"}, payload
        assert intent_tone_pack_map["steady"] == "hold|anchor", payload
        assert intent_tone_pack_map["swing"] == "prep|brace", payload
        assert intent_tone_pack_map["spike"] == "triage|stabilize", payload
        assert intent_tone_pack_map["unknown"] == "hold|anchor", payload
        current_narrative = payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("current")
        current_tone_pack = payload.get("cadenceBridgeGlyphConfidenceNarrativeSignals", {}).get("intentTonePack")
        assert current_narrative in intent_tone_pack_map, payload
        assert current_tone_pack == intent_tone_pack_map[current_narrative], payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulse") in {
            "CBGC FX PULSE:SOFT",
            "CBGC FX PULSE:EDGE",
            "CBGC FX PULSE:HARD",
        }, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).keys()) == {
            "intentCue",
            "narrative",
            "confidence",
            "volatilityRegime",
            "priorVolatilityRegime",
            "priorResolvedPulse",
            "priorExpectedPulse",
            "priorLoaded",
            "map",
            "expectedPulse",
            "resolvedPulse",
            "disagreement",
            "disagreementStreak",
            "adaptiveStepThreshold",
            "aggressivenessMode",
            "hysteresisApplied",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("intentCue") in {"H", "P", "T", "U"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("narrative") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("confidence") in {"LOW", "MID", "HIGH", "UNKNOWN"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("volatilityRegime") in {"CALM", "SWING", "SPIKE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("priorVolatilityRegime") in {"CALM", "SWING", "SPIKE", "UNKNOWN"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("priorResolvedPulse") in {"SOFT", "EDGE", "HARD", "UNKNOWN"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("priorExpectedPulse") in {"SOFT", "EDGE", "HARD", "UNKNOWN"}, payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("priorLoaded"), bool), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("expectedPulse") in {"SOFT", "EDGE", "HARD"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("resolvedPulse") in {"SOFT", "EDGE", "HARD"}, payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("disagreement"), bool), payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("disagreementStreak"), int), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("adaptiveStepThreshold") in {1, 2}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("aggressivenessMode") in {"CAUTIOUS", "BASELINE", "AGGRESSIVE"}, payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("hysteresisApplied"), bool), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("reason") in {
            "regime-map-base",
            "volatility-memory-adaptive-step-clamp",
            "volatility-memory-stable",
            "volatility-memory-disagreement-escalation",
        }, payload
        fx_pulse_map = payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("map")
        assert isinstance(fx_pulse_map, dict), payload
        assert set(fx_pulse_map.keys()) == {"H", "P", "T", "U"}, payload
        assert set(fx_pulse_map.values()) == {"SOFT", "EDGE", "HARD"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseSignals", {}).get("offlineOnly") is True, payload
        expected_fx_pulse = f"CBGC FX PULSE:{payload.get('cadenceBridgeGlyphConfidenceFxPulseSignals', {}).get('resolvedPulse')}"
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulse") == expected_fx_pulse, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseRegimeAlias") in {"FLAG OFF", "CBGCFXR:C", "CBGCFXR:S", "CBGCFXR:P"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseRegimeAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "volatilityRegime",
            "alias",
            "aliasToken",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseRegimeAliasSignals", {}).get("volatilityRegime") in {"CALM", "SWING", "SPIKE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseRegimeAliasSignals", {}).get("alias") in {"C", "S", "P"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseRegimeAliasSignals", {}).get("aliasToken") in {"CBGCFXR:C", "CBGCFXR:S", "CBGCFXR:P"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseAggressivenessAlias") in {"FLAG OFF", "CBGCFXA:C", "CBGCFXA:B", "CBGCFXA:A"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseAggressivenessAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "aggressivenessMode",
            "alias",
            "aliasToken",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseAggressivenessAliasSignals", {}).get("aggressivenessMode") in {"CAUTIOUS", "BASELINE", "AGGRESSIVE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseAggressivenessAliasSignals", {}).get("alias") in {"C", "B", "A"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseAggressivenessAliasSignals", {}).get("aliasToken") in {"CBGCFXA:C", "CBGCFXA:B", "CBGCFXA:A"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHint", "").startswith(("FLAG OFF", "CBGC FX HINT:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "aggressivenessMode",
            "resolvedPulse",
            "narrativeCurrent",
            "worldToneCue",
            "worldToneVariantPack",
            "hint",
            "aliasToken",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).get("aggressivenessMode") in {"CAUTIOUS", "BASELINE", "AGGRESSIVE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).get("resolvedPulse") in {"SOFT", "EDGE", "HARD"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).get("narrativeCurrent") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).get("worldToneCue") in {"calm skyline", "faultline jitter", "breachfront surge", "neutral field"}, payload
        variant_pack = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).get("worldToneVariantPack")
        assert isinstance(variant_pack, dict), payload
        assert set(variant_pack.keys()) == {"CAUTIOUS", "BASELINE", "AGGRESSIVE"}, payload
        for mode_key, mode_pack in variant_pack.items():
            assert isinstance(mode_pack, dict), payload
            assert set(mode_pack.keys()) == {"steady", "swing", "spike", "unknown"}, payload
            for entry in mode_pack.values():
                assert isinstance(entry, str) and entry.strip(), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).get("aliasToken", "").startswith("CBGC FX HINT:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintCompactAlias") in {"FLAG OFF", "CBGCFXH:W", "CBGCFXH:T", "CBGCFXH:P"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "aggressivenessMode",
            "alias",
            "aliasToken",
            "sourceToken",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintCompactAliasSignals", {}).get("aggressivenessMode") in {"CAUTIOUS", "BASELINE", "AGGRESSIVE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintCompactAliasSignals", {}).get("alias") in {"W", "T", "P"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintCompactAliasSignals", {}).get("aliasToken") in {"CBGCFXH:W", "CBGCFXH:T", "CBGCFXH:P"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintCompactAliasSignals", {}).get("sourceToken", "").startswith("CBGC FX HINT:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyHintCompactAliasSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAlias") in {"FLAG OFF", "CBGCFXW:S", "CBGCFXW:J", "CBGCFXW:B", "CBGCFXW:N"}, payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "narrativeCurrent",
            "worldToneCue",
            "alias",
            "aliasToken",
            "sourceToken",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAliasSignals", {}).get("narrativeCurrent") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAliasSignals", {}).get("worldToneCue") in {"calm skyline", "faultline jitter", "breachfront surge", "neutral field"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAliasSignals", {}).get("alias") in {"S", "J", "B", "N"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAliasSignals", {}).get("aliasToken") in {"CBGCFXW:S", "CBGCFXW:J", "CBGCFXW:B", "CBGCFXW:N"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAliasSignals", {}).get("sourceToken", "").startswith("CBGC FX HINT:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneAliasSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneLegend", "").startswith(("FLAG OFF", "CBGCFXW LEGEND:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneLegendSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "legend",
            "aliasMap",
            "narrativeCurrent",
            "activeAlias",
            "sourceToken",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneLegendSignals", {}).get("activeAlias") in {"S", "J", "B", "N"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneLegendSignals", {}).get("sourceToken") in {"CBGCFXW:S", "CBGCFXW:J", "CBGCFXW:B", "CBGCFXW:N"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneLegendSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDrift", "").startswith(("FLAG OFF", "CBGCFXW DRIFT:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDriftSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "currentAlias",
            "priorAlias",
            "priorLoaded",
            "shifted",
            "driftToken",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDriftSignals", {}).get("currentAlias") in {"S", "J", "B", "N"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDriftSignals", {}).get("priorAlias") in {"S", "J", "B", "N"}, payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDriftSignals", {}).get("priorLoaded"), bool), payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDriftSignals", {}).get("shifted"), bool), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDriftSignals", {}).get("driftToken", "").startswith("CBGCFXW DRIFT:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneDriftSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherence", "").startswith(("FLAG OFF", "CBGCFXW COHERENCE:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "status",
            "narrativeCurrent",
            "aggressivenessMode",
            "expectedAggressivenessMode",
            "isUnknownNarrative",
            "coherent",
            "priorStatus",
            "priorLoaded",
            "driftStreak",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("status") in {"OK", "DRIFT"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("narrativeCurrent") in {"steady", "swing", "spike", "unknown"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("aggressivenessMode") in {"CAUTIOUS", "BASELINE", "AGGRESSIVE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("expectedAggressivenessMode") in {"CAUTIOUS", "BASELINE", "AGGRESSIVE"}, payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("coherent"), bool), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("priorStatus") in {"OK", "DRIFT"}, payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("priorLoaded"), bool), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("driftStreak") in {0, 1, 2}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("token", "").startswith("CBGCFXW COHERENCE:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentum", "").startswith(("FLAG OFF", "CBGCFXW COHERENCE MOMENTUM:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "momentum",
            "currentStatus",
            "priorStatus",
            "currentDriftStreak",
            "priorDriftStreak",
            "driftStreakDelta",
            "priorLoaded",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("momentum") in {"STABLE", "WOBBLE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("currentStatus") in {"OK", "DRIFT"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("priorStatus") in {"OK", "DRIFT"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("currentDriftStreak") in {0, 1, 2}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("priorDriftStreak") in {0, 1, 2}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("driftStreakDelta") in {-2, -1, 0, 1, 2}, payload
        assert isinstance(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("priorLoaded"), bool), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("token", "").startswith("CBGCFXW COHERENCE MOMENTUM:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumAlias", "").startswith(("FLAG OFF", "CBGCFXWM:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "momentum",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumAliasSignals", {}).get("momentum") in {"STABLE", "WOBBLE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumAliasSignals", {}).get("alias") in {"S", "W"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumAliasSignals", {}).get("token", "").startswith("CBGCFXWM:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceMomentumAliasSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArc", "").startswith(("FLAG OFF", "COHERENCE ARC:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "status",
            "driftStreak",
            "momentum",
            "arcSource",
            "arc",
            "token",
            "reason",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("status") in {"OK", "DRIFT"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("driftStreak") in {0, 1, 2}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("momentum") in {"STABLE", "WOBBLE"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("arcSource") in {"fresh", "stale"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("arc") in {"LOCK", "SWAY"}, payload
        if payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("arcSource") == "stale":
            assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("arc") == "LOCK", payload
            assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("reason") == "stale-prior-guard-lock", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("token", "").startswith("COHERENCE ARC:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcAlias", "").startswith(("FLAG OFF", "CVARC:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "arc",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcAliasSignals", {}).get("arc") in {"LOCK", "SWAY"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcAliasSignals", {}).get("alias") in {"L", "S"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcAliasSignals", {}).get("token", "").startswith("CVARC:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcAliasSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePair", "").startswith(("FLAG OFF", "COHERENCE ARC COACH:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "arc",
            "selected",
            "pair",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("arc") in {"LOCK", "SWAY"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("token", "").startswith("COHERENCE ARC COACH:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("pair", {}).get("LOCK", "").startswith("LOCK:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("pair", {}).get("SWAY", "").startswith("SWAY:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("selected") in {
            payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("pair", {}).get("LOCK"),
            payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("pair", {}).get("SWAY"),
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolinePairSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAlias", "").startswith(("FLAG OFF", "CBGCFXWAC:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "arc",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasSignals", {}).get("arc") in {"LOCK", "SWAY"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasSignals", {}).get("alias") in {"L", "S"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasSignals", {}).get("token", "").startswith("CBGCFXWAC:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasSignals", {}).get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasDrift", "").startswith(("FLAG OFF", "CBGCFXWAC DRIFT:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasDriftSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "currentAlias",
            "priorAlias",
            "priorLoaded",
            "stalePriorGuard",
            "shifted",
            "token",
            "offlineOnly",
        }, payload
        drift_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasDriftSignals", {})
        assert drift_signals.get("currentAlias") in {"L", "S"}, payload
        assert drift_signals.get("priorAlias") in {"L", "S"}, payload
        assert drift_signals.get("token", "").startswith("CBGCFXWAC DRIFT:"), payload
        if drift_signals.get("stalePriorGuard"):
            assert drift_signals.get("priorAlias") == drift_signals.get("currentAlias"), payload
            assert drift_signals.get("priorLoaded") is False, payload
        assert drift_signals.get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasMomentum", "").startswith(("FLAG OFF", "CBGCFXWAC MOMENTUM:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasMomentumSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "momentum",
            "shifted",
            "priorLoaded",
            "stalePriorGuard",
            "reason",
            "token",
            "offlineOnly",
        }, payload
        momentum_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachMicrolineAliasMomentumSignals", {})
        assert momentum_signals.get("momentum") in {"LOCKED", "WOBBLE"}, payload
        assert momentum_signals.get("token", "").startswith("CBGCFXWAC MOMENTUM:"), payload
        assert momentum_signals.get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeat", "").startswith(("FLAG OFF", "CBGCFXWSB:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "worldToneAlias",
            "coherenceMomentum",
            "coherenceAlias",
            "coachMomentum",
            "coachAlias",
            "storybeat",
            "token",
            "offlineOnly",
        }, payload
        storybeat_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatSignals", {})
        assert storybeat_signals.get("worldToneAlias") in {"S", "J", "B", "N"}, payload
        assert storybeat_signals.get("coherenceMomentum") in {"STABLE", "WOBBLE"}, payload
        assert storybeat_signals.get("coachMomentum") in {"LOCKED", "WOBBLE"}, payload
        assert storybeat_signals.get("storybeat", "").strip(), payload
        assert storybeat_signals.get("token", "").startswith("CBGCFXWSB:"), payload
        assert storybeat_signals.get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhase", "").startswith(("FLAG OFF", "CBGCFXWSBP:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "phase",
            "alias",
            "coherenceMomentum",
            "coachMomentum",
            "token",
            "offlineOnly",
        }, payload
        storybeat_phase_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseSignals", {})
        assert storybeat_phase_signals.get("phase") in {"CALM", "TENSE"}, payload
        assert storybeat_phase_signals.get("alias") in {"C", "T"}, payload
        assert storybeat_phase_signals.get("coherenceMomentum") in {"STABLE", "WOBBLE"}, payload
        assert storybeat_phase_signals.get("coachMomentum") in {"LOCKED", "WOBBLE"}, payload
        assert storybeat_phase_signals.get("token", "").startswith("CBGCFXWSBP:"), payload
        assert storybeat_phase_signals.get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCue", "").startswith(("FLAG OFF", "CBGCFXWSBP FX CUE:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "phase",
            "cue",
            "reason",
            "token",
            "offlineOnly",
        }, payload
        storybeat_phase_fx_cue_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueSignals", {})
        assert storybeat_phase_fx_cue_signals.get("phase") in {"CALM", "TENSE"}, payload
        assert storybeat_phase_fx_cue_signals.get("cue") in {"SOFT", "EDGE"}, payload
        assert storybeat_phase_fx_cue_signals.get("reason") in {"calm-phase", "tense-phase"}, payload
        assert storybeat_phase_fx_cue_signals.get("token", "").startswith("CBGCFXWSBP FX CUE:"), payload
        assert storybeat_phase_fx_cue_signals.get("offlineOnly") is True, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAlias", "").startswith(("FLAG OFF", "CBGCFXWSBPFC:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "cue",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        storybeat_phase_fx_cue_compact_alias = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAlias", "")
        storybeat_phase_fx_cue_compact_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasSignals", {})
        assert storybeat_phase_fx_cue_compact_alias_signals.get("cue") in {"SOFT", "EDGE"}, payload
        assert storybeat_phase_fx_cue_compact_alias_signals.get("alias") in {"S", "E"}, payload
        assert storybeat_phase_fx_cue_compact_alias_signals.get("token", "").startswith("CBGCFXWSBPFC:"), payload
        assert storybeat_phase_fx_cue_compact_alias_signals.get("offlineOnly") is True, payload
        cue_alias_map = {
            "SOFT": "S",
            "EDGE": "E",
        }
        expected_alias = cue_alias_map[storybeat_phase_fx_cue_compact_alias_signals["cue"]]
        assert storybeat_phase_fx_cue_compact_alias_signals.get("alias") == expected_alias, payload
        assert storybeat_phase_fx_cue_compact_alias_signals.get("token") == f"CBGCFXWSBPFC:{expected_alias}", payload
        if storybeat_phase_fx_cue_compact_alias_signals.get("flagEnabled") is True:
            assert storybeat_phase_fx_cue_compact_alias == f"CBGCFXWSBPFC:{expected_alias}", payload
        else:
            assert storybeat_phase_fx_cue_compact_alias == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensity", "").startswith(("FLAG OFF", "CBGCFXWSBPFCI:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensitySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "alias",
            "intensity",
            "compactAlias",
            "token",
            "offlineOnly",
        }, payload
        storybeat_phase_fx_cue_compact_alias_intensity = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensity", "")
        storybeat_phase_fx_cue_compact_alias_intensity_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensitySignals", {})
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("alias") in {"S", "E"}, payload
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("intensity") in {"BASE", "RAISED"}, payload
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("compactAlias") in {"B", "R"}, payload
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("token", "").startswith("CBGCFXWSBPFCI:"), payload
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("offlineOnly") is True, payload
        expected_intensity_by_alias = {"S": ("BASE", "B"), "E": ("RAISED", "R")}
        expected_intensity, expected_intensity_compact_alias = expected_intensity_by_alias[storybeat_phase_fx_cue_compact_alias_intensity_signals["alias"]]
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("intensity") == expected_intensity, payload
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("compactAlias") == expected_intensity_compact_alias, payload
        assert storybeat_phase_fx_cue_compact_alias_intensity_signals.get("token") == f"CBGCFXWSBPFCI:{expected_intensity_compact_alias}", payload
        if storybeat_phase_fx_cue_compact_alias_intensity_signals.get("flagEnabled") is True:
            assert storybeat_phase_fx_cue_compact_alias_intensity == f"CBGCFXWSBPFCI:{expected_intensity_compact_alias}", payload
        else:
            assert storybeat_phase_fx_cue_compact_alias_intensity == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityPulseAlias", "").startswith(("FLAG OFF", "CBGCFXWSBPFXP:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityPulseAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "intensity",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_alias = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityPulseAlias", "")
        intensity_pulse_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityPulseAliasSignals", {})
        assert intensity_pulse_alias_signals.get("intensity") in {"BASE", "RAISED"}, payload
        assert intensity_pulse_alias_signals.get("alias") in {"S", "P"}, payload
        assert intensity_pulse_alias_signals.get("token", "").startswith("CBGCFXWSBPFXP:"), payload
        assert intensity_pulse_alias_signals.get("offlineOnly") is True, payload
        expected_pulse_alias = "P" if expected_intensity == "RAISED" else "S"
        assert intensity_pulse_alias_signals.get("intensity") == expected_intensity, payload
        assert intensity_pulse_alias_signals.get("alias") == expected_pulse_alias, payload
        assert intensity_pulse_alias_signals.get("token") == f"CBGCFXWSBPFXP:{expected_pulse_alias}", payload
        if intensity_pulse_alias_signals.get("flagEnabled") is True:
            assert intensity_pulse_alias == f"CBGCFXWSBPFXP:{expected_pulse_alias}", payload
        else:
            assert intensity_pulse_alias == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPack", "").startswith(("FLAG OFF", "CBGCFXWSBPFXP LANG:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "storybeatPhase",
            "phaseIntent",
            "pulseAlias",
            "selectedMode",
            "compactAlias",
            "selected",
            "pair",
            "dosReadabilityRowBudgetThreshold",
            "dosRowBudgetWithinThreshold",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPack", "")
        intensity_pulse_language_variant_pack_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackSignals", {})
        assert intensity_pulse_language_variant_pack_signals.get("storybeatPhase") in {"CALM", "TENSE"}, payload
        assert intensity_pulse_language_variant_pack_signals.get("phaseIntent") in {"ANCHOR", "SURGE"}, payload
        assert intensity_pulse_language_variant_pack_signals.get("pulseAlias") in {"S", "P"}, payload
        assert intensity_pulse_language_variant_pack_signals.get("selectedMode") in {"SOFT", "PUSH"}, payload
        assert intensity_pulse_language_variant_pack_signals.get("compactAlias") in {"S", "P"}, payload
        assert isinstance(intensity_pulse_language_variant_pack_signals.get("selected"), str) and intensity_pulse_language_variant_pack_signals.get("selected"), payload
        pair = intensity_pulse_language_variant_pack_signals.get("pair")
        assert isinstance(pair, dict) and set(pair.keys()) == {"SOFT", "PUSH"}, payload
        assert all(isinstance(v, dict) and set(v.keys()) == {"CALM", "TENSE"} for v in pair.values()), payload
        assert intensity_pulse_language_variant_pack_signals.get("offlineOnly") is True, payload
        expected_mode = "PUSH" if expected_pulse_alias == "P" else "SOFT"
        assert intensity_pulse_language_variant_pack_signals.get("pulseAlias") == expected_pulse_alias, payload
        assert intensity_pulse_language_variant_pack_signals.get("selectedMode") == expected_mode, payload
        assert intensity_pulse_language_variant_pack_signals.get("compactAlias") == ("P" if expected_mode == "PUSH" else "S"), payload
        expected_phase = storybeat_phase_fx_cue_signals.get("phase")
        assert intensity_pulse_language_variant_pack_signals.get("storybeatPhase") == expected_phase, payload
        expected_phase_intent = {"CALM": "ANCHOR", "TENSE": "SURGE"}[expected_phase]
        assert intensity_pulse_language_variant_pack_signals.get("phaseIntent") == expected_phase_intent, payload
        expected_selected = pair[expected_mode][expected_phase]
        assert intensity_pulse_language_variant_pack_signals.get("selected") == expected_selected, payload
        expected_compact_token = f"CBGCFXWSBPFXP LANG:{'P' if expected_mode == 'PUSH' else 'S'}"
        expected_fallback_token = f"CBGCFXWSBPFXP LANG:{expected_mode}"
        expected_budget_gate = len(expected_compact_token) <= intensity_pulse_language_variant_pack_signals.get("dosReadabilityRowBudgetThreshold")
        assert intensity_pulse_language_variant_pack_signals.get("dosRowBudgetWithinThreshold") == expected_budget_gate, payload
        expected_variant_pack_token = expected_compact_token if expected_budget_gate else expected_fallback_token
        assert intensity_pulse_language_variant_pack_signals.get("token") == expected_variant_pack_token, payload
        if intensity_pulse_language_variant_pack_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack == expected_variant_pack_token, payload
        else:
            assert intensity_pulse_language_variant_pack == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentAlias", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPI:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "phaseIntent",
            "alias",
            "phaseIntentLegendVersion",
            "phaseIntentLegendHash",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_alias = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentAlias", "")
        intensity_pulse_language_variant_pack_phase_intent_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentAliasSignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("phaseIntent") in {"ANCHOR", "SURGE", "RECOVER"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("alias") in {"A", "S", "R"}, payload
        expected_phase_intent_legend_hash = hashlib.sha256(
            json.dumps({"A": "ANCHOR", "R": "RECOVER", "S": "SURGE"}, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:12]
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("phaseIntentLegendVersion") == "v1", payload
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("phaseIntentLegendHash") == expected_phase_intent_legend_hash, payload
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("offlineOnly") is True, payload
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("phaseIntent") == expected_phase_intent, payload
        expected_phase_intent_alias = "A" if expected_phase_intent == "ANCHOR" else "S"
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("alias") == expected_phase_intent_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("token") == f"CBGCFXWSBPFXPI:{expected_phase_intent_alias}", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentAliasLegendVersion") == intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("phaseIntentLegendVersion"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentAliasLegendHash") == intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("phaseIntentLegendHash"), payload
        if intensity_pulse_language_variant_pack_phase_intent_alias_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_alias == f"CBGCFXWSBPFXPI:{expected_phase_intent_alias}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_alias == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariant", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPI LEGEND COPY:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariantSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "phaseIntent",
            "alias",
            "legendCopy",
            "phaseIntentLegendCopyHash",
            "dosWidthMax",
            "withinDosWidth",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariant", "")
        intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariantSignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("phaseIntent") in {"ANCHOR", "SURGE", "RECOVER"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("alias") in {"A", "S", "R"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("offlineOnly") is True, payload
        assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("phaseIntent") == expected_phase_intent, payload
        assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("alias") == expected_phase_intent_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("token").startswith("CBGCFXWSBPFXPI LEGEND COPY:"), payload
        emitted_legend_copy = intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("token", "").split(":", 1)[1].strip()
        expected_phase_intent_legend_copy_hash = hashlib.sha256(emitted_legend_copy.encode("utf-8")).hexdigest()[:12]
        assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("phaseIntentLegendCopyHash") == expected_phase_intent_legend_copy_hash, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariantCopyHash") == expected_phase_intent_legend_copy_hash, payload
        assert isinstance(intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("withinDosWidth"), bool), payload
        assert isinstance(intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("dosWidthMax"), int), payload
        if intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant.startswith("CBGCFXWSBPFXPI LEGEND COPY:"), payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_legend_microcopy_variant == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariantCompactAlias", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPIC:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariantCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "style",
            "alias",
            "withinDosWidth",
            "token",
            "offlineOnly",
        }, payload
        legend_copy_compact_alias = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariantCompactAlias", "")
        legend_copy_compact_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentLegendMicrocopyVariantCompactAliasSignals", {})
        assert legend_copy_compact_alias_signals.get("style") in {"WRITER", "COMPACT"}, payload
        assert legend_copy_compact_alias_signals.get("alias") in {"W", "C"}, payload
        assert legend_copy_compact_alias_signals.get("offlineOnly") is True, payload
        expected_legend_copy_alias = "W" if legend_copy_compact_alias_signals.get("withinDosWidth") is True else "C"
        assert legend_copy_compact_alias_signals.get("alias") == expected_legend_copy_alias, payload
        assert legend_copy_compact_alias_signals.get("token") == f"CBGCFXWSBPFXPIC:{expected_legend_copy_alias}", payload
        if legend_copy_compact_alias_signals.get("flagEnabled") is True:
            assert legend_copy_compact_alias == f"CBGCFXWSBPFXPIC:{expected_legend_copy_alias}", payload
        else:
            assert legend_copy_compact_alias == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarration", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPI NARR:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "phaseIntent",
            "pulseAlias",
            "coachMomentum",
            "narration",
            "reason",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_narration = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarration", "")
        intensity_pulse_language_variant_pack_phase_intent_narration_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationSignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("phaseIntent") in {"ANCHOR", "SURGE", "RECOVER"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("pulseAlias") in {"S", "P"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("coachMomentum") in {"LOCKED", "WOBBLE"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("narration") in {"ANCHOR", "SURGE", "RECOVER"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("offlineOnly") is True, payload
        expected_narration = "SURGE" if expected_phase_intent == "SURGE" else "ANCHOR"
        if expected_phase_intent == "ANCHOR" and intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("coachMomentum") == "WOBBLE":
            expected_narration = "RECOVER"
        assert intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("narration") == expected_narration, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("token") == f"CBGCFXWSBPFXPI NARR:{expected_narration}", payload
        if intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_narration == f"CBGCFXWSBPFXPI NARR:{expected_narration}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_narration == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAlias", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPIN:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "narration",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAlias", "")
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasSignals", {})
        expected_narration_alias = {"ANCHOR": "A", "SURGE": "S", "RECOVER": "R"}[expected_narration]
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_signals.get("narration") == expected_narration, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_signals.get("alias") == expected_narration_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_signals.get("token") == f"CBGCFXWSBPFXPIN:{expected_narration_alias}", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_signals.get("offlineOnly") is True, payload
        if intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias == f"CBGCFXWSBPFXPIN:{expected_narration_alias}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasDrift", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPIN DRIFT:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasDriftSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "phaseIntent",
            "phaseAlias",
            "expectedPhaseAlias",
            "narration",
            "narrationAlias",
            "expectedNarrationAlias",
            "coachMomentum",
            "phaseAliasParity",
            "narrationAliasParity",
            "narrationPhaseAliasParity",
            "cue",
            "reason",
            "token",
            "offlineOnly",
            "runtimeBalanceImpact",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasDrift", "")
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasDriftSignals", {})
        expected_parity = expected_phase_intent_alias == expected_narration_alias
        expected_drift_cue = "WATCH" if (intensity_pulse_language_variant_pack_phase_intent_narration_signals.get("coachMomentum") == "WOBBLE" and not expected_parity) else "LOCK"
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("phaseIntent") == expected_phase_intent, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("phaseAlias") == expected_phase_intent_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("expectedPhaseAlias") == expected_phase_intent_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("narration") == expected_narration, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("narrationAlias") == expected_narration_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("expectedNarrationAlias") == expected_narration_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("coachMomentum") in {"LOCKED", "WOBBLE"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("phaseAliasParity") is True, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("narrationAliasParity") is True, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("narrationPhaseAliasParity") == expected_parity, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("cue") == expected_drift_cue, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("reason") in {"wobble-parity-drift", "parity-locked"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("token") == f"CBGCFXWSBPFXPIN DRIFT:{expected_drift_cue}", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("runtimeBalanceImpact") == "none", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("offlineOnly") is True, payload
        if intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift == f"CBGCFXWSBPFXPIN DRIFT:{expected_drift_cue}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_drift == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCue", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPINF:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "narration",
            "alias",
            "cue",
            "cueMap",
            "tokenAlias",
            "token",
            "adjacencyInvariant",
            "adjacencyChain",
            "runtimeBalanceImpact",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCue", "")
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueSignals", {})
        expected_narration_cue = {"A": "SOFT", "R": "EDGE", "S": "HARD"}[expected_narration_alias]
        expected_narration_cue_alias = {"SOFT": "S", "EDGE": "E", "HARD": "H"}[expected_narration_cue]
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("narration") == expected_narration, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("alias") == expected_narration_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("cue") == expected_narration_cue, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("tokenAlias") == expected_narration_cue_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("token") == f"CBGCFXWSBPFXPINF:{expected_narration_cue_alias}", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("adjacencyInvariant") == "preserved", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("adjacencyChain") == "CBGCFXWSBPFXPIN->CBGCFXWSBPFXPIN LEGEND->CBGCFXWSBPFXPINF->CBGCFXWSBPFXPINF LEGEND", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("runtimeBalanceImpact") == "none", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("offlineOnly") is True, payload
        if intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue == f"CBGCFXWSBPFXPINF:{expected_narration_cue_alias}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueOrder", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPINF ORDER:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueOrderSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "alias",
            "cueOrder",
            "order",
            "token",
            "adjacencyInvariant",
            "adjacencyChain",
            "offlineOnly",
            "runtimeBalanceImpact",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueOrder", "")
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueOrderSignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals.get("alias") == expected_narration_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals.get("order") in {"anchor-handoff", "surge-handoff", "recover-handoff"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals.get("token") == f"CBGCFXWSBPFXPINF ORDER:{expected_narration_alias}", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals.get("adjacencyInvariant") == "preserved", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals.get("adjacencyChain") == "CBGCFXWSBPFXPINF LEGEND->CBGCFXWSBPFXPINF ORDER->CBGCFXWSBPFXPI DRILL", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals.get("offlineOnly") is True, payload
        if intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order == f"CBGCFXWSBPFXPINF ORDER:{expected_narration_alias}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueBurst", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPINF BURST:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueBurstSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "cue",
            "driftCue",
            "burst",
            "alias",
            "token",
            "adjacencyInvariant",
            "adjacencyChain",
            "offlineOnly",
            "runtimeBalanceImpact",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueBurst", "")
        intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentNarrationCompactAliasCombatVfxFxCueBurstSignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("cue") == expected_narration_cue, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("driftCue") == expected_drift_cue, payload
        expected_burst_alias = "B" if (expected_narration_cue == "HARD" or (expected_narration_cue == "EDGE" and expected_drift_cue == "WATCH")) else "Q"
        expected_burst = "BURST" if expected_burst_alias == "B" else "QUIET"
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("alias") == expected_burst_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("burst") == expected_burst, payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("token") == f"CBGCFXWSBPFXPINF BURST:{expected_burst_alias}", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("adjacencyInvariant") == "preserved", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("adjacencyChain") == "CBGCFXWSBPFXPINF->CBGCFXWSBPFXPINF BURST->CBGCFXWSBPFXPINF ORDER", payload
        assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("offlineOnly") is True, payload
        if intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst == f"CBGCFXWSBPFXPINF BURST:{expected_burst_alias}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_burst == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHint", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPI DRILL:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "phaseIntent",
            "phaseIntentAlias",
            "drillCue",
            "rehearsalHint",
            "reason",
            "runtimeBalanceImpact",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHint", "")
        intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintSignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("phaseIntent") in {"ANCHOR", "SURGE"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("phaseIntentAlias") in {"A", "S"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("drillCue") in {"SOFT", "SURGE"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("rehearsalHint") in {"SOFT drill", "SURGE drill"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("runtimeBalanceImpact") == "none", payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("offlineOnly") is True, payload
        expected_drill_cue = "SURGE" if expected_phase_intent_alias == "S" else "SOFT"
        expected_drill_hint = f"{expected_drill_cue} drill"
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("phaseIntent") == expected_phase_intent, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("phaseIntentAlias") == expected_phase_intent_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("drillCue") == expected_drill_cue, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("rehearsalHint") == expected_drill_hint, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("token") == f"CBGCFXWSBPFXPI DRILL:{expected_drill_cue}", payload
        if intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint == f"CBGCFXWSBPFXPI DRILL:{expected_drill_cue}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAlias", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPD:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "drillCue",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAlias", "")
        intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasSignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals.get("drillCue") in {"SOFT", "SURGE"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals.get("alias") in {"S", "U"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals.get("offlineOnly") is True, payload
        expected_drill_alias = "U" if expected_drill_cue == "SURGE" else "S"
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals.get("drillCue") == expected_drill_cue, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals.get("alias") == expected_drill_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals.get("token") == f"CBGCFXWSBPFXPD:{expected_drill_alias}", payload
        if intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias == f"CBGCFXWSBPFXPD:{expected_drill_alias}", payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasMicrolineVocabulary", "").startswith(("FLAG OFF", "CBGCFXWSBPFXPD MICRO:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasMicrolineVocabularySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "alias",
            "pair",
            "selected",
            "legendVersion",
            "legendHash",
            "dosReadabilityRowBudgetThreshold",
            "dosRowBudgetWithinThreshold",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasMicrolineVocabulary", "")
        intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasMicrolineVocabularySignals", {})
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("alias") in {"S", "U"}, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("selected") in {
            "SOFT drill: hold pace and rehearse one stable line.",
            "SURGE drill: tighten cadence and rehearse one urgent verb.",
        }, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("legendVersion") == "v1", payload
        assert isinstance(intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("legendHash"), str) and len(intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("legendHash")) == 12, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("dosReadabilityRowBudgetThreshold") == 56, payload
        assert isinstance(intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("dosRowBudgetWithinThreshold"), bool), payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("offlineOnly") is True, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("alias") == expected_drill_alias, payload
        assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("token", "").startswith("CBGCFXWSBPFXPD MICRO:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasMicrolineVocabularyLegendVersion") == intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("legendVersion"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseLanguageVariantPackPhaseIntentRehearsalHintCompactAliasMicrolineVocabularyLegendHash") == intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("legendHash"), payload
        if intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("flagEnabled") is True:
            assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary == intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_signals.get("token"), payload
        else:
            assert intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseDecodeMicrolinePair", "").startswith(("FLAG OFF", "CBGCFXWSBPFXP MICRO:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseDecodeMicrolinePairSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "pair",
            "selected",
            "alias",
            "legendVersion",
            "legendHash",
            "dosReadabilityRowBudgetThreshold",
            "dosRowBudgetWithinThreshold",
            "token",
            "offlineOnly",
        }, payload
        intensity_pulse_decode_microline_pair_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseDecodeMicrolinePairSignals", {})
        assert intensity_pulse_decode_microline_pair_signals.get("alias") in {"S", "P"}, payload
        assert intensity_pulse_decode_microline_pair_signals.get("selected") in {"SOFT pulse", "PUSH pulse"}, payload
        assert intensity_pulse_decode_microline_pair_signals.get("legendVersion") == "v1", payload
        assert isinstance(intensity_pulse_decode_microline_pair_signals.get("legendHash"), str) and len(intensity_pulse_decode_microline_pair_signals.get("legendHash")) == 12, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseDecodeMicrolinePairLegendVersion") == intensity_pulse_decode_microline_pair_signals.get("legendVersion"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseDecodeMicrolinePairLegendHash") == intensity_pulse_decode_microline_pair_signals.get("legendHash"), payload
        assert intensity_pulse_decode_microline_pair_signals.get("token", "").startswith("CBGCFXWSBPFXP MICRO:"), payload
        assert intensity_pulse_decode_microline_pair_signals.get("offlineOnly") is True, payload
        assert isinstance(intensity_pulse_decode_microline_pair_signals.get("dosReadabilityRowBudgetThreshold"), int), payload
        assert isinstance(intensity_pulse_decode_microline_pair_signals.get("dosRowBudgetWithinThreshold"), bool), payload
        if intensity_pulse_decode_microline_pair_signals.get("flagEnabled") is True:
            assert intensity_pulse_decode_microline_pair_signals.get("alias") == expected_pulse_alias, payload
            assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseDecodeMicrolinePair") == intensity_pulse_decode_microline_pair_signals.get("token"), payload
        else:
            assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueIntensityPulseDecodeMicrolinePair") == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityCoachMicrolinePair", "").startswith(("FLAG OFF", "CBGCFXWSBPFCI COACH COPY:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityCoachMicrolinePairSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "intensity",
            "compactAlias",
            "dosReadabilityRowBudgetThreshold",
            "dosRowBudgetWithinThreshold",
            "selected",
            "pair",
            "token",
            "offlineOnly",
        }, payload
        intensity_coach_microline_pair_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityCoachMicrolinePairSignals", {})
        assert intensity_coach_microline_pair_signals.get("intensity") in {"BASE", "RAISED"}, payload
        assert isinstance(intensity_coach_microline_pair_signals.get("selected"), str) and intensity_coach_microline_pair_signals.get("selected"), payload
        intensity_pair = intensity_coach_microline_pair_signals.get("pair")
        assert isinstance(intensity_pair, dict), payload
        assert set(intensity_pair.keys()) == {"BASE", "RAISED"}, payload
        assert all(isinstance(v, str) and v for v in intensity_pair.values()), payload
        assert intensity_coach_microline_pair_signals.get("token", "").startswith("CBGCFXWSBPFCI COACH COPY:"), payload
        assert intensity_coach_microline_pair_signals.get("offlineOnly") is True, payload
        expected_intensity_state = storybeat_phase_fx_cue_compact_alias_intensity_signals.get("intensity")
        assert intensity_coach_microline_pair_signals.get("intensity") == expected_intensity_state, payload
        expected_compact_alias = "R" if expected_intensity_state == "RAISED" else "B"
        assert intensity_coach_microline_pair_signals.get("compactAlias") == expected_compact_alias, payload
        assert isinstance(intensity_coach_microline_pair_signals.get("dosReadabilityRowBudgetThreshold"), int), payload
        assert intensity_coach_microline_pair_signals.get("dosReadabilityRowBudgetThreshold") > 0, payload
        assert intensity_coach_microline_pair_signals.get("dosRowBudgetWithinThreshold") in {True, False}, payload
        expected_selected_line = intensity_pair[expected_intensity_state]
        assert intensity_coach_microline_pair_signals.get("selected") == expected_selected_line, payload
        expected_compact_token = f"CBGCFXWSBPFCI COACH COPY:{expected_compact_alias}"
        expected_fallback_token = f"CBGCFXWSBPFCI COACH COPY:{expected_intensity_state}"
        expected_budget_gate = len(expected_compact_token) <= intensity_coach_microline_pair_signals.get("dosReadabilityRowBudgetThreshold")
        assert intensity_coach_microline_pair_signals.get("dosRowBudgetWithinThreshold") == expected_budget_gate, payload
        expected_intensity_token = expected_compact_token if intensity_coach_microline_pair_signals.get("dosRowBudgetWithinThreshold") is True else expected_fallback_token
        assert intensity_coach_microline_pair_signals.get("token") == expected_intensity_token, payload
        intensity_coach_microline_pair_token = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseFxCueCompactAliasIntensityCoachMicrolinePair", "")
        if intensity_coach_microline_pair_signals.get("flagEnabled") is True:
            assert intensity_coach_microline_pair_token == expected_intensity_token, payload
        else:
            assert intensity_coach_microline_pair_token == "FLAG OFF", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendation", "").startswith(("FLAG OFF", "CBGCFXWAC COACH COPY REC:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "arc",
            "momentum",
            "storybeatPhase",
            "intensity",
            "recommendation",
            "reason",
            "reasonPriority",
            "token",
            "offlineOnly",
        }, payload
        coach_copy_rec_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationSignals", {})
        assert coach_copy_rec_signals.get("arc") in {"LOCK", "SWAY"}, payload
        assert coach_copy_rec_signals.get("momentum") in {"LOCKED", "WOBBLE"}, payload
        assert coach_copy_rec_signals.get("storybeatPhase") in {"CALM", "TENSE"}, payload
        assert coach_copy_rec_signals.get("intensity") in {"BASE", "RAISED"}, payload
        assert coach_copy_rec_signals.get("recommendation") in {"ANCHOR_STEP", "SLOW_STEP", "HOLD_STEP"}, payload
        assert coach_copy_rec_signals.get("reason") in {"stable-calm", "tense-phase", "wobble", "raised-intensity"}, payload
        assert coach_copy_rec_signals.get("reasonPriority") in {"P1", "P2", "P3", "P4"}, payload
        assert coach_copy_rec_signals.get("token", "").startswith("CBGCFXWAC COACH COPY REC:"), payload
        assert coach_copy_rec_signals.get("offlineOnly") is True, payload
        expected_reason = "stable-calm"
        expected_recommendation = "HOLD_STEP"
        if coach_copy_rec_signals.get("momentum") == "WOBBLE" and coach_copy_rec_signals.get("arc") == "LOCK":
            expected_recommendation = "ANCHOR_STEP"
            expected_reason = "wobble"
        elif coach_copy_rec_signals.get("storybeatPhase") == "TENSE" and coach_copy_rec_signals.get("arc") == "LOCK":
            expected_recommendation = "ANCHOR_STEP"
            expected_reason = "tense-phase"
        elif coach_copy_rec_signals.get("momentum") == "WOBBLE":
            expected_recommendation = "SLOW_STEP"
            expected_reason = "wobble"
        elif coach_copy_rec_signals.get("storybeatPhase") == "TENSE":
            expected_recommendation = "SLOW_STEP"
            expected_reason = "tense-phase"
        elif coach_copy_rec_signals.get("intensity") == "RAISED":
            expected_recommendation = "SLOW_STEP"
            expected_reason = "raised-intensity"
        assert coach_copy_rec_signals.get("recommendation") == expected_recommendation, payload
        assert coach_copy_rec_signals.get("reason") == expected_reason, payload
        expected_reason_priority = {
            "wobble": "P1",
            "tense-phase": "P2",
            "raised-intensity": "P3",
            "stable-calm": "P4",
        }[expected_reason]
        assert coach_copy_rec_signals.get("reasonPriority") == expected_reason_priority, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationReasonPriorityAlias", "").startswith(("FLAG OFF", "CBGCFXWACRP:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationReasonPriorityAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "reasonPriority",
            "alias",
            "legendVersion",
            "legendHash",
            "legendMap",
            "token",
            "offlineOnly",
        }, payload
        coach_copy_reason_priority_alias_signals = payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationReasonPriorityAliasSignals", {})
        assert coach_copy_reason_priority_alias_signals.get("reasonPriority") in {"P1", "P2", "P3", "P4"}, payload
        assert coach_copy_reason_priority_alias_signals.get("alias") in {"P1", "P2", "P3", "P4"}, payload
        assert coach_copy_reason_priority_alias_signals.get("token", "").startswith("CBGCFXWACRP:"), payload
        assert coach_copy_reason_priority_alias_signals.get("offlineOnly") is True, payload
        assert coach_copy_reason_priority_alias_signals.get("reasonPriority") == coach_copy_rec_signals.get("reasonPriority"), payload
        assert coach_copy_reason_priority_alias_signals.get("alias") == coach_copy_rec_signals.get("reasonPriority"), payload
        expected_reason_priority_legend_map = {
            "P1": "wobble",
            "P2": "tense-phase",
            "P3": "raised-intensity",
            "P4": "stable-calm",
        }
        expected_reason_priority_legend_hash = hashlib.sha256(
            json.dumps(expected_reason_priority_legend_map, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:12]
        assert coach_copy_reason_priority_alias_signals.get("legendVersion") == "v1", payload
        assert coach_copy_reason_priority_alias_signals.get("legendMap") == expected_reason_priority_legend_map, payload
        assert coach_copy_reason_priority_alias_signals.get("legendHash") == expected_reason_priority_legend_hash, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationReasonPriorityAliasLegendVersion") == "v1", payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationReasonPriorityAliasLegendMap") == expected_reason_priority_legend_map, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcCoachCopyVariantRecommendationReasonPriorityAliasLegendHash") == expected_reason_priority_legend_hash, payload

        # Deterministic fixture lock for raised-intensity fallback branch:
        # CALM + LOCKED + RAISED must resolve to SLOW_STEP because intensity is elevated,
        # while still avoiding wobble/tense escalations.
        fixture_token, fixture_signals = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation(
            coach_microline_pair_signals={"arc": "SWAY"},
            coach_microline_alias_momentum_signals={"momentum": "LOCKED"},
            storybeat_phase_signals={"phase": "CALM"},
            storybeat_phase_fx_cue_compact_alias_intensity_signals={"intensity": "RAISED"},
        )
        assert fixture_token in {"FLAG OFF", "CBGCFXWAC COACH COPY REC:SLOW_STEP"}, fixture_signals
        assert fixture_signals["arc"] == "SWAY", fixture_signals
        assert fixture_signals["momentum"] == "LOCKED", fixture_signals
        assert fixture_signals["storybeatPhase"] == "CALM", fixture_signals
        assert fixture_signals["intensity"] == "RAISED", fixture_signals
        assert fixture_signals["recommendation"] == "SLOW_STEP", fixture_signals
        assert fixture_signals["reason"] == "raised-intensity", fixture_signals
        assert fixture_signals["reasonPriority"] == "P3", fixture_signals

        # Deterministic fixture lock for CBGCFXWSBPFXPDCWF DIGEST source-token coherence.
        # Toggle each FX cue family (SOFT|EDGE|HARD) via canonical cadence families and
        # verify both summary/token-coverage digest rows preserve matching source tokens.
        for fixture_family, expected_cue, expected_alias in (
            ("PACE_HOLD", "SOFT", "S"),
            ("PACE_PIVOT", "EDGE", "E"),
            ("PUNCH_BURST", "HARD", "H"),
        ):
            fixture_cadence_token, fixture_cadence_signals = (
                resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence(
                    copy_pack_variants_signals={"family": fixture_family, "token": f"CBGCFXWSBPFXPDCW COPY PACK:{fixture_family}"}
                )
            )
            assert fixture_cadence_signals.get("cadence") in {"STEADY", "PIVOT", "BURST"}, fixture_cadence_signals
            fixture_fx_token, fixture_fx_signals = (
                resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue(
                    copy_pack_cadence_signals=fixture_cadence_signals
                )
            )
            fixture_alias_token, fixture_alias_signals = (
                resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias(
                    fx_cue_signals=fixture_fx_signals
                )
            )
            assert fixture_fx_signals.get("fxCue") == expected_cue, fixture_fx_signals
            assert fixture_alias_signals.get("alias") == expected_alias, fixture_alias_signals
            assert fixture_alias_signals.get("sourceToken") == fixture_fx_signals.get("token"), fixture_alias_signals

            fixture_md = "\n".join(
                [
                    "## Summary",
                    f"- CBGCFXWSBPFXPDCWF DIGEST: **{fixture_alias_signals['alias']}** (map=S:SOFT,E:EDGE,H:HARD source={fixture_alias_signals['sourceToken']})",
                    "## Token Family Coverage",
                    f"- CBGCFXWSBPFXPDCWF DIGEST: {fixture_alias_signals['alias']} (map=S:SOFT,E:EDGE,H:HARD, source={fixture_alias_signals['sourceToken']})",
                ]
            )
            fixture_lines = fixture_md.splitlines()
            fixture_digest_rows = [
                line for line in fixture_lines if line.startswith("- CBGCFXWSBPFXPDCWF DIGEST:")
            ]
            assert len(fixture_digest_rows) == 2, fixture_md
            fixture_sources = []
            for row in fixture_digest_rows:
                assert "source=" in row, row
                source = row.split("source=", 1)[1].rstrip(")").strip()
                fixture_sources.append(source)
            assert fixture_sources[0] == fixture_sources[1], fixture_sources
            assert fixture_sources[0] == fixture_alias_signals.get("sourceToken"), fixture_sources
            assert fixture_sources[0] == f"CBGCFXWSBPFXPDCW FX CUE:{expected_cue}", fixture_sources
            assert fixture_alias_token in {"FLAG OFF", f"CBGCFXWSBPFXPDCWF:{expected_alias}"}, fixture_alias_token
            assert fixture_fx_token in {"FLAG OFF", f"CBGCFXWSBPFXPDCW FX CUE:{expected_cue}"}, fixture_fx_token
            assert fixture_cadence_token in {
                "FLAG OFF",
                "CBGCFXWSBPFXPDCW COPY PACK CADENCE:STEADY",
                "CBGCFXWSBPFXPDCW COPY PACK CADENCE:PIVOT",
                "CBGCFXWSBPFXPDCW COPY PACK CADENCE:BURST",
            }, fixture_cadence_token

        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceAlias", "").startswith(("FLAG OFF", "CBGCFXWC:")), payload
        assert set(payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "status",
            "alias",
            "token",
            "offlineOnly",
        }, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceAliasSignals", {}).get("status") in {"OK", "DRIFT"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceAliasSignals", {}).get("alias") in {"O", "D"}, payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceAliasSignals", {}).get("token", "").startswith("CBGCFXWC:"), payload
        assert payload.get("cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceAliasSignals", {}).get("offlineOnly") is True, payload
        assert set(payload.get("combatVfxCadenceCoachWhyHysteresisAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "hysteresisApplied",
            "alias",
        }, payload
        assert payload.get("combatVfxCadenceCoachAlias") in {"FLAG OFF", "CVCC:N", "CVCC:A", "CVCC:E"}, payload
        assert set(payload.get("combatVfxCadenceCoachAliasSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "coachToken",
            "alias",
        }, payload

        summary_lines = md_text.splitlines()
        summary_coach_idx = next(
            idx for idx, line in enumerate(summary_lines) if line.startswith("- LPRCG COACH:")
        )
        summary_alias_idx = next(
            idx for idx, line in enumerate(summary_lines) if line.startswith("- LPRCGC:")
        )
        assert summary_alias_idx == summary_coach_idx + 1

        summary_coach_copy_idx = next(
            idx for idx, line in enumerate(summary_lines) if line.startswith("- LPRCG COACH COPY:")
        )
        summary_coach_copy_alias_idx = next(
            idx for idx, line in enumerate(summary_lines) if line.startswith("- LPRCGCN:")
        )
        summary_coach_copy_why_idx = next(
            idx for idx, line in enumerate(summary_lines) if line.startswith("- LPRCG COACH COPY WHY:")
        )
        assert summary_coach_copy_alias_idx == summary_coach_copy_idx + 1
        assert summary_coach_copy_why_idx == summary_coach_copy_alias_idx + 1

        token_coverage_start_idx = next(
            idx
            for idx, line in enumerate(summary_lines)
            if line.strip() == "## Token Family Coverage"
        )
        token_coverage_lines = summary_lines[token_coverage_start_idx:]
        coverage_coach_idx = next(
            idx for idx, line in enumerate(token_coverage_lines) if line.startswith("- LPRCG COACH:")
        )
        coverage_alias_idx = next(
            idx for idx, line in enumerate(token_coverage_lines) if line.startswith("- LPRCGC:")
        )
        assert coverage_alias_idx == coverage_coach_idx + 1

        coverage_coach_copy_idx = next(
            idx for idx, line in enumerate(token_coverage_lines) if line.startswith("- LPRCG COACH COPY:")
        )
        coverage_coach_copy_alias_idx = next(
            idx for idx, line in enumerate(token_coverage_lines) if line.startswith("- LPRCGCN:")
        )
        coverage_coach_copy_why_idx = next(
            idx
            for idx, line in enumerate(token_coverage_lines)
            if line.startswith("- LPRCG COACH COPY WHY:")
        )
        assert coverage_coach_copy_alias_idx == coverage_coach_copy_idx + 1
        assert coverage_coach_copy_why_idx == coverage_coach_copy_alias_idx + 1

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
        assert "DMG COMBO:" in md_text
        assert "DMG COMBO CONF:" in md_text
        assert "DCR + DMG COMBO WINDOW RETUNE REC:" in md_text
        assert "DCRC + DMG COMBO WINDOW RETUNE CONF:" in md_text
        assert "DMG COMBO CHAIN COACH:" in md_text
        assert "DMG COMBO CONF COACH REC:" in md_text
        assert "DMG COMBO CONF COACH FALLBACK:" in md_text
        assert "DCCR:" in md_text
        assert "DMG COMBO CONF COACH SCENE ARC" in md_text
        assert "DMG COMBO CONF COACH COPY SWAP REC" in md_text
        assert "DCCSR:" in md_text
        assert "DCCST:" in md_text
        assert "DCCSA:" in md_text
        assert "PULSE REMAP MOMENTUM Δ:" in md_text
        assert "PULSE REMAP MOMENTUM SUPPRESS:" in md_text
        assert "PULSE REMAP SUPPRESS PLAN:" in md_text
        assert "PULSE REMAP SCENE:" in md_text
        assert "PULSE REMAP SCENE CONF:" in md_text
        assert "PULSE REMAP SCENE MICROLINE:" in md_text
        assert "PULSE REMAP SCENE MICROLINE VARIANT PACK:" in md_text
        assert "PULSE REMAP SCENE MICROLINE STYLE POLICY:" in md_text
        assert "PULSE REMAP SCENE MICROLINE STYLE POLICY SMOOTH:" in md_text
        assert "PULSE REMAP SCENE MICROLINE STYLE POSTURE:" in md_text
        assert "CBGCFXWSBPFXP LANG:" in md_text
        assert "PULSE REMAP SCENE FX GLINT:" in md_text
        assert "PRSFX:" in md_text
        assert "PULSE REMAP SCENE COPY PALETTE REC:" in md_text
        assert "PRSCP:" in md_text
        assert "PRSMPP:" in md_text
        assert "PRSMP:" in md_text
        assert "PULSE REMAP SCENE MICROLINE CADENCE:" in md_text
        assert "PRSMC:" in md_text
        assert "PRMS:" in md_text
        assert "PRSP:" in md_text
        assert "PRSMV:" in md_text
        assert "PRPW:" in md_text
        assert "PRM + PULSE REMAP MOMENTUM:" in md_text
        assert "PRMS + PULSE REMAP MOMENTUM SUPPRESS:" in md_text
        assert "PRSP + PULSE REMAP SUPPRESS PLAN:" in md_text
        assert "PRSMV + PULSE REMAP SCENE MICROLINE VARIANT PACK:" in md_text
        assert "PRSMP + PULSE REMAP SCENE MICROLINE STYLE POLICY:" in md_text
        assert "PRSMPP + PULSE REMAP SCENE MICROLINE STYLE POSTURE:" in md_text
        assert "PRSMC + PULSE REMAP SCENE MICROLINE CADENCE:" in md_text
        assert "PRSFX + PULSE REMAP SCENE FX GLINT:" in md_text
        assert "PRSCP + PULSE REMAP SCENE COPY PALETTE REC:" in md_text
        assert "PULSE REMAP SCENE FX GLINT:" in md_text
        assert "PRMS FAMILY TREND:" in md_text
        assert "PRSP FAMILY TREND:" in md_text
        assert "PRSMC FAMILY TREND:" in md_text
        assert "PRSMC FAMILY CHURN:" in md_text
        assert "PRSMP FAMILY TREND:" in md_text
        assert md_text.count("PRSMP FAMILY TREND:") == 2, md_text
        assert "PRSFX FAMILY TREND:" in md_text
        assert "PRSCP FAMILY TREND:" in md_text
        assert "DMG GLYPH:" in md_text
        assert "DMG GLYPH FX LIVE:" in md_text
        assert "LPR HYS THR:" in md_text
        assert "LPR VOL REGIME:" in md_text
        assert "LPR HYS WINDOW:" in md_text
        assert "LPR HYS WINDOW Δ:" in md_text
        assert "LPR HYS FLOOR REC + LPR HYS FLOOR:" in md_text
        assert "LPR HYS FLOOR FAMILY TREND:" in md_text
        assert "LPR HF T:" in md_text
        assert md_text.count("LPR HF T:") >= 2, md_text
        assert "LANE CADENCE SUMMARY: SYSTEMS/OPS" in md_text
        assert "PULSE HEAT FX COMPACT-BUDGET DRIFT" in md_text
        assert "ROUTE GLOW FX COMPACT-BUDGET DRIFT" in md_text
        assert "ROUTE GLOW FX CONF WHY RAIL MODE COMPACT-BUDGET DRIFT" in md_text
        assert "MODE TREND" in md_text
        assert "PRESSURE BAND" in md_text
        assert "DRIFT RISK" in md_text
        assert "RGFXWRI WHY CONF POLICY REC" in md_text
        assert "AMBIENT RAMP CONF REC" in md_text
        assert "DMG COMBO WINDOW RETUNE REC" in md_text
        assert "DCR:" in md_text
        assert "DMG COMBO WINDOW RETUNE CONF" in md_text
        assert "DCRC:" in md_text
        assert "DMG COMBO CHAIN COACH:" in md_text
        assert "DMG COMBO CONF COACH REC" in md_text
        assert "DMG COMBO CONF COACH FALLBACK" in md_text
        assert "DCCR:" in md_text
        assert "DCCSA:" in md_text
        assert "DCCR + DMG COMBO CONF COACH REC:" in md_text
        assert "DMG COMBO CONF COACH REC + DCCR FAMILY CHURN" in md_text
        assert "DMG COMBO CONF COACH SCENE ARC" in md_text
        assert "DMG COMBO CONF FX ACCENT" in md_text
        assert "DMG COMBO CONF COACH COPY SWAP REC" in md_text
        assert "DCCSR:" in md_text
        assert "DCCST:" in md_text
        assert "DCCFX:" in md_text
        assert "DCCFXT:" in md_text
        assert "DCCSA + DMG COMBO CONF COACH SCENE ARC:" in md_text
        assert "DCCFX + DMG COMBO CONF FX ACCENT:" in md_text
        assert "DCCSA FAMILY CHURN" in md_text
        assert "DCCFX FAMILY CHURN" in md_text
        assert "DCCFX FAMILY TREND" in md_text
        assert "DCCFX TREND HYS" in md_text
        assert "DCCSR FAMILY CHURN" in md_text
        assert "DCCST FAMILY CHURN" in md_text
        assert "DCCSR + DMG COMBO CONF COACH COPY SWAP REC:" in md_text
        assert "DCCFXT ALIAS:" in md_text
        assert "DCCFXH:" in md_text
        assert "DCCFXV:" in md_text
        assert "DCCFXC:" in md_text
        assert "DCCFXCW:" in md_text
        assert "DCCFXCW SCENE PALETTE:" in md_text
        assert "DCCFXCW SCENE PALETTE LEGEND:" in md_text
        assert "DCCFXCW SCENE PALETTE TREND:" in md_text
        assert "DCCFXCW SCENE PULSE:" in md_text
        assert "DCCFXCW SCENE PULSE LEGEND:" in md_text
        assert "DCCFXCW SCENE PULSE ARC:" in md_text
        assert "DCCFXCW SCENE PULSE ARC LEGEND:" in md_text
        assert "DCCFXCPA:" in md_text
        assert "DCCFXCPA LEGEND:" in md_text
        assert "DCCFXCPA FAMILY CHURN" in md_text
        assert "DCCFXCPA COPY:" in md_text
        assert "DCCFXCPA COPY ALT:" in md_text
        assert "DCCFXCPA COPY ALT PACK:" in md_text
        assert "DCCFXCPAP:" in md_text
        assert "DCCFXCPAP COACH:" in md_text
        assert "DCCFXCPAP COACH LEGEND:" in md_text
        assert "DCCFXCPAP COACH FAMILY CHURN" in md_text
        assert "DCCFXCPAP FAMILY CHURN" in md_text
        assert "DCCFXCPAP FX CUE:" in md_text
        assert "DCCFXCPAP FX CUE LEGEND:" in md_text
        assert "DCCFXCPA COPY ALT LEGEND:" in md_text
        assert "DCCFXCPA COPY ALT PACK LEGEND:" in md_text
        assert "DCCFXCPA COPY LEGEND:" in md_text
        assert "DCCFXCPA COPY FAMILY CHURN" in md_text
        assert "DCCFXCPA COPY ALT FAMILY CHURN" in md_text
        assert "DCCFXCPA COPY ALT FAMILY TREND" in md_text
        assert "DCCFXCPA COPY ALT PACK FAMILY CHURN" in md_text
        assert "DCCFXCPA COPY ALT PACK FAMILY TREND" in md_text
        assert "DCCFXV FAMILY CHURN" in md_text
        assert "DCCFXC FAMILY CHURN" in md_text
        assert "DCCFXCW FAMILY CHURN" in md_text
        assert "DCCFXH ALIAS:" in md_text
        assert "DCCFXV ALIAS:" in md_text
        assert "DCCFXC ALIAS:" in md_text
        assert "DCCFXCW ALIAS:" in md_text
        assert "DCCFXV LEGEND:" in md_text
        assert "DCCFXC LEGEND:" in md_text
        assert "DCCFXCW LEGEND:" in md_text
        assert "DCCFXV + DMG COMBO CONF FX ACCENT VOLATILITY:" in md_text
        assert "DCCST ALIAS:" in md_text
        assert "DMG COMBO CONF COACH COPY SWAP REC FAMILY TREND" in md_text

        md_lines = md_text.splitlines()

        def _find_line_index(prefix: str) -> int:
            for idx, line in enumerate(md_lines):
                if line.startswith(prefix):
                    return idx
            raise AssertionError(f"missing line prefix: {prefix}")

        def _find_line_indices(prefix: str) -> list[int]:
            indices = [idx for idx, line in enumerate(md_lines) if line.startswith(prefix)]
            if not indices:
                raise AssertionError(f"missing line prefix: {prefix}")
            return indices

        summary_row_prefix, summary_arc_alias_prefix, summary_alias_prefix, summary_legend_prefix = COHERENCE_ARC_COACH_ORDER_LOCK_SCAFFOLD["summary"]
        token_cov_row_prefix, token_cov_arc_alias_prefix, token_cov_alias_prefix, token_cov_legend_prefix = COHERENCE_ARC_COACH_ORDER_LOCK_SCAFFOLD["tokenCoverage"]
        scaffold_enabled = bool(COHERENCE_ARC_COACH_ORDER_LOCK_SCAFFOLD["enabled"])
        row_indices = [idx for idx, line in enumerate(md_lines) if line.startswith(summary_row_prefix)]
        arc_alias_indices = [idx for idx, line in enumerate(md_lines) if line.startswith(summary_arc_alias_prefix)]
        alias_indices = [idx for idx, line in enumerate(md_lines) if line.startswith(summary_alias_prefix)]
        legend_indices = [idx for idx, line in enumerate(md_lines) if line.startswith(summary_legend_prefix)]
        assert (
            summary_row_prefix == token_cov_row_prefix
            and summary_arc_alias_prefix == token_cov_arc_alias_prefix
            and summary_alias_prefix == token_cov_alias_prefix
            and summary_legend_prefix == token_cov_legend_prefix
        )
        if scaffold_enabled:
            assert len(row_indices) == 2 and len(arc_alias_indices) == 2 and len(alias_indices) == 2 and len(legend_indices) == 2, md_text
            assert arc_alias_indices[0] == row_indices[0] + 1, md_text
            assert alias_indices[0] == arc_alias_indices[0] + 1, md_text
            assert legend_indices[0] == alias_indices[0] + 1, md_text
            assert arc_alias_indices[1] == row_indices[1] + 1, md_text
            assert alias_indices[1] == arc_alias_indices[1] + 1, md_text
            assert legend_indices[1] == alias_indices[1] + 1, md_text
        else:
            assert not row_indices and not arc_alias_indices and not alias_indices and not legend_indices, md_text

        combo_conf_rec_idx = _find_line_index("- DMG COMBO CONF COACH REC:")
        combo_conf_fallback_idx = _find_line_index("- DMG COMBO CONF COACH FALLBACK:")
        combo_conf_scene_arc_idx = _find_line_index("- DMG COMBO CONF COACH SCENE ARC:")
        combo_conf_fx_accent_idx = _find_line_index("- DMG COMBO CONF FX ACCENT:")
        combo_conf_copy_swap_idx = _find_line_index("- DMG COMBO CONF COACH COPY SWAP REC:")
        combo_conf_dccsa_family_churn_idx = _find_line_index("- DCCSA FAMILY CHURN:")
        combo_conf_dccfx_family_churn_idx = _find_line_index("- DCCFX FAMILY CHURN:")
        combo_conf_dccfx_family_trend_idx = _find_line_index("- DCCFX FAMILY TREND:")
        combo_conf_dccfx_trend_hys_idx = _find_line_index("- DCCFX TREND HYS:")
        combo_conf_dccfxt_alias_idx = _find_line_index("- DCCFXT:")
        combo_conf_dccfxh_alias_idx = _find_line_index("- DCCFXH:")
        combo_conf_dccfxv_alias_idx = _find_line_index("- DCCFXV:")
        combo_conf_dccfxc_alias_idx = _find_line_index("- DCCFXC:")
        combo_conf_dccfxcw_alias_idx = _find_line_index("- DCCFXCW:")
        combo_conf_dccfxv_alias_indices = _find_line_indices("- DCCFXV:")
        combo_conf_dccfxc_alias_indices = _find_line_indices("- DCCFXC:")
        combo_conf_dccfxcw_alias_indices = _find_line_indices("- DCCFXCW:")
        combo_conf_dccfxcw_scene_palette_idx = _find_line_index("- DCCFXCW SCENE PALETTE:")
        combo_conf_dccfxcw_scene_palette_legend_idx = _find_line_index("- DCCFXCW SCENE PALETTE LEGEND:")
        combo_conf_dccfxcw_scene_palette_trend_idx = _find_line_index("- DCCFXCW SCENE PALETTE TREND:")
        combo_conf_dccfxcw_scene_pulse_idx = _find_line_index("- DCCFXCW SCENE PULSE:")
        combo_conf_dccfxcw_scene_pulse_legend_idx = _find_line_index("- DCCFXCW SCENE PULSE LEGEND:")
        combo_conf_dccfxcw_scene_pulse_arc_idx = _find_line_index("- DCCFXCW SCENE PULSE ARC:")
        combo_conf_dccfxcw_scene_pulse_arc_legend_idx = _find_line_index("- DCCFXCW SCENE PULSE ARC LEGEND:")
        combo_conf_dccfxcpa_alias_idx = _find_line_index("- DCCFXCPA:")
        combo_conf_dccfxcpa_legend_idx = _find_line_index("- DCCFXCPA LEGEND:")
        combo_conf_dccfxcpa_family_churn_idx = _find_line_index("- DCCFXCPA FAMILY CHURN:")
        combo_conf_dccfxcpa_copy_idx = _find_line_index("- DCCFXCPA COPY:")
        combo_conf_dccfxcpa_copy_alt_idx = _find_line_index("- DCCFXCPA COPY ALT:")
        combo_conf_dccfxcpa_copy_alt_pack_idx = _find_line_index("- DCCFXCPA COPY ALT PACK:")
        combo_conf_dccfxcpa_copy_alt_pack_alias_idx = _find_line_index("- DCCFXCPAP:")
        combo_conf_dccfxcpap_coach_idx = _find_line_index("- DCCFXCPAP COACH:")
        combo_conf_dccfxcpap_coach_legend_idx = _find_line_index("- DCCFXCPAP COACH LEGEND:")
        combo_conf_dccfxcpap_coach_family_churn_idx = _find_line_index("- DCCFXCPAP COACH FAMILY CHURN:")
        combo_conf_dccfxcpap_family_churn_idx = _find_line_index("- DCCFXCPAP FAMILY CHURN:")
        combo_conf_dccfxcpap_fx_cue_idx = _find_line_index("- DCCFXCPAP FX CUE:")
        combo_conf_dccfxcpap_fx_cue_legend_idx = _find_line_index("- DCCFXCPAP FX CUE LEGEND:")
        combo_conf_dccfxcpa_copy_alt_legend_idx = _find_line_index("- DCCFXCPA COPY ALT LEGEND:")
        combo_conf_dccfxcpa_copy_alt_pack_legend_idx = _find_line_index("- DCCFXCPA COPY ALT PACK LEGEND:")
        combo_conf_dccfxcpa_copy_legend_idx = _find_line_index("- DCCFXCPA COPY LEGEND:")
        combo_conf_dccfxcpa_copy_family_churn_idx = _find_line_index("- DCCFXCPA COPY FAMILY CHURN:")
        combo_conf_dccfxcpa_copy_alt_family_churn_idx = _find_line_index("- DCCFXCPA COPY ALT FAMILY CHURN:")
        combo_conf_dccfxcpa_copy_alt_family_trend_idx = _find_line_index("- DCCFXCPA COPY ALT FAMILY TREND:")
        combo_conf_dccfxcpa_copy_alt_pack_family_churn_idx = _find_line_index("- DCCFXCPA COPY ALT PACK FAMILY CHURN:")
        combo_conf_dccfxcpa_copy_alt_pack_family_trend_idx = _find_line_index("- DCCFXCPA COPY ALT PACK FAMILY TREND:")
        combo_conf_dccfxv_family_churn_idx = _find_line_index("- DCCFXV FAMILY CHURN:")
        combo_conf_dccfxc_family_churn_idx = _find_line_index("- DCCFXC FAMILY CHURN:")
        combo_conf_dccfxcw_family_churn_idx = _find_line_index("- DCCFXCW FAMILY CHURN:")
        combo_conf_copy_swap_dccsr_family_churn_idx = _find_line_index("- DCCSR FAMILY CHURN:")
        combo_conf_copy_swap_dccst_family_churn_idx = _find_line_index("- DCCST FAMILY CHURN:")
        combo_conf_copy_swap_family_trend_idx = _find_line_index("- DMG COMBO CONF COACH COPY SWAP REC FAMILY TREND:")
        prsmc_family_trend_idx = _find_line_index("- PRSMC FAMILY TREND:")
        prsmc_family_churn_idx = _find_line_index("- PRSMC FAMILY CHURN:")

        lane_cadence_miss_risk_indices = _find_line_indices("- LANE CADENCE MISS RISK:")
        lane_cadence_miss_risk_alias_indices = _find_line_indices("- LCMR:")
        lane_cadence_24h_check_indices = _find_line_indices("- LANE CADENCE 24H CHECK:")
        combat_vfx_watchdog_indices = _find_line_indices("- COMBAT/VFX CADENCE WATCHDOG:")
        combat_vfx_watchdog_streak_indices = _find_line_indices("- COMBAT/VFX CADENCE WATCHDOG STREAK:")
        combat_vfx_cadence_coach_indices = _find_line_indices("- COMBAT/VFX CADENCE COACH:")
        combat_vfx_cadence_coach_why_indices = _find_line_indices("- COMBAT/VFX CADENCE COACH WHY:")
        combat_vfx_cadence_coach_why_alias_indices = _find_line_indices("- CVCW:")
        combat_vfx_cadence_coach_why_hysteresis_alias_indices = _find_line_indices("- CVCWH:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_indices = _find_line_indices("- CVCWHR:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_indices = _find_line_indices("- CVCWHR CONF:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_alias_indices = _find_line_indices("- CVCWHRC:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_indices = _find_line_indices("- CVCWHR CONF FLOOR REC:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_alias_indices = _find_line_indices("- CVCWHRF:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_indices = _find_line_indices("- CVCWHR FX PULSE:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_indices = _find_line_indices("- CVCWHR FX PULSE LEGEND:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_rec_indices = _find_line_indices("- CVCWHR FX LEGEND REC:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_rec_conf_indices = _find_line_indices("- CVCWHR FX LEGEND REC CONF:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_indices = _find_line_indices("- CVCWHR FX LEGEND COPY PACK:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_alias_indices = _find_line_indices("- CVCWHR FX LEGEND CP:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_indices = _find_line_indices("- CVCWHR FX LEGEND COPY PACK TREND:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_alias_indices = _find_line_indices("- CVCWHR FX LEGEND CPT:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_indices = _find_line_indices("- CVCWHR FX LEGEND COPY PACK TREND CONF:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_alias_indices = _find_line_indices("- CVCWHR FX LEGEND CPTC:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_alias_legend_indices = _find_line_indices("- CVCWHR FX LEGEND CPTC LEGEND:")
        cadence_bridge_indices = _find_line_indices("- CADENCE BRIDGE:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_family_churn_indices = _find_line_indices("- CVCWHR CONF FLOOR + CVCWHRF FAMILY CHURN:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_family_churn_indices = _find_line_indices("- CVCWHR FX PULSE FAMILY CHURN:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_family_trend_indices = _find_line_indices("- CVCWHR FX PULSE FAMILY TREND:")
        cadence_bridge_family_churn_indices = _find_line_indices("- CADENCE BRIDGE FAMILY CHURN:")
        cadence_bridge_glyph_indices = _find_line_indices("- CADENCE BRIDGE GLYPH:")
        cadence_bridge_glyph_conf_indices = _find_line_indices("- CADENCE BRIDGE GLYPH CONF:")
        cadence_bridge_glyph_conf_compact_alias_enabled = bool(
            payload.get("cadenceBridgeGlyphConfidenceCompactAliasSignals", {}).get("flagEnabled", False)
        )
        cadence_bridge_glyph_conf_compact_alias_indices = (
            _find_line_indices("- CBGC:") if cadence_bridge_glyph_conf_compact_alias_enabled else []
        )
        cadence_bridge_glyph_conf_compact_alias_legend_indices = _find_line_indices("- CBGC LEGEND:")
        cadence_bridge_glyph_conf_compact_legend_alias_indices = _find_line_indices("- CBGCL:")
        cadence_bridge_glyph_conf_intent_compact_active_alias_indices = _find_line_indices("- CBGCIA:")
        cadence_bridge_glyph_conf_intent_compact_active_alias_family_churn_indices = _find_line_indices("- CBGCIA FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_regime_alias_indices = _find_line_indices("- CBGCFXR:")
        cadence_bridge_glyph_conf_fx_pulse_regime_alias_family_churn_indices = _find_line_indices("- CBGCFXR FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_indices = _find_line_indices("- CBGCFXA:")
        cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_family_churn_indices = _find_line_indices("- CBGCFXA FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_indices = _find_line_indices("- CBGC FX HINT:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_family_churn_indices = _find_line_indices("- CBGC FX HINT FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_indices = _find_line_indices("- CBGCFXH:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_family_churn_indices = _find_line_indices("- CBGCFXH FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_indices = _find_line_indices("- CBGCFXW:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_family_churn_indices = _find_line_indices("- CBGCFXW FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_legend_indices = _find_line_indices("- CBGCFXW LEGEND:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_indices = _find_line_indices("- CBGCFXW COHERENCE:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_indices = _find_line_indices("- CBGCFXW COHERENCE MOMENTUM:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_indices = _find_line_indices("- CBGCFXWM:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_legend_indices = _find_line_indices("- CBGCFXWM LEGEND:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_indices = _find_line_indices("- CBGCFXWC:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_legend_indices = _find_line_indices("- CBGCFXWC LEGEND:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_family_churn_indices = _find_line_indices("- CBGCFXWC FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_drift_indices = _find_line_indices("- CBGCFXWAC DRIFT:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_momentum_indices = _find_line_indices("- CBGCFXWAC MOMENTUM:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_momentum_family_churn_indices = _find_line_indices("- CBGCFXWAC MOMENTUM FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_indices = _find_line_indices("- CBGCFXWSB:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_family_churn_indices = _find_line_indices("- CBGCFXWSB FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_indices = _find_line_indices("- CBGCFXWSBP:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_family_churn_indices = _find_line_indices("- CBGCFXWSBP FAMILY CHURN:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_indices = _find_line_indices("- CBGCFXWSBP FX CUE:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_indices = _find_line_indices("- CBGCFXWSBPFC:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_indices = _find_line_indices("- CBGCFXWSBPFCI:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_indices = _find_line_indices("- CBGCFXWSBPFXP:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_decode_microline_pair_indices = _find_line_indices("- CBGCFXWSBPFXP MICROLINE:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_legend_indices = _find_line_indices("- CBGCFXWSBPFXP MICROLINE LEGEND:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_legend_indices = _find_line_indices("- CBGCFXWSBPFCI LEGEND:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_indices = _find_line_indices("- CBGCFXWSBPFCI COACH COPY:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_indices = _find_line_indices("- CBGCFXWSBPFXP LANG:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPI:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPI LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPI LEGEND COPY:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPIC:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPI NARR:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPIN:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPIN LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPINF:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPINF LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPINF ORDER:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPI DRILL:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPD:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPD MICROLINE:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPD MICROLINE LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPD COACH:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDC:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPD COACH WHY:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW COPY PACK:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW COPY PACK LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW COPY PACK CADENCE:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWC:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWC LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW FX CUE:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCW FX CUE LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWF:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWF LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWF DIGEST:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWF COHERENCE:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWF COHERENCE LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFC:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFC LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCT:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCT LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTA:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTA LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTA DIGEST:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTA RFALL:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTA RFALL LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CTA REVIEW CADENCE NOTE:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CTA REVIEW CADENCE NOTE LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAN:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAN LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAP:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAP LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAS:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAS LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAS CPACK:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPD ECHO:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE MATRIX:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE MATRIX DRIFT:") and "TREND" not in line
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_trend_band_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE MATRIX DRIFT TREND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDS:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDS LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_profiler_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE POLICY OPS WINDOW:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE POLICY OPS DOMINANT:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_legend_indices = [
            i for i, line in enumerate(md_lines) if line.startswith("- CBGCFXWSBPFXPDE POLICY OPS DOMINANT LEGEND:")
        ]
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_indices = _find_line_indices("- CBGCFXWAC COACH COPY REC:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_compact_alias_indices = _find_line_indices("- CBGCFXWACRC:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_compact_alias_legend_indices = _find_line_indices("- CBGCFXWACRC LEGEND:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_reason_priority_alias_indices = _find_line_indices("- CBGCFXWACRP:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_reason_priority_alias_legend_indices = _find_line_indices("- CBGCFXWACRP LEGEND:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_indices = _find_line_indices("- CBGCFXW DRIFT:")
        cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_family_churn_indices = _find_line_indices("- CBGCFXW DRIFT FAMILY CHURN:")
        cadence_bridge_glyph_conf_intent_compact_alias_indices = _find_line_indices("- CBGCI:")
        cadence_bridge_glyph_conf_intent_legend_indices = _find_line_indices("- CBGCI LEGEND:")
        cadence_bridge_glyph_conf_intent_legend_alias_indices = _find_line_indices("- CBGCIL:")
        cadence_bridge_glyph_conf_legend_indices = _find_line_indices("- CADENCE BRIDGE GLYPH CONF LEGEND:")
        cadence_bridge_glyph_legend_indices = _find_line_indices("- CADENCE BRIDGE GLYPH LEGEND:")
        combat_vfx_cadence_coach_why_hysteresis_family_churn_indices = _find_line_indices("- CVCWH FAMILY CHURN:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_family_churn_indices = _find_line_indices("- CVCWHR FAMILY CHURN:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_family_churn_indices = _find_line_indices("- CVCWHR CONF + CVCWHRC FAMILY CHURN:")
        combat_vfx_cadence_coach_alias_indices = _find_line_indices("- CVCC:")
        combat_vfx_cadence_coach_why_family_churn_indices = _find_line_indices("- COMBAT/VFX CADENCE COACH WHY + CVCW FAMILY CHURN:")
        combat_vfx_cadence_coach_family_churn_indices = _find_line_indices("- COMBAT/VFX CADENCE COACH + CVCC FAMILY CHURN:")
        combat_vfx_watchdog_legend_indices = _find_line_indices("- COMBAT/VFX CADENCE WATCHDOG LEGEND:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_override_indices = _find_line_indices("- CVCWHR FX LEGEND CPTC OVERRIDE:")
        combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_family_churn_indices = _find_line_indices("- CVCWHR FX LEGEND COPY PACK FAMILY CHURN:")

        assert combo_conf_fallback_idx == combo_conf_rec_idx + 1, (
            "expected DMG COMBO CONF COACH FALLBACK row directly after COACH REC row"
        )
        assert combo_conf_scene_arc_idx in {
            combo_conf_fallback_idx + 1,
            combo_conf_fallback_idx + 2,
            combo_conf_fallback_idx + 3,
        }, "expected DMG COMBO CONF COACH SCENE ARC row adjacent to combo-confidence coach rows"
        assert combo_conf_fx_accent_idx == combo_conf_scene_arc_idx + 1, (
            "expected FX ACCENT row directly after COACH SCENE ARC row"
        )
        assert combo_conf_copy_swap_idx == combo_conf_fx_accent_idx + 1, (
            "expected COACH COPY SWAP row directly after FX ACCENT row"
        )

        if combo_conf_scene_arc_idx == combo_conf_fallback_idx + 2:
            assert md_lines[combo_conf_fallback_idx + 1].startswith("- DCCR:"), (
                "only compact DCCR alias row may appear between COACH FALLBACK and SCENE ARC rows"
            )
        if combo_conf_scene_arc_idx == combo_conf_fallback_idx + 3:
            assert md_lines[combo_conf_fallback_idx + 1].startswith("- DCCR:"), (
                "expected DCCR row as first alias spacer before SCENE ARC"
            )
            assert md_lines[combo_conf_fallback_idx + 2].startswith("- DCCSA:"), (
                "expected DCCSA row as second alias spacer before SCENE ARC"
            )
        assert combo_conf_dccfx_family_churn_idx == combo_conf_dccsa_family_churn_idx + 1, (
            "expected DCCFX FAMILY CHURN row directly after DCCSA FAMILY CHURN row"
        )
        assert combo_conf_dccfx_family_trend_idx == combo_conf_dccfx_family_churn_idx + 1, (
            "expected DCCFX FAMILY TREND row directly after DCCFX FAMILY CHURN row"
        )
        assert combo_conf_dccfx_trend_hys_idx == combo_conf_dccfx_family_trend_idx + 1, (
            "expected DCCFX TREND HYS row directly after DCCFX FAMILY TREND row"
        )
        assert combo_conf_dccfxt_alias_idx == combo_conf_dccfx_trend_hys_idx + 1, (
            "expected DCCFXT row directly after DCCFX TREND HYS row"
        )
        assert combo_conf_dccfxh_alias_idx == combo_conf_dccfxt_alias_idx + 1, (
            "expected DCCFXH row directly after DCCFXT row"
        )
        assert combo_conf_dccfxv_alias_idx == combo_conf_dccfxh_alias_idx + 1, (
            "expected DCCFXV row directly after DCCFXH row"
        )
        assert combo_conf_dccfxc_alias_idx == combo_conf_dccfxv_alias_idx + 1, (
            "expected DCCFXC row directly after DCCFXV row"
        )
        assert combo_conf_dccfxcw_alias_idx == combo_conf_dccfxc_alias_idx + 1, (
            "expected DCCFXCW row directly after DCCFXC row"
        )
        def _find_in_range(prefix: str, start: int, end: int, label: str) -> int:
            for idx in range(start, end):
                if summary_lines[idx].startswith(prefix):
                    return idx
            raise AssertionError(f"missing {label} row in requested section: {prefix}")

        summary_dccfxv_idx = _find_in_range("- DCCFXV:", 0, token_coverage_start_idx, "summary")
        summary_dccfxc_idx = _find_in_range("- DCCFXC:", 0, token_coverage_start_idx, "summary")
        summary_dccfxcw_idx = _find_in_range("- DCCFXCW:", 0, token_coverage_start_idx, "summary")
        assert summary_dccfxc_idx == summary_dccfxv_idx + 1, (
            "expected DCCFXC row directly after DCCFXV row in summary section"
        )
        assert summary_dccfxcw_idx == summary_dccfxc_idx + 1, (
            "expected DCCFXCW row directly after DCCFXC row in summary section"
        )

        coverage_start = token_coverage_start_idx
        coverage_end = len(summary_lines)
        coverage_dccfxv_idx = _find_in_range("- DCCFXV ALIAS:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxc_idx = _find_in_range("- DCCFXC ALIAS:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_idx = _find_in_range("- DCCFXCW ALIAS:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_scene_palette_idx = _find_in_range("- DCCFXCW SCENE PALETTE:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_scene_palette_legend_idx = _find_in_range("- DCCFXCW SCENE PALETTE LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_scene_palette_trend_idx = _find_in_range("- DCCFXCW SCENE PALETTE TREND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_scene_pulse_idx = _find_in_range("- DCCFXCW SCENE PULSE:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_scene_pulse_legend_idx = _find_in_range("- DCCFXCW SCENE PULSE LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_scene_pulse_arc_idx = _find_in_range("- DCCFXCW SCENE PULSE ARC:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcw_scene_pulse_arc_legend_idx = _find_in_range("- DCCFXCW SCENE PULSE ARC LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_alias_idx = _find_in_range("- DCCFXCPA:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_legend_idx = _find_in_range("- DCCFXCPA LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_family_churn_idx = _find_in_range("- DCCFXCPA FAMILY CHURN:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_idx = _find_in_range("- DCCFXCPA COPY:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_idx = _find_in_range("- DCCFXCPA COPY ALT:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_pack_idx = _find_in_range("- DCCFXCPA COPY ALT PACK:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_pack_alias_idx = _find_in_range("- DCCFXCPAP:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpap_coach_idx = _find_in_range("- DCCFXCPAP COACH:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpap_coach_legend_idx = _find_in_range("- DCCFXCPAP COACH LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpap_coach_family_churn_idx = _find_in_range("- DCCFXCPAP COACH FAMILY CHURN:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpap_family_churn_idx = _find_in_range("- DCCFXCPAP FAMILY CHURN:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpap_fx_cue_idx = _find_in_range("- DCCFXCPAP FX CUE:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpap_fx_cue_legend_idx = _find_in_range("- DCCFXCPAP FX CUE LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_legend_idx = _find_in_range("- DCCFXCPA COPY ALT LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_pack_legend_idx = _find_in_range("- DCCFXCPA COPY ALT PACK LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_legend_idx = _find_in_range("- DCCFXCPA COPY LEGEND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_family_churn_idx = _find_in_range("- DCCFXCPA COPY FAMILY CHURN:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_family_churn_idx = _find_in_range("- DCCFXCPA COPY ALT FAMILY CHURN:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_family_trend_idx = _find_in_range("- DCCFXCPA COPY ALT FAMILY TREND:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_pack_family_churn_idx = _find_in_range("- DCCFXCPA COPY ALT PACK FAMILY CHURN:", coverage_start, coverage_end, "token coverage")
        coverage_dccfxcpa_copy_alt_pack_family_trend_idx = _find_in_range("- DCCFXCPA COPY ALT PACK FAMILY TREND:", coverage_start, coverage_end, "token coverage")
        assert coverage_dccfxc_idx == coverage_dccfxv_idx + 1, (
            "expected DCCFXC row directly after DCCFXV row in token-coverage section"
        )
        assert coverage_dccfxcw_idx == coverage_dccfxc_idx + 1, (
            "expected DCCFXCW row directly after DCCFXC row in token-coverage section"
        )
        assert coverage_dccfxcw_scene_palette_idx == coverage_dccfxcw_idx + 1, (
            "expected DCCFXCW SCENE PALETTE row directly after DCCFXCW ALIAS row in token-coverage section"
        )
        assert coverage_dccfxcw_scene_palette_legend_idx == coverage_dccfxcw_scene_palette_idx + 1, (
            "expected DCCFXCW SCENE PALETTE LEGEND row directly after DCCFXCW SCENE PALETTE row in token-coverage section"
        )
        assert coverage_dccfxcw_scene_palette_trend_idx == coverage_dccfxcw_scene_palette_legend_idx + 1, (
            "expected DCCFXCW SCENE PALETTE TREND row directly after DCCFXCW SCENE PALETTE LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcw_scene_pulse_idx == coverage_dccfxcw_scene_palette_trend_idx + 1, (
            "expected DCCFXCW SCENE PULSE row directly after DCCFXCW SCENE PALETTE TREND row in token-coverage section"
        )
        assert coverage_dccfxcw_scene_pulse_legend_idx == coverage_dccfxcw_scene_pulse_idx + 1, (
            "expected DCCFXCW SCENE PULSE LEGEND row directly after DCCFXCW SCENE PULSE row in token-coverage section"
        )
        assert coverage_dccfxcw_scene_pulse_arc_idx == coverage_dccfxcw_scene_pulse_legend_idx + 1, (
            "expected DCCFXCW SCENE PULSE ARC row directly after DCCFXCW SCENE PULSE LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcw_scene_pulse_arc_legend_idx == coverage_dccfxcw_scene_pulse_arc_idx + 1, (
            "expected DCCFXCW SCENE PULSE ARC LEGEND row directly after DCCFXCW SCENE PULSE ARC row in token-coverage section"
        )
        assert coverage_dccfxcpa_alias_idx == coverage_dccfxcw_scene_pulse_arc_legend_idx + 1, (
            "expected DCCFXCPA row directly after DCCFXCW SCENE PULSE ARC LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcpa_legend_idx == coverage_dccfxcpa_alias_idx + 1, (
            "expected DCCFXCPA LEGEND row directly after DCCFXCPA row in token-coverage section"
        )
        assert coverage_dccfxcpa_family_churn_idx == coverage_dccfxcpa_legend_idx + 1, (
            "expected DCCFXCPA FAMILY CHURN row directly after DCCFXCPA LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_idx == coverage_dccfxcpa_family_churn_idx + 1, (
            "expected DCCFXCPA COPY row directly after DCCFXCPA FAMILY CHURN row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_idx == coverage_dccfxcpa_copy_idx + 1, (
            "expected DCCFXCPA COPY ALT row directly after DCCFXCPA COPY row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_pack_idx == coverage_dccfxcpa_copy_alt_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK row directly after DCCFXCPA COPY ALT row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_pack_alias_idx == coverage_dccfxcpa_copy_alt_pack_idx + 1, (
            "expected DCCFXCPAP row directly after DCCFXCPA COPY ALT PACK row in token-coverage section"
        )
        assert coverage_dccfxcpap_coach_idx == coverage_dccfxcpa_copy_alt_pack_alias_idx + 1, (
            "expected DCCFXCPAP COACH row directly after DCCFXCPAP row in token-coverage section"
        )
        assert coverage_dccfxcpap_coach_legend_idx == coverage_dccfxcpap_coach_idx + 1, (
            "expected DCCFXCPAP COACH LEGEND row directly after DCCFXCPAP COACH row in token-coverage section"
        )
        assert coverage_dccfxcpap_coach_family_churn_idx == coverage_dccfxcpap_coach_legend_idx + 1, (
            "expected DCCFXCPAP COACH FAMILY CHURN row directly after DCCFXCPAP COACH LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcpap_family_churn_idx == coverage_dccfxcpap_coach_family_churn_idx + 1, (
            "expected DCCFXCPAP FAMILY CHURN row directly after DCCFXCPAP COACH FAMILY CHURN row in token-coverage section"
        )
        assert coverage_dccfxcpap_fx_cue_idx == coverage_dccfxcpap_family_churn_idx + 1, (
            "expected DCCFXCPAP FX CUE row directly after DCCFXCPAP FAMILY CHURN row in token-coverage section"
        )
        assert coverage_dccfxcpap_fx_cue_legend_idx == coverage_dccfxcpap_fx_cue_idx + 1, (
            "expected DCCFXCPAP FX CUE LEGEND row directly after DCCFXCPAP FX CUE row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_legend_idx == coverage_dccfxcpap_fx_cue_legend_idx + 1, (
            "expected DCCFXCPA COPY ALT LEGEND row directly after DCCFXCPAP FX CUE LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_pack_legend_idx == coverage_dccfxcpa_copy_alt_legend_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK LEGEND row directly after DCCFXCPA COPY ALT LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_legend_idx == coverage_dccfxcpa_copy_alt_pack_legend_idx + 1, (
            "expected DCCFXCPA COPY LEGEND row directly after DCCFXCPA COPY ALT PACK LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_family_churn_idx == coverage_dccfxcpa_copy_legend_idx + 1, (
            "expected DCCFXCPA COPY FAMILY CHURN row directly after DCCFXCPA COPY LEGEND row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_family_churn_idx == coverage_dccfxcpa_copy_family_churn_idx + 1, (
            "expected DCCFXCPA COPY ALT FAMILY CHURN row directly after DCCFXCPA COPY FAMILY CHURN row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_family_trend_idx == coverage_dccfxcpa_copy_alt_family_churn_idx + 1, (
            "expected DCCFXCPA COPY ALT FAMILY TREND row directly after DCCFXCPA COPY ALT FAMILY CHURN row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_pack_family_churn_idx == coverage_dccfxcpa_copy_alt_family_trend_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK FAMILY CHURN row directly after DCCFXCPA COPY ALT FAMILY TREND row in token-coverage section"
        )
        assert coverage_dccfxcpa_copy_alt_pack_family_trend_idx == coverage_dccfxcpa_copy_alt_pack_family_churn_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK FAMILY TREND row directly after DCCFXCPA COPY ALT PACK FAMILY CHURN row in token-coverage section"
        )
        assert combo_conf_dccfxcw_scene_palette_idx == combo_conf_dccfxcw_alias_idx + 1, (
            "expected DCCFXCW SCENE PALETTE row directly after DCCFXCW row"
        )
        assert combo_conf_dccfxcw_scene_palette_legend_idx == combo_conf_dccfxcw_scene_palette_idx + 1, (
            "expected DCCFXCW SCENE PALETTE LEGEND row directly after DCCFXCW SCENE PALETTE row"
        )
        assert combo_conf_dccfxcw_scene_palette_trend_idx == combo_conf_dccfxcw_scene_palette_legend_idx + 1, (
            "expected DCCFXCW SCENE PALETTE TREND row directly after DCCFXCW SCENE PALETTE LEGEND row"
        )
        assert combo_conf_dccfxcw_scene_pulse_idx == combo_conf_dccfxcw_scene_palette_trend_idx + 1, (
            "expected DCCFXCW SCENE PULSE row directly after DCCFXCW SCENE PALETTE TREND row"
        )
        assert combo_conf_dccfxcw_scene_pulse_legend_idx == combo_conf_dccfxcw_scene_pulse_idx + 1, (
            "expected DCCFXCW SCENE PULSE LEGEND row directly after DCCFXCW SCENE PULSE row"
        )
        assert combo_conf_dccfxcw_scene_pulse_arc_idx == combo_conf_dccfxcw_scene_pulse_legend_idx + 1, (
            "expected DCCFXCW SCENE PULSE ARC row directly after DCCFXCW SCENE PULSE LEGEND row"
        )
        assert combo_conf_dccfxcw_scene_pulse_arc_legend_idx == combo_conf_dccfxcw_scene_pulse_arc_idx + 1, (
            "expected DCCFXCW SCENE PULSE ARC LEGEND row directly after DCCFXCW SCENE PULSE ARC row"
        )
        assert combo_conf_dccfxcpa_alias_idx == combo_conf_dccfxcw_scene_pulse_arc_legend_idx + 1, (
            "expected DCCFXCPA row directly after DCCFXCW SCENE PULSE ARC LEGEND row"
        )
        assert combo_conf_dccfxcpa_legend_idx == combo_conf_dccfxcpa_alias_idx + 1, (
            "expected DCCFXCPA LEGEND row directly after DCCFXCPA row"
        )
        assert combo_conf_dccfxcpa_family_churn_idx == combo_conf_dccfxcpa_legend_idx + 1, (
            "expected DCCFXCPA FAMILY CHURN row directly after DCCFXCPA LEGEND row"
        )
        assert combo_conf_dccfxcpa_copy_idx == combo_conf_dccfxcpa_family_churn_idx + 1, (
            "expected DCCFXCPA COPY row directly after DCCFXCPA FAMILY CHURN row"
        )
        assert combo_conf_dccfxcpa_copy_alt_idx == combo_conf_dccfxcpa_copy_idx + 1, (
            "expected DCCFXCPA COPY ALT row directly after DCCFXCPA COPY row"
        )
        assert combo_conf_dccfxcpa_copy_alt_pack_idx == combo_conf_dccfxcpa_copy_alt_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK row directly after DCCFXCPA COPY ALT row"
        )
        assert combo_conf_dccfxcpa_copy_alt_pack_alias_idx == combo_conf_dccfxcpa_copy_alt_pack_idx + 1, (
            "expected DCCFXCPAP row directly after DCCFXCPA COPY ALT PACK row"
        )
        assert combo_conf_dccfxcpap_coach_idx == combo_conf_dccfxcpa_copy_alt_pack_alias_idx + 1, (
            "expected DCCFXCPAP COACH row directly after DCCFXCPAP row"
        )
        assert combo_conf_dccfxcpap_coach_legend_idx == combo_conf_dccfxcpap_coach_idx + 1, (
            "expected DCCFXCPAP COACH LEGEND row directly after DCCFXCPAP COACH row"
        )
        assert combo_conf_dccfxcpap_coach_family_churn_idx == combo_conf_dccfxcpap_coach_legend_idx + 1, (
            "expected DCCFXCPAP COACH FAMILY CHURN row directly after DCCFXCPAP COACH LEGEND row"
        )
        assert combo_conf_dccfxcpap_family_churn_idx == combo_conf_dccfxcpap_coach_family_churn_idx + 1, (
            "expected DCCFXCPAP FAMILY CHURN row directly after DCCFXCPAP COACH FAMILY CHURN row"
        )
        assert combo_conf_dccfxcpap_fx_cue_idx == combo_conf_dccfxcpap_family_churn_idx + 1, (
            "expected DCCFXCPAP FX CUE row directly after DCCFXCPAP FAMILY CHURN row"
        )
        assert combo_conf_dccfxcpap_fx_cue_legend_idx == combo_conf_dccfxcpap_fx_cue_idx + 1, (
            "expected DCCFXCPAP FX CUE LEGEND row directly after DCCFXCPAP FX CUE row"
        )
        assert combo_conf_dccfxcpa_copy_alt_legend_idx == combo_conf_dccfxcpap_fx_cue_legend_idx + 1, (
            "expected DCCFXCPA COPY ALT LEGEND row directly after DCCFXCPAP FX CUE LEGEND row"
        )
        assert combo_conf_dccfxcpa_copy_alt_pack_legend_idx == combo_conf_dccfxcpa_copy_alt_legend_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK LEGEND row directly after DCCFXCPA COPY ALT LEGEND row"
        )
        assert combo_conf_dccfxcpa_copy_legend_idx == combo_conf_dccfxcpa_copy_alt_pack_legend_idx + 1, (
            "expected DCCFXCPA COPY LEGEND row directly after DCCFXCPA COPY ALT PACK LEGEND row"
        )
        assert combo_conf_dccfxcpa_copy_family_churn_idx == combo_conf_dccfxcpa_copy_legend_idx + 1, (
            "expected DCCFXCPA COPY FAMILY CHURN row directly after DCCFXCPA COPY LEGEND row"
        )
        assert combo_conf_dccfxcpa_copy_alt_family_churn_idx == combo_conf_dccfxcpa_copy_family_churn_idx + 1, (
            "expected DCCFXCPA COPY ALT FAMILY CHURN row directly after DCCFXCPA COPY FAMILY CHURN row"
        )
        assert combo_conf_dccfxcpa_copy_alt_family_trend_idx == combo_conf_dccfxcpa_copy_alt_family_churn_idx + 1, (
            "expected DCCFXCPA COPY ALT FAMILY TREND row directly after DCCFXCPA COPY ALT FAMILY CHURN row"
        )
        assert combo_conf_dccfxcpa_copy_alt_pack_family_churn_idx == combo_conf_dccfxcpa_copy_alt_family_trend_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK FAMILY CHURN row directly after DCCFXCPA COPY ALT FAMILY TREND row"
        )
        assert combo_conf_dccfxcpa_copy_alt_pack_family_trend_idx == combo_conf_dccfxcpa_copy_alt_pack_family_churn_idx + 1, (
            "expected DCCFXCPA COPY ALT PACK FAMILY TREND row directly after DCCFXCPA COPY ALT PACK FAMILY CHURN row"
        )
        assert combo_conf_dccfxv_family_churn_idx == combo_conf_dccfxcpa_copy_alt_pack_family_trend_idx + 1, (
            "expected DCCFXV FAMILY CHURN row directly after DCCFXCPA COPY ALT PACK FAMILY TREND row"
        )
        assert combo_conf_dccfxc_family_churn_idx == combo_conf_dccfxv_family_churn_idx + 1, (
            "expected DCCFXC FAMILY CHURN row directly after DCCFXV FAMILY CHURN row"
        )
        assert combo_conf_dccfxcw_family_churn_idx == combo_conf_dccfxc_family_churn_idx + 1, (
            "expected DCCFXCW FAMILY CHURN row directly after DCCFXC FAMILY CHURN row"
        )
        assert combo_conf_copy_swap_dccsr_family_churn_idx == combo_conf_dccfxcw_family_churn_idx + 1, (
            "expected DCCSR FAMILY CHURN row directly after DCCFXCW FAMILY CHURN row"
        )
        assert combo_conf_copy_swap_dccst_family_churn_idx == combo_conf_copy_swap_dccsr_family_churn_idx + 1, (
            "expected DCCST FAMILY CHURN row directly after DCCSR FAMILY CHURN row"
        )
        assert combo_conf_copy_swap_family_trend_idx == combo_conf_copy_swap_dccst_family_churn_idx + 1, (
            "expected DMG COMBO CONF COACH COPY SWAP REC FAMILY TREND row directly after DCCST FAMILY CHURN row"
        )
        assert len(lane_cadence_miss_risk_indices) == 2, (
            "expected exactly two LANE CADENCE MISS RISK rows (summary + token-coverage sections)"
        )
        assert len(lane_cadence_miss_risk_alias_indices) == 2, (
            "expected exactly two LCMR alias rows (summary + token-coverage sections)"
        )
        assert len(lane_cadence_24h_check_indices) == 2, (
            "expected exactly two LANE CADENCE 24H CHECK rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_watchdog_indices) == 2, (
            "expected exactly two COMBAT/VFX CADENCE WATCHDOG rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_watchdog_streak_indices) == 2, (
            "expected exactly two COMBAT/VFX CADENCE WATCHDOG STREAK rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_indices) == 2, (
            "expected exactly two COMBAT/VFX CADENCE COACH rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_indices) == 2, (
            "expected exactly two COMBAT/VFX CADENCE COACH WHY rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_alias_indices) == 2, (
            "expected exactly two CVCW alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_alias_indices) == 2, (
            "expected exactly two CVCWH alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_indices) == 2, (
            "expected exactly two CVCWHR recommendation rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_indices) == 2, (
            "expected exactly two CVCWHR CONF rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_alias_indices) == 2, (
            "expected exactly two CVCWHRC alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_indices) == 2, (
            "expected exactly two CVCWHR CONF FLOOR REC rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_alias_indices) == 2, (
            "expected exactly two CVCWHRF alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_indices) == 2, (
            "expected exactly two CVCWHR FX PULSE rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_indices) == 2, (
            "expected exactly two CVCWHR FX PULSE LEGEND rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_rec_indices) == 2, (
            "expected exactly two CVCWHR FX PULSE LEGEND REC rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_rec_conf_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND REC CONF rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND COPY PACK rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_alias_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND CP alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND COPY PACK TREND rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_alias_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND CPT alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND COPY PACK TREND CONF rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_alias_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND CPTC alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_alias_legend_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND CPTC LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_indices) == 2, (
            "expected exactly two CADENCE BRIDGE rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_family_churn_indices) == 2, (
            "expected exactly two CVCWHR CONF FLOOR + CVCWHRF FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_family_churn_indices) == 2, (
            "expected exactly two CVCWHR FX PULSE FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_family_trend_indices) == 2, (
            "expected exactly two CVCWHR FX PULSE FAMILY TREND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_family_churn_indices) == 2, (
            "expected exactly two CADENCE BRIDGE FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_indices) == 2, (
            "expected exactly two CADENCE BRIDGE GLYPH rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_indices) == 2, (
            "expected exactly two CADENCE BRIDGE GLYPH CONF rows (summary + token-coverage sections)"
        )
        if cadence_bridge_glyph_conf_compact_alias_enabled:
            assert len(cadence_bridge_glyph_conf_compact_alias_indices) == 2, (
                "expected exactly two CBGC alias rows (summary + token-coverage sections)"
            )
        else:
            assert len(cadence_bridge_glyph_conf_compact_alias_indices) == 0, (
                "expected no CBGC alias rows when compact alias flag is disabled"
            )
        assert len(cadence_bridge_glyph_conf_compact_alias_legend_indices) == 2, (
            "expected exactly two CBGC LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_compact_legend_alias_indices) == 2, (
            "expected exactly two CBGCL rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_intent_compact_active_alias_indices) == 2, (
            "expected exactly two CBGCIA rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_intent_compact_active_alias_family_churn_indices) == 2, (
            "expected exactly two CBGCIA FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_regime_alias_indices) == 2, (
            "expected exactly two CBGCFXR rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_regime_alias_family_churn_indices) == 2, (
            "expected exactly two CBGCFXR FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_indices) == 2, (
            "expected exactly two CBGCFXA rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_family_churn_indices) == 2, (
            "expected exactly two CBGCFXA FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_indices) == 2, (
            "expected exactly two CBGC FX HINT rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_family_churn_indices) == 2, (
            "expected exactly two CBGC FX HINT FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_indices) == 2, (
            "expected exactly two CBGCFXH rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_family_churn_indices) == 2, (
            "expected exactly two CBGCFXH FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_indices) == 2, (
            "expected exactly two CBGCFXW rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_family_churn_indices) == 2, (
            "expected exactly two CBGCFXW FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_legend_indices) == 2, (
            "expected exactly two CBGCFXW LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_indices) == 2, (
            "expected exactly two CBGCFXW COHERENCE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_indices) == 2, (
            "expected exactly two CBGCFXW COHERENCE MOMENTUM rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_indices) == 2, (
            "expected exactly two CBGCFXWM rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_legend_indices) == 2, (
            "expected exactly two CBGCFXWM LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_indices) == 2, (
            "expected exactly two CBGCFXWC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_legend_indices) == 2, (
            "expected exactly two CBGCFXWC LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_family_churn_indices) == 2, (
            "expected exactly two CBGCFXWC FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_drift_indices) == 2, (
            "expected exactly two CBGCFXWAC DRIFT rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_momentum_indices) == 2, (
            "expected exactly two CBGCFXWAC MOMENTUM rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_momentum_family_churn_indices) == 2, (
            "expected exactly two CBGCFXWAC MOMENTUM FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_indices) == 2, (
            "expected exactly two CBGCFXWSB rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_family_churn_indices) == 2, (
            "expected exactly two CBGCFXWSB FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_indices) == 2, (
            "expected exactly two CBGCFXWSBP rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_family_churn_indices) == 2, (
            "expected exactly two CBGCFXWSBP FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_indices) == 2, (
            "expected exactly two CBGCFXWSBP FX CUE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_indices) == 2, (
            "expected exactly two CBGCFXWSBPFC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_indices) == 2, (
            "expected exactly two CBGCFXWSBPFCI rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_indices) == 2, (
            "expected exactly two CBGCFXWSBPFXP rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_decode_microline_pair_indices) == 2, (
            "expected exactly two CBGCFXWSBPFXP MICROLINE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_legend_indices) == 2, (
            "expected exactly two CBGCFXWSBPFXP MICROLINE LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_legend_indices) == 2, (
            "expected exactly two CBGCFXWSBPFCI LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_indices) == 2, (
            "expected exactly two CBGCFXWSBPFCI COACH COPY rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_indices) in {1, 2}, (
            "expected one or exactly two CBGCFXWSBPFXP LANG rows (summary-only or summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPI rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_indices), (
            "expected CBGCFXWSBPFXPI rollout rows to appear only when CBGCFXWSBPFXP LANG rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPI LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices), (
            "expected CBGCFXWSBPFXPI LEGEND rollout rows to appear only when CBGCFXWSBPFXPI rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPI LEGEND COPY rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_indices), (
            "expected CBGCFXWSBPFXPI LEGEND COPY rollout rows to appear only when CBGCFXWSBPFXPI LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPIC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_indices), (
            "expected CBGCFXWSBPFXPIC rollout rows to appear only when CBGCFXWSBPFXPI LEGEND COPY rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPI NARR rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices), (
            "expected CBGCFXWSBPFXPI NARR rollout rows to appear only when CBGCFXWSBPFXPI rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPIN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_indices), (
            "expected CBGCFXWSBPFXPIN rollout rows to appear only when CBGCFXWSBPFXPI NARR rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPIN LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_indices), (
            "expected CBGCFXWSBPFXPIN LEGEND rollout rows to appear only when CBGCFXWSBPFXPIN rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPINF rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPINF rollout rows to appear only when CBGCFXWSBPFXPIN LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPINF LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_indices), (
            "expected CBGCFXWSBPFXPINF LEGEND rollout rows to appear only when CBGCFXWSBPFXPINF rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPINF ORDER rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_indices), (
            "expected CBGCFXWSBPFXPINF ORDER rollout rows to appear only when CBGCFXWSBPFXPINF LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPI DRILL rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPD rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_indices) in {0, 1, 2}, (
            "expected zero, one, or exactly two CBGCFXWSBPFXPD MICROLINE rows (summary-only or summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_legend_indices) in {0, 1, 2}, (
            "expected zero, one, or exactly two CBGCFXWSBPFXPD MICROLINE LEGEND rows (summary-only or summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPD COACH rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPD COACH WHY rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW COPY PACK rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW COPY PACK LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW COPY PACK CADENCE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWC LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW FX CUE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCW FX CUE LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWF rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWF LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWF DIGEST rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWF COHERENCE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWF COHERENCE LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFC LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCT rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCT LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTA rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTA LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTA DIGEST rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTA RFALL rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTA RFALL LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_indices) in {0, 2}, (
            "expected zero or exactly two CTA REVIEW CADENCE NOTE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_indices) in {0, 2}, (
            "expected zero or exactly two CTA REVIEW CADENCE NOTE LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAN LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAP rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAP LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAS rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAS LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAS CPACK rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPD ECHO rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE MATRIX rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE MATRIX DRIFT rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices), (
            "expected CBGCFXWSBPFXPI DRILL rollout rows to appear only when CBGCFXWSBPFXPI rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_indices), (
            "expected CBGCFXWSBPFXPD rollout rows to appear only when CBGCFXWSBPFXPI DRILL rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_indices), (
            "expected CBGCFXWSBPFXPD MICROLINE rollout rows to appear only when CBGCFXWSBPFXP LANG rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_indices), (
            "expected CBGCFXWSBPFXPD MICROLINE LEGEND rows to appear only when CBGCFXWSBPFXPD MICROLINE rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_legend_indices), (
            "expected CBGCFXWSBPFXPD COACH rows to appear only when CBGCFXWSBPFXPD MICROLINE LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_indices), (
            "expected CBGCFXWSBPFXPDC rows to appear only when CBGCFXWSBPFXPD COACH rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_compact_alias_indices), (
            "expected CBGCFXWSBPFXPD COACH WHY rows to appear only when CBGCFXWSBPFXPDC rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_indices), (
            "expected CBGCFXWSBPFXPDCW rows to appear only when CBGCFXWSBPFXPD COACH WHY rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_indices), (
            "expected CBGCFXWSBPFXPDCW LEGEND rows to appear only when CBGCFXWSBPFXPDCW rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCW COPY PACK rows to appear only when CBGCFXWSBPFXPDCW LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_indices), (
            "expected CBGCFXWSBPFXPDCW COPY PACK LEGEND rows to appear only when CBGCFXWSBPFXPDCW COPY PACK rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_legend_indices), (
            "expected CBGCFXWSBPFXPDCW COPY PACK CADENCE rows to appear only when CBGCFXWSBPFXPDCW COPY PACK LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_indices), (
            "expected CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND rows to appear only when CBGCFXWSBPFXPDCW COPY PACK CADENCE rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_legend_indices), (
            "expected CBGCFXWSBPFXPDCWC rows to appear only when CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_indices), (
            "expected CBGCFXWSBPFXPDCWC LEGEND rows to appear only when CBGCFXWSBPFXPDCWC rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCW FX CUE rows to appear only when CBGCFXWSBPFXPDCWC LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_indices), (
            "expected CBGCFXWSBPFXPDCW FX CUE LEGEND rows to appear only when CBGCFXWSBPFXPDCW FX CUE rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_indices), (
            "expected CBGCFXWSBPFXPDCWF rows to appear only when CBGCFXWSBPFXPDCW FX CUE LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_indices), (
            "expected CBGCFXWSBPFXPDCWF LEGEND rows to appear only when CBGCFXWSBPFXPDCWF rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCWF DIGEST rows to appear only when CBGCFXWSBPFXPDCWF LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_indices), (
            "expected CBGCFXWSBPFXPDCWF COHERENCE rows to appear only when CBGCFXWSBPFXPDCWF DIGEST rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_indices), (
            "expected CBGCFXWSBPFXPDCWF COHERENCE LEGEND rows to appear only when CBGCFXWSBPFXPDCWF COHERENCE rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFC rows to appear only when CBGCFXWSBPFXPDCWF COHERENCE LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_indices), (
            "expected CBGCFXWSBPFXPDCWFC LEGEND rows to appear only when CBGCFXWSBPFXPDCWFC rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCT rows to appear only when CBGCFXWSBPFXPDCWFC LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_indices), (
            "expected CBGCFXWSBPFXPDCWFCT LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCT rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCTA rows to appear only when CBGCFXWSBPFXPDCWFCT LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_indices), (
            "expected CBGCFXWSBPFXPDCWFCTA LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCTA rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCTA DIGEST rows to appear only when CBGCFXWSBPFXPDCWFCTA LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_indices), (
            "expected CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCTA DIGEST rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCTA RFALL rows to appear only when CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_indices), (
            "expected CBGCFXWSBPFXPDCWFCTA RFALL LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCTA RFALL rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_indices), (
            "expected CTA REVIEW CADENCE NOTE rows to appear only when CBGCFXWSBPFXPDCWFCTA RFALL LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_indices), (
            "expected CTA REVIEW CADENCE NOTE LEGEND rows to appear only when CTA REVIEW CADENCE NOTE rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAN rows to appear only when CTA REVIEW CADENCE NOTE LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAN LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCTAN rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAP rows to appear only when CBGCFXWSBPFXPDCWFCTAN LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAP LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCTAP rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAS rows to appear only when CBGCFXWSBPFXPDCWFCTAP LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAS LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCTAS rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAS CPACK rows to appear only when CBGCFXWSBPFXPDCWFCTAS LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_indices), (
            "expected CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND rows to appear only when CBGCFXWSBPFXPDCWFCTAS CPACK rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_legend_indices), (
            "expected CBGCFXWSBPFXPD ECHO rows to appear only when CBGCFXWSBPFXPD MICROLINE LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_indices), (
            "expected CBGCFXWSBPFXPDE rows to appear only when CBGCFXWSBPFXPD ECHO rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_indices), (
            "expected CBGCFXWSBPFXPDE LEGEND rows to appear only when CBGCFXWSBPFXPDE rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDE MATRIX rows to appear only when CBGCFXWSBPFXPDE LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_indices), (
            "expected CBGCFXWSBPFXPDE MATRIX DRIFT rows to appear only when CBGCFXWSBPFXPDE MATRIX rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_trend_band_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE MATRIX DRIFT TREND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_trend_band_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_indices), (
            "expected CBGCFXWSBPFXPDE MATRIX DRIFT TREND rows to appear only when CBGCFXWSBPFXPDE MATRIX DRIFT rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_trend_band_indices), (
            "expected CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT rows to appear only when CBGCFXWSBPFXPDE MATRIX DRIFT TREND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDS rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_indices), (
            "expected CBGCFXWSBPFXPDS rows to appear only when CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_legend_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDS LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_indices), (
            "expected CBGCFXWSBPFXPDS LEGEND rows to appear only when CBGCFXWSBPFXPDS rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_profiler_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE POLICY OPS WINDOW rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_profiler_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_legend_indices), (
            "expected CBGCFXWSBPFXPDE POLICY OPS WINDOW rows to appear only when CBGCFXWSBPFXPDS LEGEND rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_indices) in {0, 2}, (
            "expected zero or exactly two CBGCFXWSBPFXPDE POLICY OPS DOMINANT rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_profiler_indices), (
            "expected CBGCFXWSBPFXPDE POLICY OPS DOMINANT rows to appear only when CBGCFXWSBPFXPDE POLICY OPS WINDOW rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_legend_indices) <= len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_indices), (
            "expected CBGCFXWSBPFXPDE POLICY OPS DOMINANT LEGEND rows to appear only when CBGCFXWSBPFXPDE POLICY OPS DOMINANT rows are present"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_indices) == 2, (
            "expected exactly two CBGCFXWAC COACH COPY REC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_compact_alias_indices) == 2, (
            "expected exactly two CBGCFXWACRC rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_compact_alias_legend_indices) == 2, (
            "expected exactly two CBGCFXWACRC LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_reason_priority_alias_indices) == 2, (
            "expected exactly two CBGCFXWACRP rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_reason_priority_alias_legend_indices) == 2, (
            "expected exactly two CBGCFXWACRP LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_indices) == 2, (
            "expected exactly two CBGCFXW DRIFT rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_family_churn_indices) == 2, (
            "expected exactly two CBGCFXW DRIFT FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_intent_compact_alias_indices) == 2, (
            "expected exactly two CBGCI rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_intent_legend_indices) == 2, (
            "expected exactly two CBGCI LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_intent_legend_alias_indices) == 2, (
            "expected exactly two CBGCIL rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_conf_legend_indices) == 2, (
            "expected exactly two CADENCE BRIDGE GLYPH CONF LEGEND rows (summary + token-coverage sections)"
        )
        assert len(cadence_bridge_glyph_legend_indices) == 2, (
            "expected exactly two CADENCE BRIDGE GLYPH LEGEND rows (summary + token-coverage sections)"
        )
        token_totals_heading_idx = md_lines.index("## Token Totals (added/removed/net)")
        token_family_coverage_heading_idx = md_lines.index("## Token Family Coverage")
        route_vibe_drift_heading_idx = md_lines.index("## Route Vibe Drift (added/removed/net)")

        first_conf_legend_idx, second_conf_legend_idx = cadence_bridge_glyph_conf_legend_indices
        assert first_conf_legend_idx < token_totals_heading_idx, (
            "expected first CADENCE BRIDGE GLYPH CONF LEGEND row in summary section before token totals"
        )
        assert token_family_coverage_heading_idx < second_conf_legend_idx < route_vibe_drift_heading_idx, (
            "expected second CADENCE BRIDGE GLYPH CONF LEGEND row in token-coverage section"
        )

        # Game Director Cycle GR lock: keep coach alias drift->momentum chain deterministic.
        for section_idx, (section_name, drift_idx, momentum_idx, momentum_family_churn_idx, storybeat_idx, storybeat_family_churn_idx, storybeat_phase_idx, storybeat_phase_family_churn_idx, storybeat_phase_fx_cue_idx, storybeat_phase_fx_cue_compact_alias_idx, storybeat_phase_fx_cue_compact_alias_intensity_idx, storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_idx, storybeat_phase_fx_cue_intensity_pulse_decode_microline_pair_idx, storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_legend_idx, storybeat_phase_fx_cue_compact_alias_intensity_legend_idx, storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_idx, coach_copy_variant_rec_idx, coach_copy_variant_rec_compact_alias_idx, coach_copy_variant_rec_compact_alias_legend_idx, coach_copy_reason_priority_alias_idx, coach_copy_reason_priority_alias_legend_idx, coherence_alias_idx) in enumerate(zip(
            ("summary", "token-coverage"),
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_drift_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_momentum_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_alias_momentum_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_decode_microline_pair_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_legend_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_legend_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_compact_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_compact_alias_legend_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_reason_priority_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_reason_priority_alias_legend_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_indices,
        )):
            assert momentum_idx == drift_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWAC MOMENTUM row directly after CBGCFXWAC DRIFT row"
            )
            assert momentum_family_churn_idx == momentum_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWAC MOMENTUM FAMILY CHURN row directly after CBGCFXWAC MOMENTUM row"
            )
            assert storybeat_idx == momentum_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSB row directly after CBGCFXWAC MOMENTUM FAMILY CHURN row"
            )
            assert storybeat_family_churn_idx == storybeat_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSB FAMILY CHURN row directly after CBGCFXWSB row"
            )
            assert storybeat_phase_idx == storybeat_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBP row directly after CBGCFXWSB FAMILY CHURN row"
            )
            assert storybeat_phase_family_churn_idx == storybeat_phase_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBP FAMILY CHURN row directly after CBGCFXWSBP row"
            )
            assert storybeat_phase_fx_cue_idx == storybeat_phase_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBP FX CUE row directly after CBGCFXWSBP FAMILY CHURN row"
            )
            assert storybeat_phase_fx_cue_compact_alias_idx == storybeat_phase_fx_cue_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFC row directly after CBGCFXWSBP FX CUE row"
            )
            assert storybeat_phase_fx_cue_compact_alias_intensity_idx == storybeat_phase_fx_cue_compact_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFCI row directly after CBGCFXWSBPFC row"
            )
            assert storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_idx == storybeat_phase_fx_cue_compact_alias_intensity_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXP row directly after CBGCFXWSBPFCI row"
            )
            assert storybeat_phase_fx_cue_intensity_pulse_decode_microline_pair_idx == storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXP MICROLINE row directly after CBGCFXWSBPFXP row"
            )
            assert storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_legend_idx == storybeat_phase_fx_cue_intensity_pulse_decode_microline_pair_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXP MICROLINE LEGEND row directly after CBGCFXWSBPFXP MICROLINE row"
            )
            assert storybeat_phase_fx_cue_compact_alias_intensity_legend_idx == storybeat_phase_fx_cue_compact_alias_intensity_pulse_alias_legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFCI LEGEND row directly after CBGCFXWSBPFXP MICROLINE LEGEND row"
            )
            assert storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_idx == storybeat_phase_fx_cue_compact_alias_intensity_legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFCI COACH COPY row directly after CBGCFXWSBPFCI LEGEND row"
            )
            assert coach_copy_variant_rec_idx >= storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_idx + 1 and coach_copy_variant_rec_idx <= storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_idx + 68, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWAC COACH COPY REC row immediately after CBGCFXWSBPFCI COACH COPY row, with optional rollout spacers CBGCFXWSBPFXP LANG -> CBGCFXWSBPFXPI -> CBGCFXWSBPFXPI LEGEND -> CBGCFXWSBPFXPI LEGEND COPY -> CBGCFXWSBPFXPIC -> CBGCFXWSBPFXPI NARR -> CBGCFXWSBPFXPIN -> CBGCFXWSBPFXPIN LEGEND -> CBGCFXWSBPFXPINF -> CBGCFXWSBPFXPINF LEGEND -> CBGCFXWSBPFXPINF ORDER -> CBGCFXWSBPFXPI DRILL -> CBGCFXWSBPFXPD -> CBGCFXWSBPFXPD MICROLINE -> CBGCFXWSBPFXPD MICROLINE LEGEND -> CBGCFXWSBPFXPD COACH -> CBGCFXWSBPFXPDC -> CBGCFXWSBPFXPD COACH WHY -> CBGCFXWSBPFXPDCW -> CBGCFXWSBPFXPDCW LEGEND -> CBGCFXWSBPFXPDCW COPY PACK -> CBGCFXWSBPFXPDCW COPY PACK LEGEND -> CBGCFXWSBPFXPDCW COPY PACK CADENCE -> CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND -> CBGCFXWSBPFXPDCWC -> CBGCFXWSBPFXPDCWC LEGEND -> CBGCFXWSBPFXPDCW FX CUE -> CBGCFXWSBPFXPDCW FX CUE LEGEND -> CBGCFXWSBPFXPDCWF -> CBGCFXWSBPFXPDCWF LEGEND -> CBGCFXWSBPFXPDCWF DIGEST -> CBGCFXWSBPFXPDCWF COHERENCE -> CBGCFXWSBPFXPDCWF COHERENCE LEGEND -> CBGCFXWSBPFXPDCWFC -> CBGCFXWSBPFXPDCWFC LEGEND -> CBGCFXWSBPFXPDCWFCT -> CBGCFXWSBPFXPDCWFCT LEGEND -> CBGCFXWSBPFXPDCWFCTA -> CBGCFXWSBPFXPDCWFCTA LEGEND -> CBGCFXWSBPFXPDCWFCTA DIGEST -> CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND -> CBGCFXWSBPFXPDCWFCTA RFALL -> CBGCFXWSBPFXPDCWFCTA RFALL LEGEND -> CTA REVIEW CADENCE NOTE -> CTA REVIEW CADENCE NOTE LEGEND -> CBGCFXWSBPFXPDCWFCTAN -> CBGCFXWSBPFXPDCWFCTAN LEGEND -> CBGCFXWSBPFXPDCWFCTAP -> CBGCFXWSBPFXPDCWFCTAP LEGEND -> CBGCFXWSBPFXPDCWFCTAS -> CBGCFXWSBPFXPDCWFCTAS LEGEND -> CBGCFXWSBPFXPDCWFCTAS CPACK -> CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND -> CBGCFXWSBPFXPD ECHO -> CBGCFXWSBPFXPDE -> CBGCFXWSBPFXPDE LEGEND -> CBGCFXWSBPFXPDE MATRIX -> CBGCFXWSBPFXPDE MATRIX DRIFT -> CBGCFXWSBPFXPDE MATRIX DRIFT TREND -> CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT -> CBGCFXWSBPFXPDS -> CBGCFXWSBPFXPDS LEGEND -> CBGCFXWSBPFXPDE SNAPSHOT POLICY -> CBGCFXWSBPFXPDE POLICY OPS WINDOW -> CBGCFXWSBPFXPDE POLICY OPS DOMINANT -> CBGCFXWSBPFXPDE POLICY OPS DOMINANT LEGEND"
            )
            spacer_lines = md_lines[
                storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_idx + 1 : coach_copy_variant_rec_idx
            ]
            expected_spacer_prefixes = [
                "- CBGCFXWSBPFXP LANG:",
                "- CBGCFXWSBPFXPI:",
                "- CBGCFXWSBPFXPI LEGEND:",
                "- CBGCFXWSBPFXPI LEGEND COPY:",
                "- CBGCFXWSBPFXPIC:",
                "- CBGCFXWSBPFXPI NARR:",
                "- CBGCFXWSBPFXPIN:",
                "- CBGCFXWSBPFXPIN LEGEND:",
                "- CBGCFXWSBPFXPINF:",
                "- CBGCFXWSBPFXPINF LEGEND:",
                "- CBGCFXWSBPFXPINF ORDER:",
                "- CBGCFXWSBPFXPI DRILL:",
                "- CBGCFXWSBPFXPD:",
                "- CBGCFXWSBPFXPD MICROLINE:",
                "- CBGCFXWSBPFXPD MICROLINE LEGEND:",
                "- CBGCFXWSBPFXPD COACH:",
                "- CBGCFXWSBPFXPDC:",
                "- CBGCFXWSBPFXPD COACH WHY:",
                "- CBGCFXWSBPFXPDCW:",
                "- CBGCFXWSBPFXPDCW LEGEND:",
                "- CBGCFXWSBPFXPDCW COPY PACK:",
                "- CBGCFXWSBPFXPDCW COPY PACK LEGEND:",
                "- CBGCFXWSBPFXPDCW COPY PACK CADENCE:",
                "- CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND:",
                "- CBGCFXWSBPFXPDCWC:",
                "- CBGCFXWSBPFXPDCWC LEGEND:",
                "- CBGCFXWSBPFXPDCW FX CUE:",
                "- CBGCFXWSBPFXPDCW FX CUE LEGEND:",
                "- CBGCFXWSBPFXPDCWF:",
                "- CBGCFXWSBPFXPDCWF LEGEND:",
                "- CBGCFXWSBPFXPDCWF DIGEST:",
                "- CBGCFXWSBPFXPDCWF COHERENCE:",
                "- CBGCFXWSBPFXPDCWF COHERENCE LEGEND:",
                "- CBGCFXWSBPFXPDCWFC:",
                "- CBGCFXWSBPFXPDCWFC LEGEND:",
                "- CBGCFXWSBPFXPDCWFCT:",
                "- CBGCFXWSBPFXPDCWFCT LEGEND:",
                "- CBGCFXWSBPFXPDCWFCTA:",
                "- CBGCFXWSBPFXPDCWFCTA LEGEND:",
                "- CBGCFXWSBPFXPDCWFCTA DIGEST:",
                "- CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND:",
                "- CBGCFXWSBPFXPDCWFCTA RFALL:",
                "- CBGCFXWSBPFXPDCWFCTA RFALL LEGEND:",
                "- CTA REVIEW CADENCE NOTE:",
                "- CTA REVIEW CADENCE NOTE LEGEND:",
                "- CBGCFXWSBPFXPDCWFCTAN:",
                "- CBGCFXWSBPFXPDCWFCTAN LEGEND:",
                "- CBGCFXWSBPFXPDCWFCTAP:",
                "- CBGCFXWSBPFXPDCWFCTAP LEGEND:",
                "- CBGCFXWSBPFXPDCWFCTAS:",
                "- CBGCFXWSBPFXPDCWFCTAS LEGEND:",
                "- CBGCFXWSBPFXPDCWFCTAS CPACK:",
                "- CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND:",
                "- CBGCFXWSBPFXPD ECHO:",
                "- CBGCFXWSBPFXPDE:",
                "- CBGCFXWSBPFXPDE LEGEND:",
                "- CBGCFXWSBPFXPDE MATRIX:",
                "- CBGCFXWSBPFXPDE MATRIX DRIFT:",
                "- CBGCFXWSBPFXPDE MATRIX DRIFT TREND:",
                "- CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT:",
                "- CBGCFXWSBPFXPDS:",
                "- CBGCFXWSBPFXPDS LEGEND:",
                "- CBGCFXWSBPFXPDE SNAPSHOT POLICY:",
                "- CBGCFXWSBPFXPDE POLICY OPS WINDOW:",
                "- CBGCFXWSBPFXPDE POLICY OPS DOMINANT:",
                "- CBGCFXWSBPFXPDE POLICY OPS DOMINANT LEGEND:",
            ]
            assert len(spacer_lines) <= len(expected_spacer_prefixes), (
                f"markdown contract violated in {section_name} section: expected at most {len(expected_spacer_prefixes)} rollout spacers before CBGCFXWAC COACH COPY REC"
            )
            last_prefix_idx = -1
            for spacer_idx, spacer_line in enumerate(spacer_lines):
                matched_prefix_idx = next(
                    (i for i, prefix in enumerate(expected_spacer_prefixes) if spacer_line.startswith(prefix)),
                    None,
                )
                assert matched_prefix_idx is not None, (
                    f"markdown contract violated in {section_name} section: unexpected spacer token order before CBGCFXWAC COACH COPY REC"
                )
                assert matched_prefix_idx > last_prefix_idx, (
                    f"markdown contract violated in {section_name} section: rollout spacers must preserve forward token order"
                )
                last_prefix_idx = matched_prefix_idx

            optional_spacer_prefix_to_index = {
                prefix: i for i, prefix in enumerate(expected_spacer_prefixes)
            }
            optional_phase_intent_narration_compact_alias_prefix_idx = optional_spacer_prefix_to_index["- CBGCFXWSBPFXPIN:"]
            optional_phase_intent_narration_compact_alias_legend_prefix_idx = optional_spacer_prefix_to_index["- CBGCFXWSBPFXPIN LEGEND:"]
            optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_prefix_idx = optional_spacer_prefix_to_index["- CBGCFXWSBPFXPINF:"]
            optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_prefix_idx = optional_spacer_prefix_to_index["- CBGCFXWSBPFXPINF LEGEND:"]
            optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_prefix_idx = optional_spacer_prefix_to_index["- CBGCFXWSBPFXPINF ORDER:"]
            assert optional_phase_intent_narration_compact_alias_prefix_idx < optional_phase_intent_narration_compact_alias_legend_prefix_idx < optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_prefix_idx < optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_prefix_idx < optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_prefix_idx, (
                "markdown contract violated: expected optional narration compact alias rollout ordering "
                "CBGCFXWSBPFXPIN -> CBGCFXWSBPFXPIN LEGEND -> CBGCFXWSBPFXPINF -> CBGCFXWSBPFXPINF LEGEND -> CBGCFXWSBPFXPINF ORDER"
            )

            optional_lang_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_indices) == 2
                else None
            )
            optional_phase_intent_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_indices) == 2
                else None
            )
            optional_phase_intent_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_indices) == 2
                else None
            )
            optional_phase_intent_alias_legend_copy_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_indices) == 2
                else None
            )
            optional_phase_intent_alias_legend_copy_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_alias_legend_copy_compact_alias_indices) == 2
                else None
            )
            optional_phase_intent_narration_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_indices) == 2
                else None
            )
            if optional_lang_idx is not None:
                assert optional_lang_idx == storybeat_phase_fx_cue_compact_alias_intensity_coach_copy_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXP LANG row directly after CBGCFXWSBPFCI COACH COPY when LANG rollout rows exist"
                )
            if optional_phase_intent_alias_idx is not None:
                assert optional_lang_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPI row cannot appear without CBGCFXWSBPFXP LANG row"
                )
                assert optional_phase_intent_alias_idx == optional_lang_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPI row directly after CBGCFXWSBPFXP LANG row"
                )
            if optional_phase_intent_alias_legend_idx is not None:
                assert optional_phase_intent_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPI LEGEND row cannot appear without CBGCFXWSBPFXPI row"
                )
                assert optional_phase_intent_alias_legend_idx == optional_phase_intent_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPI LEGEND row directly after CBGCFXWSBPFXPI row"
                )
            if optional_phase_intent_alias_legend_copy_idx is not None:
                assert optional_phase_intent_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPI LEGEND COPY row cannot appear without CBGCFXWSBPFXPI LEGEND row"
                )
                assert optional_phase_intent_alias_legend_copy_idx == optional_phase_intent_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPI LEGEND COPY row directly after CBGCFXWSBPFXPI LEGEND row"
                )
            if optional_phase_intent_alias_legend_copy_compact_alias_idx is not None:
                assert optional_phase_intent_alias_legend_copy_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPIC row cannot appear without CBGCFXWSBPFXPI LEGEND COPY row"
                )
                assert optional_phase_intent_alias_legend_copy_compact_alias_idx == optional_phase_intent_alias_legend_copy_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPIC row directly after CBGCFXWSBPFXPI LEGEND COPY row"
                )
            if optional_phase_intent_narration_idx is not None:
                expected_prior_idx = optional_phase_intent_alias_legend_copy_compact_alias_idx if optional_phase_intent_alias_legend_copy_compact_alias_idx is not None else (optional_phase_intent_alias_legend_copy_idx if optional_phase_intent_alias_legend_copy_idx is not None else (optional_phase_intent_alias_legend_idx if optional_phase_intent_alias_legend_idx is not None else optional_phase_intent_alias_idx))
                expected_prior_label = "CBGCFXWSBPFXPIC" if optional_phase_intent_alias_legend_copy_compact_alias_idx is not None else ("CBGCFXWSBPFXPI LEGEND COPY" if optional_phase_intent_alias_legend_copy_idx is not None else ("CBGCFXWSBPFXPI LEGEND" if optional_phase_intent_alias_legend_idx is not None else "CBGCFXWSBPFXPI"))
                assert expected_prior_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPI NARR row cannot appear without CBGCFXWSBPFXPI row"
                )
                assert optional_phase_intent_narration_idx == expected_prior_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPI NARR row directly after {expected_prior_label} row"
                )

            optional_phase_intent_narration_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_indices) == 2
                else None
            )
            optional_phase_intent_narration_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_legend_indices) == 2
                else None
            )
            optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_indices) == 2
                else None
            )
            optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_indices) == 2
                else None
            )
            optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_indices) == 2
                else None
            )
            if optional_phase_intent_narration_compact_alias_idx is not None:
                assert optional_phase_intent_narration_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPIN row cannot appear without CBGCFXWSBPFXPI NARR row"
                )
                assert optional_phase_intent_narration_compact_alias_idx == optional_phase_intent_narration_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPIN row directly after CBGCFXWSBPFXPI NARR row"
                )
            if optional_phase_intent_narration_compact_alias_legend_idx is not None:
                assert optional_phase_intent_narration_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPIN LEGEND row cannot appear without CBGCFXWSBPFXPIN row"
                )
                assert optional_phase_intent_narration_compact_alias_legend_idx == optional_phase_intent_narration_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPIN LEGEND row directly after CBGCFXWSBPFXPIN row"
                )
            if optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_idx is not None:
                assert optional_phase_intent_narration_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPINF row cannot appear without CBGCFXWSBPFXPIN LEGEND row"
                )
                assert optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_idx == optional_phase_intent_narration_compact_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPINF row directly after CBGCFXWSBPFXPIN LEGEND row"
                )
            if optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_idx is not None:
                assert optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPINF LEGEND row cannot appear without CBGCFXWSBPFXPINF row"
                )
                assert optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_idx == optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPINF LEGEND row directly after CBGCFXWSBPFXPINF row"
                )

            optional_rehearsal_hint_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_indices) == 2
                else None
            )
            optional_rehearsal_hint_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_compact_alias_microline_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_indices) == 2
                else None
            )
            optional_rehearsal_hint_compact_alias_microline_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_microline_vocabulary_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_indices) == 2
                else None
            )
            optional_rehearsal_hint_compact_alias_coach_action_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_indices) == 2
                else None
            )
            optional_rehearsal_hint_compact_alias_coach_action_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_compact_alias_coach_action_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_compact_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_variants_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_compact_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_indices) == 2
                else None
            )
            optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_compact_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_matrix_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_matrix_drift_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_matrix_drift_trend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_trend_band_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_trend_band_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_playtest_snapshot_compact_alias_legend_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_profiler_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_profiler_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_profiler_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_indices) == 2
                else None
            )
            optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_legend_idx = (
                cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_legend_indices[section_idx]
                if len(cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_legend_indices) == 2
                else None
            )
            if optional_rehearsal_hint_idx is not None:
                assert optional_phase_intent_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPI DRILL row cannot appear without CBGCFXWSBPFXPI row"
                )
                if optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_idx is not None:
                    expected_prior_idx = optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_idx
                    expected_prior_label = "CBGCFXWSBPFXPINF ORDER"
                elif optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_idx is not None:
                    expected_prior_idx = optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_idx
                    expected_prior_label = "CBGCFXWSBPFXPINF LEGEND"
                elif optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_idx is not None:
                    expected_prior_idx = optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_idx
                    expected_prior_label = "CBGCFXWSBPFXPINF"
                elif optional_phase_intent_narration_compact_alias_legend_idx is not None:
                    expected_prior_idx = optional_phase_intent_narration_compact_alias_legend_idx
                    expected_prior_label = "CBGCFXWSBPFXPIN LEGEND"
                elif optional_phase_intent_narration_compact_alias_idx is not None:
                    expected_prior_idx = optional_phase_intent_narration_compact_alias_idx
                    expected_prior_label = "CBGCFXWSBPFXPIN"
                elif optional_phase_intent_narration_idx is not None:
                    expected_prior_idx = optional_phase_intent_narration_idx
                    expected_prior_label = "CBGCFXWSBPFXPI NARR"
                else:
                    expected_prior_idx = optional_phase_intent_alias_idx
                    expected_prior_label = "CBGCFXWSBPFXPI"
                assert optional_rehearsal_hint_idx == expected_prior_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPI DRILL row directly after {expected_prior_label} row"
                )
            if optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_idx is not None:
                assert optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPINF ORDER row cannot appear without CBGCFXWSBPFXPINF LEGEND row"
                )
                assert optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_order_idx == optional_phase_intent_narration_compact_alias_combat_vfx_fx_cue_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPINF ORDER row directly after CBGCFXWSBPFXPINF LEGEND row"
                )
            if optional_rehearsal_hint_compact_alias_idx is not None:
                assert optional_rehearsal_hint_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPD row cannot appear without CBGCFXWSBPFXPI DRILL row"
                )
                assert optional_rehearsal_hint_compact_alias_idx == optional_rehearsal_hint_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPD row directly after CBGCFXWSBPFXPI DRILL row"
                )
            if optional_rehearsal_hint_compact_alias_microline_idx is not None:
                assert optional_rehearsal_hint_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPD MICROLINE row cannot appear without CBGCFXWSBPFXPD row"
                )
                assert optional_rehearsal_hint_compact_alias_microline_idx == optional_rehearsal_hint_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPD MICROLINE row directly after CBGCFXWSBPFXPD row"
                )
            if optional_rehearsal_hint_compact_alias_microline_legend_idx is not None:
                assert optional_rehearsal_hint_compact_alias_microline_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPD MICROLINE LEGEND row cannot appear without CBGCFXWSBPFXPD MICROLINE row"
                )
                assert optional_rehearsal_hint_compact_alias_microline_legend_idx == optional_rehearsal_hint_compact_alias_microline_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPD MICROLINE LEGEND row directly after CBGCFXWSBPFXPD MICROLINE row"
                )
            if optional_rehearsal_hint_compact_alias_coach_action_idx is not None:
                assert optional_rehearsal_hint_compact_alias_microline_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPD COACH row cannot appear without CBGCFXWSBPFXPD MICROLINE LEGEND row"
                )
                assert optional_rehearsal_hint_compact_alias_coach_action_idx == optional_rehearsal_hint_compact_alias_microline_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPD COACH row directly after CBGCFXWSBPFXPD MICROLINE LEGEND row"
                )
            if optional_rehearsal_hint_compact_alias_coach_action_compact_alias_idx is not None:
                assert optional_rehearsal_hint_compact_alias_coach_action_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDC row cannot appear without CBGCFXWSBPFXPD COACH row"
                )
                assert optional_rehearsal_hint_compact_alias_coach_action_compact_alias_idx == optional_rehearsal_hint_compact_alias_coach_action_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDC row directly after CBGCFXWSBPFXPD COACH row"
                )
            if optional_rehearsal_hint_coach_why_idx is not None:
                assert optional_rehearsal_hint_compact_alias_coach_action_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPD COACH WHY row cannot appear without CBGCFXWSBPFXPDC row"
                )
                assert optional_rehearsal_hint_coach_why_idx == optional_rehearsal_hint_compact_alias_coach_action_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPD COACH WHY row directly after CBGCFXWSBPFXPDC row"
                )
            if optional_rehearsal_hint_coach_why_compact_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW row cannot appear without CBGCFXWSBPFXPD COACH WHY row"
                )
                assert optional_rehearsal_hint_coach_why_compact_alias_idx == optional_rehearsal_hint_coach_why_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW row directly after CBGCFXWSBPFXPD COACH WHY row"
                )
            if optional_rehearsal_hint_coach_why_compact_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW LEGEND row cannot appear without CBGCFXWSBPFXPDCW row"
                )
                assert optional_rehearsal_hint_coach_why_compact_alias_legend_idx == optional_rehearsal_hint_coach_why_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW LEGEND row directly after CBGCFXWSBPFXPDCW row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_idx is not None:
                assert optional_rehearsal_hint_coach_why_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW COPY PACK row cannot appear without CBGCFXWSBPFXPDCW LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_idx == optional_rehearsal_hint_coach_why_compact_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW COPY PACK row directly after CBGCFXWSBPFXPDCW LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW COPY PACK LEGEND row cannot appear without CBGCFXWSBPFXPDCW COPY PACK row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW COPY PACK LEGEND row directly after CBGCFXWSBPFXPDCW COPY PACK row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW COPY PACK CADENCE row cannot appear without CBGCFXWSBPFXPDCW COPY PACK LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_idx == optional_rehearsal_hint_coach_why_copy_pack_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW COPY PACK CADENCE row directly after CBGCFXWSBPFXPDCW COPY PACK LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND row cannot appear without CBGCFXWSBPFXPDCW COPY PACK CADENCE row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND row directly after CBGCFXWSBPFXPDCW COPY PACK CADENCE row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWC row cannot appear without CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWC row directly after CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWC LEGEND row cannot appear without CBGCFXWSBPFXPDCWC row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWC LEGEND row directly after CBGCFXWSBPFXPDCWC row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW FX CUE row cannot appear without CBGCFXWSBPFXPDCWC LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW FX CUE row directly after CBGCFXWSBPFXPDCWC LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCW FX CUE LEGEND row cannot appear without CBGCFXWSBPFXPDCW FX CUE row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCW FX CUE LEGEND row directly after CBGCFXWSBPFXPDCW FX CUE row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWF row cannot appear without CBGCFXWSBPFXPDCW FX CUE LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWF row directly after CBGCFXWSBPFXPDCW FX CUE LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWF LEGEND row cannot appear without CBGCFXWSBPFXPDCWF row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWF LEGEND row directly after CBGCFXWSBPFXPDCWF row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWF DIGEST row cannot appear without CBGCFXWSBPFXPDCWF LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWF DIGEST row directly after CBGCFXWSBPFXPDCWF LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWF COHERENCE row cannot appear without CBGCFXWSBPFXPDCWF DIGEST row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWF COHERENCE row directly after CBGCFXWSBPFXPDCWF DIGEST row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWF COHERENCE LEGEND row cannot appear without CBGCFXWSBPFXPDCWF COHERENCE row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWF COHERENCE LEGEND row directly after CBGCFXWSBPFXPDCWF COHERENCE row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFC row cannot appear without CBGCFXWSBPFXPDCWF COHERENCE LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFC row directly after CBGCFXWSBPFXPDCWF COHERENCE LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFC LEGEND row cannot appear without CBGCFXWSBPFXPDCWFC row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFC LEGEND row directly after CBGCFXWSBPFXPDCWFC row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCT row cannot appear without CBGCFXWSBPFXPDCWFC LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCT row directly after CBGCFXWSBPFXPDCWFC LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCT LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCT row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCT LEGEND row directly after CBGCFXWSBPFXPDCWFCT row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTA row cannot appear without CBGCFXWSBPFXPDCWFCT LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTA row directly after CBGCFXWSBPFXPDCWFCT LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTA LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCTA row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTA LEGEND row directly after CBGCFXWSBPFXPDCWFCTA row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTA DIGEST row cannot appear without CBGCFXWSBPFXPDCWFCTA LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTA DIGEST row directly after CBGCFXWSBPFXPDCWFCTA LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCTA DIGEST row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND row directly after CBGCFXWSBPFXPDCWFCTA DIGEST row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTA RFALL row cannot appear without CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTA RFALL row directly after CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTA RFALL LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCTA RFALL row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTA RFALL LEGEND row directly after CBGCFXWSBPFXPDCWFCTA RFALL row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CTA REVIEW CADENCE NOTE row cannot appear without CBGCFXWSBPFXPDCWFCTA RFALL LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CTA REVIEW CADENCE NOTE row directly after CBGCFXWSBPFXPDCWFCTA RFALL LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_idx is not None, (
                    f"markdown contract violated in {section_name} section: CTA REVIEW CADENCE NOTE LEGEND row cannot appear without CTA REVIEW CADENCE NOTE row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CTA REVIEW CADENCE NOTE LEGEND row directly after CTA REVIEW CADENCE NOTE row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAN row cannot appear without CTA REVIEW CADENCE NOTE LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAN row directly after CTA REVIEW CADENCE NOTE LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAN LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCTAN row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAN LEGEND row directly after CBGCFXWSBPFXPDCWFCTAN row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAP row cannot appear without CBGCFXWSBPFXPDCWFCTAN LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAP row directly after CBGCFXWSBPFXPDCWFCTAN LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAP LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCTAP row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAP LEGEND row directly after CBGCFXWSBPFXPDCWFCTAP row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAS row cannot appear without CBGCFXWSBPFXPDCWFCTAP LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAS row directly after CBGCFXWSBPFXPDCWFCTAP LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAS LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCTAS row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAS LEGEND row directly after CBGCFXWSBPFXPDCWFCTAS row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAS CPACK row cannot appear without CBGCFXWSBPFXPDCWFCTAS LEGEND row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAS CPACK row directly after CBGCFXWSBPFXPDCWFCTAS LEGEND row"
                )
            if optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_idx is not None:
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND row cannot appear without CBGCFXWSBPFXPDCWFCTAS CPACK row"
                )
                assert optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_idx == optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND row directly after CBGCFXWSBPFXPDCWFCTAS CPACK row"
                )
            if optional_rehearsal_hint_phase_echo_idx is not None:
                assert optional_rehearsal_hint_compact_alias_coach_action_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPD ECHO row cannot appear without CBGCFXWSBPFXPD COACH row"
                )
                prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_legend_idx
                prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTAS CPACK LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_copy_pack_decode_table_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTAS CPACK"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_transition_stage_alias_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTAS"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTAP LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_operator_posture_alias_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTAP"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTAN LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_compact_alias_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTAN"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_legend_idx
                    prior_rollout_anchor_label = "CTA REVIEW CADENCE NOTE LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_cadence_note_idx
                    prior_rollout_anchor_label = "CTA REVIEW CADENCE NOTE"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTA RFALL LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTA RFALL"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTA DIGEST LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_digest_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTA DIGEST"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTA LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCTA"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCT LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_alias_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFCT"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFC LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWFC"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWF COHERENCE LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWF COHERENCE"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_digest_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWF DIGEST"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWF LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_combat_vfx_fx_cue_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCW FX CUE LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_compact_alias_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCWC LEGEND"
                if prior_rollout_anchor_idx is None:
                    prior_rollout_anchor_idx = optional_rehearsal_hint_coach_why_copy_pack_cadence_legend_idx
                    prior_rollout_anchor_label = "CBGCFXWSBPFXPDCW COPY PACK CADENCE LEGEND"
                assert prior_rollout_anchor_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPD ECHO row cannot appear without {prior_rollout_anchor_label} row"
                )
                assert optional_rehearsal_hint_phase_echo_idx == prior_rollout_anchor_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPD ECHO row directly after {prior_rollout_anchor_label} row"
                )
            if optional_rehearsal_hint_phase_echo_compact_alias_idx is not None:
                assert optional_rehearsal_hint_phase_echo_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE row cannot appear without CBGCFXWSBPFXPD ECHO row"
                )
                assert optional_rehearsal_hint_phase_echo_compact_alias_idx == optional_rehearsal_hint_phase_echo_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE row directly after CBGCFXWSBPFXPD ECHO row"
                )
            if optional_rehearsal_hint_phase_echo_compact_alias_legend_idx is not None:
                assert optional_rehearsal_hint_phase_echo_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE LEGEND row cannot appear without CBGCFXWSBPFXPDE row"
                )
                assert optional_rehearsal_hint_phase_echo_compact_alias_legend_idx == optional_rehearsal_hint_phase_echo_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE LEGEND row directly after CBGCFXWSBPFXPDE row"
                )
            if optional_rehearsal_hint_phase_echo_matrix_idx is not None:
                assert optional_rehearsal_hint_phase_echo_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE MATRIX row cannot appear without CBGCFXWSBPFXPDE LEGEND row"
                )
                assert optional_rehearsal_hint_phase_echo_matrix_idx == optional_rehearsal_hint_phase_echo_compact_alias_legend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE MATRIX row directly after CBGCFXWSBPFXPDE LEGEND row"
                )
            if optional_rehearsal_hint_phase_echo_matrix_drift_idx is not None:
                assert optional_rehearsal_hint_phase_echo_matrix_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE MATRIX DRIFT row cannot appear without CBGCFXWSBPFXPDE MATRIX row"
                )
                assert optional_rehearsal_hint_phase_echo_matrix_drift_idx == optional_rehearsal_hint_phase_echo_matrix_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE MATRIX DRIFT row directly after CBGCFXWSBPFXPDE MATRIX row"
                )
            if optional_rehearsal_hint_phase_echo_matrix_drift_trend_idx is not None:
                assert optional_rehearsal_hint_phase_echo_matrix_drift_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE MATRIX DRIFT TREND row cannot appear without CBGCFXWSBPFXPDE MATRIX DRIFT row"
                )
                assert optional_rehearsal_hint_phase_echo_matrix_drift_trend_idx == optional_rehearsal_hint_phase_echo_matrix_drift_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE MATRIX DRIFT TREND row directly after CBGCFXWSBPFXPDE MATRIX DRIFT row"
                )
            if optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_idx is not None:
                assert optional_rehearsal_hint_phase_echo_matrix_drift_trend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT row cannot appear without CBGCFXWSBPFXPDE MATRIX DRIFT TREND row"
                )
                assert optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_idx == optional_rehearsal_hint_phase_echo_matrix_drift_trend_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT row directly after CBGCFXWSBPFXPDE MATRIX DRIFT TREND row"
                )
            if optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_idx is not None:
                assert optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDS row cannot appear without CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT row"
                )
                assert optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_idx == optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDS row directly after CBGCFXWSBPFXPDE MATRIX DRIFT SNAPSHOT row"
                )
            if optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_legend_idx is not None:
                assert optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDS LEGEND row cannot appear without CBGCFXWSBPFXPDS row"
                )
                assert optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_legend_idx == optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDS LEGEND row directly after CBGCFXWSBPFXPDS row"
                )
            if optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_profiler_idx is not None:
                assert optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_legend_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE POLICY OPS WINDOW row cannot appear without CBGCFXWSBPFXPDS LEGEND row"
                )
                assert optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_profiler_idx == optional_rehearsal_hint_phase_echo_matrix_drift_snapshot_compact_alias_legend_idx + 2, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE POLICY OPS WINDOW row directly after CBGCFXWSBPFXPDE SNAPSHOT POLICY row"
                )
            if optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_idx is not None:
                assert optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_profiler_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE POLICY OPS DOMINANT row cannot appear without CBGCFXWSBPFXPDE POLICY OPS WINDOW row"
                )
                assert optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_idx == optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_profiler_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE POLICY OPS DOMINANT row directly after CBGCFXWSBPFXPDE POLICY OPS WINDOW row"
                )
            if optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_legend_idx is not None:
                assert optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_idx is not None, (
                    f"markdown contract violated in {section_name} section: CBGCFXWSBPFXPDE POLICY OPS DOMINANT LEGEND row cannot appear without CBGCFXWSBPFXPDE POLICY OPS DOMINANT row"
                )
                assert optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_legend_idx == optional_rehearsal_hint_phase_echo_snapshot_policy_ops_window_dominant_idx + 1, (
                    f"markdown contract violated in {section_name} section: expected CBGCFXWSBPFXPDE POLICY OPS DOMINANT LEGEND row directly after CBGCFXWSBPFXPDE POLICY OPS DOMINANT row"
                )
            assert coach_copy_variant_rec_compact_alias_idx == coach_copy_variant_rec_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWACRC row directly after CBGCFXWAC COACH COPY REC row"
            )
            assert coach_copy_variant_rec_compact_alias_legend_idx == coach_copy_variant_rec_compact_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWACRC LEGEND row directly after CBGCFXWACRC row"
            )
            assert coach_copy_reason_priority_alias_idx == coach_copy_variant_rec_compact_alias_legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWACRP row directly after CBGCFXWACRC LEGEND row"
            )
            assert coach_copy_reason_priority_alias_legend_idx == coach_copy_reason_priority_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWACRP LEGEND row directly after CBGCFXWACRP row"
            )
            assert coherence_alias_idx == coach_copy_reason_priority_alias_legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWC row directly after CBGCFXWACRP LEGEND row"
            )

        for section_name, legend_idx in zip(
            ("summary", "token-coverage"),
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_compact_alias_legend_indices,
        ):
            legend_line = md_lines[legend_idx]
            assert "A=ANCHOR_STEP" in legend_line and "H=HOLD_STEP" in legend_line, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWACRC LEGEND row to include deterministic A/S/H decode mapping"
            )

        for section_name, legend_idx in zip(
            ("summary", "token-coverage"),
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_coach_copy_variant_recommendation_reason_priority_alias_legend_indices,
        ):
            legend_line = md_lines[legend_idx]
            assert "P1=wobble" in legend_line and "P4=stable-calm" in legend_line, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWACRP LEGEND row to include deterministic P1..P4 decode mapping"
            )

        for section_name, legend_idx in zip(
            ("summary", "token-coverage"),
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_fx_cue_intensity_pulse_language_variant_pack_phase_intent_rehearsal_hint_phase_echo_mutation_flag_matrix_drift_snapshot_policy_ops_window_dominant_legend_indices,
        ):
            legend_line = md_lines[legend_idx]
            assert "B=BASELINE_ONLY" in legend_line and "N=NO_TRIAGE" in legend_line, (
                f"markdown contract violated in {section_name} section: expected POLICY OPS DOMINANT legend to include deterministic alias decode mapping"
            )

        # CBGC LEGEND narrative metadata contract (Cycle FZ follow-up):
        # both summary + token-coverage rows must keep narrative map and active cue fields.
        for section_name, legend_idx in zip(
            ("summary", "token-coverage"),
            cadence_bridge_glyph_conf_compact_alias_legend_indices,
        ):
            legend_line = md_lines[legend_idx]
            assert "narrative=steady/swing/spike" in legend_line, (
                f"markdown contract violated in {section_name} section: expected CBGC LEGEND row to include narrative=steady/swing/spike metadata"
            )
            assert "current=" in legend_line, (
                f"markdown contract violated in {section_name} section: expected CBGC LEGEND row to include current=<steady|swing|spike> metadata"
            )
            assert "cue=" in legend_line, (
                f"markdown contract violated in {section_name} section: expected CBGC LEGEND row to include cue=<H|P|T|U> metadata"
            )
            assert "intent=steady:hold|anchor/swing:prep|brace/spike:triage|stabilize" in legend_line, (
                f"markdown contract violated in {section_name} section: expected CBGC LEGEND row to include alternate tone-pack intent verbs"
            )
        # Explicit markdown contract for future alias-rail insertions:
        # keep CBGC LEGEND -> CBGCL -> CBGCIA -> CBGCIA FAMILY CHURN -> CBGCFXR -> CBGCFXR FAMILY CHURN -> CBGCFXA -> CBGCFXA FAMILY CHURN -> CBGC FX HINT -> CBGC FX HINT FAMILY CHURN -> CBGCFXH -> CBGCFXH FAMILY CHURN -> CBGCFXW -> CBGCFXW FAMILY CHURN -> CBGCFXW LEGEND -> CBGCFXW COHERENCE -> CBGCFXW COHERENCE MOMENTUM -> CBGCFXWM -> CBGCFXWC -> CBGCFXWC LEGEND -> CBGCFXWC FAMILY CHURN -> CBGCFXW DRIFT -> CBGCFXW DRIFT FAMILY CHURN -> CBGCI -> CBGCI LEGEND -> CBGCIL adjacent in both sections.
        for section_name, legend_idx, compact_alias_idx, intent_active_alias_idx, intent_active_alias_family_churn_idx, fx_regime_alias_idx, fx_regime_alias_family_churn_idx, fx_aggressiveness_alias_idx, fx_aggressiveness_alias_family_churn_idx, fx_microcopy_hint_idx, fx_microcopy_hint_family_churn_idx, fx_microcopy_hint_compact_alias_idx, fx_microcopy_hint_compact_alias_family_churn_idx, fx_world_tone_alias_idx, fx_world_tone_alias_family_churn_idx, fx_world_tone_legend_idx, fx_world_tone_coherence_idx, fx_world_tone_coherence_momentum_idx, fx_world_tone_coherence_momentum_alias_idx, fx_world_tone_coherence_momentum_alias_legend_idx, fx_world_tone_coherence_alias_idx, fx_world_tone_coherence_alias_legend_idx, fx_world_tone_coherence_alias_family_churn_idx, fx_world_tone_drift_idx, fx_world_tone_drift_family_churn_idx, intent_alias_idx, intent_legend_idx, intent_legend_alias_idx in zip(
            ("summary", "token-coverage"),
            cadence_bridge_glyph_conf_compact_alias_legend_indices,
            cadence_bridge_glyph_conf_compact_legend_alias_indices,
            cadence_bridge_glyph_conf_intent_compact_active_alias_indices,
            cadence_bridge_glyph_conf_intent_compact_active_alias_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_regime_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_regime_alias_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_legend_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_legend_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_legend_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_family_churn_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_indices,
            cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_family_churn_indices,
            cadence_bridge_glyph_conf_intent_compact_alias_indices,
            cadence_bridge_glyph_conf_intent_legend_indices,
            cadence_bridge_glyph_conf_intent_legend_alias_indices,
        ):
            assert compact_alias_idx == legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCL row directly after CBGC LEGEND row under future alias-rail insertions"
            )
            assert intent_active_alias_idx == compact_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCIA row directly after CBGCL row"
            )
            assert intent_active_alias_family_churn_idx == intent_active_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCIA FAMILY CHURN row directly after CBGCIA row"
            )
            assert fx_regime_alias_idx == intent_active_alias_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXR row directly after CBGCIA FAMILY CHURN row"
            )
            assert fx_regime_alias_family_churn_idx == fx_regime_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXR FAMILY CHURN row directly after CBGCFXR row"
            )
            assert fx_aggressiveness_alias_idx == fx_regime_alias_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXA row directly after CBGCFXR FAMILY CHURN row"
            )
            assert fx_aggressiveness_alias_family_churn_idx == fx_aggressiveness_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXA FAMILY CHURN row directly after CBGCFXA row"
            )
            assert fx_microcopy_hint_idx == fx_aggressiveness_alias_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGC FX HINT row directly after CBGCFXA FAMILY CHURN row"
            )
            assert fx_microcopy_hint_family_churn_idx == fx_microcopy_hint_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGC FX HINT FAMILY CHURN row directly after CBGC FX HINT row"
            )
            assert fx_microcopy_hint_compact_alias_idx == fx_microcopy_hint_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXH row directly after CBGC FX HINT FAMILY CHURN row"
            )
            assert fx_microcopy_hint_compact_alias_family_churn_idx == fx_microcopy_hint_compact_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXH FAMILY CHURN row directly after CBGCFXH row"
            )
            assert fx_world_tone_alias_idx == fx_microcopy_hint_compact_alias_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXW row directly after CBGCFXH FAMILY CHURN row"
            )
            assert fx_world_tone_alias_family_churn_idx == fx_world_tone_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXW FAMILY CHURN row directly after CBGCFXW row"
            )
            assert fx_world_tone_legend_idx == fx_world_tone_alias_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXW LEGEND row directly after CBGCFXW FAMILY CHURN row"
            )
            assert fx_world_tone_coherence_idx == fx_world_tone_legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXW COHERENCE row directly after CBGCFXW LEGEND row"
            )
            assert fx_world_tone_coherence_momentum_idx == fx_world_tone_coherence_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXW COHERENCE MOMENTUM row directly after CBGCFXW COHERENCE row"
            )
            assert fx_world_tone_coherence_momentum_alias_idx == fx_world_tone_coherence_momentum_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWM row directly after CBGCFXW COHERENCE MOMENTUM row"
            )
            assert fx_world_tone_coherence_momentum_alias_legend_idx == fx_world_tone_coherence_momentum_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWM LEGEND row directly after CBGCFXWM row"
            )
            assert fx_world_tone_coherence_alias_idx > fx_world_tone_coherence_momentum_alias_legend_idx, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWC row after CBGCFXWM LEGEND row"
            )
            assert fx_world_tone_coherence_alias_legend_idx == fx_world_tone_coherence_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWC LEGEND row directly after CBGCFXWC row"
            )
            assert fx_world_tone_coherence_alias_family_churn_idx == fx_world_tone_coherence_alias_legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXWC FAMILY CHURN row directly after CBGCFXWC LEGEND row"
            )
            assert fx_world_tone_drift_idx == fx_world_tone_coherence_alias_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXW DRIFT row directly after CBGCFXWC FAMILY CHURN row"
            )
            assert fx_world_tone_drift_family_churn_idx == fx_world_tone_drift_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCFXW DRIFT FAMILY CHURN row directly after CBGCFXW DRIFT row"
            )
            assert intent_alias_idx == fx_world_tone_drift_family_churn_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCI row directly after CBGCFXW DRIFT FAMILY CHURN row"
            )
            assert intent_legend_idx == intent_alias_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCI LEGEND row directly after CBGCI row"
            )
            assert intent_legend_alias_idx == intent_legend_idx + 1, (
                f"markdown contract violated in {section_name} section: expected CBGCIL row directly after CBGCI LEGEND row"
            )

        if cadence_bridge_glyph_conf_compact_alias_enabled:
            for section_idx, (glyph_idx, glyph_conf_idx, glyph_conf_alias_idx, glyph_conf_alias_legend_idx, glyph_conf_legend_alias_idx, glyph_conf_intent_active_alias_idx, glyph_conf_intent_active_alias_family_churn_idx, glyph_conf_fx_regime_alias_idx, glyph_conf_fx_regime_alias_family_churn_idx, glyph_conf_fx_aggressiveness_alias_idx, glyph_conf_fx_aggressiveness_alias_family_churn_idx, glyph_conf_fx_microcopy_hint_idx, glyph_conf_fx_microcopy_hint_family_churn_idx, glyph_conf_fx_microcopy_hint_compact_alias_idx, glyph_conf_fx_microcopy_hint_compact_alias_family_churn_idx, glyph_conf_fx_world_tone_alias_idx, glyph_conf_fx_world_tone_alias_family_churn_idx, glyph_conf_fx_world_tone_legend_idx, glyph_conf_fx_world_tone_coherence_idx, glyph_conf_fx_world_tone_coherence_momentum_idx, glyph_conf_fx_world_tone_coherence_momentum_alias_idx, glyph_conf_fx_world_tone_coherence_momentum_alias_legend_idx, glyph_conf_fx_world_tone_coherence_alias_idx, glyph_conf_fx_world_tone_coherence_alias_legend_idx, glyph_conf_fx_world_tone_coherence_alias_family_churn_idx, glyph_conf_fx_world_tone_drift_idx, glyph_conf_fx_world_tone_drift_family_churn_idx, glyph_conf_intent_alias_idx, glyph_conf_legend_idx, glyph_legend_idx) in enumerate(
                zip(
                    cadence_bridge_glyph_indices,
                    cadence_bridge_glyph_conf_indices,
                    cadence_bridge_glyph_conf_compact_alias_indices,
                    cadence_bridge_glyph_conf_compact_alias_legend_indices,
                    cadence_bridge_glyph_conf_compact_legend_alias_indices,
                    cadence_bridge_glyph_conf_intent_compact_active_alias_indices,
                    cadence_bridge_glyph_conf_intent_compact_active_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_regime_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_regime_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_legend_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_legend_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_legend_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_family_churn_indices,
                    cadence_bridge_glyph_conf_intent_compact_alias_indices,
                    cadence_bridge_glyph_conf_legend_indices,
                    cadence_bridge_glyph_legend_indices,
                ),
                start=1,
            ):
                assert glyph_conf_idx == glyph_idx + 1, (
                    f"expected CADENCE BRIDGE GLYPH CONF row directly after CADENCE BRIDGE GLYPH row in section {section_idx}"
                )
                assert glyph_conf_alias_idx == glyph_conf_idx + 1, (
                    f"expected CBGC alias row directly after CADENCE BRIDGE GLYPH CONF row in section {section_idx}"
                )
                assert glyph_conf_alias_legend_idx == glyph_conf_alias_idx + 1, (
                    f"expected CBGC LEGEND row directly after CBGC alias row in section {section_idx}"
                )
                assert glyph_conf_legend_alias_idx == glyph_conf_alias_legend_idx + 1, (
                    f"expected CBGCL row directly after CBGC LEGEND row in section {section_idx}"
                )
                assert glyph_conf_intent_active_alias_idx == glyph_conf_legend_alias_idx + 1, (
                    f"expected CBGCIA row directly after CBGCL row in section {section_idx}"
                )
                assert glyph_conf_intent_active_alias_family_churn_idx == glyph_conf_intent_active_alias_idx + 1, (
                    f"expected CBGCIA FAMILY CHURN row directly after CBGCIA row in section {section_idx}"
                )
                assert glyph_conf_fx_regime_alias_idx == glyph_conf_intent_active_alias_family_churn_idx + 1, (
                    f"expected CBGCFXR row directly after CBGCIA FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_regime_alias_family_churn_idx == glyph_conf_fx_regime_alias_idx + 1, (
                    f"expected CBGCFXR FAMILY CHURN row directly after CBGCFXR row in section {section_idx}"
                )
                assert glyph_conf_fx_aggressiveness_alias_idx == glyph_conf_fx_regime_alias_family_churn_idx + 1, (
                    f"expected CBGCFXA row directly after CBGCFXR FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_aggressiveness_alias_family_churn_idx == glyph_conf_fx_aggressiveness_alias_idx + 1, (
                    f"expected CBGCFXA FAMILY CHURN row directly after CBGCFXA row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_idx == glyph_conf_fx_aggressiveness_alias_family_churn_idx + 1, (
                    f"expected CBGC FX HINT row directly after CBGCFXA FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_family_churn_idx == glyph_conf_fx_microcopy_hint_idx + 1, (
                    f"expected CBGC FX HINT FAMILY CHURN row directly after CBGC FX HINT row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_compact_alias_idx == glyph_conf_fx_microcopy_hint_family_churn_idx + 1, (
                    f"expected CBGCFXH row directly after CBGC FX HINT FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_compact_alias_family_churn_idx == glyph_conf_fx_microcopy_hint_compact_alias_idx + 1, (
                    f"expected CBGCFXH FAMILY CHURN row directly after CBGCFXH row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_alias_idx == glyph_conf_fx_microcopy_hint_compact_alias_family_churn_idx + 1, (
                    f"expected CBGCFXW row directly after CBGCFXH FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_alias_family_churn_idx == glyph_conf_fx_world_tone_alias_idx + 1, (
                    f"expected CBGCFXW FAMILY CHURN row directly after CBGCFXW row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_legend_idx == glyph_conf_fx_world_tone_alias_family_churn_idx + 1, (
                    f"expected CBGCFXW LEGEND row directly after CBGCFXW FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_idx == glyph_conf_fx_world_tone_legend_idx + 1, (
                    f"expected CBGCFXW COHERENCE row directly after CBGCFXW LEGEND row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_momentum_idx == glyph_conf_fx_world_tone_coherence_idx + 1, (
                    f"expected CBGCFXW COHERENCE MOMENTUM row directly after CBGCFXW COHERENCE row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_momentum_alias_idx == glyph_conf_fx_world_tone_coherence_momentum_idx + 1, (
                    f"expected CBGCFXWM row directly after CBGCFXW COHERENCE MOMENTUM row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_momentum_alias_legend_idx == glyph_conf_fx_world_tone_coherence_momentum_alias_idx + 1, (
                    f"expected CBGCFXWM LEGEND row directly after CBGCFXWM row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_alias_idx > glyph_conf_fx_world_tone_coherence_momentum_alias_legend_idx, (
                    f"expected CBGCFXWC row after CBGCFXWM LEGEND row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_alias_legend_idx == glyph_conf_fx_world_tone_coherence_alias_idx + 1, (
                    f"expected CBGCFXWC LEGEND row directly after CBGCFXWC row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_alias_family_churn_idx == glyph_conf_fx_world_tone_coherence_alias_legend_idx + 1, (
                    f"expected CBGCFXWC FAMILY CHURN row directly after CBGCFXWC LEGEND row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_drift_idx == glyph_conf_fx_world_tone_coherence_alias_family_churn_idx + 1, (
                    f"expected CBGCFXW DRIFT row directly after CBGCFXWC FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_drift_family_churn_idx == glyph_conf_fx_world_tone_drift_idx + 1, (
                    f"expected CBGCFXW DRIFT FAMILY CHURN row directly after CBGCFXW DRIFT row in section {section_idx}"
                )
                assert glyph_conf_intent_alias_idx == glyph_conf_fx_world_tone_drift_family_churn_idx + 1, (
                    f"expected CBGCI row directly after CBGCFXW DRIFT FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_legend_idx in {
                    glyph_conf_intent_alias_idx + 1,
                    glyph_conf_intent_alias_idx + 2,
                    glyph_conf_intent_alias_idx + 3,
                }, (
                    f"expected CADENCE BRIDGE GLYPH CONF LEGEND row adjacent to CBGCI cluster in section {section_idx}"
                )
                if glyph_conf_legend_idx == glyph_conf_intent_alias_idx + 2:
                    assert md_lines[glyph_conf_intent_alias_idx + 1].startswith("- CBGCI LEGEND:"), (
                        f"expected CBGCI LEGEND spacer before CADENCE BRIDGE GLYPH CONF LEGEND in section {section_idx}"
                    )
                if glyph_conf_legend_idx == glyph_conf_intent_alias_idx + 3:
                    assert md_lines[glyph_conf_intent_alias_idx + 1].startswith("- CBGCI LEGEND:"), (
                        f"expected CBGCI LEGEND first spacer before CADENCE BRIDGE GLYPH CONF LEGEND in section {section_idx}"
                    )
                    assert md_lines[glyph_conf_intent_alias_idx + 2].startswith("- CBGCIL:"), (
                        f"expected CBGCIL second spacer before CADENCE BRIDGE GLYPH CONF LEGEND in section {section_idx}"
                    )
                assert glyph_legend_idx == glyph_conf_legend_idx + 1, (
                    f"expected CADENCE BRIDGE GLYPH LEGEND row directly after CADENCE BRIDGE GLYPH CONF LEGEND row in section {section_idx}"
                )
        else:
            for section_idx, (glyph_idx, glyph_conf_idx, glyph_conf_alias_legend_idx, glyph_conf_legend_alias_idx, glyph_conf_intent_active_alias_idx, glyph_conf_intent_active_alias_family_churn_idx, glyph_conf_fx_regime_alias_idx, glyph_conf_fx_regime_alias_family_churn_idx, glyph_conf_fx_aggressiveness_alias_idx, glyph_conf_fx_aggressiveness_alias_family_churn_idx, glyph_conf_fx_microcopy_hint_idx, glyph_conf_fx_microcopy_hint_family_churn_idx, glyph_conf_fx_microcopy_hint_compact_alias_idx, glyph_conf_fx_microcopy_hint_compact_alias_family_churn_idx, glyph_conf_fx_world_tone_alias_idx, glyph_conf_fx_world_tone_alias_family_churn_idx, glyph_conf_fx_world_tone_legend_idx, glyph_conf_fx_world_tone_coherence_idx, glyph_conf_fx_world_tone_coherence_momentum_idx, glyph_conf_fx_world_tone_coherence_momentum_alias_idx, glyph_conf_fx_world_tone_coherence_momentum_alias_legend_idx, glyph_conf_fx_world_tone_coherence_alias_idx, glyph_conf_fx_world_tone_coherence_alias_legend_idx, glyph_conf_fx_world_tone_coherence_alias_family_churn_idx, glyph_conf_fx_world_tone_drift_idx, glyph_conf_fx_world_tone_drift_family_churn_idx, glyph_conf_intent_alias_idx, glyph_conf_legend_idx, glyph_legend_idx) in enumerate(
                zip(
                    cadence_bridge_glyph_indices,
                    cadence_bridge_glyph_conf_indices,
                    cadence_bridge_glyph_conf_compact_alias_legend_indices,
                    cadence_bridge_glyph_conf_compact_legend_alias_indices,
                    cadence_bridge_glyph_conf_intent_compact_active_alias_indices,
                    cadence_bridge_glyph_conf_intent_compact_active_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_regime_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_regime_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_aggressiveness_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_hint_compact_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_legend_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_momentum_alias_legend_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_legend_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_coherence_alias_family_churn_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_indices,
                    cadence_bridge_glyph_conf_fx_pulse_microcopy_world_tone_drift_family_churn_indices,
                    cadence_bridge_glyph_conf_intent_compact_alias_indices,
                    cadence_bridge_glyph_conf_legend_indices,
                    cadence_bridge_glyph_legend_indices,
                ),
                start=1,
            ):
                assert glyph_conf_idx == glyph_idx + 1, (
                    f"expected CADENCE BRIDGE GLYPH CONF row directly after CADENCE BRIDGE GLYPH row in section {section_idx}"
                )
                assert glyph_conf_alias_legend_idx == glyph_conf_idx + 1, (
                    f"expected CBGC LEGEND row directly after CADENCE BRIDGE GLYPH CONF row in section {section_idx}"
                )
                assert glyph_conf_legend_alias_idx == glyph_conf_alias_legend_idx + 1, (
                    f"expected CBGCL row directly after CBGC LEGEND row in section {section_idx}"
                )
                assert glyph_conf_intent_active_alias_idx == glyph_conf_legend_alias_idx + 1, (
                    f"expected CBGCIA row directly after CBGCL row in section {section_idx}"
                )
                assert glyph_conf_intent_active_alias_family_churn_idx == glyph_conf_intent_active_alias_idx + 1, (
                    f"expected CBGCIA FAMILY CHURN row directly after CBGCIA row in section {section_idx}"
                )
                assert glyph_conf_fx_regime_alias_idx == glyph_conf_intent_active_alias_family_churn_idx + 1, (
                    f"expected CBGCFXR row directly after CBGCIA FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_regime_alias_family_churn_idx == glyph_conf_fx_regime_alias_idx + 1, (
                    f"expected CBGCFXR FAMILY CHURN row directly after CBGCFXR row in section {section_idx}"
                )
                assert glyph_conf_fx_aggressiveness_alias_idx == glyph_conf_fx_regime_alias_family_churn_idx + 1, (
                    f"expected CBGCFXA row directly after CBGCFXR FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_aggressiveness_alias_family_churn_idx == glyph_conf_fx_aggressiveness_alias_idx + 1, (
                    f"expected CBGCFXA FAMILY CHURN row directly after CBGCFXA row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_idx == glyph_conf_fx_aggressiveness_alias_family_churn_idx + 1, (
                    f"expected CBGC FX HINT row directly after CBGCFXA FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_family_churn_idx == glyph_conf_fx_microcopy_hint_idx + 1, (
                    f"expected CBGC FX HINT FAMILY CHURN row directly after CBGC FX HINT row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_compact_alias_idx == glyph_conf_fx_microcopy_hint_family_churn_idx + 1, (
                    f"expected CBGCFXH row directly after CBGC FX HINT FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_microcopy_hint_compact_alias_family_churn_idx == glyph_conf_fx_microcopy_hint_compact_alias_idx + 1, (
                    f"expected CBGCFXH FAMILY CHURN row directly after CBGCFXH row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_alias_idx == glyph_conf_fx_microcopy_hint_compact_alias_family_churn_idx + 1, (
                    f"expected CBGCFXW row directly after CBGCFXH FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_alias_family_churn_idx == glyph_conf_fx_world_tone_alias_idx + 1, (
                    f"expected CBGCFXW FAMILY CHURN row directly after CBGCFXW row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_legend_idx == glyph_conf_fx_world_tone_alias_family_churn_idx + 1, (
                    f"expected CBGCFXW LEGEND row directly after CBGCFXW FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_idx == glyph_conf_fx_world_tone_legend_idx + 1, (
                    f"expected CBGCFXW COHERENCE row directly after CBGCFXW LEGEND row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_momentum_idx == glyph_conf_fx_world_tone_coherence_idx + 1, (
                    f"expected CBGCFXW COHERENCE MOMENTUM row directly after CBGCFXW COHERENCE row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_momentum_alias_idx == glyph_conf_fx_world_tone_coherence_momentum_idx + 1, (
                    f"expected CBGCFXWM row directly after CBGCFXW COHERENCE MOMENTUM row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_momentum_alias_legend_idx == glyph_conf_fx_world_tone_coherence_momentum_alias_idx + 1, (
                    f"expected CBGCFXWM LEGEND row directly after CBGCFXWM row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_alias_idx > glyph_conf_fx_world_tone_coherence_momentum_alias_legend_idx, (
                    f"expected CBGCFXWC row after CBGCFXWM LEGEND row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_alias_legend_idx == glyph_conf_fx_world_tone_coherence_alias_idx + 1, (
                    f"expected CBGCFXWC LEGEND row directly after CBGCFXWC row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_coherence_alias_family_churn_idx == glyph_conf_fx_world_tone_coherence_alias_legend_idx + 1, (
                    f"expected CBGCFXWC FAMILY CHURN row directly after CBGCFXWC LEGEND row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_drift_idx == glyph_conf_fx_world_tone_coherence_alias_family_churn_idx + 1, (
                    f"expected CBGCFXW DRIFT row directly after CBGCFXWC FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_fx_world_tone_drift_family_churn_idx == glyph_conf_fx_world_tone_drift_idx + 1, (
                    f"expected CBGCFXW DRIFT FAMILY CHURN row directly after CBGCFXW DRIFT row in section {section_idx}"
                )
                assert glyph_conf_intent_alias_idx == glyph_conf_fx_world_tone_drift_family_churn_idx + 1, (
                    f"expected CBGCI row directly after CBGCFXW DRIFT FAMILY CHURN row in section {section_idx}"
                )
                assert glyph_conf_legend_idx in {
                    glyph_conf_intent_alias_idx + 1,
                    glyph_conf_intent_alias_idx + 2,
                    glyph_conf_intent_alias_idx + 3,
                }, (
                    f"expected CADENCE BRIDGE GLYPH CONF LEGEND row adjacent to CBGCI cluster in section {section_idx}"
                )
                if glyph_conf_legend_idx == glyph_conf_intent_alias_idx + 2:
                    assert md_lines[glyph_conf_intent_alias_idx + 1].startswith("- CBGCI LEGEND:"), (
                        f"expected CBGCI LEGEND spacer before CADENCE BRIDGE GLYPH CONF LEGEND in section {section_idx}"
                    )
                if glyph_conf_legend_idx == glyph_conf_intent_alias_idx + 3:
                    assert md_lines[glyph_conf_intent_alias_idx + 1].startswith("- CBGCI LEGEND:"), (
                        f"expected CBGCI LEGEND first spacer before CADENCE BRIDGE GLYPH CONF LEGEND in section {section_idx}"
                    )
                    assert md_lines[glyph_conf_intent_alias_idx + 2].startswith("- CBGCIL:"), (
                        f"expected CBGCIL second spacer before CADENCE BRIDGE GLYPH CONF LEGEND in section {section_idx}"
                    )
                assert glyph_legend_idx == glyph_conf_legend_idx + 1, (
                    f"expected CADENCE BRIDGE GLYPH LEGEND row directly after CADENCE BRIDGE GLYPH CONF LEGEND row in section {section_idx}"
                )

        assert len(combat_vfx_cadence_coach_why_hysteresis_family_churn_indices) == 2, (
            "expected exactly two CVCWH FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_family_churn_indices) == 2, (
            "expected exactly two CVCWHR FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_family_churn_indices) == 2, (
            "expected exactly two CVCWHR CONF + CVCWHRC FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_alias_indices) == 2, (
            "expected exactly two CVCC alias rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_family_churn_indices) == 2, (
            "expected exactly two COMBAT/VFX CADENCE COACH WHY + CVCW FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_family_churn_indices) == 2, (
            "expected exactly two COMBAT/VFX CADENCE COACH + CVCC FAMILY CHURN rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_watchdog_legend_indices) == 2, (
            "expected exactly two COMBAT/VFX CADENCE WATCHDOG LEGEND rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_override_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND CPTC OVERRIDE rows (summary + token-coverage sections)"
        )
        assert len(combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_family_churn_indices) == 2, (
            "expected exactly two CVCWHR FX LEGEND COPY PACK FAMILY CHURN rows (summary + token-coverage sections)"
        )
        for section_idx, (watchdog_legend_idx, cptc_override_idx, copy_pack_family_churn_idx) in enumerate(
            zip(
                combat_vfx_watchdog_legend_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_override_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_family_churn_indices,
            )
        ):
            assert cptc_override_idx == watchdog_legend_idx + 1, (
                f"expected CVCWHR FX LEGEND CPTC OVERRIDE row directly after WATCHDOG LEGEND in section {section_idx}"
            )
            assert copy_pack_family_churn_idx == cptc_override_idx + 1, (
                f"expected CVCWHR FX LEGEND COPY PACK FAMILY CHURN row directly after CPTC OVERRIDE row in section {section_idx}"
            )

        for section_idx, (miss_risk_idx, alias_idx, cadence_24h_idx, watchdog_idx, watchdog_streak_idx, coach_idx, coach_why_idx, coach_why_alias_idx, coach_why_hyst_alias_idx, coach_why_hyst_rec_idx, coach_why_hyst_rec_conf_idx, coach_why_hyst_rec_conf_alias_idx, coach_why_hyst_rec_conf_floor_idx, coach_why_hyst_rec_conf_floor_alias_idx, coach_why_hyst_rec_conf_floor_fx_pulse_idx, coach_why_hyst_rec_conf_floor_fx_pulse_legend_idx, cadence_bridge_idx, coach_why_hyst_rec_conf_floor_family_churn_idx, coach_why_hyst_rec_conf_floor_fx_pulse_family_churn_idx, coach_why_hyst_rec_conf_floor_fx_pulse_family_trend_idx, cadence_bridge_family_churn_idx, coach_why_hyst_family_churn_idx, coach_why_hyst_rec_family_churn_idx, coach_why_hyst_rec_conf_family_churn_idx, coach_why_family_churn_idx, coach_alias_idx, coach_family_churn_idx, watchdog_legend_idx) in enumerate(
            zip(
                lane_cadence_miss_risk_indices,
                lane_cadence_miss_risk_alias_indices,
                lane_cadence_24h_check_indices,
                combat_vfx_watchdog_indices,
                combat_vfx_watchdog_streak_indices,
                combat_vfx_cadence_coach_indices,
                combat_vfx_cadence_coach_why_indices,
                combat_vfx_cadence_coach_why_alias_indices,
                combat_vfx_cadence_coach_why_hysteresis_alias_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_alias_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_alias_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_indices,
                cadence_bridge_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_family_churn_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_family_churn_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_family_trend_indices,
                cadence_bridge_family_churn_indices,
                combat_vfx_cadence_coach_why_hysteresis_family_churn_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_family_churn_indices,
                combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_family_churn_indices,
                combat_vfx_cadence_coach_why_family_churn_indices,
                combat_vfx_cadence_coach_alias_indices,
                combat_vfx_cadence_coach_family_churn_indices,
                combat_vfx_watchdog_legend_indices,
            ),
            start=1,
        ):
            assert alias_idx == miss_risk_idx + 1, (
                f"expected LCMR row directly after LANE CADENCE MISS RISK row in section {section_idx}"
            )
            assert cadence_24h_idx == alias_idx + 1, (
                f"expected LANE CADENCE 24H CHECK row directly after LCMR row in section {section_idx}"
            )
            assert watchdog_idx == cadence_24h_idx + 1, (
                f"expected COMBAT/VFX CADENCE WATCHDOG row directly after LANE CADENCE 24H CHECK row in section {section_idx}"
            )
            assert watchdog_streak_idx == watchdog_idx + 1, (
                f"expected COMBAT/VFX CADENCE WATCHDOG STREAK row directly after COMBAT/VFX CADENCE WATCHDOG row in section {section_idx}"
            )
            assert coach_idx == watchdog_streak_idx + 1, (
                f"expected COMBAT/VFX CADENCE COACH row directly after COMBAT/VFX CADENCE WATCHDOG STREAK row in section {section_idx}"
            )
            assert coach_why_idx == coach_idx + 1, (
                f"expected COMBAT/VFX CADENCE COACH WHY row directly after COMBAT/VFX CADENCE COACH row in section {section_idx}"
            )
            assert coach_why_alias_idx == coach_why_idx + 1, (
                f"expected CVCW alias row directly after COMBAT/VFX CADENCE COACH WHY row in section {section_idx}"
            )
            assert coach_why_hyst_alias_idx == coach_why_alias_idx + 1, (
                f"expected CVCWH alias row directly after CVCW row in section {section_idx}"
            )
            assert coach_why_hyst_rec_idx == coach_why_hyst_alias_idx + 1, (
                f"expected CVCWHR row directly after CVCWH row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_idx == coach_why_hyst_rec_idx + 1, (
                f"expected CVCWHR CONF row directly after CVCWHR row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_alias_idx == coach_why_hyst_rec_conf_idx + 1, (
                f"expected CVCWHRC alias row directly after CVCWHR CONF row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_idx == coach_why_hyst_rec_conf_alias_idx + 1, (
                f"expected CVCWHR CONF FLOOR REC row directly after CVCWHRC row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_alias_idx == coach_why_hyst_rec_conf_floor_idx + 1, (
                f"expected CVCWHRF alias row directly after CVCWHR CONF FLOOR REC row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_idx == coach_why_hyst_rec_conf_floor_alias_idx + 1, (
                f"expected CVCWHR FX PULSE row directly after CVCWHRF row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_idx == coach_why_hyst_rec_conf_floor_fx_pulse_idx + 1, (
                f"expected CVCWHR FX PULSE LEGEND row directly after CVCWHR FX PULSE row in section {section_idx}"
            )
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_rec_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_rec_indices[section_idx - 1]
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_rec_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_idx + 1, (
                f"expected CVCWHR FX PULSE LEGEND REC row directly after CVCWHR FX PULSE LEGEND row in section {section_idx}"
            )
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_rec_conf_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_rec_conf_indices[section_idx - 1]
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_indices[section_idx - 1]
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_alias_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_alias_indices[section_idx - 1]
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_indices[section_idx - 1]
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_alias_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_alias_indices[section_idx - 1]
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_indices[section_idx - 1]
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_alias_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_alias_indices[section_idx - 1]
            coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_alias_legend_idx = combat_vfx_cadence_coach_why_hysteresis_recommendation_confidence_floor_fx_pulse_legend_copy_pack_trend_confidence_alias_legend_indices[section_idx - 1]
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_rec_conf_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_rec_idx + 1, (
                f"expected CVCWHR FX LEGEND REC CONF row directly after CVCWHR FX LEGEND REC row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_idx >= coach_why_hyst_rec_conf_floor_fx_pulse_legend_rec_conf_idx + 1, (
                f"expected CVCWHR FX LEGEND COPY PACK row after CVCWHR FX LEGEND REC CONF row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_alias_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_idx + 1, (
                f"expected CVCWHR FX LEGEND CP alias row directly after CVCWHR FX LEGEND COPY PACK row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_alias_idx + 1, (
                f"expected CVCWHR FX LEGEND COPY PACK TREND row directly after CVCWHR FX LEGEND CP row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_alias_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_idx + 1, (
                f"expected CVCWHR FX LEGEND CPT row directly after CVCWHR FX LEGEND COPY PACK TREND row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_alias_idx + 1, (
                f"expected CVCWHR FX LEGEND COPY PACK TREND CONF row directly after CVCWHR FX LEGEND CPT row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_alias_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_idx + 1, (
                f"expected CVCWHR FX LEGEND CPTC row directly after CVCWHR FX LEGEND COPY PACK TREND CONF row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_alias_legend_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_alias_idx + 1, (
                f"expected CVCWHR FX LEGEND CPTC LEGEND row directly after CVCWHR FX LEGEND CPTC row in section {section_idx}"
            )
            assert cadence_bridge_idx == coach_why_hyst_rec_conf_floor_fx_pulse_legend_copy_pack_trend_conf_alias_legend_idx + 1, (
                f"expected CADENCE BRIDGE row directly after CVCWHR FX LEGEND CPTC LEGEND row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_family_churn_idx == cadence_bridge_idx + 1, (
                f"expected CVCWHR CONF FLOOR + CVCWHRF FAMILY CHURN row directly after CADENCE BRIDGE row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_family_churn_idx == coach_why_hyst_rec_conf_floor_family_churn_idx + 1, (
                f"expected CVCWHR FX PULSE FAMILY CHURN row directly after CVCWHR CONF FLOOR + CVCWHRF FAMILY CHURN row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_floor_fx_pulse_family_trend_idx == coach_why_hyst_rec_conf_floor_fx_pulse_family_churn_idx + 1, (
                f"expected CVCWHR FX PULSE FAMILY TREND row directly after CVCWHR FX PULSE FAMILY CHURN row in section {section_idx}"
            )
            assert cadence_bridge_family_churn_idx == coach_why_hyst_rec_conf_floor_fx_pulse_family_trend_idx + 1, (
                f"expected CADENCE BRIDGE FAMILY CHURN row directly after CVCWHR FX PULSE FAMILY TREND row in section {section_idx}"
            )
            assert coach_why_hyst_family_churn_idx == cadence_bridge_family_churn_idx + 1, (
                f"expected CVCWH FAMILY CHURN row directly after CVCWHR CONF FLOOR + CVCWHRF FAMILY CHURN row in section {section_idx}"
            )
            assert coach_why_hyst_rec_family_churn_idx == coach_why_hyst_family_churn_idx + 1, (
                f"expected CVCWHR FAMILY CHURN row directly after CVCWH FAMILY CHURN row in section {section_idx}"
            )
            assert coach_why_hyst_rec_conf_family_churn_idx == coach_why_hyst_rec_family_churn_idx + 1, (
                f"expected CVCWHR CONF + CVCWHRC FAMILY CHURN row directly after CVCWHR FAMILY CHURN row in section {section_idx}"
            )
            assert coach_why_family_churn_idx == coach_why_hyst_rec_conf_family_churn_idx + 1, (
                f"expected COMBAT/VFX CADENCE COACH WHY + CVCW FAMILY CHURN row directly after CVCWHR CONF + CVCWHRC FAMILY CHURN row in section {section_idx}"
            )
            assert coach_alias_idx == coach_why_family_churn_idx + 1, (
                f"expected CVCC alias row directly after COMBAT/VFX CADENCE COACH WHY + CVCW FAMILY CHURN row in section {section_idx}"
            )
            assert coach_family_churn_idx == coach_alias_idx + 1, (
                f"expected COMBAT/VFX CADENCE COACH + CVCC FAMILY CHURN row directly after CVCC row in section {section_idx}"
            )
            assert watchdog_legend_idx == coach_family_churn_idx + 1, (
                f"expected COMBAT/VFX CADENCE WATCHDOG LEGEND row directly after cadence coach family churn row in section {section_idx}"
            )
        assert prsmc_family_churn_idx == prsmc_family_trend_idx + 1, (
            "expected PRSMC FAMILY CHURN row directly after PRSMC FAMILY TREND row"
        )
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

        cvcwhr_fx_trend_zero, cvcwhr_fx_trend_zero_signals = combat_vfx_cadence_coach_why_hysteresis_confidence_floor_fx_pulse_family_trend_from_prior(
            current_family_totals={"net": 0},
            prior_json_path=repo / "missing-cvcwhr-fx-trend-prior.json",
        )
        assert cvcwhr_fx_trend_zero == 0, (cvcwhr_fx_trend_zero, cvcwhr_fx_trend_zero_signals)
        assert cvcwhr_fx_trend_zero_signals["trend"] == "FLAT", cvcwhr_fx_trend_zero_signals

        cvcwhr_fx_trend_prior = repo / "prior-cvcwhr-fx-trend.json"
        cvcwhr_fx_trend_prior.write_text(
            json.dumps({"tokenFamilyTotals": {"combatVfxCadenceCoachWhyHysteresisConfidenceFloorFxPulseAlias": {"net": 2}}}),
            encoding="utf-8",
        )
        cvcwhr_fx_trend_up, cvcwhr_fx_trend_up_signals = combat_vfx_cadence_coach_why_hysteresis_confidence_floor_fx_pulse_family_trend_from_prior(
            current_family_totals={"net": 4},
            prior_json_path=cvcwhr_fx_trend_prior,
        )
        assert cvcwhr_fx_trend_up == 2, (cvcwhr_fx_trend_up, cvcwhr_fx_trend_up_signals)
        assert cvcwhr_fx_trend_up_signals["trend"] == "UP", cvcwhr_fx_trend_up_signals

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
            rfall_prior = repo / "prior-rfall-streak.json"
            rfall_prior.write_text(
                json.dumps({
                    "cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopyRStreak": 0
                }),
                encoding="utf-8",
            )
            rfall_token_none, rfall_signals_none = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy(
                tooltip_action_alias_signals={"actionAlias": "R"},
                prior_json_path=rfall_prior,
            )
            assert rfall_token_none in {"FLAG OFF", "CBGCFXWSBPFXPDCWFCTA RFALL:NONE"}, (rfall_token_none, rfall_signals_none)
            assert rfall_signals_none["selectedVariant"] == "NONE", rfall_signals_none
            rfall_prior.write_text(json.dumps({"cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopyRStreak": 1}), encoding="utf-8")
            rfall_token_v1, rfall_signals_v1 = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy(
                tooltip_action_alias_signals={"actionAlias": "R"},
                prior_json_path=rfall_prior,
            )
            assert rfall_token_v1 in {"FLAG OFF", "CBGCFXWSBPFXPDCWFCTA RFALL:V1"}, (rfall_token_v1, rfall_signals_v1)
            assert rfall_signals_v1["selectedVariant"] == "V1", rfall_signals_v1
            rfall_prior.write_text(json.dumps({"cadenceBridgeGlyphConfidenceFxPulseMicrocopyWorldToneCoherenceArcStorybeatPhaseIntentRehearsalCoachWhyCopyPackCadenceCombatVfxFxCueCompactAliasCoherenceCompactAliasTooltipActionAliasReviewFallbackCopyRStreak": 2}), encoding="utf-8")
            rfall_token_v2, rfall_signals_v2 = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy(
                tooltip_action_alias_signals={"actionAlias": "R"},
                prior_json_path=rfall_prior,
            )
            assert rfall_token_v2 in {"FLAG OFF", "CBGCFXWSBPFXPDCWFCTA RFALL:V2"}, (rfall_token_v2, rfall_signals_v2)
            assert rfall_signals_v2["selectedVariant"] == "V2", rfall_signals_v2
            rfall_token_reset, rfall_signals_reset = resolve_cadence_bridge_glyph_confidence_fx_pulse_microcopy_world_tone_coherence_arc_storybeat_phase_intent_rehearsal_coach_why_copy_pack_cadence_combat_vfx_fx_cue_compact_alias_coherence_compact_alias_tooltip_action_alias_review_fallback_copy(
                tooltip_action_alias_signals={"actionAlias": "S"},
                prior_json_path=rfall_prior,
            )
            assert rfall_token_reset in {"FLAG OFF", "CBGCFXWSBPFXPDCWFCTA RFALL:NONE"}, (rfall_token_reset, rfall_signals_reset)
            assert rfall_signals_reset["selectedVariant"] == "NONE", rfall_signals_reset
            assert int(rfall_signals_reset["rStreak"]) == 0, rfall_signals_reset

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
