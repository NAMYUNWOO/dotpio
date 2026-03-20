# TASKS

Last updated: 2026-03-20 16:55 KST

See project-level plans:
- `PROJECT_PLAN.md` (milestones/release gates)
- `ACTION_ITEMS.md` (detailed execution backlog)

## Immediate (current sprint focus)
- [x] Implement map item pickup flow for dropped items
  - [x] Add pickup interaction (`G` key) for item on player tile
  - [x] Add inventory-full failure feedback message
  - [x] Mark picked world item as collected/remove from map entity list
  - [x] Add DOS help text for pickup key
  - [x] Add regression test scenario: drop -> pick up -> verify count

- [x] Tune starter build/disassemble loadout for stable smoke-test baseline
  - [x] Seed balanced starter materials/equipment + BUILDER.SRL reserves by folder
  - [x] Add starter loadout regression script (`scripts/regression_starter_loadout.lua`)

- [x] Add economy telemetry baseline for build/disassemble (input/output/SRL envelope)
  - [x] Add shared telemetry writer module (`src/economy_telemetry.lua`)
  - [x] Emit build/disassemble telemetry for lock/fail/success paths in inventory workflow
  - [x] Add telemetry regression script (`scripts/regression_economy_telemetry.lua`)

- [x] Add anti-exploit loop report from economy telemetry
  - [x] Add analyzer module for sliding-window loop profit detection (`src/economy_anti_exploit.lua`)
  - [x] Add report generator script for JSON+Markdown outputs (`scripts/economy_anti_exploit_report.lua`)
  - [x] Add regression script for suspicious loop detection (`scripts/regression_anti_exploit_report.lua`)

- [x] Inventory UX improvements for build workflow
  - [x] Add item split/partial stack feature ("소분")
  - [x] Improve `BUILDER.SRL` use flow UX (action menu + F9 path)
  - [x] Build preview panel: consumed components + expected SRL cost
  - [x] Keep build material consumption explicit in confirmation/status copy

- [x] Economy tuning for low-tier build spam suppression
  - [x] Tune SRL build-cost curve to increase low-tier churn penalties without overtaxing premium recipes
  - [x] Tune disassembly salvage stack/size caps by item size tier for fairness

- [x] Validate map_01~04 progression with portal validator + playtest checklist
  - [x] Run portal wiring validator and capture output artifact
  - [x] Add scripted progression checklist artifact for map_01~04 routes

- [x] Add scripted 30-minute core-loop checklist and pass artifact
  - [x] Add a script that executes the core-loop regression suite and emits a checklist artifact
  - [x] Run it and capture pass evidence under `logs/playtests/`

## Next Up (M2 content sprint)
- [x] Design and implement map_05 layout + portal links
- [x] Design and implement map_06 layout + portal links
- [x] Add at least 3 enemy behavior variants
  - [x] Introduce variant archetypes with distinct combat/movement tendencies
  - [x] Assign variants during spawn so encounters mix behaviors per run
  - [x] Add regression coverage for variant roster/parameters
- [x] Expand AI build output category diversity constraints
  - [x] Add category-balance guardrails so generated build outputs cannot overconcentrate in one category
  - [x] Add regression coverage for diversity constraints
- [x] Add reward table pass for lootbox contents by map tier
  - [x] Add map-tier reward profile selection for lootbox generation
  - [x] Add regression coverage to validate tiered reward weighting envelope

## Next Up (M3 meta progression)
- [x] Add run mission prototype (3 objectives)
  - [x] Track run objective progress (combat/loot/build)
  - [x] Surface objective checklist in HUD
  - [x] Add regression coverage for objective completion flow
- [x] Add unlock flag framework for new build options
  - [x] Add shared unlock-state module with reset/debug helpers
  - [x] Gate advanced build target categories behind unlock flag
  - [x] Trigger unlock on run mission completion and surface status in HUD
  - [x] Add regression coverage for unlock flow + gated category pool

- [x] Add fail-forward reward (currency/material carryover)
  - [x] Compute carryover package from run inventory + mission completion state
  - [x] Apply carryover package on next run start and expose restart status copy
  - [x] Add regression coverage for carryover caps + reward application

- [x] Add summary screen for run result + unlock progress
  - [x] Present per-run mission completion snapshot at reset time
  - [x] Surface unlock status + fail-forward carryover details in summary copy
  - [x] Add regression coverage for summary snapshot formatting/state

## Next Up (M4 UX polish)
- [x] Finalize DOS terminology consistency (Menu/Action/Drop/Disasm/Build)
  - [x] Unify inventory help/status/action copy to canonical terms
  - [x] Keep build material consumption explicit in build preview/confirm/status copy
