# What a minimal failure of R\* must look like

Studio intel (token `studiointel`), 6 October 2026. Hand work only; nothing was computed for this note. Labels: [hand], [cited], [open]. "Cited" here means: taken from a message or page of another team, named in the line, **not re-derived by me**. Nothing here changes a status.

## 0. What is being attacked

Class 𝒞(φ): 4-connected spherical triangulations T with a protected face φ, at most two degree-4 vertices, all on φ, every other degree ≥ 5 (audit 13:25, §2) [cited].

R\*: some degree-5 vertex v ∉ φ is **clean**: every colouring of T − v reaches a filled state (link of v uses ≤ 3 colours) by whole-component Kempe swaps in T − v. Chain: R\* ⇒ VH_C ⇒ VH∃ ⇒ 4CT [hand, Navigator rev. 122, conditional theorem].

Exact reformulation (MathConjectureR §1) [cited]: for an unfilled state s at a degree-5 hole, if s is not doubly locked one swap fills it; so v is unclean iff some Kempe class at v consists entirely of **doubly locked** (DL) states (a *targetless* class). Radius r(s) = 1 + (Kempe distance from s to a non-DL state); finite for all s at v iff v is clean.

**A failure of R\*** is a pair (T, φ) in 𝒞 where every degree-5 vertex off φ is unclean, i.e. has a targetless class. Note the asymmetry the search must respect: every *tested* graph has finite radius everywhere (radius sup ≥ 4, T4 and the order-28 (6⁵) hole), and I know of no targetless class on any graph. So a failure needs *infinite* radius at every off-φ degree-5 vertex. Large finite radius everywhere is evidence of tension, not a failure.

## 1. Constraints on a failure [hand, from cited inputs]

Let n_d be the number of degree-d vertices, U the set of degree-5 vertices off φ, S the set of vertices of degree ≥ 6.

**C1 (Euler).** Σ(6 − d) = 12, so n₅ = 12 − 2n₄ + Σ_{d≥7}(d − 6) ≥ 12 − 2n₄ ≥ 8.

**C2 (U is large).** |U| ≥ 9 − n₄ ≥ 7 (audit 13:25 §2: the Euler repair; Math 12:33 for the strengthening to ≥ 12 vertices with ≤ 1 neighbour of degree ≥ 12) [cited]. So a failure has at least seven unclean degree-5 vertices, and the hypotheses below apply to each.

**C3 (no degree-≤4 neighbour).** A degree-5 vertex next to a vertex of degree ≤ 4 fills every start in ≤ 3 pure swaps (Math 17:27, MathVHCoreAdvance) [cited]. So no v ∈ U has a neighbour of degree ≤ 4. In particular U avoids the (at most two) degree-4 vertices' neighbourhoods.

**C4 (at least two big neighbours).** Theorem H, Theorem HP and the degree-≤4 result (Navigator rev. 122) [cited]: R\* holds at holes with at most one neighbour of degree ≥ 6. Hence every v ∈ U has m(v) ≥ 2 neighbours of degree ≥ 6, with m(v) ∈ {2,3,4,5}. HP in particular excludes (5,5,5,5,x) links; the (5,5,5,6,6)-type links are exactly the first open ones.

**C5 (counting only gives a weak floor).** Edges e(U, S) ≥ 2|U|, and each s ∈ S has at most deg(s) edges to U, so Σ_S deg(s) ≥ 2|U|. With n₄ = 0, no degree ≥ 7 and n₅ = 12 this gives |S| ≥ 4, so n ≥ 16. This is all that degree counting yields: **pure (5,6)-triangulations, the duals of fullerenes with n₅ = 12, are not excluded by counting**, and they are the cheapest place for every degree-5 vertex to have many big neighbours. The Euler lemma (≥ 12 vertices with ≤ 1 neighbour of degree ≥ 12) only bites when degrees ≥ 12 are present.

**C6 (order floor, finite evidence).** Order ≥ 12 for a core member (Math) [cited]. Finite data, not a proof: WP18 (orders 12–22) and WP19 (orders 21–24) found every start fills within a few moves, and U∃ held on every graph [computed, scope: those graphs, a related but not identical statement: mixed moves, and the fill statement, not the pure-swap R\*; I have not checked that it covers R\* verbatim]. So any failure is expected at order ≥ 25, unless the WP statements differ from R\* in a way I have not checked. The candidate search should therefore start at order ≥ 26.

## 2. The Tait lock picture, and what it forces on the targetless class

