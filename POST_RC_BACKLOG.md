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
