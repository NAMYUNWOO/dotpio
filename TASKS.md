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

## Next Up (Game Director Injection - 2026-03-21 Cycle K)
- [x] Add digest drift-risk token (`DRIFT RISK:LOW|MID|HIGH`) from compact/detailed imbalance + pressure churn for quick triage
  - [x] Add drift-risk classifier helper in weekly digest script from mode-imbalance + pressure churn signals
  - [x] Surface `driftRisk` + `driftRiskSignals` in JSON and `DRIFT RISK` line in markdown output
  - [x] Extend weekly digest regression coverage for new token/schema assertions
- [x] Add prompt-token persistence token (`STICKY TOKENS:<n>`) counting tokens present in both added/removed sets over window
- [x] Add digest lane-focus token (`FOCUS:PORTAL|ALT|PRESSURE|MIXED`) from top mover families for action routing

## Next Up (Game Director Injection - 2026-03-21 Cycle L)
- [x] Add digest route-action token (`ROUTE ACTION:PORTAL_AUDIT|ALT_TUNE|PRESSURE_REBASE|BALANCE_PASS|WATCH`) from `FOCUS + DRIFT RISK`
- [x] Add lane-focus streak token (`FOCUS STREAK:<n>`) to flag single-lane churn persistence across digest windows
- [x] Add lane-focus transition token (`FOCUS SHIFT:<FROM->TO>`) for weekly routing handoff clarity

## Next Up (Game Director Injection - 2026-03-21 Cycle M)
- [x] Add lane-focus volatility token (`FOCUS VOL:STEADY|SWING`) from lane-switch ratio over touched commits
- [x] Add route-action confidence token (`ACTION CONF:LOW|MID|HIGH`) from focus dominance + drift-risk spread
- [x] Prototype digest anomaly pulse (`ANOMALY:ON`) when sticky token count and pressure churn spike simultaneously

## Next Up (Game Director Injection - 2026-03-21 Cycle N)
- [x] Add route-action confidence telemetry line in markdown + JSON (`ACTION CONF`, confidence signals)
- [x] Add anomaly confidence tier (`ANOMALY CONF:LOW|MID|HIGH`) to avoid binary over-alerting
- [x] Add lane-lock alert token (`LANE LOCK:<lane>x<n>`) for prolonged single-lane drift streaks

## Next Up (Game Director Injection - 2026-03-21 Cycle O)
- [x] Add digest drift-momentum token (`DRIFT MOMENTUM:RISING|COOLING|FLAT`) comparing early-vs-late window risk score averages
- [x] Add route-action guardrail token (`ACTION GUARD:LOCK|SOFT`) when confidence is LOW under HIGH drift risk
- [x] Add lane-focus entropy token (`FOCUS ENTROPY:LOW|MID|HIGH`) from normalized lane score spread

## Next Up (Game Director Injection - 2026-03-21 Cycle P)
- [x] Add focus-balance token (`FOCUS BAL:<n>%`) to weekly digest for quick lane dominance readability
- [x] Add pressure-latency token (`PRESSURE LAG:FAST|STABLE|SLOW`) comparing pressure churn against drift momentum
- [x] Prototype adaptive route sandbox mode (`ROUTE SANDBOX:ON`) behind flag when digest enters sustained lane lock

## Next Up (Game Director Injection - 2026-03-21 Cycle Q)
- [x] Add route-sandbox action-plan token (`SANDBOX PLAN:SIMULATE|PROBE|PREPARE|HOLD`) from `ROUTE SANDBOX + ACTION GUARD + DRIFT RISK`
- [x] Add route-sandbox cooloff token (`SANDBOX COOLOFF:<n>`) counting consecutive non-armed windows after an ON cycle
- [x] Add sandbox lane-target token (`SANDBOX TARGET:<lane>`) to pin which lane-lock family should be tested when sandbox is active

## Next Up (Game Director Injection - 2026-03-21 Cycle R)
- [x] Add sandbox-target confidence token (`SANDBOX TARGET CONF:LOW|MID|HIGH`) for lane-target handoff quality
- [x] Add sandbox-target source token (`TARGET SRC:LOCK|MIXED|NONE`) for quick audit of lane-target derivation path
- [x] Add sandbox-target history token (`TARGET SHIFT:<FROM->TO>`) to highlight lane-target changes across digest windows

## Next Up (Game Director Injection - 2026-03-21 Cycle S)
- [x] Add sandbox readiness tier token (`SANDBOX READY:IDLE|PRIMED|ARMED`) from `ROUTE SANDBOX + TARGET CONF + ACTION GUARD` for faster go/no-go triage
- [x] Add route-action stability token (`ACTION STABILITY:LOCKED|WATCH`) from `ACTION CONF + FOCUS VOL + DRIFT MOMENTUM` to reduce whiplash retunes
- [x] Prototype digest what-if token (`WHAT-IF ALT:<lane> ΔRISK:<n>`) behind flag for low-cost alternate-lane planning

## Next Up (Game Director Injection - 2026-03-21 Cycle T)
- [x] Add what-if confidence token (`WHAT-IF CONF:LOW|MID|HIGH`) so flagged alternate-lane projection trust is glanceable
- [x] Add what-if alignment token (`WHAT-IF ALIGN:ALIGNED|DIVERGED`) comparing `ALT LANE` against current `ROUTE ACTION`
- [x] Add what-if impact-band token (`WHAT-IF BAND:GAIN|NEUTRAL|LOSS`) from projected risk delta

## Next Up (Game Director Injection - 2026-03-21 Cycle U)
- [x] Add what-if delta-magnitude token (`WHAT-IF MAG:SMALL|MED|LARGE`) from `|ΔRISK|` for glanceable planning confidence
- [x] Add what-if pressure-fit token (`WHAT-IF FIT:SAFE|EVEN|TENSE`) combining projected risk with pressure band
- [x] Prototype what-if lane fallback token (`WHAT-IF FALLBACK:<lane>`) behind flag when alternate lane diverges from route action

## Next Up (Game Director Injection - 2026-03-21 Cycle V)
- [x] Add what-if fallback confidence token (`WHAT-IF FALLBACK CONF:LOW|MID|HIGH`) from divergence strength + route confidence
- [x] Add what-if fallback pressure-safety token (`WHAT-IF FALLBACK FIT:SAFE|EVEN|TENSE`) comparing fallback lane projection vs pressure band
- [x] Prototype what-if fallback rationale token (`WHAT-IF FALLBACK WHY:<short>`) behind flag for quick operator context

## Next Up (Game Director Injection - 2026-03-21 Cycle W)
- [x] Add fallback-lane alignment token (`WHAT-IF FALLBACK ALIGN:SYNC|ASYNC`) comparing fallback lane vs digest lane-focus for routing coherence
- [x] Add fallback-delta magnitude band token (`WHAT-IF FALLBACK MAG:SMALL|MED|LARGE`) for rollback impact sizing
- [x] Prototype secondary fallback candidate token (`WHAT-IF FALLBACK ALT2:<lane>`) behind flag for dual-path planning

## Next Up (Game Director Injection - 2026-03-21 Cycle X)
- [x] Add secondary fallback quality gate (emit `ALT2` only when lane-focus score is strong + non-ambiguous)
- [x] Add secondary fallback confidence token (`WHAT-IF FALLBACK ALT2 CONF:LOW|MID|HIGH`) for dual-path trust readability
- [x] Prototype dual-path merge hint token (`WHAT-IF FALLBACK PLAN:PRIMARY|SECONDARY|HOLD`) behind flag

## Next Up (Game Director Injection - 2026-03-21 Cycle Y)
- [x] Add digest merge-plan rationale token (`WHAT-IF PLAN WHY:<short>`) for quick operator context (low-risk UX)
- [x] Add digest merge-plan pressure-fit token (`WHAT-IF PLAN FIT:SAFE|EVEN|TENSE`) from selected merge path projection (mid-risk systems)
- [x] Prototype dual-route split recommendation token (`WHAT-IF SPLIT:ON`) behind flag when primary/secondary plans diverge strongly (high-risk novelty)

## Next Up (Game Director Injection - 2026-03-21 Cycle Z)
- [x] Add split-recommendation confidence token (`WHAT-IF SPLIT CONF:LOW|MID|HIGH`) behind flag for operator trust readability
- [x] Add split route-pair token (`WHAT-IF SPLIT LANES:<primary>/<secondary>`) for handoff clarity in compact digest copy
- [x] Prototype split-safe-mode token (`WHAT-IF SPLIT SAFE:ON`) behind flag when split suggests non-escalating dual-path plans

## Next Up (Game Director Injection - 2026-03-22 Cycle AA)
- [x] Add split posture token (`WHAT-IF SPLIT POSTURE:SAFE|WATCH|HOLD`) to digest from split armed/safe/confidence trio *(lifecycle: [~] -> [x])*
- [x] Add split cooloff token (`WHAT-IF SPLIT COOLOFF:<n>`) counting consecutive OFF windows after split ON cycle
- [x] Prototype split escalation sentinel (`WHAT-IF SPLIT ESCALATE:ON`) behind flag when split lanes remain divergent under `TENSE` fit

## Next Up (Game Director Injection - 2026-03-22 Cycle AB)
- [x] Add split escalation confidence token (`WHAT-IF SPLIT ESC CONF:LOW|MID|HIGH`) from split confidence + plan-fit pressure context
- [x] Add split escalation route-pair readability token (`WHAT-IF SPLIT ESC LANES:<primary>/<secondary>`) for escalation handoff clarity
- [x] Prototype split escalation cooldown pressure token (`WHAT-IF SPLIT ESC COOL:<n>`) behind flag when escalation recently disarmed

## Next Up (Game Director Injection - 2026-03-22 Cycle AC)
- [x] Add split escalation state token (`WHAT-IF SPLIT ESC STATE:ARMED|COOLING|IDLE`) for faster digest triage
- [x] Add split escalation cooldown pressure-band token (`WHAT-IF SPLIT ESC PRESSURE:LOW|MID|HIGH`) behind flag for cooldown risk context
- [x] Prototype split escalation recovery route hint (`WHAT-IF SPLIT ESC RECOVER:<lane>`) behind flag for post-escalation planning

## Next Up (Game Director Injection - 2026-03-22 Cycle AD)
- [x] Add split escalation recovery route hint (`WHAT-IF SPLIT ESC RECOVER:<lane>`) behind flag with lowest-pressure lane selection for post-escalation planning
- [x] Add split escalation recovery confidence token (`WHAT-IF SPLIT ESC RECOVER CONF:LOW|MID|HIGH`) from lane divergence + state + pressure easing
- [x] Prototype split escalation dual-lane recovery fallback token (`WHAT-IF SPLIT ESC RECOVER ALT:<lane>`) behind flag for contingency planning

## Next Up (Game Director Injection - 2026-03-22 Cycle AE)
- [x] Add split escalation recovery ALT confidence token (`WHAT-IF SPLIT ESC RECOVER ALT CONF:LOW|MID|HIGH`) for contingency-lane trust readability
- [x] Add split escalation recovery route decision token (`WHAT-IF SPLIT ESC RECOVER PLAN:PRIMARY|ALT|HOLD`) from recover/recover-alt availability
- [x] Prototype split escalation recovery rationale token (`WHAT-IF SPLIT ESC RECOVER WHY:<short>`) behind flag for operator context

## Next Up (Game Director Injection - 2026-03-22 Cycle AF)
- [x] Add split escalation recovery tempo token (`WHAT-IF SPLIT ESC RECOVER TEMPO:FAST|STEADY|DEFER`) for operator pacing readability *(lifecycle: [~] -> [x])*
- [x] Add split escalation recovery confidence-delta token (`WHAT-IF SPLIT ESC RECOVER ΔCONF:+n|-n`) comparing against prior digest window
- [x] Prototype split escalation recovery veto sentinel (`WHAT-IF SPLIT ESC RECOVER VETO:ON`) behind flag when pressure remains HIGH under low confidence

## Next Up (Game Director Injection - 2026-03-22 Cycle AG)
- [x] Add split escalation recovery veto confidence token (`WHAT-IF SPLIT ESC RECOVER VETO CONF:LOW|MID|HIGH`) for operator trust readability
- [x] Add split escalation recovery veto rationale token (`WHAT-IF SPLIT ESC RECOVER VETO WHY:<short>`) behind flag for compact triage context
- [x] Prototype split escalation recovery veto cooloff token (`WHAT-IF SPLIT ESC RECOVER VETO COOLOFF:<n>`) behind flag after veto disarm

## Next Up (Game Director Injection - 2026-03-22 Cycle AH)
- [x] Add split escalation recovery veto state token (`WHAT-IF SPLIT ESC RECOVER VETO STATE:ARMED|COOLING|IDLE`) for rapid cooldown triage
- [x] Add split escalation recovery veto dwell token (`WHAT-IF SPLIT ESC RECOVER VETO DWELL:<n>`) to count consecutive ARMED windows
- [x] Prototype split escalation veto release cue token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE:<short>`) behind flag when state transitions `COOLING -> IDLE`

## Next Up (Game Director Injection - 2026-03-22 Cycle AI)
- [x] Add split escalation veto release confidence token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE CONF:LOW|MID|HIGH`) for release-cue trust readability *(lifecycle: [~] -> [x])*
- [x] Add split escalation veto release route token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE:<lane>`) for post-cooldown handoff clarity
- [x] Prototype split escalation veto release timer token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE TICK:<n>`) behind flag for idle-window pacing

## Next Up (Game Director Injection - 2026-03-22 Cycle AJ)
- [x] Add split escalation veto release pacing phase token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE:IDLE|EARLY|MID|LATE`) for glanceable idle-window pacing
- [x] Add split escalation veto release cadence token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE:ACCEL|STEADY|DECAY`) from tick deltas over prior window
- [x] Prototype split escalation auto-rearm warning token (`WHAT-IF SPLIT ESC RECOVER VETO REARM:WATCH`) behind flag when release tick remains late under HIGH pressure

