### Forced-Lane Task Template Draft
- status: **over-cap**
- missing cadence buckets: **none**
- forced next lanes: **world, combat, ai-content**

- [ ] World/Combat Team: Inject one underrepresented-lane gameplay experiment template for `combat` when guardrail status is `over-cap`.
  - Player fantasy: Keep lane rotation feeling alive with a visible gameplay-facing experiment in the neglected lane.
  - Impact metric: At least one underrepresented lane appears in next-cycle completed items while lane-cap warning resolves.
  - Scope/Risk: S / low
  - Rollback: Remove template row and disable over-cap gameplay injection pathway.
  - Pass/Fail: Pass when template includes deterministic lane + verification command and guardrail status remains machine-readable.
  - DoD: Template includes player-facing fantasy target, impact metric, risk/rollback, and minimal vertical-slice verification commands.
  - Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
- [ ] World/Design Team: Inject one underrepresented-lane experiment template for `world` with minimal vertical slice scope.
  - DoD: Template has explicit risk/rollback and lane-specific readability impact metric.
  - Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
- [ ] AI Content/Design Team: Inject one underrepresented-lane experiment template for `ai-content` with minimal vertical slice scope.
  - DoD: Template has explicit risk/rollback and lane-specific readability impact metric.
  - Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
