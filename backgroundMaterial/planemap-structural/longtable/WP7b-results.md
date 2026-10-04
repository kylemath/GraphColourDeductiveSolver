# WP7b results: dynamic re-partition at traps

Long Table, 4 October 2026. This follows [WP7b-declaration.md](WP7b-declaration.md), committed before the run (`15e74b0`). The run is `wp7b_test.py`, which writes `wp7b-discovery.json`, on orders 12–18 only. There are 14 traps and 547 shallow states. These are facts, not status claims.

## Declared hypotheses

| Hypothesis | Result | Witnesses |
|---|---|---|
| **H-A:** at traps, every boundary rep-move has Δ_rep > 0 | **Refuted** | 20 moves, all at order 17, graph 3, roots 3 and 13 (the short-circuit traps). It holds at every order-17, graph-0 (long-chain) trap. |
| **H-B:** every shallow state has a decreasing macro whose first move has Δ_rep ≤ 0 | **Refuted** | 116 shallow states, where every decreasing macro starts by merging repeated-colour mass |
| **H-C:** at traps, no sing-move lowers singleton mass | Survives (0 violations) | Not distinctive: 496 of 547 shallow states share it, as do 3,438 states that descend in one swap (descriptive count, not declared) |

## What the dynamics show

- **The two trap types are dynamically different, not just statically.**
  - **Long-chain traps** (order 17, graph 0): every boundary repeated-colour swap *merges* repeated-colour mass (Δ_rep > 0), outweighing what the heavy singleton links lose. H-A describes them exactly.
  - **Short-circuit traps** (order 17, graph 3): some boundary repeated-colour swaps *split* repeated-colour mass (Δ_rep ≤ 0). Every move is still uphill, so those moves must push mass *into* the singleton pairs (Δ_sing ≥ −Δ_rep ≥ 0). In words, they turn boundary-routed singleton links into exterior chains.
- **The direction of mass flow on the first step does not distinguish escapes either.** 116 shallow states escape only through a first move that merges repeated-colour mass (H-B refuted).
- **Combined with WP7,** no static summary and no first-step sign pattern that we declared characterises traps across both types.

## Bearing on the warning bound

The math team asked for a structurally bounded object that each warning charges. What WP7 and WP7b establish so far:
- Every warned state is fully locked (Lemma 7.4).
- The traps come in at least two dynamic types.
- In the corpus, the warnings per run are at most 4, and the trap basins are the trap states themselves except at order 17, graph 3.

**What is still missing** is a bounded *object*: something like "a locked configuration of the root's 2-ball", whose number is bounded independently of n and which each warning uses up.

**Proposed next step (WP7c, to be declared before running).** Describe the basin of every warning placed in the frozen breadcrumb runs: the warned state, its locked boundary pattern, and the local structure around the root. Then ask whether warnings at one root ever exceed the number of distinct locked boundary-chain patterns. That pattern count is bounded by a constant for a 5-cycle boundary, so it is a candidate charging object. If warnings can exceed it, the charging fails and the witness is recorded.
