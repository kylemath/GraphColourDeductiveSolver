# Termination and running time of the vacancy-induction algorithm

Math (research worker), 5 October 2026. A working note, no experiments, no status change. Sources: `START-HERE.md` §1, §6; `longtable/swarm/hole-induction.md`; `longtable/swarm/vh-exists.md` (Lemmas 1.1–1.3, Theorem A, Remarks 2.1–2.3); `longtable/wp19/beyond-short-fill.md`; `docs/reports/MathVHCoreAdvance.md` (as summarised in START-HERE §6). Labels: **[hand]**, **[conditional on VH∃]**, **[computed on saved data, post hoc]**, **[open]**. Counts below are hand derivations from the definitions, not measured.

## 0. The hypothesis as the induction uses it

Notation as in `vh-exists.md`: a state is (h, c) with c a proper 4-colouring of T − h; moves are Kempe swaps of a whole component of a two-colour subgraph of T − h, and singleton slides; F(T) is the set of states whose hole sees at most 3 colours.

**VH∃** [conditional]: for every spherical triangulation T of minimum degree 5 there are a degree-5 vertex v and a legal fan τ at v (both chosen from T alone, before any colouring) such that every colouring c of T^*_τ = (T − v) + τ, restricted to T − v, has (v, c) joined to F(T) in the move graph M(T).

By Remark 2.3 the "pair may depend on the colourings" variant is equivalent, so nothing is gained by weakening the quantifier order. Colourings of T^*_τ are exactly the set S(v, τ) (Lemma 1.2(d)).

## 1. The algorithm [hand, given VH∃]

Input: a spherical triangulation T on N vertices (with rotation system). Output: a proper 4-colouring.

**Phase 1 (top-down, no colours).** Set T_N = T. For m = N, N−1, …, 5 pick a vertex v_m of T_m of minimum degree d.
- d = 3: T_{m−1} = T_m − v_m.
- d = 4: T_{m−1} = T_m − v_m plus one absent diagonal of the link (one of the two is absent, Lemma 1.1).
- d = 5 (so min degree 5): let (v_m, τ_m) = W(T_m), the VH∃ witness; T_{m−1} = T^*_{τ_m}.
Stop at T_4 = K_4.

**Phase 2 (bottom-up).** Colour K_4 with four colours. For m = 5, …, N, given a colouring c_{m−1} of T_{m−1}, restrict it to T_m − v_m, then:
- d = 3: give v_m a colour missing from its three neighbours.
- d = 4: if the link uses ≤ 3 colours, fill; otherwise do the one Kempe swap of the Jordan argument (swap the component of b in H_13 if b, d are separated there; otherwise swap the component of a in H_02), then fill.
- d = 5: search M(T_m) from (v_m, c) for a state in F(T_m) (path P), apply P, fill the final hole with a missing colour. The result is a colouring of T_m, with the same vertex set, so c_m is defined.

The recursion is **linear, not branching**: one T^* per level, one recursive call per level. So the cost is a **sum** over levels, not a product. [hand]

## 2. (a) Termination

1. **Phase 1 terminates and Phase 2 is well-defined.** The order drops by exactly 1 per level (Lemma 1.2(d); the d = 3, 4 cases are in `hole-induction.md`), so there are at most N − 4 levels. Every T_m is a simple spherical triangulation with m ≥ 4 vertices. [hand]
2. **The d = 5 fill step terminates, given VH∃ and a correct witness.** Define the step as breadth-first search of M(T_m) from (v_m, c). M(T_m) is finite: |Ω| ≤ m · 4^{m−1}. BFS therefore always stops, and by VH∃ it stops at a state of F. If the witness were wrong (the pair is not a VH∃ pair) the BFS still stops, either at a fill, which is harmless, or with the whole component exhausted, which is a detectable "no fill". So termination of the algorithm is unconditional on the search; VH∃ is used only for success. [hand + conditional on VH∃]
3. **What fails without a search.** A rule-based walk (apply a fixed move rule until the hole sees ≤ 3 colours) terminates only if there is a measure that strictly decreases. That measure is exactly what is missing for general triangulations. The one family where a measure is in hand is the belt: the potential Φ of `belt-joined.md` §7 (Φ = |I| on a linear interval) and the compiled/accepted 2n-slide walk for unequal poles. [open for general T]
4. **No move cycle problem.** M(T) is undirected (Lemma 1.3(b)), so BFS from a start sees its whole component; reachability to F is a property of the component. There is no need for a termination argument beyond finiteness. [hand]

