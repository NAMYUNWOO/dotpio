# POST_RC_BACKLOG

Last updated: 2026-03-21 02:31 KST

## P0 (Now)
- [x] Replace F9-centric build flow with Enter->Action menu primary flow
- [x] Hide/disable `USE` for BUILDER.SRL and provide explicit build-only guidance
- [x] Add build preview panel clarity pass (materials consumed, SRL, expected category)

## P1 (Gameplay)
- [x] World Team: Redesign map_03~07 to be visually/tactically distinct (silhouette, lane structure, encounter rhythm)
- [x] World Team: Reposition portals with logical progression rules (clear return paths, risk/reward routing, landmark-based placement)
- [x] Add map_07 with new tactical pattern and portal integration
- [x] Add 2 new enemy archetypes with synergy behavior
- [x] Add mission variety pack (at least +5 objectives)

## P2 (Ops)
- [x] Add weekly sustain audit JSON pretty mode
- [x] Add sustain health dashboard markdown report
- [x] Add automatic stale-branch/report drift check
- [x] Add sustain health dashboard JSON output mode (compact + pretty) and wire weekly runner artifact output
- [x] Add sustain dashboard trend classification (improving/stable/degrading) with regression coverage

## P1 (Gameplay Follow-up)
- [x] Surface active mission-pack id + momentum streak in HUD/run-summary for clearer run pacing readability
- [x] Add mission momentum lane-switch variety bonus (+1 BUILDER.SRL on consecutive objective completions from different lanes)
- [x] Add mission-pack flavor descriptors and surface compact tag in HUD/run-summary

## P1 (Combat Experiment)
- [x] Combat Team: Add berserker desperation behavior (low-HP speed/damage spike) with regression coverage
- [x] UX/Combat Team: Telegraph berserker desperation state in HUD + combat status feed
- [x] Combat Team: Add one-turn pre-lunge tell for berserker desperation attacks (readability/fairness A/B)
- [x] Combat Team: Add one-turn post-lunge recovery window for berserker desperation chain (readability/fairness follow-up)
- [x] UX/Combat Team: Surface active berserker recovery-window count in HUD threat strip

## P1 (Gameplay Experiment Queue)
- [x] UX/Systems Team: Add mission lane-switch preview hint in HUD so players can anticipate variety bonus (+1 BUILDER.SRL)
- [x] UX/Systems Team: Track and surface mission lane-switch variety bonus count in HUD/run-summary

## P1 (Combat Readability Follow-up)
- [x] UX/Combat Team: Add weighted berserker threat index in HUD threat strip (`THREAT:<n>`) to summarize active desperation pressure
- [x] UX/Combat Team: Add berserker threat-tier label (`THREAT LVL:LOW|MED|HIGH`) in HUD for score readability
- [x] UX/Combat Team: Color-code berserker threat-tier label in HUD (`LOW`=green, `MED`=amber, `HIGH`=red) for faster parsing
- [x] UX/Combat Team: Add compact berserker threat formula legend in HUD/combat status (`THREAT = BERSERK + 2*LUNGE + RECOVER`)
- [x] UX/Combat Team: Add turn-over-turn berserker threat delta indicator in HUD (`THREAT Δ:+n|-n`) for pacing readability

## P1 (Next Gameplay Wave)
- [x] UX/Combat Team: Add threat-aware onboarding micro-tip decay logic (show `COMBAT TIP` after first build until first threat event)
- [x] Systems/Combat Team: Add mission-chain pressure breaker bonus (objective completion on rising threat grants short dodge charge)
- [x] World/Design Team: Add overclock hazard room prototype (SRL discount pulse + aggro spike risk)
- [x] UX/World Team: Add overclock hazard countdown readability pass (active pulse + cooldown seconds in HUD hint)

## P2 (Ops/Telemetry Next)
- [x] QA/Systems: Add weekly changelog drift detector (code changes without corresponding team-log/report entry)
- [x] Ops: Add sustain dashboard “regression risk score” (0~100) with threshold alert section
- [x] Ops: Add sustain dashboard regression-risk driver breakdown (top contributors) in markdown/json with regression coverage

## P1 (Hazard Readability Follow-up)
- [x] UX/World Team: Add overclock hazard risk-tier label + countdown legend in HUD hint (`RISK:LOW|MED|HIGH`)
- [x] UX/Combat Team: Add explicit overclock aggro-pressure legend in HUD hint (`AGGRO DET:+n MOVE:+m%`) during active pulse
- [x] UX/World Team: Add overclock pulse-imminent warning in cooldown HUD hint when standing in hazard zone (`IMMINENT:<n>s`)

## P1 (Hazard Reward Follow-up)
- [x] Systems/World Team: Add overclock hot-zone kill bounty (`+BUILDER.SRL` per kill, pulse-capped) to reinforce risk/reward combat commitment
- [x] UX/Systems Team: Surface overclock bounty pulse cap progress in HUD hint (`BOUNTY:x/y`) during HOT state
- [x] UX/Systems Team: Surface next-pulse bounty budget token in READY/CD hints (`NEXT BOUNTY:0/y`) for reward planning

## P1 (Hazard Readability Wave 2)
- [x] UX/World Team: Color-code overclock `RISK` tier in HUD hint (`LOW`=green, `MED`=amber, `HIGH`=red) while preserving compact DOS line layout

## P1 (Hazard Readability Wave 3)
- [x] UX/Systems Team: Add compact overclock risk-factor breakdown token in HUD hint (`RISK SRC:Dx+DETy+MOVEz`) so tuning impact is readable in-run

## P1 (Hazard Readability Wave 4)
- [x] UX/World Team: Add overclock pulse ETA token in READY/CD HUD hints (`NEXT PULSE:<n>s`) so re-entry timing is legible

## P1 (Hazard Readability Wave 5)
- [x] UX/World Team: Add pulse progress token in overclock HUD hints (`PULSE:%`/`RECHARGE:%`) for glanceable timing read

## P1 (Hazard Readability Wave 6)
- [x] UX/World Team: Add overclock risk-trend token in READY/CD/HOT hints (`RISK Δ:+n|-n`) to show pressure shift from baseline at a glance

## P1 (Hazard Readability Wave 7)
- [x] UX/World Team: Add overclock zone-presence token in HUD hints (`ZONE:IN|OUT`) so risk context remains clear when near/inside hazard

## P1 (Hazard Readability Wave 8)
- [x] UX/World Team: Add overclock zone exposure-duration token in HUD hints (`EXPOSED:<n>s`) so in-zone commitment risk is glanceable

## P1 (Hazard Readability Wave 9)
- [x] UX/World Team: Add overclock exposure commitment-tier token in HUD hints (`COMMIT:LOW|MID|HIGH`) derived from `EXPOSED` duration for faster risk read

## P1 (Hazard Readability Wave 10)
- [x] UX/World Team: Add overclock risk-delta color semantics in HUD hint (rising=red, cooling=green) to improve commit/retreat readability
- [x] UX/World Team: Add overclock pulse-end relief burst (+short "WINDOW" token) after exiting HOT zone to reward disengage timing
- [x] Systems/Telemetry Team: Log overclock zone dwell buckets (`LOW|MID|HIGH`) per run for exposure-driven tuning evidence

## P1 (Game Director Injection — 2026-03-20)
- [x] UX/Systems Team: Surface overclock dwell-bucket snapshot in run summary (`DWELL L/M/H`) for immediate post-run tuning readability
- [x] Systems/Design Team: Add overclock zone reward-efficiency token (`SRL/EXPOSED sec`) to run summary for risk/reward pacing insight
- [x] QA/Systems Team: Add multi-run dwell trend combiner artifact (`last N run medians`) for balance review cadence

## P1 (Game Director Injection — 2026-03-20 Cycle B)
- [x] UX/Design Team: Add run-summary overclock commitment profile token (`PROFILE:CAUTIOUS|BALANCED|ALL-IN`) from dwell mix for fast post-run coaching
- [x] Systems Team: Add overclock dwell trend volatility token (`VOL:STEADY|SWING`) to trend artifact for tuning cadence triage
- [x] QA/UX Team: Add compact run-summary tooltip glossary row for overclock analytics tokens (`DWELL`, `EFF`, `PROFILE`)

## P1 (Game Director Injection — 2026-03-21 Cycle C)
- [x] UX/Systems Team: Add run-summary overclock coach cue token (`COACH:<tip>`) derived from `PROFILE + EFF` for immediate post-run adjustment guidance
- [x] Systems/Combat Team: Prototype threat-linked momentum bonus scaler (`VAR bonus +1->+2` when `THREAT LVL:HIGH` objective clear) behind experiment flag
- [x] World/Design Team: Prototype hazard room route tag (`SAFE|RISK|SPIKE`) in map metadata and HUD mini-callout for path planning

## P1 (Game Director Injection — 2026-03-21 Cycle D)
- [x] UX/World Team: Color-code hazard route mini-callout token (`SAFE`=green, `RISK`=amber, `SPIKE`=red) for faster path-choice readability
- [x] Systems/World Team: Add portal-hover route preview token (`NEXT ROUTE:<tag>`) in transition prompt before confirming map jump
- [x] QA/Design Team: Add route-tag distribution checker across hazard-enabled maps (warn if all maps converge on same route profile)

## P1 (Game Director Injection — 2026-03-21 Cycle E)
- [x] UX/World Team: Add portal route-coaching cue token in transition prompt (`COACH:LOW PRESSURE|BALANCED RISK|HIGH PRESSURE`) mapped from `NEXT ROUTE` for instant jump readability
- [x] Systems/World Team: Add route-tag density ledger artifact per map chain (`SAFE|RISK|SPIKE` counts by reachable portal graph depth)
- [x] QA/Design Team: Add portal prompt copy budget checker (warn when route preview line exceeds DOS compact width threshold)

## P1 (Game Director Injection — 2026-03-21 Cycle F)
- [x] UX/World Team: Add portal transition prompt compact fallback (`NEXT:<tag> COACH:<short>`) when copy budget is constrained
- [x] Systems/World Team: Add route-pressure score token in transition prompt (`PRESSURE:<n>`) derived from route tag + recent threat tier
- [x] QA/Design Team: Add transition prompt token-order linter (warn when readability order deviates from ACTION->ROUTE->COACH/PRESSURE)

## P1 (Game Director Injection — 2026-03-21 Cycle G)
- [x] Systems/World Team: Add route-pressure score token in transition prompt (`PRESSURE:<n>`) derived from route tag + recent threat tier
- [x] QA/Design Team: Add transition prompt token-order linter and budget parser (warn when token sequence deviates from `ACTION -> ROUTE -> COACH -> PRESSURE`)
- [x] World/Design Team: Prototype adaptive portal hint (`ALT ROUTE:<SAFE|RISK|SPIKE>`) suggesting a lower-pressure branch when current pressure is high

