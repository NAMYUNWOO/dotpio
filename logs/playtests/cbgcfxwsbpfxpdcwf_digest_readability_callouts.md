# CBGCFXWSBPFXPDCWF DIGEST Readability Callouts

Timestamp: 2026-03-30 17:36 KST
Scope: Playtest-facing readability callouts for compact FX cue alias digest (`S|E|H`).

## Fixture snapshots

```text
- CBGCFXWSBPFXPDCWF DIGEST: **S** (map=S:SOFT,E:EDGE,H:HARD source=CBGCFXWSBPFXPDCW FX CUE:SOFT)
- CBGCFXWSBPFXPDCWF DIGEST: **E** (map=S:SOFT,E:EDGE,H:HARD source=CBGCFXWSBPFXPDCW FX CUE:EDGE)
- CBGCFXWSBPFXPDCWF DIGEST: **H** (map=S:SOFT,E:EDGE,H:HARD source=CBGCFXWSBPFXPDCW FX CUE:HARD)
```

## Row-budget check

- DOS row budget threshold: 140 chars

- S: len=96 -> PASS
- E: len=96 -> PASS
- H: len=96 -> PASS

Result: PASS (all digest aliases remain within row budget while preserving source-token readability).
