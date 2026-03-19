#!/usr/bin/env python3
"""Regression checks for weekly sustain cron installer CLI behavior."""

from __future__ import annotations

import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_weekly_sustain_cron.sh"


def run(cmd: list[str], expect_ok: bool, must_contain: list[str] | None = None) -> None:
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = f"{result.stdout}\n{result.stderr}"

    if expect_ok and result.returncode != 0:
        raise AssertionError(f"Expected success but failed ({result.returncode}): {' '.join(cmd)}\n{output}")
    if not expect_ok and result.returncode == 0:
        raise AssertionError(f"Expected failure but succeeded: {' '.join(cmd)}\n{output}")

    for token in must_contain or []:
        if token not in output:
            raise AssertionError(f"Missing token `{token}` in output of: {' '.join(cmd)}\n{output}")


def main() -> int:
    if not INSTALLER.exists():
        raise FileNotFoundError(f"Installer not found: {INSTALLER}")

    # Default dry-run path should show managed preview and no mutation message.
    run(
        ["bash", str(INSTALLER)],
        expect_ok=True,
        must_contain=[
            "[INFO] Proposed managed cron entry:",
            "# DOTPIO_WEEKLY_SUSTAIN",
            "[DRY-RUN] No changes applied. Re-run with --apply to upsert.",
        ],
    )

    # CLI override path should reflect provided schedule arguments in output.
    run(
        [
            "bash",
            str(INSTALLER),
            "--minute",
            "15",
            "--hour",
            "6",
            "--dow",
            "2",
            "--tz",
            "UTC",
        ],
        expect_ok=True,
        must_contain=["CRON_TZ=UTC 15 6 * * 2"],
    )

    # Invalid args must fail with explicit guidance.
    run(
        ["bash", str(INSTALLER), "--hour", "99"],
        expect_ok=False,
        must_contain=["[ERROR] --hour must be 0-23"],
    )

    print("[PASS] weekly cron installer regression checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1)