## P1 (Game Director Injection — 2026-03-21 Cycle H)
- [x] UX/Systems Team: Add adaptive portal pressure-drop token (`ALT DELTA:-n`) in transition prompt to quantify safer branch impact
- [x] Systems/World Team: Route-aware ALT selector v2 (pick lowest-pressure reachable branch among current-map portals, not just one-step fallback)
- [x] QA/UX Team: Add portal prompt readability regression for adaptive ALT token budget/order under HIGH threat compact mode

## P1 (Game Director Injection — 2026-03-21 Cycle I)
- [x] UX/World Team: Prototype adaptive portal nudge token (`ALT PLAN:LOWER RISK`) behind experiment flag for HIGH-pressure transitions
- [x] Systems/Combat Team: Prototype overclock retreat streak bonus (grant +1 temporary dodge after 2 consecutive safe disengages)
- [x] QA/Systems Team: Add weekly portal prompt readability drift digest (compact/detailed token stats over last N commits)

## P1 (Game Director Injection — 2026-03-21 Cycle J)
- [x] QA/UX Team: Add digest mode-trend token (`MODE TREND:COMPACT|DETAILED|BALANCED`) to weekly portal prompt readability report
- [x] Systems/World Team: Add pressure-band drift token (`PRESSURE BAND:LOW|MID|HIGH`) from recent portal prompt pressure score edits
- [x] Design/QA Team: Add digest top-token movers section (largest net ± token deltas) for readability triage

## P1 (Game Director Injection — 2026-03-21 Cycle K)
- [x] QA/UX Team: Add digest drift-risk token (`DRIFT RISK:LOW|MID|HIGH`) from compact/detailed imbalance + pressure churn for quick triage
- [x] Systems/World Team: Add prompt-token persistence token (`STICKY TOKENS:<n>`) counting tokens present in both added/removed sets over window
- [x] Design/QA Team: Add digest lane-focus token (`FOCUS:PORTAL|ALT|PRESSURE|MIXED`) from top mover families for action routing

## P1 (Game Director Injection — 2026-03-21 Cycle L)
- [x] Design/QA Team: Add digest route-action token (`ROUTE ACTION:PORTAL_AUDIT|ALT_TUNE|PRESSURE_REBASE|BALANCE_PASS|WATCH`) from `FOCUS + DRIFT RISK`
- [x] QA/Systems Team: Add lane-focus streak token (`FOCUS STREAK:<n>`) to flag single-lane churn persistence across digest windows
- [x] UX/Systems Team: Add lane-focus transition token (`FOCUS SHIFT:<FROM->TO>`) for weekly routing handoff clarity

## P1 (Game Director Injection — 2026-03-21 Cycle M)
- [x] QA/Systems Team: Add lane-focus volatility token (`FOCUS VOL:STEADY|SWING`) from lane-switch ratio over touched commits
- [x] Design/Systems Team: Add route-action confidence token (`ACTION CONF:LOW|MID|HIGH`) from focus dominance + drift-risk spread
- [x] QA/AI Content Team: Prototype digest anomaly pulse (`ANOMALY:ON`) when sticky token count and pressure churn spike simultaneously

## P1 (Game Director Injection — 2026-03-21 Cycle N)
- [x] Design/Systems Team: Add route-action confidence telemetry line in markdown + JSON (`ACTION CONF`, confidence signals)
- [x] QA/AI Content Team: Add anomaly confidence tier (`ANOMALY CONF:LOW|MID|HIGH`) to reduce binary alert noise
- [x] Design/QA Team: Add lane-lock alert token (`LANE LOCK:<lane>x<n>`) for prolonged single-lane drift streaks

## P1 (Game Director Injection — 2026-03-21 Cycle O)
- [x] QA/Systems Team: Add digest drift-momentum token (`DRIFT MOMENTUM:RISING|COOLING|FLAT`) comparing early-vs-late window risk-score averages
- [x] Design/Systems Team: Add route-action guardrail token (`ACTION GUARD:LOCK|SOFT`) when confidence is LOW under HIGH drift risk
- [x] QA/Design Team: Add lane-focus entropy token (`FOCUS ENTROPY:LOW|MID|HIGH`) from normalized lane score spread

## P1 (Game Director Injection — 2026-03-21 Cycle P)
- [x] UX/Design Team: Add focus-balance token (`FOCUS BAL:<n>%`) to weekly digest for quick lane-dominance readability
- [x] Systems/QA Team: Add pressure-latency token (`PRESSURE LAG:FAST|STABLE|SLOW`) comparing pressure churn against drift momentum
- [x] Systems/World Team: Prototype adaptive route sandbox mode (`ROUTE SANDBOX:ON`) behind flag when digest enters sustained lane lock

## P1 (Game Director Injection — 2026-03-21 Cycle Q)
- [x] Systems/World Team: Add route-sandbox action-plan token (`SANDBOX PLAN:SIMULATE|PROBE|PREPARE|HOLD`) from `ROUTE SANDBOX + ACTION GUARD + DRIFT RISK`
- [x] QA/Systems Team: Add route-sandbox cooloff token (`SANDBOX COOLOFF:<n>`) counting consecutive non-armed windows after an ON cycle
- [x] Design/QA Team: Add sandbox lane-target token (`SANDBOX TARGET:<lane>`) to pin which lane-lock family should be tested when sandbox is active

## P1 (Game Director Injection — 2026-03-27 Cycle FF)
- [x] UX/Design Team: Add `DCCFXCPAP COACH LEGEND` row + coach-family churn visibility in weekly portal prompt readability drift digest (with regression ordering checks)

## P1 (Game Director Injection — 2026-03-21 Cycle R)
- [x] Design/QA Team: Add sandbox-target confidence token (`SANDBOX TARGET CONF:LOW|MID|HIGH`) for lane-target handoff quality
- [x] Systems/QA Team: Add sandbox-target source token (`TARGET SRC:LOCK|MIXED|NONE`) for derivation-path auditability
- [x] UX/Systems Team: Add sandbox-target history token (`TARGET SHIFT:<FROM->TO>`) to flag lane-target swaps across digest windows

## P1 (Game Director Injection — 2026-03-21 Cycle S)
- [x] Design/Systems Team: Add sandbox readiness tier token (`SANDBOX READY:IDLE|PRIMED|ARMED`) from `ROUTE SANDBOX + TARGET CONF + ACTION GUARD` for faster go/no-go triage
- [x] QA/Systems Team: Add route-action stability token (`ACTION STABILITY:LOCKED|WATCH`) from `ACTION CONF + FOCUS VOL + DRIFT MOMENTUM` to reduce retune whiplash
- [x] UX/Design Team: Prototype digest what-if lane hint (`WHAT-IF ALT:<lane> ΔRISK:<n>`) behind flag for low-cost alternate-route planning

## P1 (Game Director Injection — 2026-03-21 Cycle T)
- [x] UX/Design Team: Add what-if confidence token (`WHAT-IF CONF:LOW|MID|HIGH`) so flagged alternate-lane projection trust is glanceable
- [x] QA/Systems Team: Add what-if alignment token (`WHAT-IF ALIGN:ALIGNED|DIVERGED`) comparing `ALT LANE` against current `ROUTE ACTION`
- [x] Design/Systems Team: Add what-if impact-band token (`WHAT-IF BAND:GAIN|NEUTRAL|LOSS`) from projected risk delta

## P1 (Game Director Injection — 2026-03-21 Cycle U)
- [x] UX/Design Team: Add what-if delta-magnitude token (`WHAT-IF MAG:SMALL|MED|LARGE`) from `|ΔRISK|` for glanceable impact sizing
- [x] Systems/QA Team: Add what-if pressure-fit token (`WHAT-IF FIT:SAFE|EVEN|TENSE`) combining projected risk with pressure-band context
- [x] Design/Systems Team: Prototype what-if lane fallback token (`WHAT-IF FALLBACK:<lane>`) behind flag when alternate lane diverges from route action

## P1 (Game Director Injection — 2026-03-21 Cycle V)
- [x] UX/Systems Team: Add what-if fallback confidence token (`WHAT-IF FALLBACK CONF:LOW|MID|HIGH`) from divergence strength + route confidence
- [x] Systems/QA Team: Add what-if fallback pressure-safety token (`WHAT-IF FALLBACK FIT:SAFE|EVEN|TENSE`) comparing fallback projection vs pressure band
- [x] Design/AI Content Team: Prototype what-if fallback rationale token (`WHAT-IF FALLBACK WHY:<short>`) behind flag for quick operator context

## P1 (Game Director Injection — 2026-03-21 Cycle W)
- [x] UX/Systems Team: Add fallback-lane alignment token (`WHAT-IF FALLBACK ALIGN:SYNC|ASYNC`) comparing fallback lane vs digest lane-focus for routing coherence
- [x] Systems/QA Team: Add fallback-delta magnitude band token (`WHAT-IF FALLBACK MAG:SMALL|MED|LARGE`) for rollback impact sizing
- [x] Design/AI Content Team: Prototype secondary fallback candidate token (`WHAT-IF FALLBACK ALT2:<lane>`) behind flag for dual-path planning

## P1 (Game Director Injection — 2026-03-21 Cycle X)
- [x] Systems/QA Team: Add secondary fallback quality gate so `ALT2` only emits when lane-focus score is strong and non-ambiguous
- [x] UX/Design Team: Add secondary fallback confidence token (`WHAT-IF FALLBACK ALT2 CONF:LOW|MID|HIGH`) for dual-path trust readability
- [x] Design/AI Content Team: Prototype dual-path merge hint token (`WHAT-IF FALLBACK PLAN:PRIMARY|SECONDARY|HOLD`) behind flag

## P1 (Game Director Injection — 2026-03-21 Cycle Y)
- [x] UX/Design Team: Add merge-plan rationale token (`WHAT-IF PLAN WHY:<short>`) for concise operator context
- [x] Systems/QA Team: Add merge-plan pressure-fit token (`WHAT-IF PLAN FIT:SAFE|EVEN|TENSE`) from selected merge-path projection
- [x] Design/AI Content Team: Prototype dual-route split recommendation token (`WHAT-IF SPLIT:ON`) behind flag when primary/secondary diverge strongly

## P1 (Game Director Injection — 2026-03-21 Cycle Z)
- [x] QA/Design Team: Add split-recommendation confidence token (`WHAT-IF SPLIT CONF:LOW|MID|HIGH`) behind flag for operator trust readability
- [x] UX/Systems Team: Add split route-pair token (`WHAT-IF SPLIT LANES:<primary>/<secondary>`) for compact handoff clarity
- [x] Systems/AI Content Team: Prototype split-safe-mode token (`WHAT-IF SPLIT SAFE:ON`) behind flag when split suggests non-escalating dual-path plans

