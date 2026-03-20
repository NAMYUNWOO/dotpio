# Design Team Log


### 2026-03-19 23:59 KST
- Task: Mission momentum bonus payout experiment (objective completion streak SRL micro-reward).
- Decision: Logged lane impact for streak-based reward model (1,1,2 SRL) with reward cap and no duplicate payout on already-complete objectives.
- Evidence: `src/run_missions.lua`, `main.lua`, `scripts/regression_mission_momentum.lua` (+ mission regressions).
- Follow-up: Monitor telemetry for early-run SRL inflation and tune reward curve if low-tier churn increases.

## 2026-03-20 00:26 KST — cross-lane sync note
- Context: World/System completed map_03~07 identity metadata + encounter rhythm profile wiring.
- Impact: No content schema break; existing flows remain stable with differentiated pacing.
- Follow-up: Validate player readability and portal landmark cues in upcoming portal reposition task.

## 2026-03-20 00:58 KST
- Cross-lane note: World portal reposition pass completed for map_03~07 with validator/regression green.
- Impact: traversal landmarks and fallback routes are clearer; no economy/combat/UI schema changes required in this patch.
- Follow-up: monitor playtest readability feedback and tune labels/cues if confusion persists.

## 2026-03-20 01:28:00 KST
- Task: P2 backlog item `Add weekly sustain audit JSON pretty mode`.
- Commit: HEAD (pending)
- Files:
  - `scripts/audit_weekly_sustain_cron.sh`
  - `scripts/regression_weekly_cron_audit.py`
  - `POST_RC_BACKLOG.md`
- Verification:
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_audit.py` ✅
- Decisions:
  - Added `--pretty` flag for `--format json` to emit indented, human-readable audit payload while keeping compact JSON default stable.
  - Added guardrail: `--pretty` rejects non-JSON formats to avoid ambiguous output modes.
- Follow-up:
  - Next P2 priority: `Add sustain health dashboard markdown report`.

## 2026-03-20 01:59:00 KST
- Task: P2 backlog item `Add sustain health dashboard markdown report`.
- Commit: HEAD (pending)
- Files:
  - scripts/sustain_health_dashboard.py
  - scripts/regression_sustain_health_dashboard.py
  - scripts/run_weekly_sustain.sh
  - logs/playtests/rc_checklist.md
  - POST_RC_BACKLOG.md
  - logs/sustain_health_dashboard.md
- Verification:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py` ✅
  - `python3 scripts/regression_sustain_health_dashboard.py` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Weekly sustain runner now emits a single markdown dashboard rollup (economy safety, telemetry freshness, scheduler audit signal).
  - Dashboard consumes cron audit JSON when available and degrades gracefully to warning when managed cron entry is absent.
- Follow-up:
  - Next P2 priority: `Add automatic stale-branch/report drift check`.

## 2026-03-20 02:26 KST — P2 stale-branch/report drift guardrail handoff
- Design lane reviewed markdown artifact readability.
- Decision: generate a concise markdown summary (`logs/stale_branch_report_drift.md`) with clear checkmarks/warnings for human weekly review.
- Follow-up: none.

## 2026-03-20 03:00 KST — P2 sustain dashboard JSON mode handoff
- Design lane reviewed operator readability split: markdown for humans, pretty JSON for tooling/debug readability.
- Decision: gate `--pretty` to JSON-only mode to avoid ambiguous CLI expectations.
- Follow-up: none.

## 2026-03-20 03:29 KST — P2 sustain dashboard trend classification handoff
- Design lane reviewed dashboard readability with new trend row.
- Decision: expose trend near overall tier for at-a-glance weekly triage.
- Follow-up: none.

## 2026-03-20 03:58 KST — cross-lane handoff
- Design lane approved compact readability pass for mission pacing metadata (`PACK`, `STREAK`) in both mission panel and run summary.
- Decision: maintain terse DOS-style labels to avoid panel clutter.
- Follow-up: revisit panel density only if additional mission metadata is added.

## 2026-03-20 04:29 KST
- Task: Mission pacing readability micro-pass via status copy.
- Commit: HEAD (this run)
- Files: `main.lua`
- Verification: `luac -p main.lua` ✅
- Decisions:
  - Reward status copy now appends `[VARIETY +1]` when lane-switch bonus is awarded, preserving DOS-style compact readability.

## 2026-03-20 04:59 KST
- Task: Design readability pass for mission metadata row.
- Verification: `luac -p src/hud.lua` ✅
- Decisions:
  - Added terse DOS-style `TAG` and `PACE` labels to communicate run rhythm while avoiding panel clutter.