Tait lock criterion (Long Table, `explore-vhphi/pathways/pd2_lock_proof.md`) [hand, cited]: in the Z₂×Z₂ edge-colouring of the dual of T − v, with pentagon node P and the link repeat at x_j, x_{j+2}: lock 1 ⇔ the (β,γ)-path Z1 leaving P by e_{j+2} returns by e_{j+1}; lock 2 ⇔ the (β,δ)-path Z2 leaving P by e_{j+4} returns by e_j. Both are about **how two two-colour dual paths pair up the five pentagon edges**.

Corollary (F keeps one lock) [cited]: if s has lock 2, then F s has lock 1, so F s is DL iff F s has lock 2, and the (β,δ) 2-factor is invariant under F.

What a targetless class therefore needs [hand, my reading, not a theorem]: a set 𝒦 of Tait colourings of the dual cubic graph H = (T − v)\*, closed under all Kempe-chain exchanges (changing the colouring along one two-colour cycle), such that on every member both Z-pairings are "returning" (both locks). In dual language: **a Kempe class of 3-edge-colourings of a planar cubic graph with one pentagonal face, in which every colouring has the same local pairing pattern at the pentagon.** A class of this kind is closed under switching any two-colour cycle that does not pass through P in a way that changes the pairing. So every two-colour cycle through the *pentagon's edges* in any member must reproduce the DL pairing. This is a strong rigidity: whenever a (β,γ)- or (β,δ)-path through P is a long path, the Kempe switch of a cycle that crosses it nearby must not change which P-edge it returns on.

I can't turn this into an exclusion; it tells the search what to optimise: **make every pentagon pairing path long and tangled, and keep every non-P two-colour cycle either disjoint from them or "parallel" to them.** That is the "Möbius-like" structure the A_r family has with its infinite F-orbits, and that is exactly what hill-climbing on the number of DL states and on the largest all-DL Kempe class should reward.

## 3. Degree-pattern candidates, ranked by how cheaply every degree-5 vertex can have ≥ 2 big neighbours [hand]

1. **Goldberg–Coxeter / icosahedral family GC(k,l)**: n = 10(k² + kl + l²) + 2, degrees 5 (twelve vertices) and 6; n = 12, 32, 42, 72, 92, 122, … For k, l ≥ 1 and (k,l) ≠ (1,0) every degree-5 vertex has m(v) = 5, so these are fully in the open region C4. They are 4-connected for k, l ≥ 1 apart from small cases [claim not checked; the program will check]. GC(1,1) (n = 32) and GC(2,0) (n = 42) are the first. Their symmetry (icosahedral group, order 60 or 120) reduces the twelve vertices to one class, so the radius computation is one hole.
2. **Fullerene duals with adjacent pentagons**, n = 26 upward: still only degrees 5, 6, with m(v) ≥ 2 forced by adjacency of the 5's being ≤ 3.
3. **Mixed (5,6,7) graphs**: n₅ = 12 + #7 + …, Euler bound C1; more freedom, more vertices. Second tier.

## 4. What the constructive search should do [hand, design]

- Fitness per graph and hole: ρ(v) = max over unfilled states s at v of r(s) (finite) or ∞ if a targetless class exists. Per graph, with φ chosen to give the failure the best chance: F(T) = max over faces φ of min over degree-5 v ∉ φ of ρ(v). In (5,6)-graphs with n₅ = 12 and at most 3 degree-5 vertices on a face, F(T) is the fourth-smallest ρ(v) (or the third, if the three smallest are on one face).
- Secondary fitness: fraction of DL states per hole, size of the largest all-DL Kempe class.
- Moves: edge flips that keep min degree ≥ 5 and degrees ≤ 7 and keep 4-connectivity, starting from the GC graphs and fullerene duals; and the symmetric constructions (§3.1). Hill-climbing with restarts from fixed seeds, not random sampling.
- Kill criteria and certificates are stated in the pre-registration message.

## 5. What I do not know [open]

- Whether a targetless class exists on any triangulation at all. (If one existed at *one* hole of an otherwise fine graph it would already disprove "every degree-5 vertex is clean" at that vertex but not R\*, which needs only one clean vertex.)
- Whether n ≥ 25 failures are excluded by a global argument. The Tait lock criterion does not obviously give one.
- Whether the F/B-orbit rigidity of §2 can be made into an invariant. If a short argument shows the number of DL states is bounded in terms of something that fails at the (6⁵) holes, the adversary search is finished; that is also a positive outcome to report.
