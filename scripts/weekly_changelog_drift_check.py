#!/usr/bin/env python3
"""Detect code commits that missed team-log/changelog/report evidence updates."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_JSON = SCRIPT_ROOT / "logs" / "weekly_changelog_drift.json"
DEFAULT_OUT_MD = SCRIPT_ROOT / "logs" / "weekly_changelog_drift.md"

CODE_PREFIXES = (
    "src/",
    "maps/",
    "assets/",
    "libs/",
    "scripts/",
)
CODE_EXACT = {
    "main.lua",
    "map_data.lua",
    "tile_data.lua",
    "item_tile_data.json",
    "conf.lua",
}
EVIDENCE_PREFIXES = (
    "logs/teams/",
    "logs/playtests/",
)
EVIDENCE_EXACT = {
    "CHANGELOG.md",
    "ACTION_ITEMS.md",
    "TASKS.md",
    "POST_RC_BACKLOG.md",
    "logs/sustain_health_dashboard.md",
    "logs/sustain_health_dashboard.json",
    "logs/stale_branch_report_drift.md",
    "logs/stale_branch_report_drift.json",
    "logs/weekly_changelog_drift.md",
    "logs/weekly_changelog_drift.json",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--since-days", type=int, default=7, help="Scan commits in this recent window")
    p.add_argument("--max-commits", type=int, default=200)
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    p.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    return p.parse_args()


def run_git(root: Path, args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def commit_changed_files(root: Path, commit: str) -> list[str]:
    out = run_git(root, ["show", "--name-only", "--pretty=format:", commit])
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_code_file(path: str) -> bool:
    if path in CODE_EXACT:
        return True
    return path.startswith(CODE_PREFIXES)


def is_evidence_file(path: str) -> bool:
    if path in EVIDENCE_EXACT:
        return True
    return path.startswith(EVIDENCE_PREFIXES)


def commit_info(root: Path, commit: str) -> dict[str, Any]:
    raw = run_git(root, ["show", "-s", "--format=%H%n%ct%n%an%n%s", commit]).splitlines()
    sha = raw[0]
    ts = int(raw[1])
    author = raw[2]
    subject = raw[3] if len(raw) >= 4 else ""
    changed = commit_changed_files(root, commit)
    code_files = [p for p in changed if is_code_file(p)]
    evidence_files = [p for p in changed if is_evidence_file(p)]
    return {
        "sha": sha,
        "shortSha": sha[:7],
        "author": author,
        "subject": subject,
        "committedAt": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        "changedFiles": changed,
        "codeFiles": code_files,
        "evidenceFiles": evidence_files,
        "missingEvidence": bool(code_files and not evidence_files),
    }


def main() -> int:
    args = parse_args()
    now = datetime.now(timezone.utc)

    root = args.repo_root.resolve()
    commits_raw = run_git(root, ["rev-list", f"--since={args.since_days}.days", f"--max-count={args.max_commits}", "HEAD"])
    commits = [c for c in commits_raw.splitlines() if c.strip()]

    rows = [commit_info(root, commit) for commit in commits]
    checked = [row for row in rows if row["codeFiles"]]
    missing = [row for row in checked if row["missingEvidence"]]

    payload = {
        "generatedAt": now.isoformat().replace("+00:00", "Z"),
        "status": "ok" if not missing else "warn",
        "window": {"sinceDays": args.since_days, "maxCommits": args.max_commits},
        "checkedCodeCommits": len(checked),
        "missingEvidenceCommits": len(missing),
        "commits": rows,
        "violations": [
            {
                "sha": row["sha"],
                "shortSha": row["shortSha"],
                "committedAt": row["committedAt"],
                "author": row["author"],
                "subject": row["subject"],
                "codeFiles": row["codeFiles"],
            }
            for row in missing
        ],
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Weekly Changelog Drift Check",
        "",
        f"- GeneratedAt(UTC): {payload['generatedAt']}",
        f"- Status: **{payload['status'].upper()}**",
        f"- Window: last {args.since_days} days (max {args.max_commits} commits)",
        f"- Checked code commits: {payload['checkedCodeCommits']}",
        f"- Missing evidence commits: {payload['missingEvidenceCommits']}",
        "",
        "## Violations",
    ]
    if not missing:
        lines.append("- ✅ None")
    else:
        for row in missing:
            lines.append(
                f"- ⚠️ `{row['shortSha']}` {row['subject']} ({row['committedAt']}) code={', '.join(row['codeFiles'][:6])}"
            )

    lines.extend(
        [
            "",
            "## Rule",
            "- Any commit touching code/gameplay paths must include at least one evidence update in the same commit (team log, playtest/report artifact, or changelog/backlog tracker).",
        ]
    )
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[PASS] weekly changelog drift status={payload['status']} -> {args.out_json} {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
