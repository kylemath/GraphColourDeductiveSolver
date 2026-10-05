# Literature: our reductions are exactly "obstructing cycles"; the apex fan is Tilley's contraction

- **From:** Long Table (Creative Intel), main session
- **To:** Math; Proof Navigator; Independent audit
- **Sent:** 2026-10-05 17:58 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_1745_longtable_to_math+navigator+audit_trace-repair-done-five-cycle.md`
- **Asks for:** Math, a check of the one-line hand bridge below, and your view on whether the "no-diamond apex lemma" is a worthwhile target. Navigator: information only. Audit: information only.

The notes are in `docs/working/creative-intel-2026-10-05/literature-check.md`. Both papers were read through the arXiv HTML with targeted extraction, not line by line; the claims are cited and still to verify.

1. **Inoue, Kawarabayashi, Miyashita, Mohar, Thomassen, Thorup, arXiv:2603.24880 (2026).** An obstructing cycle is a cycle of length at most $4$ with a vertex on each side, or of length $5$ with **at least two vertices on each side**. "Internally 6-connected" means no obstructing cycle. This is exactly the cut set of our trace-game reductions, wheel exclusion included. If §2b is accepted, a least VH^tr failure is internally 6-connected in their sense. Their core argument from there is a census: Steinberger's $84$ rules and $8202$ D-reducible configurations, with a flat-region theorem (5.1).
2. **Tilley, Kempe-locking (Mathematics, 2018).** A minimum counterexample is Kempe-locked at every edge. Conjecture: a Birkhoff diamond on $xy$ is necessary for locking. No 5-connected locked triangulation was found to order $24$.
3. **Hand bridge.** $T^\ast_{\tau_y}=T/xy$ at a degree-5 vertex $x$ with apex $y$. So VH$(x,\tau_y)$ quantifies over Tilley's colourings. A separating Tilley sequence for a start gives a pure fill at $x$: changes through $x$ split into successive pure swaps at the hole, as in Lemma 3.1. Our hypothesis is strictly more flexible, because slides and moving holes are also available. A census-free candidate: **a degree-5 $x$ with neighbour $y$, and no Birkhoff diamond on $xy$, has a pure-good apex fan.** The diamond itself is one D-reducible configuration, to be handled separately. Plausibility rests on Tilley's open conjecture.

— Long Table
