# Math: trace-game hypothesis and four-connectivity: first attack finds no proof and no counterexample

- **From:** Math, main session (research worker report)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-05 20:56 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_2051_user_to_math+longtable+navigator+audit_math-go-ahead-waived-long-horizon-tasks.md`
- **Asks for:** Long Table, a view on the "pentagram confinement" question below. Navigator, no status change.

Write-up: `SolvingFrameworkPlan/docs/working/MathTraceFourConnAttack.md`. **Neither the trace-game hypothesis nor four-connectivity of a least plain failure is proved.** No census was run. **Math has not yet reviewed the write-up line by line**; the points below are the worker's, labelled as it labelled them.

1. [hand, worker] **Good-pair criterion.** In the four-connected core a degree-5 root has a good fan iff all its targetless states share a common repeat vertex. So a vertex is bad iff two targetless states have disjoint repeat pairs.
2. [hand, worker] A single swap in a stuck state rotates the repeat pair along pentagram edges that share a vertex. A local "pairs are confined" argument is a dead end; a non-local invariant (how lock paths wind around φ) would be needed.
3. [hand, worker] A relaxed relative target R+ lifts. It allows a landing on a separator vertex of global degree 6 with a 4|4 split. It helps only if stuck paths exit through such vertices, which depends on the far side.
4. [hand, worker] Four routes to four-connectivity fail at the same place: the good pair's path may land on the separating triangle F. Four-connectivity of a least plain failure is in effect equivalent to R or R+ on the innermost side.
5. [open] **Unlock lemma, "pentagram confinement":** in the four-connected core with protected triangle φ, some off-φ degree-5 vertex has all its targetless states sharing a repeat vertex. A proof would give VH_C, hence plain VH∃.
6. [worker; Math's quick check agrees] In the minimum-degree-5 class, a separating 5-cycle with 2 to 4 interior vertices cannot occur (e.g. two interior vertices have degree sum at most 9). So the "at least two interior vertices" hypothesis excludes only the 5-wheel.
7. [computed, no universal content] The icosahedron with a protected face: 180 canonical states, one move component, no targetless state.

**Plan.** Math will take item 5 next, as the single sharpest open lemma. Long Table: any exploratory data on whether targetless states at one degree-5 root always share a repeat vertex would help; it needs a declaration if it is a census.

— Math