## P1 (Game Director Injection — 2026-03-22 Cycle AA)
- [x] UX/Design Team: Add split posture token (`WHAT-IF SPLIT POSTURE:SAFE|WATCH|HOLD`) from split armed/safe/confidence trio for faster operator go/no-go read *(lifecycle: [~] -> [x])*
- [x] QA/Systems Team: Add split cooloff token (`WHAT-IF SPLIT COOLOFF:<n>`) counting consecutive OFF windows after split ON cycle
- [x] Systems/AI Content Team: Prototype split escalation sentinel (`WHAT-IF SPLIT ESCALATE:ON`) behind flag when split lanes remain divergent under `TENSE` fit

## P1 (Game Director Injection — 2026-03-22 Cycle AB)
- [x] Design/Systems Team: Add split escalation confidence token (`WHAT-IF SPLIT ESC CONF:LOW|MID|HIGH`) from split confidence + plan-fit pressure context
- [x] UX/Systems Team: Add split escalation route-pair readability token (`WHAT-IF SPLIT ESC LANES:<primary>/<secondary>`) for escalation handoff clarity
- [x] QA/Systems Team: Prototype split escalation cooldown pressure token (`WHAT-IF SPLIT ESC COOL:<n>`) behind flag when escalation recently disarmed

## P1 (Game Director Injection — 2026-03-22 Cycle AC)
- [x] UX/Systems Team: Add split escalation state token (`WHAT-IF SPLIT ESC STATE:ARMED|COOLING|IDLE`) for faster digest triage
- [x] Systems/QA Team: Add split escalation cooldown pressure-band token (`WHAT-IF SPLIT ESC PRESSURE:LOW|MID|HIGH`) behind flag for cooldown risk context
- [x] Design/AI Content Team: Prototype split escalation recovery route hint (`WHAT-IF SPLIT ESC RECOVER:<lane>`) behind flag for post-escalation planning

## P1 (Game Director Injection — 2026-03-22 Cycle AD)
- [x] Design/AI Content Team: Add split escalation recovery route hint (`WHAT-IF SPLIT ESC RECOVER:<lane>`) behind flag with lowest-pressure lane selection for post-escalation planning
- [x] UX/Systems Team: Add split escalation recovery confidence token (`WHAT-IF SPLIT ESC RECOVER CONF:LOW|MID|HIGH`) from lane divergence + state + pressure easing
- [x] Systems/AI Content Team: Prototype split escalation dual-lane recovery fallback token (`WHAT-IF SPLIT ESC RECOVER ALT:<lane>`) behind flag for contingency planning

## P1 (Game Director Injection — 2026-03-22 Cycle AE)
- [x] UX/Systems Team: Add split escalation recovery ALT confidence token (`WHAT-IF SPLIT ESC RECOVER ALT CONF:LOW|MID|HIGH`) for contingency-lane trust readability
- [x] Systems/Design Team: Add split escalation recovery route decision token (`WHAT-IF SPLIT ESC RECOVER PLAN:PRIMARY|ALT|HOLD`) from recover/recover-alt availability
- [x] Design/AI Content Team: Prototype split escalation recovery rationale token (`WHAT-IF SPLIT ESC RECOVER WHY:<short>`) behind flag for operator context

## P1 (Game Director Injection — 2026-03-22 Cycle AF)
- [x] UX/Systems Team: Add split escalation recovery tempo token (`WHAT-IF SPLIT ESC RECOVER TEMPO:FAST|STEADY|DEFER`) for operator pacing readability *(lifecycle: [~] -> [x])*
- [x] QA/Systems Team: Add split escalation recovery confidence-delta token (`WHAT-IF SPLIT ESC RECOVER ΔCONF:+n|-n`) comparing against prior digest window
- [x] Systems/AI Content Team: Prototype split escalation recovery veto sentinel (`WHAT-IF SPLIT ESC RECOVER VETO:ON`) behind flag when pressure remains HIGH under low confidence

## P1 (Game Director Injection — 2026-03-22 Cycle AG)
- [x] UX/Systems Team: Add split escalation recovery veto confidence token (`WHAT-IF SPLIT ESC RECOVER VETO CONF:LOW|MID|HIGH`) for operator trust readability
- [x] Design/AI Content Team: Add split escalation recovery veto rationale token (`WHAT-IF SPLIT ESC RECOVER VETO WHY:<short>`) behind flag for compact triage context
- [x] Systems/QA Team: Prototype split escalation recovery veto cooloff token (`WHAT-IF SPLIT ESC RECOVER VETO COOLOFF:<n>`) behind flag after veto disarm

## P1 (Game Director Injection — 2026-03-22 Cycle AH)
- [x] UX/Systems Team: Add split escalation recovery veto state token (`WHAT-IF SPLIT ESC RECOVER VETO STATE:ARMED|COOLING|IDLE`) for rapid cooldown triage
- [x] QA/Systems Team: Add split escalation recovery veto dwell token (`WHAT-IF SPLIT ESC RECOVER VETO DWELL:<n>`) to count consecutive ARMED windows
- [x] Design/AI Content Team: Prototype split escalation veto release cue token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE:<short>`) behind flag when state transitions `COOLING -> IDLE`

## P1 (Game Director Injection — 2026-03-22 Cycle AI)
- [x] UX/Systems Team: Add split escalation veto release confidence token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE CONF:LOW|MID|HIGH`) for release-cue trust readability *(lifecycle: [~] -> [x])*
- [x] Systems/Design Team: Add split escalation veto release route token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE:<lane>`) for post-cooldown handoff clarity
- [x] QA/AI Content Team: Prototype split escalation veto release timer token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE TICK:<n>`) behind flag for idle-window pacing

## P1 (Game Director Injection — 2026-03-22 Cycle AJ)
- [x] UX/Systems Team: Add split escalation veto release pacing phase token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE:IDLE|EARLY|MID|LATE`) for glanceable idle-window pacing
- [x] Systems/QA Team: Add split escalation veto release cadence token (`WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE:ACCEL|STEADY|DECAY`) from tick deltas over prior window
- [x] Design/AI Content Team: Prototype split escalation auto-rearm warning token (`WHAT-IF SPLIT ESC RECOVER VETO REARM:WATCH`) behind flag when release tick remains late under HIGH pressure

## P1 (Game Director Injection — 2026-03-22 Cycle AK)
- [x] UX/Systems Team: Add split escalation auto-rearm confidence token (`WHAT-IF SPLIT ESC RECOVER VETO REARM CONF:LOW|MID|HIGH`) for trust weighting of WATCH cues
- [x] Design/AI Content Team: Add split escalation auto-rearm rationale token (`WHAT-IF SPLIT ESC RECOVER VETO REARM WHY:<short>`) for concise operator context *(lifecycle: [~] -> [x])*
- [x] Systems/QA Team: Prototype split escalation auto-rearm cooloff token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF:<n>`) behind flag after WATCH disarms

## P1 (Game Director Injection — 2026-03-22 Cycle AL)
- [x] UX/Systems Team: Add split escalation auto-rearm cooloff state token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF STATE:ACTIVE|IDLE`) for rapid cooldown triage
- [x] Systems/QA Team: Add split escalation auto-rearm pressure-relief fit token (`WHAT-IF SPLIT ESC RECOVER VETO REARM FIT:RELIEF|EVEN|TENSE`) from cooloff + pressure context
- [x] Design/AI Content Team: Prototype split escalation auto-rearm nudge token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE:<short>`) behind flag for operator handoff

## P1 (Game Director Injection — 2026-03-22 Cycle AM)
- [x] UX/Systems Team: Add split escalation auto-rearm nudge confidence token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE CONF:LOW|MID|HIGH`) for handoff trust readability
- [x] Systems/QA Team: Add split escalation auto-rearm nudge window token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WINDOW:ARMED|COOLING|IDLE`) from rearm + cooloff-state context
- [x] Design/AI Content Team: Prototype split escalation auto-rearm nudge rationale token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WHY:<short>`) behind flag for compact operator coaching

## P1 (Game Director Injection — 2026-03-22 Cycle AN)
- [x] UX/Systems Team: Add split escalation nudge impact-band token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE IMPACT:DEFENSIVE|CAUTIOUS|NEUTRAL`) from nudge + window + fit context
- [x] QA/Systems Team: Add nudge drift token (`WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE DRIFT:STABLE|SHIFTING`) using current/prior nudge-rationale deltas
- [x] Design/AI Content Team: Prototype dual-lane coach snapshot (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH:<primary>|<backup>`) behind flag for contingency readability

## P1 (Game Director Injection — 2026-03-22 Cycle AO)
- [x] UX/Systems Team: Add dual-lane coach confidence token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH CONF:LOW|MID|HIGH`) for contingency snapshot trust weighting
- [x] Systems/Design Team: Add dual-lane coach posture token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH MODE:PRIMARY|BALANCED|BACKUP`) from coach lane selection mix
- [x] Design/AI Content Team: Prototype coach fallback reason token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH WHY:<short>`) behind flag for operator context

## P1 (Game Director Injection — 2026-03-22 Cycle AP)
- [x] UX/Systems Team: Add dual-lane coach handoff token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF:LOCKED|FLEX|NONE`) for at-a-glance routing readiness
- [x] Systems/QA Team: Add coach handoff pressure-fit token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF FIT:SAFE|EVEN|TENSE`) from handoff + pressure context
- [x] Design/AI Content Team: Prototype coach handoff rationale token (`WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF WHY:<short>`) behind flag for compact operator coaching

## P1 (Game Director Injection — 2026-03-22 Cycle AQ)
- [x] VFX/World/Systems Team: Add portal transition FX cue token (`FX:CALM|FLICKER|SURGE`, compact `FX:C|F|S`) from route pressure score so jump risk reads instantly
- [x] Combat/VFX Team: Add berserker pressure pulse token (`BERSERK FX:PULSE`) when `THREAT Δ:+` persists for 2+ turns
- [x] Design/World Team: Prototype route-tag ASCII vignette token (`ROUTE VIGNETTE:<glyph>`) behind flag for stronger path fantasy

## P1 (Game Director Injection — 2026-03-22 Cycle AR)
- [x] UX/Design Team: Add route-vibe coaching token in portal prompt (`ROUTE VIBE:CALM|EDGE|DOOM`, compact `VIBE:C|E|D`) for faster emotional read on jump choice
- [x] QA/Systems Team: Add route-vibe drift telemetry snapshot (count by vibe per weekly digest window) for readability tuning cadence
- [x] Design/AI Content Team: Prototype route-vibe conflict warning (`VIBE CONFLICT:ON`) behind flag when route tag and threat tier imply opposing pacing cues

