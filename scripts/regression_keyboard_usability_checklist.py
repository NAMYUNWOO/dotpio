#!/usr/bin/env python3
"""Regression: keyboard-only usability checklist artifact.
Run: python3 scripts/regression_keyboard_usability_checklist.py
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "logs" / "playtests" / "keyboard_only_usability_checklist.md"
KST = timezone(timedelta(hours=9))


@dataclass
class Check:
    label: str
    command: List[str]


CHECKS: List[Check] = [
    Check("keyboard shortcut wiring/help text coverage", ["lua", "scripts/regression_keyboard_shortcuts.lua"]),
    Check("disabled actions keep explicit lock reasons", ["lua", "scripts/regression_action_menu_lock_reasons.lua"]),
    Check("onboarding strip still guides keyboard-first progression", ["lua", "scripts/regression_onboarding_hints.lua"]),
    Check("build preview/confirm keyboard flow remains available", ["lua", "scripts/regression_build_preview_confirm.lua"]),
]


def run_check(check: Check) -> tuple[bool, str]:
    proc = subprocess.run(check.command, cwd=ROOT, capture_output=True, text=True)
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, output if output else "(no output)"


def main() -> int:
    generated = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")
    results: List[tuple[Check, bool, str]] = []

    for check in CHECKS:
        ok, detail = run_check(check)
        results.append((check, ok, detail))

    all_ok = all(ok for _, ok, _ in results)

    lines = [
        "# Keyboard-only Usability Checklist",
        "",
        f"Generated: {generated}",
        "",
        "## Scripted pass/fail",
    ]

    for check, ok, detail in results:
        lines.append(f"- [{'x' if ok else ' '}] {check.label}")
        for row in detail.splitlines()[:6]:
            lines.append(f"  - {row}")
        if len(detail.splitlines()) > 6:
            lines.append("  - ...")

    lines.extend(
        [
            "",
            "## Manual keyboard-only quick pass",
            "- [ ] Start run without mouse input and complete move/search/pickup/inventory/build sequence.",
            "- [ ] In inventory, use only keyboard to navigate panels, open Action Menu, and execute U/E/D/S/X quick actions.",
            "- [ ] Confirm lock reasons are readable without attempting disabled actions.",
            "- [ ] Confirm help dialog (F1) includes all critical keys (F1/F5/F9/Tab/I/G).",
            "- [ ] Confirm inventory can be closed/reopened with keyboard (Esc/F10 + Tab/I) and gameplay resumes cleanly.",
            "",
            f"Result: {'PASS' if all_ok else 'FAIL'}",
        ]
    )

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if all_ok:
        print("[PASS] keyboard-only usability checklist regression validated")
        print(f"artifact: {ARTIFACT}")
        return 0

    failed = [check.label for check, ok, _ in results if not ok]
    print(f"[FAIL] keyboard-only checklist failed: {', '.join(failed)}")
    print(f"artifact: {ARTIFACT}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