## Next Up (Game Director Injection - 2026-03-22 Cycle AK)
- [x] Add split escalation auto-rearm confidence token (`WHAT-IF SPLIT ESC RECOVER VETO REARM CONF:LOW|MID|HIGH`) for trust weighting of WATCH cues
- [x] Add split escalation auto-rearm rationale token (`WHAT-IF SPLIT ESC RECOVER VETO REARM WHY:<short>`) for concise operator context *(lifecycle: [~] -> [x])*
- [x] Prototype split escalation auto-rearm cooloff token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF:<n>`) behind flag after WATCH disarms

## Next Up (Game Director Injection - 2026-03-22 Cycle AL)
- [x] Add split escalation auto-rearm cooloff state token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF STATE:ACTIVE|IDLE`) for rapid cooldown triage
- [x] Add split escalation auto-rearm pressure-relief fit token (`WHAT-IF SPLIT ESC RECOVER VETO REARM FIT:RELIEF|EVEN|TENSE`) from cooloff + pressure context
- [x] Prototype split escalation auto-rearm nudge token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE:<short>`) behind flag for operator handoff

## Next Up (Game Director Injection - 2026-03-22 Cycle AM)
- [x] Add split escalation auto-rearm nudge confidence token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE CONF:LOW|MID|HIGH`) for handoff trust readability
- [x] Add split escalation auto-rearm nudge window token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WINDOW:ARMED|COOLING|IDLE`) from rearm + cooloff-state context
- [x] Prototype split escalation auto-rearm nudge rationale token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WHY:<short>`) behind flag for compact operator coaching

## Next Up (Game Director Injection - 2026-03-22 Cycle AN)
- [x] Add split escalation nudge impact-band token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE IMPACT:DEFENSIVE|CAUTIOUS|NEUTRAL`) from nudge + window + fit signals
- [x] Add nudge drift token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE DRIFT:STABLE|SHIFTING`) from current/prior nudge rationale changes
- [x] Prototype dual-lane coach snapshot (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH:<primary>|<backup>`) behind flag for contingency readability

## Next Up (Game Director Injection - 2026-03-22 Cycle AO)
- [x] Add dual-lane coach confidence token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH CONF:LOW|MID|HIGH`) for contingency snapshot trust weighting
- [x] Add dual-lane coach posture token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH MODE:PRIMARY|BALANCED|BACKUP`) from coach lane selection mix
- [x] Prototype coach fallback reason token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH WHY:<short>`) behind flag for operator context

## Next Up (Game Director Injection - 2026-03-22 Cycle AP)
- [x] Add dual-lane coach handoff token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF:LOCKED|FLEX|NONE`) for at-a-glance routing readiness
- [x] Add coach handoff pressure-fit token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF FIT:SAFE|EVEN|TENSE`) from handoff + pressure context
- [x] Prototype coach handoff rationale token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF WHY:<short>`) behind flag for compact operator coaching

## Next Up (Game Director Injection - 2026-03-22 Cycle AQ)
- [x] Add portal transition FX cue token (`FX:CALM|FLICKER|SURGE`, compact `FX:C|F|S`) from route pressure score for player-facing jump readability *(forced lane rebalance: vfx/world + systems)*
- [x] Add combat hit-rhythm warning pulse token (`BERSERK FX:PULSE`) when `THREAT Δ:+` persists for 2+ turns (combat/vfx readability follow-up)
- [x] Prototype route-tag ASCII vignette in portal prompt (`ROUTE VIGNETTE:<glyph>`) behind flag for stronger world-choice fantasy

## Next Up (Game Director Injection - 2026-03-22 Cycle AR)
- [x] Add route-vibe coaching token in portal prompt (`ROUTE VIBE:CALM|EDGE|DOOM`, compact `VIBE:C|E|D`) for faster emotional read on jump choice
- [x] Add route-vibe drift telemetry snapshot (count by vibe per weekly digest window) for readability tuning cadence
- [x] Prototype route-vibe conflict warning (`VIBE CONFLICT:ON`) behind flag when route tag and threat tier imply opposing pacing cues

## Next Up (Game Director Injection - 2026-03-22 Cycle AS)
- [x] Add route-vibe conflict rationale token (`VIBE WHY:<vibe>vs<tier>`, compact `VCWHY:<vibe>/<tier>`) behind flag for faster operator triage *(lifecycle: [~] -> [x])*
- [x] Prototype conflict-aware coach override token (`COACH OVERRIDE:DE-ESCALATE`) behind flag when `VIBE CONFLICT:ON` and adaptive ALT exists *(lifecycle: [~] -> [x])*
- [x] Prototype vibe-consistency reward hint (`VIBE SYNC:+1`) behind flag when route vibe aligns with threat tier for 3 consecutive transitions

## Next Up (Game Director Injection - 2026-03-22 Cycle AT)
- [x] Add vibe-sync streak progress token in portal prompt (`VIBE CHAIN:<n>/3`, compact `VSC:<n>/3`) behind flag for pre-reward readability
- [x] Prototype sync-threshold dodge charge handoff (`VIBE SYNC DODGE:+1`) behind flag when `VIBE SYNC:+1` triggers
- [x] Prototype route-vibe snapback warning (`VIBE SNAPBACK:ON`) behind flag on immediate post-sync misalignment

## Next Up (Game Director Injection - 2026-03-22 Cycle AU)
- [x] Add post-snapback recovery cue token (`VIBE RECOVER:READY`, compact `VR:OK`) behind flag on first re-aligned transition
- [x] Add route-vibe resilience streak token (`VIBE RESILIENCE:<n>`) behind flag for consecutive recoveries after snapback
- [x] Prototype route-vibe drift alarm token (`VIBE DRIFT:WIDE`) behind flag when conflict + snapback co-occur in short window

## Next Up (Game Director Injection - 2026-03-22 Cycle AV)
- [x] Add berserker cooldown relief token (`BERSERK FX:FADE`) when pulse streak breaks after sustained rise (combat/vfx cadence guard)
- [x] Add lane-coverage watchdog token in weekly digest (`LANE CADENCE:OK|GAP`) to flag missing combat-vfx/design-world/systems-ops buckets over trailing 24h (systems/ops)
- [x] Prototype route-vibe drift alarm token (`VIBE DRIFT:WIDE`) with escalating glyph cue (`DRIFT GLYPH:<...>`) behind flag for world/design readability

## Next Up (Game Director Injection - 2026-03-22 Cycle AW)
- [x] Add digest action-pace token (`ACTION PACE:ACCEL|STEADY|BRAKE`) from `ACTION GUARD + ACTION STABILITY + PRESSURE LAG` for quicker route-operation cadence triage *(lifecycle: [~] -> [x])*
- [x] Add digest pace-drift token (`PACE DRIFT:+n|-n`) by comparing current/prior `ACTION PACE` windows
- [x] Prototype flagged pace coach rationale token (`ACTION PACE WHY:<short>`) for compact operator context *(lifecycle: [ ] -> [~] -> [x])*

## Next Up (Game Director Injection - 2026-03-23 Cycle AX)
- [x] Add digest pace-window token (`ACTION PACE WINDOW:OPEN|HOLD|CLOSE`) from `ACTION PACE + PACE DRIFT + ACTION GUARD` for operator go/no-go timing
- [x] Add digest pace-window confidence token (`ACTION PACE WINDOW CONF:LOW|MID|HIGH`) from window stability + drift continuity
- [x] Prototype flagged pace-window fallback token (`ACTION PACE ALT WINDOW:<short>`) when primary pace window is `CLOSE` but sandbox lane is `ON`

## Next Up (Game Director Injection - 2026-03-23 Cycle AY)
- [x] Add flagged pace-window fallback confidence token (`ACTION PACE ALT WINDOW CONF:LOW|MID|HIGH`) from fallback readiness + sandbox target quality
- [x] Add flagged fallback fit token (`ACTION PACE ALT WINDOW FIT:SAFE|EVEN|TENSE`) for pressure-aware alternate pacing guidance
- [x] Prototype fallback rationale micro-token (`ACTION PACE ALT WINDOW WHY:<short>`) for operator handoff clarity


## Next Up (Game Director Injection - 2026-03-23 Cycle AZ)
- [x] UX/Systems Team: Prototype fallback urgency token (`ACTION PACE ALT WINDOW URGENCY:NOW|SOON|LATER`) from fallback window + fit/confidence for quicker operator handoff
- [x] QA/Systems Team: Add fallback urgency drift token (`ACTION PACE ALT WINDOW URGENCY Δ:+n|-n`) comparing current/prior urgency band
- [x] Design/AI Content Team: Prototype compact fallback step token (`ACTION PACE ALT WINDOW STEP:<verb>`) for one-action operator nudges

## Next Up (Game Director Injection - 2026-03-23 Cycle BA)
- [x] Design/UX Team: Add compact fallback step glyph token (`ACTION PACE ALT WINDOW STEP GLYPH:<sigil>`) behind flag for DOS-width scanability
- [x] Systems/QA Team: Prototype fallback step drift token (`ACTION PACE ALT WINDOW STEP Δ:<n>`) against prior digest snapshot
- [x] Combat/VFX Team: Prototype fallback cadence pulse token (`ACTION PACE ALT WINDOW PULSE:COOL|LIVE|HOT`) for pressure readability

## Next Up (Game Director Injection - 2026-03-23 Cycle BB)
- [x] Combat/VFX Team: Ship fallback cadence pulse token (`ACTION PACE ALT WINDOW PULSE:COOL|LIVE|HOT`) with flag + digest schema + markdown wiring
- [x] Systems/QA Team: Add pulse drift token (`ACTION PACE ALT WINDOW PULSE Δ:+n|-n`) comparing current/prior pulse bands
- [x] Design/World Team: Prototype pulse-aware portal handoff cue (`ROUTE PULSE LINK:SOFT|SHARP`) behind flag for cross-surface readability

## Next Up (Game Director Injection - 2026-03-23 Cycle BC)
- [x] Design/World Team: Add pulse-aware portal handoff confidence token (`ROUTE PULSE LINK CONF:LOW|MID|HIGH`) for operator trust readability
- [x] UX/World Team: Prototype compact portal prompt pulse cue (`PULSE LINK:S|H`) behind flag for in-run route cadence readability
- [x] Systems/QA Team: Prototype pulse-link drift streak token (`ROUTE PULSE LINK STREAK:<n>`) in weekly digest for persistence triage

## Next Up (Game Director Injection - 2026-03-23 Cycle BD)
- [x] UX/Systems Team: Add route pulse-link mode token (`ROUTE PULSE LINK MODE:IDLE|SUSTAIN|SURGE`) from link + streak + pulse drift for faster cadence triage
- [x] Systems/QA Team: Add route pulse-link mode drift token (`ROUTE PULSE LINK MODE Δ:+n|-n`) versus prior digest window
- [x] Design/World Team: Prototype compact portal mode cue (`PULSE MODE:I|S|X`) behind flag for in-run route readability parity

## Next Up (Game Director Injection - 2026-03-23 Cycle BE)
- [x] UX/Systems Team: Add route pulse-link mode rationale micro-token (`ROUTE PULSE LINK MODE WHY:<short>`) behind flag for compact triage context
- [x] Systems/QA Team: Add route pulse-link mode stability streak token (`ROUTE PULSE LINK MODE STREAK:<n>`) across digest windows
- [x] Design/World Team: Prototype detailed portal pulse mode cue (`ROUTE PULSE MODE:IDLE|SUSTAIN|SURGE`) behind flag for full-prompt parity
## Next Up (Game Director Injection - 2026-03-23 Cycle BF)
- [x] UX/Systems Team: Add route pulse-link mode fit token (`ROUTE PULSE LINK MODE FIT:SYNC|WATCH|BREAK|RESET`) for handoff stability triage *(lifecycle: [~] -> [x])*
- [x] QA/Systems Team: Add route pulse-link mode fit drift token (`ROUTE PULSE LINK MODE FIT Δ:+n|-n`) against prior digest window
- [x] Design/World Team: Prototype compact portal pulse fit cue (`PULSE FIT:Y|W|B|R`) behind flag for in-run readability parity

## Next Up (Game Director Injection - 2026-03-23 Cycle BG)
- [x] Design/World Team: Prototype compact portal pulse-fit cue (`PULSE FIT:Y|W|B|R`) behind flag for in-run readability parity
- [x] Combat/VFX Team: Prototype compact pulse-flare warning token (`PULSE FLARE:+`) when `PULSE MODE:X` and fit downgrades (`B|R`) *(lifecycle: [~] -> [x])*
- [x] Systems/UX Team: Prototype compact prompt token-priority mode (`FIT-FIRST|MODE-FIRST`) behind flag under strict DOS width budget

## Next Up (Game Director Injection - 2026-03-23 Cycle BH)
- [x] UX/Systems Team: Prototype compact pulse-priority cue token (`PRI:F|M`) tied to token-priority mode so operators can instantly read active ordering
- [x] QA/Systems Team: Add weekly digest token for compact pulse-priority mode usage (`ROUTE PULSE TOKEN PRIORITY:FIT-FIRST|MODE-FIRST|OFF`) with drift guard
- [x] Design/World Team: Prototype portal fallback micro-cue (`ALT STEP:<SAFE|BAIT|PUSH>`) behind flag for faster branch intent scan

## Next Up (Game Director Injection - 2026-03-23 Cycle BI)
- [x] UX/World Team: Prototype fallback micro-cue confidence token (`ALT STEP CONF:LOW|MID|HIGH`) behind flag for branch-intent trust readability
- [x] Systems/QA Team: Add fallback micro-cue confidence drift token (`ALT STEP CONF Δ:+n|-n`) to weekly digest for stability triage
- [x] Design/AI Content Team: Prototype compact fallback intent rationale token (`ALT STEP WHY:<short>`) behind flag for operator context

## Next Up (Game Director Injection - 2026-03-23 Cycle BJ)
- [x] UX/AI Content Team: Prototype fallback rationale confidence token (`ALT STEP WHY CONF:LOW|MID|HIGH`) behind flag for trust readability
- [x] Systems/QA Team: Add fallback rationale confidence drift token (`ALT STEP WHY CONF Δ:+n|-n`) in weekly digest for stability triage
- [x] Design/World Team: Prototype compact rationale glyph token (`ALT WHY GLYPH:<sigil>`) behind flag for DOS-width scanability

## Next Up (Game Director Injection - 2026-03-23 Cycle BK)
- [x] UX/World Team: Prototype compact rationale glyph alias token (`AWG:<sigil>`) behind flag for stricter DOS-width prompt scanability
- [x] Systems/QA Team: Add compact rationale glyph drift token (`ALT WHY GLYPH Δ:+n|-n`) in weekly digest for stability triage
- [x] Design/AI Content Team: Prototype glyph rationale cadence token (`ALT WHY GLYPH MODE:STEADY|SPIKE`) behind flag for operator readability

### Game Director Cycle BL (2026-03-23)
- [x] QA/Systems Team: Add weekly digest drift token `ALT WHY GLYPH MODE Δ:+n|-n` with prior-window signals
- [x] Design/AI Content Team: Prototype compact prompt alias for glyph mode token (`AWGM:<S|K>`) behind flag
- [x] Systems/QA Team: Add digest confidence token for glyph-mode drift (`ALT WHY GLYPH MODE CONF:LOW|MID|HIGH`)

## Next Up (Game Director Injection - 2026-03-23 Cycle BM)
- [x] Systems/QA Team: Add glyph-mode confidence drift token (`ALT WHY GLYPH MODE CONF Δ:+n|-n`) to weekly digest for confidence stability triage
- [x] UX/World Team: Prototype compact confidence alias token (`AWGMC:<L|M|H>`) behind flag for prompt-width budget
- [x] Design/AI Content Team: Prototype glyph-mode confidence rationale micro-token (`ALT WHY GLYPH MODE CONF WHY:<short>`) behind flag

## Next Up (Game Director Injection — 2026-03-23 Cycle BN, forced-lane rebalance)
- [x] Combat/VFX Team: Add berserker cooldown intensity tier token to status feed (`BERSERK FX:FADE(SOFT|HARD)`) using threat-drop severity for clearer post-spike readability
- [x] Design/World Team: Prototype portal cooloff vibe trail token (`VIBE TRAIL:CALM|ASH`) behind flag after berserk fade events to reinforce recovery fantasy *(lifecycle: [~] -> [x])* 
- [x] Systems/Ops Team: Add weekly cadence watchdog detail row (`LANE GAP DETAIL`) with combat/vfx last-touch age so forced-lane triggers become auditable

## Next Up (Game Director Injection — 2026-03-23 Cycle BO)
- [x] UX/World Team: Prototype portal vibe-trail confidence token (`VIBE TRAIL CONF:LOW|MID|HIGH`, compact `VTC:<L|M|H>`) behind flag for post-fade handoff trust readability *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token family coverage for vibe-trail confidence token churn (`VIBE TRAIL CONF`) for drift triage
- [x] Design/AI Content Team: Prototype compact vibe-trail rationale token (`VIBE TRAIL WHY:<short>`) behind flag for operator context
## Next Up (Game Director Injection - 2026-03-23 Cycle BP)
- [x] UX/World Team: Add compact vibe-trail rationale alias token (`VTW:<short>`) behind flag for DOS-width scanability while keeping detailed `VIBE TRAIL WHY` label *(lifecycle: [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token family coverage for compact vibe-trail rationale alias churn (`VTW:` + `VIBE TRAIL WHY:`) *(lifecycle: [~] -> [x])*
- [x] Design/AI Content Team: Prototype vibe-trail rationale confidence token (`VIBE TRAIL WHY CONF:LOW|MID|HIGH`, compact `VTWC:<L|M|H>`) behind flag

## Next Up (Game Director Injection - 2026-03-23 Cycle BQ)
- [x] Systems/QA Team: Add weekly digest token-family coverage for rationale-confidence alias churn (`VIBE TRAIL WHY CONF:` + `VTWC:`) with markdown triage row
- [x] UX/World Team: Prototype compact portal rationale-confidence rail token (`VIBE TRAIL CONF RAIL:<STEADY|SPIKE>`) behind flag for faster jump triage
- [x] Design/AI Content Team: Prototype rationale-confidence micro-rationale token (`VIBE TRAIL WHY CONF WHY:<short>`) behind flag for operator trust context

## Next Up (Game Director Injection - 2026-03-23 Cycle BR)
- [x] Systems/AI Content Team: Prototype micro-rationale confidence token (`VIBE TRAIL WHY CONF WHY CONF:LOW|MID|HIGH`, compact `VTCWC:<L|M|H>`) behind flag for trust readability *(lifecycle: [~] -> [x])*
- [x] UX/World Team: Prototype portal micro-rationale rail token (`VIBE TRAIL WHY CONF WHY RAIL:STEADY|SPIKE`) behind flag for fast route triage *(lifecycle: [~] -> [x])*
- [x] QA/Systems Team: Add weekly digest token-family coverage for micro-rationale confidence alias churn (`VTCWC:` + detailed label) *(lifecycle: [ ] -> [x])*

## Next Up (Game Director Injection - 2026-03-23 Cycle BS)
- [x] UX/Design Team: Prototype portal vibe-trail arc token (`VIBE TRAIL ARC:RECOVER|SCAR|MIXED`, compact `VTA:<R|S|M>`) behind flag for route fantasy readability *(lifecycle: [~] -> [x])*
- [x] Combat/VFX Team: Prototype pulse-heat cue token (`PULSE HEAT:COOL|WARM|HOT`) in compact prompt behind flag for pressure readability
- [x] QA/Systems Team: Add weekly digest token-family coverage for vibe-trail arc alias churn (`VIBE TRAIL ARC:` + `VTA:`)

## Next Up (Game Director Injection — 2026-03-23 Cycle BT)
- [x] Combat/VFX Team: Add compact pulse-heat FX cue token (`PULSE HEAT FX:CALM|SPARK|BLAZE`) behind `DOTPIO_EXPERIMENT_PULSE_HEAT_FX`
  - [x] Add deterministic heat-to-fx mapper wired to existing pulse-heat tiers (`COOL/WARM/HOT`)
  - [x] Render compact prompt token without altering route pressure/combat mechanics
  - [x] Add regression coverage for COOL/WARM/HOT FX token emission (`scripts/regression_portal_pulse_heat_fx.lua`)
- [x] Design/World Team: Prototype compact route afterglow cue (`ROUTE GLOW:SOFT|SHARP`) tied to `VIBE TRAIL ARC` for post-jump fantasy readability
- [x] Systems/QA Team: Add weekly digest token-family coverage for pulse-heat FX churn (`PULSE HEAT FX:`) with compact-budget drift note

## Next Up (Game Director Injection — 2026-03-23 Cycle BU)
- [x] UX/World Team: Prototype route-afterglow confidence token (`ROUTE GLOW CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF` for post-jump handoff trust readability *(lifecycle: [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family coverage for route-afterglow confidence churn (`ROUTE GLOW CONF:`)
- [x] Combat/VFX Team: Prototype route-glow pulse-overdrive token (`ROUTE GLOW FX:SOFT|SHARP|SURGE`) behind flag when pulse-heat reaches `HOT`

## Next Up (Game Director Injection — 2026-03-24 Cycle BV)
- [x] UX/World Team: Prototype compact route-glow FX alias token (`RGFX:<S|H|X>`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_COMPACT` for tighter DOS prompt budget
- [x] Systems/QA Team: Add weekly digest token-family coverage for route-glow FX churn (`ROUTE GLOW FX:` + `RGFX:`) with compact-budget drift note
- [x] Combat/VFX Team: Prototype route-glow FX confidence token (`ROUTE GLOW FX CONF:LOW|MID|HIGH`, compact `RGFXC:<L|M|H>`) behind flag for overdrive cue trust readability