## 3. (b) Cost per level

Let L(T, c) be the length of the shortest path in M(T) from (v, c) to F(T), counting swaps and slides alike, and let κ(T, c) be the length of the shortest pure-swap path at the original hole. Pure paths are mixed paths, so L ≤ κ.

**Cost of one move** [hand]. A swap needs the components of one two-colour subgraph of a graph with ≤ 3m edges: O(m). A slide is O(d). The edge count is 3m − 6.

**Number of moves out of a state** [hand]. A swap is determined by a component; each vertex lies in three of the six two-colour subgraphs, so there are at most 3(m − 1) components, plus ≤ d slides. Branching b ≤ 3m + d = O(m). The tempting bound "only swaps meeting the link matter" is false for shortest paths: a swap far from the link can change later components. So the branching is O(m), not O(deg h). [hand]

**Iterated search to depth L** costs O(b^L · m) = O(m^{L+1}) time, with a constant of at most 4^L. With visited-state hashing the state count is at most min(b^L, m·4^{m−1}).

**What is accepted about L, case by case** (all single-start facts, none is uniform in T):
- Degree-5 hole: the hole fills in 1 swap, or reaches any chosen neighbour by ≤ 1 swap and 1 slide (mobility, Math 17:27, START-HERE §6). Local: gives L ≤ 2 only on the sub-branch.
- ℓ ≤ 2 ⇒ κ = ℓ (compiled: `short_fill`). So for starts with ℓ ≤ 2 the search can be restricted to pure swaps: cost O(m^3).
- ℓ = 3 < κ: the path starts with a slide and every two-swap finish uses the slid colour (compiled, L3). L4 (hand, accepted) adds that u keeps a ρ-neighbour in the {σ,ρ}-component of h after the slide. This narrows the search but is not a length bound.
- κ is not bounded by any function of ℓ in general graphs (E1–E4, accepted hand), so "ℓ small ⇒ short pure fill" is false beyond ℓ = 2. This does not bound ℓ itself.
- Degree-5 vertex next to a degree-≤ 4 vertex: every legal fan fills every start in ≤ 3 pure swaps (accepted). Degree-5 vertex of a separating triangle: ≤ 2 swaps at the fixed hole (accepted). Degree-6 separator hole with a 4+4 split: ≤ 3 swaps (accepted). These handle specified local configurations, so on those T the per-level cost is O(m^4) with the search above, or O(m) with the direct rule (a few components).
- Belt family G_n: unequal poles: ≤ 2n slides, explicit walk, compiled (`belt_unequal_at`). The walk is deterministic, so a level on that family costs O(n) moves × O(n) = O(n^2). Equal poles and pole holes: outside the compiled theorem. The fact that the proven bound is linear in n, with a deterministic rule, shows that a uniform constant bound on L is not the natural conjecture; a bound of the form O(n) or poly(n) with an explicit rule is. Whether 2n is attained as a shortest distance on belts is not known to me. [open]

**Sum over levels.** If L ≤ K(m) at level m and the search is generic BFS, total cost T_alg(N) ≤ Σ_{m ≤ N} [witness cost W(m) + O((4m)^{K(m)} · m)] [conditional on VH∃]. Degree-3 and degree-4 levels cost O(m) each (one component computation, one Jordan swap). Total is polynomial exactly when W(m) is polynomial and (4m)^{K(m)} is polynomial. [hand]

## 4. (c) Polynomial total time: what extra bound is needed

**Statement P(K).** There is a constant K such that, for every triangulation T of minimum degree 5, the VH∃ witness (v, τ) satisfies L(T, c) ≤ K for all c ∈ S(v, τ).

- [conditional on VH∃ + P(K)]: each fill step costs O(m^{K+1}) by iterative deepening, so the total is O(N · N^{K+1}) = O(N^{K+2}) with a witness oracle (sum over ≤ N levels), plus the witness cost. [hand]
- **Weaker form.** If only L ≤ f(m) is known, generic search costs m^{O(f(m))}. Polynomial needs f = O(1). For f = Θ(log m) this is quasipolynomial, m^{O(log m)}. For f = poly(m) the search can be exponential, and a polynomial algorithm needs, in addition to the length bound, a **search-free rule**: a locally computable move (or a polynomial-size family of candidates) that makes progress in a measure with polynomially many values. A length bound alone never gives a polynomial algorithm. [hand]
- **Cost of finding the fill given only existence.** Reachability in M(T) has up to m · 4^{m−1} states. I know of no polynomial algorithm for reachability to F without a structural rule. I claim no hardness result either. [open]

