#!/usr/bin/env python3
"""Regression checks for weekly sustain cron installer CLI behavior."""

from __future__ import annotations

import os
import pathlib
import subprocess
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_weekly_sustain_cron.sh"
MARKER = "# DOTPIO_WEEKLY_SUSTAIN"


def run(
    cmd: list[str],
    expect_ok: bool,
    must_contain: list[str] | None = None,
    env: dict[str, str] | None = None,
) -> str:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=run_env,
    )
    output = f"{result.stdout}\n{result.stderr}"

    if expect_ok and result.returncode != 0:
        raise AssertionError(f"Expected success but failed ({result.returncode}): {' '.join(cmd)}\n{output}")
    if not expect_ok and result.returncode == 0:
        raise AssertionError(f"Expected failure but succeeded: {' '.join(cmd)}\n{output}")

    for token in must_contain or []:
        if token not in output:
            raise AssertionError(f"Missing token `{token}` in output of: {' '.join(cmd)}\n{output}")

    return output


def assert_has_exactly_one_marker(cron_content: str) -> None:
    marker_hits = [line for line in cron_content.splitlines() if MARKER in line]
    if len(marker_hits) != 1:
        raise AssertionError(
            f"Expected exactly one managed cron entry, got {len(marker_hits)}.\n{cron_content}"
        )


def main() -> int:
    if not INSTALLER.exists():
        raise FileNotFoundError(f"Installer not found: {INSTALLER}")

    # Default dry-run path should show managed preview and no mutation message.
    run(
        ["bash", str(INSTALLER)],
        expect_ok=True,
        must_contain=[
            "[INFO] Proposed managed cron entry:",
            MARKER,
            "[DRY-RUN] No changes applied. Re-run with --apply to upsert.",
        ],
    )

    # CLI override path should reflect provided schedule arguments + custom log path in output.
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
            "--log-path",
            "/tmp/dotpio-weekly.log",
            "--max-log-size-mb",
            "12",
        ],
        expect_ok=True,
        must_contain=[
            "CRON_TZ=UTC 15 6 * * 2",
            "/tmp/dotpio-weekly.log",
            "bash scripts/rotate_log_if_needed.sh /tmp/dotpio-weekly.log 12",
        ],
    )

    # Invalid args must fail with explicit guidance.
    run(
        ["bash", str(INSTALLER), "--hour", "99"],
        expect_ok=False,
        must_contain=["[ERROR] --hour must be 0-23"],
    )
    run(
        ["bash", str(INSTALLER), "--max-log-size-mb", "0"],
        expect_ok=False,
        must_contain=["[ERROR] --max-log-size-mb must be a positive integer"],
    )

    # Apply path should be safely testable via injected crontab binary.
    with tempfile.TemporaryDirectory(prefix="dotpio-cron-reg-") as temp_dir:
        temp_path = pathlib.Path(temp_dir)
        fake_crontab = temp_path / "fake_crontab.py"
        state_file = temp_path / "cron_state.txt"

        fake_crontab.write_text(
            """#!/usr/bin/env python3
import os
import pathlib
import sys

state_path = pathlib.Path(os.environ.get(\"FAKE_CRON_STATE\", \"\"))
if not str(state_path):
    print(\"missing FAKE_CRON_STATE\", file=sys.stderr)
    raise SystemExit(2)
state_path.parent.mkdir(parents=True, exist_ok=True)
state_path.touch(exist_ok=True)

arg = sys.argv[1] if len(sys.argv) > 1 else \"\"
if arg == \"-l\":
    sys.stdout.write(state_path.read_text(encoding=\"utf-8\"))
    raise SystemExit(0)
if arg == \"-\":
    state_path.write_text(sys.stdin.read(), encoding=\"utf-8\")
    raise SystemExit(0)

print(f\"unsupported args: {' '.join(sys.argv[1:])}\", file=sys.stderr)
raise SystemExit(2)
""",
            encoding="utf-8",
        )
        fake_crontab.chmod(0o755)

        env = {
            "CRONTAB_BIN": str(fake_crontab),
            "FAKE_CRON_STATE": str(state_file),
        }

        # First apply should insert exactly one managed entry.
        run(
            ["bash", str(INSTALLER), "--apply", "--minute", "5", "--hour", "10", "--dow", "3"],
            expect_ok=True,
            must_contain=["[OK] Managed weekly sustain cron upserted."],
            env=env,
        )
        first_state = state_file.read_text(encoding="utf-8")
        assert_has_exactly_one_marker(first_state)
        if "CRON_TZ=Asia/Seoul 5 10 * * 3" not in first_state:
            raise AssertionError(f"Applied cron content missing expected schedule.\n{first_state}")

        # Re-apply with new schedule should upsert (replace marker entry, not duplicate).
        run(
            ["bash", str(INSTALLER), "--apply", "--minute", "25", "--hour", "11", "--dow", "4"],
            expect_ok=True,
            must_contain=["[OK] Managed weekly sustain cron upserted."],
            env=env,
        )
        second_state = state_file.read_text(encoding="utf-8")
        assert_has_exactly_one_marker(second_state)
        if "CRON_TZ=Asia/Seoul 25 11 * * 4" not in second_state:
            raise AssertionError(f"Updated cron content missing latest schedule.\n{second_state}")

    print("[PASS] weekly cron installer regression checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1)
