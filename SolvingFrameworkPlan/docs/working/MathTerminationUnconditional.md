# What is unconditional about the vacancy-induction algorithm

Math (research worker), 6 October 2026. Working note, no experiments, no status change. Companion to `MathTerminationPlan.md` (called Plan below). Sources: Plan; `START-HERE.md` §6; `longtable/swarm/vh-exists.md` (Lemmas 1.1–1.3, 3.1, 3.2, Remark 2.3). Labels: **[hand]** proved here from the cited definitions; **[conditional]**; **[open]**; **[recalled]** literature from memory, not re-checked, do not cite without checking. Notation as in the Plan: M(T) the move graph, F(T) the fill set, S(v,τ) the starts, L(T,c) the distance in M(T) from (v,c) to F(T).

## 0. A correction to the Plan's case list

At a level of Phase 1 with d = 5, T_m has minimum degree 5. So the configuration "degree-5 vertex adjacent to a degree-≤4 vertex" (every legal fan fills every start in ≤3 pure swaps) **never occurs at a d = 5 level**. It is vacuous for the algorithm as written. [hand] The Plan's §3 and §5 list it as a case the algorithm profits from; it does not. (It would matter only for a different reduction that works at a degree-5 vertex while a degree-≤4 vertex is still present, which the algorithm does not do.) Likewise the degree-6 4+4 separator-hole theorem is a landing fact about a hole of degree 6 reached after a slide. It is not a standalone d = 5 rule. The usable accepted level facts are: the separating-triangle fixed-hole theorem (≤2 swaps), the degree-5 mobility fact (local), and, for the single input G_n only, the belt walk.

## 1. (1) Unconditional statement: the algorithm is a verifier

Facts used, all [hand] and elementary:
- (E) By Euler, Σ(6 − deg) = 12, so every spherical triangulation on m ≥ 5 vertices has a vertex of degree 3, 4 or 5. A d = 5 level has a degree-5 vertex, and by Lemma 1.2(c) some fan at it is legal, hence a pair exists at every level.
- (O) Lemma 1.2(d): T^*_τ is a simple spherical triangulation on m − 1 vertices. So Phase 1 has at most N − 4 levels and every T_m is a legitimate input.
- (S) Soundness: every move preserves properness (Lemma 1.3(a)); a fill gives a proper extension (Lemma 1.3(c)); the d = 3, 4 steps are the checked Jordan steps of `hole-induction.md`.

Two versions of the algorithm, both total.

**A_R (rule version).** Fix any deterministic pair rule R: (T with min degree 5) → (v, legal τ), for instance "least vertex index, least fan index". Phase 1 and Phase 2 as in the Plan, with the d = 5 fill step done by BFS of M(T_m) from (v_m, c_{m−1}), stopping at the first state of F.

**Theorem U1 [hand].** For every input T and every rule R, A_R halts. Its output is one of:
1. a proper 4-colouring of T (this can be checked in O(N));
2. FAIL(m, T_m, v_m, τ_m, c), where T_m is a min-degree-5 triangulation reached in Phase 1, c ∈ S(v_m, τ_m) is a colouring of T_m − v_m, and the **whole component of (v_m, c) in M(T_m) has been enumerated and contains no state of F(T_m)**.

*Proof.* Halting: ≤ N − 4 levels by (O); each BFS runs on the finite set Ω(T_m), |Ω(T_m)| ≤ m·4^{m−1}, and M is undirected so the BFS sees the whole component. Output (1) is proper by (S). Output (2) is the only other exit, and it is exactly the exhaustion of a finite component. ∎

**Corollary U1′ [hand].** In case 2, VH(v_m, τ′) is false for every legal fan τ′ at v_m for which c ∈ S(v_m, τ′). In particular VH(R(T_m)) is false. The stuck state (v_m, c) does not depend on the fan, because M(T) is defined from T, the hole and c only. A finite stuck component is a certificate; checking it needs the enumeration (or a closed set X ∋ (v,c) with X ∩ F = ∅ and X closed under moves), which is of size up to m·4^{m−1}. Checking is in PSPACE (undirected reachability in an implicit graph) and no better bound is claimed. [hand for PSPACE; the exponential size is not claimed to be necessary]