## 2026-03-20 05:29 KST
- Cross-lane design note: introduced berserker as a readability-friendly high-threat archetype (predictable low-HP power spike).
- Decision: keep behavior trigger simple (`hp <= 2`) to maintain player learnability and avoid hidden randomness.
- Follow-up: evaluate optional visual cue for desperation state in a later polish pass.

## 2026-03-20 05:44 KST
- Task: Design readability check for berserker escalation cue.
- Verification: `luac -p src/hud.lua main.lua` ✅
- Decisions:
  - Used terse DOS-compatible wording and compact HUD slot (`Berserk`) to preserve panel density.
  - Alert only triggers on transition to avoid noisy message churn.

## 2026-03-20 06:02 KST
- Task: Design readability check for one-turn lunge tell messaging.
- Verification: `luac -p src/hud.lua main.lua` ✅
- Decisions:
  - Preserved terse DOS-style warning copy and compact HUD telemetry to avoid panel overload.

## 2026-03-20 06:30 KST — Combat readability rhythm adjustment
- Decision: preserve high-threat berserker identity while introducing a recover beat after desperation lunge.
- Rationale: telegraph-only pattern remained punishing in chain engagements; recovery beat improves tactical readability without removing spike moments.
- Follow-up: monitor if map choke points over-amplify recovery exploitation.

## 2026-03-20 06:58 KST — HUD berserker recovery counter readability slice
- Threat strip hierarchy now reads: Berserk -> Lunge Tell -> Recovering, preserving urgency order.
- Decision: use warm amber for recovery indicator to communicate reduced immediate threat vs lunge tell.

## 2026-03-20 07:26 KST — Mission panel readability pass
- Decision: append compact `NEXT:<lane> +1` token to mission metadata row to communicate achievable variety reward with minimal HUD footprint.
- Follow-up: monitor line width if future metadata fields expand.

## 2026-03-20 07:56 KST — HUD readability: add compact mission mastery token
- Decision: added concise `VAR:<n>` alongside `PACK/TAG/STREAK` to communicate earned lane-switch mastery without increasing panel height.
- Follow-up: monitor line-width pressure if future metadata expands.

## 2026-03-20 08:28 KST — HUD hierarchy tweak
- Decision: expanded top-left HUD panel height to preserve legibility while adding threat aggregate line.
- Follow-up: validate alignment against onboarding strip and mission panel in next screenshot pass.

## 2026-03-20 08:56 KST — HUD semantic readability note
- Approved compact text augmentation (`Threat score + tier`) over adding a new panel row to preserve DOS HUD density.

## 2026-03-20 09:28 KST — HUD danger hierarchy polish
- Decision: aligned threat tier semantics with intuitive color hierarchy (safe->warn->danger) for faster glance parsing.
- Constraint: kept DOS density unchanged (no extra row added).

## 2026-03-20 10:06 KST — Threat math affordance placement
- Approved in-strip formula placement under berserker counters instead of a separate panel to preserve DOS hierarchy and keep threat context local.

## 2026-03-20 10:35 KST — Compact hierarchy-preserving delta row
- Approved placing threat delta directly beneath existing threat line to preserve DOS HUD locality and avoid new panel sprawl.

## 2026-03-20 11:06 KST — Combat readability alignment for pressure-breaker
- Kept pressure-breaker communication diegetic and compact (HUD count + status pulse) to avoid crowding the DOS combat strip.
- Maintained existing threat decomposition rows; dodge counter sits in left status cluster for quick glance during movement/combat.

## 2026-03-20 11:26 KST — Risk/reward readability for hazard room prototype
- Kept prototype lightweight: hazard lives in contested center room to make risk legible through natural encounter density.
- Added compact HUD/state messaging (`OVERCLOCK READY/HOT/CD`) instead of new paneling to preserve DOS hierarchy.

## 2026-03-20 12:01 KST — Weekly changelog drift detector rollout
- Completed backlog item: `QA/Systems: Add weekly changelog drift detector (code changes without corresponding team-log/report entry)`.
- Added `scripts/weekly_changelog_drift_check.py` + `scripts/regression_weekly_changelog_drift.py` and wired them into `scripts/run_weekly_sustain.sh` / RC sustain checklist.
- Verification: `python3 -m py_compile scripts/weekly_changelog_drift_check.py scripts/regression_weekly_changelog_drift.py`; `python3 scripts/regression_weekly_changelog_drift.py`; `bash scripts/run_weekly_sustain.sh`.
- Follow-up: next backlog priority is `Ops: Add sustain dashboard regression risk score (0~100) with threshold alert section`.

