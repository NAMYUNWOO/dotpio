#!/usr/bin/env python3
"""Combine last-N overclock dwell run artifacts into median trend snapshot."""
from __future__ import annotations

import argparse
import json
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "overclock_dwell_buckets_run_*.json"
DEFAULT_OUT_JSON = ROOT / "logs" / "playtests" / "overclock_dwell_trend.json"
DEFAULT_OUT_MD = ROOT / "logs" / "playtests" / "overclock_dwell_trend.md"


@dataclass
class RunSample:
    path: Path
    generated_at: str
    low: int
    mid: int
    high: int

    @property
    def total(self) -> int:
        return self.low + self.mid + self.high


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-dir", type=Path, default=ROOT / "logs" / "playtests")
    p.add_argument("--pattern", default=DEFAULT_GLOB)
    p.add_argument("--runs", type=int, default=5, help="Number of most recent runs to combine")
    p.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    p.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    return p.parse_args()


def _parse_sample(path: Path) -> RunSample | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    buckets = payload.get("dwellBuckets") or {}
    try:
        low = max(0, int(buckets.get("LOW", 0)))
        mid = max(0, int(buckets.get("MID", 0)))
        high = max(0, int(buckets.get("HIGH", 0)))
    except (TypeError, ValueError):
        return None

    generated_at = str(payload.get("generatedAt", ""))
    if not generated_at:
        generated_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return RunSample(path=path, generated_at=generated_at, low=low, mid=mid, high=high)


def _median_int(values: list[int]) -> int:
    if not values:
        return 0
    return int(round(statistics.median(values)))


def _pct(n: int, d: int) -> float:
    if d <= 0:
        return 0.0
    return round((n / d) * 100.0, 2)


def _classify_volatility(totals: list[int]) -> tuple[str, float, float]:
    if len(totals) < 2:
        return "STEADY", 0.0, 0.0

    rel_deltas: list[float] = []
    for prev, curr in zip(totals, totals[1:]):
        baseline = max(1, prev)
        rel_deltas.append(abs(curr - prev) / baseline)

    max_rel = max(rel_deltas)
    avg_rel = sum(rel_deltas) / len(rel_deltas)
    level = "SWING" if (max_rel >= 0.45 or avg_rel >= 0.30) else "STEADY"
    return level, round(max_rel * 100.0, 2), round(avg_rel * 100.0, 2)


def main() -> int:
    args = parse_args()
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    candidates = sorted(args.input_dir.glob(args.pattern), key=lambda p: p.name)
    samples: list[RunSample] = []
    for path in candidates:
        sample = _parse_sample(path)
        if sample:
            samples.append(sample)

    selected = samples[-max(1, args.runs) :]
    selected_count = len(selected)

    lows = [s.low for s in selected]
    mids = [s.mid for s in selected]
    highs = [s.high for s in selected]
    totals = [s.total for s in selected]

    med_low = _median_int(lows)
    med_mid = _median_int(mids)
    med_high = _median_int(highs)
    med_total = _median_int(totals)

    total_sum = sum(totals)
    low_sum = sum(lows)
    mid_sum = sum(mids)
    high_sum = sum(highs)

    generated_at = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status = "ok" if selected_count > 0 else "insufficient-data"
    volatility_level, max_rel_delta_pct, avg_rel_delta_pct = _classify_volatility(totals)

    payload = {
        "generatedAt": generated_at,
        "status": status,
        "windowRuns": selected_count,
        "requestedRuns": max(1, args.runs),
        "input": {
            "dir": str(args.input_dir),
            "pattern": args.pattern,
        },
        "medians": {
            "LOW": med_low,
            "MID": med_mid,
            "HIGH": med_high,
            "TOTAL": med_total,
        },
        "mixPct": {
            "LOW": _pct(low_sum, total_sum),
            "MID": _pct(mid_sum, total_sum),
            "HIGH": _pct(high_sum, total_sum),
        },
        "volatility": {
            "level": volatility_level,
            "token": f"VOL:{volatility_level}",
            "maxRelDeltaPct": max_rel_delta_pct,
            "avgRelDeltaPct": avg_rel_delta_pct,
        },
        "runs": [
            {
                "generatedAt": s.generated_at,
                "path": str(s.path),
                "LOW": s.low,
                "MID": s.mid,
                "HIGH": s.high,
                "TOTAL": s.total,
            }
            for s in selected
        ],
    }

    args.out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Overclock Dwell Trend",
        "",
        f"- GeneratedAt(UTC): {generated_at}",
        f"- Status: {status}",
        f"- Window runs: {selected_count}/{max(1, args.runs)}",
        f"- Median LOW/MID/HIGH/TOTAL: {med_low} / {med_mid} / {med_high} / {med_total}",
        f"- Exposure mix LOW/MID/HIGH (%): {payload['mixPct']['LOW']} / {payload['mixPct']['MID']} / {payload['mixPct']['HIGH']}",
        f"- Volatility: VOL:{volatility_level} (maxΔ {max_rel_delta_pct}%, avgΔ {avg_rel_delta_pct}%)",
        "",
        "## Included Runs",
    ]

    if selected:
        for s in selected:
            lines.append(
                f"- {s.generated_at} :: L/M/H={s.low}/{s.mid}/{s.high} (TOTAL {s.total}) :: {s.path.name}"
            )
    else:
        lines.append("- No valid run artifacts found for requested window.")

    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[PASS] overclock dwell trend status={status} -> {args.out_json} {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