## Next Up (Game Director Injection — 2026-03-24 Cycle BW)
- [x] Systems/QA Team: Add weekly digest token-family coverage for route-glow FX confidence churn (`ROUTE GLOW FX CONF:` + `RGFXC:`) with compact-budget drift note
- [x] UX/World Team: Prototype compact route-glow confidence alias token (`RGC:<L|M|H>`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF_COMPACT` for tighter DOS prompt budget *(lifecycle: [ ] -> [~] -> [x])*
- [x] Design/AI Content Team: Prototype route-glow confidence rationale token (`ROUTE GLOW FX CONF WHY:<short>`) behind flag for trust context *(lifecycle: [~] -> [x])*

## Next Up (Game Director Injection — 2026-03-24 Cycle BX)
- [x] Design/AI Content Team: Prototype compact route-glow FX confidence rationale alias token (`RGFXW:<O|P|S>`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_COMPACT` while preserving detailed token fallback *(lifecycle: [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family coverage for route-glow FX confidence rationale token churn (`ROUTE GLOW FX CONF WHY:` + `RGFXW:`)
- [x] UX/World Team: Prototype compact route-glow rationale rail token (`ROUTE GLOW FX CONF WHY RAIL:STEADY|SPIKE`) behind flag for trust pacing readability

## Next Up (Game Director Injection — 2026-03-24 Cycle BY)
- [x] UX/World Team: Add compact alias token for route-glow rationale rail (`RGFXWR:<STEADY|SPIKE>`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_COMPACT` while preserving detailed fallback
- [x] Systems/QA Team: Add weekly digest token-family coverage for route-glow rationale rail churn (`ROUTE GLOW FX CONF WHY RAIL:` + `RGFXWR:`) *(lifecycle: [ ] -> [~] -> [x])*
- [x] Design/UX Team: Prototype confidence-adaptive rail compression token (`RGFXWRM:LOCK|FLEX`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE` for pressure readability under compact budgets *(lifecycle: [ ] -> [x])* 

## Next Up (Game Director Injection — 2026-03-24 Cycle BZ)
- [x] Systems/QA Team: Add weekly digest token-family coverage for rail-mode churn (`RGFXWRM:`) with compact-budget drift note
- [x] Combat/VFX Team: Prototype rail-mode intensity accent token (`RGFXWRI:SOFT|HARD`) keyed off `LOCK|FLEX` for stronger overdrive feel
- [x] AI Content/Design Team: Add rationale copy guard so rail-mode `LOCK|FLEX` wording remains deterministic with `RGFXW` mappings *(lifecycle: [ ] -> [~] -> [x])*

## Next Up (Game Director Injection — 2026-03-24 Cycle CA)
- [x] Systems/QA Team: Add weekly digest token-family coverage for rail-intensity churn (`RGFXWRI:`) with markdown triage rows
- [x] UX/World Team: Prototype detailed parity cue for rail intensity (`ROUTE GLOW FX CONF WHY RAIL INTENSITY:SOFT|HARD`) behind flag while preserving compact `RGFXWRI` *(lifecycle: [ ] -> [~] -> [x])*
- [x] Design/AI Content Team: Prototype flagged rail-intensity rationale token (`RGFXWRI WHY:<short>`) for overdrive readability context *(lifecycle: [ ] -> [~] -> [x])*
- [x] Combat/Design Team: Prototype rail-intensity rationale confidence token (`RGFXWRI WHY CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF` for overdrive trust readability *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family coverage for rail-intensity rationale churn (`RGFXWRI WHY:`) with markdown triage row *(lifecycle: [~] -> [x])*
- [x] UX/World Team: Prototype compact rail-intensity rationale confidence alias (`RGFXWRIWC:<L|M|H>`) behind flag for DOS-width scanability *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CC - Game Director Review (2026-03-24 07:10 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest alias-family churn coverage for `RGFXWRI WHY CONF:` + `RGFXWRIWC:`.
- Idea 2 (mid risk, UX/Design): Add detailed parity label `ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF:LOW|MID|HIGH` behind flag.
- Idea 3 (high risk, AI Content/Systems): Auto-tune `RGFXWRI WHY CONF` from weekly drift risk level.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family coverage for rail-intensity rationale confidence alias churn (`RGFXWRI WHY CONF:` + `RGFXWRIWC:`) *(lifecycle: [ ] -> [~] -> [x])*
- [x] UX/Design Team: Prototype detailed parity label for rail-intensity rationale confidence (`ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF:LOW|MID|HIGH`) behind flag *(lifecycle: [~] -> [x])*
- [x] AI Content/Systems Team: Prototype drift-adaptive confidence copy policy for `RGFXWRI WHY CONF` (offline recommendation only) *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CD - Game Director Review (2026-03-24 09:01 KST)
- Idea 1 (low risk, UX/World): Add compact rail-intensity confidence urgency token (`RGFXWRIU:LOW|MID|HIGH`) behind flag for faster prompt triage.
- Idea 2 (mid risk, Systems/Combat): Add one-step confidence trend token (`RGFXWRI WHY CONF Δ:+n|-n`) using prior transition state.
- Idea 3 (high risk, AI Content/Systems): Runtime adaptive confidence remap from weekly drift recommendation policy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact rail-intensity confidence urgency token (`RGFXWRIU:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY`.
- [x] Systems/QA Team: Add weekly digest token-family coverage for urgency alias churn (`RGFXWRIU:` + detailed label).
- [x] AI Content/Design Team: Prototype detailed parity label for urgency token (`ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:<LOW|MID|HIGH`) behind flag.

## Cycle CE - Game Director Review (2026-03-24 09:41 KST, forced lane rebalance)
- Coverage check (last 10 completed): systems=4, world=3, design=3, combat=1, vfx=0, ai-content=2, ux=4, qa=3. Bucket rollup: design/world=6 (60%), systems/ops=4 (40%), combat/vfx=1 (10%).
- Forced-lane rule triggered (`design/world` > 40%), so this cycle prioritizes underrepresented lanes with combat/vfx first.
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Combat/VFX): Add compact urgency FX token (`RGFXWRIUFX:CALM|SPARK|BLAZE`) mapped from urgency for stronger overdrive feel.
- Idea 2 (mid risk, Design/World): Add detailed parity urgency label (`ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:<LOW|MID|HIGH`) behind flag.
- Idea 3 (high risk, Systems/Ops): Add weekly digest urgency-family coverage + cadence watch row (`RGFXWRIUFX:` drift + lane-bucket reminder) for operator auditability.
- Selected experiment: Idea 1 (minimal vertical slice, additive + reversible).
- [x] Combat/VFX Team: Add compact urgency FX token (`RGFXWRIUFX:CALM|SPARK|BLAZE`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_FX`.
- [x] Design/World Team: Prototype detailed parity urgency label (`ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:<LOW|MID|HIGH`) behind dedicated flag.
- [x] Systems/Ops Team: Add weekly digest token-family coverage for urgency FX alias churn (`RGFXWRIUFX:`) plus lane cadence summary row.


## Cycle CF - Game Director Review (triggered after actionable backlog clear)
- Coverage check (last 10 completions): design/world heavy trend remained >40%; selected Systems/QA low-risk slice for balance.
- Ideas generated:
  - Low-risk (Systems/QA): add dedicated weekly digest family row for detailed urgency parity label churn.
  - Mid-risk (Design/Combat): urgency parity-conditioned coach suffix token for spike routes.
  - High-risk (Novelty): adaptive prompt budget swap that replaces route-glow family with urgency glyph burst under overload.
- Selected experiment: low-risk Systems/QA digest parity-family coverage.
- [x] Systems/QA Team: Add dedicated digest family churn row for detailed urgency parity label and lock via regression.

## Next Up (Game Director Injection — 2026-03-24 Cycle CG)
- [x] UX/Systems Team: Add compact urgency-parity alias token (`RGFXWRIUP:<LOW|MID|HIGH>`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY_COMPACT`.
- [x] Design/UX Team: Add budget-aware unknown-route coach fallback (`COACH:NO DATA` short form) in compact prompt mode.
- [x] Systems/AI Content Team: Prototype deterministic budget-headroom token-pruning order for urgency parity/FX stacks. *(lifecycle: [ ] -> [~] -> [x])*


## Cycle CH - Game Director Review (2026-03-24 13:40 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for compact urgency-parity alias (`RGFXWRIUP:`) with markdown triage row.
- Idea 2 (mid risk, UX/World): Prototype compact urgency-stack pruning tier token (`URG STACK:TIGHT|MID|LOOSE`) behind flag for prompt-debug readability.
- Idea 3 (high risk, AI Content/Systems): Prototype drift-aware urgency-stack pruning order recommendation from weekly digest trends.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for compact urgency-parity alias (`RGFXWRIUP:`) and lock via regression. *(lifecycle: [~] -> [x])*
- [x] UX/World Team: Prototype compact urgency-stack pruning tier token (`URG STACK:TIGHT|MID|LOOSE`) behind flag for prompt-debug readability.
- [x] AI Content/Systems Team: Prototype drift-aware urgency-stack pruning order recommendation from weekly digest trends.


## Cycle CI - Game Director Review (2026-03-24 14:30 KST)
- Idea 1 (low risk, VFX/Combat): Add floating damage numbers on hit for combat feedback readability.
- Idea 2 (mid risk, World/Design): Add map-zone ambient color tint to differentiate dungeon areas visually.
- Idea 3 (high risk, AI Content/VFX): Elemental damage type visual differentiation for projectiles based on player elemental stats.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] VFX/Combat Team: Add floating damage numbers on melee and magic hit with upward drift + fade animation.

## Cycle CJ - Game Director Review (2026-03-24 16:01 KST)
- Coverage check (last 10 completions): systems=5, world=3, design=2, combat=2, vfx=1, ai-content=2, ux=3, qa=4. Bucket rollup: systems/ops=50%, design/world=50%, combat/vfx=20%.
- Idea 1 (low risk, Combat/VFX): Keep slain enemies visible for 0.4s with fade-out so floating damage numbers have clear visual anchor.
- Idea 2 (mid risk, Systems/QA): Add floating-number stack cap token + digest telemetry for high-action turns.
- Idea 3 (high risk, AI Content/VFX): Add procedural glyph burst variants based on damage magnitude bands.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add short corpse fade window (`deathTimer`) with non-interactive draw-state + regression coverage.

## Cycle CK - Game Director Review (2026-03-24 16:31 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family coverage for urgency-stack tier cue (`URG STACK:`) so compact pruning guidance drift is auditable.
- Idea 2 (mid risk, UX/World): Add compact urgency-stack confidence rail token (`URG STACK RAIL:STEADY|SPIKE`) behind flag for prompt-debug pacing.
- Idea 3 (high risk, AI Content/Systems): Add drift-adaptive urgency-stack tier recommendation from weekly digest trend windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add token-family coverage + markdown triage row for `URG STACK:` in weekly digest and lock via regression.

## Cycle CL - Game Director Review (2026-03-24 17:05 KST)
- Idea 1 (low risk, UX/World): Add compact urgency-stack confidence rail token (`URG STACK RAIL:STEADY|SPIKE`) behind `DOTPIO_EXPERIMENT_URGENCY_STACK_RAIL` for prompt-debug pacing readability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family coverage for `URG STACK RAIL:` churn with markdown triage row + regression lock.
- Idea 3 (high risk, AI Content/Systems): Add drift-adaptive urgency-stack rail recommendation policy from weekly digest trend windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact urgency-stack confidence rail token (`URG STACK RAIL:STEADY|SPIKE`) behind `DOTPIO_EXPERIMENT_URGENCY_STACK_RAIL`.
- [x] Systems/QA Team: Add weekly digest token-family coverage for `URG STACK RAIL:` churn and markdown triage row; lock with regression. *(lifecycle: [~] -> [x])*
- [x] AI Content/Systems Team: Prototype drift-adaptive urgency-stack rail recommendation policy from weekly digest trend windows.

## Cycle CM - Game Director Review (2026-03-24 18:01 KST)
- Coverage check (last 10 completions): systems/qa dominant; combat/vfx underrepresented, so lane rebalance prioritized combat-facing slice.
- Idea 1 (low risk, Combat/VFX): Add lethal-hit floating damage accent (`<damage>!` + red tint) so kill confirmation reads instantly during high-action turns.
- Idea 2 (mid risk, Systems/QA): Add capped floating-number stack telemetry token in weekly digest for dense combat turns.
- Idea 3 (high risk, AI Content/VFX): Add procedural glyph burst families keyed off damage bands and urgency rail mode.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add lethal-hit floating damage accent (`<damage>!` + red tint) with debug-state exposure + regression lock. *(lifecycle: [~] -> [x])*
- [x] Systems/QA Team: Add floating-number stack-cap telemetry token to weekly digest (`DMGNUM STACK CAP:`) with churn row + regression lock. *(lifecycle: [~] -> [x])*
- [x] AI Content/VFX Team: Prototype damage-band glyph burst variants behind flag (`DMG GLYPH:BASIC|SPIKE|OVERDRIVE`).

## Cycle CN - Game Director Review (2026-03-24 19:12 KST)
- Coverage check (last 10 completions): combat/vfx recovered in prior cycle; systems/qa now selected for low-risk observability follow-up.
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for combat burst token family (`DMG GLYPH:`) with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Add compact combat prompt/debug token for active glyph burst band (`DMG GLYPH LIVE:BASIC|SPIKE|OVERDRIVE`) behind flag.
- Idea 3 (high risk, AI Content/VFX): Add dynamic glyph-shape remap policy from weekly drift pressure bands.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family coverage for `DMG GLYPH:` churn and lock via regression.
- [x] UX/Combat Team: Prototype compact debug token `DMG GLYPH LIVE:BASIC|SPIKE|OVERDRIVE` behind flag for live-readability audits. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype drift-aware glyph-shape remap recommendation policy (offline only). *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CO - Game Director Review (2026-03-24 20:40 KST)
- Coverage check (last 10 completions): systems/qa-heavy trend persisted; selected combat/vfx-facing player feedback slice for lane balance.
- Idea 1 (low risk, Combat/VFX): Add compact combat FX live token (`DMG GLYPH FX LIVE:CALM|SPARK|BLAZE`) behind flag mapped from latest glyph band.
- Idea 2 (mid risk, UX/Combat): Add compact damage-number lifecycle token (`DMGNUM LIFE:EARLY|MID|LATE`) for readability tuning.
- Idea 3 (high risk, AI Content/VFX): Add drift-aware runtime glyph FX remap policy from digest recommendations.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact combat FX live token (`DMG GLYPH FX LIVE:CALM|SPARK|BLAZE`) behind `DOTPIO_EXPERIMENT_DMG_GLYPH_FX_LIVE_DEBUG`.
- [x] Systems/QA Team: Add weekly digest token-family coverage for `DMG GLYPH FX LIVE:` churn + regression lock.
- [x] AI Content/VFX Team: Prototype offline-only glyph FX remap recommendation policy tied to drift risk. *(lifecycle: [~] -> [x])*

## Cycle CP - Game Director Review (2026-03-24 21:34 KST)
- Coverage check (last 10 completions): systems/qa + ai-content drift tooling dominant; selected low-risk systems slice with explicit confidence output to reduce recommendation ambiguity.
- Idea 1 (low risk, Systems/QA): Add offline digest confidence token for glyph FX remap recommendation (`DMG GLYPH FX REMAP CONF:LOW|MID|HIGH`).
- Idea 2 (mid risk, UX/Combat): Surface compact debug token for current offline glyph FX remap stance in HUD debug lane (`DMG FX PLAN:<mode>`), flag-gated.
- Idea 3 (high risk, AI Content/VFX): Prototype digest-driven auto-generated FX remap candidate table (offline sandbox artifact).
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add offline digest confidence token for glyph FX remap recommendation (`DMG GLYPH FX REMAP CONF:LOW|MID|HIGH`) with regression lock. *(lifecycle: [~] -> [x])*
- [x] UX/Combat Team: Prototype compact HUD debug token for glyph FX remap stance (`DMG FX PLAN:<mode>`) behind flag. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype offline digest-generated FX remap candidate table artifact for review workflows.

## Cycle CQ - Game Director Review (2026-03-24 21:52 KST)
- Coverage check (last 10 completions by lane): systems=5, ai-content=2, combat=1, vfx=1, ux=1, world=0, design=0, qa=0.
- Lane cap breach: systems (50%) > 40%; forced priority to underrepresented lanes (world/design + combat/vfx) this cycle.
- Idea 1 (low risk, UX/Combat/VFX): Add compact HUD debug remap-plan token (`DMG FX PLAN:HOLD_FX|MICRO_TUNE_FX|SYNC_WITH_GLYPH`) for live readability.
- Idea 2 (mid risk, World/Design): Add route-side ambient ramp hint token (`AMBIENT RAMP:CALM|TENSE`) in portal preview under flag.
- Idea 3 (high risk, Systems/Ops): Build offline FX remap candidate table artifact (`logs/playtests/dmg_glyph_fx_remap_candidates.{md,json}`).
- Selected experiment: Idea 1 (minimal vertical slice, forced-lane compliant).
- [x] UX/Combat Team: Add compact HUD debug remap-plan token (`DMG FX PLAN:<mode>`) behind `DOTPIO_EXPERIMENT_DMG_FX_PLAN_DEBUG`. *(lifecycle: [ ] -> [~] -> [x])*
- [x] World/Design Team: Prototype portal ambient-ramp hint token (`AMBIENT RAMP:CALM|TENSE`) behind flag for readability cadence.
- [x] Systems/Ops Team: Add offline glyph FX remap candidate table artifact generation for review workflows.

## Cycle CR - Game Director Review (2026-03-24 22:31 KST)
- Idea 1 (low risk, UX/World): Add compact ambient-ramp alias token (`AR:<C|T>`) behind flag for DOS-width readability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `AMBIENT RAMP:`.
- Idea 3 (high risk, AI Content/World): Drift-aware ambient ramp recommendation policy from weekly prompt pressure trends.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact ambient-ramp alias token (`AR:<C|T>`) behind `DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_COMPACT`.

## Next Up (Post-RC portal readability wave)
- [x] UX/World Team: Add portal ambient-ramp confidence readability token (`AMBIENT RAMP CONF:HIGH|MID|LOW`, compact `ARC:<H|M|L>`) behind `DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF` + `DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF_COMPACT`. *(lifecycle: [~] -> [x])*
  - [x] Add ambient-ramp confidence resolver with deterministic thresholds (CALM->HIGH, RISK/TENSE->MID, SPIKE/TENSE->LOW)
  - [x] Surface full prompt token `AMBIENT RAMP CONF:*` and compact alias `ARC:*`
  - [x] Add regression coverage script `scripts/regression_portal_ambient_ramp_confidence.lua`
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `AMBIENT RAMP CONF:` + `ARC:` and lock with regression. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/World Team: Prototype drift-aware ambient confidence recommendation policy (offline recommendation only). *(lifecycle: [~] -> [x])*

## Cycle CT - Game Director Review (2026-03-25 00:31 KST)
- Coverage check (last 10 completions): systems/qa drift tooling remained dense while combat/vfx readability has fewer fresh debug affordances; prioritize a combat-facing low-risk slice.
- Idea 1 (low risk, Combat/VFX): Add compact floating-number lifecycle token (`DMGNUM LIFE:EARLY|MID|LATE`) behind debug flag for instant combat feedback-phase triage.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE:` with markdown triage row.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware damage-number fade-curve remap recommendation policy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact floating-number lifecycle token (`DMGNUM LIFE:EARLY|MID|LATE`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_DEBUG` with regression lock.

## Cycle CU - Game Director Review (2026-03-25 01:01 KST)
- Coverage check (last 10 completions): combat/vfx slices improved, but digest observability still missing `DMGNUM LIFE` family churn visibility.
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE:` with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Add compact damage-number lifecycle confidence token (`DMGNUM LIFE CONF:LOW|MID|HIGH`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware damage-number fade-curve remap recommendation policy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE:` and lock via regression.

## Cycle CV - Game Director Review (2026-03-25 01:31 KST)
- Coverage check (last 10 completions): systems/qa observability slices are stable; selected combat-facing readability follow-up to keep debug feedback actionable during live tuning.
- Idea 1 (low risk, UX/Combat): Add compact damage-number lifecycle confidence token (`DMGNUM LIFE CONF:LOW|MID|HIGH`) behind debug flag.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF:` with markdown triage row.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware damage-number confidence remap recommendation policy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Combat Team: Add compact damage-number lifecycle confidence token (`DMGNUM LIFE CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG` with deterministic phase mapping and regression lock. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CW - Game Director Review (2026-03-25 02:04 KST)
- Coverage check (last 10 completions): combat-facing slices recovered; selected low-risk systems/qa observability follow-up for new confidence token family.
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF:` with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Add compact lifecycle confidence drift token (`DMGNUM LIFE CONF Δ:+n|-n`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline confidence remap recommendation policy from drift-risk + churn.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF:` and lock via regression. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CX - Game Director Review (2026-03-25 02:31 KST)
- Coverage check (last 10 completions): systems/qa digest instrumentation remained stable while combat debug readability can absorb one additive follow-up.
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:`) with markdown triage row.
- Idea 2 (mid risk, UX/Combat): Add compact lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:+n|-n`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware confidence-delta smoothing policy for damage-number fades.
- Selected experiment: Idea 2 (minimal vertical slice).
- [x] UX/Combat Team: Add compact lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:+n|-n`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CY - Game Director Review (2026-03-25 03:01 KST)
- Coverage check (last 10 completions): combat debug readability slices progressed; systems/qa digest visibility for `DMGNUM LIFE CONF Δ` remains the lowest-risk closure candidate.
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:`) with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Prototype compact lifecycle-confidence trend band token (`DMGNUM LIFE TREND:UP|HOLD|DOWN`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline confidence-delta smoothing recommendation policy from digest drift signals.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF Δ:` and lock via regression. *(lifecycle: [~] -> [x])*

## Cycle CZ - Game Director Review (2026-03-25 03:31 KST)
- Coverage check (last 10 completions): systems/qa observability remains represented; selected combat-facing debug readability slice to keep player-facing cadence visible.
- Idea 1 (low risk, UX/Combat): Add compact lifecycle-confidence trend token (`DMGNUM LIFE TREND:UP|HOLD|DOWN`) behind debug flag.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND:` with markdown triage row + regression lock.
- Idea 3 (high risk, AI Content/VFX): Prototype offline lifecycle-trend smoothing recommendation policy from digest drift windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Combat Team: Add compact lifecycle-confidence trend token (`DMGNUM LIFE TREND:UP|HOLD|DOWN`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_DEBUG` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND:` and lock via regression. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype offline lifecycle-trend smoothing recommendation policy (offline recommendation only). *(lifecycle: [ ] -> [~] -> [x])*

## Next Up (Game Director Injection — 2026-03-25 Cycle DA)
- [x] World/Design Team: Add portal ambient-ramp rationale token (`AMBIENT RAMP WHY`) with compact alias (`ARW`) for confidence-context readability.
- [x] Combat/VFX Team: Add optional trend-accent color mapping for `DMGNUM LIFE TREND` debug token (`UP`/`HOLD`/`DOWN`) and verify DOS contrast budget.
- [x] AI-Content/VFX Team: Prototype offline ambient-rationale recommendation policy (`AMBIENT RAMP WHY REC`) in weekly digest from churn + pressure signals. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DB - Game Director Review (2026-03-25 04:45 KST)
- Idea 1 (low risk, Systems/QA): Add offline confidence tier token for ambient-rationale recommendation (`AMBIENT RAMP WHY REC CONF:LOW|MID|HIGH`) in weekly digest.
- Idea 2 (mid risk, UX/World): Add compact parity summary line for ambient-rationale recommendation in digest token-family section.
- Idea 3 (high risk, AI Content/Systems): Prototype drift-adaptive runtime auto-remap from ambient-rationale recommendation outputs.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add offline confidence tier token for ambient-rationale recommendation (`AMBIENT RAMP WHY REC CONF:LOW|MID|HIGH`) in weekly digest with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] UX/World Team: Prototype compact parity summary line for ambient-rationale recommendation in digest token-family section.
- [x] AI Content/Systems Team: Prototype digest-driven ambient rationale auto-remap plan as offline sandbox artifact (no runtime coupling).

## Cycle DC - Game Director Review (2026-03-25 05:35 KST)
- Idea 1 (low risk, UX/AI Content): Add compact ambient auto-remap plan alias token (`ARW AUTO PLAN:HOLD|SHADOW|OPEN`) to weekly digest for faster operator triage.
- Idea 2 (mid risk, Systems/QA): Add weekly digest churn/drift row for ambient auto-remap plan alias and lock with regression.
- Idea 3 (high risk, AI Content/Systems): Prototype offline drift-aware ambient auto-remap candidate re-ranking policy from prior-window outcomes.
- Selected experiment: Idea 1 (minimal vertical slice, additive + reversible).
- [x] UX/AI Content Team: Add compact ambient auto-remap plan alias token (`ARW AUTO PLAN:HOLD|SHADOW|OPEN`) in weekly digest + sandbox artifact payload.
- [x] Systems/QA Team: Add weekly digest token-family churn/drift coverage for `ARW AUTO PLAN:` and lock via regression. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/Systems Team: Prototype offline drift-aware ambient auto-remap candidate re-ranking policy (sandbox artifact only, no runtime coupling). *(lifecycle: [ ] -> [x])*

## Cycle DD - Game Director Review (2026-03-25 06:31 KST)
- Idea 1 (low risk, Systems/QA): Add ambient auto-remap plan confidence token (`ARW AUTO PLAN CONF:LOW|MID|HIGH`) to weekly digest for quicker operator trust triage.
- Idea 2 (mid risk, UX/AI Content): Add compact ambient auto-remap rationale shorthand (`ARW AUTO WHY:<short>`) in offline artifact for handoff clarity.
- Idea 3 (high risk, AI Content/Systems): Prototype drift-adaptive auto-remap candidate suppression policy when confidence remains LOW for 3+ windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add ambient auto-remap plan confidence token (`ARW AUTO PLAN CONF:LOW|MID|HIGH`) with regression lock. *(lifecycle: [~] -> [x])*
- [x] UX/AI Content Team: Prototype compact ambient auto-remap rationale shorthand (`ARW AUTO WHY:<short>`) in offline artifact. *(lifecycle: [~] -> [x])*
- [x] AI Content/Systems Team: Prototype confidence-streak suppression policy for auto-remap candidates (offline-only). *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DE - Game Director Review (2026-03-25 08:01 KST)
- Idea 1 (low risk, Systems/QA): Add ambient auto-remap confidence drift token (`ARW AUTO PLAN CONF Δ:+n|-n`) from prior digest window to make trust changes auditable.
- Idea 2 (mid risk, UX/World): Add compact ambient auto-remap confidence band alias (`ARW APC:<L|M|H>`) behind flag in digest summary for tight scanability.
- Idea 3 (high risk, AI Content/Systems): Prototype offline confidence momentum policy that recommends plan freeze when confidence oscillates across windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add ambient auto-remap confidence drift token (`ARW AUTO PLAN CONF Δ:+n|-n`) and lock via regression. *(lifecycle: [~] -> [x])*
- [x] UX/World Team: Prototype compact ambient auto-remap confidence band alias (`ARW APC:<L|M|H>`) behind flag in digest summary. *(lifecycle: [~] -> [x])* 
- [x] AI Content/Systems Team: Prototype offline confidence momentum policy for auto-remap freeze recommendation. *(lifecycle: [ ] -> [~] -> [x])*


## Cycle DF - Game Director Review (2026-03-25 09:06 KST)
- Coverage check (last 10 completions): systems/qa-heavy observability trend persists while combat/vfx and world/design remain represented; choose a low-risk systems slice to lock newly added ambient remap aliases.
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for `ARW APC:` + momentum recommendation line (`ARW AUTO PLAN CONF MOMENTUM:`) with markdown triage rows + regression lock.
- Idea 2 (mid risk, UX/World): Add compact digest debug token for confidence momentum state (`ARW MOMENTUM:FREEZE|WATCH|ALLOW`) behind flag.
- Idea 3 (high risk, AI Content/Systems): Prototype offline confidence-oscillation dampening score (`ARW MOMENTUM SCORE:<n>`) from multi-window confidence drift.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `ARW APC:` + `ARW AUTO PLAN CONF MOMENTUM:` and lock via regression. *(lifecycle: [~] -> [x])*
- [x] UX/World Team: Prototype compact digest momentum alias token (`ARW MOMENTUM:<F|W|A>`) behind flag for tighter scanability.
- [x] AI Content/Systems Team: Prototype offline confidence-oscillation dampening score (`ARW MOMENTUM SCORE:<n>`) from multi-window confidence drift.

## Cycle DG - Game Director Review (2026-03-25 09:41 KST, forced-lane rebalance)
- Coverage check (last 10 completions): systems=7, world=2, ux=3, qa=4, ai-content=3, combat=0, vfx=0, design=0.
- Lane cap breach: systems (70%) > 40%, so this cycle forced an underrepresented-lane pick (combat/vfx prioritized).
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Combat/VFX): Add compact damage-number trend-FX token (`DMGNUM LIFE TREND FX:CALM|SPARK|BLAZE`) behind debug flag for instant pacing-readability.
- Idea 2 (mid risk, Design/World): Add compact ambient rationale momentum token (`ARW MOMENTUM ARC:CALM|TENSE`) behind flag in digest summary.
- Idea 3 (high risk, Systems/Ops): Add digest watchdog row for 24h bucket freshness (`LANE BUCKET AGE:<hours>`) to harden cadence audits.
- Selected experiment: Idea 1 (minimal vertical slice, additive + reversible).
- [x] Combat/VFX Team: Add compact damage-number trend-FX token (`DMGNUM LIFE TREND FX:CALM|SPARK|BLAZE`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_DEBUG` with regression lock.
- [x] Design/World Team: Prototype compact ambient rationale momentum token (`ARW MOMENTUM ARC:CALM|TENSE`) behind dedicated flag.
- [x] Systems/Ops Team: Add digest 24h bucket-freshness watchdog row (`LANE BUCKET AGE:<hours>`) for cadence auditability.

## Cycle DH - Game Director Review (2026-03-25 11:10 KST)
- Coverage check (last 10 completions): systems/qa regained momentum; choose low-risk observability slice with no runtime gameplay coupling.
- Idea 1 (low risk, Systems/Ops): Add lane-bucket freshness drift token (`LANE BUCKET AGE Δ:+n|-n`) versus prior digest window.
- Idea 2 (mid risk, UX/World): Add compact lane freshness alias token (`LBA:<sys>/<dw>/<cv>`) behind flag for summary scanability.
- Idea 3 (high risk, AI Content/Systems): Prototype offline lane-priority recommendation policy from bucket-age momentum.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/Ops Team: Add lane-bucket freshness drift token (`LANE BUCKET AGE Δ:+n|-n`) to weekly digest + regression lock.
- [x] UX/World Team: Prototype compact lane freshness alias token (`LBA:<sys>/<dw>/<cv>`) behind flag.
- [x] AI Content/Systems Team: Prototype offline lane-priority recommendation policy from bucket-age momentum.

## Cycle DI - Game Director Review (2026-03-25 12:31 KST, forced underrepresented-lane pick)
- Coverage check (last 10 completions): systems/ops-heavy digest observability still dominates; underrepresented design/world + combat/vfx lanes should be favored this cycle.
- Idea 1 (low risk, UX/World): Add compact lane-priority recommendation alias token (`LPR:<BAL|SYS|DW|CV>`) behind flag for digest summary scanability.
- Idea 2 (mid risk, Systems/QA): Add lane-priority recommendation confidence token (`LANE PRIORITY REC CONF:LOW|MID|HIGH`) derived from age spread + momentum gap.
- Idea 3 (high risk, AI Content/Systems): Prototype offline lane-priority hysteresis policy to suppress recommendation flapping.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact lane-priority recommendation alias token (`LPR:<BAL|SYS|DW|CV>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_ALIAS` with regression lock. *(lifecycle: [~] -> [x])*
- [x] Systems/QA Team: Add lane-priority recommendation confidence token (`LANE PRIORITY REC CONF:LOW|MID|HIGH`) with payload + markdown contract. *(lifecycle: [~] -> [x])*
- [x] AI Content/Systems Team: Prototype offline lane-priority hysteresis suppression policy for recommendation flapping.

## Cycle DJ - Game Director Review (2026-03-25 13:31 KST)
- Coverage check (last 10 completions): systems/ops instrumentation still dominant; selected low-risk AI Content/Systems offline-stability slice to reduce lane recommendation flapping without runtime coupling.
- Idea 1 (low risk, AI Content/Systems): Add offline lane-priority hysteresis suppression policy so recommendation only flips when score-gap clears a threshold.
- Idea 2 (mid risk, UX/World): Add compact hysteresis confidence rail token (`LPR HYS RAIL:STEADY|SPIKE`) behind flag for digest triage pacing.
- Idea 3 (high risk, Systems/QA): Prototype adaptive hysteresis-threshold tuning policy from multi-window lane-age volatility.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] AI Content/Systems Team: Prototype offline lane-priority hysteresis suppression policy for recommendation flapping.
- [x] Systems/QA Team: Add compact hysteresis alias token (`LPR HYS:H|S`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_ALIAS` with payload + markdown wiring.
- [x] UX/World Team: Prototype compact hysteresis confidence rail token (`LPR HYS RAIL:STEADY|SPIKE`) behind flag. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Prototype adaptive hysteresis-threshold tuning policy from lane-age volatility windows (offline recommendation only).

## Cycle DK - Game Director Review (2026-03-25 14:24 KST)
- Coverage check (last 10 completions): systems/qa digest observability remained dominant; selected low-risk compact-readability follow-up on the new hysteresis-threshold tuning output.
- Idea 1 (low risk, UX/Systems): Add compact hysteresis-threshold recommendation alias token (`LPR HYS THR:<L|H|R>`) behind flag for tight digest scanability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `LPR HYS THR:` + regression lock.
- Idea 3 (high risk, AI Content/Systems): Prototype adaptive hysteresis-threshold floor/ceiling learning policy from multi-window volatility outcomes.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact hysteresis-threshold recommendation alias token (`LPR HYS THR:<L|H|R>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_THRESHOLD_ALIAS` with payload + markdown + regression lock. *(lifecycle: [ ] -> [~] -> [x])* 
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `LPR HYS THR:` with markdown triage row + regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/Systems Team: Prototype offline adaptive hysteresis-threshold floor/ceiling learning policy from volatility outcomes.

## Cycle DL - Game Director Review (2026-03-25 15:34 KST)
- Coverage check (last 10 completions): systems/qa and offline observability still dominant; selected low-risk AI Content/Systems vertical slice that remains offline and reversible.
- Idea 1 (low risk, AI Content/Systems): Add adaptive hysteresis-threshold floor/ceiling learning policy from prior-window volatility outcomes.
- Idea 2 (mid risk, UX/Systems): Add compact adaptive-window drift token (`LPR HYS WINDOW Δ:+n|-n`) in digest summary for trend triage.
- Idea 3 (high risk, AI Content/Systems): Prototype offline volatility-regime memory (`CALM|SWING|SPIKE`) to auto-tune floor/ceiling step sizes.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] AI Content/Systems Team: Prototype offline adaptive hysteresis-threshold floor/ceiling learning policy from volatility outcomes.
- [x] Systems/QA Team: Add digest triage token (`LPR HYS WINDOW:TIGHT|BASE|WIDE`) from adaptive floor/ceiling span + regression lock.
- [x] UX/Systems Team: Prototype compact adaptive-window drift token (`LPR HYS WINDOW Δ:+n|-n`) for multi-window stability scanability.
- [x] AI Content/Systems Team: Prototype offline volatility-regime memory (`CALM|SWING|SPIKE`) for adaptive floor/ceiling step-size tuning. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DM - Game Director Review (2026-03-25 15:41 KST, forced-lane rebalance)
- Coverage check (last 10 completions by lane): systems=8, ai-content=3, ux=2, world=2, combat=0, vfx=0, design=0, qa=0.
- Lane cap breach: systems (80%) > 40%, so this cycle forced underrepresented lane selection.
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Combat/VFX): Add debug token `DMGNUM LIFE TREND FX PULSE:COAST|RUSH|BURST` behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_DEBUG`.
- Idea 2 (mid risk, Design/World): Add compact ambient momentum pulse alias (`ARW ARC PULSE:SOFT|LIVE|HOT`) behind flag in digest summary.
- Idea 3 (high risk, Systems/Ops): Add digest row `LANE CADENCE RECENCY:<ok|warn>` from bucket-age + delta drift.
- Selected experiment: Idea 1 (minimal vertical slice, combat/vfx lane rebalancing).
- [x] Combat/VFX Team: Add debug token `DMGNUM LIFE TREND FX PULSE:COAST|RUSH|BURST` behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_DEBUG` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Design/World Team: Prototype compact ambient momentum pulse alias (`ARW ARC PULSE:SOFT|LIVE|HOT`) behind flag in digest summary.
- [x] Systems/Ops Team: Prototype digest row `LANE CADENCE RECENCY:<ok|warn>` from bucket-age + delta drift. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DN - Game Director Review (2026-03-25 18:20 KST)
- Coverage check (last 10 completions): systems/ops + digest observability remained dense; selected a combat/vfx debug-readability slice to keep player-facing cadence cues fresh.
- Idea 1 (low risk, Combat/VFX): Add compact confidence token for pulse intensity (`DMGNUM LIFE TREND FX PULSE CONF:LOW|MID|HIGH`) behind debug flag.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND FX PULSE:` and confidence token family.
- Idea 3 (high risk, AI Content/VFX): Prototype offline pulse-intensity remap recommendation policy from weekly drift + lane pressure signals.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact pulse-intensity confidence token (`DMGNUM LIFE TREND FX PULSE CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_CONF_DEBUG`. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND FX PULSE:` + `DMGNUM LIFE TREND FX PULSE CONF:` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype offline pulse-intensity remap recommendation policy from drift-risk + cadence pressure bands. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DO - Game Director Review (2026-03-25 19:05 KST)
- Coverage check (last 10 completions): systems/qa + ai-content digest lane still dominant, so this cycle prioritized a visible combat/vfx-facing debug readability slice.
- Idea 1 (low risk, Combat/VFX): Add compact pulse remap-plan token (`DMGNUM LIFE TREND FX PULSE REMAP PLAN:HOLD|TUNE|SYNC`) behind debug flag.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND FX PULSE REMAP PLAN:` with regression lock.
- Idea 3 (high risk, AI Content/VFX): Prototype offline pulse-remap confidence momentum policy (`PULSE REMAP MOMENTUM:FREEZE|WATCH|ALLOW`) from multi-window churn + cadence pressure.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact pulse remap-plan token (`DMGNUM LIFE TREND FX PULSE REMAP PLAN:HOLD|TUNE|SYNC`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_REMAP_PLAN_DEBUG` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND FX PULSE REMAP PLAN:` with regression lock.
- [x] AI Content/VFX Team: Prototype offline pulse-remap confidence momentum policy (`PULSE REMAP MOMENTUM:FREEZE|WATCH|ALLOW`) from drift-risk + cadence pressure windows.

## Cycle DP - Game Director Review (2026-03-25 19:31 KST)
- Idea 1 (low risk, UX/Combat): Add compact pulse-remap momentum alias token (`PRM:<F|W|A>`) behind flag for digest scanability.
- Idea 2 (mid risk, Systems/QA): Add momentum drift token (`PULSE REMAP MOMENTUM Δ:+n|-n`) using prior digest window.
- Idea 3 (high risk, AI Content/VFX): Prototype offline momentum-streak suppression policy when `FREEZE` repeats across windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Combat Team: Add compact pulse-remap momentum alias token (`PRM:<F|W|A>`) behind `DOTPIO_EXPERIMENT_PULSE_REMAP_MOMENTUM_ALIAS` with regression lock.
- [x] Systems/QA Team: Add momentum drift token (`PULSE REMAP MOMENTUM Δ:+n|-n`) using prior digest window.
- [x] AI Content/VFX Team: Prototype offline momentum-streak suppression policy when `FREEZE` repeats across windows. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DQ - Game Director Review (2026-03-25 21:06 KST)
- Idea 1 (low risk, UX/Systems): Add compact pulse-remap suppression alias token (`PRMS:<S|A|O>`) behind flag for digest scanability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for suppression alias (`PRMS:` + `PULSE REMAP MOMENTUM SUPPRESS:`) with regression lock.
- Idea 3 (high risk, AI Content/VFX): Prototype offline suppression-escalation recommendation policy from freeze-streak + drift-risk windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact pulse-remap suppression alias token (`PRMS:<S|A|O>`) behind `DOTPIO_EXPERIMENT_PULSE_REMAP_MOMENTUM_SUPPRESSION_ALIAS` in digest payload/markdown with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add dedicated digest family churn triage note for suppression alias trend (`PRMS FAMILY TREND`) with prior-window drift context.
- [x] AI Content/VFX Team: Prototype offline suppression-escalation recommendation policy (`PULSE REMAP SUPPRESS PLAN:HOLD|ARM|LOCK`) without runtime coupling. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DR - Game Director Review (2026-03-25 21:50 KST, lane-cap forced underrepresented pick)
- Coverage check (last 10 completions by lane): systems=5, qa=4, vfx=4, ai-content=3, combat=2, ux=2, world=0, design=0.
- Lane cap breach: systems (50%) > 40%; forced next experiment into an underrepresented lane family.
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, UX/VFX): Add compact suppression-plan alias token (`PRSP:<H|A|L>`) for faster digest scanability.
- Idea 2 (mid risk, AI Content/VFX): Add offline suppression-escalation recommendation token (`PULSE REMAP SUPPRESS PLAN:HOLD|ARM|LOCK`) from suppression streak + drift-risk + lane cadence.
- Idea 3 (high risk, Design/World): Prototype ambient scene-reactive pulse remap flavor text remap table for portal narration (offline artifact only).
- Selected experiment: Idea 2 (minimal vertical slice, additive + reversible).
- [x] AI Content/VFX Team: Ship offline suppression-escalation recommendation token (`PULSE REMAP SUPPRESS PLAN:HOLD|ARM|LOCK`) plus compact alias (`PRSP:<H|A|L>`) behind `DOTPIO_EXPERIMENT_PULSE_REMAP_SUPPRESSION_PLAN_ALIAS` with regression lock.
- [x] Design/World Team: Prototype ambient scene-reactive pulse-remap flavor mapping (`CALM|BRACE|LOCK`) for digest readability copy.
- [x] Systems/Ops Team: Add lane-cadence guardrail row for suppression-plan family churn drift (`PRSP FAMILY TREND`) with prior-window context. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-25 22:35 KST)*

## Cycle DS - Game Director Review (2026-03-25 22:42 KST)
- Coverage check (last 10 completions): systems/qa lane remained dominant, so this cycle prioritized a design/world-facing readability cue while keeping the slice additive.
- Idea 1 (low risk, Design/World): Add digest confidence cue for suppression scene mapping (PULSE REMAP SCENE CONF:LOW|MED|HIGH).
- Idea 2 (mid risk, Combat/UX): Add compact suppression posture warning token for combat readability handoff.
- Idea 3 (high risk, AI Content/World): Prototype scene-reactive narrative microline generator from suppression-plan cadence memory (offline artifact).
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Design/World Team: Add suppression-scene confidence cue token (PULSE REMAP SCENE CONF:LOW|MED|HIGH) with payload signals and regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Combat/UX Team: Prototype compact suppression posture warning token for combat readability handoff (offline-only, gated). *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-25 23:01 KST)*
- [x] AI Content/World Team: Prototype scene-reactive narrative microline generator from suppression-plan cadence memory (offline artifact).

## Cycle DT - Game Director Review (2026-03-26 00:01 KST)
- Coverage check (last 10 completions): suppression-readability work remained systems/qa-heavy; this cycle forced an underrepresented Combat/UX handoff-facing slice while staying offline-only.
- Idea 1 (low risk, Combat/UX): Add suppression microline cadence token (`PULSE REMAP SCENE MICROLINE CADENCE:RISE|HOLD|COOL`) for one-glance warning posture scan.
- Idea 2 (mid risk, Systems/QA): Add cadence token-family trend drift row (`PRSMC FAMILY TREND`) with prior-window context.
- Idea 3 (high risk, AI Content/World): Prototype dual-line narrative microline variant pack with confidence-aware fallback copy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/UX Team: Add suppression microline cadence token (`PULSE REMAP SCENE MICROLINE CADENCE:RISE|HOLD|COOL`) with payload signals + markdown rows + regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add cadence token-family trend drift row (`PRSMC FAMILY TREND`) with prior-window context. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/World Team: Prototype dual-line narrative microline variant pack with confidence-aware fallback copy (offline-only). *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DU - Game Director Review (2026-03-26 01:01 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for `PULSE REMAP SCENE MICROLINE VARIANT PACK:` with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/World): Add compact variant-pack selection alias (`PRSMV:PRI|ALT|FBK`) behind flag for digest scanability.
- Idea 3 (high risk, AI Content/World): Prototype offline microline-style diversification policy from cadence-memory volatility windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `PULSE REMAP SCENE MICROLINE VARIANT PACK:` and lock via regression. *(lifecycle: [ ] -> [~] -> [x])* 
- [x] UX/World Team: Prototype compact variant-pack selection alias (`PRSMV:PRI|ALT|FBK`) behind flag for digest scanability. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 01:37 KST)*
- [x] AI Content/World Team: Prototype offline microline-style diversification policy from cadence-memory volatility windows. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 02:02 KST)*

## Cycle DV - Game Director Review (2026-03-26 02:08 KST)
- Idea 1 (low risk, UX/World): Add compact style-policy alias token (`PRSMP:<A|B|D>`) behind flag for digest scanability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `PULSE REMAP SCENE MICROLINE STYLE POLICY:` + `PRSMP:`.
- Idea 3 (high risk, AI Content/World): Prototype offline cadence-memory volatility smoothing policy to reduce style-policy oscillation across windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact style-policy alias token (`PRSMP:<A|B|D>`) behind `DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_STYLE_POLICY_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 02:08 KST)*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `PULSE REMAP SCENE MICROLINE STYLE POLICY:` + `PRSMP:`. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 02:33 KST)*
- [x] AI Content/World Team: Prototype offline cadence-memory volatility smoothing policy for style-policy oscillation control. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 02:33 KST)*

## Cycle DW - Game Director Review (2026-03-26 02:34 KST)
- Idea 1 (low risk, Systems/QA): Add style-policy family trend drift row (`PRSMP FAMILY TREND`) with prior-window context.
- Idea 2 (mid risk, AI Content/World): Add style-policy smoothing parity token (`PULSE REMAP SCENE MICROLINE STYLE POLICY SMOOTH`) for oscillation visibility.
- Idea 3 (high risk, Combat/UX): Prototype style-policy-aware posture warning escalation hook for readability pacing.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add style-policy family trend drift row (`PRSMP FAMILY TREND`) with prior-window context + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 02:34 KST)*

## Cycle DX - Game Director Review (2026-03-26 03:01 KST)
- Idea 1 (low risk, Systems/QA): Add offline style-policy posture token (`PULSE REMAP SCENE MICROLINE STYLE POSTURE:CALM|WARN|ALERT`) from smoothed style policy + family-trend drift for one-glance pacing triage.
- Idea 2 (mid risk, UX/World): Add compact alias (`PRSMP POSTURE:<C|W|A>`) behind flag for tighter digest scanability.
- Idea 3 (high risk, AI Content/Combat): Prototype style-policy-aware suppression posture escalation hook for combat warning copy coupling.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add offline style-policy posture token (`PULSE REMAP SCENE MICROLINE STYLE POSTURE:CALM|WARN|ALERT`) to weekly digest payload + markdown + regression lock. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DY - Game Director Review (2026-03-26 03:31 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for style-posture alias (`PRSMPP:`) with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/World): Add compact style-posture alias token (`PRSMPP:<C|W|A>`) behind flag for tighter digest scanability.
- Idea 3 (high risk, AI Content/Combat): Prototype style-posture-aware suppression escalation hook recommendation policy from trend momentum.
- Selected experiment: Idea 2 (minimal vertical slice).
- [x] UX/World Team: Add compact style-posture alias token (`PRSMPP:<C|W|A>`) behind `DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_STYLE_POSTURE_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 03:36 KST)*

## Cycle DZ - Game Director Review (2026-03-26 03:45 KST, lane-cap forced underrepresented pick)
- Coverage check (last 10 completions by lane): systems=4, qa=4, world=5, ux=3, ai-content=3, combat=0, design=0, vfx=0.
- Lane cap breach: world (50%) > 40%; forced next experiment into underrepresented lanes (combat/design/vfx).
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Combat/VFX): Add offline glint cue token (`PULSE REMAP SCENE FX GLINT:SOFT|VOID|SPIKE`) from style posture + suppression warning + scene confidence.
  - Player fantasy target: "my warnings visually breathe with danger level".
  - Expected impact metric: faster one-glance triage in digest playtest reviews; reduce ambiguous warning rows.
  - Scope: S | Risk: low | Rollback: remove token row + payload keys.
  - Pass/fail: pass if regression and digest generation stay green and token row appears in markdown + JSON.
- Idea 2 (mid risk, Design/World): Add glint-linked narrative palette recommendation (`COOL|ASH|SCAR`) for scene-copy flavor parity.
  - Player fantasy target: atmospheric scene tone coherence.
  - Metric: higher copy-consistency in offline review notes.
  - Scope: M | Risk: medium | Rollback: keep recommendation offline-only behind digest field.
  - Pass/fail: pass if deterministic mapping survives regression without churn spike.
- Idea 3 (high risk, Systems/Ops + VFX): Add prior-window drift trend row for glint family with lane-cadence escalation hook.
  - Player fantasy target: predictable FX stability over long sessions.
  - Metric: reduced oscillation incidents in weekly drift snapshots.
  - Scope: M | Risk: high | Rollback: quarantine as optional trend row.
  - Pass/fail: pass if trend row remains stable and does not trigger false alerts.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Ship offline digest glint cue token (`PULSE REMAP SCENE FX GLINT:SOFT|VOID|SPIKE`) with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 03:45 KST)*
- [x] Systems/QA Team: Add prior-window trend drift row for `PULSE REMAP SCENE FX GLINT` token family with regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 04:05 KST)*
- [x] Design/World Team: Prototype glint-linked scene-copy palette recommendation (`COOL|ASH|SCAR`) as offline digest recommendation.
- [x] Combat/VFX Team: Prototype compact glint alias (`PRSFX:<S|V|P>`) behind flag for DOS-width scanability.