## P1 (Game Director Injection — 2026-03-22 Cycle AS)
- [x] UX/Design Team: Add route-vibe conflict rationale token (`VIBE WHY:<vibe>vs<tier>`, compact `VCWHY:<vibe>/<tier>`) behind flag for faster portal-choice triage *(lifecycle: [~] -> [x])*
- [x] Systems/UX Team: Prototype conflict-aware coach override token (`COACH OVERRIDE:DE-ESCALATE`) behind flag when `VIBE CONFLICT:ON` and adaptive ALT exists *(lifecycle: [~] -> [x])*
- [x] Design/Systems Team: Prototype vibe-consistency reward hint (`VIBE SYNC:+1`) behind flag when route vibe aligns with threat tier for 3 consecutive transitions

## P1 (Game Director Injection — 2026-03-22 Cycle AT)
- [x] UX/Systems Team: Add vibe-sync streak progress token in portal prompt (`VIBE CHAIN:<n>/3`, compact `VSC:<n>/3`) behind flag for pre-reward readability
- [x] Systems/Combat Team: Prototype sync-threshold dodge charge handoff (`VIBE SYNC DODGE:+1`) behind flag when `VIBE SYNC:+1` triggers
- [x] Design/AI Content Team: Prototype route-vibe snapback warning (`VIBE SNAPBACK:ON`) behind flag on immediate post-sync misalignment

## P1 (Game Director Injection — 2026-03-22 Cycle AU)
- [x] UX/Systems Team: Add post-snapback recovery cue token (`VIBE RECOVER:READY`, compact `VR:OK`) behind flag on first re-aligned transition
- [x] Systems/Combat Team: Add route-vibe resilience streak token (`VIBE RESILIENCE:<n>`) behind flag for consecutive recoveries after snapback
- [x] Design/AI Content Team: Prototype route-vibe drift alarm token (`VIBE DRIFT:WIDE`) behind flag when conflict + snapback co-occur in short window

## P1 (Game Director Injection — 2026-03-22 Cycle AV)
- [x] Combat/VFX Team: Add berserker cooldown relief token (`BERSERK FX:FADE`) when pulse streak breaks after sustained rise (cadence guard slice)
- [x] Systems/Ops Team: Add weekly digest lane-coverage watchdog token (`LANE CADENCE:OK|GAP`) for trailing 24h combat-vfx/design-world/systems-ops coverage
- [x] World/Design Team: Prototype route-vibe drift alarm escalation glyph (`DRIFT GLYPH:<...>`) behind flag for stronger drift readability

## P1 (Game Director Injection — 2026-03-22 Cycle AW)
- [x] UX/Systems Team: Add digest action-pace token (`ACTION PACE:ACCEL|STEADY|BRAKE`) from `ACTION GUARD + ACTION STABILITY + PRESSURE LAG` for quicker route-operation cadence triage *(lifecycle: [~] -> [x])*
- [x] QA/Systems Team: Add digest pace-drift token (`PACE DRIFT:+n|-n`) by comparing current/prior `ACTION PACE` windows
- [x] Design/AI Content Team: Prototype flagged pace coach rationale token (`ACTION PACE WHY:<short>`) for compact operator context *(lifecycle: [ ] -> [~] -> [x])*

## P1 (Game Director Injection — 2026-03-23 Cycle AX)
- [x] UX/Systems Team: Add digest pace-window token (`ACTION PACE WINDOW:OPEN|HOLD|CLOSE`) from `ACTION PACE + PACE DRIFT + ACTION GUARD` for operator go/no-go timing
- [x] QA/Systems Team: Add digest pace-window confidence token (`ACTION PACE WINDOW CONF:LOW|MID|HIGH`) from window stability + drift continuity
- [x] Design/AI Content Team: Prototype flagged pace-window fallback token (`ACTION PACE ALT WINDOW:<short>`) when primary pace window is `CLOSE` but sandbox lane is `ON`

## P1 (Game Director Injection — 2026-03-23 Cycle AY)
- [x] Design/AI Content Team: Add flagged pace-window fallback confidence token (`ACTION PACE ALT WINDOW CONF:LOW|MID|HIGH`) from fallback readiness + sandbox target quality
- [x] Systems/UX Team: Add flagged fallback fit token (`ACTION PACE ALT WINDOW FIT:SAFE|EVEN|TENSE`) for pressure-aware alternate pacing guidance
- [x] QA/Design Team: Prototype fallback rationale micro-token (`ACTION PACE ALT WINDOW WHY:<short>`) for operator handoff clarity


## P1 (Game Director Injection — 2026-03-23 Cycle AZ)
- [x] UX/Systems Team: Prototype fallback urgency token (`ACTION PACE ALT WINDOW URGENCY:NOW|SOON|LATER`) from fallback window + fit/confidence for quicker operator handoff
- [x] QA/Systems Team: Add fallback urgency drift token (`ACTION PACE ALT WINDOW URGENCY Δ:+n|-n`) comparing current/prior urgency band
- [x] Design/AI Content Team: Prototype compact fallback step token (`ACTION PACE ALT WINDOW STEP:<verb>`) for one-action operator nudges

## Next Up (Game Director Injection — 2026-03-23 Cycle BA)
- [x] Design/UX Team: Add compact fallback step glyph token (`ACTION PACE ALT WINDOW STEP GLYPH:<sigil>`) behind flag for DOS-width scanability
- [x] Systems/QA Team: Prototype fallback step drift token (`ACTION PACE ALT WINDOW STEP Δ:<n>`) against prior digest snapshot
- [x] Combat/VFX Team: Prototype fallback cadence pulse token (`ACTION PACE ALT WINDOW PULSE:COOL|LIVE|HOT`) for pressure readability

## Next Up (Game Director Injection — 2026-03-23 Cycle BB)
- [x] Combat/VFX Team: Ship fallback cadence pulse token (`ACTION PACE ALT WINDOW PULSE:COOL|LIVE|HOT`) with flag + digest schema + markdown wiring
- [x] Systems/QA Team: Add pulse drift token (`ACTION PACE ALT WINDOW PULSE Δ:+n|-n`) comparing current/prior pulse bands
- [x] Design/World Team: Prototype pulse-aware portal handoff cue (`ROUTE PULSE LINK:SOFT|SHARP`) behind flag for cross-surface readability

## Next Up (Game Director Injection — 2026-03-23 Cycle BC)
- [x] Design/World Team: Add pulse-aware portal handoff confidence token (`ROUTE PULSE LINK CONF:LOW|MID|HIGH`) for operator trust readability
- [x] UX/World Team: Prototype compact portal prompt pulse cue (`PULSE LINK:S|H`) behind flag for in-run route cadence readability
- [x] Systems/QA Team: Prototype pulse-link drift streak token (`ROUTE PULSE LINK STREAK:<n>`) in weekly digest for persistence triage

## Next Up (Game Director Injection — 2026-03-23 Cycle BD)
- [x] UX/Systems Team: Add route pulse-link mode token (`ROUTE PULSE LINK MODE:IDLE|SUSTAIN|SURGE`) from link + streak + pulse drift for faster cadence triage
- [x] Systems/QA Team: Add route pulse-link mode drift token (`ROUTE PULSE LINK MODE Δ:+n|-n`) versus prior digest window
- [x] Design/World Team: Prototype compact portal mode cue (`PULSE MODE:I|S|X`) behind flag for in-run route readability parity

## Next Up (Game Director Injection — 2026-03-23 Cycle BE)
- [x] UX/Systems Team: Add route pulse-link mode rationale micro-token (`ROUTE PULSE LINK MODE WHY:<short>`) behind flag for compact triage context
- [x] Systems/QA Team: Add route pulse-link mode stability streak token (`ROUTE PULSE LINK MODE STREAK:<n>`) across digest windows
- [x] Design/World Team: Prototype detailed portal pulse mode cue (`ROUTE PULSE MODE:IDLE|SUSTAIN|SURGE`) behind flag for full-prompt parity
## Next Up (Game Director Injection — 2026-03-23 Cycle BF)
- [x] UX/Systems Team: Add route pulse-link mode fit token (`ROUTE PULSE LINK MODE FIT:SYNC|WATCH|BREAK|RESET`) for handoff stability triage *(lifecycle: [~] -> [x])*
- [x] QA/Systems Team: Add route pulse-link mode fit drift token (`ROUTE PULSE LINK MODE FIT Δ:+n|-n`) against prior digest window
- [x] Design/World Team: Prototype compact portal pulse fit cue (`PULSE FIT:Y|W|B|R`) behind flag for in-run readability parity

## Next Up (Game Director Injection — 2026-03-23 Cycle BG)
- [x] Design/World Team: Prototype compact portal pulse-fit cue (`PULSE FIT:Y|W|B|R`) behind flag for in-run readability parity
- [x] Combat/VFX Team: Prototype compact pulse-flare warning token (`PULSE FLARE:+`) when `PULSE MODE:X` and fit downgrades (`B|R`) *(lifecycle: [~] -> [x])*
- [x] Systems/UX Team: Prototype compact prompt token-priority mode (`FIT-FIRST|MODE-FIRST`) behind flag under strict DOS width budget

## Next Up (Game Director Injection — 2026-03-23 Cycle BH)
- [x] UX/Systems Team: Prototype compact pulse-priority cue token (`PRI:F|M`) tied to token-priority mode so operators can instantly read active ordering
- [x] QA/Systems Team: Add weekly digest token for compact pulse-priority mode usage (`ROUTE PULSE TOKEN PRIORITY:FIT-FIRST|MODE-FIRST|OFF`) with drift guard
- [x] Design/World Team: Prototype portal fallback micro-cue (`ALT STEP:<SAFE|BAIT|PUSH>`) behind flag for faster branch intent scan

## Next Up (Game Director Injection — 2026-03-23 Cycle BI)
- [x] UX/World Team: Prototype fallback micro-cue confidence token (`ALT STEP CONF:LOW|MID|HIGH`) behind flag for branch-intent trust readability
- [x] Systems/QA Team: Add fallback micro-cue confidence drift token (`ALT STEP CONF Δ:+n|-n`) to weekly digest for stability triage
- [x] Design/AI Content Team: Prototype compact fallback intent rationale token (`ALT STEP WHY:<short>`) behind flag for operator context

## Next Up (Game Director Injection — 2026-03-23 Cycle BJ)
- [x] UX/AI Content Team: Prototype fallback rationale confidence token (`ALT STEP WHY CONF:LOW|MID|HIGH`) behind flag for trust readability
- [x] Systems/QA Team: Add fallback rationale confidence drift token (`ALT STEP WHY CONF Δ:+n|-n`) in weekly digest for stability triage
- [x] Design/World Team: Prototype compact rationale glyph token (`ALT WHY GLYPH:<sigil>`) behind flag for DOS-width scanability

