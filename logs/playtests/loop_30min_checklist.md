# 30-minute Core Loop Checklist

Generated: 2026-03-19 13:12:34 KST

## Scripted pass/fail
- [x] starter loadout baseline is stable
  - [PASS] starter loadout regression validated (BUILDER.SRL=18)
- [x] economy telemetry emits build/disassemble envelopes
  - [PASS] economy telemetry regression validated
- [x] build preview/confirm gate preserves explicit consumption
  - [PASS] build preview/confirm regression validated
- [x] BUILDER.SRL affordance copy stays explicit
  - [PASS] BUILDER.SRL affordance copy regression validated
- [x] SRL cost curve suppresses low-tier spam
  - [PASS] srl cost curve regression validated (low=7 high=5)
- [x] disassembly caps remain size-tier fair
  - [PASS] disassembly cap regression validated (tiny=1/1 medium=2/1 large=3/4)
- [x] anti-exploit loop detection flags suspicious windows
  - [PASS] anti-exploit report regression validated
- [x] map_01~04 progression + portal wiring remains valid
  - [PASS] map_01~04 progression regression validated
  - artifact: /home/namyunwoo/.openclaw/workspace/dotpio/logs/playtests/map_01_04_progression_checklist.md

## Session momentum checklist (manual quick pass)
- [ ] In one run, complete at least one fight -> loot -> disassemble -> build chain.
- [ ] Confirm BUILDER.SRL drops/replenishes in expected range without flat-profit farming.
- [ ] Confirm map progression map_01 -> map_0X transitions do not break combat/loot flow.

Result: PASS
