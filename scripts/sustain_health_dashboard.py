#!/usr/bin/env python3
"""Generate sustain health dashboard markdown/json from weekly sustain artifacts."""
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
DEFAULT_OUT_JSON = ROOT / "logs" / "sustain_health_dashboard.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-json", type=Path, default=DEFAULT_SNAPSHOT_JSON)
    parser.add_argument("--anti-exploit-json", type=Path, default=DEFAULT_ANTI_JSON)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--format", choices=("md", "json"), default="md")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output (requires --format json)")
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


def classify_trend(decision: str, suspicious_count: int, delta_events: int | None, delta_srl_spent: int | None) -> str:
    if suspicious_count > 0 or decision != "NO_CURVE_CHANGE":
        return "degrading"
    if delta_events is None and delta_srl_spent is None:
        return "stable"

    score = 0
    if delta_events is not None:
        score += 1 if delta_events > 0 else -1 if delta_events < 0 else 0
    if delta_srl_spent is not None:
        score += 1 if delta_srl_spent > 0 else -1 if delta_srl_spent < 0 else 0

    if score > 0:
        return "improving"
    if score < 0:
        return "degrading"
    return "stable"


def compute_regression_risk_score(
    *,
    economy_ok: bool,
    decision: str,
    suspicious_count: int,
    telemetry_ok: bool,
    cron_ok: bool,
    trend: str,
    delta_events: int | None,
) -> tuple[int, str, str]:
    score = 0

    if not economy_ok:
        score += 35
    if decision != "NO_CURVE_CHANGE":
        score += 20
    if suspicious_count > 0:
        score += min(30, suspicious_count * 10)
    if not telemetry_ok:
        score += 15
    if delta_events is not None and delta_events < 0:
        score += 10
    if not cron_ok:
        score += 20

    if trend == "degrading":
        score += 15
    elif trend == "stable":
        score += 5

    score = max(0, min(100, score))

    if score >= 60:
        level = "HIGH"
        alert = "ALERT"
    elif score >= 30:
        level = "MEDIUM"
        alert = "WARN"
    else:
        level = "LOW"
        alert = "OK"

    return score, level, alert


def build_regression_risk_drivers(
    *,
    economy_ok: bool,
    decision: str,
    suspicious_count: int,
    telemetry_ok: bool,
    cron_ok: bool,
    trend: str,
    delta_events: int | None,
) -> list[dict[str, Any]]:
    drivers: list[tuple[str, int, str]] = []

    if not economy_ok:
        drivers.append(("economySafetyFail", 35, "Economy safety signal failed"))
    if decision != "NO_CURVE_CHANGE":
        drivers.append(("curveChangeRequired", 20, f"Decision={decision}"))
    if suspicious_count > 0:
        points = min(30, suspicious_count * 10)
        drivers.append(("suspiciousWindows", points, f"suspiciousWindows={suspicious_count}"))
    if not telemetry_ok:
        drivers.append(("telemetryFreshnessFail", 15, "Weekly telemetry events missing"))
    if delta_events is not None and delta_events < 0:
        drivers.append(("deltaEventsNegative", 10, f"deltaEvents={delta_events}"))
    if not cron_ok:
        drivers.append(("schedulerPolicyAuditFail", 20, "Cron audit status not ok"))

    if trend == "degrading":
        drivers.append(("trendDegrading", 15, "Trend classification is degrading"))
    elif trend == "stable":
        drivers.append(("trendStable", 5, "Trend classification is stable"))

    if not drivers:
        drivers.append(("baseline", 0, "No active risk contributors"))

    drivers.sort(key=lambda row: row[1], reverse=True)
    return [
        {"name": name, "points": points, "detail": detail}
        for name, points, detail in drivers
    ]


