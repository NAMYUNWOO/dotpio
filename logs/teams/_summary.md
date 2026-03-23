# Team Logs Summary

Last updated: 2026-03-23 20:12 KST

## Purpose
Compact decision memory for AI context efficiency.

## Loading policy
- Default load:
  1) `_summary.md`
  2) only recent tail from each team log (last 20~50 lines)
- Expanded load: pull older ranges only when a task explicitly needs history.

## Current key decisions


- Closed Cycle BQ UX/World item: portal prompts now emit confidence-rail token `VIBE TRAIL CONF RAIL:STEADY|SPIKE` behind `DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF_RAIL`.
- Compact parity shipped with alias `VTCR:S|X`; calm contexts resolve to `STEADY/S`, ash contexts to `SPIKE/X`.
- Regression guardrails updated: `scripts/regression_portal_vibe_trail.lua` now validates detailed+compact rail tokens and invalid-context suppression.
- Weekly digest token catalogs/families extended for `VIBE TRAIL CONF RAIL:` and `VTCR:` coverage with schema assertions in `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Remaining top unchecked item: `VIBE TRAIL WHY CONF WHY:<short>` (Design/AI Content, flagged).
- Game Director Cycle BO executed after ACTION_ITEMS + TASKS + POST_RC remained fully checked.
- Cycle BO generated 3 ideas (low/mid/high) and selected low-risk UX/world vertical slice: portal vibe-trail confidence token.
- Shipped `VIBE TRAIL CONF:LOW|MID|HIGH` + compact alias `VTC:<L|M|H>` behind `DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF`.
- Mapping is deterministic (`CALM -> MID`, `ASH -> HIGH`) and emits only when valid vibe-trail context exists.
- Regression guardrail updated: `scripts/regression_portal_vibe_trail.lua` now validates detailed/compact confidence tokens and invalid-context suppression.
- Follow-up backlog injected (Cycle BO): weekly digest token-family coverage for `VIBE TRAIL CONF` and flagged `VIBE TRAIL WHY:<short>` rationale token.

- Closed Cycle BJ final unchecked item: portal prompts now emit `ALT WHY GLYPH:<sigil>` behind `DOTPIO_EXPERIMENT_ALT_WHY_GLYPH` in both detailed and compact modes.
- ACTION_ITEMS/TASKS/POST_RC actionable queues were fully checked after BJ closure, so Game Director Cycle BK executed (3 ideas generated).
- Selected/shipped Cycle BK minimal slice: compact prompt can now emit alias token `AWG:<sigil>` behind `DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_COMPACT` while detailed mode keeps full `ALT WHY GLYPH` label.
- Added regression guardrail `scripts/regression_portal_alt_why_glyph_compact.lua`; glyph baseline + weekly digest regression remain passing.
- Cycle BK backlog injected: next queued items are `ALT WHY GLYPH Δ:+n|-n` (Systems/QA) and flagged `ALT WHY GLYPH MODE:STEADY|SPIKE` (Design/AI Content).

- Closed Cycle BG combat/vfx slice: compact portal prompts now emit flag-gated pulse flare warning `PULSE FLARE:+` (`DOTPIO_EXPERIMENT_ROUTE_PULSE_FLARE_PROMPT`) only when `PULSE MODE:X` and pulse-fit downgrades (`B|R`).
- Added QA guardrail `scripts/regression_portal_prompt_pulse_flare.lua`; pulse mode/fit regressions remain green under required flags.
- Updated backlog state: Cycle BG combat/vfx item is complete with lifecycle trace (`[~] -> [x]`); next highest-priority unchecked item is Systems/UX token-priority mode (`FIT-FIRST|MODE-FIRST`).

- Closed final unchecked Cycle BF world/design item: compact portal prompts now support flag-gated pulse-fit cue `PULSE FIT:Y|W|B|R` (`DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT`).
- Coverage check over last 10 completed items: systems/ops=5, design/world=3, combat/vfx=2 (others=0); since systems/ops exceeded 40%, this cycle was forced into underrepresented lanes and selected design/world parity slice.
- Added new QA guardrail `scripts/regression_portal_prompt_pulse_fit.lua`; existing pulse mode/link prompt regressions remain passing.
- Injected next-cycle candidates: compact pulse-flare warning (`PULSE FLARE:+`) and adaptive compact token-budget ordering (`FIT-first` vs `MODE-first`).

- Closed Cycle BF drift task: weekly digest now emits `ROUTE PULSE LINK MODE FIT Δ:+n|-n` with prior-window context (`current/prior/loaded`).
- Payload contract extended with `routePulseLinkModeFitDrift` + `routePulseLinkModeFitDriftSignals`; markdown now includes `ROUTE PULSE LINK MODE FIT Δ` row.
- Regression coverage expanded in `scripts/regression_weekly_portal_prompt_readability_drift.py` for new payload keys, markdown token presence, and prior-window drift math.
- Closed remaining unchecked compact portal parity item: `PULSE MODE:I|S|X` now ships behind `DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT` in compact transition prompts.
- Compact pulse mode mapping contract is deterministic and regression-covered: `X` (surge/high pressure), `S` (sustain/elevated), `I` (idle/low).
- Added QA guardrail `scripts/regression_portal_prompt_pulse_mode.lua`; existing compact and pulse-link prompt regressions remain passing.
- Closed Cycle BC remaining systems/qa task: weekly digest now emits `ROUTE PULSE LINK STREAK:<n>` with prior-window persistence signals.
- Since actionable backlogs were fully checked after Cycle BC closure, executed Game Director Cycle BD (3 ideas -> 1 selected vertical slice).
- Selected/shipped Cycle BD slice: weekly digest now emits `ROUTE PULSE LINK MODE:IDLE|SUSTAIN|SURGE` from link + streak + pulse-drift context.
- Injected Cycle BD follow-ups in backlog: `ROUTE PULSE LINK MODE Δ:+n|-n` and flagged compact portal parity cue `PULSE MODE:I|S|X`.
- Verification artifacts refreshed and passing: `scripts/regression_weekly_portal_prompt_readability_drift.py`, `scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`.
- Cycle BA Systems/QA slice shipped: weekly digest now emits `ACTION PACE ALT WINDOW STEP Δ:+n|-n` by comparing current step token against prior digest snapshot.
- Digest payload now persists step drift fields (`actionPaceAltWindowStepDrift`, `actionPaceAltWindowStepDriftSignals`) and markdown summary includes signed drift with score breakdown.
- Regression coverage expanded for step drift: markdown token presence + prior snapshot drift math checks (no-prior baseline, escalated delta case).
- Game Director Cycle AW executed after confirming ACTION_ITEMS + TASKS + POST_RC_BACKLOG were fully checked.
- Cycle AW ideas generated (3): low-risk digest action-pace token, mid-risk pace-drift prior-window token, high-risk flagged pace-coach rationale token.
- Selected/implemented Cycle AW vertical slice: weekly portal readability digest now emits `ACTION PACE:ACCEL|STEADY|BRAKE` from `ACTION GUARD + ACTION STABILITY + PRESSURE LAG`.
- Regression and artifact evidence: `scripts/regression_weekly_portal_prompt_readability_drift.py` PASS; `scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200` PASS.
- Cycle AW backlog injected with follow-ups: `PACE DRIFT:+n|-n` and flagged `ACTION PACE WHY:<short>`.

- Game Director Cycle AU executed after confirming ACTION_ITEMS + TASKS + POST_RC_BACKLOG remained fully checked.
- Cycle AU ideas generated (3): low-risk post-snapback recovery cue, mid-risk resilience streak token, high-risk drift alarm token under short-window conflict+snapback overlap.
- Selected/implemented Cycle AU vertical slice: portal prompt now supports flag-gated recovery cue token (`VIBE RECOVER:READY`, compact `VR:OK`) on the first re-aligned transition after snapback.
- Recovery cue lifecycle is one-shot and reversible: it arms after immediate post-sync misalignment (`VIBE SNAPBACK:ON`) and auto-clears after first confirmed recovery transition.
- Regression coverage added in `scripts/regression_portal_route_vibe_recovery.lua`; existing snapback regression remains green.
- Cycle AQ executed with forced lane rebalance after coverage check showed systems dominance over the last 10 completed items (systems=10/10, all other lanes=0).
- Shipped underrepresented-lane vertical slice: portal transition prompt now emits pressure-tied FX cue token (`FX:CALM|FLICKER|SURGE`, compact `FX:C|F|S`) to improve world-choice readability without mechanics change.
- Injected Cycle AQ follow-ups: combat/vfx pressure pulse token (`BERSERK FX:PULSE`) and flagged world-design route vignette token (`ROUTE VIGNETTE:<glyph>`).
- Closed Cycle AM final task: weekly digest now emits flag-gated `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WHY:<short>` (`DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE_WHY`) for compact operator coaching context.
- ACTION_ITEMS + TASKS + POST_RC_BACKLOG were fully checked, so Game Director review cycle ran immediately.
- Game Director Cycle AN ideas generated: low-risk `NUDGE IMPACT` band, mid-risk `NUDGE DRIFT` token, high-risk flagged dual-lane `COACH` snapshot.
- Selected Cycle AN experiment shipped as minimal vertical slice: weekly digest now emits `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE IMPACT:DEFENSIVE|CAUTIOUS|NEUTRAL` from nudge/window/fit signals.
- Injected Cycle AN follow-up backlog tasks: `NUDGE DRIFT` token and flagged dual-lane `COACH` snapshot.
- Closed Cycle AM follow-up task: weekly digest now emits `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WINDOW:ARMED|COOLING|IDLE` derived from rearm + cooloff-state context (`WATCH -> ARMED`, `OFF+ACTIVE -> COOLING`, otherwise `IDLE`).
- Closed Cycle AH follow-up task: weekly digest now emits `WHAT-IF SPLIT ESC RECOVER VETO DWELL:<n>` that tracks consecutive `ARMED` windows and resets when veto state is not armed.
- Closed the final Cycle AF unchecked item: weekly digest now emits flag-gated `WHAT-IF SPLIT ESC RECOVER VETO:ON|OFF` (`DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO`) when recovery remains `LOW` confidence under `HIGH` pressure with actionable plan context.
- Since ACTION_ITEMS + TASKS + POST_RC were fully checked, executed Game Director review cycle (low/mid/high idea generation) and shipped selected low-risk slice: `WHAT-IF SPLIT ESC RECOVER VETO CONF:LOW|MID|HIGH`.
- Injected Cycle AG follow-up backlog items: `WHAT-IF SPLIT ESC RECOVER VETO WHY:<short>` (flag-gated) and `WHAT-IF SPLIT ESC RECOVER VETO COOLOFF:<n>` (flag-gated).
- Cycle AF follow-up slice shipped: weekly digest now emits `WHAT-IF SPLIT ESC RECOVER ΔCONF:+n|-n` by comparing current vs prior digest recovery confidence (`LOW=0`, `MID=1`, `HIGH=2`) and exposing `priorLoaded` + reason signals.
- Cycle AF backlog now has one remaining unchecked item: flag-gated `WHAT-IF SPLIT ESC RECOVER VETO:ON` under HIGH pressure + LOW confidence.
- Cycle AC follow-up slice shipped: weekly digest now emits `WHAT-IF SPLIT ESC PRESSURE:LOW|MID|HIGH` with lifecycle-aware cooling decay for escalation cooldown risk context.
- `WHAT-IF SPLIT ESC PRESSURE` is guarded by `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_PRESSURE`; when disabled it defaults to `LOW` with explicit `flag-disabled` reason to preserve default contract stability.
- Remaining highest-priority unchecked item is Cycle AC recovery hint prototype: `WHAT-IF SPLIT ESC RECOVER:<lane>` (flag-gated).
- Cycle AB follow-up backlog is now closed: weekly digest ships `WHAT-IF SPLIT ESC LANES:<primary>/<secondary>` for escalation handoff readability and `WHAT-IF SPLIT ESC COOL:<n>` for flag-gated disarm cooloff pressure context.
- `WHAT-IF SPLIT ESC COOL` is guarded by `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL`; when disabled it stays `0` with explicit `flag-disabled` reason to preserve default contract stability.
- Game Director Cycle AB ideation completed (low/mid/high concepts), and the selected vertical slice shipped: weekly digest now emits `WHAT-IF SPLIT ESC CONF:LOW|MID|HIGH` tied to escalation arm state + split confidence + plan fit.
- Cycle AB backlog injected with two follow-up candidates: `WHAT-IF SPLIT ESC LANES` and flag-gated `WHAT-IF SPLIT ESC COOL`.
- Game Director Cycle AA follow-up slice delivered: weekly digest now emits flag-gated `WHAT-IF SPLIT ESCALATE:ON|OFF` when split remains divergent under `TENSE` fit (`DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESCALATE`).
- Split escalation sentinel is regression-covered in weekly digest payload + markdown assertions to keep schema/report stability.
- Game Director Cycle AA slice delivered: weekly digest now emits `WHAT-IF SPLIT POSTURE:SAFE|WATCH|HOLD` from split armed/safe/confidence signals for quick go/no-go triage.
- Cycle AA backlog injected with two follow-up experiments: `WHAT-IF SPLIT COOLOFF:<n>` and flag-gated `WHAT-IF SPLIT ESCALATE:ON`.
- Game Director Cycle Y slice delivered: weekly digest now emits `WHAT-IF PLAN WHY:<short>` (flag `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN_WHY`) to explain selected merge-path rationale in one glance.
- Weekly portal readability digest now includes `WHAT-IF FALLBACK PLAN:PRIMARY|SECONDARY|HOLD` (flag: `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN`) to merge primary/secondary fallback routing into one actionable handoff token.
- Game Director Cycle Y vertical slice shipped: `WHAT-IF PLAN FIT:SAFE|EVEN|TENSE` now rates selected merge plan against pressure band for quick go/no-go reading.
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
- Weekly cron installer now supports `CRONTAB_BIN` override so mocked apply-mode upsert behavior can be regression-tested safely without mutating host crontab; regression now asserts single-marker upsert semantics under `--apply`.
- RC checklist sign-off rows are now synchronized with actual release state: all lane sign-offs checked, release tag recorded as `0.5.0-rc.1` (`d82cab1`), and sign-off note includes auditable timestamp/hash.
- Weekly cron installer now supports configurable log sinks via `--log-path` / `SUSTAIN_CRON_LOG_PATH` (default still `logs/weekly_sustain_cron.log`), with regression coverage ensuring custom path rendering stays stable.
- Weekly sustain scheduler now includes size-based pre-run log rotation via `scripts/rotate_log_if_needed.sh`; installer exposes `--max-log-size-mb` / `SUSTAIN_CRON_MAX_LOG_SIZE_MB` and regression coverage checks rotate-command rendering + validation.
- Weekly sustain log rotation now enforces keep-latest-N retention pruning via `scripts/rotate_log_if_needed.sh <log> <max-size-mb> <retain-rotated>` to avoid rotated-log accumulation.
- Cron installer now exposes `--retain-rotated-logs` / `SUSTAIN_CRON_RETAIN_ROTATED_LOGS`, wiring retention policy directly into managed cron entries.
- Retention behavior is regression-covered by `scripts/regression_rotate_log_retention.py` (repeated over-threshold rotations + prune assertions).
- Weekly sustain log rotation now also supports optional age-based pruning (`max-age-days`) via rotate helper + cron installer (`--max-rotated-age-days` / `SUSTAIN_CRON_MAX_ROTATED_AGE_DAYS`), with regression coverage for stale-file deletion and CLI token rendering.
- Added `scripts/audit_weekly_sustain_cron.sh` to introspect the managed `DOTPIO_WEEKLY_SUSTAIN` cron entry and print parsed schedule + rotation policy fields; regression-covered by `scripts/regression_weekly_cron_audit.py` including missing-entry diagnostics.
- Weekly sustain cron audit helper now supports machine-readable output via `--format json` (default remains text), and regression coverage now validates JSON payload fields plus invalid-format rejection.
- Folder rows now use Enter -> Action Menu (`OPEN`/`BUILD`) as the primary build flow, with `B` quick action opening the same build preview/confirm gate; F9 remains as shortcut.
- `BUILDER.SRL` can no longer be directly consumed via `USE`; item Action Menu now shows a locked `USE` row with explicit build-only guidance (`B` or `Enter->BUILD`), and quick-use attempts emit matching status text.
- Regression coverage in `scripts/regression_action_menu_lock_reasons.lua` now asserts `BUILDER.SRL`-specific `USE` lock + guidance copy.
- Build preview dialog now includes an explicit `Expected category` line (derived from constrained component-category mix via `AiDescribe.debugConstrainBuildCategory`) so players can see projected output class before confirming material/SRL spend.
- Added `scripts/regression_build_preview_clarity.lua` to enforce preview-plan expected-category metadata presence while existing preview confirm/action-menu regressions stay green.
- Added `map_07` as a post-RC P1 world expansion with additional mid-lane collision barricades to create a tighter tactical choke pattern compared to map_06.
- Portal graph now includes a bidirectional `map_06` <-> `map_07` pair (`map_06` portal `07` at 47,13 to `map_07` portal `06`, reciprocal return path on `map_07`).
- Enemy roster now includes two P1 synergy archetypes: `warcaller` (nearby ally alert propagation on player sight) and `hunter` (proximity buff when a living warcaller is nearby), with regression coverage extended for synergy activation and ally-alert behavior.
- Run missions now support rotating 3-objective packs instead of a fixed prototype list, preserving HUD readability while varying run goals across resets.
- Mission variety pack now includes +5 new objective variants (`kills_5`, `pickup_4`, `build_2`, `search_2`, `inventory_3`) with shared event-key progress tracking.
- Gameplay hooks now increment mission progress on crate search completion and inventory-open actions, enabling the new mission variants without extra controls.
- Mission variety behavior is regression-covered by `scripts/regression_mission_variety_pack.lua` (catalog floor, pack rotation, and new objective inclusion assertions).

## 2026-03-19 — Mission Momentum Bonus Experiment Shipped
- Completed backlog item: objective streak micro-reward for missions.
- Durable decision: mission objective completions now grant capped momentum payout in BUILDER.SRL using streak curve **1, 1, 2** (cap at streak 3+).
- Implementation notes:
  - `RunMissions.addProgress` now returns structured completion payload (`completedObjectiveIds`, `completionStreak`, `rewardSrl`).
  - Main loop consumes completion payload and applies `builder_scroll` payout immediately with DOS status messaging.
  - Inventory-full path is explicit (`... DROPPED (BAG FULL)`) to avoid silent reward loss.
- Verification:
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
  - `luac -p main.lua src/run_missions.lua`
- Next recommended item (POST_RC_BACKLOG): `Add weekly sustain audit JSON pretty mode`.

## 2026-03-20 00:26 KST — Post-RC P1 map identity pass completed
- map_03~07 now carry explicit tactical identity metadata (`silhouette`, `laneStructure`, `encounterRhythm`) to prevent map feel drift.
- Runtime now reads `Map.metadata` and applies per-map encounter pacing through enemy count multipliers + behavior bias.
- Added regression guardrail: `scripts/regression_map_profile_distinctness.lua` ensures map_03~07 identity tags stay unique and encounter profile fields remain valid.
- Validation set: profile distinctness PASS, portal integrity PASS, map_01~04 progression PASS, enemy behavior regression PASS.
- Backlog state: `POST_RC_BACKLOG.md` P1 item “Redesign map_03~07 …” marked complete.
- Next priority: P1 portal repositioning with return-path + landmark rules.

## 2026-03-20 00:58 KST — P1 portal progression rules completed
- Completed backlog item: `World Team: Reposition portals with logical progression rules (clear return paths, risk/reward routing, landmark-based placement)`.
- Durable decisions:
  - map_03 portals were redistributed to three distinct landmarks (west-upper return, north apex progression, east-south fallback).
  - map_04 now serves as a hinge hub with explicit fallback (`map_01`) and forward push (`map_05`) at separated landmarks.
  - map_05~07 chain portals moved away from corner clustering to improve landmark legibility while preserving bidirectional progression.
- Verification set:
  - `luac -p maps/map_03.lua maps/map_04.lua maps/map_05.lua maps/map_06.lua maps/map_07.lua`
  - `python3 scripts/validate_portals.py`
  - `python3 scripts/regression_map_progression.py`
- Backlog update: `POST_RC_BACKLOG.md` P1 portal repositioning item marked done.
- Next priority item: P2 `Add weekly sustain audit JSON pretty mode`.

## 2026-03-20 01:28 KST — P2 weekly audit JSON pretty mode completed
- Completed backlog item: `Add weekly sustain audit JSON pretty mode`.
- Durable decision: `scripts/audit_weekly_sustain_cron.sh --format json --pretty` now emits indented JSON for operator readability while plain `--format json` remains compact/stable for machine consumers.
- Guardrail: `--pretty` is now explicitly rejected unless `--format json` is selected.
- Verification set:
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py`
  - `python3 scripts/regression_weekly_cron_audit.py`
- Backlog update: `POST_RC_BACKLOG.md` P2 pretty-mode item marked done.
- Next priority item: P2 `Add sustain health dashboard markdown report`.

## 2026-03-20 01:59 KST — P2 sustain health dashboard report completed
- Completed backlog item: `Add sustain health dashboard markdown report`.
- Durable decisions:
  - Added `scripts/sustain_health_dashboard.py` to generate `logs/sustain_health_dashboard.md` with a 3-signal health rollup (economy safety, telemetry freshness, scheduler audit).
  - `scripts/run_weekly_sustain.sh` now attempts cron audit capture (`logs/weekly_sustain_cron_audit.json`) and gracefully degrades to warning state when no managed cron entry exists.
  - Added regression guardrail `scripts/regression_sustain_health_dashboard.py` and linked dashboard commands into RC sustain checklist.
- Verification set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Backlog update: `POST_RC_BACKLOG.md` P2 dashboard item marked done.
- Next priority item: P2 `Add automatic stale-branch/report drift check`.

## 2026-03-20 02:26 KST — P2 stale-branch/report drift check completed
- Completed backlog item: `Add automatic stale-branch/report drift check`.
- Durable decisions:
  - Added `scripts/stale_branch_report_drift_check.py` to emit `logs/stale_branch_report_drift.{md,json}` with combined branch freshness (upstream behind/ahead + commit age) and sustain-report freshness checks.
  - Drift checker prefers embedded JSON `generatedAt` and gracefully falls back to file mtime for markdown artifacts.
  - Weekly sustain runner now includes drift check + regression (`scripts/regression_stale_branch_report_drift.py`) in the one-command pipeline.
- Verification set:
  - `python3 -m py_compile scripts/stale_branch_report_drift_check.py scripts/regression_stale_branch_report_drift.py`
  - `python3 scripts/regression_stale_branch_report_drift.py`
  - `python3 scripts/stale_branch_report_drift_check.py`
- Backlog update: `POST_RC_BACKLOG.md` item marked done.
- Next priority item: none remaining in `POST_RC_BACKLOG.md` (all checked).

