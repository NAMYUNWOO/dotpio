#!/usr/bin/env python3
"""Regression checks for weekly_portal_prompt_readability_drift.py."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly_portal_prompt_readability_drift.py"


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def run_output(cmd: list[str], cwd: Path) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True)


def commit_all(repo: Path, message: str) -> None:
    run(["git", "add", "-A"], repo)
    run(["git", "commit", "-m", message], repo)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="portal-prompt-drift-reg-") as td:
        repo = Path(td)
        run(["git", "init"], repo)
        run(["git", "config", "user.email", "reg@example.com"], repo)
        run(["git", "config", "user.name", "Regression Bot"], repo)

        (repo / "src").mkdir(parents=True, exist_ok=True)
        (repo / "src" / "portal.lua").write_text(
            'return "PORTAL READY -> ENTER:JUMP  NEXT ROUTE:SAFE  COACH:LOW PRESSURE  PRESSURE:1"\n',
            encoding="utf-8",
        )
        commit_all(repo, "feat: add detailed portal prompt")

        (repo / "src" / "portal.lua").write_text(
            'return "PORTAL READY -> ENTER:JUMP  NEXT:SAFE  COACH:LOW  P:1  ALT:RISK  ADEL:-1  AP:LOW"\n',
            encoding="utf-8",
        )
        commit_all(repo, "feat: compact portal prompt")

        out_json = repo / "out.json"
        out_md = repo / "out.md"

        run_output(
            [
                "python3",
                str(SCRIPT),
                "--since-days",
                "3650",
                "--max-commits",
                "20",
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ],
            repo,
        )

        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["checkedCommits"] >= 2, payload
        assert payload["portalPromptCommits"] >= 2, payload
        assert payload["totals"]["added"]["compact"] > 0, payload
        assert payload["totals"]["added"]["detailed"] > 0, payload
        assert payload["modeTrend"] in {"COMPACT", "DETAILED", "BALANCED"}, payload
        assert payload["pressureBand"] in {"LOW", "MID", "HIGH"}, payload
        assert payload["driftRisk"] in {"LOW", "MID", "HIGH"}, payload
        assert set(payload["driftRiskSignals"].keys()) == {"score", "imbalance", "pressureChurn"}, payload
        assert payload["laneFocus"] in {"PORTAL", "ALT", "PRESSURE", "MIXED"}, payload
        assert set(payload["laneFocusScores"].keys()) == {"portal", "alt", "pressure"}, payload
        assert payload["routeAction"] in {"PORTAL_AUDIT", "ALT_TUNE", "PRESSURE_REBASE", "BALANCE_PASS", "WATCH"}, payload
        assert isinstance(payload["routeActionReason"], str) and payload["routeActionReason"], payload
        assert set(payload["pressureEdits"].keys()) == {"added", "removed", "net"}, payload
        assert "tokenTotals" in payload, payload
        assert "stickyTokens" in payload, payload
        assert set(payload["stickyTokens"].keys()) == {"count", "tokens"}, payload
        assert payload["stickyTokens"]["count"] == len(payload["stickyTokens"]["tokens"]), payload
        assert isinstance(payload.get("topTokenMovers"), list), payload
        if payload["topTokenMovers"]:
            assert {"token", "net", "added", "removed"}.issubset(payload["topTokenMovers"][0].keys()), payload
        md_text = out_md.read_text(encoding="utf-8")
        assert "Token Totals" in md_text
        assert "Top Token Movers" in md_text
        assert "MODE TREND" in md_text
        assert "PRESSURE BAND" in md_text
        assert "DRIFT RISK" in md_text
        assert "FOCUS" in md_text
        assert "ROUTE ACTION" in md_text
        assert "STICKY TOKENS" in md_text
        assert "Sticky Tokens" in md_text

    print("[PASS] weekly portal prompt readability drift regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
