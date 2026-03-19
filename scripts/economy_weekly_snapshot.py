#!/usr/bin/env python3
"""Generate weekly SRL telemetry snapshot for post-RC sustain checks."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TELEMETRY_PATH = ROOT / "logs" / "economy_telemetry.ndjson"
DEFAULT_ANTI_EXPLOIT_PATH = ROOT / "logs" / "economy_anti_exploit_report.json"
DEFAULT_OUT_MD = ROOT / "logs" / "economy_weekly_snapshot.md"
DEFAULT_OUT_JSON = ROOT / "logs" / "economy_weekly_snapshot.json"


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--telemetry", type=Path, default=DEFAULT_TELEMETRY_PATH)
    parser.add_argument("--anti-exploit", type=Path, default=DEFAULT_ANTI_EXPLOIT_PATH)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    return parser.parse_args()


def load_previous_snapshot(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def main() -> int:
    args = parse_args()

    rows = []
    with args.telemetry.open("r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError:
                continue
            ts = entry.get("ts")
            if not ts:
                continue
            try:
                entry["_ts"] = parse_ts(ts)
            except ValueError:
                continue
            rows.append(entry)

    if not rows:
        raise SystemExit("No telemetry rows found")

    latest_ts = max(r["_ts"] for r in rows)
    week_start = latest_ts - timedelta(days=7)
    weekly = [r for r in rows if r["_ts"] >= week_start]

    status_counts = Counter(r.get("status", "unknown") for r in weekly)
    event_counts = Counter(r.get("event", "unknown") for r in weekly)

    total_srl_spent = sum(int(r.get("srlSpent", 0) or 0) for r in weekly)
    build_ok_spent = sum(int(r.get("srlSpent", 0) or 0) for r in weekly if r.get("event") == "build" and r.get("status") == "ok")

    anti = {}
    if args.anti_exploit.exists():
        anti = json.loads(args.anti_exploit.read_text(encoding="utf-8"))

    suspicious_count = int(anti.get("suspiciousCount", 0) or 0)
    decision = "NO_CURVE_CHANGE" if suspicious_count == 0 else "REBALANCE_REQUIRED"
    rationale = (
        "No suspicious net-positive exploit windows detected in the latest anti-exploit report."
        if suspicious_count == 0
        else "Suspicious exploit windows detected; adjust SRL cost/salvage knobs before next release cut."
    )

    previous = load_previous_snapshot(args.out_json)
    previous_event_count = int(previous.get("telemetryEventCount", 0) or 0)
    previous_total_srl_spent = int(previous.get("totalSrlSpent", 0) or 0)

    telemetry_event_count = len(weekly)
    telemetry_event_delta = telemetry_event_count - previous_event_count if previous else None
    total_srl_spent_delta = total_srl_spent - previous_total_srl_spent if previous else None

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "windowStart": week_start.isoformat().replace("+00:00", "Z"),
        "windowEnd": latest_ts.isoformat().replace("+00:00", "Z"),
        "telemetryEventCount": telemetry_event_count,
        "events": dict(event_counts),
        "status": dict(status_counts),
        "totalSrlSpent": total_srl_spent,
        "buildOkSrlSpent": build_ok_spent,
        "suspiciousCount": suspicious_count,
        "decision": decision,
        "decisionRationale": rationale,
        "comparedToPrevious": bool(previous),
        "deltaFromPrevious": {
            "telemetryEventCount": telemetry_event_delta,
            "totalSrlSpent": total_srl_spent_delta,
        },
    }
    args.out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if previous:
        delta_line = f"- Delta vs previous snapshot: events {telemetry_event_delta:+d}, total SRL spent {total_srl_spent_delta:+d}"
    else:
        delta_line = "- Delta vs previous snapshot: n/a (first snapshot baseline)"

    md = [
        "# Weekly SRL Economy Snapshot",
        "",
        f"- GeneratedAt(UTC): {payload['generatedAt']}",
        f"- Window: {payload['windowStart']} ~ {payload['windowEnd']}",
        f"- Telemetry events: {telemetry_event_count}",
        f"- Event counts: {dict(event_counts)}",
        f"- Status counts: {dict(status_counts)}",
        f"- Total SRL spent: {total_srl_spent}",
        f"- Build(ok) SRL spent: {build_ok_spent}",
        f"- Anti-exploit suspicious windows: {suspicious_count}",
        delta_line,
        "",
        "## Rebalance Decision",
        f"- Decision: **{decision}**",
        f"- Rationale: {rationale}",
    ]
    args.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {args.out_md}")
    print(f"Wrote {args.out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
