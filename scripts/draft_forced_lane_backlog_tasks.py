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


def _pick_over_cap_gameplay_lane(forced_next_lanes: list[str]) -> str | None:
    if not forced_next_lanes:
        return None
    for lane in GAMEPLAY_LANE_PRIORITY:
        if lane in forced_next_lanes:
            return lane
    return forced_next_lanes[0]


def build_templates(report: dict, max_templates: int) -> list[dict]:
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
        if gameplay_lane:
            templates.append(
                {
                    "source": "forcedNextLanes",
                    "lane": gameplay_lane,
                    "team": "World/Combat Team",
                    "task": f"Inject one underrepresented-lane gameplay experiment template for `{gameplay_lane}` when guardrail status is `over-cap`.",
                    "playerFantasy": "Keep lane rotation feeling alive with a visible gameplay-facing experiment in the neglected lane.",
                    "impactMetric": "At least one underrepresented lane appears in next-cycle completed items while lane-cap warning resolves.",
                    "scope": "S",
                    "risk": "low",
                    "rollback": "Remove template row and disable over-cap gameplay injection pathway.",
                    "passFail": "Pass when template includes deterministic lane + verification command and guardrail status remains machine-readable.",
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


def to_markdown(report: dict, templates: list[dict]) -> str:
    lines = [
        "### Forced-Lane Task Template Draft",
        f"- status: **{report.get('status', 'unknown')}**",
        f"- missing cadence buckets: **{', '.join(report.get('missingCadenceBuckets', [])) or 'none'}**",
        f"- forced next lanes: **{', '.join(report.get('forcedNextLanes', [])) or 'none'}**",
        "",
    ]

    if not templates:
        lines.append("- No forced injection templates required from current guardrail snapshot.")
        return "\n".join(lines)

    for template in templates:
        team = template.get("team", "Cross-Lane Team")
        task = template.get("task", "")
        dod = template.get("definitionOfDone", "")
        verification = template.get("verification", "")
        lines.append(f"- [ ] {team}: {task}")
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
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    args = parser.parse_args()

    report = json.loads(args.guardrail_json.read_text(encoding="utf-8"))
    templates = build_templates(report, max_templates=args.max_templates)

    payload = {
        "status": report.get("status"),
        "missingCadenceBuckets": report.get("missingCadenceBuckets", []),
        "forcedNextLanes": report.get("forcedNextLanes", []),
        "templates": templates,
    }

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))

    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(to_markdown(report, templates) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