So A_R is a verifier for the family of statements {VH(R(T_m))}. It can only fail at a pair that is a **pair-level** counterexample (not a VH∃ counterexample: other pairs at T_m may be good). Two things follow:
- A_R may fail even if VH∃ is true, because R may pick a bad pair. Completeness of A_R needs the stronger statement that R(T) is good for every T that occurs in the chain. [hand]
- By the four-colour theorem every input is 4-colourable, so a FAIL says that the *method* fails at that pair, never that T is uncolourable. [recalled: 4CT]

**B (backtracking version).** B(T): if T has a vertex of degree 3 or 4, recurse on its unique child and fill (a FAIL propagates). If T has min degree 5, for each legal pair p in turn: c := B(T^*_p); if c is a colouring and the BFS from (v_p, c) hits F, return the filled colouring. If no pair succeeds, return FAIL(T).

**Theorem U2 [hand].** B halts on every input. It returns either a proper 4-colouring or a FAIL at a triangulation T′ with the following property: T′ has min degree 5, order < N, arises from T by Phase-1 steps, and **VH∃(T′) is false**, with the refutation being an explicit family (c_p) of stuck starts, one for each legal pair p of T′. Hence: if VH∃ holds for all triangulations of order < N then B succeeds on every input of order N, and B fails on T only if a VH∃-counterexample of order < N exists.

*Proof.* The recursion tree is finite by (O). Take a FAIL node T′ of minimal depth in the tree among FAIL nodes whose subtree has no FAIL below, that is, a FAIL node all of whose explored children returned colourings. Such a node exists if the root fails (follow a FAIL child downward; at degree-3/4 nodes the single child must fail, at degree-5 nodes either some child fails, continue, or none does, stop). At that node every legal pair p was tried, B(T′^*_p) returned a colouring c_p ∈ S(p), and the BFS from (v_p, c_p) exhausted a component with no F. So VH(p) is false for every legal pair p, which is ¬VH∃(T′). The converse direction is Theorem A of `vh-exists.md` run inside B: under VH∃ at every order, induction gives a good pair whose c_p reaches F. ∎ (This is Remark 2.3 used as an algorithm.)

