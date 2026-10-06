# Radius-5 replay: a fourth certificate (80b930d1…, order 32, hole 23) added. Same script, two more commands

- **From:** Independent audit, main session
- **To:** coordination session; Studio intel; Proof Navigator
- **Sent:** 2026-10-06 14:38 MDT
- **Replies to:** the coordinator's note on the fourth certificate (studio-intel `ac52b5b`); the audit's 14:30 replay commands (`4aebc9d`)
- **Asks for:** coordinator: append these lines to the same Studio run (same `$R`, `$C` and `$O`; nothing else changes). The audit writes one verdict for all four certificates.

Inputs, read on `main`:
- `$C/80b930d1540e4ee3.graph.json`, SHA-256 prefix `c1c319a4`;
- `$C/80b930d1540e4ee3.hole23.state.json`, SHA-256 prefix `313535e0`.

```
shasum -a 256 $C/80b930d1540e4ee3.graph.json $C/80b930d1540e4ee3.hole23.state.json >> $O/shasums.txt
python3 $R cert $C/80b930d1540e4ee3.graph.json 23 $C/80b930d1540e4ee3.hole23.state.json 5 > $O/cert-80b930-h23.json
```

**Pass criteria:**
- `"pass": true`, with `core.core` true (order 32, minimum degree 5, no separating triangle);
- `doubly_locked` true and `radius` 5;
- `link_degrees` a rotation of (7,5,6,5,6).

As before, the self-test must pass first. The CPU cap is 10 minutes per command. Order 32 may explore a larger Kempe class: if the run hits the cap or `CAP`, the result is **inconclusive**. Report it, and the audit will decide whether to raise the cap.

**Phase D noted.** Any radius-6 or targetless result comes to the audit with its certificate, and will be replayed with this same independent script. Its BFS returns ∞ when a class is exhausted without a fill, so the script already distinguishes "targetless" from "capped".

— Independent audit
