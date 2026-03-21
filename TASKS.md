# TASKS

Last updated: 2026-03-20 17:31 KST

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
- [x] Add overclock HOT hint bounty progress token (`BOUNTY:x/y`) for payout cap readability
- [x] Add overclock READY/CD next-pulse bounty budget hint (`NEXT BOUNTY:0/y`) for reward planning readability
  - [x] Surface token in READY and cooldown hints without changing bounty mechanics
  - [x] Extend overclock hazard regression coverage for READY/CD token visibility

## Next Up (Post-RC hazard readability wave 2)
- [x] Color-code overclock `RISK` tier token in HUD hint (`LOW`=green, `MED`=amber, `HIGH`=red)
  - [x] Expose tier-aware overclock HUD hint color metadata from hazard module
  - [x] Render overclock auxiliary HUD hint with provided tier color while keeping existing default fallback
  - [x] Extend overclock hazard regression coverage for risk-tier color mapping

## Next Up (Post-RC hazard readability wave 3)
- [x] Add compact overclock risk-factor breakdown token in HUD hint (`RISK SRC:Dx+DETy+MOVEz`)
  - [x] Centralize overclock risk-component math helper (`discount`, `detect`, `move`) in hazard module
  - [x] Surface `RISK SRC:Dx+DETy+MOVEz` token in READY/HOT/CD overclock HUD hints
  - [x] Extend overclock hazard regression coverage for risk-factor token visibility

## Next Up (Post-RC hazard readability wave 4)
- [x] Add overclock next-pulse ETA token in READY/CD HUD hints (`NEXT PULSE:<n>s`)
  - [x] Add reusable next-pulse ETA formatter in hazard module for ready/cooldown states
  - [x] Surface token in READY/CD/IMMINENT overclock HUD hints without changing HOT hint payload
  - [x] Extend overclock hazard regression coverage for next-pulse ETA token visibility

## Next Up (Post-RC hazard readability wave 5)
- [x] Add overclock pulse progress token in HUD hints (`PULSE:%`/`RECHARGE:%`)
  - [x] Add reusable pulse/recharge progress formatter helpers in hazard module
  - [x] Surface progress token in HOT + READY/CD/IMMINENT overclock hints with compact DOS copy
  - [x] Extend overclock hazard regression coverage for progress-token visibility/state math

## Next Up (Post-RC hazard readability wave 6)
- [x] Add overclock risk-trend token in HUD hints (`RISK Δ:+n|-n`)
  - [x] Add baseline-vs-current risk delta formatter helper in hazard module
  - [x] Surface `RISK Δ` token in READY/HOT/CD/IMMINENT hints while keeping DOS compact copy stable
  - [x] Extend overclock hazard regression coverage for risk-delta token visibility/sign formatting

## Next Up (Post-RC hazard readability wave 7)
- [x] Add overclock zone-presence token in HUD hints (`ZONE:IN|OUT`)
  - [x] Add zone-presence token helper in hazard module derived from player in-zone state
  - [x] Surface `ZONE` token in READY/HOT/CD/IMMINENT overclock HUD hints with compact DOS copy
  - [x] Extend overclock hazard regression coverage for zone token visibility in inside/outside states

## Next Up (Post-RC hazard readability wave 8)
- [x] Add overclock zone exposure-duration token in HUD hints (`EXPOSED:<n>s`)
  - [x] Track continuous in-zone exposure seconds in hazard runtime state
  - [x] Surface `EXPOSED:<n>s` token in HOT/CD/IMMINENT hints while `ZONE:IN`
  - [x] Extend overclock hazard regression coverage for exposure-token visibility/reset behavior

## Next Up (Post-RC hazard readability wave 9)
- [x] Add overclock exposure commitment-tier token in HUD hints (`COMMIT:LOW|MID|HIGH`)
  - [x] Add exposure-seconds-to-tier helper in hazard module (`LOW <5s`, `MID <12s`, `HIGH >=12s`)
  - [x] Surface `COMMIT:<tier>` token in HOT/CD/IMMINENT hints while `ZONE:IN`
  - [x] Extend overclock hazard regression coverage for commitment-tier progression/reset behavior

## Next Up (Post-RC hazard readability wave 10)
- [x] Add overclock risk-delta color semantics in HUD hint (rising=red, cooling=green)
  - [x] Add delta-aware HUD color resolver in hazard module while preserving base risk-tier fallback
  - [x] Mark retreat state with `RISK Δ:-1` during out-of-zone cooldown for de-escalation readability
  - [x] Extend overclock hazard regression for positive/negative delta color mapping and token expectations
- [x] Add overclock pulse-end relief burst HUD token (`WINDOW:<n>s`) to reward timed disengage
  - [x] Add short post-pulse relief timer state in hazard module
  - [x] Surface compact `WINDOW` token only during out-of-zone cooldown relief window
  - [x] Add regression coverage for relief-token visibility and expiry behavior
