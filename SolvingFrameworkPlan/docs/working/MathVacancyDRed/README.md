# Vacancy D-reducibility: definition, checker, verifier, first runs

Math worker, 6 October 2026. Label: **[computed, exploratory]**, plus [hand] for the soundness argument in section 2. Implements the statement in `messages/2026-10-06/2026-10-06_1235_math_to_longtable+coordination+audit+navigator_right-statement-vacancy-D-reducibility.md`. Python 3.9, one process, total CPU under 1 minute. Nothing committed and no other file edited.

Files: `graphs.py` (T4, A_r, pentakis, r-ball extraction), `vdred.py` (checker), `verify.py` (brute-force verifier), `run_log.txt`, `verify_log.txt`.

## 1. Definition (the model implemented)

**Configuration.** T is a triangulation of the sphere, v is a vertex of degree 5, and r ≥ 1. The disc K is the union of the faces of T whose vertices are all at distance ≤ r from v, with at least one vertex at distance < r. We require the boundary of K to be a simple cycle R, the ring: these are the vertices at distance r, in cyclic order. The inside graph H is K − v, with every edge of K not incident to v. Ring chords that lie outside K are not in H. The outside O is the closure of T minus K. It is a triangulated disc bounded by R.

**States.** A state is a proper 4-colouring c of H in which the link of v uses all four colours. States are taken up to renaming colours. Every proper colouring of H is admitted, including colourings that do not extend to O. This is conservative.

**Outside patterns.** Fix a split θ = {p,q}|{r,s} (there are three). A ring edge is θ-transitional if its two ends lie in different halves of θ. Every triangle of O has three distinct colours, so it has exactly two transitional edges. The dual curves through transitional edges therefore form disjoint arcs and loops in O. The arcs give a **non-crossing perfect matching M_θ of the transitional ring edges**. The faces of this chord diagram are the outside regions. All ring vertices in one region lie in one θ-half, and they belong to one two-coloured component of O. Ring vertices in different regions are not joined outside. This is the classical Birkhoff–Heesch bookkeeping, written as a matching rather than as a partition. Every non-crossing perfect matching is allowed: the adversary may use any of them.

**θ-components** of (c, M_θ) are the classes of the vertices of H under two relations: the edges of H whose ends lie in the same θ-half, and same-region membership. They are exactly the traces on H of the {p,q}- and {r,s}-components of T − v that meet H. The verifier checks this (check A).

**Game.** In the state (c, knowledge), the player picks a split θ. If M_θ is not known, the adversary reveals some M_θ. The player then swaps one θ-component (p↔q or r↔s on its vertices), at a cost of 1. A θ-swap leaves every θ-transition unchanged, so **M_θ is kept as knowledge**. The other two splits' matchings are forgotten: when the player next uses one of them, the adversary chooses it afresh. Several swaps of the same split in a row therefore behave like one classical D-reducibility step. The player wins when the link uses at most 3 colours.

**Subtle points: the conservative choices made.**
- Components that lie entirely outside are never swapped. Swaps that reach outside vertices may change the other splits' patterns arbitrarily; the adversary decides.
- The three matchings are not required to be jointly realisable.
- Ring colourings are not required to extend to the outside.
- Knowledge of M_θ is kept only while the player keeps swapping θ-components.

**K is vacancy-D-reducible** if the player wins from every state with no knowledge. Its **depth** is the max over states of the min-max number of swaps. The checker computes this by value iteration from +∞; round n gives exactly the states that are won within n swaps:
U(c) = min_θ max_M A(c,θ,M), A = 1 + min_C K(swap_C c, θ, M), K(c,θ,M) = min(U(c), A(c,θ,M)), and U = K = 0 when c is filled.

## 2. Soundness [hand, checked by computer]

Take a real triangulation containing K and a real state s. The real outside fixes the true M_θ for every θ. The real θ-components restrict to the abstract ones for that M_θ (check A). A θ-swap preserves the true M_θ. So the abstract winning strategy can be played literally in T − v, and real Kempe radius(s) ≤ abstract U(s|H) (check B). If K is vacancy-D-reducible, every state at v fills in every triangulation containing K as a disc.

**Verifier** (`verify.py`). It runs on 36 explicit triangulations: T4, A_3, A_4 and pentakis, plus 10, 10, 10 and 2 random completions made by edge flips strictly outside K. For each one it enumerates all colourings of T − v, computes the real Kempe radius by BFS over whole-component swaps of all six colour pairs, and applies checks A and B to every state and split. **Result: 0 violations of A or B in all 36 graphs.** The real radius histograms reproduce MathConjectureR: T4 has 68 states with radii {0:22, 1:25, 2:15, 3:4, 4:2}, A_3 has 100 states, and pentakis has 130 DL states of radius 2.

**Sanity check: Kempe's error.** The radius-1 ball (K = v plus its link, R = link) is **not** reducible for any of the four graphs: all 5 unfilled states lose, as the classical theory requires.

## 3. Results

| configuration | r | \|H\| | ring | colourings (unfilled) | game nodes | value | depth, histogram | CPU |
|---|---|---|---|---|---|---|---|---|
| T4, v = 4 (link degrees 5,5,6,6,5) | 2 | 12 | 7 | 182 (94) | 890 | **reducible** | **7**: {1:46, 2:23, 3:7, 4:8, 5:4, 6:4, 7:2} | 0.02 s |
| icosahedral (A_3 centre; A_4 identical) | 2 | 10 | 5 | 50 (30) | 150 | **reducible** | **3**: {1:15, 2:10, 3:5} | <0.01 s |
| pentakis (6^5) | 2 | 15 | 10 | 1320 (550) | 16,260 | **not reducible** | 180 states won in 1 swap, **370 lost** | 0.5 s |
| pentakis (6^5) | 3 | 25 | 10 | 18,420 (7,710) | 224,710 | **reducible** | **7**: {1:4830, …, 7:20} | 11 s |
| T4 (whole graph, ring 6,11,16,15) | 3 | 16 | 4 | 132 (84) | 344 | reducible | 4 (equal to the real radius) | 0.01 s |
| any of the four | 1 | 5 | 5 | 10 (5) | 25 | not reducible | all 5 lost | 0 |

Reading:
- **(a) T4 passes the first kill test at radius 2.** The game value is 7, which is larger than T4's real radius of 4: the uniform outside-blind strategy costs more swaps.
- **(b) The icosahedral 2-ball has depth exactly 3.** This is a machine version of Theorem H (radius ≤ 3), and it is tight: the A_3 real radius is 3.
- **(c) The (6^5) 2-ball fails.** This matches MathSixFiveHole: ball-closed breakers can leak. The pentakis 3-ball passes with depth 7. Caution: this 3-ball is pentakis-specific, because it is 26 of pentakis's 32 vertices. It is not the generic (6^5) configuration.

## 4. Caveats and open points

- Exploratory. Each configuration was checked on one explicit embedding. The family of configurations for an unavoidable set has not been enumerated.
- A 2-ball whose boundary is not a simple cycle (separating triangles) is rejected by `ball_config`, and the model does not cover it.
- Allowing all matchings independently is conservative but may be too strong for the adversary at ring 10. That is one possible reason the (6^5) 2-ball fails. Imposing joint realisability of (M_1, M_2, M_3) is a sound strengthening that has not been implemented.
- Depth counts single swaps. Classical D-reducibility "steps" correspond to maximal runs of swaps of the same split.