## Cycle EA - Game Director Review (2026-03-26 06:15 KST)
- Coverage check (last 10 completions): world/ux-heavy trend in recent digest readability slices; prioritize combat/vfx-facing low-risk slice for lane rebalance while staying additive.
- Idea 1 (low risk, Combat/VFX): Add compact kill-combo cadence debug token (`DMG COMBO:<n>x<HOT|WARM|COLD>`) behind flag for one-glance multi-kill pacing readability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMG COMBO:` with markdown triage row + regression lock.
- Idea 3 (high risk, AI Content/Combat): Prototype offline combo-window retune recommendation policy from kill-cadence volatility + threat pressure.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact kill-combo cadence debug token (`DMG COMBO:<n>x<HOT|WARM|COLD>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_DEBUG` with regression coverage. *(lifecycle: [~] -> [x]; completed: 2026-03-26 06:22 KST)*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMG COMBO:` with markdown triage row + regression lock. *(lifecycle: [~] -> [x]; completed: 2026-03-26 06:40 KST)*
- [x] AI Content/Combat Team: Prototype offline combo-window retune recommendation policy from kill-cadence volatility + threat pressure (offline-only). *(lifecycle: [ ] -> [x]; completed: 2026-03-26 06:40 KST)*

## Cycle EB - Game Director Review (2026-03-26 06:52 KST)
- Coverage check (last 10 completions): Systems/QA + combat instrumentation dominate; selected a player-facing readability pass with reversible flagging to keep combat/debug lane scanable.
- Idea 1 (low risk, Combat/UX): Add compact alias token for combo-window recommendation (`DCR:<T|H|E>`) to improve one-glance digest scanability.
- Idea 2 (mid risk, Systems/QA): Add confidence-band token-family churn coverage for combo-window recommendation confidence (`DMG COMBO WINDOW RETUNE CONF:` + compact alias).
- Idea 3 (high risk, AI Content/Combat): Prototype offline combo-chain narrative coach line linked to combo-window retune recommendation + pressure trend.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/UX Team: Add compact combo-window retune alias (`DCR:<T|H|E>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_RETUNE_ALIAS` with digest markdown row + token-family churn coverage + regression lock. *(lifecycle: [ ] -> [x]; completed: 2026-03-26 06:52 KST)*
- [x] Systems/QA Team: Add combo-window retune confidence token-family churn coverage (`DMG COMBO WINDOW RETUNE CONF:` + compact alias) with regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 07:01 KST)*
- [x] AI Content/Combat Team: Prototype offline combo-chain narrative coach line tied to combo-window retune + pressure trend (offline-only). *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 07:31 KST)*