- [x] Add always-visible lock reason for all disabled actions
  - [x] Surface per-action lock reason text directly in Action Menu rows
  - [x] Add regression coverage for disabled action lock-reason labels
- [x] Add compact onboarding hint flow for first 5 minutes
  - [x] Show concise contextual hint strip without obscuring HUD
  - [x] Rotate/advance hints based on elapsed run time and first interactions
  - [x] Add regression coverage for hint window expiry and progression
- [x] Add keyboard-only usability pass checklist
  - [x] Add scripted keyboard-coverage regression for core inventory controls
  - [x] Generate keyboard-only usability checklist artifact under logs/playtests/

## Next Up (M5 RC/Launch)
- [x] Create RC checklist document
  - [x] Define release gate checklist rows for combat/inventory/build/disasm/portal regressions
  - [x] Link each row to concrete command + artifact path for pass evidence
  - [x] Include blocker triage and release sign-off section
- [x] Execute full regression (combat/inventory/build/disasm/portal)
  - [x] Run RC regression command matrix and record pass/fail evidence
  - [x] Update blocker triage + sign-off rows from latest results
- [x] Fix all critical blockers
  - [x] Re-run blocker-focused regression subset and confirm no critical/high failures
  - [x] Update blocker triage status in RC checklist
- [x] Capture launch screenshots + changelog
- [x] Tag release candidate

## Next Up (M5 Post-RC sustain)
- [x] Weekly SRL telemetry snapshot + rebalance decision log
  - [x] Generate weekly SRL telemetry summary artifact under `logs/`
  - [x] Run anti-exploit report and record rebalance/no-change decision with rationale

- [x] Add week-over-week delta signals to SRL telemetry snapshot output
  - [x] Include deltas vs previous snapshot for telemetry volume and SRL spend
  - [x] Surface delta-aware decision context in markdown/json artifacts
  - [x] Add regression check for weekly snapshot schema including delta fields

- [x] Wire weekly snapshot delta regression into RC/sustain checklist command matrix
  - [x] Add `scripts/regression_weekly_snapshot.py` to RC checklist regression matrix with sustain context
  - [x] Re-run weekly snapshot regression and keep checklist references in sync

- [x] Add one-command weekly sustain runner (snapshot + anti-exploit + regression)
  - [x] Add script entrypoint to execute anti-exploit report, weekly snapshot generation, and weekly regression in one pass
  - [x] Document/validate command usage in RC sustain checklist context

- [x] Add weekly scheduler wiring helper for sustain runner (cron install script + usage)
  - [x] Add helper script to print/apply a weekly cron entry for `scripts/run_weekly_sustain.sh`
  - [x] Add runbook note in RC checklist for scheduler verification workflow

- [x] Add regression coverage for weekly scheduler installer CLI validation/dry-run evidence
  - [x] Add regression script that asserts valid dry-run output and invalid flag rejection for `scripts/install_weekly_sustain_cron.sh`
  - [x] Link regression command into RC/sustain checklist command matrix

- [x] Sync RC checklist sign-off status with actual tagged RC evidence
  - [x] Reconcile `logs/playtests/rc_checklist.md` sign-off rows with lane completion and tag state
  - [x] Add evidence note (tag hash + verification timestamp) for auditable RC closure

- [x] Add safe apply-mode test hook for weekly cron installer
  - [x] Support overriding crontab binary path in installer for sandboxed/mocked apply verification
  - [x] Extend weekly cron installer regression to cover `--apply` upsert behavior without touching host crontab

- [x] Add optional weekly cron log path override for multi-instance deployments
  - [x] Add installer support for `--log-path`/`SUSTAIN_CRON_LOG_PATH` override while keeping default logs path
  - [x] Extend weekly cron installer regression coverage for custom log-path rendering

- [x] Add weekly sustain cron log rotation guard
  - [x] Add a size-based pre-run log rotation helper script for weekly sustain cron logs
  - [x] Wire installer support for configurable max-log-size MB threshold in managed cron entry
  - [x] Extend cron installer regression coverage for log-rotation command rendering

- [x] Add rotated sustain-log retention policy
  - [x] Keep only latest N rotated weekly sustain logs to prevent disk creep
  - [x] Add regression coverage for retention pruning behavior

- [x] Add optional age-based pruning for rotated sustain logs
  - [x] Support max-age-days pruning in rotate helper and cron installer wiring
  - [x] Extend regressions for age-based prune behavior + installer CLI rendering/validation

- [x] Add weekly sustain cron policy audit command
  - [x] Add script to inspect managed DOTPIO weekly cron entry and print parsed rotate/schedule policy
  - [x] Add regression coverage for parse success + managed-entry-missing failure path

