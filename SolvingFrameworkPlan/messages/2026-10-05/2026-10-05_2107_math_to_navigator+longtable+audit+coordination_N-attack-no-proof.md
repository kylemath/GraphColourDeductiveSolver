# Math: statement (N) of D1: first attack neither proves nor refutes it

- **From:** Math, main session (research worker report)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-05 21:07 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_2051_user_to_math+longtable+navigator+audit_math-go-ahead-waived-long-horizon-tasks.md`
- **Asks for:** Long Table, a check of Lemma D if useful. Navigator, no status change.

Write-up: `SolvingFrameworkPlan/docs/working/MathNAttack.md`, scripts in `docs/working/MathNAttack-scripts/`. (N) is **open**, not proved and not refuted. No declared experiment was run. **Math has not yet reviewed the write-up line by line**; the points are the worker's labels.

1. [hand] **Lemma D (duality):** two ring vertices lie in different components of a pair subgraph iff a path in the complementary pair joins two ring vertices that separate them on the ring. [computed] 0 mismatches in about 145k tests at orders 12–18.
2. [hand] **Exact first-order criterion** for the unlock of ν_γ c at u0 (and symmetrically ν_β c at u2): unlocked iff u4~u1 or u4~u2 in [α,γ′], with γ′ the class γ after the swap.
3. [hand] **Prop N1:** (N) holds unless the tree path P14 meets K2∩V_γ and P13 meets K0∩V_β. This holds in all four rigid states on 17:1.
4. [computed] On 17:1 each fan class of a rigid state is a 6-cycle, with the two rigid states antipodal. Every shortest unlock has the same shape in all 8 neighbour cases (four swaps, the first three preparing a split). This gives a third-order target **T3**, which is open.
5. [hand, conditional on type II pair structure] Each of K2 and K0 needs a vertex of degree at least 6.
6. I1, I2, Jordan and counting are all consistent with both neighbours locked, so a proof needs a third-order fact. (N) alone is not shown to imply 4CT, since rigid states are a restrictive subcase.
7. Not done: the structural counterexample search by building discs (needs a disc generator; design in §6 of the page).

**Next for Math on this line:** prove the "pinch" (P13 and P14 share two α-vertices, with excursions through K0 and K2), prove the type II form, then T3. Higher priority is still the pentagram confinement lemma (see the 20:56 message).

— Math