## Cycle EE - Game Director Review (2026-03-26 08:02 KST)
- Coverage check (last 10 completions): systems/qa and combat instrumentation remain dominant; selected a low-risk systems/qa hygiene slice to harden digest readability contracts.
- Idea 1 (low risk, Systems/QA): Remove duplicate `PRSMP FAMILY TREND` markdown row and lock uniqueness with regression assertion.
- Idea 2 (mid risk, UX/World): Add compact style-posture family trend row (`PRSMPP FAMILY TREND`) for parity with style-policy trend visibility.
- Idea 3 (high risk, AI Content/Systems): Prototype offline de-dup normalizer that auto-collapses repeated digest lines before publish.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: De-duplicate `PRSMP FAMILY TREND` markdown emission and add regression guard (`count == 2` digest occurrences: summary + token-family section). *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 08:03 KST)*

## Cycle EF - Game Director Review (2026-03-26 08:31 KST)
- Coverage check (last 10 completions): systems/qa observability remained dominant; selected a low-risk combat-facing debug readability slice to maintain lane cadence balance.
- Idea 1 (low risk, Combat/UX): Add compact combo-confidence debug token (`DMG COMBO CONF:LOW|MID|HIGH`) behind flag for faster multi-kill trust read.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMG COMBO CONF:` with markdown triage row + regression lock.
- Idea 3 (high risk, AI Content/Combat): Prototype offline combo-confidence coach recommendation policy from kill heat volatility + pressure drift.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/UX Team: Add compact combo-confidence debug token (`DMG COMBO CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_DEBUG` with regression coverage. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 08:33 KST)*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMG COMBO CONF:` with markdown triage row + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 09:01 KST)*
- [x] AI Content/Combat Team: Prototype offline combo-confidence coach recommendation policy from kill heat volatility + pressure drift. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 09:31 KST; completed: 2026-03-26 09:39 KST)*

