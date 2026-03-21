# Weekly Portal Prompt Readability Drift Digest

- GeneratedAt(UTC): 2026-03-21T07:33:12.348367Z
- Status: **OK**
- Window: last 7 days (max 120 commits)
- Checked commits: 120
- Portal prompt commits: 9
- Dominant mode commits: compact=2, detailed=5, neutral=2
- MODE TREND: **DETAILED**
- PRESSURE BAND: **HIGH** (edits +17 / -2 / net 15)
- DRIFT RISK: **HIGH** (score=19 | imbalance=4 | pressure=15)
- FOCUS: **PORTAL** (portal=35 | alt=23 | pressure=15)
- FOCUS STREAK: **0**
- FOCUS SHIFT: **ALT->PORTAL**
- FOCUS VOL: **SWING** (switches=5/8 ratio=0.625)
- ROUTE ACTION: **PORTAL_AUDIT** (portal-family tokens dominate top movers)
- ACTION CONF: **LOW** (dom=0.479 spread=12 driftSpread=11)
- FOCUS BAL: **48%** (top=35 total=73 dom=0.479)
- FOCUS ENTROPY: **HIGH** (norm=0.948 raw=1.503 max=1.585)
- ACTION GUARD: **LOCK** (high-drift-low-confidence; risk=HIGH conf=LOW)
- LANE LOCK: **NONE** (threshold=3 lane=PORTAL streak=0)
- ROUTE SANDBOX: **OFF** (flag-disabled-and-lane-lock-not-armed; flag=DOTPIO_EXPERIMENT_ROUTE_SANDBOX enabled=False laneLock=PORTALx0)
- SANDBOX PLAN: **PREPARE** (high-risk-waiting-on-sandbox-flag; guard=LOCK risk=HIGH)
- SANDBOX TARGET: **NONE** (sandbox-inactive; lane=PORTAL armed=False streak=0)
- TARGET SRC: **NONE** (sandbox=OFF target=NONE)
- SANDBOX TARGET CONF: **LOW** (no-single-lane-target; routeConf=LOW lock=Falsex0)
- SANDBOX READY: **PRIMED** (preconditions-forming; sandbox=OFF conf=LOW guard=LOCK lock=Falsex0)
- TARGET SHIFT: **NONE->NONE** (target-stable; changed=False priorLoaded=True)
- SANDBOX COOLOFF: **0** (no-prior-on-cycle; active=False prior=OFF:0)
- DRIFT MOMENTUM: **FLAT** (recent=4.6 older=3.5 delta=1.1)
- ACTION STABILITY: **WATCH** (retune-watch-needed; conf=LOW vol=SWING momentum=FLAT)
- PRESSURE LAG: **SLOW** (churn=15 momentum=FLAT |Δ|=1.1)
- STICKY TOKENS: **6**
- ANOMALY: **ON** (sticky=6/3 pressure=15/5)
- ANOMALY CONF: **HIGH** (triggers=2 gap=13)

## Token Totals (added/removed/net)
- Compact: +28 / -3 / net 25
- Detailed: +35 / -6 / net 29
- Shared: +32 / -13 / net 19

## Top Token Movers (net ±)
- `COACH:` net +12 (added 18, removed 6)
- `NEXT ROUTE:` net +10 (added 15, removed 5)
- `P:` net +8 (added 9, removed 1)
- `PRESSURE:` net +7 (added 8, removed 1)
- `ENTER:JUMP` net +7 (added 14, removed 7)

## Sticky Tokens
- `NEXT:`, `P:`, `NEXT ROUTE:`, `PRESSURE:`, `ENTER:JUMP`, `COACH:`

## Commit-level digest
- `0aa530c` feat: add flagged ALT PLAN portal nudge experiment | mode=compact | compact net=5 detailed net=3 shared net=0
- `a1fac91` test: add adaptive ALT compact prompt readability regression | mode=compact | compact net=8 detailed net=1 shared net=3
- `a6ca3a1` feat(portal): select lowest-pressure reachable ALT route | mode=detailed | compact net=0 detailed net=3 shared net=0
- `61be8ff` feat(portal): add adaptive alt-route pressure delta hint | mode=detailed | compact net=4 detailed net=7 shared net=0
- `cbd5289` qa: add portal transition prompt token-order linter + budget parser | mode=neutral | compact net=4 detailed net=4 shared net=6
- `721a173` feat(portal): add route-pressure transition token with threat context | mode=detailed | compact net=2 detailed net=5 shared net=0
- `a02ee9c` feat: add portal prompt copy-budget audit and compact fallback | mode=detailed | compact net=2 detailed net=3 shared net=6
- `534c6a6` feat: add route-tag distribution audit and portal route coaching cue | mode=neutral | compact net=0 detailed net=0 shared net=3
- `1b83237` feat: add portal transition route preview prompt | mode=detailed | compact net=0 detailed net=3 shared net=1
