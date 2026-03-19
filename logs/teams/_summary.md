# Team Logs Summary

Last updated: 2026-03-19 (KST)

## Purpose
Compact decision memory for AI context efficiency.

## Loading policy
- Default load:
  1) `_summary.md`
  2) only recent tail from each team log (last 20~50 lines)
- Expanded load: pull older ranges only when a task explicitly needs history.

## Current key decisions
- Core fun: AI-generated disassemble/build loop with DOS-style inventory UX.
- Build economy: SRL is enforced as sink; repeated low-tier loops are penalized.
- Build requirement scales with folder/component quality and loop-risk signals.
- Disassemble is constrained by size-tier costs and salvage caps.
- map_04 and portal validation flow are integrated with validator checks.
- Dropped world items can now be picked up via `G` on player tile; pickup enforces inventory capacity and consumes map entity on success.
- Pickup affordance is now surfaced in both realtime HUD controls and inventory help dialog (`G:Pickup`).
- Drop->pickup regression is now scripted in `scripts/regression_drop_pickup.lua` to validate item count restoration + world item cleanup.
- Starter build-test loadout is now folder-seeded (`SCROLLS`/`POTIONS`/`WEAPONS`) with `BUILDER.SRL` baseline 18 and mixed-tier materials for stable smoke loops.
- Starter loadout sanity is scripted in `scripts/regression_starter_loadout.lua` (Player.init baseline check).
- Economy telemetry baseline now logs build/disassemble lock/fail/success events into `logs/economy_telemetry.ndjson` with input/output metadata and SRL envelope fields.
- Telemetry schema regression is scripted in `scripts/regression_economy_telemetry.lua`.
- Inventory stacks now support split interaction (`S`) via action menu/quick key with quantity dialog and guardrails.
- Stack split regression is scripted in `scripts/regression_split_stack.lua`.
- F9 build flow now requires preview/confirm before execution, showing planned component usage + SRL have/need to keep build consumption explicit.
- Build preview confirmation gate is covered by `scripts/regression_build_preview_confirm.lua`.
- BUILDER.SRL affordance copy is now explicit across action menu, lock/status messages, and F9 preview/help text (no generic SRL-only wording).
- BUILDER.SRL copy consistency is regression-covered in `scripts/regression_builder_srl_affordance.lua`.
- Anti-exploit monitoring now has a sliding-window analyzer (`src/economy_anti_exploit.lua`) and report generator (`scripts/economy_anti_exploit_report.lua`) that flags net-positive/flat-profit loops over N actions.
- Build SRL cost curve now applies stronger low-tier + salvage-ratio surcharges so cheap churn recipes stay expensive relative to premium recipes.
- SRL curve guardrail is covered by `scripts/regression_srl_cost_curve.lua` (expects low-tier spam fixture >=6 BUILDER.SRL and not cheaper than premium fixture).
- Disassembly salvage caps are now size-tiered for fairness (stack cap 1/2/3 and budget scale 35%/45%/55% with source-size clamp), regression-covered in `scripts/regression_disassembly_caps.lua`.
- map_01~04 progression validation is now scripted via `scripts/regression_map_progression.py`, which captures reachability/return-path checks + `validate_portals.py` output into `logs/playtests/map_01_04_progression_checklist.md`.
- M1 30-minute momentum gate now has a single scripted orchestrator `scripts/regression_30min_loop_checklist.py` that executes core-loop regressions and emits `logs/playtests/loop_30min_checklist.md` with PASS/FAIL summary.
- M2 map expansion started with new `maps/map_05.lua`; map_04 now exposes portal `05` (47,24) and map_05 provides reciprocal return portal `04` (1,13), validated by portal validator.
- M2 expansion now includes `maps/map_06.lua`; map_05 exposes portal `06` (47,24) and map_06 provides reciprocal return portal `05` (1,13), validated by portal validator.
- Enemy roster now includes behavior variants (`skirmisher`, `bruiser`, `sentinel`) with profile-driven move/aggro/flee/attack modifiers and weighted spawn mix for encounter diversity.
- Build synthesis now enforces rolling category diversity (window 6 / cap 3) and shifts saturated AI targets toward underused synergy categories.
- Diversity constraint behavior is regression-covered in `scripts/regression_build_category_diversity.lua`.
- Lootbox rewards are now map-tiered (01~02 consumable-heavy, 03~04 mixed gear, 05~06 gear/accessory weighted) via weighted category profiles in `src/entities.lua`.
- Tiered loot distribution is regression-covered in `scripts/regression_lootbox_rewards_by_tier.lua`.
- M3 run mission prototype now tracks three objective lanes (`kills`, `pickup`, `build`) in runtime state and surfaces checklist progress in HUD.
- Mission objective flow is regression-covered in `scripts/regression_run_missions.lua`.
- New unlock flag framework (`src/unlocks.lua`) now gates advanced build targets (`ring`, `wand`, `gem`) behind mission completion (`advanced_build_categories`) and surfaces unlock state in HUD/status copy.
- Unlock gating/regression is covered in `scripts/regression_unlock_flags.lua`.
- Fail-forward progression now computes capped carryover rewards from failed run state (BUILDER.SRL/coin/gem), reapplies them on next run reset, and is regression-covered in `scripts/regression_fail_forward_rewards.lua`.
- Run reset now opens a summary overlay with pre-reset mission snapshot, advanced schematic unlock status, and applied carryover details; regression-covered in `scripts/regression_run_summary.lua`.
- Progress/report protocol: commit + verification + next task on each run.
- DOS inventory terminology is now normalized around canonical labels (`Action Menu`, `Disasm`, `Drop`, `Build`), and build result status explicitly lists consumed materials (`USED: ...`).
- Disabled Action Menu entries now show inline lock reasons (`[LOCK: ...]`) for USE/EQUIP/DISASM/SPLIT constraints, with regression coverage in `scripts/regression_action_menu_lock_reasons.lua`.
- Added compact first-5-minute onboarding hint strip on HUD, progressing by early interactions (move/search/pickup/inventory/build) and expiring at 300s; covered by `scripts/regression_onboarding_hints.lua`.
- Keyboard-only usability pass now has scripted coverage (`scripts/regression_keyboard_shortcuts.lua`) plus generated checklist artifact (`logs/playtests/keyboard_only_usability_checklist.md`) via `scripts/regression_keyboard_usability_checklist.py`.
- M5 RC checklist artifact is now defined at `logs/playtests/rc_checklist.md`, mapping each release gate area to executable regression commands, evidence paths, blocker triage, and cross-team sign-off rows.
- M5 full regression matrix has been executed end-to-end (combat/inventory/build/disasm/portal); all scripted checks passed, screenshots regenerated, and blocker triage currently reports 0 critical/high blockers.
- M5 blocker-closure audit rerun (30-min loop + anti-exploit + portal integrity) also passed, confirming 0 critical/high blockers remain before launch packaging.
- Launch packaging now includes refreshed screenshot artifacts (`screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`) and a root `CHANGELOG.md` (`0.5.0-rc.1`) for RC notes.
- Release candidate tag `0.5.0-rc.1` is now published on `feature/ai-disassemble-builder`, closing the final M5 unchecked item.
- Post-RC sustain now includes `scripts/economy_weekly_snapshot.py`, generating `logs/economy_weekly_snapshot.{md,json}` with a weekly SRL rebalance decision (`NO_CURVE_CHANGE`/`REBALANCE_REQUIRED`) gated by anti-exploit suspicious-window count.
- Weekly SRL snapshots now include delta signals vs previous snapshot (telemetry event count + total SRL spend), and schema stability is guarded by `scripts/regression_weekly_snapshot.py` (baseline null deltas + compare-mode zero/nonzero deltas).
- RC checklist command matrix now includes a dedicated Post-RC sustain guardrail row for `python3 scripts/regression_weekly_snapshot.py` so weekly telemetry reporting always verifies delta-schema compatibility.
- Weekly sustain operations now have a one-command runner (`bash scripts/run_weekly_sustain.sh`) that refreshes anti-exploit reports, regenerates weekly snapshot artifacts, and executes delta-schema regression in sequence.
- Scheduler handoff now includes `scripts/install_weekly_sustain_cron.sh` (dry-run/apply), with managed marker `DOTPIO_WEEKLY_SUSTAIN` and default weekly cadence Monday 09:00 KST.
- Weekly scheduler installer behavior is now regression-covered by `scripts/regression_weekly_cron_installer.py` (dry-run evidence, CLI override reflection, invalid arg rejection).