## Cycle EG - Game Director Review (2026-03-26 09:46 KST)
- Coverage check (last 10 completions): AI-content/combat + systems digest observability dominated; selected low-risk UX/combat readability slice to keep offline recommendations scanable and reversible.
- Idea 1 (low risk, Combat/UX): Add compact alias token for combo-confidence coach recommendation (`DCCR:<G|S|U>`) behind flag for digest scanability.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage row for `DMG COMBO CONF COACH REC` + alias contract in weekly digest.
- Idea 3 (high risk, AI Content/Combat): Prototype offline confidence-coach fallback narrative line chained to recommendation streak drift.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/UX Team: Add compact combo-confidence coach alias (`DCCR:<G|S|U>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_COACH_ALIAS` with digest markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 09:46 KST; completed: 2026-03-26 09:50 KST)*


## Cycle EH - Game Director Review (2026-03-26 10:08 KST, lane-cap forced underrepresented pick)
- Coverage check (last 10 completions by lane): combat=6, systems=4, qa=4, ux=3, ai-content=3, world=0, design=0, vfx=0.
- Lane cap breach: combat (60%) > 40%; forced next experiment into underrepresented lanes (design/world/vfx).
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Design/World): Add offline scene-arc cue token (`DMG COMBO CONF COACH SCENE ARC:ASH|IRON|EMBER`) mapped from combo-confidence coach recommendation + pressure/drift.
  - Player fantasy target: combat guidance reads like world tone, not raw telemetry.
  - Expected impact metric: fewer ambiguous coach rows in digest triage notes.
  - Scope: S | Risk: low | Rollback: remove row + payload keys (offline-only).
  - Pass/fail: pass if digest markdown/json include deterministic scene-arc cue and regression stays green.