## 2026-03-20 03:00 KST — P2 sustain dashboard JSON mode completed
- Completed backlog item: `Add sustain health dashboard JSON output mode (compact + pretty) and wire weekly runner artifact output`.
- Durable decisions:
  - `scripts/sustain_health_dashboard.py` now supports `--format md|json` (default `md`) and optional `--pretty` for indented JSON output.
  - JSON payload schema is standardized around `overall`, `signals`, `weeklySnapshot`, and `schedulerPolicy` to support automation consumers.
  - `--pretty` is explicitly rejected unless `--format json` is selected to keep CLI behavior unambiguous.
  - Weekly sustain runner now publishes both dashboard artifacts: `logs/sustain_health_dashboard.md` and `logs/sustain_health_dashboard.json`.
- Verification set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Backlog update: `POST_RC_BACKLOG.md` new P2 item marked done.
- Next priority item: none remaining in `POST_RC_BACKLOG.md` (all checked).

## 2026-03-20 03:29 KST — P2 sustain dashboard trend classification
- Completed task: Add sustain dashboard trend classification (`improving|stable|degrading`) with regression coverage.
- Durable decisions:
  - Added `overall.trend` to dashboard JSON; markdown now surfaces `Trend: **...**` directly under overall tier.
  - Trend is computed from weekly delta signals (events/SRL) and economy safety override (suspicious windows or curve-change decisions force `degrading`).
  - Health-tier scoring remains unchanged (trend is additive, non-breaking for existing consumers).
- Verification set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Backlog update: `POST_RC_BACKLOG.md` P2 trend-classification item marked done.
- Next priority item: none remaining in `POST_RC_BACKLOG.md` (all checked).
- Mission HUD now surfaces compact pacing metadata (`PACK:<id>`, `STREAK:<n>`) directly under `RUN MISSIONS` for in-run readability.
- Run summary snapshots now persist mission metadata (`missionPackId`, `momentumStreak`) alongside objective/carryover details.
- Regression coverage extended in `scripts/regression_run_summary.lua` to lock mission metadata snapshot integrity.

## 2026-03-20 03:58 KST — P1 mission pacing readability metadata
- Completed backlog item: `Surface active mission-pack id + momentum streak in HUD/run-summary for clearer run pacing readability`.
- Durable decisions:
  - Added compact mission panel metadata row (`PACK`, `STREAK`) without changing mission/combat/economy logic.
  - Run summary now records pack id + streak so post-run reviews retain pacing context.
- Verification set:
  - `luac -p src/hud.lua src/run_summary.lua scripts/regression_run_summary.lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update: `POST_RC_BACKLOG.md` P1 gameplay follow-up item marked done.
- Next priority item: none currently unchecked in `POST_RC_BACKLOG.md`.
- Mission momentum rewards now include a lane-switch variety bonus (+1 BUILDER.SRL) when consecutive objective completions come from different lanes, while preserving the base streak curve (1/1/2).
- Mission status messaging now annotates variety payouts with `[VARIETY +1]` (including bag-full drop path) for readable reward causality.

## 2026-03-20 04:29 KST — P1 mission momentum lane-switch variety bonus
- Completed backlog item: `Add mission momentum lane-switch variety bonus (+1 BUILDER.SRL on consecutive objective completions from different lanes)`.
- Durable decisions:
  - Added `lastCompletedLane` tracking in run mission state to detect lane alternation between objective completions.
  - Reward payload now exposes `baseRewardSrl`, `laneSwitchBonusSrl`, and total `rewardSrl` so downstream UX can explain payout composition.
  - Applied compact UX annotation `[VARIETY +1]` in mission reward status text without changing inventory/economy fundamentals.
- Verification set:
  - `luac -p main.lua src/run_missions.lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update: `POST_RC_BACKLOG.md` item marked done.
- Next priority item: none unchecked in tracked backlogs; next cycle should inject a fresh Game Director experiment candidate.
- Mission pack rotation now includes deterministic flavor metadata (`lastPackTag`, `lastPackLabel`) in mission state for pacing readability without altering objective logic.
- HUD mission panel now surfaces `PACK/TAG/STREAK`, and run summary snapshot now persists and displays `missionPackTag` + `missionPackLabel` (`PACE`) for post-run context.
- Regression coverage extended so mission variety/summary tests assert flavor metadata presence and snapshot integrity.

## 2026-03-20 04:59 KST — P1 gameplay follow-up: mission pack flavor descriptors
- Completed backlog item: `Add mission-pack flavor descriptors and surface compact tag in HUD/run-summary`.
- Durable decisions:
  - Default mission packs now define explicit flavor descriptors (`BASELINE/HUNT/FORGE/PIVOT`) plus short pacing labels.
  - Summary snapshot contract expanded with `missionPackTag` and `missionPackLabel` for durable run review context.
- Verification set:
  - `luac -p src/run_missions.lua src/run_summary.lua src/hud.lua scripts/regression_run_summary.lua scripts/regression_mission_variety_pack.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update: `POST_RC_BACKLOG.md` item marked done.
- Next priority item: none currently unchecked in tracked backlogs; inject next Game Director experiment in next cycle.

## 2026-03-20 05:29 KST — P1 combat experiment: berserker desperation behavior
- Completed backlog item: `Combat Team: Add berserker desperation behavior (low-HP speed/damage spike) with regression coverage`.
- Durable decisions:
  - Added new enemy archetype `berserker` to spawn roster and behavior catalog.
  - Enemy modifier sync now composes synergy and low-HP desperation in one deterministic pass (move cadence, attack cadence, attack damage).
  - Berserker desperation trigger is profile-driven (`hp <= 2`) to keep tuning/rollback low-risk.
- Verification set:
  - `luac -p src/enemy_ai.lua src/entities.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update: `POST_RC_BACKLOG.md` combat experiment item marked done.
- Next priority item: none unchecked in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate next cycle.

## 2026-03-20 05:44 KST — P1 combat readability experiment: berserker telegraph
- Completed experiment slice: `UX/Combat Team: Telegraph berserker desperation state in HUD + combat status feed`.
- Durable decisions:
  - Enemy AI now exposes one-shot transition signal `justEnteredDesperation` when berserker low-HP mode first activates.
  - Runtime emits explicit warning status text only when enraging enemy is visible, then clears signal to prevent spam.
  - HUD now surfaces active desperate berserker count (`Berserk: n`) for persistent threat readability.
- Verification set:
  - `luac -p src/enemy_ai.lua main.lua src/hud.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update:
  - Marked telegraph experiment done in `POST_RC_BACKLOG.md` and `TASKS.md`.
  - Added next candidate: berserker pre-lunge tell (one-turn warning) as unchecked follow-up.

## 2026-03-20 06:02 KST — P1 combat readability/fairness experiment: berserker pre-lunge tell
- Completed backlog item: `Combat Team: Add one-turn pre-lunge tell for berserker desperation attacks (readability/fairness A/B)`.
- Durable decisions:
  - Berserker desperation attacks now run a deterministic two-step cadence: telegraph turn first, then lunge hit turn.
  - Enemy AI tracks `desperationLungePrimed`; runtime surfaces telegraph via status feed and HUD (`Lunge Tell: n`).
  - Combat event plumbing in `Entities.update` now reports lunge telegraph counts without changing non-berserker behavior paths.
- Verification set:
  - `lua scripts/regression_enemy_behavior_variants.lua`
  - `luac -p src/enemy_ai.lua src/entities.lua src/hud.lua main.lua`
- Backlog update:
  - Marked pre-lunge tell task done in `TASKS.md` and `POST_RC_BACKLOG.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; request next Game Director experiment injection.

## 2026-03-20 06:30 KST — P1 combat fairness follow-up: berserker post-lunge recovery
- Completed backlog item: `Combat Team: Add one-turn post-lunge recovery window for berserker desperation chain (readability/fairness follow-up)`.
- Durable decisions:
  - Berserker desperation cadence is now deterministic three-step: **telegraph -> lunge hit -> one-turn recovery**.
  - Enemy AI now tracks `desperationRecoveryPending`; recovery consumes one attack turn and then clears.
  - Runtime status feed now emits explicit recovery feedback (`BERSERKER RECOVERING: BRIEF BREATHER`) via new combat event `berserker_lunge_recovery`.
- Verification set:
  - `luac -p src/enemy_ai.lua src/entities.lua main.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update:
  - Marked new P1 combat follow-up item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate next cycle.

## 2026-03-20 06:58 KST — P1 combat readability follow-up: berserker recovery HUD counter
- Completed backlog item: `UX/Combat Team: Surface active berserker recovery-window count in HUD threat strip`.
- Durable decisions:
  - Refactored HUD combat-threat counting into `HUD.collectCombatThreatCounters(enemies)` to keep threat-strip semantics testable.
  - Added `Recovering: n` HUD row (amber) for berserkers with `desperationRecoveryPending`, shown only while desperation is active.
  - Threat hierarchy remains urgency-ordered: `Berserk` -> `Lunge Tell` -> `Recovering`.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update:
  - Marked new HUD recovery-counter item done in `POST_RC_BACKLOG.md` and `TASKS.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; next cycle should inject a fresh Game Director experiment candidate.

## 2026-03-20 07:26 KST — P1 gameplay experiment: mission variety bonus preview hint
- Completed backlog item: `UX/Systems Team: Add mission lane-switch preview hint in HUD so players can anticipate variety bonus (+1 BUILDER.SRL)`.
- Durable decisions:
  - `RunMissions.getState()` now exposes `nextVarietyLane` + `varietyBonusPreview` derived from unfinished alternate-lane objectives after the latest completion.
  - HUD mission metadata row now conditionally appends `NEXT:<lane> +1` when variety bonus is currently achievable.
  - Variety payout mechanics remain unchanged (preview-only readability pass).
- Verification set:
  - `luac -p src/run_missions.lua src/hud.lua scripts/regression_mission_variety_preview.lua`
  - `lua scripts/regression_mission_variety_preview.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update:
  - Marked new P1 gameplay experiment item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate.

## 2026-03-20 07:56 KST — P1 gameplay readability follow-up: mission variety mastery counter
- Completed backlog item: `UX/Systems Team: Track and surface mission lane-switch variety bonus count in HUD/run-summary`.
- Durable decisions:
  - Added mission-state stat `varietyBonusCount` (increments only on lane-switch bonus payouts, resets on mission reset).
  - HUD mission metadata now includes compact `VAR:<n>` token next to `PACK/TAG/STREAK`.
  - Run summary snapshot now persists/displays `varietyBonusCount` for post-run pacing review.
- Verification set:
  - `luac -p src/run_missions.lua src/run_summary.lua src/hud.lua scripts/regression_mission_momentum.lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_mission_variety_preview.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update:
  - Marked new P1 gameplay experiment item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject a fresh Game Director experiment candidate next cycle.

## 2026-03-20 08:28 KST — P1 combat readability follow-up: weighted berserker threat index
- Completed backlog item: `UX/Combat Team: Add weighted berserker threat index in HUD threat strip (THREAT:<n>)`.
- Durable decisions:
  - `HUD.collectCombatThreatCounters()` now computes `berserkerThreatScore` using weighted pressure formula: desperate +2(lunge primed) +1(recovery pending).
  - HUD threat strip now renders `Threat:<n>` below berserker count for faster danger scanning.
  - Top-left HUD panel height/help-row spacing adjusted to prevent text overlap while preserving existing counters.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog update:
  - Marked item done in `POST_RC_BACKLOG.md` and `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject a fresh Game Director experiment candidate.

## 2026-03-20 08:56 KST — P1 combat readability follow-up: threat tier label
- Completed backlog item: `UX/Combat Team: Add berserker threat-tier label (LOW|MED|HIGH) in HUD for score readability`.
- Durable decisions:
  - Added `HUD.getBerserkerThreatTier(score)` with deterministic thresholds: `LOW(0-2)`, `MED(3-5)`, `HIGH(>=6)`.
  - HUD threat-strip line now renders `Threat: <score> (<tier>)` to pair quantitative and qualitative danger cues.
  - Preserved existing compact combat rows (`Berserk`, `Lunge Tell`, `Recovering`) to avoid panel growth.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog update:
  - Marked new P1 item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject a fresh Game Director experiment candidate next cycle.

## 2026-03-20 09:28 KST — P1 combat readability follow-up: threat-tier color coding
- Completed backlog item: `UX/Combat Team: Color-code berserker threat-tier label in HUD (LOW=green, MED=amber, HIGH=red)`.
- Durable decisions:
  - Added `HUD.getBerserkerThreatColor(score)` to centralize tier-to-color mapping.
  - Threat row rendering now reuses existing `Threat: <score> (<tier>)` text while applying tier-specific color to reduce scan latency.
  - Kept explicit tier token in text to avoid color-only communication risk.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog update:
  - Marked item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate.

## 2026-03-20 10:06 KST — Post-RC Combat Readability: Threat formula legend
- Completed item:
  - `UX/Combat Team: Add compact berserker threat formula legend in HUD/combat status (THREAT = BERSERK + 2*LUNGE + RECOVER)`
- Product decisions:
  - Added reusable helpers in `src/hud.lua` for threat legend and weighted breakdown formatting.
  - HUD now shows live decomposition line when berserkers are active: `THREAT = <berserk> + 2*<lunge> + <recover> = <score>`.
  - Enrage combat status copy now includes compact teaching token: `[THREAT=B+2L+R]`.
- Verification set:
  - `luac -p main.lua src/hud.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog sync:
  - Marked done in `POST_RC_BACKLOG.md`.
  - Added mirrored completed entry in `TASKS.md`.
- Next priority:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; queue next Game Director experiment candidate (e.g., threat-aware onboarding micro-tip decay logic).

## 2026-03-20 10:35 KST — Berserker threat delta HUD slice
- Completed: Added turn-over-turn berserker threat delta indicator (`THREAT Δ:+n|-n`) in HUD combat strip.
- Durable decisions:
  - Keep delta math centralized in HUD helpers (`getBerserkerThreatDelta`, `formatBerserkerThreatDelta`) for deterministic testing.
  - Keep signed text visible even with directional colors (accessibility + log readability).
  - Persist compact layout by placing delta row directly below `Threat: <score> (<tier)`.
- Verification set:
  - `luac -p main.lua src/hud.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog sync:
  - Marked completed in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; queue next Game Director experiment candidate.

## 2026-03-20 10:58 KST — Game Director experiment: threat-aware onboarding micro-tip
- Completed vertical slice: after build onboarding milestone, HUD hint now teaches combat pressure model (`THREAT` + `THREAT Δ`) until first berserker threat event is observed.
- Durable decisions:
  - Added onboarding `threat` milestone in `src/onboarding_hints.lua` and state export.
  - Runtime marks milestone from berserker enrage/lunge signals in `main.lua` to avoid permanent tutorial copy.
  - Kept economy/combat mechanics untouched (UX-only reversible slice).
- Verification set:
  - `luac -p main.lua src/onboarding_hints.lua`
  - `lua scripts/regression_onboarding_hints.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog sync:
  - Marked completed in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
  - Added next experiment candidates: pressure-breaker bonus, overclock hazard room.

## 2026-03-20 11:06 KST — Mission pressure-breaker bonus shipped
- Completed: Systems/Combat P1 experiment `mission-chain pressure breaker bonus`.
- Durable decisions:
  - `RunMissions.addProgress` now accepts optional context and emits `pressureBreakerDodgeCharge` on rising-threat completions.
  - Main loop tracks short rising-threat window from berserker threat-score delta and applies pressure-breaker dodge charge grants (6s TTL).
  - Enemy attack resolution consumes dodge charges before damage (`dodged_player`) while preserving berserker recovery flow.
  - HUD/status readability updated with `Dodge:<n>` + pressure-breaker trigger copy.
- Verification:
  - `luac -p main.lua src/run_missions.lua src/player.lua src/enemy_ai.lua src/entities.lua src/hud.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_pressure_breaker.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Next priority: `World/Design Team: Add overclock hazard room prototype (SRL discount pulse + aggro spike risk)`.

## 2026-03-20 11:26 KST — Overclock hazard room prototype shipped
- Completed: `World/Design Team: Add overclock hazard room prototype (SRL discount pulse + aggro spike risk)`.
- Durable decisions:
  - New runtime module `src/overclock_hazard.lua` owns zone pulse/cooldown state, build-cost discount, and combat pressure profile.
  - `maps/map_07.lua` now defines prototype hazard room metadata in center contest zone.
  - Build-cost plan (`src/inventory_ui.lua`) applies temporary SRL discount during active pulse.
  - Enemy AI consumes hazard pressure (`EnemyAI.setThreatPressure`) to increase aggro via move-cadence + detection boost.
  - HUD/status now surface overclock state (`OVERCLOCK READY/HOT/CD`) and pulse activation/expiry messages.
- Verification:
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_mission_pressure_breaker.lua`
  - `luac -p src/overclock_hazard.lua src/entities.lua src/enemy_ai.lua src/inventory_ui.lua src/hud.lua main.lua maps/map_07.lua`
- Next priority: `P2 Ops — QA/Systems: weekly changelog drift detector`.

## 2026-03-20 12:01 KST — P2 weekly changelog drift detector completed
- Completed backlog item: `QA/Systems: Add weekly changelog drift detector (code changes without corresponding team-log/report entry)`.
- Durable decision: weekly sustain now audits recent code commits for same-commit evidence updates (team logs/playtest artifacts/changelog trackers) via `scripts/weekly_changelog_drift_check.py` with artifacts at `logs/weekly_changelog_drift.{md,json}`.
- Regression guardrail: `scripts/regression_weekly_changelog_drift.py` validates WARN on code-only commit and OK on code+evidence commit.
- Ops wiring: `scripts/run_weekly_sustain.sh` now runs detector + regression and includes drift artifacts in its output manifest.
- RC checklist matrix now includes a dedicated row for weekly changelog drift detection.
- Verification set:
  - `python3 -m py_compile scripts/weekly_changelog_drift_check.py scripts/regression_weekly_changelog_drift.py`
  - `python3 scripts/regression_weekly_changelog_drift.py`
  - `python3 scripts/weekly_changelog_drift_check.py`
  - `bash scripts/run_weekly_sustain.sh`
- Current detector status on branch: `WARN` (historical code commits in scan window without same-commit evidence updates), which is expected baseline before enforcement adoption.
- Next priority item (POST_RC_BACKLOG): `Ops: Add sustain dashboard regression risk score (0~100) with threshold alert section`.
- Sustain health dashboard now includes a computed `regressionRisk` block (0~100) with thresholded alert states (`OK`/`WARN`/`ALERT`) and fixed thresholds (`warnAt=30`, `alertAt=60`).
- Markdown dashboard includes a dedicated **Regression Risk** section so weekly ops reviews can spot escalating regression pressure without parsing raw signals.
- Overclock hazard HUD hint now includes explicit active-pulse and cooldown countdown seconds (`OVERCLOCK HOT <n>s`, `OVERCLOCK CD <n>s`) for better risk/reward timing readability while traversing map_07 hazard zones.
- Added sustain dashboard `regressionRisk.topDrivers` (top 3 weighted contributors) to both markdown and JSON outputs for faster root-cause scanning during weekly ops review.
- Regression coverage now asserts driver rendering in markdown and payload correctness in JSON (`trendStable` baseline case).
- Completed POST_RC item: `Ops: Add sustain dashboard regression-risk driver breakdown (top contributors) in markdown/json with regression coverage`.
- Next priority item: none currently unchecked in `POST_RC_BACKLOG.md` (needs new Game Director experiment injection).
- 2026-03-20 14:29 KST: Completed POST-RC hazard readability follow-up — overclock HUD hint now includes persistent `RISK:<tier>(<score>)` label in READY/HOT/CD states.
- Risk-tier derivation is display-only and computed from existing hazard knobs (`discountPct`, `aggroDetectBonus`, `aggroMoveMul`) to avoid content/schema churn.
- Regression coverage updated: `scripts/regression_overclock_hazard.lua` now asserts risk label presence across all hazard hint states.
- Verification pass: `lua scripts/regression_overclock_hazard.lua`, `luac -p src/overclock_hazard.lua`.
- Next priority: no unchecked items currently present in `POST_RC_BACKLOG.md` (requires new backlog injection).
- 2026-03-20 14:56 KST: Added active overclock pulse aggro-pressure legend in HUD hint (`AGGRO DET:+n MOVE:+m%`) so hazard risk is explicit beyond generic `AGGRO+` text.
- Change is readability-only: hazard mechanics, scoring, and map metadata remain unchanged.
- Regression coverage updated in `scripts/regression_overclock_hazard.lua` to assert detect/move legend tokens in HOT state.
- Verification pass: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`, `lua scripts/regression_overclock_hazard.lua`.


- Overclock hazard cooldown hint now shows in-zone near-ready warning token `IMMINENT:<n>s` during final 3 seconds before pulse re-arm; warning hides outside the hazard zone.
- Regression coverage for overclock hazard now asserts imminent warning visibility/hide behavior (`scripts/regression_overclock_hazard.lua`).

## 2026-03-20 16:29 KST — P1 hazard readability follow-up: pulse-imminent warning
- Completed backlog item: `UX/World Team: Add overclock pulse-imminent warning in cooldown HUD hint when standing in hazard zone (IMMINENT:<n>s)`.
- Durable decisions:
  - Show imminent warning only when player is inside hazard zone and cooldown is within 3 seconds.
  - Keep warning embedded in existing cooldown hint line to preserve DOS HUD compactness.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked new item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; inject fresh Game Director experiment candidate next cycle.
- Overclock hazard now supports pulse-capped hot-zone kill bounty rewards (`killBonusPerKill`, `killBonusPulseCap`) and runtime payout via `OverclockHazard.consumeKillBonus(kills)`.
- map_07 overclock metadata now sets baseline bounty tuning (`killBonusPerKill=1`, `killBonusPulseCap=3`).
- Overclock hazard regression now asserts kill bounty payout, pulse cap enforcement, and outside-zone no-reward behavior.

## 2026-03-20 16:55 KST — P1 hazard reward follow-up: hot-zone kill bounty
- Completed backlog item: `Systems/World Team: Add overclock hot-zone kill bounty (+BUILDER.SRL per kill, pulse-capped)`.
- Durable decisions:
  - Kill bounty awards only while player is inside active overclock pulse zone.
  - Payout is pulse-capped to keep reward additive without opening an infinite SRL loop.
  - Runtime status copy explains bonus trigger immediately (`OVERCLOCK BOUNTY...`).
- Verification set:
  - `luac -p main.lua src/overclock_hazard.lua maps/map_07.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md` and `TASKS.md`.
  - Added next follow-up candidate: HOT-hint bounty progress token (`BOUNTY:x/y`).

## 2026-03-20 17:03 KST — P1 hazard reward follow-up: HOT bounty progress token
- Completed backlog item: `UX/Systems Team: Surface overclock bounty pulse cap progress in HUD hint (BOUNTY:x/y) during HOT state`.
- Durable decisions:
  - HOT hint now includes `BOUNTY:x/y` derived from pulse reward units granted vs per-pulse cap.
  - Token initializes at `0/cap` when pulse activates and updates as kills consume bounty budget.
  - Layout stays single-line DOS style (`discount / aggro legend / bounty`) to avoid HUD row growth.
- Verification set:
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked item done in `POST_RC_BACKLOG.md` and mirrored done in `TASKS.md`.
- Next priority item:
  - No unchecked items currently remain in `POST_RC_BACKLOG.md`.

## 2026-03-20 17:31 KST — P1 hazard reward readability: READY/CD next-pulse bounty budget
- Completed backlog item: `UX/Systems Team: Surface next-pulse bounty budget token in READY/CD hints (NEXT BOUNTY:0/y) for reward planning`.
- Durable decisions:
  - Overclock READY and cooldown HUD hints now include `NEXT BOUNTY:0/y` so reward budget is legible before pulse activation.
  - This is display-only; kill-bounty payout/cap mechanics are unchanged.
  - Imminent cooldown warning (`IMMINENT`) now coexists with `NEXT BOUNTY` token in a single compact hint line.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md` and mirrored done in `TASKS.md`.