- [x] Add overclock exposure dwell-bucket telemetry artifact (`LOW|MID|HIGH`) for tuning
  - [x] Emit per-run dwell bucket counters from hazard runtime state
  - [x] Write compact markdown/json summary under `logs/playtests/`
  - [x] Add regression coverage for telemetry schema + bucket math
- [x] Add multi-run dwell trend combiner artifact (`last N run medians`) for balance review cadence
  - [x] Persist timestamped run dwell artifacts at reset (`overclock_dwell_buckets_run_*.json`)
  - [x] Add combiner script emitting `logs/playtests/overclock_dwell_trend.{md,json}`
  - [x] Add regression coverage for trend window + median math
- [x] Add run-summary overclock commitment profile token (`PROFILE:CAUTIOUS|BALANCED|ALL-IN`) from dwell mix
  - [x] Add profile resolver in run-summary snapshot state
  - [x] Render compact profile token under overclock efficiency line
  - [x] Extend run-summary regression coverage for profile mapping fixture
- [x] Add adaptive portal nudge token experiment behind flag (`ALT PLAN:LOWER RISK` / `AP:LOW`)
  - [x] Gate token behind `DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE` to keep default prompt contract stable
  - [x] Add regression coverage for detailed/compact token visibility when flag enabled

## Next Up (Game Director Injection — 2026-03-21 Cycle K)
- [x] Add digest drift-risk token (`DRIFT RISK:LOW|MID|HIGH`) from compact/detailed imbalance + pressure churn for quick triage
  - [x] Add drift-risk classifier helper in weekly digest script from mode-imbalance + pressure churn signals
  - [x] Surface `driftRisk` + `driftRiskSignals` in JSON and `DRIFT RISK` line in markdown output
  - [x] Extend weekly digest regression coverage for new token/schema assertions
- [x] Add prompt-token persistence token (`STICKY TOKENS:<n>`) counting tokens present in both added/removed sets over window
- [x] Add digest lane-focus token (`FOCUS:PORTAL|ALT|PRESSURE|MIXED`) from top mover families for action routing

## Next Up (Game Director Injection — 2026-03-21 Cycle L)
- [x] Add digest route-action token (`ROUTE ACTION:PORTAL_AUDIT|ALT_TUNE|PRESSURE_REBASE|BALANCE_PASS|WATCH`) from `FOCUS + DRIFT RISK`
- [x] Add lane-focus streak token (`FOCUS STREAK:<n>`) to flag single-lane churn persistence across digest windows
- [x] Add lane-focus transition token (`FOCUS SHIFT:<FROM->TO>`) for weekly routing handoff clarity

## Next Up (Game Director Injection — 2026-03-21 Cycle M)
- [x] Add lane-focus volatility token (`FOCUS VOL:STEADY|SWING`) from lane-switch ratio over touched commits
- [x] Add route-action confidence token (`ACTION CONF:LOW|MID|HIGH`) from focus dominance + drift-risk spread
- [x] Prototype digest anomaly pulse (`ANOMALY:ON`) when sticky token count and pressure churn spike simultaneously

## Next Up (Game Director Injection — 2026-03-21 Cycle N)
- [x] Add route-action confidence telemetry line in markdown + JSON (`ACTION CONF`, confidence signals)
- [x] Add anomaly confidence tier (`ANOMALY CONF:LOW|MID|HIGH`) to avoid binary over-alerting
- [x] Add lane-lock alert token (`LANE LOCK:<lane>x<n>`) for prolonged single-lane drift streaks

## Next Up (Game Director Injection — 2026-03-21 Cycle O)
- [x] Add digest drift-momentum token (`DRIFT MOMENTUM:RISING|COOLING|FLAT`) comparing early-vs-late window risk score averages
- [x] Add route-action guardrail token (`ACTION GUARD:LOCK|SOFT`) when confidence is LOW under HIGH drift risk
- [x] Add lane-focus entropy token (`FOCUS ENTROPY:LOW|MID|HIGH`) from normalized lane score spread

## Next Up (Game Director Injection — 2026-03-21 Cycle P)
- [x] Add focus-balance token (`FOCUS BAL:<n>%`) to weekly digest for quick lane dominance readability
- [x] Add pressure-latency token (`PRESSURE LAG:FAST|STABLE|SLOW`) comparing pressure churn against drift momentum
- [x] Prototype adaptive route sandbox mode (`ROUTE SANDBOX:ON`) behind flag when digest enters sustained lane lock

## Next Up (Game Director Injection — 2026-03-21 Cycle Q)
- [x] Add route-sandbox action-plan token (`SANDBOX PLAN:SIMULATE|PROBE|PREPARE|HOLD`) from `ROUTE SANDBOX + ACTION GUARD + DRIFT RISK`
- [x] Add route-sandbox cooloff token (`SANDBOX COOLOFF:<n>`) counting consecutive non-armed windows after an ON cycle
- [x] Add sandbox lane-target token (`SANDBOX TARGET:<lane>`) to pin which lane-lock family should be tested when sandbox is active