- Idea 2 (mid risk, Combat/VFX): Add compact coach-scene alias (`DCCSA:<A|I|E>`) behind flag for dense digest scanability.
  - Player fantasy target: instant one-token mood read in combat review.
  - Expected impact metric: faster parse time in playtest postmortems.
  - Scope: S | Risk: medium | Rollback: disable/remove flag-gated alias.
  - Pass/fail: pass if alias appears only when flag enabled and contracts remain stable.
- Idea 3 (high risk, Systems/Ops): Add 24h lane-cadence miss predictor (`LANE CADENCE MISS RISK:LOW|MID|HIGH`) from rolling completion spread.
  - Player fantasy target: maintain variety rhythm without manual policing.
  - Expected impact metric: reduced cadence misses across daily cycles.
  - Scope: M | Risk: high | Rollback: quarantine as optional digest advisory.
  - Pass/fail: pass if predictor is stable across prior-window replay without false HIGH spikes.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Design/World Team: Add offline scene-arc cue token (`DMG COMBO CONF COACH SCENE ARC:ASH|IRON|EMBER`) with payload + markdown + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 10:01 KST; completed: 2026-03-26 10:08 KST)*

## Cycle EI - Game Director Review (2026-03-26 12:31 KST)
- Coverage check (last 10 completions): world/design readability tokens progressed while systems/qa digest contract parity remained the lowest-risk closure lane.
- Idea 1 (low risk, UX/World): Add compact cadence alias token (`PRSMC:<R|H|C>`) behind flag for one-glance scanability of `PULSE REMAP SCENE MICROLINE CADENCE`.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage row for cadence alias family (`PRSMC + PULSE REMAP SCENE MICROLINE CADENCE`) with regression lock.
- Idea 3 (high risk, AI Content/Combat): Prototype offline cadence-reactive coach-copy swap policy tied to `PRSMC` trend volatility.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact cadence alias token (`PRSMC:<R|H|C>`) behind `DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_CADENCE_ALIAS`, wire payload/markdown rows, and lock via regression. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 12:31 KST; completed: 2026-03-26 12:39 KST)*
- [x] Systems/QA Team: Add explicit cadence-alias family trend markdown triage row (`PRSMC FAMILY CHURN`) adjacent to `PRSMC FAMILY TREND` in weekly digest summary.
- [x] AI Content/Combat Team: Prototype offline cadence-reactive coach-copy swap recommendation policy from `PRSMC` family churn + lane cadence miss risk.

## Cycle EJ - Game Director Review (2026-03-26 13:31 KST)
- Coverage check (last 10 completions): cadence alias observability landed; best low-risk closure was AI Content/Combat policy wiring using existing digest signals.
- Idea 1 (low risk, AI Content/Combat): Add offline cadence-reactive coach-copy swap recommendation token (`DMG COMBO CONF COACH COPY SWAP REC:HOLD_COPY|ARM_SWAP|SWAP_NOW`) derived from `PRSMC` churn + lane cadence miss risk.
- Idea 2 (mid risk, Systems/QA): Add dedicated token-family churn summary row for swap recommendation family in digest markdown.
- Idea 3 (high risk, UX/Design): Prototype compact swap rationale microline alias for dense digest budgets.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] AI Content/Combat Team: Add offline cadence-reactive coach-copy swap recommendation policy from `PRSMC` churn + lane cadence miss risk with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 13:24 KST; completed: 2026-03-26 13:31 KST)*
- [x] Systems/QA Team: Add swap-recommendation token-family churn row (`DMG COMBO CONF COACH COPY SWAP REC FAMILY CHURN`) and keep it adjacent to recommendation trend lines. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 13:31 KST)*
- [x] UX/Design Team: Keep recommendation vocabulary compact (`HOLD_COPY|ARM_SWAP|SWAP_NOW`) for DOS-width digest readability while staying offline-only.
- [x] Systems/QA Team: Add prior-window drift trend row for `DMG COMBO CONF COACH COPY SWAP REC` family to separate net direction vs churn magnitude.
- [x] UX/Design Team: Prototype compact swap alias token (`DCCSR:<H|A|S>`) behind experiment flag for dense digest budgets. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 15:42 KST; completed: 2026-03-26 15:46 KST)*

