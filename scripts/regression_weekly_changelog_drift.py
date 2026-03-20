#!/usr/bin/env python3
"""Regression checks for weekly changelog drift detector."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly_changelog_drift_check.py"


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def run_output(cmd: list[str], cwd: Path) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True)


def make_commit(repo: Path, message: str) -> None:
    run(["git", "add", "-A"], repo)
    run(["git", "commit", "-m", message], repo)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="weekly-changelog-drift-reg-") as td:
        repo = Path(td)
        run(["git", "init"], repo)
        run(["git", "config", "user.email", "reg@example.com"], repo)
        run(["git", "config", "user.name", "Regression Bot"], repo)

        (repo / "src").mkdir(parents=True, exist_ok=True)
        (repo / "logs" / "teams").mkdir(parents=True, exist_ok=True)

        (repo / "src" / "game.lua").write_text("return {}\n", encoding="utf-8")
        make_commit(repo, "feat: code only change")

        out_json = repo / "out.json"
        out_md = repo / "out.md"
        run_output([
            "python3",
            str(SCRIPT),
            "--since-days",
            "3650",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
        ], repo)
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["status"] == "warn", payload
        assert payload["missingEvidenceCommits"] >= 1, payload

        (repo / "src" / "game.lua").write_text("return {ok=true}\n", encoding="utf-8")
        (repo / "logs" / "teams" / "qa.md").write_text("- log update\n", encoding="utf-8")
        make_commit(repo, "chore: code + evidence update")

        run_output([
            "python3",
            str(SCRIPT),
            "--since-days",
            "1",
            "--max-commits",
            "1",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
        ], repo)
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["status"] == "ok", payload
        assert payload["missingEvidenceCommits"] == 0, payload

    print("[PASS] weekly changelog drift regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
