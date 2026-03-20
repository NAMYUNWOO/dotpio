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