## Cycle EK - Game Director Review (2026-03-26 15:52 KST)
- Idea 1 (low risk, UX/Design): Add compact copy-swap trend alias token (`DCCST:<U|F|D>`) behind flag for faster digest trend scanability.
- Idea 2 (mid risk, Systems/QA): Add dedicated token-family churn split row for `DCCSR` vs `DCCST` to separate recommendation-vs-trend noise.
- Idea 3 (high risk, AI Content/Combat): Prototype offline copy-swap trend hysteresis policy to suppress rapid `UP/DOWN` oscillation.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Design Team: Add compact copy-swap trend alias token (`DCCST:<U|F|D>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_COACH_COPY_SWAP_TREND_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 15:48 KST; completed: 2026-03-26 15:52 KST)*
- [x] Systems/QA Team: Add split family churn rows (`DCCSR FAMILY CHURN`, `DCCST FAMILY CHURN`) for recommendation-vs-trend triage.
- [x] AI Content/Combat Team: Prototype offline copy-swap trend hysteresis policy for `UP/DOWN` oscillation dampening.
## Cycle EL - Game Director Review (2026-03-26 16:12 KST, lane-cap forced underrepresented pick)
- Coverage check (last 10 completions by lane): systems=3, world=2, ai-content=2, combat=2, design=5, vfx=0, ux=5, qa=2.
- Lane cap breach: design/ux at 50% (>40%); forced next experiment into underrepresented lane family (combat/vfx first, with vfx at 0%).
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Combat/VFX): Add offline combo-confidence FX accent token (`DMG COMBO CONF FX ACCENT:SMOKE|STEEL|EMBER`) from scene arc + fallback volatility regime.
  - Player fantasy target: coaching tone and visual accent read as one signal in postmortems.
  - Expected impact metric: fewer ambiguous “which vibe should this warning feel like?” notes.
  - Scope: S | Risk: low | Rollback: remove row + payload keys + alias family.
  - Pass/fail: pass if markdown/json expose deterministic accent token and regression remains green.
- Idea 2 (mid risk, Systems/QA): Add dedicated family trend split for FX accent alias churn to distinguish stable palette vs noisy alias toggles.
- Idea 3 (high risk, Design/World): Prototype scene-arc-to-palette narrative harmonizer that mutates fallback lines by lane cadence pressure.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Ship offline `DMG COMBO CONF FX ACCENT:SMOKE|STEEL|EMBER` token plus compact alias `DCCFX:<S|T|E>` behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_ALIAS` (digest-only, reversible) with regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 16:12 KST)*
- [x] Systems/QA Team: Add split family churn rows for `DCCSA` vs `DCCFX` to isolate scene-arc vs fx-accent noise.
- [x] AI Content/Combat Team: Prototype offline accent hysteresis rule to reduce STEEL/EMBER bounce during SWING volatility windows.

## Cycle EM - Game Director Review (2026-03-26 17:10 KST)
- Idea 1 (low risk, Systems/QA): Add `DCCFX FAMILY TREND` prior-window drift row so FX-accent direction (`UP|DOWN|FLAT`) is auditable, not just churn.
- Idea 2 (mid risk, UX/Combat): Add compact FX-accent trend alias token (`DCCFXT:<U|F|D>`) behind flag for digest scanability.
- Idea 3 (high risk, AI Content/Combat): Prototype offline accent trend hysteresis policy that adapts threshold by volatility regime.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add `DCCFX FAMILY TREND` markdown + JSON signals (`currentNet`, `priorNet`, `Δnet`, `reason`) with regression lock. *(lifecycle: [~] -> [x]; completed: 2026-03-26 17:18 KST)*
- [x] UX/Combat Team: Prototype compact FX-accent trend alias (`DCCFXT:<U|F|D>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_TREND_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 17:31 KST)*
- [x] AI Content/Combat Team: Prototype volatility-aware accent trend hysteresis policy (offline-only). *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 18:01 KST; completed: 2026-03-26 18:07 KST)*

## Cycle EN - Game Director Review (2026-03-26 18:31 KST)
- Idea 1 (low risk, UX/Combat): Add compact hysteresis alias token (`DCCFXH:<H|A><L|M|H>`) behind flag for one-glance digest scanability.
- Idea 2 (mid risk, Systems/QA): Add dedicated token-family churn coverage row for hysteresis recommendation/confidence pair.
- Idea 3 (high risk, AI Content/Combat): Prototype offline adaptive hysteresis confidence floor by lane-cadence miss risk.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Combat Team: Add compact hysteresis alias token (`DCCFXH:<H|A><L|M|H>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_TREND_HYS_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 18:31 KST; completed: 2026-03-26 18:37 KST)*

## Cycle EO - Game Director Review (2026-03-26 19:10 KST)
- Coverage check (last 10 completions): digest-heavy systems/ux cadence continued; selected low-risk systems/ops observability slice that stays reversible and supports faster scan.
- Idea 1 (low risk, Systems/Ops): Add compact lane cadence miss-risk alias (`LCMR:<L|M|H>`) behind flag for dense digest scanability.
- Idea 2 (mid risk, QA/Design): Add contract/order lock ensuring `LCMR` remains adjacent to `LANE CADENCE MISS RISK` in both markdown sections.
- Idea 3 (high risk, AI Content/Systems): Prototype offline adaptive lane-priority hysteresis floor tied to sustained `LCMR:H` streaks.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/Ops Team: Add compact lane cadence miss-risk alias (`LCMR:<L|M|H>`) behind `DOTPIO_EXPERIMENT_LANE_CADENCE_MISS_RISK_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 19:03 KST; completed: 2026-03-26 19:10 KST)*
- [x] QA/Design Team: Add explicit adjacency/order regression lock for `LANE CADENCE MISS RISK` -> `LCMR` in summary + token-coverage sections. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 19:32 KST; completed: 2026-03-26 19:34 KST)*
- [x] AI Content/Systems Team: Prototype offline `LCMR` streak-aware lane-priority hysteresis floor recommendation (`LPR HYS FLOOR REC:HOLD|RAISE`) with rollback-safe digest-only wiring.

## Cycle EP - Game Director Review (2026-03-26 20:01 KST)
- Coverage check (last 10 completions): systems/qa + ai-content observability remained dominant; selected a compact UX-facing digest readability slice to keep lane handoff scanable.
- Idea 1 (low risk, UX/Systems): Add compact alias token for hysteresis-floor recommendation (`LPR HYS FLOOR:<H|R>`) behind flag for digest density control.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage row for `LPR HYS FLOOR REC:` + alias with regression lock.
- Idea 3 (high risk, AI Content/Systems): Prototype offline adaptive floor-raise threshold policy from `LCMR` streak momentum + lane volatility regime.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact hysteresis-floor recommendation alias token (`LPR HYS FLOOR:<H|R>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_FLOOR_REC_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 20:01 KST)*
- [x] Systems/QA Team: Add token-family churn coverage row for `LPR HYS FLOOR REC:` + `LPR HYS FLOOR:` with regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 21:12 KST)*
- [x] AI Content/Systems Team: Prototype offline adaptive `LPR HYS FLOOR REC` threshold policy from `LCMR` streak momentum + lane volatility regime (digest-only). *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 21:16 KST)*

## Cycle ER - Game Director Injection (2026-03-26 21:41 KST)
- [x] Combat/VFX Team: Add compact FX volatility alias token (`DCCFXV:<C|S|P>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_VOLATILITY_ALIAS` with payload/markdown wiring + regression lock. *(completed: 2026-03-26 21:41 KST)*
- [x] Systems/QA Team: Add `DCCFXV FAMILY CHURN` markdown/token-coverage row with adjacency lock after `DCCFXH` rail.
- [x] Design/World Team: Add legend/readability annotation for `DCCFXV` mapping (`C=CALM`, `S=SWING`, `P=SPIKE`) in digest docs.

## Cycle ET - Game Director Review (2026-03-27 00:10 KST)
- Coverage check (last 10 completions): systems/qa remained overrepresented, so this cycle prioritized a lightweight UX/readability slice that exposes guard-threshold posture without runtime coupling.
- Idea 1 (low risk, UX/Design): Surface compact guard-threshold token (`LPRCG THRESH:<n>`) in weekly digest for faster operator triage.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage for `LPRCG THRESH:` with compact alias wiring and regression lock.
- Idea 3 (high risk, AI Content/World): Prototype narrative lane coach line when confidence guard stays armed across ≥3 windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Design Team: Add digest token `LPRCG THRESH:<n>` from adaptive confidence-guard threshold policy with payload+markdown wiring and regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 00:06 KST; completed: 2026-03-27 00:10 KST)*
- [x] Systems/QA Team: Add token-family churn coverage for `LPRCG THRESH:` and keep adjacency with `LPRCG` rows. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 00:31 KST; completed: 2026-03-27 00:33 KST)*
- [x] AI Content/World Team: Prototype offline guard-persistence coaching cue when `LPRCG` remains `APPLY` for consecutive windows. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 01:03 KST; completed: 2026-03-27 01:05 KST)*

## Cycle EU - Game Director Review (2026-03-27 01:08 KST)
- Coverage check (last 10 completions): systems/qa cadence remained dominant, so this cycle forced a lightweight AI Content/World readability slice to keep lane coaching actionable in dense digests.
- Idea 1 (low risk, UX/Systems): Add compact guard-persistence coach alias token (`LPRCGC:<R|W|S>`) behind flag for digest scanability.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage/order lock for `LPRCG COACH:` + `LPRCGC:` rows.
- Idea 3 (high risk, AI Content/World): Prototype offline adaptive coach-copy variant pack tied to prolonged `LPRCG:APPLY` streak + volatility regime transitions.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact guard-persistence coach alias token (`LPRCGC:<R|W|S>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_COACH_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 01:06 KST; completed: 2026-03-27 01:08 KST)*
- [x] Systems/QA Team: Add explicit adjacency/order regression lock for `LPRCG COACH` -> `LPRCGC` in summary + token-coverage sections. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-27 01:20 KST)*
- [x] AI Content/World Team: Prototype offline adaptive guard-persistence coach copy variant-pack policy from sustained `LPRCG:APPLY` streak depth.

## Cycle EV - Game Director Review (2026-03-27 02:10 KST)
- Coverage check (last 10 completions): systems/qa + ai-content digest policy lane remained dominant; selected compact UX/systems readability slice to keep new coach-pack signal scanable.
- Idea 1 (low risk, UX/Systems): Add compact guard-persistence coach-pack alias token (`LPRCGCP:<B|A|N>`) behind flag for dense digest scanability.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage row for `LPRCG COACH PACK:` + alias and lock with regression.
- Idea 3 (high risk, AI Content/World): Prototype offline adaptive coach-copy narrative line from coach-pack + volatility-regime transitions.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact guard-persistence coach-pack alias token (`LPRCGCP:<B|A|N>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_COACH_PACK_ALIAS` with payload/markdown wiring + regression lock.
- [x] Systems/QA Team: Add token-family churn coverage row for `LPRCG COACH PACK:` + `LPRCGCP:` with regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-27 02:31 KST)*
- [x] AI Content/World Team: Prototype offline adaptive coach-copy narrative line from coach-pack + volatility regime transitions. *(started: 2026-03-27 03:01 KST, completed: 2026-03-27 03:08 KST)*

## Cycle EW - Game Director Review (2026-03-27 03:12 KST)
- Coverage check (last 10 completions): systems/qa + ai-content digest-policy lane remains dominant; selected low-risk compact readability slice to keep newly-added coach-copy cue scanable.
- Idea 1 (low risk, UX/Systems): Add compact coach-copy alias token (`LPRCGCN:<R|B|A|N>`) behind flag for dense digest scanning.
- Idea 2 (mid risk, Systems/QA): Add family-churn coverage row/order lock for `LPRCG COACH COPY:` + alias.
- Idea 3 (high risk, AI Content/World): Prototype flagged rationale token `LPRCG COACH COPY WHY:<short>`.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact coach-copy alias token (`LPRCGCN:<R|B|A|N>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_COACH_COPY_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 03:10 KST; completed: 2026-03-27 03:12 KST)*
- [x] Systems/QA Team: Add token-family churn coverage + adjacency lock for `LPRCG COACH COPY:` + `LPRCGCN:` rows in summary and token-coverage sections. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 03:31 KST; completed: 2026-03-27 03:50 KST)*
- [x] AI Content/World Team: Prototype flagged rationale token `LPRCG COACH COPY WHY:<short>` for offline coaching context. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 03:55 KST; completed: 2026-03-27 04:03 KST)*


## Cycle EX - Game Director Review (2026-03-27 04:03 KST)
- Coverage check (last 10 completions): systems=6, qa=4, ai-content=3, world=2, ux=2, combat=1, design=1, vfx=1. Systems exceeded 40%, so this cycle forced underrepresented lane selection.
- 24h cadence check: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, AI Content/World): Ship flagged rationale token `LPRCG COACH COPY WHY:<short>` to explain coach-copy intent at scan speed.
- Idea 2 (mid risk, Combat/VFX): Add compact flash cue alias from `DCCFX` + volatility (`DCCFXC:<H|T|M>`), digest-only + flag gated.
- Idea 3 (high risk, Design/World): Add scene-arc text palette recommendation from `LPRCG COACH COPY WHY` + regime transitions.
- Selected experiment: Idea 1 (forced underrepresented lane, minimal vertical slice).
- [x] AI Content/World Team: Implement flagged `LPRCG COACH COPY WHY:<short>` token + payload signals + markdown rows + regression assertions.
- [x] Systems/QA Team: Add adjacency/order lock so `LPRCG COACH COPY:` → `LPRCGCN:` → `LPRCG COACH COPY WHY:` is deterministic in summary + token coverage.
- [x] Combat/VFX Team: Prototype optional compact cue alias from `DCCFX` volatility to bridge coach-copy rationale and FX accent triage. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 04:34 KST; completed: 2026-03-27 04:40 KST)*

## Cycle EY - Game Director Review (2026-03-27 04:41 KST)
- Coverage check (last 10 completions): systems/qa still leads; force player-facing combat/vfx readability slice this cycle.
- Idea 1 (low risk, Combat/VFX): Add compact bridge rationale alias `DCCFXCW:<R|S|F|B>` derived from `LPRCG COACH COPY WHY` for FX triage scan speed.
- Idea 2 (mid risk, Systems/QA): Lock adjacency `DCCFXV -> DCCFXC -> DCCFXCW` in summary + token coverage.
- Idea 3 (high risk, Design/World): Generate scene copy palette hints from DCC cue mode + volatility transitions.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact bridge rationale alias token `DCCFXCW:<R|S|F|B>` with payload + markdown wiring + regression coverage. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 04:41 KST; completed: 2026-03-27 04:48 KST)*
- [ ] Systems/QA Team: Add deterministic adjacency/order lock for `DCCFXV` -> `DCCFXC` -> `DCCFXCW` rows in summary + token coverage.
- [ ] Design/World Team: Prototype scene copy palette hint token driven by `DCCFXCW` transitions.
