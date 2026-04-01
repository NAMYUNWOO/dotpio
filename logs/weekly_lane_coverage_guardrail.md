### Lane Coverage Guardrail
- status: **within-cap** (cap=40.0%)
- recent completed items: **10**
- over-cap lanes: **none**
- forced next lanes (if over-cap): **none**
- cadence buckets missing: **none**
- trend-score band snapshot (recent rows): **CALM=0, EDGE=0, HEATED=0**
- trend-score band snapshot alias: **TSSB:C0E0H0**
- trend-score alias decode: **TSSB legend (C=calm, E=edge, H=heated)**
- trend-score dispatch hint (offline): **BALANCED**
- trend-score dispatch hint alias: **TSDH:B**
- trend-score dispatch pressure (offline): **LIGHT**
- trend-score dispatch pressure alias: **TSDP:L**
- trend-score dispatch-pressure momentum (offline): **0**
- trend-score dispatch-pressure momentum band (offline): **LOW**
- trend-score dispatch-pressure momentum band alias: **TSDPM:L**
- trend-score dispatch-pressure momentum band progression (last-10 rolling): **TSDPM-SPARK:NA**
- trend-score momentum sparkline legend: **L=LOW, M=MID, H=HIGH (older->newer)**
- trend-score dispatch-pressure momentum slope (ai-content/systems): **COOLING**
- trend-score dispatch-pressure momentum slope alias: **TSDPMS:C**
- trend-score momentum-slope rec state alias: **TSDPMSR:H** (HOLD)
- trend-score momentum-slope rec decode: **TSDPMSR legend (H=HOLD, P=PREP, C=CLAMP)**
- trend-score momentum-slope rec family alias: **TSDPMSRF:S** (STABLE)
- trend-score momentum-slope rec family decode: **TSDPMSRF legend (S=STABLE, R=READY, T=TRIAGE)**
- trend-score momentum-slope rec family trend alias: **TSDPMSRFT:F** (FLAT)
- trend-score momentum-slope rec family trend decode: **TSDPMSRFT legend (U=UP, F=FLAT, D=DOWN)**
- trend-score dispatch-pressure momentum slope rec (ai-content/systems): **hold steady; validate calm-lane continuity**
- trend-score dispatch-pressure momentum fx cue (combat/vfx): **SOFT**
- trend-score dispatch-pressure momentum fx cue alias: **TSDPMFX:S**
- trend-score dispatch-pressure momentum fx cue cadence decode (design/world): **SOFT=CALM cadence, EDGE=EDGE cadence, HARD=HEATED cadence**
- trend-score dispatch-pressure momentum fx cue microcopy rec (ai-content/design): **steady pace; hold broad scan**
- trend-score momentum-slope rec family trend decode variant (design/world): **TSDPMSRFT legend (U=escalate, F=hold, D=cool)**
- trend-score momentum-slope rec family trend why alias: **TSDPMSRFTWHYA:H**
- trend-score momentum-slope rec family trend why alias decode: **TSDPMSRFTWHYA legend (E=escalate, H=hold, C=cool)**
- trend-score momentum-slope rec family trend why (ai-content/systems): **TSDPMSRFT WHY:hold lane pressure cadence**

| lane | count | percent |
|---|---:|---:|
| systems | 3 | 30.0% |
| world | 1 | 10.0% |
| ai-content | 1 | 10.0% |
| combat | 1 | 10.0% |
| design | 3 | 30.0% |
| ux | 1 | 10.0% |
| qa | 2 | 20.0% |
| vfx | 1 | 10.0% |

| cadence bucket | lanes | count | status |
|---|---|---:|---|
| combat-or-vfx | combat/vfx | 2 | met |
| design-or-world | design/world | 4 | met |
| systems-or-ops | systems/qa | 5 | met |