def build_dashboard_payload(snapshot: dict[str, Any], anti: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    decision = str(snapshot.get("decision", "UNKNOWN"))
    suspicious_count = int(snapshot.get("suspiciousCount", anti.get("suspiciousCount", 0)) or 0)
    telemetry_event_count = int(snapshot.get("telemetryEventCount", 0) or 0)
    total_srl_spent = int(snapshot.get("totalSrlSpent", 0) or 0)
    delta = snapshot.get("deltaFromPrevious", {}) if isinstance(snapshot.get("deltaFromPrevious"), dict) else {}

    delta_events = delta.get("telemetryEventCount") if isinstance(delta.get("telemetryEventCount"), int) else None
    delta_srl_spent = delta.get("totalSrlSpent") if isinstance(delta.get("totalSrlSpent"), int) else None

    economy_ok = decision == "NO_CURVE_CHANGE" and suspicious_count == 0
    telemetry_ok = telemetry_event_count > 0
    cron_ok = audit.get("status") == "ok"

    health_score = sum([economy_ok, telemetry_ok, cron_ok])
    health_tier = {3: "GREEN", 2: "YELLOW", 1: "ORANGE", 0: "RED"}[health_score]
    trend = classify_trend(decision, suspicious_count, delta_events, delta_srl_spent)
    risk_score, risk_level, risk_alert = compute_regression_risk_score(
        economy_ok=economy_ok,
        decision=decision,
        suspicious_count=suspicious_count,
        telemetry_ok=telemetry_ok,
        cron_ok=cron_ok,
        trend=trend,
        delta_events=delta_events,
    )
    risk_drivers = build_regression_risk_drivers(
        economy_ok=economy_ok,
        decision=decision,
        suspicious_count=suspicious_count,
        telemetry_ok=telemetry_ok,
        cron_ok=cron_ok,
        trend=trend,
        delta_events=delta_events,
    )

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return {
        "generatedAt": generated_at,
        "overall": {
            "tier": health_tier,
            "trend": trend,
            "score": health_score,
            "totalChecks": 3,
        },
        "regressionRisk": {
            "score": risk_score,
            "level": risk_level,
            "alert": risk_alert,
            "topDrivers": risk_drivers[:3],
            "thresholds": {
                "warnAt": 30,
                "alertAt": 60,
            },
        },
        "signals": {
            "economySafety": {
                "ok": economy_ok,
                "decision": decision,
                "suspiciousWindows": suspicious_count,
            },
            "telemetryFreshness": {
                "ok": telemetry_ok,
                "weeklyEvents": telemetry_event_count,
                "totalSrlSpent": total_srl_spent,
            },
            "schedulerPolicyAudit": {
                "ok": cron_ok,
                "status": audit.get("status", "missing"),
            },
        },
        "weeklySnapshot": {
            "windowStart": snapshot.get("windowStart", "n/a"),
            "windowEnd": snapshot.get("windowEnd", "n/a"),
            "decision": decision,
            "decisionRationale": snapshot.get("decisionRationale", "n/a"),
            "delta": {
                "telemetryEventCount": delta.get("telemetryEventCount", "n/a"),
                "totalSrlSpent": delta.get("totalSrlSpent", "n/a"),
            },
        },
        "schedulerPolicy": {
            "status": audit.get("status", "missing"),
            "tz": audit.get("tz", "n/a"),
            "minute": audit.get("minute", "n/a"),
            "hour": audit.get("hour", "n/a"),
            "dow": audit.get("dow", "n/a"),
            "logPath": audit.get("log_path", "n/a"),
            "maxLogSizeMb": audit.get("max_log_size_mb", "n/a"),
            "retainRotatedLogs": audit.get("retain_rotated_logs", "n/a"),
            "maxRotatedAgeDays": audit.get("max_rotated_age_days", "n/a"),
        },
        "action": "If overall is YELLOW/ORANGE/RED OR regression risk alert is WARN/ALERT: run `bash scripts/run_weekly_sustain.sh` and investigate before next RC cut.",
    }


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    signals = payload["signals"]
    weekly = payload["weeklySnapshot"]
    scheduler = payload["schedulerPolicy"]
    risk = payload["regressionRisk"]

    lines = [
        "# DOTPIO Sustain Health Dashboard",
        "",
        f"- GeneratedAt(UTC): {payload['generatedAt']}",
        f"- Overall: **{payload['overall']['tier']}** ({payload['overall']['score']}/{payload['overall']['totalChecks']} checks green)",
        f"- Trend: **{payload['overall']['trend']}**",
        "",
        "## Regression Risk",
        f"- Score: **{risk['score']} / 100**",
        f"- Level: **{risk['level']}**",
        f"- Threshold alert: **{risk['alert']}** (WARN >= {risk['thresholds']['warnAt']}, ALERT >= {risk['thresholds']['alertAt']})",
        "- Top drivers:",
    ]

    for driver in risk.get("topDrivers", []):
        lines.append(f"  - {driver['name']}: +{driver['points']} ({driver['detail']})")

    lines.extend([
        "",
        "## Signals",
        f"- {badge(bool(signals['economySafety']['ok']), 'Economy safety')}: decision={signals['economySafety']['decision']}, suspiciousWindows={signals['economySafety']['suspiciousWindows']}",
        f"- {badge(bool(signals['telemetryFreshness']['ok']), 'Telemetry freshness')}: weeklyEvents={signals['telemetryFreshness']['weeklyEvents']}, totalSrlSpent={signals['telemetryFreshness']['totalSrlSpent']}",
        f"- {badge(bool(signals['schedulerPolicyAudit']['ok']), 'Scheduler policy audit')}: status={signals['schedulerPolicyAudit']['status']}",
        "",
        "## Weekly Snapshot",
        f"- Window: {weekly['windowStart']} ~ {weekly['windowEnd']}",
        f"- Decision: **{weekly['decision']}**",
        f"- Rationale: {weekly['decisionRationale']}",
        f"- Delta events: {weekly['delta']['telemetryEventCount']}",
        f"- Delta total SRL spent: {weekly['delta']['totalSrlSpent']}",
        "",
        "## Scheduler Policy",
    ])

    if signals["schedulerPolicyAudit"]["ok"]:
        lines.extend(
            [
                f"- CRON_TZ: {scheduler['tz']}",
                f"- Schedule: minute={scheduler['minute']} hour={scheduler['hour']} dow={scheduler['dow']}",
                f"- Log path: {scheduler['logPath']}",
                f"- Rotate max size (MB): {scheduler['maxLogSizeMb']}",
                f"- Retain rotated logs: {scheduler['retainRotatedLogs']}",
                f"- Max rotated age days: {scheduler['maxRotatedAgeDays']}",
            ]
        )
    else:
        lines.append("- Managed weekly sustain cron entry not found or audit artifact missing.")

    lines.extend(["", "## Action", f"- {payload['action']}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any], pretty: bool) -> None:
    if pretty:
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    else:
        text = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()

    if args.pretty and args.format != "json":
        raise SystemExit("--pretty is only supported with --format json")

    snapshot = load_json(args.snapshot_json)
    anti = load_json(args.anti_exploit_json)
    audit = load_json(args.audit_json)

    payload = build_dashboard_payload(snapshot, anti, audit)

    if args.format == "json":
        write_json(args.out_json, payload, args.pretty)
        print(f"Wrote {args.out_json}")
    else:
        write_markdown(args.out_md, payload)
        print(f"Wrote {args.out_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
