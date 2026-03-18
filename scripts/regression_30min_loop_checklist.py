#!/usr/bin/env python3
"""Regression: scripted 30-minute core-loop checklist + artifact.
Run: python3 scripts/regression_30min_loop_checklist.py
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "logs" / "playtests" / "loop_30min_checklist.md"
KST = timezone(timedelta(hours=9))


@dataclass
class Check:
    label: str
    command: List[str]


CHECKS: List[Check] = [
    Check("starter loadout baseline is stable", ["lua", "scripts/regression_starter_loadout.lua"]),
    Check("economy telemetry emits build/disassemble envelopes", ["lua", "scripts/regression_economy_telemetry.lua"]),
    Check("build preview/confirm gate preserves explicit consumption", ["lua", "scripts/regression_build_preview_confirm.lua"]),
    Check("BUILDER.SRL affordance copy stays explicit", ["lua", "scripts/regression_builder_srl_affordance.lua"]),
    Check("SRL cost curve suppresses low-tier spam", ["lua", "scripts/regression_srl_cost_curve.lua"]),
    Check("disassembly caps remain size-tier fair", ["lua", "scripts/regression_disassembly_caps.lua"]),
    Check("anti-exploit loop detection flags suspicious windows", ["lua", "scripts/regression_anti_exploit_report.lua"]),
    Check("map_01~04 progression + portal wiring remains valid", [sys.executable, "scripts/regression_map_progression.py"]),
]


def run_check(check: Check) -> tuple[bool, str]:
    proc = subprocess.run(check.command, cwd=ROOT, capture_output=True, text=True)
    output = (proc.stdout + proc.stderr).strip()
    detail = output if output else "(no output)"
    return proc.returncode == 0, detail


def main() -> int:
    kst_label = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")
    results: List[tuple[Check, bool, str]] = []

    for check in CHECKS:
        ok, detail = run_check(check)
        results.append((check, ok, detail))

    all_ok = all(ok for _, ok, _ in results)

    lines = [
        "# 30-minute Core Loop Checklist",
        "",
        f"Generated: {kst_label}",
        "",
        "## Scripted pass/fail",
    ]

    for check, ok, detail in results:
        lines.append(f"- [{'x' if ok else ' '}] {check.label}")
        for chunk_line in detail.splitlines()[:6]:
            lines.append(f"  - {chunk_line}")
        if len(detail.splitlines()) > 6:
            lines.append("  - ...")

    lines.extend(
        [
            "",
            "## Session momentum checklist (manual quick pass)",
            "- [ ] In one run, complete at least one fight -> loot -> disassemble -> build chain.",
            "- [ ] Confirm BUILDER.SRL drops/replenishes in expected range without flat-profit farming.",
            "- [ ] Confirm map progression map_01 -> map_0X transitions do not break combat/loot flow.",
            "",
            f"Result: {'PASS' if all_ok else 'FAIL'}",
        ]
    )

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if all_ok:
        print("[PASS] 30-minute core loop checklist regression validated")
        print(f"artifact: {ARTIFACT}")
        return 0

    failed = [check.label for check, ok, _ in results if not ok]
    print(f"[FAIL] 30-minute core loop checklist failed: {', '.join(failed)}")
    print(f"artifact: {ARTIFACT}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
