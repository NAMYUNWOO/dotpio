# ACTION_ITEMS (Execution Backlog)

Last updated: 2026-03-18
Tracking rule:
- [ ] todo
- [~] in progress
- [x] done

## M0 - Immediate Stabilization
- [x] Implement dropped-item pickup (`G`) from player tile
- [x] Pickup fail message on inventory full
- [x] Remove/flag collected world item after pickup
- [ ] Add `G:Pickup` to in-game help/UI hints
- [ ] Add regression scenario: drop -> pickup -> count validation
- [ ] Add inventory build-test starter loadout tuning pass

## M1 - Core Loop Lock
- [ ] Add economy telemetry logging for build/disassemble (input/output/SRL)
- [ ] Add anti-exploit report (loop profit detection over N actions)
- [ ] Tune SRL cost curve for low-tier spam suppression
- [ ] Tune salvage size/stack caps for fairness
- [ ] Validate map_01~04 progression with portal validator + playtest checklist
- [ ] Add one scripted 30-minute loop checklist and pass it

## M2 - Content Sprint
- [ ] Design and implement map_05 layout + portal links
- [ ] Design and implement map_06 layout + portal links
- [ ] Add at least 3 new enemy behavior variants
- [ ] Expand AI build output category diversity constraints
- [ ] Add reward table pass for lootbox contents by map tier

## M3 - Meta Progression
- [ ] Add run mission prototype (3 objectives)
- [ ] Add unlock flag framework for new build options
- [ ] Add fail-forward reward (currency/material carryover)
- [ ] Add summary screen for run result + unlock progress

## M4 - UX/Accessibility
- [ ] Finalize DOS terminology consistency (Menu/Action/Drop/Disasm/Build)
- [ ] Add always-visible lock reason for all disabled actions
- [ ] Add compact onboarding hint flow for first 5 minutes
- [ ] Add keyboard-only usability pass checklist

## M5 - RC/Launch
- [ ] Create RC checklist document
- [ ] Execute full regression (combat/inventory/build/disasm/portal)
- [ ] Fix all critical blockers
- [ ] Capture launch screenshots + changelog
- [ ] Tag release candidate

---

## Weekly Cadence
- Daily: ship at least 1 meaningful commit
- Daily: post progress report (task, commit, verification, next)
- Weekly: rebalance SRL economy based on telemetry snapshot