- Next priority item:
  - No unchecked items remain in ACTION_ITEMS/TASKS/POST_RC; inject next Game Director experiment candidate next cycle.

## 2026-03-20 18:01 KST — P1 hazard readability wave 2: risk-tier color coding in overclock HUD hint
- Completed backlog item: `UX/World Team: Color-code overclock RISK tier in HUD hint (LOW=green, MED=amber, HIGH=red)`.
- Durable decisions:
  - Overclock hazard module now exposes tier-aware HUD color metadata (`getHudHintColor`) to keep risk semantics centralized.
  - HUD auxiliary threat hint renderer accepts optional per-hint RGBA color and falls back to existing amber tone when metadata is absent.
  - Risk-tier color mapping mirrors established threat readability palette: LOW green, MED amber, HIGH red.
- Verification set:
  - `luac -p main.lua src/hud.lua src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md` and mirrored done in `TASKS.md`.
- Next priority item:
  - ACTION_ITEMS/TASKS/POST_RC currently fully checked; inject next validated Game Director experiment candidate.
- Overclock HUD hints now include compact risk-factor breakdown token `RISK SRC:Dx+DETy+MOVEz` in READY/HOT/CD states so hazard tuning impact is legible in-run without opening configs.

## 2026-03-20 18:31 KST — P1 hazard readability wave 3: risk-factor breakdown token
- Completed backlog item: `UX/Systems Team: Add compact overclock risk-factor breakdown token in HUD hint (RISK SRC:Dx+DETy+MOVEz)`.
- Durable decisions:
  - Added `getRiskComponents` + `getRiskBreakdownToken` in `src/overclock_hazard.lua` so risk score internals remain centralized and testable.
  - OVERCLOCK READY/HOT/CD HUD hints now append `RISK SRC:Dx+DETy+MOVEz` alongside existing `RISK:<tier>(<score>)` token.
  - Change is readability-only (no hazard reward/aggro/economy tuning changes).
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md`.
- Next priority item:
  - ACTION_ITEMS/TASKS/POST_RC currently fully checked; inject next validated Game Director experiment candidate next cycle.

## 2026-03-20 19:03 KST — P1 hazard readability wave 4 (next-pulse ETA)
- Completed backlog item: `UX/World Team: Add overclock pulse ETA token in READY/CD HUD hints (NEXT PULSE:<n>s)`.
- Durable decisions:
  - Added `getNextPulseEtaToken()` helper in `src/overclock_hazard.lua` to standardize cooldown/ready timing copy.
  - READY and CD/IMMINENT hints now include `NEXT PULSE:<n>s` while HOT hint payload remains unchanged to preserve compact combat readability.
  - Regression guardrail extended in `scripts/regression_overclock_hazard.lua` to assert ETA token visibility in READY/CD/IMMINENT states.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update: `POST_RC_BACKLOG.md` wave-4 item marked done.
- Next priority item: none currently unchecked in tracked backlogs; inject next Game Director experiment candidate.

## 2026-03-20 19:39 KST — P1 hazard readability wave 5 (pulse/recharge progress)
- Completed backlog item: `UX/World Team: Add pulse progress token in overclock HUD hints (PULSE:%/RECHARGE:%)`.
- Durable decisions:
  - Added reusable timing-format helpers in `src/overclock_hazard.lua` for pulse and cooldown progress percentages.
  - HOT hint now shows `PULSE:%`; READY/CD/IMMINENT hints now show `RECHARGE:%` while preserving existing risk/bounty/ETA tokens.
  - Regression updated in `scripts/regression_overclock_hazard.lua` to lock token visibility across state transitions.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-5 item done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
- Next priority item:
  - No unchecked entries currently remain in ACTION_ITEMS/TASKS/POST_RC; queue next Game Director experiment candidate for injection.

## 2026-03-20 20:01 KST — Hazard Readability Wave 6
- Completed backlog item: `UX/World Team: Add overclock risk-trend token in READY/CD/HOT hints (RISK Δ:+n|-n)`.
- Durable decisions:
  - Added state-aware `RISK Δ` formatter in `src/overclock_hazard.lua` (+2 during HOT pulse, +1 while in-zone IMMINENT cooldown, 0 otherwise).
  - Kept existing `RISK:<tier>(score)` + `RISK SRC` tokens unchanged to preserve tuning readability while adding pressure-shift signal.
  - Applied token to READY/HOT/CD/IMMINENT copy paths with compact DOS-safe line format.
- Verification set:
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-6 item done in `POST_RC_BACKLOG.md` and mirrored subtask completion in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain across ACTION_ITEMS/TASKS/POST_RC; inject next validated Game Director experiment candidate.

## 2026-03-20 20:33 KST — P1 hazard readability wave 7 (zone presence token)
- Completed backlog item: `UX/World Team: Add overclock zone-presence token in HUD hints (ZONE:IN|OUT)`.
- Durable decisions:
  - Added `getZonePresenceToken()` in `src/overclock_hazard.lua` driven by in-zone runtime state (`state.enteredZone`).
  - Overclock READY/HOT/CD/IMMINENT hints now include `ZONE:IN|OUT` while preserving existing risk/bounty/ETA/progress tokens.
  - Change is readability-only; no hazard balance/economy tuning adjustments.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-7 item done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; inject next validated Game Director experiment candidate.
- 2026-03-20 21:04 KST: Completed POST-RC P1 hazard readability wave 8 — overclock HUD hints now include `EXPOSED:<n>s` while player remains in-zone (`ZONE:IN`) across HOT/CD/IMMINENT states.
- Durable decision: exposure timer is continuous-in-zone only (accumulates inside, resets on exit) and is display-only with no hazard balance/economy changes.
- Regression coverage: `scripts/regression_overclock_hazard.lua` now asserts exposure token presence in-zone and absence out-of-zone.
- Verification pass: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`, `lua scripts/regression_overclock_hazard.lua`.

## 2026-03-20 21:34 KST — P1 hazard readability wave 9 (exposure commitment tier)
- Completed backlog item: `UX/World Team: Add overclock exposure commitment-tier token in HUD hints (COMMIT:LOW|MID|HIGH)`.
- Durable decisions:
  - Added exposure-tier helpers in `src/overclock_hazard.lua` with stable thresholds (`LOW <5s`, `MID <12s`, `HIGH >=12s`).
  - HUD hints now append `COMMIT:<tier>` alongside `EXPOSED:<n>s` during HOT/CD/IMMINENT in-zone states; token clears when player leaves zone (`ZONE:OUT`).
  - Change is readability-only (no economy/combat parameter changes).
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-9 done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
- Next priority item:
  - No unchecked entries currently remain in ACTION_ITEMS/TASKS/POST_RC; inject next validated Game Director experiment candidate.

## 2026-03-20 21:42 KST — P1 hazard readability wave 10 (`RISK Δ` color semantics)
- Completed backlog item: `UX/World Team: Add overclock risk-delta color semantics in HUD hint (rising=red, cooling=green)`.
- Durable decisions:
  - `OverclockHazard.getHudHintColor()` now prioritizes delta-state color when `RISK Δ` is non-zero (red on rising pressure, green on cooling retreat).
  - During out-of-zone cooldown, hazard hint now emits `RISK Δ:-1` to make safe disengage timing explicit.
  - Neutral states keep existing risk-tier color mapping (LOW/MED/HIGH).
- Verification set:
  - `lua scripts/regression_overclock_hazard.lua`
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-10 delta-color item done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
  - Added next candidates: post-pulse relief `WINDOW` token and exposure dwell-bucket telemetry.
- Next priority item:
  - `UX/World Team: Add overclock pulse-end relief burst HUD token (WINDOW:<n>s)`.

## 2026-03-20 22:01 KST — P1 hazard readability wave 10 follow-up (`WINDOW` relief token)
- Completed backlog item: `UX/World Team: Add overclock pulse-end relief burst (+short WINDOW token) after exiting HOT zone to reward disengage timing`.
- Implementation notes:
  - Added relief-window state in `src/overclock_hazard.lua` (`pendingRelief`, `reliefTimer`, configurable `reliefWindowDuration`, default 3s).
  - Relief now arms on HOT-zone disengage and activates only after pulse expiry while player remains outside.
  - Cooldown hint now appends `WINDOW:<n>s` only in out-of-zone cooldown during active relief window; token expires automatically.
- Regression updates:
  - Extended `scripts/regression_overclock_hazard.lua` with relief-window visibility/expiry assertions.
- Verification:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Next priority:
  - `Systems/Telemetry Team: Log overclock zone dwell buckets (LOW|MID|HIGH) per run for exposure-driven tuning evidence`.

## 2026-03-20 22:35 KST — Overclock exposure dwell telemetry baseline
- Completed Post-RC hazard wave follow-up: per-run overclock exposure dwell buckets now tracked as `LOW|MID|HIGH` seconds in hazard runtime state.
- Decision: accumulate dwell using threshold-aware segmentation so long ticks crossing 5s/12s boundaries distribute correctly across buckets (avoids single-bucket misattribution).
- Runtime integration: latest per-run artifact now written on run reset (`R`) to `logs/playtests/overclock_dwell_buckets_latest.json` + `.md`.
- QA coverage: `scripts/regression_overclock_dwell_buckets.lua` validates bucket math + telemetry schema + total exposure aggregation.
- Impact hypothesis: gives tuning evidence for overclock commitment risk profile before adding dashboard-level trending.

## 2026-03-20 22:41 KST — Game Director review cycle executed
- Idea set (L/M/H risk) generated and backlog-injected under `POST_RC_BACKLOG.md` (Game Director Injection section).
- Implemented experiment: run-summary overclock dwell snapshot (`OVERCLOCK DWELL L/M/H`).
- Wiring: `OverclockHazard.getRunDwellBuckets()` snapshot is captured on reset and injected into `RunSummary` state.
- Verification: run summary + hazard + dwell telemetry regressions all PASS.
- Next candidates retained in backlog:
  - reward-efficiency token (`SRL/EXPOSED sec`)
  - multi-run dwell trend combiner artifact.

## 2026-03-20 23:03 KST — P1 Game Director injection: overclock reward-efficiency token
- Completed backlog item: `Systems/Design Team: Add overclock zone reward-efficiency token (SRL/EXPOSED sec) to run summary`.
- Durable decisions:
  - Overclock module now tracks per-run bounty reward total (`runRewardSrl`) and exposes `getRunRewardSrl()`.
  - Run summary snapshot now persists `overclockRewardSrl` and renders token: `OVERCLOCK EFF: <srl> SRL / <sec>s = <ratio> SRL/EXPOSED sec`.
  - Zero-exposure edge case renders `n/a` ratio to prevent divide-by-zero misinformation.
- Verification set:
  - `luac -p main.lua src/overclock_hazard.lua src/run_summary.lua src/hud.lua scripts/regression_run_summary.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_run_summary.lua`
- Next priority item: `QA/Systems Team: Add multi-run dwell trend combiner artifact (last N run medians)`.

## 2026-03-20 23:33 KST — P1 Game Director injection: multi-run dwell trend combiner
- Completed backlog item: `QA/Systems Team: Add multi-run dwell trend combiner artifact (last N run medians)`.
- Durable decisions:
  - Persist per-reset timestamped dwell snapshots (`overclock_dwell_buckets_run_*.json`) alongside latest snapshot to build review history.
  - New combiner `scripts/overclock_dwell_trend.py` computes median LOW/MID/HIGH/TOTAL and aggregate mix% over last-N runs.
  - Weekly sustain runner now emits trend artifacts (`logs/playtests/overclock_dwell_trend.{md,json}`) and executes trend regression.
- Verification set:
  - `luac -p main.lua src/overclock_hazard.lua`
  - `python3 scripts/regression_overclock_dwell_trend.py`
  - `python3 scripts/overclock_dwell_trend.py --runs 3`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_run_summary.lua`
- Next item: all listed backlog lanes are checked; trigger next Game Director review cycle (3 ideas -> choose 1 -> vertical slice).

## 2026-03-20 23:36 KST — Game Director Cycle B completed (3 ideas -> 1 slice)
- Candidate ideas:
  1) **Chosen (low-risk UX):** run-summary commitment profile token from dwell mix.
  2) Mid-risk systems: trend artifact volatility classifier (`VOL:STEADY|SWING`).
  3) High-risk UX density: analytics glossary row in run summary.
- Implemented slice: `src/run_summary.lua` now computes `overclockProfile` and `src/hud.lua` renders `OVERCLOCK PROFILE: ...` under efficiency line.
- Backlog updated in `POST_RC_BACKLOG.md`: chosen item marked done; remaining two ideas retained as open injections.
- Verification:
  - `luac -p main.lua src/run_summary.lua src/hud.lua src/overclock_hazard.lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `python3 scripts/regression_overclock_dwell_trend.py`

## 2026-03-21 00:02 KST — P1 Game Director follow-up: dwell trend volatility token
- Completed backlog item: `Systems Team: Add overclock dwell trend volatility token (VOL:STEADY|SWING) to trend artifact`.
- Durable decisions:
  - `scripts/overclock_dwell_trend.py` now emits `volatility.level`, `volatility.token`, and compact diagnostics (`maxRelDeltaPct`, `avgRelDeltaPct`).
  - Volatility classification uses run-to-run total-exposure relative deltas with deterministic thresholds: `SWING` when `maxΔ>=45%` or `avgΔ>=30%`; otherwise `STEADY`.
  - Markdown trend report now includes a compact line: `Volatility: VOL:<level> (maxΔ ... , avgΔ ...)`.
- Verification set:
  - `python3 -m py_compile scripts/overclock_dwell_trend.py scripts/regression_overclock_dwell_trend.py`
  - `python3 scripts/regression_overclock_dwell_trend.py`
  - `python3 scripts/overclock_dwell_trend.py --runs 3`
- Backlog sync: marked the volatility token item done in `POST_RC_BACKLOG.md`.
- Next priority item: `QA/UX Team: Add compact run-summary tooltip glossary row for overclock analytics tokens (DWELL, EFF, PROFILE)`.

## 2026-03-21 00:32 KST — Post-RC backlog closure: run-summary overclock glossary row
- Closed remaining unchecked Post-RC item by shipping a compact glossary row in run summary:
  - `GLOSSARY: DWELL=EXPOSURE sec(L/M/H)  EFF=SRL/EXPOSED sec  PROFILE=COMMIT TIER`
- Files:
  - `src/hud.lua` (new glossary helper + rendered row)
  - `scripts/regression_run_summary.lua` (copy-stability assertion)
  - `POST_RC_BACKLOG.md` (item lifecycle `[ ] -> [~] -> [x]`)
- Verification:
  - `lua scripts/regression_run_summary.lua` PASS
  - `luac -p src/hud.lua` PASS
- State: ACTION_ITEMS/TASKS/POST_RC_BACKLOG all checked; next cycle should execute Game Director review loop (3 ideas -> pick 1 -> minimal vertical slice).

## 2026-03-21 00:36 KST — Game Director Cycle C executed (all prior backlogs completed)
- Idea slate generated:
  1) Low-risk UX: run-summary `COACH` cue from `PROFILE + EFF`
  2) Mid-risk systems: HIGH-threat objective clear boosts variety payout
  3) High-risk novelty: hazard route tags (`SAFE|RISK|SPIKE`) + HUD callout
- Chosen experiment: #1 (minimal vertical slice, reversible).
- Implementation:
  - `src/run_summary.lua`: added `resolveOverclockCoachTip(...)` and snapshot field `overclockCoachTip`.
  - `src/hud.lua`: renders `OVERCLOCK COACH: <tip>` line in run summary.
  - `scripts/regression_run_summary.lua`: added assertion for coach tip and kept glossary copy guard.
- Verification:
  - `lua scripts/regression_run_summary.lua` PASS
  - `luac -p src/run_summary.lua` PASS
  - `luac -p src/hud.lua` PASS
- Backlog updates (`POST_RC_BACKLOG.md`):
  - Coach cue task marked done.
  - Threat-scaler + hazard-route-tag tasks injected as next experiment candidates.

## 2026-03-21 01:04 KST — Game Director Cycle C follow-up: threat-linked momentum scaler prototype
- Completed Post-RC Cycle C item: `Systems/Combat Team: Prototype threat-linked momentum bonus scaler` behind experiment flag.
- Durable decisions:
  - Added env-gated experiment toggle `DOTPIO_EXPERIMENT_THREAT_LINKED_VARIETY_SCALER` in `src/run_missions.lua`.
  - Lane-switch variety bonus remains `+1` by default; scales to `+2` only when flag is ON and mission completion occurs at `THREAT LVL:HIGH`.
  - Mission progress context now receives live `threatTier` from combat threat counters.
  - UX status line explicitly labels scaled payout as `HIGH-THREAT SCALER`.
- Verification set (PASS):
  - `lua scripts/regression_mission_momentum.lua`
  - `DOTPIO_EXPERIMENT_THREAT_LINKED_VARIETY_SCALER=1 lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_pressure_breaker.lua`
- Next priority item: `World/Design Team: Prototype hazard room route tag (SAFE|RISK|SPIKE) in map metadata and HUD mini-callout for path planning`.

## 2026-03-21 01:34 KST — Game Director Cycle D (route-callout readability slice)
- Context: ACTION_ITEMS/TASKS/POST_RC backlog reached fully-checked state, triggering Game Director review cycle.
- Idea slate generated:
  1) Low-risk UX: route callout color semantics (`SAFE|RISK|SPIKE`).
  2) Mid-risk systems: portal transition route preview token (`NEXT ROUTE:<tag>`).
  3) High-risk QA/design: route-tag distribution drift checker across hazard maps.
- Selected experiment: #1 (low-risk, reversible, immediate readability gain).
- Shipped decisions:
  - Route tags are map-metadata-driven (`overclockHazard.routeTag`).
  - Hazard module now exposes `getRouteTag/getRouteCallout/getRouteCalloutColor` with strict tag validation.
  - HUD renders `ROUTE:<tag>` mini-callout near enemy strip and applies semantic colors (SAFE green / RISK amber / SPIKE red).
  - Berserker threat rows offset when route callout exists to avoid visual overlap.
