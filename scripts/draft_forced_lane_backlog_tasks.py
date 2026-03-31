#!/usr/bin/env python3
"""Draft forced-lane backlog task templates from lane guardrail output.

Consumes JSON from `check_lane_coverage_guardrail.py` and emits deterministic
JSON/Markdown templates that can be copy-pasted into TASKS/POST_RC_BACKLOG.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BUCKET_TASK_MAP = {
    "combat-or-vfx": {
        "label": "Combat/VFX",
        "task": "Inject one combat/vfx readability experiment template (payload-first, reversible).",
        "dod": "At least one combat/vfx template row drafted with flag, rollback path, and verification command.",
    },
    "design-or-world": {
        "label": "Design/World",
        "task": "Inject one design/world readability experiment template with deterministic row-order contract.",
        "dod": "Template includes legend/adjacency expectations and DOS-width budget note.",
    },
    "systems-or-ops": {
        "label": "Systems/Ops",
        "task": "Inject one systems/ops guardrail follow-up template with schema/domain lock coverage.",
        "dod": "Template includes payload contract keys + regression lock command.",
    },
}

LANE_TEAM_MAP = {
    "systems": "Systems/QA Team",
    "world": "World/Design Team",
    "ai-content": "AI Content/Design Team",
    "combat": "Combat/VFX Team",
    "design": "Design/UX Team",
    "ux": "UX/Design Team",
    "qa": "Systems/QA Team",
    "vfx": "Combat/VFX Team",
}

GAMEPLAY_LANE_PRIORITY = ["combat", "vfx", "world", "design", "ux", "ai-content", "systems", "qa"]
COPY_PACKS = {
    "steady": {
        "playerFantasy": "Keep lane rotation feeling reliable with a predictable, confidence-first gameplay experiment handoff.",
        "impactMetric": "At least one underrepresented lane appears in next-cycle completed items while lane-cap warning resolves.",
        "risk": "low",
        "scope": "S",
        "rollback": "Remove template row and disable over-cap gameplay injection pathway.",
        "passFail": "Pass when template includes deterministic lane + verification command and guardrail status remains machine-readable.",
    },
    "spike": {
        "playerFantasy": "Inject a visible tension spike in the neglected lane while preserving deterministic operator dispatch copy.",
        "impactMetric": "At least one underrepresented lane ships with player-facing intensity uplift while lane-cap warning resolves.",
        "risk": "mid",
        "scope": "S",
        "rollback": "Revert to steady copy pack and remove the spike phrasing from template rows.",
        "passFail": "Pass when template keeps deterministic fields, lane key, and verification command while delivering higher-intensity copy.",
    },
}
COPY_PACK_ALIAS = {"steady": "ST", "spike": "SP"}
COMPAT_ROW_POLICY_ALIAS = {"ALWAYS": "A", "SPIKE_ONLY": "S"}
COMPAT_ROW_POLICY_SOURCE_ALIAS = {"COPY_PACK": "C", "VOLATILITY_MEMORY": "V"}
COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_ALIAS = {"LOW": "L", "MID": "M", "HIGH": "H"}
COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_TREND_ALIAS = {"UP": "U", "FLAT": "F", "DOWN": "D"}
COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_TREND_SCORE_BAND_ALIAS = {
    "CALM": "C",
    "EDGE": "E",
    "HEATED": "H",
}
VOLATILITY_SCORE = {"steady": 0, "calm": 0, "swing": 1, "spike": 2}

def _collect_volatility_windows(report: dict) -> list[str]:
    candidates = [
        report.get("laneVolatilityMemory"),
        report.get("volatilityMemory"),
        report.get("volatilityWindows"),
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            for key in ("recentBands", "bands", "windows"):
                value = candidate.get(key)
                if isinstance(value, list):
                    return [str(item).lower() for item in value]
        if isinstance(candidate, list):
            return [str(item).lower() for item in candidate]
    return []


def _resolve_compat_row_policy_source(report: dict) -> str:
    windows = _collect_volatility_windows(report)
    if len(windows) >= 2 and all(window in {"swing", "spike"} for window in windows[-2:]):
        return "VOLATILITY_MEMORY"
    return "COPY_PACK"


def _resolve_compat_row_policy_source_confidence(report: dict) -> str:
    windows = _collect_volatility_windows(report)
    if len(windows) >= 3:
        recent = windows[-3:]
        if all(window in {"swing", "spike"} for window in recent):
            if recent.count("spike") >= 2:
                return "HIGH"
            return "MID"
    if len(windows) >= 2 and all(window in {"swing", "spike"} for window in windows[-2:]):
        return "MID"
    return "LOW"


def _resolve_compat_row_policy_source_confidence_trend(report: dict) -> str:
    windows = _collect_volatility_windows(report)
    if len(windows) < 3:
        return "FLAT"

    recent = windows[-2:]
    prior = windows[-4:-2] if len(windows) >= 4 else windows[-3:-1]

    recent_score = sum(VOLATILITY_SCORE.get(window, 1) for window in recent)
    prior_score = sum(VOLATILITY_SCORE.get(window, 1) for window in prior)
    delta = recent_score - prior_score

    if delta >= 1:
        return "UP"
    if delta <= -1:
        return "DOWN"
    return "FLAT"


def _resolve_compat_row_policy_source_confidence_trend_score(report: dict) -> int:
    windows = _collect_volatility_windows(report)
    if not windows:
        return 50

    recent = windows[-4:]
    weights = list(range(1, len(recent) + 1))
    weighted = sum(VOLATILITY_SCORE.get(window, 1) * weight for window, weight in zip(recent, weights))
    max_weighted = 2 * sum(weights)
    if max_weighted <= 0:
        return 50

    return int(round((weighted / max_weighted) * 100))


def _resolve_compat_row_policy_source_confidence_trend_score_band(score: int) -> str:
    if score <= 33:
        return "CALM"
    if score <= 66:
        return "EDGE"
    return "HEATED"


def _resolve_compat_row_policy(gameplay_copy_pack: str) -> str:
    if gameplay_copy_pack == "spike":
        return "SPIKE_ONLY"
    return "ALWAYS"


def _pick_over_cap_gameplay_lane(forced_next_lanes: list[str]) -> str | None:
    if not forced_next_lanes:
        return None
    for lane in GAMEPLAY_LANE_PRIORITY:
        if lane in forced_next_lanes:
            return lane
    return forced_next_lanes[0]


def _resolve_copy_pack(preferred: str, gameplay_lane: str | None) -> str:
    if preferred in COPY_PACKS:
        return preferred
    if gameplay_lane in {"combat", "vfx"}:
        return "spike"
    return "steady"


def build_templates(report: dict, max_templates: int, gameplay_copy_pack: str) -> list[dict]:
    templates: list[dict] = []

    for bucket in report.get("missingCadenceBuckets", []):
        details = BUCKET_TASK_MAP.get(bucket)
        if not details:
            continue
        templates.append(
            {
                "source": "missingCadenceBuckets",
                "bucket": bucket,
                "team": f"{details['label']} Team",
                "task": details["task"],
                "definitionOfDone": details["dod"],
                "verification": "python3 scripts/regression_weekly_portal_prompt_readability_drift.py",
            }
        )

    if report.get("status") == "over-cap":
        forced_next_lanes = report.get("forcedNextLanes", [])
        gameplay_lane = _pick_over_cap_gameplay_lane(forced_next_lanes)
        gameplay_pack = _resolve_copy_pack(gameplay_copy_pack, gameplay_lane)
        gameplay_pack_copy = COPY_PACKS[gameplay_pack]
        if gameplay_lane:
            templates.append(
                {
                    "source": "forcedNextLanes",
                    "lane": gameplay_lane,
                    "team": "World/Combat Team",
                    "copyPack": gameplay_pack,
                    "copyPackAlias": COPY_PACK_ALIAS[gameplay_pack],
                    "task": f"Inject one underrepresented-lane gameplay experiment template for `{gameplay_lane}` when guardrail status is `over-cap`.",
                    "playerFantasy": gameplay_pack_copy["playerFantasy"],
                    "impactMetric": gameplay_pack_copy["impactMetric"],
                    "scope": gameplay_pack_copy["scope"],
                    "risk": gameplay_pack_copy["risk"],
                    "rollback": gameplay_pack_copy["rollback"],
                    "passFail": gameplay_pack_copy["passFail"],
                    "definitionOfDone": "Template includes player-facing fantasy target, impact metric, risk/rollback, and minimal vertical-slice verification commands.",
                    "verification": "python3 scripts/regression_weekly_portal_prompt_readability_drift.py",
                }
            )

        for lane in forced_next_lanes:
            if lane == gameplay_lane:
                continue
            team = LANE_TEAM_MAP.get(lane, "Cross-Lane Team")
            templates.append(
                {
                    "source": "forcedNextLanes",
                    "lane": lane,
                    "team": team,
                    "task": f"Inject one underrepresented-lane experiment template for `{lane}` with minimal vertical slice scope.",
                    "definitionOfDone": "Template has explicit risk/rollback and lane-specific readability impact metric.",
                    "verification": "python3 scripts/regression_weekly_portal_prompt_readability_drift.py",
                }
            )

    return templates[:max_templates]


def to_markdown(
    report: dict,
    templates: list[dict],
    gameplay_copy_pack: str,
    include_copy_pack_compat_row: bool,
) -> str:
    lines = [
        "### Forced-Lane Task Template Draft",
        f"- status: **{report.get('status', 'unknown')}**",
        f"- missing cadence buckets: **{', '.join(report.get('missingCadenceBuckets', [])) or 'none'}**",
        f"- forced next lanes: **{', '.join(report.get('forcedNextLanes', [])) or 'none'}**",
        f"- gameplay copy pack: **{gameplay_copy_pack}**",
    ]
    if include_copy_pack_compat_row:
        lines.append("- COPY PACK COMPAT:STEADY=ST|SPIKE=SP")
        lines.append("- COPY PACK COMPAT LEGEND:ST=STEADY|SP=SPIKE")
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicyAlias in {A,S} and compatRowPolicySignals.policyAlias mirrors compatRowPolicyAlias"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceAlias in {C,V} and compatRowPolicySignals.policySourceAlias mirrors compatRowPolicySourceAlias"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceConfidence in {LOW,MID,HIGH} and compatRowPolicySignals.policySourceConfidence mirrors compatRowPolicySourceConfidence"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidence mirrors compatRowPolicySourceConfidence exactly"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceConfidenceAlias in {L,M,H} and compatRowPolicySignals.policySourceConfidenceAlias mirrors compatRowPolicySourceConfidenceAlias"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidenceAlias mirrors compatRowPolicySourceConfidenceAlias exactly"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceConfidenceTrend in {UP,FLAT,DOWN} and compatRowPolicySignals.policySourceConfidenceTrend mirrors compatRowPolicySourceConfidenceTrend"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidenceTrend mirrors compatRowPolicySourceConfidenceTrend exactly"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceConfidenceTrendAlias in {U,F,D} and compatRowPolicySignals.policySourceConfidenceTrendAlias mirrors compatRowPolicySourceConfidenceTrendAlias"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidenceTrendAlias mirrors compatRowPolicySourceConfidenceTrendAlias exactly"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceConfidenceTrendScore in [0..100] and compatRowPolicySignals.policySourceConfidenceTrendScore mirrors compatRowPolicySourceConfidenceTrendScore"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidenceTrendScore mirrors compatRowPolicySourceConfidenceTrendScore exactly"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceConfidenceTrendScoreBand in {CALM,EDGE,HEATED} and compatRowPolicySignals.policySourceConfidenceTrendScoreBand mirrors compatRowPolicySourceConfidenceTrendScoreBand"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidenceTrendScoreBand mirrors compatRowPolicySourceConfidenceTrendScoreBand exactly"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySourceConfidenceTrendScoreBandAlias in {C,E,H} and compatRowPolicySignals.policySourceConfidenceTrendScoreBandAlias mirrors compatRowPolicySourceConfidenceTrendScoreBandAlias"
    )
    lines.append(
        "- CONTRACT CHECKLIST: compatRowPolicySignals.policySourceConfidenceTrendScoreBandAlias mirrors compatRowPolicySourceConfidenceTrendScoreBandAlias exactly"
    )
    lines.append("")

    if not templates:
        lines.append("- No forced injection templates required from current guardrail snapshot.")
        return "\n".join(lines)

    for template in templates:
        team = template.get("team", "Cross-Lane Team")
        task = template.get("task", "")
        dod = template.get("definitionOfDone", "")
        verification = template.get("verification", "")
        lines.append(f"- [ ] {team}: {task}")
        if template.get("copyPack"):
            lines.append(f"  - Copy pack: {template['copyPack']}")
        if template.get("copyPackAlias"):
            lines.append(f"  - Copy pack alias: CP:{template['copyPackAlias']}")
        if template.get("playerFantasy"):
            lines.append(f"  - Player fantasy: {template['playerFantasy']}")
        if template.get("impactMetric"):
            lines.append(f"  - Impact metric: {template['impactMetric']}")
        if template.get("scope") or template.get("risk"):
            lines.append(
                f"  - Scope/Risk: {template.get('scope', '?')} / {template.get('risk', '?')}"
            )
        if template.get("rollback"):
            lines.append(f"  - Rollback: {template['rollback']}")
        if template.get("passFail"):
            lines.append(f"  - Pass/Fail: {template['passFail']}")
        if template.get("playerFantasy") or template.get("impactMetric"):
            lines.append(
                "  - Quality bar legend: FANT=Player fantasy | IMP=Impact metric | S/R=Scope/Risk | RB=Rollback | P/F=Pass-Fail"
            )
        lines.extend(
            [
                f"  - DoD: {dod}",
                f"  - Verification: `{verification}`",
            ]
        )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guardrail-json", required=True, type=Path)
    parser.add_argument("--max-templates", type=int, default=3)
    parser.add_argument(
        "--gameplay-copy-pack",
        choices=["auto", "steady", "spike"],
        default="auto",
        help="Optional over-cap gameplay template copy pack. Auto resolves to spike for combat/vfx lanes, else steady.",
    )
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    parser.add_argument(
        "--include-copy-pack-compat-row",
        action="store_true",
        help="Emit optional markdown onboarding row: COPY PACK COMPAT:STEADY=ST|SPIKE=SP.",
    )
    args = parser.parse_args()

    report = json.loads(args.guardrail_json.read_text(encoding="utf-8"))
    gameplay_pack = _resolve_copy_pack(
        args.gameplay_copy_pack,
        _pick_over_cap_gameplay_lane(report.get("forcedNextLanes", [])),
    )
    templates = build_templates(
        report,
        max_templates=args.max_templates,
        gameplay_copy_pack=args.gameplay_copy_pack,
    )

    compat_row_policy = _resolve_compat_row_policy(gameplay_pack)
    compat_row_policy_source = _resolve_compat_row_policy_source(report)
    compat_row_policy_source_confidence = _resolve_compat_row_policy_source_confidence(report)
    compat_row_policy_source_confidence_trend = _resolve_compat_row_policy_source_confidence_trend(
        report
    )
    compat_row_policy_source_confidence_trend_score = (
        _resolve_compat_row_policy_source_confidence_trend_score(report)
    )
    compat_row_policy_source_confidence_trend_score_band = (
        _resolve_compat_row_policy_source_confidence_trend_score_band(
            compat_row_policy_source_confidence_trend_score
        )
    )

    payload = {
        "status": report.get("status"),
        "missingCadenceBuckets": report.get("missingCadenceBuckets", []),
        "forcedNextLanes": report.get("forcedNextLanes", []),
        "gameplayCopyPack": gameplay_pack,
        "gameplayCopyPackAlias": COPY_PACK_ALIAS[gameplay_pack],
        "compatRowPolicy": compat_row_policy,
        "compatRowPolicySource": compat_row_policy_source,
        "compatRowPolicySourceAlias": COMPAT_ROW_POLICY_SOURCE_ALIAS[compat_row_policy_source],
        "compatRowPolicySourceConfidence": compat_row_policy_source_confidence,
        "compatRowPolicySourceConfidenceAlias": COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_ALIAS[
            compat_row_policy_source_confidence
        ],
        "compatRowPolicySourceConfidenceTrend": compat_row_policy_source_confidence_trend,
        "compatRowPolicySourceConfidenceTrendAlias": COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_TREND_ALIAS[
            compat_row_policy_source_confidence_trend
        ],
        "compatRowPolicySourceConfidenceTrendScore": compat_row_policy_source_confidence_trend_score,
        "compatRowPolicySourceConfidenceTrendScoreBand": (
            compat_row_policy_source_confidence_trend_score_band
        ),
        "compatRowPolicySourceConfidenceTrendScoreBandAlias": COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_TREND_SCORE_BAND_ALIAS[
            compat_row_policy_source_confidence_trend_score_band
        ],
        "compatRowPolicyAlias": COMPAT_ROW_POLICY_ALIAS[compat_row_policy],
        "compatRowPolicySignals": {
            "volatilityBand": "spike" if gameplay_pack == "spike" else "steady",
            "source": "gameplayCopyPack",
            "policySource": compat_row_policy_source,
            "policySourceAlias": COMPAT_ROW_POLICY_SOURCE_ALIAS[compat_row_policy_source],
            "policySourceConfidence": compat_row_policy_source_confidence,
            "policySourceConfidenceAlias": COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_ALIAS[
                compat_row_policy_source_confidence
            ],
            "policySourceConfidenceTrend": compat_row_policy_source_confidence_trend,
            "policySourceConfidenceTrendAlias": COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_TREND_ALIAS[
                compat_row_policy_source_confidence_trend
            ],
            "policySourceConfidenceTrendScore": compat_row_policy_source_confidence_trend_score,
            "policySourceConfidenceTrendScoreBand": compat_row_policy_source_confidence_trend_score_band,
            "policySourceConfidenceTrendScoreBandAlias": COMPAT_ROW_POLICY_SOURCE_CONFIDENCE_TREND_SCORE_BAND_ALIAS[
                compat_row_policy_source_confidence_trend_score_band
            ],
            "reason": "spike-pack-recommends-gated-onboarding"
            if compat_row_policy == "SPIKE_ONLY"
            else "steady-pack-recommends-always-onboarding",
            "policyAlias": COMPAT_ROW_POLICY_ALIAS[compat_row_policy],
        },
        "templates": templates,
    }

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))

    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(
            to_markdown(
                report,
                templates,
                gameplay_copy_pack=gameplay_pack,
                include_copy_pack_compat_row=args.include_copy_pack_compat_row,
            )
            + "\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
