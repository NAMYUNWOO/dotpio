#!/usr/bin/env python3
"""Generate sustain health dashboard markdown from weekly sustain artifacts."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT_JSON = ROOT / "logs" / "economy_weekly_snapshot.json"
DEFAULT_ANTI_JSON = ROOT / "logs" / "economy_anti_exploit_report.json"
DEFAULT_AUDIT_JSON = ROOT / "logs" / "weekly_sustain_cron_audit.json"
DEFAULT_OUT_MD = ROOT / "logs" / "sustain_health_dashboard.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-json", type=Path, default=DEFAULT_SNAPSHOT_JSON)
    parser.add_argument("--anti-exploit-json", type=Path, default=DEFAULT_ANTI_JSON)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def badge(ok: bool, label: str) -> str:
    icon = "✅" if ok else "⚠️"
    return f"{icon} {label}"


def main() -> int:
    args = parse_args()

    snapshot = load_json(args.snapshot_json)
    anti = load_json(args.anti_exploit_json)
    audit = load_json(args.audit_json)

    decision = str(snapshot.get("decision", "UNKNOWN"))
    suspicious_count = int(snapshot.get("suspiciousCount", anti.get("suspiciousCount", 0)) or 0)
    telemetry_event_count = int(snapshot.get("telemetryEventCount", 0) or 0)
    total_srl_spent = int(snapshot.get("totalSrlSpent", 0) or 0)
    delta = snapshot.get("deltaFromPrevious", {}) if isinstance(snapshot.get("deltaFromPrevious"), dict) else {}

    economy_ok = decision == "NO_CURVE_CHANGE" and suspicious_count == 0
    telemetry_ok = telemetry_event_count > 0
    cron_ok = audit.get("status") == "ok"

    health_score = sum([economy_ok, telemetry_ok, cron_ok])
    health_tier = {3: "GREEN", 2: "YELLOW", 1: "ORANGE", 0: "RED"}[health_score]

    lines = [
        "# DOTPIO Sustain Health Dashboard",
        "",
        f"- GeneratedAt(UTC): {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        f"- Overall: **{health_tier}** ({health_score}/3 checks green)",
        "",
        "## Signals",
        f"- {badge(economy_ok, 'Economy safety')}: decision={decision}, suspiciousWindows={suspicious_count}",
        f"- {badge(telemetry_ok, 'Telemetry freshness')}: weeklyEvents={telemetry_event_count}, totalSrlSpent={total_srl_spent}",
        f"- {badge(cron_ok, 'Scheduler policy audit')}: status={audit.get('status', 'missing')}",
        "",
        "## Weekly Snapshot",
        f"- Window: {snapshot.get('windowStart', 'n/a')} ~ {snapshot.get('windowEnd', 'n/a')}",
        f"- Decision: **{decision}**",
        f"- Rationale: {snapshot.get('decisionRationale', 'n/a')}",
        f"- Delta events: {delta.get('telemetryEventCount', 'n/a')}",
        f"- Delta total SRL spent: {delta.get('totalSrlSpent', 'n/a')}",
        "",
        "## Scheduler Policy",
    ]

    if cron_ok:
        lines.extend(
            [
                f"- CRON_TZ: {audit.get('tz', 'n/a')}",
                f"- Schedule: minute={audit.get('minute', 'n/a')} hour={audit.get('hour', 'n/a')} dow={audit.get('dow', 'n/a')}",
                f"- Log path: {audit.get('log_path', 'n/a')}",
                f"- Rotate max size (MB): {audit.get('max_log_size_mb', 'n/a')}",
                f"- Retain rotated logs: {audit.get('retain_rotated_logs', 'n/a')}",
                f"- Max rotated age days: {audit.get('max_rotated_age_days', 'n/a')}",
            ]
        )
    else:
        lines.append("- Managed weekly sustain cron entry not found or audit artifact missing.")

    lines.extend(
        [
            "",
            "## Action",
            "- If overall is YELLOW/ORANGE/RED: run `bash scripts/run_weekly_sustain.sh` and investigate the failing signal before next RC cut.",
        ]
    )

    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