- Verification set (PASS):
  - `luac -p main.lua src/hud.lua src/overclock_hazard.lua maps/map_07.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog injection status:
  - Done: route mini-callout color semantics.
  - Pending: portal hover route preview, route-tag distribution checker.
- Next priority item: `Systems/World Team: Add portal-hover route preview token (NEXT ROUTE:<tag>) in transition prompt before confirming map jump`.

## 2026-03-21 02:06 KST — Post-RC Cycle D follow-up shipped (portal route preview)
- Completed backlog item: `Systems/World Team: Add portal-hover route preview token (NEXT ROUTE:<tag>) in transition prompt before confirming map jump`.
- Gameplay/runtime decision: portal contact now opens a confirm/cancel transition prompt instead of immediate warp.
- Route preview token source: destination map metadata `overclockHazard.routeTag` (`SAFE|RISK|SPIKE`, fallback `UNKNOWN`).
- Evidence (PASS):
  - `luac -p main.lua src/portal.lua src/overclock_hazard.lua src/hud.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_portal_route_preview.lua`
- Backlog status:
  - Done: portal-hover route preview token.
  - Remaining top priority: route-tag distribution checker across hazard-enabled maps.

## 2026-03-21 02:31 KST — Route-tag audit closure + Cycle E slice
- Closed remaining Post-RC item by shipping route-tag distribution checker across hazard-enabled maps.
- New analyzer module: `src/route_tag_distribution.lua` with audit runner `scripts/check_route_tag_distribution.lua` and artifacts under `logs/playtests/route_tag_distribution.{md,json}`.
- Current live audit result is `WARN` (single hazard-enabled map profile: SPIKE-only), matching expected convergence warning behavior.
- All ACTION_ITEMS/TASKS/POST_RC were checked, so Game Director Cycle E executed:
  - Generated 3 ideas (low/mid/high risk).
  - Implemented low-risk vertical slice: portal prompt coaching cue token (`COACH:*`) mapped from `NEXT ROUTE`.
  - Injected two follow-up ideas into backlog as new unchecked tasks.
- Regression additions/updates:
  - New: `scripts/regression_route_tag_distribution.lua`
  - Updated: `scripts/regression_portal_route_preview.lua` for coaching token coverage.

## 2026-03-21 03:06 KST — Route-tag density ledger completed (Cycle E follow-up)
- Closed backlog item: route-tag density ledger artifact per map chain depth.
- New files:
  - 
  - 
  - 
  - 
  - 
- Key finding: current chain depth exposure is overwhelmingly  until  due limited routeTag metadata coverage.
- Next highest-priority unchecked backlog item: portal prompt copy budget checker (DOS width guard).

## 2026-03-21 03:06 KST — Route-tag density ledger completed (Cycle E follow-up)
- Closed backlog item: route-tag density ledger artifact per map chain depth.
- New files:
  - `src/route_tag_density_ledger.lua`
  - `scripts/check_route_tag_density_ledger.lua`
  - `scripts/regression_route_tag_density_ledger.lua`
  - `logs/playtests/route_tag_density_ledger.md`
  - `logs/playtests/route_tag_density_ledger.json`
- Key finding: current chain depth exposure is overwhelmingly `NONE` until `map_07 (SPIKE)` due limited routeTag metadata coverage.
- Next highest-priority unchecked backlog item: portal prompt copy budget checker (DOS width guard).

## 2026-03-21 03:35 KST — Portal prompt budget closure + Game Director Cycle F
- Closed remaining Cycle E unchecked backlog item with a new portal prompt copy budget audit:
  - `src/portal_prompt_budget.lua`
  - `scripts/check_portal_prompt_copy_budget.lua`
  - `scripts/regression_portal_prompt_copy_budget.lua`
  - Artifacts: `logs/playtests/portal_prompt_copy_budget.{md,json}`
- Audit baseline: `status=OK`, `checked=20`, `budget=76`, `maxObserved=75`, `warnings=0`.
- With ACTION_ITEMS/TASKS/POST_RC fully checked, executed Game Director Cycle F (3 ideas -> pick 1 -> vertical slice):
  - Chosen slice shipped: portal transition compact fallback when prompt budget is constrained (`NEXT:<tag> COACH:<short>`), while default detailed copy remains unchanged.
  - Added regression: `scripts/regression_portal_prompt_compact_mode.lua`.
- Backlog injection for next cycle (`POST_RC_BACKLOG.md` Cycle F):
  - Done: compact fallback.
  - Pending: route-pressure score token (`PRESSURE:<n>`), prompt token-order linter.


## 2026-03-21 03:36 KST — Game Director Cycle G: route-pressure token slice
- Idea slate (L/M/H risk):
  1) Low-risk UX/System (chosen): transition prompt `PRESSURE:<n>` token (route tag + live threat tier).
  2) Mid-risk QA/Design: prompt token-order linter (`ACTION -> ROUTE -> COACH -> PRESSURE`) with budget parser.
  3) High-risk novelty: adaptive `ALT ROUTE:<tag>` branch suggestion when pressure is high.
- Shipped vertical slice:
  - Portal prompt now includes pressure token in detailed mode and compact `P:<n>` fallback.
  - Pressure score mapping: route base (`SAFE=1`, `RISK=2`, `SPIKE=3`) + threat tier offset (`LOW=0`, `MED=+1`, `HIGH=+2`), clamped 1..5.
  - Main draw path now injects live berserker threat tier context into portal prompt rendering.
  - Prompt-budget analyzer updated to include pressure token in measured copy length.
- Verification (PASS):
  - `lua scripts/regression_portal_route_preview.lua`
  - `lua scripts/regression_portal_prompt_compact_mode.lua`
  - `lua scripts/regression_portal_prompt_copy_budget.lua`
  - `lua scripts/check_portal_prompt_copy_budget.lua`
- Result:
  - `PRESSURE` cue is now visible at transition decision point, but copy-budget audit flipped to `WARN` baseline (`max=87 > budget=76`), validating need for next QA linter/budget follow-up.
- Backlog sync:
  - Marked Cycle F pressure-token item done.
  - Added Cycle G trio with two follow-ups retained (token-order linter, adaptive alt-route hint).

## 2026-03-21 04:12 KST — Cycle G follow-up: transition prompt token-order linter + budget parser
- Completed backlog closure items:
  - `QA/Design Team: Add transition prompt token-order linter (warn when readability order deviates from ACTION->ROUTE->COACH/PRESSURE)`
  - `QA/Design Team: Add transition prompt token-order linter and budget parser (warn when token sequence deviates from ACTION -> ROUTE -> COACH -> PRESSURE)`
- Shipped tooling:
  - `src/portal_prompt_linter.lua` (shared prompt-order + budget-selection analyzer)
  - `scripts/check_portal_prompt_token_order.lua` (artifact generator)
  - `scripts/regression_portal_prompt_token_order.lua` (baseline regression)
- Evidence (PASS):
  - `luac -p src/portal_prompt_linter.lua scripts/check_portal_prompt_token_order.lua scripts/regression_portal_prompt_token_order.lua`
  - `lua scripts/regression_portal_prompt_token_order.lua`
  - `lua scripts/check_portal_prompt_token_order.lua`
- Artifact output:
  - `logs/playtests/portal_prompt_token_order.md`
  - `logs/playtests/portal_prompt_token_order.json`
- Next highest-priority unchecked backlog item:
  - `World/Design Team: Prototype adaptive portal hint (ALT ROUTE:<SAFE|RISK|SPIKE>) suggesting a lower-pressure branch when current pressure is high`.

## 2026-03-21 04:34 KST — Game Director Cycle H: adaptive pressure-drop coaching
- Idea slate (L/M/H risk):
  1) Low-risk UX/System (chosen): add `ALT DELTA:-n` token to quantify safer portal branch pressure reduction.
  2) Mid-risk Systems/World: ALT selector v2 from current-map reachable portal graph (true lowest-pressure suggestion).
  3) High-risk Novelty: dynamic route mutation event (temporary `SAFE` reroute after hazard clear streak).
- Shipped vertical slice:
  - `src/portal.lua` now computes adaptive alternate-route pressure delta with threat-aware pressure scoring and appends `ALT DELTA` (`ADEL` compact).
  - Existing adaptive `ALT ROUTE` hint retained; compact/full prompts keep parity.
- Verification (PASS):
  - `luac -p src/portal.lua scripts/regression_portal_route_preview.lua scripts/regression_portal_prompt_compact_mode.lua`
  - `lua scripts/regression_portal_route_preview.lua`
  - `lua scripts/regression_portal_prompt_compact_mode.lua`
  - `lua scripts/regression_portal_prompt_token_order.lua`
- Backlog sync:
  - Marked Cycle G adaptive portal hint task done.
  - Added Cycle H injection trio; completed `ALT DELTA` slice, queued ALT selector v2 + ALT token budget/order regression.

## 2026-03-21 05:04 KST — Cycle H follow-up: route-aware ALT selector v2
- Completed backlog item:
  - `Systems/World Team: Route-aware ALT selector v2 (pick lowest-pressure reachable branch among current-map portals, not just one-step fallback)`
- Durable decisions:
  - Adaptive alt-route selection now evaluates all reachable portal targets on the current map and chooses the lowest pressure branch that is strictly safer than the selected route.
  - If no safer reachable tagged route exists, behavior falls back to legacy downgrade mapping (`SPIKE->RISK`, `RISK->SAFE`) to preserve guidance continuity.
  - Added test-only route-tag override hook in `src/portal.lua` (`Portal._setRouteTagOverride`) to keep selector regression deterministic without mutating shipped map metadata.
- Shipped files:
  - `src/portal.lua`
  - `scripts/regression_portal_alt_selector_v2.lua`
  - `POST_RC_BACKLOG.md`
- Verification (PASS):
  - `lua scripts/regression_portal_route_preview.lua`
  - `lua scripts/regression_portal_prompt_compact_mode.lua`
  - `lua scripts/regression_portal_prompt_token_order.lua`
  - `lua scripts/regression_portal_alt_selector_v2.lua`
- Next highest-priority unchecked backlog item:
  - `QA/UX Team: Add portal prompt readability regression for adaptive ALT token budget/order under HIGH threat compact mode`.

## 2026-03-21 05:33 KST — Portal adaptive ALT compact-readability regression
- Closed final unchecked backlog item in `POST_RC_BACKLOG.md` (Cycle H QA/UX readability regression).
- Added `scripts/regression_portal_prompt_adaptive_alt_readability.lua` to enforce HIGH-threat compact prompt readability contract:
  - compact mode selection under constrained budget,
  - adaptive ALT token presence (`ALT`, `ADEL`),
  - token order `ACTION -> ROUTE -> COACH -> PRESSURE -> ALT -> ALT_DELTA`,
  - compact prompt length stays within budget.
- Verification set:
  - `lua scripts/regression_portal_prompt_adaptive_alt_readability.lua`
  - `lua scripts/regression_portal_prompt_compact_mode.lua`
  - `lua scripts/regression_portal_prompt_token_order.lua`
- All checks passed.

## 2026-03-21 05:38 KST — Game Director Cycle I experiment shipped
- All previously tracked ACTION_ITEMS/TASKS were complete; after closing the final Cycle H QA item, initiated required Game Director review cycle.
- Candidate ideas generated:
  1) Low-risk UX: adaptive portal ALT PLAN nudge token,
  2) Mid-risk systems: overclock retreat streak bonus,
  3) High-risk novelty/ops: portal readability drift digest automation.
- Chosen experiment: idea (1).
- Vertical slice implementation:
  - `src/portal.lua`: experiment-gated adaptive nudge copy (`ALT PLAN:LOWER RISK` / `AP:LOW`) under `DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE`.
  - `scripts/regression_portal_alt_plan_nudge.lua`: new regression for detailed+compact nudge token visibility when flag is enabled.
- Safety/rollback: feature is fully off by default; disable by unsetting the env flag.
- Verification: portal prompt regression suite remains green with/without flag.
- Backlog injection updated in `POST_RC_BACKLOG.md` (Cycle I): selected idea marked done; 2 follow-up ideas queued unchecked.

## 2026-03-21 06:03 KST — Retreat Streak Bonus Prototype (Cycle I item 2)
- Completed: `POST_RC_BACKLOG` item `Systems/Combat Team: Prototype overclock retreat streak bonus`.
- Core implementation: `src/overclock_hazard.lua` now tracks consecutive safe disengages and emits one dodge-charge bonus on every 2nd valid streak completion.
- Runtime integration: `main.lua` consumes event, grants 6s temporary dodge via `Player.grantDodgeCharge`, and prints explicit status feedback.
- Regression: `scripts/regression_overclock_hazard.lua` now validates first disengage=0 bonus, second consecutive disengage=+1 bonus.
- Remaining top backlog item: `QA/Systems Team: Add weekly portal prompt readability drift digest (compact/detailed token stats over last N commits)`.

## 2026-03-21 06:33 KST — Weekly portal prompt readability drift digest completed
- Completed backlog item: `QA/Systems Team: Add weekly portal prompt readability drift digest (compact/detailed token stats over last N commits)`.
- Durable decisions:
  - Added `scripts/weekly_portal_prompt_readability_drift.py` to produce weekly digest artifacts (`logs/weekly_portal_prompt_readability_drift.{md,json}`) from recent commit diffs.
  - Digest tracks compact/detailed/shared portal prompt token churn, dominant mode per commit, and window-level net drift.
  - Added regression guardrail `scripts/regression_weekly_portal_prompt_readability_drift.py` (temp-repo fixture with detailed+compact commits).
  - Wired digest + regression into `scripts/run_weekly_sustain.sh` and output manifest.
- Verification set (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`
  - `bash scripts/run_weekly_sustain.sh`
- Next priority item: ACTION_ITEMS/TASKS/POST_RC now fully checked; execute next Game Director review cycle (3 ideas -> choose 1 -> vertical slice).

## 2026-03-21 06:36 KST — Game Director Cycle J executed (3 ideas -> 1 slice)
- Idea slate generated:
  1) Low-risk (chosen): add digest mode-trend token (`MODE TREND:COMPACT|DETAILED|BALANCED`).
  2) Mid-risk: pressure-band drift token from portal prompt pressure score edits.
  3) High-risk: top-token movers section for readability triage.
- Implemented minimal vertical slice:
  - `scripts/weekly_portal_prompt_readability_drift.py` now emits `modeTrend` in JSON and `MODE TREND` line in markdown.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py` now validates `modeTrend` enum + markdown token presence.
- Verification set (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`
- Backlog sync:
  - Marked mode-trend slice done in `POST_RC_BACKLOG.md` (Cycle J).
  - Left two injected follow-up ideas unchecked for next cycle.
- Next priority item: `Systems/World Team: Add pressure-band drift token (PRESSURE BAND:LOW|MID|HIGH)`.

## 2026-03-21 07:01 KST — Game Director Cycle J follow-up slice completed
- Completed item: `Systems/World Team: Add pressure-band drift token (PRESSURE BAND:LOW|MID|HIGH)`.
- Implementation:
  - `scripts/weekly_portal_prompt_readability_drift.py`: added pressure-token aggregation, `pressureBand` classification, `pressureEdits` payload, and markdown `PRESSURE BAND` line.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py`: added assertions for new JSON fields and markdown token.
  - Regenerated `logs/weekly_portal_prompt_readability_drift.{json,md}` with new token.
- Verification (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`
- Progress: POST_RC backlog Cycle J now 2/3 complete; remaining unchecked item is top-token movers section.
- Next priority item: `Design/QA Team: Add digest top-token movers section`.

- Weekly portal prompt readability digest now includes **Top Token Movers** (largest net ± token deltas) with per-token added/removed/net fields in JSON + markdown, improving triage for prompt-copy drift.

## 2026-03-21 07:44 KST — Cycle J closure: top-token movers section
- Completed backlog item: `Design/QA Team: Add digest top-token movers section (largest net ± token deltas) for readability triage`.
- Durable decisions:
  - Weekly digest now tracks per-token edits across all portal prompt tokens and publishes top absolute movers (top 5).
  - Markdown digest adds a dedicated `Top Token Movers (net ±)` section for fast human triage.
  - JSON digest adds `tokenTotals` and `topTokenMovers` fields for tooling consumers.
- Verification set:
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`
- Backlog update: marked final unchecked Cycle J item done in `POST_RC_BACKLOG.md`.
- Next priority item: all tracked backlogs checked; execute next Game Director review cycle (3 ideas -> choose 1 -> vertical slice).
- 2026-03-21 08:03 KST: Game Director Cycle K started and shipped first vertical slice: weekly portal prompt digest now includes `DRIFT RISK:LOW|MID|HIGH` derived from mode-imbalance + pressure churn (`driftRiskSignals.score/imbalance/pressureChurn`); regression coverage extended in `scripts/regression_weekly_portal_prompt_readability_drift.py`.

## 2026-03-21 08:31 KST — Cycle K follow-up (sticky token persistence)
- Shipped: Weekly portal prompt readability digest now computes `stickyTokens` (`count`, `tokens`) where tokens were both added and removed within the window.
- Why: Captures prompt copy churn that net/mover-only signals can hide.
- Verification: Dedicated regression PASS + live digest regeneration PASS.
- Backlog sync: Marked sticky-token item done in `TASKS.md` and `POST_RC_BACKLOG.md`; lane-focus token remains next highest priority.

## 2026-03-21 09:03 KST — Cycle K closure + Cycle L injection
- Completed pending Cycle K item: digest `FOCUS:PORTAL|ALT|PRESSURE|MIXED` token now ships from top-mover family aggregation (`laneFocus`, `laneFocusScores`) in weekly readability digest JSON/markdown.
- Since ACTION_ITEMS/TASKS/POST_RC were fully checked, executed Game Director review cycle (Cycle L):
  1) low-risk UX idea: route-action token from `FOCUS + DRIFT RISK`
  2) mid-risk systems idea: lane-focus streak token
  3) high-risk novelty idea: lane-focus transition token
- Chosen experiment (Cycle L vertical slice): route-action token.
- Shipped: digest now emits `routeAction` + `routeActionReason` in JSON and `ROUTE ACTION:<...>` line in markdown (`PORTAL_AUDIT|ALT_TUNE|PRESSURE_REBASE|BALANCE_PASS|WATCH`).
- Verification set (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Backlog sync:
  - Marked lane-focus token done in `TASKS.md` + `POST_RC_BACKLOG.md` (Cycle K complete).
  - Injected Cycle L tasks in `TASKS.md` + `POST_RC_BACKLOG.md`; marked route-action task done, leaving `FOCUS STREAK` and `FOCUS SHIFT` as next items.

## 2026-03-21 09:35 KST — Cycle L completed + Cycle M launched
- Closed remaining Cycle L backlog: weekly portal prompt digest now emits `FOCUS STREAK` and `FOCUS SHIFT` in both JSON (`focusStreak`, `focusShift`) and markdown.
- Because ACTION_ITEMS/TASKS/POST_RC were fully checked, executed Game Director review cycle:
  - Ideas generated: (1) `FOCUS VOL` volatility token (low risk), (2) `ACTION CONF` confidence token (mid risk), (3) `ANOMALY` pulse sentinel (high risk).
  - Selected experiment: `FOCUS VOL:STEADY|SWING` minimal vertical slice.
- Shipped Cycle M slice: digest now adds `focusVolatility` + `focusVolatilitySignals` and markdown `FOCUS VOL` line based on lane-switch ratio across touched commits.
- Regression updated and passing: `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Backlog sync: Cycle M volatility item marked done; `ACTION CONF` and `ANOMALY` remain queued.

## 2026-03-21 09:36 KST — Cycle M follow-up: route-action confidence token shipped
- Reviewed current sprint state + team tails and generated 3 ideas for this cycle:
  1) Low-risk UX (chosen): `ACTION CONF:LOW|MID|HIGH` from focus-dominance + drift-spread.
  2) Mid-risk systems: anomaly confidence tier (`ANOMALY CONF`) instead of binary pulse.
  3) High-risk novelty: lane-lock sentinel (`LANE LOCK:<lane>x<n>`) for prolonged single-lane drift.
