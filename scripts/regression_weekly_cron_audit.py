#!/usr/bin/env python3
"""Regression checks for weekly sustain cron policy audit helper."""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "scripts" / "audit_weekly_sustain_cron.sh"
MARKER = "# DOTPIO_WEEKLY_SUSTAIN"


def run(cmd: list[str], expect_ok: bool, must_contain: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    output = f"{result.stdout}\n{result.stderr}"
    if expect_ok and result.returncode != 0:
        raise AssertionError(f"Expected success but failed ({result.returncode}): {' '.join(cmd)}\n{output}")
    if not expect_ok and result.returncode == 0:
        raise AssertionError(f"Expected failure but succeeded: {' '.join(cmd)}\n{output}")
    for token in must_contain:
        if token not in output:
            raise AssertionError(f"Missing token `{token}` in output:\n{output}")
    return output


def main() -> int:
    if not AUDIT.exists():
        raise FileNotFoundError(f"Audit script missing: {AUDIT}")

    with tempfile.TemporaryDirectory(prefix="dotpio-cron-audit-") as temp_dir:
        temp_path = pathlib.Path(temp_dir)
        fake_crontab = temp_path / "fake_crontab.py"
        state_file = temp_path / "cron_state.txt"

        fake_crontab.write_text(
            """#!/usr/bin/env python3
import os
import pathlib
import sys

state_path = pathlib.Path(os.environ.get("FAKE_CRON_STATE", ""))
if not str(state_path):
    print("missing FAKE_CRON_STATE", file=sys.stderr)
    raise SystemExit(2)
state_path.parent.mkdir(parents=True, exist_ok=True)
state_path.touch(exist_ok=True)

arg = sys.argv[1] if len(sys.argv) > 1 else ""
if arg == "-l":
    sys.stdout.write(state_path.read_text(encoding="utf-8"))
    raise SystemExit(0)

print(f"unsupported args: {' '.join(sys.argv[1:])}", file=sys.stderr)
raise SystemExit(2)
""",
            encoding="utf-8",
        )
        fake_crontab.chmod(0o755)

        managed_entry = (
            "CRON_TZ=UTC 15 6 * * 2 "
            "cd /tmp/dotpio && bash scripts/rotate_log_if_needed.sh /tmp/dotpio-weekly.log 12 4 14 "
            "&& bash scripts/run_weekly_sustain.sh >> /tmp/dotpio-weekly.log 2>&1 "
            f"{MARKER}\n"
        )
        state_file.write_text(managed_entry, encoding="utf-8")

        env = os.environ.copy()
        env.update({"CRONTAB_BIN": str(fake_crontab), "FAKE_CRON_STATE": str(state_file)})

        run(
            ["bash", str(AUDIT)],
            expect_ok=True,
            must_contain=[
                "[OK] Managed weekly sustain entry found.",
                "tz=UTC",
                "minute=15",
                "hour=6",
                "dow=2",
                "log_path=/tmp/dotpio-weekly.log",
                "max_log_size_mb=12",
                "retain_rotated_logs=4",
                "max_rotated_age_days=14",
            ],
            env=env,
        )

        json_output = run(
            ["bash", str(AUDIT), "--format", "json"],
            expect_ok=True,
            must_contain=['"status": "ok"', '"tz": "UTC"'],
            env=env,
        )
        json_payload = json.loads(json_output.strip().splitlines()[0])
        if json_payload["minute"] != 15 or json_payload["retain_rotated_logs"] != 4:
            raise AssertionError(f"Unexpected json payload fields: {json_payload}")

        run(
            ["bash", str(AUDIT), "--format", "yaml"],
            expect_ok=False,
            must_contain=["[ERROR] --format must be one of: text, json"],
            env=env,
        )

        state_file.write_text("# no managed entries\n", encoding="utf-8")
        run(
            ["bash", str(AUDIT)],
            expect_ok=False,
            must_contain=["[ERROR] Managed weekly sustain entry not found"],
            env=env,
        )

    print("[PASS] weekly cron audit regression checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1)
