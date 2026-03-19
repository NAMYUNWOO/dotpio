#!/usr/bin/env python3
"""Generate weekly SRL telemetry snapshot for post-RC sustain checks."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TELEMETRY_PATH = ROOT / "logs" / "economy_telemetry.ndjson"
ANTI_EXPLOIT_PATH = ROOT / "logs" / "economy_anti_exploit_report.json"
OUT_MD = ROOT / "logs" / "economy_weekly_snapshot.md"
OUT_JSON = ROOT / "logs" / "economy_weekly_snapshot.json"


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def main() -> int:
    rows = []
    with TELEMETRY_PATH.open("r", encoding="utf-8") as f:
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
    if ANTI_EXPLOIT_PATH.exists():
        anti = json.loads(ANTI_EXPLOIT_PATH.read_text(encoding="utf-8"))

    suspicious_count = int(anti.get("suspiciousCount", 0) or 0)
    decision = "NO_CURVE_CHANGE" if suspicious_count == 0 else "REBALANCE_REQUIRED"
    rationale = (
        "No suspicious net-positive exploit windows detected in the latest anti-exploit report."
        if suspicious_count == 0
        else "Suspicious exploit windows detected; adjust SRL cost/salvage knobs before next release cut."
    )

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "windowStart": week_start.isoformat().replace("+00:00", "Z"),
        "windowEnd": latest_ts.isoformat().replace("+00:00", "Z"),
        "events": dict(event_counts),
        "status": dict(status_counts),
        "totalSrlSpent": total_srl_spent,
        "buildOkSrlSpent": build_ok_spent,
        "suspiciousCount": suspicious_count,
        "decision": decision,
        "decisionRationale": rationale,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Weekly SRL Economy Snapshot",
        "",
        f"- GeneratedAt(UTC): {payload['generatedAt']}",
        f"- Window: {payload['windowStart']} ~ {payload['windowEnd']}",
        f"- Telemetry events: {len(weekly)}",
        f"- Event counts: {dict(event_counts)}",
        f"- Status counts: {dict(status_counts)}",
        f"- Total SRL spent: {total_srl_spent}",
        f"- Build(ok) SRL spent: {build_ok_spent}",
        f"- Anti-exploit suspicious windows: {suspicious_count}",
        "",
        "## Rebalance Decision",
        f"- Decision: **{decision}**",
        f"- Rationale: {rationale}",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
