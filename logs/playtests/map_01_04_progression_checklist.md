# map_01~04 Progression Playtest Checklist

Generated: 2026-03-20 00:29:10 KST

## Scripted checks
- [x] map_01~map_04 files exist
  - detail: Expected map_01.lua..map_04.lua
- [x] each map has outbound portal within map_01~04
  - detail: {'01': {'04', '03', '02'}, '02': {'01', '03'}, '03': {'04', '01', '02'}, '04': {'01', '03'}}
- [x] progression path from map_01 reaches map_02~04
  - detail: reachable=['01', '02', '03', '04']
- [x] all maps have return path back toward map_01
  - detail: {'01': {'04', '03', '02'}, '02': {'01', '03'}, '03': {'04', '01', '02'}, '04': {'01', '03'}}
- [x] portal validator passes
  - detail: Maps scanned: 7
Portals scanned: 20
OK: all portal targets resolve

## Route snapshot
- map_01 -> 02, 03, 04
- map_02 -> 01, 03
- map_03 -> 01, 02, 04
- map_04 -> 01, 03

## Manual playtest checklist (quick pass)
- [ ] Start on map_01 and use portals to visit map_02, map_03, map_04 in one run
- [ ] From each visited map, confirm at least one portal can return toward map_01
- [ ] Confirm no spawn-on-portal softlock after transition
- [ ] Confirm combat + loot loop remains playable after each transition