**What the data suggest** [computed on saved data, post hoc; not evidence of a bound]. Per `beyond-short-fill.md` §4 (saved WP19 outputs, orders 21–24): maximum κ = 5, "nofill" and "capped" never occur, κ − ℓ ≤ 2 on every observed start, and κ = 5 occurs with ℓ = 3 and ℓ = 4. Since ℓ ≤ κ, on those graphs P(5) held for the tested pairs. Cautions:
1. The numbers are maxima over finitely many graphs and starts at orders ≤ 24; the START-HERE page classes them as post hoc and says a finite pass is never generalised.
2. The belt shows linear-length fills exist as proved upper bounds, so the maximum over all T may grow with n even though it is flat at the orders tested. A flat maximum over orders 21–24 cannot distinguish constant from slowly growing.
3. The relevant maximum is over all starts for the chosen pair (the universal quantifier), not over the starts that happened to be sampled; I could not tell from the note whether the order-24 starts were exhaustive.
So the data make P(K) with K around 5 a reasonable **conjecture**, and nothing more. [open]

A route to P(K) from known local facts would be: show every min-degree-5 triangulation contains a vertex in one of the accepted local configurations (degree-5 next to degree-≤4 in T; separating-triangle degree-5; and so on) with a constant bound. That is the complement of the 4-connected core of order ≥ 12 (Math's results), so the open case is exactly the 4-connected core without a degree-≤4 neighbour of any degree-5 vertex. [open]

## 5. (d) The witness search

The algorithm needs the pair W(T) at each min-degree-5 level.

1. **Candidate set is polynomial** [hand]: at most one degree-5 vertex per deletion and 5 fans per vertex, so ≤ 5m candidate pairs; legality is a constant-time adjacency test per chord (Lemma 1.2).
2. **Verifying a candidate is not obviously polynomial.** VH(v, τ) is "for all c in S(v, τ), some move sequence reaches F": a universal statement over up to 4^{m−1} colourings of a graph with a reachability predicate in the matrix. That has the form ∀∃ over exponential domains. I know of no polynomial test and expect none without structure. [open]
3. **The algorithm does not need verification, only a good guess**, but guessing wrong has a price. If a pair p fails on its start c_p, the search for another pair needs a second colouring of T^*_{p'}, which is a second recursive call. With r tries per level the recurrence is R(m) ≤ r · R(m − 1) + (level cost), which is r^m, exponential, as soon as r ≥ 2 on a positive fraction of levels. So the **recursion is polynomial only if the witness is a polynomial-time computable function W(T)** (a rule), or the number of wrong guesses is O(1) in total. [hand]
4. **Partial retry without recursion** [hand]. Different starts for the same pair p can be obtained from c_p by Kempe swaps in T^*_p without a recursive call, since colourings of T^*_p are closed under swaps. This repairs a bad start but not a bad pair (VH(p) false means a start class is stuck), so it is a heuristic, not a bound.
5. **Where a rule could come from.** The accepted local theorems are in effect partial rules: if there is a degree-5 vertex adjacent to a degree-≤ 4 vertex (every legal fan good), or on a separating triangle (apex-a fan good), then W(T) is read off in O(m). So the unresolved portion is the 4-connected core with no such vertex. A proof of VH∃ that is constructive on the core (for instance a fan selected by a degree/diagonal criterion such as the "far diagonals cross" reduction in `wp18/analysis-17-1.md`) would give W in polynomial time. A non-constructive proof (counting, minimal counterexample) would give existence only, and then the best known algorithm is "try all ≤ 5m pairs per level", exponential as in item 3. [conditional on VH∃; open]

## 6. Summary

| Item | Status |
|---|---|
| Algorithm well-defined, depth ≤ N − 4, linear recursion | [hand], given a witness oracle |
| Terminates (BFS on a finite M(T), ≤ m·4^{m−1} states) | [hand]; success needs [conditional on VH∃] |
| Cost per level = witness + search to depth L; search O(m^{L+1}) | [hand] |
| Polynomial total if witness is a polynomial rule and L ≤ K constant: O(N^{K+2}) | [conditional on VH∃ + P(K) + rule] |
| Length bound alone does not give polynomial time; need constant L or a search-free rule | [hand] |
| P(K), K ≈ 5, from κ ≤ 5 at orders 21–24 | [post hoc]; [open] |
| Verifying a witness pair; computing W(T) in polynomial time | [open] |