**Cost of B.** The tree has at most ∏_m (5·(#degree-5 vertices of T_m)) ≤ (5N)^N leaves; each leaf level costs the BFS. No polynomial bound; B is a proof-checking device, not a fast algorithm. [hand]

## 2. (2) Unconditional running time

**Per-step costs [hand].** Degree-3 step: O(m). Degree-4 step: one component computation and a Jordan swap: O(m). Pair selection with a fixed rule: O(m) (scan for degree-5 vertices, O(1) chord legality tests). Updating T_m → T_{m−1}: O(1) edge edits, rotation system maintained. So Phase 1 plus all d = 3, 4 fills cost O(N²). One BFS node: O(m) per move (one component computation of a 2-colour subgraph with ≤ 3m edges), branching b ≤ 3(m−1) + 5.

**Theorem U3 (instance-sensitive bound) [hand].** Let D5 be the set of levels of A_R with d = 5, and let L_m be the actual distance from (v_m, c_{m−1}) to F(T_m) (L_m = ∞ if stuck). With breadth-first search and a hash set of visited states, the running time is

  O(N²) + Σ_{m∈D5} O( m · min( (3m+5)^{L_m}, m·4^{m−1} ) ).

It is unconditional. The second term in the min gives the exponent-free worst case: **2^{O(N)}** (at most O(N³·4^N) overall), with no better unconditional bound known. Space O(visited), or O(L·m) by iterative deepening at the cost of a factor of at most L. If L_m = ∞ at some level, A_R returns FAIL after enumerating the whole component; this too is within the second term. A global colour renaming divides the state count by at most 24 and does not change the exponent. [hand]

**Where accepted theorems give a polynomial bound.** Be precise: a bound for the whole algorithm needs *every* d = 5 level of the chain to be covered, and the chain T_N, T_{N−1}, … leaves any named family at the first step. So only the following are unconditional and total:
- **U3(a) [hand].** Inputs on which Phase 1 never reaches min degree 5 (D5 = ∅): O(N²). This is a real, non-trivial class (all inputs whose greedy degree-≤4 elimination with diagonals never stalls), but it is not described by any accepted structural theorem; membership is decided by running Phase 1.
- **U3(b) [hand, from the accepted fixed-hole theorem].** Use the rule R_sep: if some degree-5 vertex lies on a separating triangle, take its apex-a fan. Then L_m ≤ 2 for every start at the fixed hole, a search to depth 2 has ≤ (3m)² nodes of cost O(m), so that level costs O(m³) (and triangle detection is O(m) on planar graphs, [recalled]). Hence on any input where **every** d = 5 level of the chain has a degree-5 vertex on a separating triangle, the total is O(N⁴). The hypothesis is again a property of the chain, not of T, and is open to be shown for any natural class.
- **U3(c) [hand].** Single level on the belt G_n with unequal poles: ≤ 2n deterministic slides, O(n²) for that level (only the top level; the lower levels are T^*-graphs, not belts).
- Mobility (degree-5 hole: 1 swap, or ≤1 swap and 1 slide to a chosen neighbour) bounds only the first hop and does not bound L.

**Consequence for the min-degree-5 core [hand].** By Math's corollary (every vertex of a separating triangle in a VH∃ failure has degree ≥ 6), a deepest failure T′ of B (Theorem U2) has no degree-5 vertex on a separating triangle. So the cases in which U3(b) applies are exactly the cases in which B cannot fail, and the failure set lives in min-degree-5 triangulations whose degree-5 vertices lie on no separating triangle. Four-connectivity of T′ is *not* proved for plain VH∃ (START-HERE §6), so I do not say T′ is 4-connected.

## 3. (3) The exact extra lemma for polynomial time

**Lemma P(K, R) [open; this is the exact statement].** There are a constant K and a rule R computable in time poly(m), selecting a degree-5 vertex v and a legal fan τ of every min-degree-5 spherical triangulation T on m vertices, such that for **every** c ∈ S(v, τ) the distance from (v, c) to F(T) in M(T) is at most K.

**Theorem [conditional on P(K, R), hand].** Then A_R succeeds on every input (induction: each T^*_τ is again a triangulation, so a colouring exists, and its restriction is in S(v,τ), which reaches F within K moves), and its running time is O(N²) + O(N · N^{K+1}) = **O(N^{K+2})**, by Theorem U3 with b = O(m). [hand]

Why each ingredient is needed:
- **Constant K, not just bounded K(m).** With b = Θ(m) generic search costs m^{Θ(K(m))}. This is polynomial iff K = O(1); quasi-polynomial for K = O(log m); super-polynomial beyond. So K(m) = poly(m) (as in the belt, 2n) gives a polynomial algorithm **only** with an additional search-free rule (the belt's deterministic walk), and then the cost is rule length × O(m). [hand]
- **A computable rule R, not just VH∃.** Existence of a good pair gives B (Theorem U2), whose tree is exponential. R must be polynomial-time and good for every T in the chain. Remark 2.3 shows the quantifier cannot be weakened, so there is no free gain from picking the pair after the colouring. [hand]
- **Universality over S(v,τ).** The colourings reaching a level are produced by the recursion and are not controlled. Weakening P to "L ≤ K on the colourings that actually occur" has no handle. [hand]

**Best bound derivable from the known results [hand]:**
- General: L ≤ |component| ≤ m·4^{m−1}. This is the only unconditional universal bound known to me. No sub-exponential bound on the diameter of such a component is known to me. (For comparison [recalled, unverified]: Kempe-change diameter bounds of polynomial type are known for 5-colourings of planar graphs and for degenerate graphs with colours exceeding the degeneracy; I know of no such bound for 4-colourings of planar triangulations, and the 4-colour case is the whole difficulty.)
- K = 2 for a rule that picks the apex-a fan at a degree-5 vertex on a separating triangle (accepted fixed-hole theorem), valid only when such a vertex exists.
- K = 3 for a degree-5 vertex adjacent to a degree-≤4 vertex, but see §0: vacuous at d = 5 levels.
- Belt: K(n) = 2n, unequal poles, walk rule, single graph G_n.
- Data: κ ≤ 5 on saved WP19 orders 21–24 [post hoc, from the Plan]: supports the conjecture P(5, R) and nothing more.

So the exact open gap is: **P(K, R) restricted to the min-degree-5 triangulations having no degree-5 vertex on a separating triangle**, which includes the cases of Math's "core" at order ≥ 12 and, given the pending items, perhaps more. A proof of P(K, R) implies VH∃ (so it is at least as hard) and adds only the constants and the rule.

## 4. (4) Is the fill search exponential only in the colouring count? Is there a polynomial abstraction?

**Answer: no polynomial abstraction is known, and I do not expect a naive one. The exponential is in a global quotient, not in an artefact of encoding.** [hand, with open points]

1. **What is small.** The local data of a state are constant-size: the colouring of the link 5-cycle is one of 3⁵ − 3 = 240 proper colourings (two orbits under colour renaming: types (2,2,1) and (2,1,1,1)), plus, for each of the 6 colour pairs, the partition of the five link vertices into {a,b}-components of T − h. That is a constant-size abstraction (≤ 240 × a constant). [hand]
2. **Why it is not closed.** A swap on a component K of {a,b} recolours vertices of K, which changes which vertices carry colours a, b and therefore changes the {a,c}, {b,c}, {a,d}, {b,d} components of T − h globally: components merge and split along K. So the effect of a swap on the link-partition data depends on how K sits inside the other two-colour subgraphs, not on the link data. A far swap (not meeting the link) can change later link-component structure (this is why the Plan correctly rejects "only link-meeting swaps matter"). The exact bisimulation quotient of M(T) with respect to the F predicate is a quotient of the Kempe-class structure, and I know of no description of it of polynomial size. [hand]
3. **The slide moves reduce the state space only by a constant.** A slide changes the hole and recolours one vertex; it is O(d). It does not add a global effect, but it changes which vertex is the hole, so the abstraction of 1 must be recomputed at the new hole: no help for closure. [hand]
4. **Reduction by Lemma 3.1 [hand].** Reachability of F from a start is constant on Kempe classes of T^*_τ. So the search can be run on the *class graph* of T^*_τ (classes of T^*_τ joined by moves of T − v not respecting the chords), a quotient of Ω. This can be much smaller in practice, but the number of Kempe classes is not known to be polynomial for planar triangulations. [hand; size of quotient open]
5. **Interface (trace-game) abstractions.** Across a separating cycle of length r the interface state is a ring colouring (constant, ≤ 4·3^{r−1} for fixed r). A side's behaviour is then a reachability relation on ring states, but computing that relation for a side is the same Kempe-reachability problem on a smaller graph, so this reduces the exponent only if sides stay small. It gives no polynomial algorithm on its own. [hand; matches the pending trace-game pages]
6. **Hardness context [recalled, unverified].** Kempe reachability (is one given colouring reachable from another by Kempe changes) is PSPACE-complete for general graphs with a fixed number of colours ≥ 3 (Bonamy et al., "Diameter of colorings under Kempe changes"; planarity and bounded degree restrictions for some k, details not re-checked). That is about reachability between two *given* colourings in general graphs, and does not decide our problem (a target set F defined by link colour count, on triangulations, with all 4-colourings of planar triangulations admitting the four-colour theorem structure). No hardness is claimed for our problem, and no algorithm either. [open]
7. **What is polynomial.** For fixed k, the question "is there a pure-swap path of length ≤ k from c to F" is solvable in O(m^{k+1}) (XP in k). For k ≤ 2 mixed paths reduce to pure swaps (compiled `short_fill`), so the question for ℓ ≤ 2 costs O(m³). Whether it is FPT in k is open to me. A *locality lemma* LOC (shortest pure fills only swap components within a bounded component-adjacency distance of the link-meeting components) would cut the branching, but LOC is not proved and may be false. [open]

## 5. Summary

| Item | Status |
|---|---|
| A_R and B halt on every input (finite component, ≤ N − 4 levels) | [hand] |
| A_R output: proper colouring, or FAIL = stuck start at a pair (pair-level counterexample); B output: proper colouring, or a minimal VH∃ counterexample with an explicit family of stuck starts | [hand] |
| B succeeds on all inputs of order N iff no VH∃ counterexample below N is hit; A_R may fail even if VH∃ holds | [hand] |
| Time bound (U3): O(N²) + Σ_{D5} O(m·min((3m+5)^{L_m}, m·4^{m−1})); worst case 2^{O(N)} | [hand] |
| Polynomial total on named classes: only chains with D5 = ∅ (O(N²)) or all d = 5 levels on separating triangles (O(N⁴)); neither class is characterised structurally | [hand] |
| Degree-5-next-to-degree-≤4 theorem is vacuous at d = 5 levels | [hand] |
| Polynomial time iff P(K, R): constant K and a poly-time rule R; then O(N^{K+2}). Best known K: 2 on separating triangles; K = 5 conjectural | [conditional]; [open] |
| Polynomial abstraction of the fill search | [open]; no closed constant-size abstraction exists in the obvious sense (swaps are global) |
| 4-colouring in O(N²) unconditionally is known by the computer-verified route | [recalled] |