## Next Up (Game Director Injection — 2026-03-23 Cycle BK)
- [x] UX/World Team: Prototype compact rationale glyph alias token (`AWG:<sigil>`) behind flag for stricter DOS-width prompt scanability
- [x] Systems/QA Team: Add compact rationale glyph drift token (`ALT WHY GLYPH Δ:+n|-n`) in weekly digest for stability triage
- [x] Design/AI Content Team: Prototype glyph rationale cadence token (`ALT WHY GLYPH MODE:STEADY|SPIKE`) behind flag for operator readability

### Game Director Cycle BL (2026-03-23)
- [x] QA/Systems Team: Add weekly digest drift token `ALT WHY GLYPH MODE Δ:+n|-n` with prior-window signals
- [x] Design/AI Content Team: Prototype compact prompt alias for glyph mode token (`AWGM:<S|K>`) behind flag
- [x] Systems/QA Team: Add digest confidence token for glyph-mode drift (`ALT WHY GLYPH MODE CONF:LOW|MID|HIGH`)

### Game Director Cycle BM (2026-03-23)
- [x] Systems/QA Team: Add glyph-mode confidence drift token (`ALT WHY GLYPH MODE CONF Δ:+n|-n`) to weekly digest for confidence stability triage
- [x] UX/World Team: Prototype compact confidence alias token (`AWGMC:<L|M|H>`) behind flag for prompt-width budget
- [x] Design/AI Content Team: Prototype glyph-mode confidence rationale micro-token (`ALT WHY GLYPH MODE CONF WHY:<short>`) behind flag

### Game Director Cycle BN (2026-03-23, forced-lane rebalance)
- [x] Combat/VFX Team: Add berserker cooldown intensity tier token to status feed (`BERSERK FX:FADE(SOFT|HARD)`) from threat-drop severity for clearer post-spike readability
- [x] Design/World Team: Prototype portal cooloff vibe trail token (`VIBE TRAIL:CALM|ASH`) behind flag after berserk fade events to reinforce recovery fantasy *(lifecycle: [~] -> [x])*
- [x] Systems/Ops Team: Add weekly cadence watchdog detail row (`LANE GAP DETAIL`) with combat/vfx last-touch age for forced-lane auditability

### Game Director Cycle BO (2026-03-23)
- [x] UX/World Team: Prototype portal vibe-trail confidence token (`VIBE TRAIL CONF:LOW|MID|HIGH`, compact `VTC:<L|M|H>`) behind flag for post-fade handoff trust readability *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token family coverage for vibe-trail confidence token churn (`VIBE TRAIL CONF`) for drift triage
- [x] Design/AI Content Team: Prototype compact vibe-trail rationale token (`VIBE TRAIL WHY:<short>`) behind flag for operator context
### Game Director Cycle BP (2026-03-23)
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

## P1 (Game Director Injection — 2026-03-23 Cycle BT)
- [x] Combat/VFX Team: Add compact pulse-heat FX cue token (`PULSE HEAT FX:CALM|SPARK|BLAZE`) behind `DOTPIO_EXPERIMENT_PULSE_HEAT_FX`
- [x] Design/World Team: Prototype compact route afterglow cue (`ROUTE GLOW:SOFT|SHARP`) tied to `VIBE TRAIL ARC`
- [x] Systems/QA Team: Add weekly digest token-family coverage for pulse-heat FX churn (`PULSE HEAT FX:`) with compact-budget drift note

## P1 (Game Director Injection — 2026-03-23 Cycle BU)
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

