### Lane Coverage Guardrail
- status: **within-cap** (cap=40.0%)
- recent completed items: **10**
- over-cap lanes: **none**
- forced next lanes (if over-cap): **none**
- cadence buckets missing: **combat-or-vfx, design-or-world**
- trend-score band snapshot (recent rows): **CALM=0, EDGE=0, HEATED=0**
- trend-score band snapshot alias: **TSSB:C0E0H0**
- trend-score alias decode: **TSSB legend (C=calm, E=edge, H=heated)**
- trend-score dispatch hint (offline): **BALANCED**
- trend-score dispatch hint alias: **TSDH:B**
- trend-score dispatch pressure (offline): **HOT**
- trend-score dispatch pressure alias: **TSDP:H**
- trend-score dispatch pressure base class (pre-cadence override): **HOT**
- trend-score dispatch pressure cadence override: **TSDPCO:E** (ESCALATE, bucket=combat-or-vfx)
- trend-score dispatch pressure cadence override streak: **TSDPCOS:2**
- trend-score dispatch pressure cadence override note (ai-content/design, offline): **TSDPCO NOTE:PUSH**
- trend-score dispatch pressure cadence override note alias: **TSDPCON:P**
- trend-score dispatch pressure cadence override note decode: **TSDPCON legend (H=HOLD, W=WATCH, P=PUSH)**
- trend-score dispatch pressure cadence override decode: **TSDPCO legend (B=BASE, E=ESCALATE)**
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
- trend-score dispatch-pressure momentum fx combat callout (combat/vfx): **HOLD_LINE**
- trend-score dispatch-pressure momentum fx combat callout alias: **TSDPMFXC:HL**
- trend-score dispatch-pressure momentum fx combat callout decode (design/world): **HL=hold line, PE=press edge, BC=burst clear**

| lane | count | percent |
|---|---:|---:|
| systems | 1 | 10.0% |
| world | 0 | 0.0% |
| ai-content | 0 | 0.0% |
| combat | 0 | 0.0% |
| design | 0 | 0.0% |
| ux | 0 | 0.0% |
| qa | 0 | 0.0% |
| vfx | 0 | 0.0% |

| cadence bucket | lanes | count | status |
|---|---|---:|---|
| combat-or-vfx | combat/vfx | 0 | missing |
| design-or-world | design/world | 0 | missing |
| systems-or-ops | systems/qa | 1 | met |