- Implemented minimal vertical slice (#1): weekly portal prompt digest now emits `routeActionConfidence` + `routeActionConfidenceSignals` in JSON and `ACTION CONF` line in markdown.
- Confidence model (reversible): derived from lane-focus dominance ratio, top-vs-second focus spread, and drift spread (`|imbalance-pressureChurn|`).
- Verification (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Commit: `1067216`
- Backlog sync:
  - Marked Cycle M `ACTION CONF` item done in `TASKS.md` + `POST_RC_BACKLOG.md`.
  - Added Cycle N candidates and marked chosen confidence telemetry task validated/done.

## 2026-03-21 10:03 KST — Cycle M anomaly pulse vertical slice
- Scope: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`, `logs/teams/*`.
- Shipped:
  - Added digest-level anomaly classifier `anomaly_pulse_from_signals(...)`.
  - JSON now includes `anomalyPulse` (`ON|OFF`) + `anomalyPulseSignals` (`stickyCount`, `stickyThreshold`, `pressureChurn`, `pressureThreshold`, `spike`).
  - Markdown digest now includes `ANOMALY` row with threshold diagnostics.
  - Regression updated to enforce schema + markdown token presence.
- Verification (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Backlog sync:
  - Marked Cycle M anomaly pulse item done in `TASKS.md` + `POST_RC_BACKLOG.md`.
  - Remaining highest-priority unchecked items: Cycle N `ANOMALY CONF` tier, `LANE LOCK` alert.

## 2026-03-21 10:33 KST — Cycle N anomaly-confidence vertical slice
- Completed highest-priority unchecked item: `ANOMALY CONF:LOW|MID|HIGH` for weekly portal prompt readability digest.
- Implementation:
  - Upgraded anomaly classifier to emit `(anomalyPulse, anomalyConfidence, anomalyPulseSignals)` with richer diagnostics (`triggerCount`, threshold met flags, per-signal gaps, combined gap).
  - Added JSON field `anomalyConfidence` and markdown row `ANOMALY CONF` with compact diagnostics.
  - Extended regression coverage to assert new schema + markdown token.
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md` ✅
- Backlog sync:
  - Marked Cycle N anomaly-confidence item done in `TASKS.md` and `POST_RC_BACKLOG.md`.
  - Next highest open item: `LANE LOCK:<lane>x<n>` alert token.

## 2026-03-21 11:03 KST — Cycle N close: lane-lock alert token shipped
- Closed remaining unchecked Cycle N backlog item by adding digest lane-lock continuity token.
- Shipped in `scripts/weekly_portal_prompt_readability_drift.py`:
  - New JSON fields: `laneLock`, `laneLockSignals` (`threshold`, `armed`, `lane`, `streak`)
  - New markdown row: `LANE LOCK: <lane>x<n>` (or `NONE` when not armed)
  - Arming rule: non-MIXED lane focus with `focusStreak >= 3`.
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Backlog sync:
  - `TASKS.md` Cycle N lane-lock task marked `[x]`
  - `POST_RC_BACKLOG.md` Cycle N lane-lock task marked `[x]`
- Next hook: all ACTION_ITEMS + TASKS + POST_RC_BACKLOG checked; next autonomous cycle should execute Game Director review loop (3 ideas → pick 1 experiment → vertical slice).

## 2026-03-21 11:31 KST — Game Director Cycle O: drift-momentum token shipped
- Trigger: ACTION_ITEMS/TASKS/POST_RC reached all-checked state, so executed Game Director review cycle with 3 candidates:
  1) Low-risk (chosen): `DRIFT MOMENTUM:RISING|COOLING|FLAT`.
  2) Mid-risk: `ACTION GUARD:LOCK|SOFT` from confidence+risk.
  3) High-risk: `FOCUS ENTROPY:LOW|MID|HIGH` from lane score spread.
- Shipped vertical slice:
  - `scripts/weekly_portal_prompt_readability_drift.py` now computes `driftMomentum` + `driftMomentumSignals` (recent/older averages, delta, split counts) from chronological commit-window drift scores.
  - Markdown digest now includes `DRIFT MOMENTUM` line for fast trend triage.
  - Regression extended in `scripts/regression_weekly_portal_prompt_readability_drift.py` for schema + markdown token checks.
- Verification (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Backlog sync:
  - Marked Cycle O drift-momentum item done in `TASKS.md` and `POST_RC_BACKLOG.md`.
  - Remaining Cycle O items: `ACTION GUARD`, `FOCUS ENTROPY`.

## 2026-03-21 12:03 KST — Cycle O: action-guardrail token shipped
- Completed Cycle O item: `ACTION GUARD:LOCK|SOFT` for weekly portal prompt readability digest.
- Implementation (`scripts/weekly_portal_prompt_readability_drift.py`):
  - Added `route_action_guardrail_from_signals(driftRisk, routeActionConfidence)`.
  - Emits JSON: `actionGuard`, `actionGuardSignals`.
  - Emits markdown row: `ACTION GUARD` with compact reason + risk/conf tuple.
  - Arming condition: `driftRisk=HIGH && actionConfidence=LOW` => `LOCK`; else `SOFT`.
- Regression (`scripts/regression_weekly_portal_prompt_readability_drift.py`):
  - Added schema assertions for `actionGuard` and `actionGuardSignals`.
  - Added markdown token assertion for `ACTION GUARD`.
- Verification (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Backlog sync:
  - `TASKS.md` Cycle O action-guardrail item marked `[x]`
  - `POST_RC_BACKLOG.md` Cycle O action-guardrail item marked `[x]`
- Next highest open item: `FOCUS ENTROPY:LOW|MID|HIGH`.

## 2026-03-21 12:31 KST — Cycle O complete, Cycle P injected
- Closed remaining Cycle O item by shipping `FOCUS ENTROPY:LOW|MID|HIGH` in weekly portal prompt readability digest.
- Entropy implementation details:
  - Normalized Shannon entropy over lane-focus scores (`portal/alt/pressure`) with thresholds `LOW <0.34`, `MID <0.67`, else `HIGH`.
  - Added JSON fields: `focusEntropy`, `focusEntropySignals`.
  - Added markdown line: `FOCUS ENTROPY`.
- Because ACTION_ITEMS + TASKS + POST_RC backlog were fully checked, executed Game Director review cycle and injected Cycle P:
  - Low-risk UX: `FOCUS BAL:<n>%` (chosen, implemented this cycle)
  - Mid-risk systems: `PRESSURE LAG:FAST|STABLE|SLOW` (queued)
  - High-risk novelty: `ROUTE SANDBOX:ON` under sustained lane lock (queued)
- `FOCUS BAL` vertical slice shipped:
  - Added JSON fields `focusBalance`, `focusBalanceSignals` and markdown token `FOCUS BAL`.
  - Regression extended for payload schema + markdown token assertion.
- Verification artifacts refreshed:
  - `logs/weekly_portal_prompt_readability_drift.json`
  - `logs/weekly_portal_prompt_readability_drift.md`

## 2026-03-21 13:03 KST — Cycle P pressure-latency token shipped
- Closed highest-priority unchecked item by adding `PRESSURE LAG:FAST|STABLE|SLOW` to weekly portal prompt readability digest.
- Implementation (`scripts/weekly_portal_prompt_readability_drift.py`):
  - Added `pressure_latency_from_signals()` classifier comparing pressure churn (`driftRiskSignals.pressureChurn`) vs drift momentum trend/delta.
  - Added payload fields: `pressureLag`, `pressureLagSignals`.
  - Added markdown row: `PRESSURE LAG` with churn/momentum/|Δ| diagnostics.
- Regression (`scripts/regression_weekly_portal_prompt_readability_drift.py`):
  - Added schema assertions for `pressureLag` + `pressureLagSignals`.
  - Added markdown token assertion for `PRESSURE LAG`.
- Verification (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Backlog sync:
  - `TASKS.md` pressure-latency item marked `[x]`.
  - `POST_RC_BACKLOG.md` pressure-latency item marked `[x]`.
- Next hook: only remaining unchecked item is `ROUTE SANDBOX:ON` prototype behind sustained lane-lock flag.
- 2026-03-21 13:31 KST: Cycle P route-sandbox prototype shipped in weekly portal digest.
- Durable decision: `ROUTE SANDBOX:ON|OFF` is now experiment-gated by `DOTPIO_EXPERIMENT_ROUTE_SANDBOX` and only arms when lane-lock signal is sustained (non-MIXED focus streak >= threshold).
- Digest outputs now include `routeSandbox` + `routeSandboxSignals` JSON fields and markdown `ROUTE SANDBOX` row for operational triage.
- Regression coverage extended in `scripts/regression_weekly_portal_prompt_readability_drift.py`; digest generation remains PASS.
- 2026-03-21 13:31 KST: Game Director Cycle Q executed after all tracked backlogs were checked.
- Idea slate generated (L/M/H): sandbox action-plan token (chosen), sandbox cooloff counter, sandbox lane-target token.
- Shipped vertical slice: digest now emits `SANDBOX PLAN:SIMULATE|PROBE|PREPARE|HOLD` (`routeSandboxPlan`, `routeSandboxPlanSignals`) derived from `ROUTE SANDBOX + ACTION GUARD + DRIFT RISK`.
- Backlog injection updated in `TASKS.md` and `POST_RC_BACKLOG.md` with Cycle Q section; chosen slice marked done and two follow-up ideas queued unchecked.
- 2026-03-21 14:33 KST: Cycle Q cooloff vertical slice shipped for weekly portal prompt digest.
- Durable decision: `SANDBOX COOLOFF:<n>` starts at 1 immediately after an `ON -> OFF` transition, increments while sandbox stays OFF, and resets to 0 when sandbox is ON.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now persists `sandboxCooloff`/`sandboxCooloffSignals` in JSON and emits markdown `SANDBOX COOLOFF` triage line with prior-state context.
- QA evidence: `scripts/regression_weekly_portal_prompt_readability_drift.py` now validates cooloff schema + transition fixtures (`no-prior`, `just-disarmed`, `continuing`) and markdown token presence.
- Next hook: execute remaining Cycle Q backlog item `SANDBOX TARGET:<lane>`.

- 2026-03-21 15:01 KST: Cycle Q completed — weekly portal digest now emits `SANDBOX TARGET:<lane>` (json+markdown), with regression coverage for payload/schema and digest line presence. Enables explicit lane-family routing when route sandbox activates.
- 2026-03-21 15:01 KST: Game Director Cycle R ideation completed. Candidate ideas: (1) SANDBOX TARGET CONF token (low-risk UX/game-feel handoff), (2) TARGET SRC derivation token (mid-risk systems auditability), (3) TARGET SHIFT history token (high-risk novelty for window-over-window churn cues). Selected/implemented #1 as vertical slice with regression + digest artifact refresh.
- 2026-03-21 15:33 KST: Closed Cycle R backlog item `TARGET SRC:LOCK|MIXED|NONE`.
- Weekly portal digest now emits derivation-path audit token as JSON `sandboxTargetSource` and markdown `TARGET SRC`, sourced from sandbox-target resolver signals.
- Durable decision: keep source taxonomy minimal (`LOCK|MIXED|NONE`) to avoid overfitting while preserving operator traceability.
- Verification: py_compile PASS, regression PASS, digest artifact refresh PASS (`logs/weekly_portal_prompt_readability_drift.{json,md}`).
- Next hook: implement remaining unchecked Cycle R item `TARGET SHIFT:<FROM->TO>`.

## 2026-03-21 15:38 KST — Cycle R closure: sandbox target history token
- Completed remaining Cycle R backlog item: `TARGET SHIFT:<FROM->TO>` in weekly portal prompt readability digest.
- Digest now emits JSON fields `sandboxTargetShift`, `sandboxTargetShiftSignals` and markdown row `TARGET SHIFT`.
- Shift semantics compare prior digest `sandboxTarget` to current target; emits stable `X->X` when unchanged and still reports prior-load/change signals for auditability.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 ...` PASS.

## 2026-03-21 16:01 KST — Game Director Cycle S (sandbox readiness)
- Review cycle generated 3 candidates and selected low-risk digest UX/systems slice: `SANDBOX READY:IDLE|PRIMED|ARMED`.
- Durable decision: readiness tier now derives from `ROUTE SANDBOX + SANDBOX TARGET CONF + ACTION GUARD + lane-lock armed` and is emitted in both JSON (`sandboxReadiness`, `sandboxReadinessSignals`) and markdown (`SANDBOX READY`) outputs.
- Backlog injection updated for Cycle S with two queued follow-ups: `ACTION STABILITY` token and flagged `WHAT-IF ALT` hint prototype.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120` passed.

## 2026-03-21 16:33 KST — Cycle S stability slice shipped
- Completed highest-priority unchecked task: `ACTION STABILITY:LOCKED|WATCH` from `ACTION CONF + FOCUS VOL + DRIFT MOMENTUM`.
- Durable rule: emit `LOCKED` only when `(routeActionConfidence in {MID,HIGH}) AND (focusVolatility=STEADY) AND (driftMomentum in {FLAT,COOLING})`; else `WATCH`.
- Artifacts updated:
  - `scripts/weekly_portal_prompt_readability_drift.py` (new classifier + JSON/markdown outputs)
  - `scripts/regression_weekly_portal_prompt_readability_drift.py` (schema + markdown assertions)
  - `logs/weekly_portal_prompt_readability_drift.{json,md}` regenerated
  - `TASKS.md`, `POST_RC_BACKLOG.md` item status set to done
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120` ✅
- Next item: Cycle S `WHAT-IF ALT:<lane> ΔRISK:<n>` flagged prototype.

- 2026-03-21 17:01 KST: Closed final unchecked Cycle S backlog item by adding flag-gated digest token `WHAT-IF ALT:<lane> ΔRISK:<n>` (`DOTPIO_EXPERIMENT_WHAT_IF_ALT`).
  - Code: `scripts/weekly_portal_prompt_readability_drift.py` adds `what_if_alt_from_signals()` and emits `whatIfAlt`/`whatIfAltSignals` in JSON + `WHAT-IF` markdown line.
  - QA: `scripts/regression_weekly_portal_prompt_readability_drift.py` now validates new schema and markdown token presence; regression passes.
  - Artifacts refreshed: `logs/weekly_portal_prompt_readability_drift.json` and `.md` regenerated.
  - Backlog state: `TASKS.md` + `POST_RC_BACKLOG.md` item marked done; all currently listed ACTION_ITEMS/TASKS/POST_RC entries are checked.

## 2026-03-21 17:31 KST — Game Director Cycle T started: WHAT-IF confidence slice shipped
- Trigger: ACTION_ITEMS/TASKS/POST_RC were all checked, so new Game Director cycle was injected.
- Idea slate generated:
  1) **Chosen (low-risk UX):** `WHAT-IF CONF:LOW|MID|HIGH` for alt-lane projection trust.
  2) Mid-risk QA/Systems: `WHAT-IF ALIGN:ALIGNED|DIVERGED`.
  3) High-risk Design/Systems: `WHAT-IF BAND:GAIN|NEUTRAL|LOSS`.
- Shipped vertical slice:
  - `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfConfidence` + `whatIfConfidenceSignals` and markdown line `WHAT-IF CONF`.
  - Confidence model is conservative by default and only reaches HIGH on strong projected risk drop plus non-low route confidence.
- Verification (PASS): py_compile + digest regression + digest artifact refresh.
- Backlog sync: Cycle T `WHAT-IF CONF` marked done in `TASKS.md` and `POST_RC_BACKLOG.md`; two Cycle T follow-ups remain unchecked.
- Cycle T update: weekly portal readability digest now emits `WHAT-IF ALIGN:ALIGNED|DIVERGED` based on `ALT LANE` vs mapped `ROUTE ACTION` lane intent (`PORTAL_AUDIT->PORTAL`, `ALT_TUNE->ALT`, `PRESSURE_REBASE->PRESSURE`, `BALANCE_PASS/WATCH->MIXED`), with JSON fields `whatIfAlign` + `whatIfAlignSignals` and regression coverage in `scripts/regression_weekly_portal_prompt_readability_drift.py`.

## 2026-03-21 18:31 KST — Game Director Cycle U started + first vertical slice shipped
- Trigger: ACTION_ITEMS + TASKS + POST_RC_BACKLOG were fully checked, so Game Director review cycle executed immediately per protocol.
- Idea set generated:
  1) **Chosen (low-risk UX):** `WHAT-IF MAG:SMALL|MED|LARGE` from `|ΔRISK|`.
  2) Mid-risk systems: `WHAT-IF FIT:SAFE|EVEN|TENSE` from projected risk + pressure band.
  3) High-risk novelty: flag-gated `WHAT-IF FALLBACK:<lane>` when alt lane diverges from route action.
- Implemented vertical slice (#1):
  - `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfMagnitude` + `whatIfMagnitudeSignals` and markdown line `WHAT-IF MAG`.
  - Thresholds: SMALL(0-1), MED(2-3), LARGE(>=4); flag-disabled path remains SMALL for stable default signal.
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py`
  - Both PASS; digest artifacts refreshed under `logs/weekly_portal_prompt_readability_drift.{json,md}`.
- Backlog sync:
  - Marked Cycle T `WHAT-IF BAND` done in `TASKS.md` + `POST_RC_BACKLOG.md`.
  - Injected Cycle U tasks into both backlog files; marked and completed `WHAT-IF MAG`.
  - Remaining queued: `WHAT-IF FIT`, `WHAT-IF FALLBACK`.

## 2026-03-21 19:03 KST — Cycle U experiment slice: WHAT-IF FIT
- Shipped `WHAT-IF FIT:SAFE|EVEN|TENSE` in weekly portal prompt readability digest.
- Decision rule: compare projected what-if risk band (from `projectedRisk`) to current `pressureBand`.
  - lower => `SAFE`, equal => `EVEN`, higher => `TENSE` (flag disabled defaults to `EVEN`).
- Artifacts updated:
  - `scripts/weekly_portal_prompt_readability_drift.py`
  - `scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `logs/weekly_portal_prompt_readability_drift.{json,md}` regenerated.
- Regression status: pass.
- Backlog state: Cycle U pressure-fit item marked done in `TASKS.md` + `POST_RC_BACKLOG.md`; remaining unchecked item is fallback-lane token.

## 2026-03-21 19:33 KST — Cycle U what-if fallback token completed
- Closed highest-priority remaining unchecked item in TASKS/POST_RC: `WHAT-IF FALLBACK:<lane>` prototype behind flag.
- Durable behavior added to weekly digest (`scripts/weekly_portal_prompt_readability_drift.py`):
  - New JSON fields: `whatIfFallback`, `whatIfFallbackSignals`.
  - New markdown token: `WHAT-IF FALLBACK`.
  - Rule: if `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK` is enabled and `WHAT-IF ALIGN` is `DIVERGED`, fallback maps to route-action lane (`PORTAL|ALT|PRESSURE`); else `NONE` (or `OFF` when flag disabled).
- Regression coverage extended in `scripts/regression_weekly_portal_prompt_readability_drift.py` for schema + markdown assertions.
- Verification PASS:
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`
- Backlog state: ACTION_ITEMS, TASKS, and POST_RC_BACKLOG are now fully checked. Next autonomous cycle should execute Game Director review loop.

## 2026-03-21 19:36 KST — Game Director Cycle V injected and first slice shipped
- Because ACTION_ITEMS/TASKS/POST_RC reached fully-checked state, executed required Game Director review cycle.
- Candidate ideas generated:
  1) Low-risk UX: `WHAT-IF FALLBACK CONF:LOW|MID|HIGH`
  2) Mid-risk systems: `WHAT-IF FALLBACK FIT:SAFE|EVEN|TENSE`
  3) High-risk novelty: flagged `WHAT-IF FALLBACK WHY:<short>` rationale token
- Selected experiment (vertical slice): idea #1 (`WHAT-IF FALLBACK CONF`).
- Durable implementation:
  - `scripts/weekly_portal_prompt_readability_drift.py` now outputs `whatIfFallbackConfidence` and `whatIfFallbackConfidenceSignals` in JSON.
  - Markdown digest now prints `WHAT-IF FALLBACK CONF` line.
  - Confidence rule combines fallback actionability + divergence state + delta risk + route-action confidence.
- Regression/verification:
  - `scripts/regression_weekly_portal_prompt_readability_drift.py` extended for new schema + markdown assertions.
  - `python3 -m py_compile ...` PASS
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 ...` PASS
- Backlog injection completed:
  - Added Cycle V entries to `TASKS.md` and `POST_RC_BACKLOG.md`.
  - Marked confidence item done; left fallback-fit + fallback-why as next queued items.

## 2026-03-21 20:01 KST — Cycle V fallback pressure-safety token shipped
- Completed next highest-priority unchecked task in `TASKS.md`/`POST_RC_BACKLOG.md`: `WHAT-IF FALLBACK FIT:SAFE|EVEN|TENSE`.
- `scripts/weekly_portal_prompt_readability_drift.py` updates:
  - Added `what_if_fallback_pressure_fit_from_signals(...)`.
  - Added JSON fields `whatIfFallbackFit` + `whatIfFallbackFitSignals`.
  - Added markdown line `WHAT-IF FALLBACK FIT` with pressure/fallback projection context.
  - Extended `whatIfAltSignals` with `imbalance`/`pressureChurn` so fallback projection math is explicit.
- `scripts/regression_weekly_portal_prompt_readability_drift.py` updates:
  - Expanded schema expectations for `whatIfAltSignals`.
  - Added assertions for `whatIfFallbackFit` + signal schema.
  - Added markdown assertion for `WHAT-IF FALLBACK FIT`.
- Verification PASS:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 30 --max-commits 120 --out-json logs/playtests/weekly_portal_prompt_readability_drift.json --out-md logs/playtests/weekly_portal_prompt_readability_drift.md`
- Backlog state: fallback-fit item marked done in `TASKS.md` and `POST_RC_BACKLOG.md`; remaining unchecked item is fallback rationale token (`WHAT-IF FALLBACK WHY:<short>`).
- Weekly portal prompt digest now supports experimental fallback rationale token `WHAT-IF FALLBACK WHY:<short>` (flag: `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_WHY`), with JSON fields `whatIfFallbackWhy` + `whatIfFallbackWhySignals` and regression guardrails for schema/markdown presence.

## 2026-03-21 21:01 KST — Game Director Cycle W started (fallback alignment slice)
- Trigger: ACTION_ITEMS/TASKS/POST_RC were fully checked, so Game Director review cycle executed.
- Idea slate generated:
  1) Low-risk (chosen): `WHAT-IF FALLBACK ALIGN:SYNC|ASYNC` from fallback lane vs lane focus coherence.
  2) Mid-risk: `WHAT-IF FALLBACK MAG:SMALL|MED|LARGE` for rollback impact sizing.
  3) High-risk: flag-gated `WHAT-IF FALLBACK ALT2:<lane>` secondary candidate.
- Implemented vertical slice:
  - Added `whatIfFallbackAlign` + `whatIfFallbackAlignSignals` to weekly digest JSON.
  - Added markdown token line `WHAT-IF FALLBACK ALIGN`.
  - Extended regression coverage in `scripts/regression_weekly_portal_prompt_readability_drift.py` for schema + markdown assertions.
- Verification (PASS): py_compile, regression script, digest artifact refresh.
- Backlog sync: Cycle W alignment task marked done in `TASKS.md` + `POST_RC_BACKLOG.md`; two Cycle W follow-ups remain queued.

## 2026-03-21 21:35 KST — Game Director Cycle W (partial)
- Completed: `WHAT-IF FALLBACK MAG` token (`SMALL|MED|LARGE`) in weekly portal prompt readability digest.
- Added (flagged prototype): `WHAT-IF FALLBACK ALT2:<lane>` secondary candidate lane from lane-focus ranking (`DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_ALT2`).
- Regression updated and passing for new JSON schema + markdown lines.
- Remaining in Cycle W backlog: finish ALT2 prototype task closure criteria in backlog wording.

## 2026-03-21 21:58 KST — Cycle W closed + Cycle X injected
- Closed remaining Cycle W backlog item: `WHAT-IF FALLBACK ALT2` now marked done in `TASKS.md` and `POST_RC_BACKLOG.md`.
- Shipped Cycle X minimal vertical slice (chosen from 3 ideas): ALT2 quality gate in weekly portal digest.
  - `what_if_fallback_alt2_from_signals(...)` now requires a strong, non-ambiguous secondary lane before emitting `ALT2`.
  - New diagnostics in JSON signals: `topScore`, `secondScore`, `minTopScore`, `minGap`.
- Verification (PASS): py_compile, digest regression, and digest artifact regeneration.
- Next queued experiments (Cycle X): `WHAT-IF FALLBACK ALT2 CONF`, `WHAT-IF FALLBACK PLAN`.

## 2026-03-21 22:04 KST — Game Director Cycle X follow-up: ALT2 confidence token
- Closed highest-priority unchecked item in `TASKS.md`/`POST_RC_BACKLOG.md`: `WHAT-IF FALLBACK ALT2 CONF:LOW|MID|HIGH`.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfFallbackAlt2Confidence` + signals from existing ALT2 quality-gate metrics (`topScore`, `secondScore`, `scoreGap`) and writes markdown line `WHAT-IF FALLBACK ALT2 CONF`.
- QA: `scripts/regression_weekly_portal_prompt_readability_drift.py` updated for payload+markdown assertions; regression PASS.
- Remaining unchecked backlog item: `WHAT-IF FALLBACK PLAN:PRIMARY|SECONDARY|HOLD` (next priority).

## 2026-03-21 23:34 KST — Game Director Cycle Y closure (`WHAT-IF SPLIT`)
- Closed the last unchecked TASKS/POST_RC item by shipping `WHAT-IF SPLIT:ON|OFF` in `scripts/weekly_portal_prompt_readability_drift.py`.
- Contract: feature is off by default and guarded by `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT`; `ON` requires dual actionable lanes (`fallback` + `fallbackAlt2`), lane divergence, MID/HIGH confidence on both, and strong projected risk delta (`|ΔRISK| >= 4`).
- Regression: extended `scripts/regression_weekly_portal_prompt_readability_drift.py` with schema assertions (`whatIfSplit`, `whatIfSplitSignals`) and markdown presence assertion (`WHAT-IF SPLIT`), then ran it successfully.
- Backlog sync: marked `WHAT-IF SPLIT` done in both `TASKS.md` and `POST_RC_BACKLOG.md`; action queues are now fully checked and ready for next Game Director idea injection cycle.

## 2026-03-21 23:36 KST — Game Director Cycle Z launched after full backlog clear
- Trigger: ACTION_ITEMS + TASKS + POST_RC backlog reached fully checked state, so immediate Game Director review cycle executed.
- Idea generation (3):
  1) Low-risk UX `WHAT-IF SPLIT CONF:LOW|MID|HIGH`
  2) Mid-risk systems `WHAT-IF SPLIT LANES:<primary>/<secondary>`
  3) High-risk novelty `WHAT-IF SPLIT SAFE:ON` (flagged)
- Selected vertical slice: idea #1 (`WHAT-IF SPLIT CONF`).
- Implementation details:
  - `scripts/weekly_portal_prompt_readability_drift.py`: added `what_if_split_confidence_from_signals(...)`; payload now includes `whatIfSplitConfidence` + `whatIfSplitConfidenceSignals`; markdown now includes `WHAT-IF SPLIT CONF` row.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py`: added schema assertions for split confidence fields and markdown presence check.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` passed.
- Backlog injection/sync:
  - Added Cycle Z section to `TASKS.md` and `POST_RC_BACKLOG.md`.
  - Marked selected item done; left two follow-ups queued (`SPLIT LANES`, `SPLIT SAFE`).

## 2026-03-22 00:03 KST — Game Director Cycle Z progress (`WHAT-IF SPLIT LANES`)
- Closed one of two remaining unchecked Cycle Z items by shipping `WHAT-IF SPLIT LANES:<primary>/<secondary>` in the weekly portal readability digest.
- Implementation details:
  - `scripts/weekly_portal_prompt_readability_drift.py` now derives `whatIfSplitLanes` + `whatIfSplitLanesSignals` from split signals and emits a markdown line `WHAT-IF SPLIT LANES` for compact handoff clarity.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py` now validates the new JSON fields and markdown token presence.
- Backlog sync: marked route-pair token done in both `TASKS.md` and `POST_RC_BACKLOG.md`.
- Remaining priority item: `WHAT-IF SPLIT SAFE:ON` (flagged novelty gate).

## 2026-03-22 00:33 KST — Cycle Z final novelty closure (`WHAT-IF SPLIT SAFE`)
- Closed last unchecked item in `TASKS.md` and `POST_RC_BACKLOG.md`: flag-gated token `WHAT-IF SPLIT SAFE:ON|OFF`.
- Implementation (`scripts/weekly_portal_prompt_readability_drift.py`):
  - Added `what_if_split_safe_from_signals(...)`.
  - Added payload fields `whatIfSplitSafe`, `whatIfSplitSafeSignals`.
  - Added markdown line `WHAT-IF SPLIT SAFE` after `WHAT-IF SPLIT CONF`.
- Safety rule for `ON`: split must be armed, primary fit must be non-escalating (`SAFE|EVEN`), ALT2 confidence gate `MID|HIGH`, and both split confidences >= MID.
- Regression (`scripts/regression_weekly_portal_prompt_readability_drift.py`): schema + markdown assertions added; test run PASS.
- Backlog state: ACTION_ITEMS, TASKS, POST_RC_BACKLOG all fully checked; next run should execute Game Director review cycle (3 ideas -> select 1 -> implement vertical slice).

## 2026-03-22 01:01 KST — Game Director Cycle AA
- Trigger: ACTION_ITEMS + TASKS + POST_RC_BACKLOG were fully checked, so executed mandatory Game Director review cycle.
- Idea slate generated (L/M/H):
  1) `WHAT-IF SPLIT POSTURE` (chosen)
  2) `WHAT-IF SPLIT COOLOFF`
  3) `WHAT-IF SPLIT ESCALATE` (flagged)
- Shipped vertical slice:
  - Added posture classifier `SAFE|WATCH|HOLD` from `whatIfSplit`, `whatIfSplitSafe`, `whatIfSplitConfidence`.
  - Emitted `whatIfSplitPosture` + `whatIfSplitPostureSignals` in JSON and markdown `WHAT-IF SPLIT POSTURE` row.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.

## 2026-03-22 01:35 KST — Cycle AA systems closure (`WHAT-IF SPLIT COOLOFF`)
- Added `what_if_split_cooloff_from_prior(...)` in `scripts/weekly_portal_prompt_readability_drift.py` to persist split cooloff lifecycle across digest windows.
- Digest now emits JSON fields `whatIfSplitCooloff` + `whatIfSplitCooloffSignals` and markdown row `WHAT-IF SPLIT COOLOFF`.
- Rule locked: `ON` => cooloff `0`; prior `ON` then current `OFF` => `1`; continuing `OFF` with prior cooloff => increment.
- Regression expanded in `scripts/regression_weekly_portal_prompt_readability_drift.py` (schema+markdown assertions and direct helper lifecycle tests).
- Backlog sync: `WHAT-IF SPLIT COOLOFF` marked done in `TASKS.md` and `POST_RC_BACKLOG.md`.

## 2026-03-22 03:04 KST — Game Director Cycle AC closure (`WHAT-IF SPLIT ESC STATE`)
- Action/TASK/Post-RC queues were fully checked, so Game Director review cycle executed (3 ideas generated, 1 selected, minimal slice shipped).
- Shipped low-risk UX slice: digest now emits `WHAT-IF SPLIT ESC STATE:ARMED|COOLING|IDLE` with lifecycle signals (`splitEscalate`, `splitEscCool`, `cooling`, `reason`) for faster escalation triage.
- Code changes:
  - `scripts/weekly_portal_prompt_readability_drift.py`: added `what_if_split_escalate_state_from_signals(...)`; payload adds `whatIfSplitEscState` + `whatIfSplitEscStateSignals`; markdown adds `WHAT-IF SPLIT ESC STATE` row.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py`: schema + markdown assertions extended for the new state token.
- Verification passed:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 60`
- Backlog injection (Cycle AC):
  1) ✅ `WHAT-IF SPLIT ESC STATE` (implemented this cycle)
  2) ⏳ `WHAT-IF SPLIT ESC PRESSURE` (flagged follow-up)
  3) ⏳ `WHAT-IF SPLIT ESC RECOVER` (flagged follow-up)

## 2026-03-22 03:41 KST — Game Director Cycle AD vertical slice: split escalation recovery hint
- Idea slate (L/M/H): (1) recovery hint lane token (chosen), (2) recovery confidence token, (3) dual-lane recovery fallback token.
- Shipped: weekly digest now emits WHAT-IF SPLIT ESC RECOVER:<lane> behind DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER; when enabled it suggests the lowest-pressure actionable lane from escalation lane-pair, otherwise OFF/NONE with explicit reason.
- Files: scripts/weekly_portal_prompt_readability_drift.py, scripts/regression_weekly_portal_prompt_readability_drift.py, TASKS.md, POST_RC_BACKLOG.md.
- Verification: python3 -m py_compile + python3 scripts/regression_weekly_portal_prompt_readability_drift.py + digest generation PASS.
- Backlog sync: Cycle AC recovery item closed; Cycle AD injected with recovery-confidence + recovery-alt follow-ups.

## 2026-03-22 04:01 KST — Cycle AD: Split Escalation Recovery Confidence
- Completed: Added WHAT-IF SPLIT ESC RECOVER CONF:LOW|MID|HIGH token derived from recovery lane availability, escalation lifecycle state, lane divergence, and pressure easing context.
- Decision: Confidence stays LOW when recover route is OFF/NONE or state is ARMED; rises to MID/HIGH only during easing (COOLING/IDLE) with actionable/divergent lanes and manageable pressure.
- Files: scripts/weekly_portal_prompt_readability_drift.py, scripts/regression_weekly_portal_prompt_readability_drift.py, TASKS.md, POST_RC_BACKLOG.md
- Verification: python3 scripts/regression_weekly_portal_prompt_readability_drift.py (PASS); python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py (PASS).
- Next: Implement WHAT-IF SPLIT ESC RECOVER ALT:<lane> prototype behind flag for contingency planning.

## 2026-03-22 04:33 KST — Cycle AD closure (`WHAT-IF SPLIT ESC RECOVER ALT`)
- Completed pending Cycle AD backlog item: prototype `WHAT-IF SPLIT ESC RECOVER ALT:<lane>` behind `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_ALT`.
- Implementation: added `what_if_split_escalate_recover_alt_from_signals(...)` in `scripts/weekly_portal_prompt_readability_drift.py`.
- Behavior contract:
  - `OFF` when flag disabled
  - `NONE` when escalation is ARMED / no primary recovery / no secondary candidate
  - otherwise select contingency lane different from primary recovery, ordered by lowest-pressure lane rank.
- Output contract added to digest artifacts:
  - JSON: `whatIfSplitEscRecoverAlt`, `whatIfSplitEscRecoverAltSignals`
  - Markdown: `WHAT-IF SPLIT ESC RECOVER ALT` row
- Regression updated and passing (`scripts/regression_weekly_portal_prompt_readability_drift.py`).

## 2026-03-22 04:41 KST — Game Director Cycle AE (3 ideas -> 1 shipped)
- Idea slate generated:
  1) **Low-risk UX**: `WHAT-IF SPLIT ESC RECOVER ALT CONF` token for fallback trust readability. *(chosen)*
  2) **Mid-risk systems**: `WHAT-IF SPLIT ESC RECOVER PLAN:PRIMARY|ALT|HOLD` decision token.
  3) **High-risk novelty**: flagged `WHAT-IF SPLIT ESC RECOVER WHY:<short>` rationale token.
- Implemented minimal vertical slice (#1):
  - Added `what_if_split_escalate_recover_alt_confidence_from_signals(...)`.
  - Digest emits JSON fields `whatIfSplitEscRecoverAltConfidence` + `whatIfSplitEscRecoverAltConfidenceSignals`.
  - Markdown row `WHAT-IF SPLIT ESC RECOVER ALT CONF` added.
- Verification PASS:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`
- Backlog update: Cycle AE section injected into `TASKS.md` + `POST_RC_BACKLOG.md`; selected item closed, remaining two queued.

## 2026-03-22 05:04 KST — Cycle AE systems closure (`WHAT-IF SPLIT ESC RECOVER PLAN`)
- Closed highest-priority unchecked AE item by shipping `WHAT-IF SPLIT ESC RECOVER PLAN:PRIMARY|ALT|HOLD` in weekly portal readability digest.
- Implementation details:
  - `scripts/weekly_portal_prompt_readability_drift.py` now computes `whatIfSplitEscRecoverPlan` + `whatIfSplitEscRecoverPlanSignals` from `RECOVER` / `RECOVER ALT` availability.
  - Markdown digest now includes `WHAT-IF SPLIT ESC RECOVER PLAN` line with deterministic reason and availability booleans.
- Regression coverage:
  - Extended `scripts/regression_weekly_portal_prompt_readability_drift.py` payload schema + markdown assertions for new plan token.
  - Added resolver unit checks for `PRIMARY` and `HOLD` branches.
  - Verification pass: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Backlog sync: marked `WHAT-IF SPLIT ESC RECOVER PLAN` done in both `TASKS.md` and `POST_RC_BACKLOG.md`.
- Remaining top unchecked item: `WHAT-IF SPLIT ESC RECOVER WHY:<short>` (flag-gated rationale token).

## 2026-03-22 05:34 KST — Cycle AE closure (`WHAT-IF SPLIT ESC RECOVER WHY`)
- Closed final unchecked backlog item by shipping flag-gated rationale token `WHAT-IF SPLIT ESC RECOVER WHY:<short>` in weekly portal readability digest.
- Implementation details:
  - `scripts/weekly_portal_prompt_readability_drift.py`: added `what_if_split_escalate_recover_why_from_signals(...)`, payload fields `whatIfSplitEscRecoverWhy` + `whatIfSplitEscRecoverWhySignals`, and markdown row `WHAT-IF SPLIT ESC RECOVER WHY`.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py`: extended payload schema assertions, markdown presence check, and helper-level flag-on/off behavior tests for recover-why token.
- Verification passed:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py`
- Backlog sync target reached: this token is now complete in both `TASKS.md` and `POST_RC_BACKLOG.md`.

## 2026-03-22 05:38 KST — Game Director Cycle AF (post-clearance injection)
- Trigger: after closing all ACTION_ITEMS/TASKS/POST_RC items, executed mandatory Game Director review cycle.
- Generated ideas:
  1) **Low-risk UX (chosen):** `WHAT-IF SPLIT ESC RECOVER TEMPO:FAST|STEADY|DEFER`.
  2) **Mid-risk systems:** `WHAT-IF SPLIT ESC RECOVER ΔCONF:+n|-n`.
  3) **High-risk novelty (flagged):** `WHAT-IF SPLIT ESC RECOVER VETO:ON`.
- Shipped vertical slice (#1):
  - `scripts/weekly_portal_prompt_readability_drift.py`
    - Added helper `what_if_split_escalate_recover_tempo_from_signals(...)`.
    - Added payload fields `whatIfSplitEscRecoverTempo`, `whatIfSplitEscRecoverTempoSignals`.
    - Added markdown row `WHAT-IF SPLIT ESC RECOVER TEMPO`.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py`
    - Added payload schema assertions + markdown presence assertion for tempo token.
    - Added helper-level regression checks (`FAST` and `DEFER` paths).
- Verification passed:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py`
- Backlog updated:
  - `TASKS.md` + `POST_RC_BACKLOG.md` now include Cycle AF with selected task marked done and two follow-up experiments queued.

## 2026-03-22 07:05 KST — Cycle AG closure
- Completed Post-RC/Game Director Cycle AG tail work by shipping two flagged digest tokens:
  - WHAT-IF SPLIT ESC RECOVER VETO WHY:<short>
  - WHAT-IF SPLIT ESC RECOVER VETO COOLOFF:<n>
- Added deterministic signal builders + payload/markdown emission in weekly portal prompt digest.
- Extended regression suite to validate flag-off/on rationale behavior and veto cooloff rollover after disarm.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Backlog sync: TASKS.md + POST_RC_BACKLOG.md Cycle AG entries moved to done.

## 2026-03-22 07:08 KST — Game Director Cycle AH
- Generated 3 ideas (state, dwell, release cue) and selected **veto state token** for this cycle's minimal vertical slice.
- Shipped `WHAT-IF SPLIT ESC RECOVER VETO STATE:ARMED|COOLING|IDLE` in digest JSON+markdown plus regression coverage.
- Injected new backlog items for remaining AH ideas (dwell + release cue) as unchecked follow-ups.

## 2026-03-22 08:02 KST — Game Director Cycle AI
- Generated 3 ideas: (1) release confidence token, (2) release route token, (3) release timer token.
- Selected experiment: **release confidence token** as minimal vertical slice for immediate operator trust readability.
- Shipped `WHAT-IF SPLIT ESC RECOVER VETO RELEASE CONF:LOW|MID|HIGH` in digest JSON+markdown, with deterministic mapping from release cue/state/dwell.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Backlog injected/updated: Cycle AI keeps remaining unchecked tasks for release route + release timer follow-ups.

## 2026-03-22 08:34 KST — Cycle AI follow-up closure (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE`)
- Closed highest-priority unchecked item by shipping `WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE:<lane>` in weekly portal readability digest.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now derives route token from release-state + recovery plan/lanes and emits payload keys `whatIfSplitEscRecoverVetoReleaseRoute` / `...Signals` plus markdown row `WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE`.
- Regression: extended `scripts/regression_weekly_portal_prompt_readability_drift.py` schema + markdown assertions and helper tests; full regression passed.
- Next priority item remains unchecked: prototype `WHAT-IF SPLIT ESC RECOVER VETO RELEASE TICK:<n>` behind flag.

## 2026-03-22 09:06 KST — Cycle AJ closure (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE`)
- Closed highest-priority unchecked item by shipping `WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE:IDLE|EARLY|MID|LATE` in weekly portal readability digest output.
- Implementation: Added `what_if_split_escalate_recover_veto_release_tick_from_prior` + `...tick_phase_from_signals` wiring to JSON payload and markdown rows in `scripts/weekly_portal_prompt_readability_drift.py`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 -m py_compile ...` both PASS.
- Game Director cycle executed (3 ideas):
  1) Low-risk UX (selected): release pacing phase token (shipped).
  2) Mid-risk systems: release cadence token (`ACCEL|STEADY|DECAY`) from tick deltas.
  3) High-risk novelty (flagged): auto-rearm warning token (`WHAT-IF SPLIT ESC RECOVER VETO REARM:WATCH`).
- Injected backlog (Cycle AJ): cadence token + auto-rearm warning prototype remain open.

- Closed Cycle AJ cadence item: weekly portal readability digest now emits `WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE:ACCEL|STEADY|DECAY` from current-vs-prior release tick deltas.
- Cadence token is schema-covered in JSON (`whatIfSplitEscRecoverVetoReleaseCadence` + `...Signals`) and markdown-covered in regression checks.
- Remaining highest-priority unchecked backlog item is the flag-gated auto-rearm warning prototype (`WHAT-IF SPLIT ESC RECOVER VETO REARM:WATCH`).

## 2026-03-22 09:42 KST — Cycle AK (Game Director)
- Ideation (fun-factor):
  1) Auto-rearm warning cue when release stays late under HIGH pressure.
  2) Recovery route combo token (`primary/alt`) for playful lane-callout readability.
  3) Risk streak meter for consecutive high-pressure veto windows.
- Chosen experiment: #1 (auto-rearm warning) as smallest high-signal vertical slice.
- Hypothesis: Surfacing `WHAT-IF SPLIT ESC RECOVER VETO REARM:WATCH` will reduce operator miss-risk for repeated escalation loops.
- Implemented: New rearm classifier + payload + markdown digest + regression tests.
- Verification: regression PASS, py_compile PASS, weekly digest generation PASS.
- Backlog updated: Cycle AJ rearm prototype marked done; Cycle AK queued (rearm confidence/why/cooloff).

## 2026-03-22 10:04 KST — Cycle AK: auto-rearm confidence token completed
- Shipped `WHAT-IF SPLIT ESC RECOVER VETO REARM CONF:LOW|MID|HIGH` in weekly portal prompt readability digest.
- Added `whatIfSplitEscRecoverVetoRearmConfidence` + `...Signals` to JSON payload and markdown row `WHAT-IF SPLIT ESC RECOVER VETO REARM CONF`.
- Decision: confidence scoring anchors on rearm token + phase/pressure/cadence alignment (`WATCH+LATE+HIGH+STEADY => HIGH`, guarded/suppressed late-high contexts => MID, otherwise LOW).
- Validation passed:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
- Next priority: Cycle AK item 2 — `WHAT-IF SPLIT ESC RECOVER VETO REARM WHY:<short>`.

## 2026-03-22 10:35 KST — Cycle AK: auto-rearm rationale token completed
- Shipped `WHAT-IF SPLIT ESC RECOVER VETO REARM WHY:<short>` behind experiment flag `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_WHY`.
- Decision: rationale copy prioritizes operator triage clarity (`HIGH PRESSURE REARM`, `PRESSURE STAY ALERT`, `NO WATCH CUE`, `LOW CONF HOLD`) and degrades safely to `FLAG OFF` when disabled.
- Added `whatIfSplitEscRecoverVetoRearmWhy` + `...Signals` to digest JSON payload and markdown row `WHAT-IF SPLIT ESC RECOVER VETO REARM WHY`.
- Validation passed: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Next priority: Cycle AK item 3 — `WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF:<n>`.

## 2026-03-22 11:03 KST — Cycle AK: auto-rearm cooloff token completed
- Shipped `WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF:<n>` behind `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF`.
- Added cooloff lifecycle helper to weekly portal readability digest; outputs `whatIfSplitEscRecoverVetoRearmCooloff` + `...Signals` in JSON and markdown digest row.
- Behavior: resets on active `WATCH`, starts at 1 on `WATCH -> OFF` transition, increments while OFF cooldown persists.
- Validation passed: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Backlog sync: Cycle AK final checklist item marked done in `TASKS.md` and `POST_RC_BACKLOG.md`.

## 2026-03-22 11:08 KST — Cycle AL (Game Director review cycle)
- Idea candidates generated:
  1) Low-risk UX: add `WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF STATE:ACTIVE|IDLE`.
  2) Mid-risk systems: add `WHAT-IF SPLIT ESC RECOVER VETO REARM FIT:RELIEF|EVEN|TENSE`.
  3) High-risk novelty: flagged `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE:<short>`.
- Selected + implemented vertical slice: idea #1 (cooloff state token).
- Code + evidence: weekly digest now emits `whatIfSplitEscRecoverVetoRearmCooloffState` and markdown `WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF STATE` line; regression pass confirmed.
- Backlog injection: appended Cycle AL section to `TASKS.md` and `POST_RC_BACKLOG.md`; item #1 completed, #2/#3 queued.

- 2026-03-22 11:33 KST: Closed Cycle AL pressure-relief fit item; weekly digest now emits `WHAT-IF SPLIT ESC RECOVER VETO REARM FIT:RELIEF|EVEN|TENSE` with deterministic cooloff-state + pressure mapping and regression coverage.

## 2026-03-22 12:09 KST — Game Director Cycle AM
- Ideation set:
  1) Low-risk UX: nudge confidence token (NUDGE CONF) for quick trust weighting.
  2) Mid-risk systems: nudge window token (ARMED|COOLING|IDLE) from rearm/cooloff state.
  3) High-risk novelty: flagged nudge rationale token (NUDGE WHY:<short>).
- Chosen experiment: #1 nudge confidence token as minimal vertical slice.
- Shipped: `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE CONF:LOW|MID|HIGH` in digest JSON + markdown.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS; `python3 scripts/weekly_portal_prompt_readability_drift.py` PASS (artifacts updated under `logs/weekly_portal_prompt_readability_drift.{json,md}`).
- Backlog injected: Cycle AM added to TASKS + POST_RC_BACKLOG with item #1 complete and #2/#3 queued.

## 2026-03-22 13:34 KST — Cycle AN nudge drift slice
- Shipped new digest token `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE DRIFT:STABLE|SHIFTING` by comparing current `Nudge WHY` rationale against prior digest window.
- Durable decision: drift is strictly rationale-change based (`STABLE` when unchanged, `SHIFTING` when changed), independent from nudge impact band.
- Added payload fields `whatIfSplitEscRecoverVetoRearmNudgeDrift` and `...Signals` plus markdown status line for operator triage.
- Regression coverage extended for payload schema, markdown token presence, and prior-window drift detection helper behavior.
- Next priority item remains Cycle AN final prototype: `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH:<primary>|<backup>` behind flag.

## 2026-03-22 14:03 KST — Cycle AN coach snapshot prototype
- Shipped new digest prototype token `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH:<primary>|<backup>` behind `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH`.
- Durable decision: coach lane selection honors `RECOVER PLAN` first (ALT preferred when plan=ALT), then falls back to primary/alt actionable lanes; backup lane is emitted only when distinct/actionable.
- Added payload fields `whatIfSplitEscRecoverVetoRearmCoach` + `whatIfSplitEscRecoverVetoRearmCoachSignals` and markdown line for operator triage.
- Regression expanded to assert payload schema and markdown token presence; full weekly portal drift regression passes.

## 2026-03-22 14:06 KST — Cycle AO experiment (selected)
- Generated idea set (low/mid/high):
  - Low-risk UX: add `COACH CONF` token for dual-lane coach trust weighting.
  - Mid-risk systems: add coach posture token (`PRIMARY|BALANCED|BACKUP`) from selected vs fallback lane mix.
  - High-risk novelty: prototype coach rationale token behind flag for adaptive operator coaching.
- Selected experiment: low-risk `COACH CONF` vertical slice to keep digest readability stable while improving triage trust.
- Implemented `whatIfSplitEscRecoverVetoRearmCoachConfidence` + signals and markdown line `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH CONF`.
- Regression suite remains green; AO backlog created with remaining two follow-up tasks.

## 2026-03-22 14:34 KST — Cycle AO follow-up shipped
- Selected in-flight AO item: `COACH MODE` posture token (mid-risk systems/design) to expose whether coach guidance is primary-only, balanced dual-lane, or backup-driven.
- Implemented `whatIfSplitEscRecoverVetoRearmCoachMode` with signals (`coachPrimaryLane`, `coachBackupLane`, reason) and markdown line `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH MODE`.
- Durable decision: posture classification defaults to `PRIMARY` when flag is off or no actionable lane exists, uses `BALANCED` only for distinct actionable primary+backup lanes, and `BACKUP` only when primary is unavailable.
- Regression: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS, including new token + mode branch assertions.
- Next priority remains AO final prototype: `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH WHY:<short>` behind flag.
- 2026-03-22 15:04 KST: Closed remaining AO unchecked item by shipping flag-gated `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH WHY:<short>` (`DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_WHY`) with JSON payload keys `whatIfSplitEscRecoverVetoRearmCoachWhy` + `...Signals` and markdown digest row.
- Regression updated and passing: `scripts/regression_weekly_portal_prompt_readability_drift.py` now asserts markdown presence for `COACH WHY` and validates flag-off/flag-on rationale paths for the new token classifier.
- Backlog sync complete: the item is marked done in both `TASKS.md` and `POST_RC_BACKLOG.md`; ACTION_ITEMS/TASKS/POST_RC are all fully checked, so next cycle should execute Game Director review injection flow.
- 2026-03-22 16:01 KST: Closed AP pressure-fit item by adding weekly digest tokens `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF` and `...COACH HANDOFF FIT` with deterministic mapping (`LOCKED|FLEX|NONE` + pressure -> `SAFE|EVEN|TENSE`).
- Regression `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS after schema and markdown coverage updates.
- Backlog sync: marked done in both `TASKS.md` and `POST_RC_BACKLOG.md`; next highest unchecked item is AP prototype `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF WHY:<short>`. 
- 2026-03-22 16:34 KST: Closed AP final unchecked item by shipping flag-gated `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF WHY:<short>` token.
- Added JSON payload keys `whatIfSplitEscRecoverVetoRearmCoachHandoffWhy` + `...Signals` and markdown digest line `WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF WHY` in `scripts/weekly_portal_prompt_readability_drift.py`.
- Added regression coverage for payload/schema presence, markdown row inclusion, and flag-off/flag-on behavior via `what_if_split_escalate_recover_veto_rearm_coach_handoff_why_from_signals`.
- Backlog sync: marked done in `TASKS.md` and `POST_RC_BACKLOG.md`; next top unchecked item is Cycle AQ `Combat/VFX: BERSERK FX:PULSE`.

## 2026-03-22 17:01 KST — Cycle AQ berserker FX pulse shipped
- Completed highest-priority unchecked item: `BERSERK FX:PULSE` warning token now appears when threat pressure rises for 2+ consecutive turns.
- Durable decision: streak and trigger logic moved into HUD helpers (`updateBerserkerThreatRiseStreak`, `shouldTriggerBerserkerFxPulse`) so main loop stays thin and behavior is regression-testable.
- Runtime integration: main combat loop tracks consecutive positive threat deltas and emits `BERSERK FX:PULSE [THREAT Δ:+n]` when conditions are met.
- Verification: `lua scripts/regression_hud_berserker_counters.lua` PASS; `lua scripts/regression_enemy_behavior_variants.lua` PASS.
- Backlog sync: marked done in both `TASKS.md` and `POST_RC_BACKLOG.md`; next highest unchecked item is route vignette prototype (`ROUTE VIGNETTE:<glyph>`) behind flag.

## 2026-03-22 17:35 KST — Cycle AQ closure + Cycle AR injection
- Closed remaining Cycle AQ prototype by shipping flag-gated portal ASCII vignette token (`ROUTE VIGNETTE:<glyph>`, compact `RV:<glyph>`) via `DOTPIO_EXPERIMENT_ROUTE_VIGNETTE_ASCII`; regression added (`scripts/regression_portal_route_vignette.lua`).
- ACTION_ITEMS/TASKS/POST_RC_BACKLOG reached fully checked state (excluding checklist legend rows), so Game Director review cycle executed immediately.
- Cycle AR idea set generated:
  - Low-risk UX/game-feel: route-vibe coaching token (`ROUTE VIBE:CALM|EDGE|DOOM`).
  - Mid-risk systems/QA: weekly route-vibe drift telemetry snapshot.
  - High-risk novelty: `VIBE CONFLICT:ON` flag when route and threat pacing cues diverge.
- Selected experiment: low-risk route-vibe coaching token vertical slice. Implemented in `src/portal.lua` for detailed+compact prompts (`VIBE:C|E|D` compact), with new regression `scripts/regression_portal_route_vibe.lua`.
- Durable decision: keep route-vibe token always-on (player-facing readability), while keeping ASCII vignette experimental to protect prompt copy budget.
- Backlog injected for Cycle AR in `TASKS.md` + `POST_RC_BACKLOG.md`; route-vibe token marked done, telemetry/conflict-warning tasks remain queued.

## 2026-03-22 18:05 KST — Cycle AR follow-up: route-vibe drift telemetry snapshot
- Completed backlog item: weekly digest now tracks route-vibe drift counts (`CALM|EDGE|DOOM`) as added/removed/net across window.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py`
  - Added per-line vibe counters for detailed (`ROUTE VIBE:*`) + compact (`VIBE:*`) tokens.
  - Added payload block `routeVibeTotals` and markdown sections (`ROUTE VIBE DRIFT`, `Route Vibe Drift (added/removed/net)`).
- Regression coverage updated in `scripts/regression_weekly_portal_prompt_readability_drift.py` (schema + markdown assertions, fixture includes `VIBE:E`).
- Verification: PASS weekly digest regression + PASS route-vibe portal regression.
- Remaining highest-priority unchecked item: prototype `VIBE CONFLICT:ON` behind flag.

## 2026-03-22 18:31 KST — Cycle AR completion: Route-vibe conflict warning prototype
- Completed highest-priority unchecked item: `VIBE CONFLICT:ON` prototype behind flag.
- Implementation (`src/portal.lua`):
  - Added `DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT` gate.
  - Added conflict classifier from route expected tier (SAFE/LOW, RISK/MED, SPIKE/HIGH) vs live threat tier.
  - Conflict emits only on extreme mismatch (tier delta >= 2), producing:
    - Detailed: `VIBE CONFLICT:ON`
    - Compact: `VC:ON`
- Regression added: `scripts/regression_portal_route_vibe_conflict.lua`.
- Verification: PASS route-vibe baseline + new conflict regression + compact-mode regression.
- Backlog state updated from `[~]` to `[x]` in `TASKS.md` and `POST_RC_BACKLOG.md`.

## 2026-03-22 18:36 KST — Cycle AS (Game Director review cycle) shipped
- Generated 3 ideas (low/mid/high risk), selected low-risk vertical slice:
  - Shipped: `VIBE WHY:<vibe>vs<tier>` + compact `VCWHY:<vibe>/<tier>` behind `DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT_REASON`.
- Implementation notes:
  - `src/portal.lua`: reason-flag gate + conflict reason resolver + detailed/compact prompt injection.
  - New regression: `scripts/regression_portal_route_vibe_conflict_reason.lua`.
- Verification: PASS route-vibe baseline, conflict baseline, conflict-reason regression, compact-mode regression.
- Backlog injected (Cycle AS):
  - Completed: conflict rationale token.
  - Pending: `COACH OVERRIDE:DE-ESCALATE`, `VIBE SYNC:+1` prototypes.

## 2026-03-22 19:01 KST — Cycle AS follow-up shipped: conflict-aware coach override
- Completed highest-priority unchecked item from TASKS/POST_RC: `COACH OVERRIDE:DE-ESCALATE` prototype behind `DOTPIO_EXPERIMENT_ROUTE_VIBE_COACH_OVERRIDE`.
- Implementation (`src/portal.lua`):
  - Added coach-override experiment gate helper.
  - Added conflict-aware fallback ALT recompute path (force adaptive ALT resolution when conflict exists but pressure gate previously blocked ALT discovery).
  - Emitted override tokens only when `(VIBE CONFLICT:ON && adaptive ALT exists)`:
    - Detailed: `COACH OVERRIDE:DE-ESCALATE`
    - Compact: `COVR:DEESC`
- Regression coverage: new `scripts/regression_portal_route_vibe_coach_override.lua` + existing conflict/conflict-reason regressions all passing.
- Durable decision: keep de-escalation override strictly conditional on actionable branch availability to avoid false guidance.
- Next highest-priority unchecked backlog item: `VIBE SYNC:+1` prototype behind flag (3 consecutive vibe/threat alignment transitions).

## 2026-03-22 19:34 KST — Cycle AS completion: VIBE SYNC hint prototype shipped
- Completed pending backlog item: `VIBE SYNC:+1` prototype behind `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT`.
- Implementation (`src/portal.lua`):
  - Added route-vibe/threat exact-alignment evaluator.
  - Added consecutive alignment streak tracker persisted across confirmed transitions.
  - Added threshold hint emission on preview/prompt when next transition reaches streak >= 3.
  - Added prompt tokens:
    - Detailed: `VIBE SYNC:+1`
    - Compact: `VS:+1`
- Regression added: `scripts/regression_portal_route_vibe_sync_hint.lua`.
- Verification: PASS sync-hint regression + conflict-reason + coach-override regressions.
- Durable decision: ship as hint-only experiment first; defer actual SRL payout mutation until telemetry validates readability and behavior shift.

## 2026-03-22 19:41 KST — Cycle AT injection + slice complete
- Game Director generated 3 ideas (low/mid/high risk) and selected low-risk slice:
  1) **Selected (low-risk UX/systems):** pre-reward sync chain token (`VIBE CHAIN` / `VSC`).
  2) Mid-risk systems/combat candidate: sync-threshold dodge-charge handoff (`VIBE SYNC DODGE:+1`) [queued].
  3) High-risk design/AI-content candidate: route-vibe snapback warning (`VIBE SNAPBACK:ON`) [queued].
- Shipped: chain token projection in `src/portal.lua` behind `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT`.
- Regression upgraded: `scripts/regression_portal_route_vibe_sync_hint.lua` now validates chain and reset behavior.
- Backlog injected in TASKS/POST_RC as Cycle AT with one completed + two queued tasks.

## 2026-03-22 20:04 KST — Cycle AT sync-threshold dodge handoff shipped
- Completed highest-priority unchecked item in TASKS/POST_RC Cycle AT: `VIBE SYNC DODGE:+1` prototype behind experiment flag.
- Durable decisions:
  - Added `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_DODGE` to gate new reward behavior; default flow remains unchanged when flag is off.
  - `Portal.confirmTransition()` now queues dodge charges only when route-vibe sync threshold (`VIBE SYNC:+1`) actually triggers.
  - Runtime consumes queued charges via `Portal.consumeVibeSyncDodgeCharges()` and grants temporary dodge charges (6s) with explicit DOS status copy.
- Verification set:
  - `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 lua scripts/regression_portal_route_vibe_sync_hint.lua`
  - `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_DODGE=1 lua scripts/regression_portal_route_vibe_sync_dodge.lua`
  - `lua scripts/regression_portal_route_preview.lua`
- Backlog progression: Cycle AT first item moved `[ ] -> [~] -> [x]` in both `TASKS.md` and `POST_RC_BACKLOG.md`.
- Next highest-priority unchecked item: `Prototype route-vibe snapback warning (VIBE SNAPBACK:ON) behind flag on immediate post-sync misalignment`.

## 2026-03-22 20:31 KST — Cycle AT route-vibe snapback warning shipped
- Completed highest-priority unchecked item: `Prototype route-vibe snapback warning (VIBE SNAPBACK:ON) behind flag on immediate post-sync misalignment`.
- Implementation summary:
  - `src/portal.lua` adds `DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK` and emits `VIBE SNAPBACK:ON` (compact `VSB:ON`) only when misalignment occurs immediately after sync-threshold streak.
  - `scripts/regression_portal_route_vibe_snapback.lua` validates trigger window + compact parity + suppression on later mismatches.
- Validation set:
  - `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 lua scripts/regression_portal_route_vibe_snapback.lua`
  - `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 lua scripts/regression_portal_route_vibe_sync_hint.lua`
  - `lua scripts/regression_portal_route_preview.lua`
- Backlog progression: Cycle AT final item moved `[ ] -> [~] -> [x]` in both `TASKS.md` and `POST_RC_BACKLOG.md`.
- Note: `ACTION_ITEMS.md` still contains placeholder tracking row `- [ ] todo`; Game Director auto-cycle trigger deferred until ACTION_ITEMS is explicitly closed or replaced.

## [2026-03-22 21:34 KST] Cycle AU progress — resilience streak shipped
- Completed backlog item: `VIBE RESILIENCE:<n>` behind `DOTPIO_EXPERIMENT_ROUTE_VIBE_RESILIENCE`.
- Implementation:
  - `src/portal.lua`: added resilience flag parser, recovery-streak state, detailed (`VIBE RESILIENCE`) + compact (`VRES`) token rendering.
  - `scripts/regression_portal_route_vibe_resilience.lua`: validates streak progression across two snapback->recovery episodes.
  - `TASKS.md` and `POST_RC_BACKLOG.md`: Cycle AU resilience item moved `[ ] -> [~] -> [x]`.
- Verification:
  - `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_RECOVERY_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_RESILIENCE=1 lua scripts/regression_portal_route_vibe_resilience.lua`
  - `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_RECOVERY_HINT=1 lua scripts/regression_portal_route_vibe_recovery.lua`
  - `DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 lua scripts/regression_portal_route_vibe_snapback.lua`
- Next highest-priority unchecked item: `VIBE DRIFT:WIDE` prototype (conflict + snapback short-window alarm).

## 2026-03-22 21:46 KST — Game Director Cycle AV (forced lane rebalance)
- Coverage check over last 10 completed items by lane showed hard skew: `world/design=10/10 (100%)`, all other lanes `0%`; this breached >40% cap.
- Forced-lane policy applied: selected underrepresented **combat/vfx** experiment instead of another world/design token.
- Shipped minimal vertical slice: new cooldown feedback token `BERSERK FX:FADE [THREAT Δ:<n>]` when sustained rise streak breaks (`>=2` prior streak, non-positive delta, prior threat > 0).
- Verification passed: `lua scripts/regression_hud_berserker_counters.lua`, `lua scripts/regression_enemy_behavior_variants.lua`, `luac -p main.lua src/hud.lua`.
- Backlog injected for cadence balancing: systems/ops `LANE CADENCE:OK|GAP` watchdog + world/design `DRIFT GLYPH` readability prototype.
- Cycle AU high-risk follow-up shipped as flagged prototype: portal transition prompts now emit `VIBE DRIFT:WIDE` (compact `VDR:WIDE`) when route-vibe conflict and snapback co-occur within a short transition window.
- Drift alarm is gated behind `DOTPIO_EXPERIMENT_ROUTE_VIBE_DRIFT_ALARM` and uses bounded transition-age counters (`<=2`) to prevent permanent alert latching.
- Added regression coverage in `scripts/regression_portal_route_vibe_drift_alarm.lua`; existing snapback/conflict regressions remain green.
- Post-RC backlog status updated: Cycle AU drift-alarm prototype marked complete; highest remaining unchecked items are lane cadence watchdog and drift-glyph escalation prototype.

## 2026-03-22 22:34 KST — Cycle AV lane cadence watchdog shipped (systems/ops)
- Completed highest-priority unchecked item: weekly digest lane coverage watchdog token `LANE CADENCE:OK|GAP`.
- Implementation:
  - `scripts/economy_weekly_snapshot.py` now computes trailing-24h lane buckets from team logs (`combat-vfx`, `design-world`, `systems-ops`) and emits structured `laneCadence` data in JSON + digest token line in markdown.
  - `scripts/regression_weekly_snapshot.py` now enforces `laneCadence` schema/token/bucket presence.
- Verification:
  - `python3 scripts/regression_weekly_snapshot.py`
  - `python3 scripts/economy_weekly_snapshot.py`
- Backlog progression: lane cadence item moved `[~] -> [x]` in `TASKS.md` and `POST_RC_BACKLOG.md`.
- Next highest-priority unchecked item: drift alarm escalation glyph prototype (`DRIFT GLYPH:<...>`) in world/design lane.

## 2026-03-22 23:03 KST — Cycle AV completion: drift glyph escalation shipped
- Completed remaining unchecked backlog item in TASKS/POST_RC: route-vibe drift alarm escalation glyph prototype.
- Implementation (`src/portal.lua`):
  - Added experiment flag `DOTPIO_EXPERIMENT_ROUTE_VIBE_DRIFT_GLYPH`.
  - Added escalation resolver using existing conflict/snapback age windows.
  - Added prompt tokens: detailed `DRIFT GLYPH:!|!!|!!!`, compact `DGL:!|!!|!!!`.
- Regression upgraded (`scripts/regression_portal_route_vibe_drift_alarm.lua`) for max/medium glyph assertions.
- Verification: syntax + drift/snapback/preview regressions PASS.
- Backlog status: Cycle AV final unchecked item moved `[~] -> [x]` in both TASKS and POST_RC.

## 2026-03-23 — Cycle AW digest pacing continuity
- Shipped `PACE DRIFT:+n|-n` token in weekly portal readability digest to make `ACTION PACE` trend direction explicit across windows.
- Scoring contract set to BRAKE=-1, STEADY=0, ACCEL=+1 and drift computed as current minus prior snapshot score.
- Digest outputs now include `paceDrift`/`paceDriftSignals` (JSON) and a `PACE DRIFT` markdown row with prior-load visibility.
- Regression updated to lock schema + markdown token + helper edge behavior.

## 2026-03-23 00:37 KST — Cycle AW closure + Cycle AX injected
- Closed final Cycle AW unchecked task: digest now emits `ACTION PACE WHY:<short>` behind `DOTPIO_EXPERIMENT_ACTION_PACE_WHY` with deterministic short rationale mapping.
- Since TASKS + POST_RC were fully checked (actionable queue), executed Game Director review cycle and injected Cycle AX ideas (low/mid/high).
- Selected/implemented Cycle AX minimal vertical slice: `ACTION PACE WINDOW:OPEN|HOLD|CLOSE` derived from `ACTION PACE + PACE DRIFT + ACTION GUARD`.
- Added backlog follow-ups: `ACTION PACE WINDOW CONF` and flagged `ACTION PACE ALT WINDOW:<short>`.
- Verification artifacts PASS: weekly digest regression + digest generation.

## 2026-03-23 01:04 KST — Cycle AX confidence slice shipped
- Completed TASKS/POST_RC item: digest now emits `ACTION PACE WINDOW CONF:LOW|MID|HIGH` from action stability + pace drift continuity.
- Payload/schema now include `actionPaceWindowConfidence` and `actionPaceWindowConfidenceSignals`; markdown digest includes `ACTION PACE WINDOW CONF` row.
- Regression and generator verification PASS:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py`
- Next highest-priority unchecked item remains: flagged fallback token `ACTION PACE ALT WINDOW:<short>`.

## 2026-03-23 01:37 KST — Cycle AY Game Director review + experiment slice
- Review trigger: ACTION_ITEMS + active TASKS queue were fully checked; executed mandatory Game Director cycle.
- Candidate ideas generated:
  1. Low-risk UX: `ACTION PACE ALT WINDOW CONF` token to grade fallback viability under CLOSED primary window.
  2. Mid-risk systems/UX: `ACTION PACE ALT WINDOW FIT` pressure-fit classifier for fallback pacing lanes.
  3. High-risk novelty: `ACTION PACE ALT WINDOW WHY` micro-coach rationale token with compressed handoff copy.
- Selected experiment: Idea #1 (`ACTION PACE ALT WINDOW CONF`) for minimal vertical slice.
- Implementation:
  - Added `action_pace_alt_window_confidence_from_signals()` in `scripts/weekly_portal_prompt_readability_drift.py`.
  - Wired JSON payload fields: `actionPaceAltWindowConfidence`, `actionPaceAltWindowConfidenceSignals`.
  - Added markdown digest line: `ACTION PACE ALT WINDOW CONF`.
  - Expanded regression schema + helper coverage in `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Verification passed:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW=1 python3 scripts/weekly_portal_prompt_readability_drift.py`
- Backlog updates:
  - Cycle AX fallback token completed in both `TASKS.md` + `POST_RC_BACKLOG.md`.
  - Injected Cycle AY with three ideas; completed confidence slice, leaving `FIT` and `WHY` queued.

## 2026-03-23 02:01 KST — Cycle AY fallback fit token shipped
- Closed Cycle AY mid-risk Systems/UX item: added flagged digest token `ACTION PACE ALT WINDOW FIT:SAFE|EVEN|TENSE`.
- New classifier `action_pace_alt_window_fit_from_signals()` maps alternate pace-window actionability + pressure band to fit guidance.
- Payload/schema updated with `actionPaceAltWindowFit` and `actionPaceAltWindowFitSignals`; markdown digest now includes `ACTION PACE ALT WINDOW FIT` row.
- Regression + generation PASS:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT=1 python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 30 --max-commits 50 --out-json logs/playtests/weekly_portal_prompt_readability_drift.json --out-md logs/playtests/weekly_portal_prompt_readability_drift.md`
- Remaining highest-priority unchecked item: `ACTION PACE ALT WINDOW WHY:<short>`.

- 2026-03-23 02:34 KST: Closed final Cycle AY unchecked task by shipping flagged token `ACTION PACE ALT WINDOW WHY:<short>` with payload/schema + markdown wiring in `scripts/weekly_portal_prompt_readability_drift.py`.
- Decision: keep fallback rationale behind `DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY` and map to compact operator verbs (`PROBE NOW`, `ARM SANDBOX`, `PRIMARY HOLD`, `HOLD FALLBACK`) to preserve digest readability.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and flagged digest run (`DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY=1 python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 30 --max-commits 50 --out-json logs/playtests/weekly_portal_prompt_readability_drift.json --out-md logs/playtests/weekly_portal_prompt_readability_drift.md`).
- Backlog state: ACTION_ITEMS/TASKS/POST_RC now fully checked; next run should execute Game Director 3-idea review cycle and inject new tasks.

- 2026-03-23 02:36 KST: Ran Game Director review cycle after all prior backlog items were checked; generated three ideas and selected low-risk UX/systems experiment `ACTION PACE ALT WINDOW URGENCY`.
- Implemented minimal vertical slice in weekly digest: new flagged token `ACTION PACE ALT WINDOW URGENCY:NOW|SOON|LATER` with payload + markdown + regression coverage.
- Injected Cycle AZ backlog tasks (remaining unchecked): `ACTION PACE ALT WINDOW URGENCY Δ:+n|-n` and `ACTION PACE ALT WINDOW STEP:<verb>`.
- Cycle AZ follow-up shipped: weekly portal readability digest now emits `ACTION PACE ALT WINDOW URGENCY Δ:+n|-n` using persisted urgency band scoring (`OFF=0/LATER=1/SOON=2/NOW=3`) against prior digest snapshot.
- First-run behavior for urgency drift is stabilized to `Δ:+0` with `no-prior-urgency-band` reason when prior JSON is missing/unreadable.
- Regression coverage expanded in `scripts/regression_weekly_portal_prompt_readability_drift.py` for markdown token presence and urgency-drift helper behavior (missing-prior + escalation path).

## 2026-03-23 03:36 KST — Closed remaining AZ item + executed BA Game Director cycle
- Completed the last unchecked AZ backlog item by shipping `ACTION PACE ALT WINDOW STEP:<verb>` (flag: `DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP`) with payload/schema + markdown wiring.
- With ACTION_ITEMS/TASKS/POST_RC backlog fully checked (ignoring template tracker line), immediately ran Game Director review cycle:
  1. Low-risk Design/UX: `ACTION PACE ALT WINDOW STEP GLYPH:<sigil>` readability companion
  2. Mid-risk Systems/QA: `ACTION PACE ALT WINDOW STEP Δ:<n>` prior-window drift token
  3. High-risk Combat/VFX: `ACTION PACE ALT WINDOW PULSE:COOL|LIVE|HOT` pressure pulse token
- Selected and shipped Idea #1 as minimal vertical slice in same cycle (`STEP GLYPH`) behind `DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP_GLYPH`.
- Backlog injected for Cycle BA: glyph done, `STEP Δ` and `PULSE` queued.
- Verification: regression suite + weekly digest generator both PASS.

## 2026-03-23 03:41 KST — Cycle BB forced-lane follow-up (combat/vfx)
- Coverage check over the last 10 completed items (from latest summary cycles) showed lane skew above cap: design/ux-heavy cadence exceeded 40%, while combat/vfx remained underrepresented.
- Forced-lane policy applied: selected underrepresented **combat/vfx** experiment and shipped `ACTION PACE ALT WINDOW PULSE:COOL|LIVE|HOT` behind `DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_PULSE`.
- Implementation: added pulse classifier + JSON payload (`actionPaceAltWindowPulse*`) + markdown digest row in `scripts/weekly_portal_prompt_readability_drift.py`; regression schema updated in `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Verification PASS:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_URGENCY=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP_GLYPH=1 DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_PULSE=1 python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 30 --max-commits 50 --out-json logs/playtests/weekly_portal_prompt_readability_drift.json --out-md logs/playtests/weekly_portal_prompt_readability_drift.md`
- Backlog updates: marked BA pulse item done; injected Cycle BB follow-ups (`PULSE Δ`, `ROUTE PULSE LINK`).

- 2026-03-23 04:34 KST: Cycle BB follow-up complete — weekly portal digest now emits `ACTION PACE ALT WINDOW PULSE Δ:+n|-n` with persisted prior-window comparison (`current/prior/loaded/reason`) in JSON+Markdown; regression coverage expanded for schema + delta behavior. Next up: `ROUTE PULSE LINK:SOFT|SHARP` prototype behind flag.

## 2026-03-23 05:04 KST
- Shipped Game Director Cycle BB follow-up vertical slice: `ROUTE PULSE LINK:SOFT|SHARP` (flag: `DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK`) in weekly portal readability digest.
- Token now bridges fallback cadence pulse (`ACTION PACE ALT WINDOW PULSE` + drift + fit) into a portal handoff cue for cross-surface readability.
- Regression extended to validate markdown presence plus JSON schema/enum for `routePulseLink` and `routePulseLinkSignals`.
- Game Director Cycle BC executed: generated 3 ideas, selected and shipped `ROUTE PULSE LINK CONF` token; deferred compact in-run cue + streak telemetry as backlog items.

## 2026-03-23 05:31 KST — Cycle BC compact portal pulse cue shipped
- Completed TASKS/POST_RC unchecked item: `PULSE LINK:S|H` compact portal prompt cue behind `DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_PROMPT`.
- Scope: `src/portal.lua` now adds compact-only token emission (no detailed prompt contract change) and `scripts/regression_portal_prompt_pulse_link.lua` validates high/low pressure token mapping.
- Verification PASS:
  - `lua scripts/regression_portal_prompt_compact_mode.lua`
  - `DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_PROMPT=1 lua scripts/regression_portal_prompt_pulse_link.lua`
- Remaining highest-priority unchecked item: `ROUTE PULSE LINK STREAK:<n>` (Systems/QA weekly digest persistence triage).

- 2026-03-23 06:34 KST: Closed Cycle BD Systems/QA follow-up by shipping `ROUTE PULSE LINK MODE Δ:+n|-n` in weekly digest JSON+markdown.
- Drift token uses prior-window score diff (`IDLE=0`, `SUSTAIN=1`, `SURGE=2`) with explicit signals (`current/prior`, `priorLoaded`, `reason`) for auditability.
- Regression + artifact evidence refreshed and passing: `scripts/regression_weekly_portal_prompt_readability_drift.py`, `scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`.
- Backlog state: `ROUTE PULSE LINK MODE Δ` marked done in `TASKS.md` and `POST_RC_BACKLOG.md`; next unchecked item is flagged compact portal cue `PULSE MODE:I|S|X`.
- 2026-03-23 07:34 KST: Game Director Cycle BE injected (3 ideas) after actionable queues were fully checked; selected low-risk vertical slice `ROUTE PULSE LINK MODE WHY:<short>` and shipped it as a flag-gated digest token.
- New digest contract: JSON emits `routePulseLinkModeWhy` + `routePulseLinkModeWhySignals`, markdown includes `ROUTE PULSE LINK MODE WHY` with mode/link/drift/streak diagnostics (`DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_MODE_WHY`).
- Verification refreshed and passing: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_MODE_WHY=1 python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`.
- Cycle BE backlog now tracks remaining follow-ups: `ROUTE PULSE LINK MODE STREAK:<n>` and flagged detailed prompt parity cue `ROUTE PULSE MODE:IDLE|SUSTAIN|SURGE`.
- 2026-03-23 08:04 KST: Closed Cycle BE Systems/QA item by shipping `ROUTE PULSE LINK MODE STREAK:<n>` across digest windows.
- New digest contract: JSON adds `routePulseLinkModeStabilityStreak` + `routePulseLinkModeStabilityStreakSignals`; markdown adds `ROUTE PULSE LINK MODE STREAK` with current/prior mode context.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Backlog state: Cycle BE now has one unchecked item left — flagged detailed portal pulse-mode cue (`ROUTE PULSE MODE:IDLE|SUSTAIN|SURGE`).
- 2026-03-23 08:31 KST: Closed final unchecked Cycle BE backlog item by shipping flagged detailed portal cue `ROUTE PULSE MODE:IDLE|SUSTAIN|SURGE` in `src/portal.lua` (full-prompt parity with compact mode token).
- Regression upgrade: `scripts/regression_portal_prompt_pulse_mode.lua` now validates both detailed (`ROUTE PULSE MODE:*`) and compact (`PULSE MODE:*`) outputs across HIGH/MED/LOW fixtures.
- Verification PASS: `[PASS] portal detailed+compact pulse-mode prompt regression validated`; `[PASS] portal compact pulse-link prompt regression validated`.
- Backlog state: `TASKS.md` and `POST_RC_BACKLOG.md` Cycle BE items are now fully checked.

## 2026-03-23 09:05 KST — Game Director Cycle BF
- Shipped vertical slice: weekly digest token `ROUTE PULSE LINK MODE FIT:SYNC|WATCH|BREAK|RESET`.
- Durable decision: fit classification should be derived from route pulse mode + drift + stability streak to avoid binary handoff signals.
- Verification locked by regression schema, markdown presence checks, and helper behavior tests.
- Backlog injected: remaining Cycle BF tasks are fit drift token and compact portal cue prototype.

### 2026-03-23 10:31 KST — Cycle BG completion: compact pulse token-priority mode
- Completed backlog item: `Systems/UX Team: Prototype compact prompt token-priority mode (FIT-FIRST|MODE-FIRST) behind flag under strict DOS width budget`.
- Shipped behavior:
  - New flag `DOTPIO_EXPERIMENT_ROUTE_PULSE_TOKEN_PRIORITY` (`FIT-FIRST|MODE-FIRST`) in compact portal prompt pipeline.
  - Under priority-mode flag, pulse token append becomes budget-aware for `PULSE FIT`/`PULSE MODE`; first-priority token is preserved when width is constrained.
  - Without flag, legacy compact ordering/coverage remains unchanged.
- Verification: new token-priority regression + existing pulse mode/fit/flare regressions all pass.
- Next candidate item: run Game Director cycle because ACTION_ITEMS/TASKS/POST_RC are now fully checked.

### 2026-03-23 10:31 KST — Game Director Cycle BH (auto-trigger after full check completion)
- Trigger: `ACTION_ITEMS.md` + `TASKS.md` + `POST_RC_BACKLOG.md` reached fully checked state (Cycle BG closure).
- Candidate ideas generated:
  1. **Low-risk UX/game-feel** — add compact pulse-priority cue (`PRI:F|M`) so strict-budget prompts still expose active token-order policy.
  2. **Mid-risk QA/systems** — add weekly digest token `ROUTE PULSE TOKEN PRIORITY` with drift tracking.
  3. **High-risk design/world** — add `ALT STEP:<SAFE|BAIT|PUSH>` micro-cue in portal prompts for branch-intent flavor.
- Chosen experiment: **Idea #1** (low-risk, reversible, immediate readability impact).
- Vertical slice shipped:
  - `src/portal.lua`: compact prompt now emits `PRI:F|M` when `DOTPIO_EXPERIMENT_ROUTE_PULSE_TOKEN_PRIORITY` is active.
  - `scripts/regression_portal_prompt_pulse_token_priority.lua`: verifies FIT-FIRST and MODE-FIRST cue+drop behavior under constrained budget.
- Backlog injection recorded in `TASKS.md` and `POST_RC_BACKLOG.md` as **Cycle BH** (1 done, 2 queued).

### 2026-03-23 11:12 KST — Cycle BH QA/Systems shipped
- Shipped weekly digest token `ROUTE PULSE TOKEN PRIORITY` with values `FIT-FIRST|MODE-FIRST|OFF`.
- Added drift guard: if configured mode flips but `ROUTE PULSE LINK MODE FIT Δ` is neutral, digest holds prior priority mode for stability.
- Added JSON payload fields: `routePulseTokenPriority`, `routePulseTokenPrioritySignals`.
- Regression coverage updated in `scripts/regression_weekly_portal_prompt_readability_drift.py` (payload schema + markdown line assertions).
- Remaining highest-priority unchecked backlog item: `ALT STEP:<SAFE|BAIT|PUSH>` portal fallback micro-cue prototype.

## 2026-03-23 11:31 KST — Cycle BH completion (Design/World)
- Shipped flagged portal fallback micro-cue: `ALT STEP:<SAFE|BAIT|PUSH>` (`DOTPIO_EXPERIMENT_ALT_STEP_CUE`) in both detailed and compact transition prompts.
- Added resolver semantics to classify fallback intent from pressure/alt-route context (SAFE=strong de-escalation, BAIT=high-pressure soft fallback, PUSH=limited relief fallback).
- Added regression: `scripts/regression_portal_alt_step_cue.lua` and kept ALT token observability in weekly digest by adding `ALT STEP:` token family coverage.
- Verification passes: `regression_portal_alt_step_cue`, `regression_portal_alt_plan_nudge`, `regression_weekly_portal_prompt_readability_drift`.

## 2026-03-23 11:31 KST — Game Director Cycle BI (executed)
- Coverage-driven ideation generated 3 ideas (UX trust token, systems drift token, AI/design rationale token) and selected UX trust token as minimal vertical slice.
- Shipped flagged portal trust micro-cue: `ALT STEP CONF:LOW|MID|HIGH` (`DOTPIO_EXPERIMENT_ALT_STEP_CONF`) paired with `ALT STEP` in detailed+compact prompts.
- Added confidence resolver and weekly digest token observability (`ALT STEP CONF:` in token groups/families).
- New regression: `scripts/regression_portal_alt_step_confidence.lua`; verification suite passes.
- Backlog injected (Cycle BI): remaining tasks are confidence drift token + compact rationale token.
- 2026-03-23 12:06 KST: Closed Cycle BI Systems/QA drift item by shipping `ALT STEP CONF Δ:+n|-n` in weekly portal readability digest.
- Added payload fields `altStepConfidenceDrift` + `altStepConfidenceDriftSignals` and markdown row `ALT STEP CONF Δ` (current/prior confidence score with loaded-state reason).
- Regression coverage extended: markdown contract assertion + `alt_step_confidence_drift_from_prior` behavioral checks in `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Remaining highest-priority unchecked backlog item: `ALT STEP WHY:<short>` (Design/AI Content, flag-gated).

## 2026-03-23 12:36 KST — Game Director Cycle BJ (executed)
- Triggered immediate Game Director review cycle after clearing prior unchecked task; generated 3 ideas (low/mid/high risk) and selected low-risk trust-readability slice.
- Shipped vertical slice: `ALT STEP WHY CONF:LOW|MID|HIGH` behind `DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF` in detailed+compact portal transition prompts.
- Added helper `resolveAltStepWhyConfidence(...)` and kept output deterministic for parser stability.
- Added regression `scripts/regression_portal_alt_step_why_confidence.lua`; paired run with existing `regression_portal_alt_step_why.lua` passes.
- Backlog injection recorded as Cycle BJ (1 done, 2 queued):
  - Done: `ALT STEP WHY CONF`
  - Next: `ALT STEP WHY CONF Δ` (digest drift), `ALT WHY GLYPH` (compact rationale sigil)

## 2026-03-23 13:04 KST — Cycle BJ systems/QA slice shipped
- Shipped `ALT STEP WHY CONF Δ:+n|-n` in weekly portal prompt readability digest (JSON + markdown) with prior-window confidence drift signals.
- Expanded digest token catalog/family coverage to include `ALT STEP WHY CONF:` so lane-focus and token-mover math now account for rationale-confidence token churn.
- Regression status: weekly digest regression + py_compile + digest regeneration PASS.
- Backlog sync: TASKS + POST_RC marked done for the Systems/QA BJ item; next unchecked priority is Design/World `ALT WHY GLYPH:<sigil>` prototype.

## 2026-03-23 14:05 KST — Cycle BK Systems/QA slice completed
- Shipped compact rationale glyph drift digest token: `ALT WHY GLYPH Δ:+n|-n`.
- Added prior-aware drift computation to weekly readability digest (`scripts/weekly_portal_prompt_readability_drift.py`) with JSON fields `altWhyGlyphDrift` + `altWhyGlyphDriftSignals`.
- Regression coverage updated in `scripts/regression_weekly_portal_prompt_readability_drift.py`; markdown digest now emits `ALT WHY GLYPH Δ` line for quick stability triage.
- Backlog sync: marked `ALT WHY GLYPH Δ` item done in `TASKS.md` and `POST_RC_BACKLOG.md`; next unchecked item is `ALT WHY GLYPH MODE:STEADY|SPIKE` prototype.

## 2026-03-23 14:31 KST — Cycle BK follow-up: ALT WHY GLYPH MODE token
- Completed backlog item: `ALT WHY GLYPH MODE:STEADY|SPIKE` behind `DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE`.
- Updated portal prompt rendering (detailed + compact) and regression coverage for glyph-mode token visibility.
- Updated weekly readability digest token catalogs (`TOKEN_GROUPS` / `TOKEN_FAMILIES`) to track `ALT WHY GLYPH MODE` churn.
- Verification: glyph regressions + digest py_compile PASS.
- Follow-up: next unchecked queue item is Systems/QA `ALT WHY GLYPH compact alias drift token` in TASKS/POST_RC.

## 2026-03-23 14:44 KST — Game Director Cycle BL (weekly digest glyph-mode drift)
- Ideas generated: (1) glyph-mode drift token, (2) compact mode alias `AWGM`, (3) glyph-mode confidence tier.
- Selected experiment: (1) `ALT WHY GLYPH MODE Δ:+n|-n` for minimal reversible slice.
- Implemented in weekly digest script + regression; backlog updated with remaining BL queue items.
- Verification: py_compile + weekly drift regression PASS.

## 2026-03-23 15:04 KST — Cycle BL: AWGM compact glyph-mode alias
- Completed backlog slice: compact portal prompt now supports `AWGM:<S|K>` behind `DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_COMPACT`.
- Detailed prompt retains full `ALT WHY GLYPH MODE:<...>` label; compact alias is reversible and flag-gated.
- Updated drift digest token catalogs to include `AWGM:` in compact/alt token families.
- Verification: `regression_portal_alt_why_glyph_compact.lua` + `regression_weekly_portal_prompt_readability_drift.py` PASS.
- Next priority item: `ALT WHY GLYPH MODE CONF:LOW|MID|HIGH` (Systems/QA, Cycle BL).

## 2026-03-23 15:31 KST — Cycle BL complete (glyph-mode confidence)
- Completed backlog item: `ALT WHY GLYPH MODE CONF:LOW|MID|HIGH` in weekly digest.
- Durable decision: confidence stays `LOW` when prior window is unavailable; escalates via drift magnitude + current net activity.
- Implementation files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, backlog tracking docs.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.

## 2026-03-23 15:39 KST — Game Director Cycle BM
- Ideas: (1) CONF drift token, (2) compact confidence alias, (3) confidence rationale micro-token.
- Selected/implemented experiment: (1) `ALT WHY GLYPH MODE CONF Δ:+n|-n` minimal vertical slice.
- New backlog injected: queued items (2) `AWGMC:<L|M|H>` and (3) `ALT WHY GLYPH MODE CONF WHY:<short>`.
- Verification: weekly digest regression PASS.

## 2026-03-23 15:41 KST — Cycle BN forced-lane rebalance (combat/vfx)
- Coverage check over last 10 completed items by lane: `systems/qa=6`, `design/world=4`, `combat/vfx=0`, others `0`; systems exceeded 40% cap.
- Mandatory rebalance applied: selected underrepresented combat/vfx slice.
- Shipped minimal vertical slice: status feed now emits `BERSERK FX:FADE(SOFT|HARD)` based on cooldown severity (`src/hud.lua`, `main.lua`).
- Verification PASS: `lua scripts/regression_hud_berserker_counters.lua`, `lua scripts/regression_enemy_behavior_variants.lua`, `luac -p main.lua src/hud.lua`.
- 24h cadence check: now explicitly covered `combat/vfx` (this slice), `design/world` (BM/BL portal glyph work), and `systems/ops` (digest + cadence watchdog lineages).
- Backlog injected (Cycle BN): queued `VIBE TRAIL:CALM|ASH` (design/world) and `LANE GAP DETAIL` (systems/ops).

## 2026-03-23 16:09 KST — Cycle BM: AWGMC compact confidence alias
- Completed highest-priority unchecked item from TASKS/POST_RC_BACKLOG: `AWGMC:<L|M|H>` compact confidence alias behind flag.
- Implementation:
  - `src/portal.lua`: added `DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_CONF_COMPACT` gate and compact token label switch (`ALT STEP WHY CONF` -> `AWGMC`).
  - `scripts/weekly_portal_prompt_readability_drift.py`: token catalogs/families updated to track `AWGMC:`.
  - `scripts/regression_portal_alt_why_glyph_mode_confidence_compact.lua`: new regression for alias behavior.
- Verification passed:
  - `scripts/regression_portal_alt_why_glyph_compact.lua`
  - `scripts/regression_portal_alt_why_glyph_mode_confidence_compact.lua`
  - `scripts/regression_weekly_portal_prompt_readability_drift.py`
- Next highest-priority unchecked item: `ALT WHY GLYPH MODE CONF WHY:<short>` (Design/AI Content, flag-gated).

## 2026-03-23 16:35 KST — Cycle BM shipped (`ALT WHY GLYPH MODE CONF WHY`)
- Implemented flagged digest micro-token `ALT WHY GLYPH MODE CONF WHY:<short>` via `DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_CONF_WHY`.
- Added rationale derivation from glyph-mode confidence + drift/net signals with deterministic short outputs for triage.
- Extended JSON schema with `altWhyGlyphModeConfidenceWhy` and `altWhyGlyphModeConfidenceWhySignals`.
- Extended markdown digest with `ALT WHY GLYPH MODE CONF WHY` diagnostics row.
- Regression updated and passing: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Next unchecked queue head: BN world token `VIBE TRAIL:CALM|ASH` prototype (flagged) then systems `LANE GAP DETAIL` watchdog row.

## 2026-03-23 17:01 KST — Cycle BN closure (world + systems/ops)
- Closed remaining forced-lane BN items in TASKS/POST_RC:
  - `VIBE TRAIL:CALM|ASH` prototype behind `DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL`.
  - `LANE GAP DETAIL` row in weekly cadence watchdog with combat/vfx last-touch age.
- Runtime integration:
  - `main.lua` now carries short-lived portal cooloff context from berserker fade events (`SOFT -> CALM`, `HARD -> ASH`, 8s window).
  - `src/portal.lua` renders detailed `VIBE TRAIL:*` and compact `VTR:*` token parity when flag is enabled.
- Ops artifact integration:
  - `scripts/economy_weekly_snapshot.py` now emits `laneCadence.laneGapDetail`, `combatVfxLastTouchAgeHours`, and `sourceLatestAgeHours`; markdown includes `LANE GAP DETAIL`.
- Regression/evidence:
  - Added `scripts/regression_portal_vibe_trail.lua`.
  - Updated `scripts/regression_weekly_snapshot.py` for new lane-gap detail contract.
  - PASS: portal vibe-trail regression, baseline route-vibe regression, weekly snapshot regression.

## 2026-03-23 18:04 KST — Cycle BO shipped (`VIBE TRAIL CONF` token-family coverage)
- Completed Systems/QA backlog item: weekly portal readability digest now includes `VIBE TRAIL CONF:` and compact alias `VTC:` in token catalogs/families.
- This makes confidence-token churn visible in token totals/top movers/lane-focus scoring for drift triage.
- Regression updated (`scripts/regression_weekly_portal_prompt_readability_drift.py`) with payload-key assertions for both tokens; PASS.
- Queue head now: Design/AI Content `VIBE TRAIL WHY:<short>` flagged rationale token.
- Closed final unchecked Cycle BO item: portal prompts now emit flag-gated rationale token `VIBE TRAIL WHY:RECOVER|SCAR` (`DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY`) in detailed + compact paths when valid vibe trail context is present.
- ACTION_ITEMS/TASKS/POST_RC actionable queues were fully checked after BO closure, so Game Director Cycle BP executed (3 ideas generated).
- Selected/shipped Cycle BP minimal vertical slice: compact prompt can now emit alias token `VTW:<short>` behind `DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_COMPACT_ALIAS` while detailed mode keeps full `VIBE TRAIL WHY` label.
- Added QA guardrail `scripts/regression_portal_vibe_trail_why_compact_alias.lua`; vibe-trail + weekly digest regressions remain passing.
- Cycle BP backlog injected: next queued items are digest alias churn coverage (`VTW:` + `VIBE TRAIL WHY:`) and flagged rationale-confidence token (`VIBE TRAIL WHY CONF`, compact `VTWC`).

## 2026-03-23 19:01 KST — Cycle BP closure: VTW alias-family churn coverage
- Completed item: `Systems/QA Team: Add weekly digest token family coverage for compact vibe-trail rationale alias churn (VTW + VIBE TRAIL WHY)`.
- Durable decisions:
  - Added alias-family aggregator (`tokenFamilyTotals.vibeTrailWhyAlias`) in weekly digest payload.
  - Added markdown triage lines (`VTW FAMILY CHURN`) + dedicated `Token Family Coverage` section.
  - Regression now asserts new payload schema and markdown presence.
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` PASS
- Follow-up: continue ACTION_ITEMS/TASKS priority with lane-cadence force-flag trigger item.

## 2026-03-23 19:37 KST — Cycle BP closure + Game Director Cycle BQ injection
- Completed queued item: `VIBE TRAIL WHY CONF:LOW|MID|HIGH` with compact alias `VTWC:<L|M|H>` behind `DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF`.
- Runtime prompt updates:
  - detailed: `VIBE TRAIL WHY CONF:<tier>`
  - compact: `VTWC:<L|M|H>`
  - deterministic mapping: `CALM -> MID`, `ASH -> HIGH`.
- Weekly digest updates:
  - token catalogs/families now track `VIBE TRAIL WHY CONF:` + `VTWC:`
  - new alias-family totals key: `vibeTrailWhyConfidenceAlias`
  - markdown triage rows: `VTWC FAMILY CHURN` + token-family coverage line.
- Verification PASS: portal vibe-trail regression, compact-alias regression, weekly digest regression, Lua/Python compile checks.
- Game Director review cycle (BQ):
  - Generated ideas: (1) confidence-alias churn coverage, (2) confidence rail token, (3) confidence micro-rationale token.
  - Chosen minimal vertical slice: (1) confidence-alias churn coverage (implemented).
  - Backlog injected: queued (2) `VIBE TRAIL CONF RAIL:<STEADY|SPIKE>` and (3) `VIBE TRAIL WHY CONF WHY:<short>`.

## 2026-03-23 20:38 KST — Cycle BQ complete: vibe-trail rationale-confidence micro-rationale
- Completed item: Design/AI Content prototype `VIBE TRAIL WHY CONF WHY:<short>` behind `DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF_WHY`.
- Implementation:
  - `src/portal.lua` now emits detailed `VIBE TRAIL WHY CONF WHY:<short>` and compact `VTCW:<short>` whenever `VIBE TRAIL WHY CONF` is available.
  - Added resolver mapping for initial micro-rationale terms (`LOCKED`, `TREND`, fallback tiers).
  - Updated weekly digest token tracking/family churn coverage for `VIBE TRAIL WHY CONF WHY:` + `VTCW:`.
- Verification:
  - `DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF_RAIL=1 lua scripts/regression_portal_vibe_trail.lua`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
- Durable decision: keep micro-rationale token behind flag until churn + readability indicate stable operator value.

- Closed vibe-trail micro-rationale backlog slice: confidence token (`VIBE TRAIL WHY CONF WHY CONF`/`VTCWC`) is now wired through portal prompts and covered by regressions.
- Added flagged rail cue `VIBE TRAIL WHY CONF WHY RAIL:STEADY|SPIKE` with compact alias `VTCWR:S|X` for fast route triage.
- Weekly digest token-family coverage now includes `VTCWC + VIBE TRAIL WHY CONF WHY CONF` churn/coverage metrics.
- TASKS + POST_RC items for micro-rationale confidence, rail, and digest coverage are now marked complete.