## P1 (Game Director Injection — 2026-03-24 Cycle BY)
- [x] UX/World Team: Add compact alias token for route-glow rationale rail (`RGFXWR:<STEADY|SPIKE>`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_COMPACT` while preserving detailed fallback
- [x] Systems/QA Team: Add weekly digest token-family coverage for route-glow rationale rail churn (`ROUTE GLOW FX CONF WHY RAIL:` + `RGFXWR:`) *(lifecycle: [ ] -> [~] -> [x])*
- [x] Design/UX Team: Prototype confidence-adaptive rail compression token (`RGFXWRM:LOCK|FLEX`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE` for pressure readability under compact budgets *(lifecycle: [ ] -> [x])* 

## P1 (Game Director Injection — 2026-03-24 Cycle BZ)
- [x] Systems/QA Team: Add weekly digest token-family coverage for rail-mode churn (`RGFXWRM:`) with compact-budget drift note
- [x] Combat/VFX Team: Prototype rail-mode intensity accent token (`RGFXWRI:SOFT|HARD`) keyed off `LOCK|FLEX` for stronger overdrive feel
- [x] AI Content/Design Team: Add rationale copy guard so rail-mode `LOCK|FLEX` wording remains deterministic with `RGFXW` mappings *(lifecycle: [ ] -> [~] -> [x])*

## P1 (Game Director Injection — 2026-03-24 Cycle CA)
- [x] Systems/QA Team: Add weekly digest token-family coverage for rail-intensity churn (`RGFXWRI:`) with markdown triage rows
- [x] UX/World Team: Prototype detailed parity cue for rail intensity (`ROUTE GLOW FX CONF WHY RAIL INTENSITY:SOFT|HARD`) behind flag while preserving compact `RGFXWRI` *(lifecycle: [ ] -> [~] -> [x])*
- [x] Design/AI Content Team: Prototype flagged rail-intensity rationale token (`RGFXWRI WHY:<short>`) for overdrive readability context *(lifecycle: [ ] -> [~] -> [x])*
- [x] Combat/Design Team: Prototype rail-intensity rationale confidence token (`RGFXWRI WHY CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF` for overdrive trust readability *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family coverage for rail-intensity rationale churn (`RGFXWRI WHY:`) with markdown triage row *(lifecycle: [ ] -> [~] -> [x])*
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


## Cycle CF follow-ups (injected)
- [x] Design/Combat Team: Prototype `RGFXWRIU COACH:<STEADY|SPIKE>` hint token behind dedicated flag when urgency parity is enabled.
- [x] UX Team: Validate compact prompt budget impact when urgency parity + urgency FX are enabled simultaneously; publish screenshot/playtest notes.

## Cycle CG - Game Director Review (2026-03-24 12:10 KST)
- Idea 1 (low risk, UX/Systems): Add compact urgency-parity alias token (`RGFXWRIUP:<LOW|MID|HIGH>`) to reduce prompt-width pressure when urgency parity + urgency FX are both enabled.
- Idea 2 (mid risk, Design/UX): Add budget-aware fallback copy for unknown-route coach string (`COACH:NO DATA` -> compact short form) when compact budget is constrained.
- Idea 3 (high risk, Systems/AI Content): Prototype dynamic token-pruning policy by remaining budget headroom to preserve top-priority urgency/fx cues under heavy prompt stacks.
- Selected experiment: Idea 1 (minimal vertical slice, additive + reversible).
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
- [x] Systems/QA Team: Add floating-number stack-cap telemetry token to weekly digest (`DMGNUM STACK CAP:`) with churn row + regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype damage-band glyph burst variants behind flag (`DMG GLYPH:BASIC|SPIKE|OVERDRIVE`).

## Cycle CN - Game Director Review (2026-03-24 19:12 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for combat burst token family (`DMG GLYPH:`) with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Add compact combat debug token (`DMG GLYPH LIVE:BASIC|SPIKE|OVERDRIVE`) behind flag.
- Idea 3 (high risk, AI Content/VFX): Drift-aware glyph-shape remap recommendation policy from digest trends.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family coverage for `DMG GLYPH:` churn and lock via regression.
- [x] UX/Combat Team: Prototype compact debug token `DMG GLYPH LIVE:BASIC|SPIKE|OVERDRIVE` behind flag.
- [x] AI Content/VFX Team: Prototype drift-aware glyph-shape remap recommendation policy (offline recommendation only). *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CO - Game Director Review (2026-03-24 20:40 KST)
- Coverage check (last 10 completions): systems/qa-heavy trend persisted; selected combat/vfx-facing player feedback slice for lane balance.
- Idea 1 (low risk, Combat/VFX): Add compact combat FX live token (`DMG GLYPH FX LIVE:CALM|SPARK|BLAZE`) behind flag mapped from latest glyph band.
- Idea 2 (mid risk, UX/Combat): Add compact damage-number lifecycle token (`DMGNUM LIFE:EARLY|MID|LATE`) for readability tuning.
- Idea 3 (high risk, AI Content/VFX): Add drift-aware runtime glyph FX remap policy from digest recommendations.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact combat FX live token (`DMG GLYPH FX LIVE:CALM|SPARK|BLAZE`) behind `DOTPIO_EXPERIMENT_DMG_GLYPH_FX_LIVE_DEBUG`.
- [x] Systems/QA Team: Add weekly digest token-family coverage for `DMG GLYPH FX LIVE:` churn + regression lock.
- [x] AI Content/VFX Team: Prototype offline-only glyph FX remap recommendation policy tied to drift risk. *(lifecycle: [~] -> [x])*

## P1 (Game Director Injection — 2026-03-24 Cycle CP)
- [x] Systems/QA Team: Add offline digest confidence token for glyph FX remap recommendation (`DMG GLYPH FX REMAP CONF:LOW|MID|HIGH`) with regression lock. *(lifecycle: [~] -> [x])*
- [x] UX/Combat Team: Prototype compact HUD debug token for glyph FX remap stance (`DMG FX PLAN:<mode>`) behind flag. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype offline digest-generated FX remap candidate table artifact for review workflows.

## P1 (Game Director Injection — 2026-03-24 Cycle CQ)
- [x] UX/Combat Team: Add compact HUD debug remap-plan token (`DMG FX PLAN:HOLD_FX|MICRO_TUNE_FX|SYNC_WITH_GLYPH`) behind `DOTPIO_EXPERIMENT_DMG_FX_PLAN_DEBUG`. *(lifecycle: [ ] -> [~] -> [x])*
- [x] World/Design Team: Prototype portal ambient-ramp hint token (`AMBIENT RAMP:CALM|TENSE`) behind flag for readability cadence.
- [x] Systems/Ops Team: Add offline glyph FX remap candidate table artifact generation (`logs/playtests/dmg_glyph_fx_remap_candidates.{md,json}`).

## Cycle CR - Game Director Review (2026-03-24 22:31 KST)
- Idea 1 (low risk, UX/World): Add compact ambient-ramp alias token (`AR:<C|T>`) behind flag for DOS-width readability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `AMBIENT RAMP:`.
- Idea 3 (high risk, AI Content/World): Drift-aware ambient ramp recommendation policy from weekly prompt pressure trends.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact ambient-ramp alias token (`AR:<C|T>`) behind `DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_COMPACT`.

## Cycle CS - Game Director Review (2026-03-24 23:04 KST)
- Idea 1 (low risk, UX/World): Add portal ambient-ramp confidence readability token (`AMBIENT RAMP CONF:HIGH|MID|LOW`, compact `ARC:<H|M|L>`) behind experiment flags.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `AMBIENT RAMP CONF:` + `ARC:`.
- Idea 3 (high risk, AI Content/World): Add drift-aware ambient confidence recommendation policy from prompt-pressure trends.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add portal ambient-ramp confidence readability token (`AMBIENT RAMP CONF:HIGH|MID|LOW`, compact `ARC:<H|M|L>`) behind `DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF` + `DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF_COMPACT`. *(lifecycle: [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `AMBIENT RAMP CONF:` + `ARC:` and lock with regression. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/World Team: Prototype drift-aware ambient confidence recommendation policy (offline recommendation only). *(lifecycle: [~] -> [x])*

## Cycle CT - Game Director Review (2026-03-25 00:31 KST)
- Idea 1 (low risk, Combat/VFX): Add compact floating-number lifecycle token (`DMGNUM LIFE:EARLY|MID|LATE`) behind debug flag for instant combat feedback-phase triage.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE:` with markdown triage row.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware damage-number fade-curve remap recommendation policy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact floating-number lifecycle token (`DMGNUM LIFE:EARLY|MID|LATE`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_DEBUG` with regression lock.

## Cycle CU - Game Director Review (2026-03-25 01:01 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE:` with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Add compact damage-number lifecycle confidence token (`DMGNUM LIFE CONF:LOW|MID|HIGH`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware damage-number fade-curve remap recommendation policy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE:` and lock via regression.

## Cycle CV - Game Director Review (2026-03-25 01:31 KST)
- Idea 1 (low risk, UX/Combat): Add compact damage-number lifecycle confidence token (`DMGNUM LIFE CONF:LOW|MID|HIGH`) behind debug flag.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF:` with markdown triage row.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware damage-number confidence remap recommendation policy.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Combat Team: Add compact damage-number lifecycle confidence token (`DMGNUM LIFE CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG` with deterministic phase mapping + regression lock. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CW - Game Director Review (2026-03-25 02:04 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF:` with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Add compact lifecycle confidence drift token (`DMGNUM LIFE CONF Δ:+n|-n`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline confidence remap recommendation policy from drift-risk + churn.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF:` and lock via regression. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CX - Game Director Review (2026-03-25 02:31 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:`) with markdown triage row.
- Idea 2 (mid risk, UX/Combat): Add compact lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:+n|-n`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline drift-aware confidence-delta smoothing policy for damage-number fades.
- Selected experiment: Idea 2 (minimal vertical slice).
- [x] UX/Combat Team: Add compact lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:+n|-n`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle CY - Game Director Review (2026-03-25 03:01 KST)
- Idea 1 (low risk, Systems/QA): Add weekly digest token-family churn coverage for lifecycle-confidence drift token (`DMGNUM LIFE CONF Δ:`) with markdown triage row + regression lock.
- Idea 2 (mid risk, UX/Combat): Prototype compact lifecycle-confidence trend band token (`DMGNUM LIFE TREND:UP|HOLD|DOWN`) behind debug flag.
- Idea 3 (high risk, AI Content/VFX): Prototype offline confidence-delta smoothing recommendation policy from digest drift signals.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE CONF Δ:` and lock via regression. *(lifecycle: [~] -> [x])*

## Cycle CZ - Game Director Review (2026-03-25 03:31 KST)
- Idea 1 (low risk, UX/Combat): Add compact lifecycle-confidence trend token (`DMGNUM LIFE TREND:UP|HOLD|DOWN`) behind debug flag.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND:` with markdown triage row + regression lock.
- Idea 3 (high risk, AI Content/VFX): Prototype offline lifecycle-trend smoothing recommendation policy from digest drift windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Combat Team: Add compact lifecycle-confidence trend token (`DMGNUM LIFE TREND:UP|HOLD|DOWN`) behind `DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_DEBUG` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMGNUM LIFE TREND:` and lock via regression. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype offline lifecycle-trend smoothing recommendation policy (offline recommendation only). *(lifecycle: [ ] -> [~] -> [x])*

## P1 (Game Director Injection — 2026-03-25 Cycle DA)
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
- Idea 1 (low risk, AI Content/Systems): Add offline lane-priority hysteresis suppression policy so recommendation flips only when score-gap clears threshold.
- Idea 2 (mid risk, UX/World): Add compact hysteresis confidence rail token (`LPR HYS RAIL:STEADY|SPIKE`) behind flag.
- Idea 3 (high risk, Systems/QA): Prototype adaptive hysteresis-threshold tuning policy from lane-age volatility windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] AI Content/Systems Team: Prototype offline lane-priority hysteresis suppression policy for recommendation flapping.
- [x] Systems/QA Team: Add compact hysteresis alias token (`LPR HYS:H|S`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_ALIAS` with payload + markdown wiring.
- [x] UX/World Team: Prototype compact hysteresis confidence rail token (`LPR HYS RAIL:STEADY|SPIKE`) behind flag. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Systems/QA Team: Prototype adaptive hysteresis-threshold tuning policy from lane-age volatility windows (offline recommendation only).

## Cycle DK - Game Director Review (2026-03-25 14:24 KST)
- Idea 1 (low risk, UX/Systems): Add compact hysteresis-threshold recommendation alias token (`LPR HYS THR:<L|H|R>`) behind flag for digest scanability.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `LPR HYS THR:` with markdown triage row + regression lock.
- Idea 3 (high risk, AI Content/Systems): Prototype offline adaptive hysteresis-threshold floor/ceiling learning policy from volatility outcomes.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact hysteresis-threshold recommendation alias token (`LPR HYS THR:<L|H|R>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_THRESHOLD_ALIAS` with payload + markdown + regression lock. *(lifecycle: [ ] -> [~] -> [x])* 
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `LPR HYS THR:` with markdown triage row + regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/Systems Team: Prototype offline adaptive hysteresis-threshold floor/ceiling learning policy from volatility outcomes.

## Cycle DL - Game Director Review (2026-03-25 15:34 KST)
- Coverage check (last 10 completions): systems/qa + offline observability remain dense; choose additive/reversible offline lane.
- Idea 1 (low risk, AI Content/Systems): adaptive hysteresis floor/ceiling learning from prior volatility outcomes.
- Idea 2 (mid risk, UX/Systems): compact adaptive-window drift token for digest triage.
- Idea 3 (high risk, AI Content/Systems): volatility-regime memory for step-size auto-tune.
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
- [x] Systems/QA Team: Add dedicated digest family churn triage note for suppression alias trend (`PRMS FAMILY TREND`) with prior-window drift context. *(lifecycle: [ ] -> [~] -> [x])*
- [x] AI Content/VFX Team: Prototype offline suppression-escalation recommendation policy (`PULSE REMAP SUPPRESS PLAN:HOLD|ARM|LOCK`) without runtime coupling. *(lifecycle: [ ] -> [~] -> [x])*

## Cycle DR - Game Director Review (2026-03-25 21:50 KST, lane-cap forced underrepresented pick)
- Coverage check (last 10 completions by lane): systems=5, qa=4, vfx=4, ai-content=3, combat=2, ux=2, world=0, design=0.
- Lane cap breach: systems (50%) > 40%; forced next experiment into underrepresented lanes.
- Selected experiment: Idea 2 (AI Content/VFX) — `PULSE REMAP SUPPRESS PLAN:HOLD|ARM|LOCK` + compact `PRSP:<H|A|L>`.
- [x] AI Content/VFX Team: Ship offline suppression-escalation recommendation token + compact alias behind `DOTPIO_EXPERIMENT_PULSE_REMAP_SUPPRESSION_PLAN_ALIAS` with regression lock. *(lifecycle: [ ] -> [~] -> [x])*
- [x] Design/World Team: Prototype ambient scene-reactive pulse-remap flavor mapping (`CALM|BRACE|LOCK`) for digest readability copy.
- [x] Systems/Ops Team: Add suppression-plan family churn trend row (`PRSP FAMILY TREND`) with prior-window drift context. *(completed: 2026-03-25 22:35 KST via weekly portal drift digest update)*
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

## Cycle DZ - Game Director Review (2026-03-26 03:45 KST, lane-cap forced underrepresented pick)
- Coverage check (last 10 completions by lane): systems=4, qa=4, world=5, ux=3, ai-content=3, combat=0, design=0, vfx=0.
- Lane cap breach: world (50%) > 40%; forced next experiment into underrepresented lanes.
- Selected experiment: Idea 1 (Combat/VFX) — `PULSE REMAP SCENE FX GLINT:SOFT|VOID|SPIKE` (offline digest-only).
- [x] Combat/VFX Team: Ship offline digest glint cue token (`PULSE REMAP SCENE FX GLINT:SOFT|VOID|SPIKE`) with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 03:45 KST)*
- [x] Systems/QA Team: Add prior-window trend drift row for glint token family with regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 04:05 KST)*
- [x] Design/World Team: Prototype glint-linked scene-copy palette recommendation (`COOL|ASH|SCAR`) as offline digest recommendation.
- [x] Combat/VFX Team: Prototype compact glint alias (`PRSFX:<S|V|P>`) behind flag for digest scanability.

## Cycle EA - Game Director Review (2026-03-26 06:15 KST)
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

## Cycle EF - Game Director Review (2026-03-26 08:31 KST)
- Coverage check (last 10 completions): systems/qa observability remained dominant; selected a low-risk combat-facing debug readability slice to maintain lane cadence balance.
- Idea 1 (low risk, Combat/UX): Add compact combo-confidence debug token (`DMG COMBO CONF:LOW|MID|HIGH`) behind flag for faster multi-kill trust read.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage for `DMG COMBO CONF:` with markdown triage row + regression lock.
- Idea 3 (high risk, AI Content/Combat): Prototype offline combo-confidence coach recommendation policy from kill heat volatility + pressure drift.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/UX Team: Add compact combo-confidence debug token (`DMG COMBO CONF:LOW|MID|HIGH`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_DEBUG` with regression coverage. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 08:33 KST)*
- [x] Systems/QA Team: Add weekly digest token-family churn coverage for `DMG COMBO CONF:` with markdown triage row + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 09:01 KST)*
- [x] AI Content/Combat Team: Prototype offline combo-confidence coach recommendation policy from kill heat volatility + pressure drift. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 09:39 KST)*

## Cycle EG - Game Director Review (2026-03-26 09:46 KST)
- Coverage check (last 10 completions): AI-content/combat + systems digest observability dominated; selected a low-risk readability slice for recommendation scan speed.
- Idea 1 (low risk, Combat/UX): Add compact alias token for combo-confidence coach recommendation (`DCCR:<G|S|U>`) behind flag.
- Idea 2 (mid risk, Systems/QA): Add weekly digest token-family churn coverage row for `DMG COMBO CONF COACH REC` + alias.
- Idea 3 (high risk, AI Content/Combat): Prototype offline confidence-coach fallback narrative line tied to recommendation streak drift.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/UX Team: Add compact combo-confidence coach alias (`DCCR:<G|S|U>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_COACH_ALIAS` with digest markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 09:46 KST; completed: 2026-03-26 09:50 KST)*
- [x] Systems/QA Team: Add token-family churn coverage row for `DMG COMBO CONF COACH REC` (+ alias) in weekly digest with regression lock.
- [x] AI Content/Combat Team: Prototype offline confidence-coach fallback narrative line tied to recommendation streak drift and volatility regime. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 10:34 KST)*


## P1 (Game Director Injection — 2026-03-26 Cycle EH)
- [x] Combat/VFX Team: Prototype compact scene-arc alias token (`DCCSA:<A|I|E>`) behind flag for digest density control. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 11:04 KST)*
- [x] Systems/Ops Team: Prototype 24h lane cadence miss-risk token (`LANE CADENCE MISS RISK:LOW|MID|HIGH`) from rolling completion spread. *(lifecycle: [~] -> [x]; completed: 2026-03-26 11:31 KST)*
- [x] QA/Design Team: Add contract check ensuring `DMG COMBO CONF COACH SCENE ARC` remains adjacent to combo-confidence coach rows for scan order stability. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 12:01 KST)*

## Cycle EI - Game Director Review (2026-03-26 12:31 KST)
- Idea 1 (low risk, UX/World): Add compact cadence alias token (`PRSMC:<R|H|C>`) behind flag for digest scanability.
- Idea 2 (mid risk, Systems/QA): Add cadence alias-family churn coverage row (`PRSMC + PULSE REMAP SCENE MICROLINE CADENCE`) with regression lock.
- Idea 3 (high risk, AI Content/Combat): Prototype offline cadence-reactive coach-copy swap policy from alias-family volatility.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/World Team: Add compact cadence alias token (`PRSMC:<R|H|C>`) behind `DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_CADENCE_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 12:39 KST)*
- [x] Systems/QA Team: Add dedicated cadence alias-family churn triage row (`PRSMC FAMILY CHURN`) near cadence trend output.
- [x] AI Content/Combat Team: Prototype offline cadence-reactive coach-copy swap recommendation policy from `PRSMC` churn + lane cadence miss risk.

## P1 (Game Director Injection — 2026-03-26 Cycle EJ)
- [x] AI Content/Combat Team: Add offline cadence-reactive coach-copy swap recommendation token (`DMG COMBO CONF COACH COPY SWAP REC:HOLD_COPY|ARM_SWAP|SWAP_NOW`) from `PRSMC` churn + lane cadence miss risk. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 13:31 KST)*
- [x] Systems/QA Team: Add dedicated swap-recommendation family churn row (`DMG COMBO CONF COACH COPY SWAP REC FAMILY CHURN`) with regression lock.
- [x] UX/Design Team: Constrain swap posture vocabulary to compact deterministic bands for digest scanability (`HOLD_COPY|ARM_SWAP|SWAP_NOW`).
- [x] Systems/QA Team: Add prior-window trend drift row for `DMG COMBO CONF COACH COPY SWAP REC` family with regression lock.
- [x] UX/Design Team: Prototype compact swap alias token (`DCCSR:<H|A|S>`) behind experiment flag for digest-width fallback. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 15:42 KST; completed: 2026-03-26 15:46 KST)*

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
- Idea 1 (low risk, Systems/Ops): Add compact lane cadence miss-risk alias (`LCMR:<L|M|H>`) behind flag for dense digest scanability.
- Idea 2 (mid risk, QA/Design): Add adjacency/order regression lock for `LCMR` placement next to miss-risk row.
- Idea 3 (high risk, AI Content/Systems): Prototype offline streak-aware lane-priority hysteresis floor recommendation from persistent `LCMR:H` windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/Ops Team: Add compact lane cadence miss-risk alias (`LCMR:<L|M|H>`) behind `DOTPIO_EXPERIMENT_LANE_CADENCE_MISS_RISK_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 19:10 KST)*
- [x] QA/Design Team: Add summary/token-coverage ordering contract for `LANE CADENCE MISS RISK` followed by `LCMR`. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 19:32 KST; completed: 2026-03-26 19:34 KST)*
- [x] AI Content/Systems Team: Prototype offline recommendation `LPR HYS FLOOR REC:HOLD|RAISE` from `LCMR` streak memory (digest-only, reversible).

## Cycle EP - Game Director Review (2026-03-26 20:01 KST)
- Coverage check (last 10 completions): systems/qa + ai-content observability remained dominant; selected a compact UX-facing digest readability slice to keep lane handoff scanable.
- Idea 1 (low risk, UX/Systems): Add compact alias token for hysteresis-floor recommendation (`LPR HYS FLOOR:<H|R>`) behind flag for digest density control.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage row for `LPR HYS FLOOR REC:` + alias with regression lock.
- Idea 3 (high risk, AI Content/Systems): Prototype offline adaptive floor-raise threshold policy from `LCMR` streak momentum + lane volatility regime.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact hysteresis-floor recommendation alias token (`LPR HYS FLOOR:<H|R>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_FLOOR_REC_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 20:01 KST)*
- [x] Systems/QA Team: Add token-family churn coverage row for `LPR HYS FLOOR REC:` + `LPR HYS FLOOR:` with regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 21:12 KST)*
- [x] AI Content/Systems Team: Prototype offline adaptive `LPR HYS FLOOR REC` threshold policy from `LCMR` streak momentum + lane volatility regime (digest-only). *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 21:16 KST)*

