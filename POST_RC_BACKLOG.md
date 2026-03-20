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
- [ ] Systems/World Team: Add route-tag density ledger artifact per map chain (`SAFE|RISK|SPIKE` counts by reachable portal graph depth)
- [ ] QA/Design Team: Add portal prompt copy budget checker (warn when route preview line exceeds DOS compact width threshold)
