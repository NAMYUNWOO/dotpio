#!/usr/bin/env python3
"""Regression checks for weekly sustain log rotation retention pruning."""

from __future__ import annotations

import os
import pathlib
import subprocess
import tempfile
import time

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
ROTATE_HELPER = REPO_ROOT / "scripts" / "rotate_log_if_needed.sh"


def run(
    log_path: pathlib.Path,
    max_size_mb: int,
    retain: int,
    max_age_days: int = 0,
    expect_tokens: list[str] | None = None,
) -> str:
    result = subprocess.run(
        [
            "bash",
            str(ROTATE_HELPER),
            str(log_path),
            str(max_size_mb),
            str(retain),
            str(max_age_days),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = f"{result.stdout}\n{result.stderr}"
    if result.returncode != 0:
        raise AssertionError(f"rotate helper failed ({result.returncode})\n{output}")
    for token in expect_tokens or []:
        if token not in output:
            raise AssertionError(f"missing token `{token}`\n{output}")
    return output


def write_payload(path: pathlib.Path, size_bytes: int) -> None:
    path.write_bytes(b"x" * size_bytes)


def rotated_files(log_path: pathlib.Path) -> list[pathlib.Path]:
    return sorted(log_path.parent.glob(f"{log_path.name}.*"), key=lambda p: p.stat().st_mtime, reverse=True)


def main() -> int:
    if not ROTATE_HELPER.exists():
        raise FileNotFoundError(f"rotate helper missing: {ROTATE_HELPER}")

    with tempfile.TemporaryDirectory(prefix="dotpio-rotate-reg-") as temp_dir:
        log_path = pathlib.Path(temp_dir) / "weekly.log"

        # Below threshold should not rotate.
        write_payload(log_path, 128)
        run(log_path, max_size_mb=1, retain=2)
        if rotated_files(log_path):
            raise AssertionError("unexpected rotation for below-threshold file")

        # Trigger repeated rotations; retain only latest 2 artifacts.
        for idx in range(4):
            write_payload(log_path, 1024 * 1024 + 64)
            out = run(log_path, max_size_mb=1, retain=2, expect_tokens=["[log-rotate] rotated"])
            if idx >= 2 and "pruned" not in out:
                raise AssertionError(f"expected prune message on iteration {idx}\n{out}")
            time.sleep(1.1)

        files = rotated_files(log_path)
        if len(files) != 2:
            raise AssertionError(f"expected 2 rotated files after pruning, got {len(files)}: {files}")

        # Age-based pruning should remove stale rotated files even when retain cap is high.
        stale = files[-1]
        stale_mtime = time.time() - (2 * 24 * 60 * 60)
        os.utime(stale, (stale_mtime, stale_mtime))
        out = run(log_path, max_size_mb=99, retain=10, max_age_days=1)
        if "pruned 1 rotated logs by age" not in out:
            raise AssertionError(f"expected age-based prune message\n{out}")
        if stale.exists():
            raise AssertionError("expected stale rotated file to be pruned by age")

    print("[PASS] rotate log retention regression checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1)
