# ACTION_ITEMS (Execution Backlog)

Last updated: 2026-03-19
Tracking rule:
- [ ] todo
- [~] in progress
- [x] done

## M0 - Immediate Stabilization
- [x] Implement dropped-item pickup (`G`) from player tile
- [x] Pickup fail message on inventory full
- [x] Remove/flag collected world item after pickup
- [x] Add `G:Pickup` to in-game help/UI hints
- [x] Add regression scenario: drop -> pickup -> count validation
- [x] Add inventory build-test starter loadout tuning pass

## M1 - Core Loop Lock
- [x] Add economy telemetry logging for build/disassemble (input/output/SRL)
- [x] Add stack split (partial item quantity split) interaction in inventory
- [x] Add build preview/confirm UX (consumed materials + SRL cost before execute)
- [x] Make BUILDER.SRL usage affordance explicit in action menu and F9 flow
- [x] Add anti-exploit report (loop profit detection over N actions)
- [x] Tune SRL cost curve for low-tier spam suppression
- [x] Tune salvage size/stack caps for fairness
- [x] Validate map_01~04 progression with portal validator + playtest checklist
- [x] Add one scripted 30-minute loop checklist and pass it

## M2 - Content Sprint
- [x] Design and implement map_05 layout + portal links
- [x] Design and implement map_06 layout + portal links
- [x] Add at least 3 new enemy behavior variants
- [x] Expand AI build output category diversity constraints
- [x] Add reward table pass for lootbox contents by map tier

## M3 - Meta Progression
- [x] Add run mission prototype (3 objectives)
- [x] Add unlock flag framework for new build options
- [x] Add fail-forward reward (currency/material carryover)
- [x] Add summary screen for run result + unlock progress

## M4 - UX/Accessibility
- [x] Finalize DOS terminology consistency (Menu/Action/Drop/Disasm/Build)
- [x] Add always-visible lock reason for all disabled actions
- [x] Add compact onboarding hint flow for first 5 minutes
- [x] Add keyboard-only usability pass checklist

## M5 - RC/Launch
- [x] Create RC checklist document
- [x] Execute full regression (combat/inventory/build/disasm/portal)
- [x] Fix all critical blockers
- [x] Capture launch screenshots + changelog
- [x] Tag release candidate

## M5 - Post-RC Sustain
- [x] Weekly SRL telemetry snapshot + rebalance decision log
- [x] Add week-over-week delta signals to SRL telemetry snapshot output
- [x] Wire weekly snapshot delta regression into RC/sustain checklist command matrix
- [x] Add one-command weekly sustain runner (snapshot + anti-exploit + regression)
- [x] Add weekly scheduler wiring helper for sustain runner (cron install script + usage)
- [x] Add regression coverage for weekly scheduler installer CLI validation/dry-run evidence
- [x] Sync RC checklist sign-off status with actual tagged RC evidence
- [x] Add safe apply-mode test hook for weekly cron installer (mockable crontab binary + regression)
- [x] Add optional weekly cron log path override for multi-instance deployments
- [x] Add weekly sustain cron log rotation guard (size-based pre-run rotate helper + installer wiring)
- [x] Add rotated sustain-log retention policy (keep-latest-N pruning + regression)
- [x] Add optional rotated sustain-log max-age pruning window (days-based) for long-lived nodes
- [x] Add weekly sustain cron policy audit command (managed entry introspection + regression)

---

## Weekly Cadence
- Daily: ship at least 1 meaningful commit
- Daily: post progress report (task, commit, verification, next)
- Weekly: rebalance SRL economy based on telemetry snapshot
