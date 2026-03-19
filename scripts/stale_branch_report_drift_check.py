#!/usr/bin/env python3
"""Check branch freshness and sustain-report drift, emit markdown+json status."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATHS = [
    ROOT / "logs" / "economy_anti_exploit_report.json",
    ROOT / "logs" / "economy_weekly_snapshot.json",
    ROOT / "logs" / "sustain_health_dashboard.md",
]
DEFAULT_OUT_JSON = ROOT / "logs" / "stale_branch_report_drift.json"
DEFAULT_OUT_MD = ROOT / "logs" / "stale_branch_report_drift.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--branch-max-age-days", type=int, default=7)
    p.add_argument("--report-max-age-days", type=int, default=8)
    p.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    p.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    p.add_argument("--report-path", action="append", type=Path, default=[])
    return p.parse_args()


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def iso_to_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_generated_at(path: Path) -> datetime | None:
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    if path.suffix.lower() == ".json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict):
            ts = iso_to_dt(str(payload.get("generatedAt", "")))
            if ts:
                return ts
    for line in text.splitlines():
        if line.lower().startswith("- generatedat"):
            _, _, raw = line.partition(":")
            ts = iso_to_dt(raw.strip())
            if ts:
                return ts
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def main() -> int:
    args = parse_args()
    now = datetime.now(timezone.utc)

    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    upstream = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    behind, ahead = [int(v) for v in run_git(["rev-list", "--left-right", "--count", f"{upstream}...HEAD"]).split()]
    last_commit_ts = int(run_git(["show", "-s", "--format=%ct", "HEAD"]))
    last_commit_at = datetime.fromtimestamp(last_commit_ts, tz=timezone.utc)
    branch_age_days = (now - last_commit_at).total_seconds() / 86400

    branch_ok = behind == 0 and branch_age_days <= args.branch_max_age_days

    report_paths = args.report_path if args.report_path else DEFAULT_REPORT_PATHS
    reports: list[dict[str, Any]] = []
    report_ok = True
    for path in report_paths:
        ts = parse_generated_at(path)
        if ts is None:
            age_days = None
            ok = False
            report_ok = False
        else:
            age_days = (now - ts).total_seconds() / 86400
            ok = age_days <= args.report_max_age_days
            if not ok:
                report_ok = False
        try:
            path_label = str(path.relative_to(ROOT)) if path.is_absolute() else str(path)
        except ValueError:
            path_label = str(path)
        reports.append(
            {
                "path": path_label,
                "generatedAt": ts.isoformat().replace("+00:00", "Z") if ts else None,
                "ageDays": round(age_days, 2) if age_days is not None else None,
                "ok": ok,
            }
        )

    status = "ok" if branch_ok and report_ok else "warn"
    payload = {
        "status": status,
        "generatedAt": now.isoformat().replace("+00:00", "Z"),
        "thresholds": {
            "branchMaxAgeDays": args.branch_max_age_days,
            "reportMaxAgeDays": args.report_max_age_days,
        },
        "branch": {
            "name": branch,
            "upstream": upstream,
            "ahead": ahead,
            "behind": behind,
            "lastCommitAt": last_commit_at.isoformat().replace("+00:00", "Z"),
            "ageDays": round(branch_age_days, 2),
            "ok": branch_ok,
        },
        "reports": reports,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        "# Stale Branch / Report Drift Check",
        "",
        f"- GeneratedAt(UTC): {payload['generatedAt']}",
        f"- Status: **{status.upper()}**",
        f"- Branch: `{branch}` (upstream `{upstream}`)",
        f"- Ahead/Behind: {ahead}/{behind}",
        f"- Last commit age: {payload['branch']['ageDays']} days (threshold <= {args.branch_max_age_days})",
        "",
        "## Report Freshness",
    ]
    for row in reports:
        mark = "✅" if row["ok"] else "⚠️"
        md_lines.append(
            f"- {mark} `{row['path']}` age={row['ageDays']} days generatedAt={row['generatedAt']}"
        )

    args.out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[PASS] stale/drift check status={status} -> {args.out_json} {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
