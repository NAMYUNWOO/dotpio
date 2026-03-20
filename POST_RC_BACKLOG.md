# POST_RC_BACKLOG

Last updated: 2026-03-20 14:00 KST

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