- [x] Add machine-readable JSON output mode for weekly sustain cron audit helper
  - [x] Add `--format json` support while keeping default text output stable
  - [x] Extend audit regression for JSON success payload + missing-entry error path

## Next Up (Post-RC gameplay experiments)
- [x] Add mission variety pack with at least +5 objective variants
  - [x] Add rotating mission packs (3 objectives/run) that preserve core loop readability
  - [x] Add new objective variants for higher-intensity kill/pickup/build cadence plus search/inventory planning beats
  - [x] Add regression coverage for mission-pack rotation + objective catalog floor
- [x] Add mission momentum bonus payout experiment (partial SRL reward per objective completion streak)
- [x] Add berserker desperation readability telegraph (HUD + status feed)
  - [x] Expose one-shot `justEnteredDesperation` transition signal in enemy AI state sync
  - [x] Emit DOS combat status warning when visible berserker first enrages
  - [x] Surface active desperate berserker count in HUD
  - [x] Extend enemy behavior regression for desperation transition signal edge
- [x] Add pre-lunge telegraph for berserker desperation attacks (one-turn warning before boosted hit)
- [x] Add one-turn post-lunge recovery window for berserker desperation chain (readability/fairness follow-up)
- [x] Add HUD threat-strip counter for active berserker recovery windows
- [x] Add mission lane-switch variety bonus preview hint in HUD metadata (`NEXT:<lane> +1`)
- [x] Track and surface mission lane-switch variety bonus count in HUD/run-summary (`VAR:<n>`)
- [x] Add weighted berserker threat index in HUD threat strip (`THREAT:<n>`)
  - [x] Weight active desperate berserkers + primed lunges + recovery windows into one compact pressure score
  - [x] Surface `THREAT:<n>` in HUD combat strip without hiding existing counters
  - [x] Extend HUD threat regression coverage for weighted index math
- [x] Add berserker threat-tier label in HUD (`THREAT LVL:LOW|MED|HIGH`)
  - [x] Map weighted threat score to stable tier thresholds for fast readability
  - [x] Surface tier label near `THREAT:<n>` without cluttering existing counters
  - [x] Extend HUD threat regression coverage for tier mapping edge-cases
- [x] Color-code berserker threat-tier label in HUD (`LOW`=green, `MED`=amber, `HIGH`=red)
  - [x] Add tier-to-color resolver helper in HUD module
  - [x] Render threat line using tier-specific color while preserving DOS compact text layout
  - [x] Extend HUD threat regression coverage for tier color mapping
- [x] Add compact berserker threat-formula legend in HUD/combat status (`THREAT = BERSERK + 2*LUNGE + RECOVER`)
  - [x] Add reusable HUD formatter for weighted threat breakdown text
  - [x] Surface formula hint in berserker enrage status feed copy for quick onboarding
  - [x] Extend HUD threat regression coverage for formula-string stability
- [x] Add turn-over-turn berserker threat delta indicator in HUD (`THREAT Δ:+n|-n`)
  - [x] Add HUD threat delta helpers for signed score change math/copy
  - [x] Render color-coded delta row beneath threat tier in combat strip
  - [x] Extend HUD threat regression coverage for delta formatting edge-cases
- [x] Add threat-aware onboarding micro-tip after first build (`COMBAT TIP` until first berserker threat event)
  - [x] Extend onboarding hint state/events with `threat` milestone
  - [x] Mark milestone from berserker enrage/lunge signals in runtime loop
  - [x] Extend onboarding regression coverage for threat-tip progression

## Next Up (Game Director experiment candidates)
- [x] Add mission-chain pressure breaker bonus (complete objective during `THREAT Δ:+` turn grants temporary dodge charge)
- [x] Add map hazard overclock rooms (high-risk interactable gives short burst SRL discounts + enemy aggro spike)
- [x] Add overclock hazard countdown readability pass (active pulse + cooldown seconds in HUD hint)
- [x] Add overclock aggro-pressure legend in active HUD hint (`AGGRO DET:+n MOVE:+m%`)
- [x] Add overclock pulse-imminent warning in cooldown HUD hint when standing inside hazard zone (`IMMINENT:<n>s`)
- [x] Add overclock hot-zone kill bounty reward (+BUILDER.SRL per kill, pulse-capped)
  - [x] Add hazard config knobs for kill bounty payout/cap (`killBonusPerKill`, `killBonusPulseCap`)
  - [x] Award bonus SRL when kills occur during active in-zone overclock pulse
  - [x] Extend overclock hazard regression coverage for bounty payout + pulse cap
- [ ] Add overclock HOT hint bounty progress token (`BOUNTY:x/y`) for payout cap readability