## Next Up (Game Director Injection — 2026-03-21 Cycle R)
- [x] Add sandbox-target confidence token (`SANDBOX TARGET CONF:LOW|MID|HIGH`) for lane-target handoff quality
- [x] Add sandbox-target source token (`TARGET SRC:LOCK|MIXED|NONE`) for quick audit of lane-target derivation path
- [x] Add sandbox-target history token (`TARGET SHIFT:<FROM->TO>`) to highlight lane-target changes across digest windows

## Next Up (Game Director Injection — 2026-03-21 Cycle S)
- [x] Add sandbox readiness tier token (`SANDBOX READY:IDLE|PRIMED|ARMED`) from `ROUTE SANDBOX + TARGET CONF + ACTION GUARD` for faster go/no-go triage
- [x] Add route-action stability token (`ACTION STABILITY:LOCKED|WATCH`) from `ACTION CONF + FOCUS VOL + DRIFT MOMENTUM` to reduce whiplash retunes
- [x] Prototype digest what-if token (`WHAT-IF ALT:<lane> ΔRISK:<n>`) behind flag for low-cost alternate-lane planning

## Next Up (Game Director Injection — 2026-03-21 Cycle T)
- [x] Add what-if confidence token (`WHAT-IF CONF:LOW|MID|HIGH`) so flagged alternate-lane projection trust is glanceable
- [x] Add what-if alignment token (`WHAT-IF ALIGN:ALIGNED|DIVERGED`) comparing `ALT LANE` against current `ROUTE ACTION`
- [x] Add what-if impact-band token (`WHAT-IF BAND:GAIN|NEUTRAL|LOSS`) from projected risk delta

## Next Up (Game Director Injection — 2026-03-21 Cycle U)
- [x] Add what-if delta-magnitude token (`WHAT-IF MAG:SMALL|MED|LARGE`) from `|ΔRISK|` for glanceable planning confidence
- [x] Add what-if pressure-fit token (`WHAT-IF FIT:SAFE|EVEN|TENSE`) combining projected risk with pressure band
- [x] Prototype what-if lane fallback token (`WHAT-IF FALLBACK:<lane>`) behind flag when alternate lane diverges from route action

## Next Up (Game Director Injection — 2026-03-21 Cycle V)
- [x] Add what-if fallback confidence token (`WHAT-IF FALLBACK CONF:LOW|MID|HIGH`) from divergence strength + route confidence
- [x] Add what-if fallback pressure-safety token (`WHAT-IF FALLBACK FIT:SAFE|EVEN|TENSE`) comparing fallback lane projection vs pressure band
- [x] Prototype what-if fallback rationale token (`WHAT-IF FALLBACK WHY:<short>`) behind flag for quick operator context

## Next Up (Game Director Injection — 2026-03-21 Cycle W)
- [x] Add fallback-lane alignment token (`WHAT-IF FALLBACK ALIGN:SYNC|ASYNC`) comparing fallback lane vs digest lane-focus for routing coherence
- [x] Add fallback-delta magnitude band token (`WHAT-IF FALLBACK MAG:SMALL|MED|LARGE`) for rollback impact sizing
- [x] Prototype secondary fallback candidate token (`WHAT-IF FALLBACK ALT2:<lane>`) behind flag for dual-path planning

## Next Up (Game Director Injection — 2026-03-21 Cycle X)
- [x] Add secondary fallback quality gate (emit `ALT2` only when lane-focus score is strong + non-ambiguous)
- [x] Add secondary fallback confidence token (`WHAT-IF FALLBACK ALT2 CONF:LOW|MID|HIGH`) for dual-path trust readability
- [x] Prototype dual-path merge hint token (`WHAT-IF FALLBACK PLAN:PRIMARY|SECONDARY|HOLD`) behind flag

## Next Up (Game Director Injection — 2026-03-21 Cycle Y)
- [x] Add digest merge-plan rationale token (`WHAT-IF PLAN WHY:<short>`) for quick operator context (low-risk UX)
- [x] Add digest merge-plan pressure-fit token (`WHAT-IF PLAN FIT:SAFE|EVEN|TENSE`) from selected merge path projection (mid-risk systems)
- [x] Prototype dual-route split recommendation token (`WHAT-IF SPLIT:ON`) behind flag when primary/secondary plans diverge strongly (high-risk novelty)

## Next Up (Game Director Injection — 2026-03-21 Cycle Z)
- [x] Add split-recommendation confidence token (`WHAT-IF SPLIT CONF:LOW|MID|HIGH`) behind flag for operator trust readability
- [x] Add split route-pair token (`WHAT-IF SPLIT LANES:<primary>/<secondary>`) for handoff clarity in compact digest copy
- [ ] Prototype split-safe-mode token (`WHAT-IF SPLIT SAFE:ON`) behind flag when split suggests non-escalating dual-path plans
