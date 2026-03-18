#!/usr/bin/env python3
"""Regression: validate map_01~04 portal progression + generate playtest checklist artifact.
Run: python3 scripts/regression_map_progression.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parent.parent
MAPS_DIR = ROOT / "maps"
ARTIFACT = ROOT / "logs" / "playtests" / "map_01_04_progression_checklist.md"
MAP_IDS = ["01", "02", "03", "04"]
KST = timezone(timedelta(hours=9))

PORTAL_RE = re.compile(
    r'\{\s*name="(?P<name>[^"]+)",\s*x=(?P<x>\d+),\s*y=(?P<y>\d+),\s*tileX=(?P<tile_x>\d+),\s*tileY=(?P<tile_y>\d+),\s*targetMap="(?P<target_map>[^"]+)",\s*targetPortal="(?P<target_portal>[^"]+)"\s*\}'
)


@dataclass
class Portal:
    name: str
    target_map: str
    target_portal: str


def load_portals(map_id: str) -> List[Portal]:
    text = (MAPS_DIR / f"map_{map_id}.lua").read_text(encoding="utf-8")
    return [
        Portal(
            name=m.group("name"),
            target_map=m.group("target_map"),
            target_portal=m.group("target_portal"),
        )
        for m in PORTAL_RE.finditer(text)
    ]


def bfs(start: str, edges: Dict[str, Set[str]]) -> Set[str]:
    seen: Set[str] = {start}
    q: deque[str] = deque([start])
    while q:
        cur = q.popleft()
        for nxt in edges.get(cur, set()):
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen


def main() -> int:
    checks: List[tuple[str, bool, str]] = []

    existing_maps = all((MAPS_DIR / f"map_{mid}.lua").exists() for mid in MAP_IDS)
    checks.append(("map_01~map_04 files exist", existing_maps, "Expected map_01.lua..map_04.lua"))

    portals_by_map: Dict[str, List[Portal]] = {}
    for mid in MAP_IDS:
        portals_by_map[mid] = load_portals(mid)

    edges: Dict[str, Set[str]] = {mid: set() for mid in MAP_IDS}
    for mid, portals in portals_by_map.items():
        for p in portals:
            if p.target_map in edges:
                edges[mid].add(p.target_map)

    outbound_ok = all(len(edges[mid]) > 0 for mid in MAP_IDS)
    checks.append(("each map has outbound portal within map_01~04", outbound_ok, str(edges)))

    reach_from_01 = bfs("01", edges)
    can_reach_all = all(mid in reach_from_01 for mid in MAP_IDS)
    checks.append(("progression path from map_01 reaches map_02~04", can_reach_all, f"reachable={sorted(reach_from_01)}"))

    reverse_edges: Dict[str, Set[str]] = {mid: set() for mid in MAP_IDS}
    for src, targets in edges.items():
        for tgt in targets:
            reverse_edges[tgt].add(src)
    can_return_to_01 = all(mid in bfs("01", reverse_edges) for mid in MAP_IDS)
    checks.append(("all maps have return path back toward map_01", can_return_to_01, str(reverse_edges)))

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_portals.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    portal_validator_ok = proc.returncode == 0
    checks.append(("portal validator passes", portal_validator_ok, (proc.stdout + proc.stderr).strip()))

    kst_label = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")

    lines = [
        "# map_01~04 Progression Playtest Checklist",
        "",
        f"Generated: {kst_label}",
        "",
        "## Scripted checks",
    ]

    for label, ok, detail in checks:
        lines.append(f"- [{'x' if ok else ' '}] {label}")
        lines.append(f"  - detail: {detail}")

    lines.extend([
        "",
        "## Route snapshot",
        f"- map_01 -> {', '.join(sorted(edges['01']))}",
        f"- map_02 -> {', '.join(sorted(edges['02']))}",
        f"- map_03 -> {', '.join(sorted(edges['03']))}",
        f"- map_04 -> {', '.join(sorted(edges['04']))}",
        "",
        "## Manual playtest checklist (quick pass)",
        "- [ ] Start on map_01 and use portals to visit map_02, map_03, map_04 in one run",
        "- [ ] From each visited map, confirm at least one portal can return toward map_01",
        "- [ ] Confirm no spawn-on-portal softlock after transition",
        "- [ ] Confirm combat + loot loop remains playable after each transition",
    ])

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    failed = [label for label, ok, _ in checks if not ok]
    if failed:
        print(f"[FAIL] map progression regression failed: {', '.join(failed)}")
        print(f"artifact: {ARTIFACT}")
        return 1

    print("[PASS] map_01~04 progression regression validated")
    print(f"artifact: {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