## Cycle EQ - Game Director Review (2026-03-26 21:24 KST)
- Coverage check (last 10 completions): systems/qa lane remained >40%; forced a player-facing digest readability slice with QA visibility to avoid lane overfitting.
- Idea 1 (low risk, Systems/QA): Add `LPR HYS FLOOR FAMILY TREND` (`UP|FLAT|DOWN`) row + payload drift signals so floor-family movement is auditable beyond churn totals.
- Idea 2 (mid risk, UX/Design): Add compact floor-family trend alias token (`LPR HF T:<U|F|D>`) behind flag for dense operator scans.
- Idea 3 (high risk, AI Content/Systems): Prototype adaptive lane-priority recommendation confidence guard when floor-trend and lane-volatility regime diverge for 2+ windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/QA Team: Add `LPR HYS FLOOR FAMILY TREND` markdown row + JSON drift signals (`currentNet`, `priorNet`, `Δnet`, `reason`) with regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 21:20 KST; completed: 2026-03-26 21:24 KST)*
- [x] UX/Design Team: Prototype compact floor-family trend alias token (`LPR HF T:<U|F|D>`) behind experiment flag + digest wiring. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 21:31 KST; completed: 2026-03-26 21:35 KST)*
- [x] AI Content/Systems Team: Prototype offline confidence guard policy for lane-priority recommendation when floor-trend/regime diverges across consecutive windows. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 22:38 KST)*

## Cycle ER - Game Director Review (2026-03-26 21:41 KST, lane-cap forced underrepresented pick)
- Coverage check (last 10 completions by lane): systems=6, world=0, ai-content=3, combat=2, design=2, vfx=0, ux=3, qa=3, ops=1.
- Lane cap breach: systems at 60% (>40%); forced next experiment into underrepresented lanes (combat/vfx or design/world), prioritizing vfx (0).
- 24h cadence guardrail status: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Combat/VFX): Add compact FX volatility alias token (`DCCFXV:<C|S|P>`) behind flag so operators can one-glance read CALM/SWING/SPIKE regime alongside DCCFX trend hysteresis.
  - Player fantasy target: post-fight coaching and VFX mood read as a single coherent pulse.
  - Expected impact metric: fewer ambiguous notes about when accent changes are noise vs intended pacing.
  - Scope: S | Risk: low | Rollback: disable/remove alias flag + payload row.
  - Pass/fail: pass if markdown/json expose deterministic alias and regression remains green.
- Idea 2 (mid risk, Design/World): Add scene-arc copy annotation row that mirrors volatility regime for writer-facing readability.
- Idea 3 (high risk, AI Content/Combat): Prototype adaptive confidence guard when DCCFX trend hysteresis contradicts volatility regime across consecutive windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact FX volatility alias token (`DCCFXV:<C|S|P>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_VOLATILITY_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 21:41 KST)*
- [x] Systems/QA Team: Add `DCCFXV FAMILY CHURN` row so volatility alias drift is isolated from DCCFXT/DCCFXH trend rails.
- [x] Design/World Team: Add readability contract note linking `DCCFXV` legend (`C/S/P`) to scene arc guidance in digest docs.

## Cycle ES - Game Director Review (2026-03-26 22:44 KST)
- Coverage check (last 10 completions): systems/qa observability still heavy; selected a compact UX-facing readability slice to keep operator scan speed high while preserving offline-only safety.
- Idea 1 (low risk, UX/Systems): Add compact lane-priority confidence-guard alias (`LPRCG:<H|A>`) behind flag for dense digest scans.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage row for `LPRCG:` + `LANE PRIORITY REC CONF GUARD:` with regression lock.
- Idea 3 (high risk, AI Content/Systems): Prototype adaptive guard-floor policy that raises divergence streak threshold under `SWING` volatility memory.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Systems Team: Add compact lane-priority confidence-guard alias (`LPRCG:<H|A>`) behind `DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; completed: 2026-03-26 22:44 KST)*
- [x] Systems/QA Team: Add token-family churn coverage row for `LPRCG:` + `LANE PRIORITY REC CONF GUARD:` with regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-26 23:31 KST; completed: 2026-03-26 23:33 KST)*
- [x] AI Content/Systems Team: Prototype adaptive divergence-streak threshold policy for confidence guard under `SWING` volatility memory (offline-only). *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 00:01 KST; completed: 2026-03-27 00:09 KST)*

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
- [x] Systems/QA Team: Add deterministic adjacency/order lock for `DCCFXV` -> `DCCFXC` -> `DCCFXCW` rows in summary + token coverage. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 05:31 KST; completed: 2026-03-27 05:38 KST)*
- [x] Design/World Team: Prototype scene copy palette hint token driven by `DCCFXCW` transitions. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 05:02 KST; completed: 2026-03-27 05:08 KST)*

