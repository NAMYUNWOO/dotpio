#!/usr/bin/env python3
"""Validate generated map portal wiring.

Checks:
1) Every portal targetMap points to an existing map_XX.lua file.
2) Every portal targetPortal exists in the target map.
3) Optional reciprocal check (warn-only): target portal returns to source map.
4) Same-name portals inside one map must resolve to one consistent target.
5) Every map must have at least one inbound + outbound portal (warn-only).
"""

from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


PORTAL_RE = re.compile(
    r'\{\s*name="(?P<name>[^"]+)",.*?targetMap="(?P<target_map>[^"]+)",\s*targetPortal="(?P<target_portal>[^"]+)"\s*\}'
)
MAP_RE = re.compile(r"map_(\d+)\.lua$")


@dataclass
class Portal:
    map_id: str
    name: str
    target_map: str
    target_portal: str


def load_portals(maps_dir: str) -> Dict[str, List[Portal]]:
    by_map: Dict[str, List[Portal]] = {}
    for path in sorted(glob.glob(os.path.join(maps_dir, "map_*.lua"))):
        m = MAP_RE.search(path)
        if not m:
            continue
        map_id = m.group(1)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        portals: List[Portal] = []
        for hit in PORTAL_RE.finditer(text):
            portals.append(
                Portal(
                    map_id=map_id,
                    name=hit.group("name"),
                    target_map=hit.group("target_map"),
                    target_portal=hit.group("target_portal"),
                )
            )
        by_map[map_id] = portals
    return by_map


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    maps_dir = os.path.join(root, "maps")
    by_map = load_portals(maps_dir)

    errors: List[str] = []
    warnings: List[str] = []

    available_maps = set(by_map.keys())
    names_by_map = {mid: {p.name for p in portals} for mid, portals in by_map.items()}
    inbound_counts = {mid: 0 for mid in by_map}

    for src_map, portals in by_map.items():
        grouped_targets: Dict[str, Set[Tuple[str, str]]] = {}

        for p in portals:
            grouped_targets.setdefault(p.name, set()).add((p.target_map, p.target_portal))

            if p.target_map not in available_maps:
                errors.append(
                    f"map_{src_map}:{p.name} -> missing target map_{p.target_map}"
                )
                continue
            if p.target_portal not in names_by_map[p.target_map]:
                errors.append(
                    f"map_{src_map}:{p.name} -> target portal {p.target_portal} missing in map_{p.target_map}"
                )
                continue

            inbound_counts[p.target_map] += 1

            reciprocal = any(
                tp.name == p.target_portal and tp.target_map == src_map
                for tp in by_map[p.target_map]
            )
            if not reciprocal:
                warnings.append(
                    f"map_{src_map}:{p.name} -> map_{p.target_map}:{p.target_portal} is one-way"
                )

        for portal_name, targets in grouped_targets.items():
            if len(targets) > 1:
                serialized = ", ".join(
                    sorted(f"map_{tm}:{tp}" for tm, tp in targets)
                )
                errors.append(
                    f"map_{src_map}:{portal_name} has inconsistent multi-tile targets: {serialized}"
                )

    for map_id, portals in by_map.items():
        if not portals:
            warnings.append(f"map_{map_id} has no outbound portals")
        if inbound_counts[map_id] == 0:
            warnings.append(f"map_{map_id} has no inbound portals")

    print(f"Maps scanned: {len(by_map)}")
    print(f"Portals scanned: {sum(len(v) for v in by_map.values())}")

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OK: all portal targets resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