## 2026-03-20 13:05 KST
- Task: P2 Ops backlog — sustain dashboard regression risk score (0~100) + threshold alert section.
- Commit: HEAD (this run)
- Files: `scripts/sustain_health_dashboard.py`, `scripts/regression_sustain_health_dashboard.py`, `POST_RC_BACKLOG.md`
- Verification:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py` ✅
  - `python3 scripts/regression_sustain_health_dashboard.py` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Dashboard now emits `regressionRisk` payload with score/level/alert and fixed thresholds (`warnAt=30`, `alertAt=60`).
  - Markdown dashboard now includes a dedicated **Regression Risk** section with threshold alert status.
- Follow-up:
  - Backlog item marked done; queue next Game Director/Ops candidate.


## 2026-03-20 13:28 KST — Overclock hazard HUD countdown readability pass
- Decision: Overclock status hint now includes live seconds for active pulse (`OVERCLOCK HOT <n>s`) and cooldown (`OVERCLOCK CD <n>s`) to reduce timing ambiguity.
- Evidence: `lua scripts/regression_overclock_hazard.lua`; `luac -p src/overclock_hazard.lua`.
- Follow-up: Consider mirroring countdown near build preview panel for players who open inventory during hazard pulses.

## 2026-03-20 14:00 KST — Sustain dashboard regression-risk driver breakdown
- Decision: Added `regressionRisk.topDrivers` (top 3 contributors) to dashboard payload and markdown so ops reviews can immediately see what is driving score changes.
- Evidence: `python3 scripts/regression_sustain_health_dashboard.py`; `python3 scripts/sustain_health_dashboard.py --format json --pretty`.
- Follow-up: If risk repeatedly trends WARN/ALERT, add automated recommendation mapping each driver to a concrete remediation runbook step.

## 2026-03-20 14:29 KST — Hazard readability hierarchy note
- Approved compact text hierarchy: state token first (`READY/HOT/CD`), then reward/timer, then risk tier.
- Keeps DOS-style single-line affordance without extra panel footprint.

## 2026-03-20 14:56 KST — overclock aggro-pressure legend follow-up
- Task: Add active-pulse HUD hint legend for overclock aggro pressure (`AGGRO DET:+n MOVE:+m%`).
- Decision: Keep mechanic unchanged; surface detect/move pressure explicitly in HOT hint for faster risk parsing.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`; `lua scripts/regression_overclock_hazard.lua`.
- Follow-up: Observe readability during next map_07 playtest and adjust wording only if hint width becomes noisy.

## 2026-03-20 16:29 KST — Hazard readability micro-polish
- Decision: Reused existing overclock hint line to retain DOS compactness and avoid panel-height growth.
- Follow-up: Consider unified hazard legend style if more hazard-room variants are introduced.

## 2026-03-20 16:55 KST — Risk/reward pacing pass
- Decision: Overclock room now pays a small pulse-capped kill bounty so players are incentivized to stay in HOT zone briefly instead of always dipping out after build.
- Intent: tighten "high risk center contest" fantasy with immediate SRL feedback.

## 2026-03-20 17:31 KST — Overclock next-pulse bounty budget readability
- Decision: READY/CD overclock HUD hints now include `NEXT BOUNTY:0/y` so players can pre-plan hot-zone reward windows before pulse activation.
- Scope: No combat/economy math changes; display-only hint extension around existing kill-bounty cap.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua` PASS.
- Follow-up: Add next Game Director experiment candidate (no unchecked backlog items remain).

## 2026-03-20 18:01 KST — Post-RC hazard readability wave 2: overclock risk-tier HUD color
- Task: Color-code overclock RISK tier token in HUD hint (LOW/MED/HIGH).
- Decision: Implemented tier-aware HUD color metadata from hazard module and threaded it through HUD auxiliary hint rendering with fallback color.
- Evidence: ; [PASS] overclock hazard regression validated.
- Follow-up: Queue next Post-RC gameplay/UX experiment candidate.

## 2026-03-20 18:31 KST — P1 hazard readability wave 3: overclock risk-factor breakdown token
- Task: Added compact HUD token "RISK SRC:Dx+DETy+MOVEz" across OVERCLOCK READY/HOT/CD hints.
- Decision: Expose risk component math (discount + detect + move) inline for fast tuning readability without changing hazard mechanics.
- Evidence: luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua; lua scripts/regression_overclock_hazard.lua (PASS).
- Follow-up: If HUD width pressure appears in smaller layouts, abbreviate token labels while keeping component values visible.