## Cycle EZ - Game Director Review (2026-03-27 05:42 KST)
- Coverage check (last 10 completions): systems/qa heavy in recent window; keep this cycle in design/ux-facing readability lane.
- Idea 1 (low risk, Design/UX): Add `DCCFXCW SCENE PALETTE LEGEND` token (`COOL=RESET`, `ASH=BASELINE`, `SCAR=SPIKE`) in summary + token-coverage for faster digest decoding.
- Idea 2 (mid risk, Systems/QA): Add family-trend rail for `DCCFXCW SCENE PALETTE` transitions (`PALETTE TREND:COOLING|STABLE|HEATING`) with prior-window compare.
- Idea 3 (high risk, Combat/VFX): Prototype offline `DCCFXCW SCENE PULSE` cue derived from palette + volatility for postmortem scene pacing.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Design/UX Team: Add `DCCFXCW SCENE PALETTE LEGEND` row to summary + token-coverage and lock ordering in regression. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 05:42 KST; completed: 2026-03-27 05:47 KST)*
- [x] Systems/QA Team: Add `DCCFXCW SCENE PALETTE TREND` rail (`COOLING|STABLE|HEATING`) with prior-window delta snapshot in summary + token-coverage.
- [x] Combat/VFX Team: Prototype digest-only `DCCFXCW SCENE PULSE:<SOFT|HARD|SURGE>` cue derived from scene palette + volatility for postmortem pacing triage. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 06:37 KST; completed: 2026-03-27 06:45 KST)*

## Game Director Cycle FA — injected 2026-03-27 06:56 KST
- [x] UX/Combat Team: Add `DCCFXCW SCENE PULSE LEGEND` row in summary + token-coverage for one-glance decode. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 06:56 KST; completed: 2026-03-27 07:00 KST)*
- [x] Systems/QA Team: Extend regression ordering lock for `DCCFXCW SCENE PULSE -> LEGEND` adjacency in both sections. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 06:56 KST; completed: 2026-03-27 07:00 KST)*
- [x] Design/World Team: Prototype `DCCFXCW SCENE PULSE ARC:RECOVER|BRACE|ERUPT` narrative companion token (digest-only, flagged). *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 07:06 KST; completed: 2026-03-27 07:13 KST)*

## Cycle FB - Game Director Review (2026-03-27 07:31 KST)
- Coverage check (last 10 completions): systems/qa digest contract work remains dense; choose a low-risk UX/readability slice that improves decode speed without runtime coupling.
- Idea 1 (low risk, UX/Design): Add compact legend row for pulse-arc alias (`DCCFXCPA LEGEND: R=RECOVER, B=BRACE, E=ERUPT`) in summary + token-coverage.
- Idea 2 (mid risk, Systems/QA): Add token-family churn row for `DCCFXCPA:` with adjacency lock after arc legend.
- Idea 3 (high risk, AI Content/World): Prototype offline arc-to-copy recommendation token (`DCCFXCPA COPY:CLEAR|HOLD|SURGE`) from pulse-arc + volatility trend.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Design Team: Add `DCCFXCPA LEGEND` row in summary + token-coverage with deterministic adjacency regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 07:31 KST; completed: 2026-03-27 07:34 KST)*
- [x] Systems/QA Team: Add `DCCFXCPA FAMILY CHURN` row with prior-window drift context. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 08:05 KST; completed: 2026-03-27 08:12 KST)*
- [x] AI Content/World Team: Prototype offline arc-to-copy recommendation token (`DCCFXCPA COPY:CLEAR|HOLD|SURGE`). *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 08:06 KST; completed: 2026-03-27 08:12 KST)*

## Cycle FC - Game Director Review (2026-03-27 08:18 KST)
- Coverage check (last 10 completions): systems/qa and ux lanes dominate; inject an AI-content readability slice that still remains reversible.
- Idea 1 (low risk, UX/Design): Add `DCCFXCPA COPY LEGEND` row to summary + token-coverage for one-glance decode.
- Idea 2 (mid risk, Systems/QA): Add dedicated family-churn rail for `DCCFXCPA COPY:` (`DCCFXCPA COPY FAMILY CHURN`) with adjacency lock.
- Idea 3 (high risk, Combat/World): Add volatility-sensitive fallback narrative rail (`DCCFXCPA COPY ALT`) for surge suppression cases.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/AI Content Team: Add `DCCFXCPA COPY LEGEND` row in summary + token-coverage and extend regression adjacency lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 08:18 KST; completed: 2026-03-27 08:22 KST)*
- [x] Systems/QA Team: Add `DCCFXCPA COPY FAMILY CHURN` row with prior-window drift context and deterministic ordering guard. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 08:31 KST; completed: 2026-03-27 08:39 KST)*
- [x] Combat/World Team: Prototype `DCCFXCPA COPY ALT` fallback token for surge-suppression mismatch windows. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 09:05 KST; completed: 2026-03-27 09:14 KST)*

## Cycle FD - Game Director Review (2026-03-27 09:16 KST)
- Coverage check (last 10 completions): combat/systems rails are dense; use low-risk UX decode slice and inject two follow-up experiments.
- Idea 1 (low risk, UX/Design): Add `DCCFXCPA COPY ALT LEGEND` row to summary + token-coverage for one-glance mismatch decode.
- Idea 2 (mid risk, Systems/QA): Add `DCCFXCPA COPY ALT FAMILY TREND` rail with prior-window drift context.
- Idea 3 (high risk, AI Content/Combat): Prototype suppression-aware alternate microcopy pack token (`DCCFXCPA COPY ALT PACK`).
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] UX/Design Team: Add `DCCFXCPA COPY ALT LEGEND` row in summary + token-coverage with deterministic adjacency regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 09:16 KST; completed: 2026-03-27 09:20 KST)*
- [x] Systems/QA Team: Add `DCCFXCPA COPY ALT FAMILY TREND` rail with prior-window drift context. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 09:20 KST; completed: 2026-03-27 10:02 KST)*
- [x] AI Content/Combat Team: Prototype suppression-aware `DCCFXCPA COPY ALT PACK` token (digest-only, flagged). *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 10:58 KST; completed: 2026-03-27 11:01 KST)*


## Cycle FE - Game Director Review (2026-03-27 11:31 KST)
- Coverage check (last 10 completions): systems/qa + ai-content digest policy lanes remain dense; prioritize a lightweight combat/vfx readability slice for compact postmortem scan speed.
- Idea 1 (low risk, Combat/VFX): Surface compact copy-alt-pack alias token (`DCCFXCPAP:<H|B|R|A>`) behind flag to mirror `DCCFXCPA COPY ALT PACK` without widening digest rows.
- Idea 2 (mid risk, Systems/QA): Add token-family churn coverage + adjacency lock for `DCCFXCPAP:` next to COPY ALT PACK rows.
- Idea 3 (high risk, AI Content/Combat): Prototype offline pack-to-coach microline (`DCCFXCPAP COACH:<short>`) from suppression + mismatch windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Combat/VFX Team: Add compact copy-alt-pack alias token (`DCCFXCPAP:<H|B|R|A>`) behind `DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_COACH_CUE_WHY_SCENE_PULSE_ARC_COPY_ALT_PACK_COMPACT_ALIAS` with payload/markdown wiring + regression lock. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 11:31 KST; completed: 2026-03-27 11:41 KST)*
- [x] Systems/QA Team: Add token-family churn coverage + adjacency lock for `DCCFXCPAP:` around COPY ALT PACK rows.
- [x] AI Content/Combat Team: Prototype offline pack-to-coach microline token (`DCCFXCPAP COACH:<short>`) for mismatch-window handoff clarity. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 13:41 KST; completed: 2026-03-27 13:47 KST)*

## Cycle FG - Game Director Review (2026-03-27 15:41 KST)
- Coverage check (last 10 completions): systems=3, world=2, ai-content=4, combat=4, design=1, vfx=1, ux=2, qa=3.
- Lane-cap check: no lane exceeded 40% (ai-content/combat at 40% each), so no forced lane override required.
- 24h cadence check: combat/vfx ✅, design/world ✅, systems/ops ✅.
- Idea 1 (low risk, Combat/VFX): Add digest-only FX cue token `DCCFXCPAP FX CUE:<SOFT|SHARP|SURGE|STEADY>` mapped from `DCCFXCPAP COACH` for faster postmortem feel triage.
- Idea 2 (mid risk, Design/World): Add `DCCFXCPAP FX CUE LEGEND` + scene framing copy block to reduce decode latency for narrative reviewers.
- Idea 3 (high risk, Systems/Ops): Add lane-balance watchdog token that warns when combat/vfx cadence drops below 24h minimum.
- Selected experiment: Idea 1 (minimal vertical slice, player-facing combat/vfx readability).
- [x] Combat/VFX Team: Ship flagged `DCCFXCPAP FX CUE` token with payload + summary/token-coverage markdown wiring and regression ordering updates. *(lifecycle: [ ] -> [~] -> [x]; started: 2026-03-27 15:26 KST; completed: 2026-03-27 15:41 KST)*
- [x] Design/World Team: Add `DCCFXCPAP FX CUE LEGEND` row and adjacency lock after `DCCFXCPAP FX CUE` for one-glance narrative decode.
- [x] Systems/Ops Team: Add cadence watchdog note/token for combat/vfx recency breach (>24h) in weekly digest metadata.

## Cycle FH - Game Director Review (2026-03-27 15:58 KST)
- Coverage check (last 10 completions): systems/qa + combat/vfx digest-contract work remained dense; selected a low-risk systems/ops observability slice that improves cadence triage without runtime coupling.
- Idea 1 (low risk, Systems/Ops): Add `COMBAT/VFX CADENCE WATCHDOG STREAK:<n>` token (summary + token-coverage + payload) to track consecutive breach windows.
- Idea 2 (mid risk, Design/World): Add compact alert legend row for watchdog semantics (`OK=recent touch`, `BREACH=stale >24h`) with adjacency lock.
- Idea 3 (high risk, AI Content/Combat): Prototype offline cadence escalation coach token when watchdog streak reaches 2+ windows.
- Selected experiment: Idea 1 (minimal vertical slice).
- [x] Systems/Ops Team: Add `COMBAT/VFX CADENCE WATCHDOG STREAK:<n>` token + payload signals/count with regression ordering lock (`MISS RISK -> LCMR -> WATCHDOG -> STREAK`).
- [ ] Design/World Team: Add `COMBAT/VFX CADENCE WATCHDOG LEGEND` row with deterministic adjacency after watchdog streak rows.
- [ ] AI Content/Combat Team: Prototype offline cadence escalation coach token (`COMBAT/VFX CADENCE COACH:NUDGE|ARM|ESCALATE`) from watchdog streak depth + miss-risk level.
