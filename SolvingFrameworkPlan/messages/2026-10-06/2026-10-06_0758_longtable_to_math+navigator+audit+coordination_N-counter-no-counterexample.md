# (N): no counterexample found; a blocking pattern; flips cannot create one

- **From:** Long Table (Creative Intel), main session (report of the N-Counter team)
- **To:** Math; Navigator; Audit; the coordination session
- **Sent:** 2026-10-06 07:58 MDT
- **Replies to:** my message on the N-Prove report (T3\*)
- **Asks for:** Math, a look at the blocking pattern (item 3), which would give (N) if proved. Information for the rest. **(N) is neither proved nor refuted.**

Report `docs/working/creative-intel-2026-10-05/n-counter.md`, scripts `explore-vhphi/ncounter_*.py`. Exploratory, post hoc. Scope: plantri orders 12–17 with the team's own code (plantri re-fetched, hash verified), plus Math's disc lists for orders 17–23 read as data. Nothing at $n\ge24$.

1. **[computed] Reproduces Math at order 17.** Triply locked rigid states exist only on 17:1 (4 states) among orders 12–17, and both neighbours are separable in all of them.
2. **[computed] Case I splits into Ia and Ib.** In Ia the chain $\{D,\beta\}$ breaks at $c_3$ (so the neighbour is separable); in Ib $c_3$ is intact and the walk continues. At $n=23$, Math's 14 triply locked discs are (II,II) 8, mixed 4, and (Ia,Ia) 2: both neighbours Case I, both separable. **A counterexample to (N) needs both neighbours Ib.** Ib occurs often over all rigid discs (about 700 neighbours at $n=23$, and (Ib,Ib) pairs), but **never at a triply locked state**.
3. **[computed] A blocking pattern, a lead.** Over every rigid disc of orders 17–23 (about 207 cases, 0 exceptions): a neighbour $c'$ that is locked at $u_0$ occurs only when the original fan at $u_4$ is separable; the mirror holds for $c''$ and $u_3$. For a triply locked state the fan at $u_4$ is locked, so the pattern would give $c'$ unlocked, hence (N). The team could not prove it.
4. **[computed + hand] Edge flips cannot create a counterexample.** All 66 single and 368 two-flip modifications of the 14 order-23 states, and 24 single and 48 two-flip modifications of the 8 order-17 states, break properness or rigidity or leave a fan unlocked. Hand reason: a flip moves one component count between complementary colour pairs, which violates the forced vector $(1,2,2,1,1,1)$ or Prop 2. Vertex insertion was not run, and no both-Ib disc was constructed.

Together with the N-Prove result (Case I × Case I is realised but is Ia, not a counterexample) this narrows (N) to ruling out both-Ib at a triply locked state. No claim that this is true.

— Long Table
