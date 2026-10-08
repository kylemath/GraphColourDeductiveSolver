# Rigid isolation on the sphere: proof [hand, independently reviewed — CORRECT with three expository gaps, now patched; every step data-checked]

**Revision after review (8 Oct 2026).** `TrackI-review/README.md` found the proof of Theorem 6 and of RI correct on the sphere (0 failures in 2,224,936 fresh DL states; every intermediate identity checked on 2,207,592), with three expository gaps G1–G3. They are fixed in place below; each edit is marked **[rev G1]**, **[rev G2]** or **[rev G3]**.
- **G1** (topology of S² − C, needed by Lemma R): a paragraph added after the proof of Lemma 4(b) showing that every component of S² − C other than R is a disc bounded by exactly one C_i, and that the disc D₀ beyond X contains e₀, e₄ and Y.
- **G2** (flip connectivity): Lemma R step 1 now inducts on an innermost pair of the *target* matching, not on an arbitrary consecutive pair.
- **G3** (planarity accounting): §0's "exactly four places" is replaced by the complete list of seven planar inputs. The review's off-sphere data (§4 there) show Lemma R step 2 is an independent planar input: on RP² its conclusion fails in 2,857 states whose outer matchings are combinatorially non-crossing; on the torus every failure comes through Lemma 2 and Euler, never through Lemma R.
- **Remark 7** is relabelled **[unproved, data-supported]**: no proof is written (review data: 19,448 link-free moves, 0 failures).
- One extra hypothesis made explicit (review §3a): Lemma R also needs Σ_I planar (disjoint arcs in R). It was already stated; with a crossing Σ_I it fails from 8 points.

Track I, 8 Oct 2026. Notation follows `TrackF/LockParity.md` and `TrackH/README.md`. Data references point to `README.md` §3 of this directory.

## 0. Statements

T is a triangulated sphere (simple), h a vertex of degree 5 with link x₀ … x₄ in rotation order, and c a proper 4-colouring of T − h that is unfilled with repeat index j. Indices are relative to j, so the link colours are (α, μ, α, A, B) at x₀ … x₄. Locks, π, K_{pq}(·) and DL are as in LockParity.md. **Rigid** means DL with pair-graph component counts (#αμ, #AB, #αA, #μB, #αB, #μA) = (1, 1, 2, 1, 2, 1) (TrackH H4).

Write **N(s)** for the total number of Kempe chains of a state s: the sum over the six colour pairs of the number of components of the pair graph in T − h.

> **Theorem RI (rigid isolation).** If c is rigid, then π(c) is not rigid.

> **Theorem 6 (chain-parity law).** For every DL state c at a degree-5 hole of a triangulated sphere,
> N(π(c)) − N(c) ≡ [π(c) is DL] (mod 2).

RI is the case N(c) = 8 of Theorem 6. On the sphere every DL state has N ≥ 8, with equality iff it is rigid (Lemma 3).
- If c is rigid and π(c) were rigid, then π(c) would be DL and N(π(c)) = 8 = N(c).
- But Theorem 6 then gives 0 ≡ 1.

**[rev G3]** Planarity enters in seven places:
1. Lemma 0 (Jordan: v-loops do not cross at v);
2. Lemma 1 (Euler's formula for plane multigraphs; the region/chain bijection itself holds on any surface);
3. Lemma 2 (Jordan: a v-loop separates corners);
4. Theorem D (used in Lemma 3, and for x₀ ∉ K in Lemma 4b — the latter also follows from Lemma 2, since X separates corner (e₁,e₂) from corner (e₄,e₀));
5. the disc structure of S² − C (G1, Jordan region tree + Schoenflies; paragraph after Lemma 4);
6. step (P-ii) of Lemma 5 (disjoint paths in a disc give a non-crossing matching);
7. Lemma R step 2 (Schoenflies: a band on a single curve splits it).

Item 7 is used non-trivially and independently of item 6: on RP², Lemma R's conclusion fails in states whose outer matchings are non-crossing (TrackI-review §4). On the torus, Lemma R's conclusion never failed; the failures come through items 2–3. (The original text said "exactly four places" and omitted items 4, 5, 7 and the Euler content of item 2.)

## 1. Tait form

**The graph G.**
- F = T\* is the cubic dual. The five faces at h form a 5-cycle P = h\* in F.
- G := F / P contracts P to a single vertex v. G is a plane multigraph without loops.
- v has degree 5; every other vertex is cubic.
- Faces of G ↔ V(T) − h, and edges of G ↔ edges of T − h.
- e_t is the edge at v dual to the link edge x_t x_{t+1}. The rotation at v is e₀, e₁, e₂, e₃, e₄, and the link vertex x_t is the face in the corner (e_{t−1}, e_t).

**The colouring.**
- Identify the four colours with ℤ₂², via any bijection. The edge of G dual to uw gets the colour c(u) + c(w) ≠ 0.
- Name the colours 1 := α+μ, 2 := α+A, 3 := α+B.
- An edge has colour i iff its two ends lie in a common pair of the partition P_i: P₁ = {αμ|AB}, P₂ = {αA|μB}, P₃ = {αB|μA}. This does not depend on the bijection.
- Every cubic vertex sees 1, 2, 3 (a face of T has three distinct colours). At v the colours are (1, 1, 2, 1, 3).

**The subgraphs.** M_i is the set of edges of colour i. Let H := M₂ ∪ M₃, F12 := M₁ ∪ M₂ and F13 := M₁ ∪ M₃.
- Every cubic vertex has degree 2 in each of them.
- v has degree 2 in H (e₂, e₄), degree 4 in F12 (e₀, e₁, e₂, e₃) and degree 4 in F13 (e₀, e₁, e₃, e₄).
- k(S) is the number of connected components of S.
- If v has degree 4 in S, its edges lie on two closed trails through v (the *v-loops*). The **pairing** p(S) records which v-edges are joined by a v-loop.

**Lemma 0 (Jordan).**
- (a) A v-loop passes v once and every other vertex at most once, so it is a simple closed curve.
- (b) The two v-loops of S meet only at v. On the sphere they do not cross there, because two simple closed curves meeting in one transversal crossing contradict the Jordan curve theorem.
- So p(S) is one of the two non-crossing pairings of S's four v-edges in rotation order.

**Lemma 1 (regions = chains; sphere).** Let S₁ = H, S₂ = F13 and S₃ = F12, so S_i is the subgraph without colour i. The vertex sets of the components of the two pair graphs of P_i are exactly the face sets of the regions of S² − S_i. Hence:

- #αμ + #AB = 1 + k(H)
- #αA + #μB = 2 + k(F13)
- #αB + #μA = 2 + k(F12)

and so N(s) = 5 + k(H) + k(F12) + k(F13). The same holds for every unfilled state in its own frame.

*Proof.*
- An edge of G not in S_i has colour i, and the two faces it separates lie in a common pair of P_i. Conversely, adjacent same-class vertices of T − h are faces separated by a colour-i edge.
- Every vertex of G lies on S_i, so a region of S² − S_i is a union of open faces and open non-S_i edges, connected across those edges. This gives the bijection.
- The count is Euler's formula for plane multigraphs: regions = |E(S)| − |V(G)| + 1 + k(S), with |E(H)| = |V(G)| and |E(F12)| = |E(F13)| = |V(G)| + 1. ∎

**Lemma 2 (locks = pairings; sphere; cf. NightG66IPR §1.3).**
- Lock1 ⇔ p(F12) = (e₀e₃)(e₁e₂).
- Lock2 ⇔ p(F13) = (e₁e₃)(e₀e₄).

*Proof.* Take Lock1 first. x₁ is the face in the corner (e₀,e₁) and x₃ the face in the corner (e₂,e₃). By Lemma 1, Lock1 holds iff these two faces lie in one region of S² − F12.
- **p(F12) = (e₀e₁)(e₂e₃).** The v-loop through e₀, e₁ bounds a disc containing the corner (e₀,e₁) but not the corner (e₂,e₃). The other loop touches it only at v, from the other side. So the faces lie in different regions.
- **p(F12) = (e₀e₃)(e₁e₂).** Run a path just outside the loop L′ through e₁, e₂, from the corner (e₀,e₁) to the corner (e₂,e₃). Every vertex of L′ has both its F12-edges on L′, so the path crosses only colour-3 edges and meets no F12-edge. The two faces therefore lie in one region.

Lock2 is the same argument with the faces x₁ and x₄ (corners (e₀,e₁) and (e₃,e₄)) and the subgraph F13. ∎

**Lemma 3 (rigid states).**
- A DL state c on the sphere has #αA ≥ 2 and #αB ≥ 2 (Theorem D), so N(c) ≥ 8.
- c is rigid ⇔ N(c) = 8 ⇔ k(H) = k(F12) = k(F13) = 1.
- If c is rigid, then F13 = X ∪ Y, where X is the v-loop through e₁ and e₃ and Y is the v-loop through e₀ and e₄ (Lemma 2).

*Proof.*
- By Theorem D (formal), Lock2 gives x₀ ∉ K_{αA}(x₂), so αA has at least 2 components. Likewise Lock1 gives x₀ ∉ K_{αB}(x₂).
- With the other counts at least 1, Lemma 1 gives the lower bounds (2, 3, 3) for the three partitions, so N ≥ 8, and equality holds exactly in the rigid case.
- A connected F13 in which v has degree 4 is the union of its two v-loops. ∎

**Lemma 4 (π in Tait form; sphere).** Let c be DL, K = K_{αA}(x₂), and R the region of S² − F13 formed by K's faces (Lemma 1).

- (a) The Tait colouring of π(c) is that of c with 1 ↔ 3 exchanged on C := ∂R.
- (b) C = X ∪ Z₁ ∪ … ∪ Z_r, where X is the v-loop of F13 through e₁, e₃ and the Z_i are components of F13 not through v. If c is rigid, then C = X.
- (c) Let c^C denote the switched colouring. π(c) has frame j + 3 and roles (α, B, μ, A) (LockParity §5.2). Its own colour names are 1′ = 3, 2′ = 1 and 3′ = 2, and its v-labels are e′_t = e_{t+3}. Hence:
  - H′ = F12 Δ C
  - F12′ = F13 (as an edge set)
  - F13′ = H Δ C
- (d) π(c) always has Lock1, and **π(c) is DL ⇔ p(H Δ C) = (e₁e₄)(e₂e₃)**.

*Proof.*
- **(a)** π swaps α ↔ A on K. The colour of the dual of uw changes iff exactly one of u, w lies in K, and then it changes by α + A = 2, i.e. 1 ↔ 3. Those edges are exactly the edges separating a face of R from a face outside R.
- **(b)** The corners of R at v are (e₁,e₂) and (e₂,e₃), since they contain x₂ and x₃ ∈ K. The other three corners are not in R: x₁ and x₄ have colours μ and B, and x₀ ∉ K by D2. So ∂R uses e₁ and e₃ at v and no other v-edge.
  - At a cubic vertex the colour-2 edge separates two corners of one region, so ∂R contains either both F13-edges of that vertex or neither.
  - Hence ∂R is a union of whole F13-components and v-loops: the v-loop X through e₁ (which returns through e₃ by Lemma 2), plus whole cycles Z_i.
  - If c is rigid, F13 = X ∪ Y and Y ⊄ ∂R, so C = X.

**[rev G1] Topology of S² − C.** Write C = C₀ ∪ … ∪ C_r with C₀ = X and C_i = Z_i; these are pairwise disjoint simple closed curves (X by Lemma 0(a), each Z_i a cycle of the 2-regular part of F13).
- R is a connected component of S² − C (open, connected, frontier ⊆ C).
- Every C_i lies in the frontier of R: each C-edge separates an R-face from a non-R face, by definition of C = ∂R.
- r + 1 disjoint simple closed curves cut S² into r + 2 regions, and the graph with a node per region and an edge per curve (joining the two regions on its sides) is a tree (Jordan, by induction on r).
- R is incident with all r + 1 curves, so the tree is a star centred at R. Hence each other region D_i is incident with exactly one curve C_i, and is the component of S² − C_i not containing R; by Schoenflies it is an open disc with ∂D_i = C_i.
- D₀, the region beyond X, contains the corners (e₃,e₄), (e₄,e₀), (e₀,e₁) at v, hence the edges e₀ and e₄, and (rigid case or not) the loop Y of F13 through e₀, e₄.

This is exactly the setting assumed in Lemma R.
- **(c)** Direct substitution, using C ⊆ M₁ ∪ M₃.
- **(d)** Apply Lemma 2 to π(c) in its own frame.
  - Lock1(π c) ⇔ p(F13) = (e′₀e′₃)(e′₁e′₂) = (e₃e₁)(e₄e₀). This is p(F13) for the DL state c.
  - Lock2(π c) ⇔ p(H Δ C) = (e′₁e′₃)(e′₀e′₄) = (e₄e₁)(e₃e₂). ∎

(Data: π(c) "loses Lock 2" in every non-DL image; TrackH §6.)

## 2. The switching-parity lemma

**Lemma 5 (sphere).** For every DL state c, with C = ∂R as in Lemma 4,

  k(H) + k(F12) + k(H Δ C) + k(F12 Δ C) ≡ [p(H Δ C) = (e₁e₄)(e₂e₃)] (mod 2).

**Proof of Theorem 6 from Lemma 5.**
- By Lemmas 1 and 4(c), N(π c) − N(c) = k(F12ΔC) + k(F13) + k(HΔC) − k(H) − k(F12) − k(F13).
- By Lemma 5 this is ≡ [p(HΔC) = (e₁e₄)(e₂e₃)], which equals [π(c) DL] by Lemma 4(d). ∎

### 2.1 Lemma R (rotation parity; the planar input)

**Setting.**
- C₀, …, C_r are disjoint simple closed curves in S², forming the boundary of a connected open region R. The other complementary components are open discs D₀, …, D_r with ∂D_i = C_i.
- On each C_i lie an even number of points in cyclic order. B₁ and B₃ are the two complementary sets of arcs of C_i joining consecutive points (the two alternating perfect matchings). On all circles together they are again written B₁, B₃.
- Each point is labelled I or O.
- Σ_I is a fixed family of disjoint arcs in R pairing the I-points. Σ_O is a family of disjoint arcs, each inside some D_i, pairing the O-points of C_i. (Equivalently, Σ_O is a non-crossing matching on each C_i.)
- For B ∈ {B₁, B₃}, B ∪ Σ_I ∪ Σ_O is a disjoint union of simple closed curves. λ(B, Σ_O) denotes their number.

**Lemma R.** λ(B₁, Σ_O) + λ(B₃, Σ_O) mod 2 does not depend on Σ_O.

*Proof.*
1. **Flips connect.** Any two non-crossing perfect matchings of the O-points of one circle C_i are connected by *flips*. A flip replaces two arcs of Σ_O that border a common face of D_i − Σ_O by the two arcs obtained by band surgery along a core γ inside that face.
   - **[rev G2]** Induction on the number of O-points of C_i, transforming Σ_O into a target non-crossing matching Σ′_O. Choose (s, s′) to be an *innermost* arc of the target Σ′_O, i.e. a pair of Σ′_O whose points are consecutive among the O-points of C_i (one always exists for a non-crossing matching). If Σ_O already pairs s–s′, skip to the last bullet. Otherwise Σ_O pairs s–q and s′–r with q ≠ s′.
   - No arc of Σ_O ends on the boundary segment from s to s′. So the arcs at s and s′ border the face adjacent to that segment, and a flip along a core γ in that face gives the non-crossing pairing (s s′)(q r) (not (s r)(s′ q), because γ lies in a disc face).
   - Now both matchings contain (s s′). Delete s and s′ and apply the induction to the remaining O-points. Arcs already removed by the induction lie nested against the boundary, so this face argument still applies at later steps.
2. **Band surgery changes λ by ±1 on the sphere.** Do surgery on a system of disjoint simple closed curves along an arc γ whose interior misses all curves.
   - If the ends of γ lie on two different curves, those curves merge: −1.
   - If both ends lie on the same curve σ: γ lies in one component of S² − σ, which is a disc (Jordan–Schoenflies), and is a cross-cut of it. The surgery splits σ into the two cycles of the theta graph σ ∪ γ: +1.
3. **The same flip acts on both systems.** A flip changes only Σ_O. Its core γ lies in D_i, so it is disjoint from C_i ⊇ B₁ ∪ B₃, from Σ_I ⊂ R, and from the other Σ_O arcs. It therefore acts on both B₁ ∪ Σ and B₃ ∪ Σ, changing each λ by ±1, and the sum keeps its parity. ∎

*Check:* `ti_lemmaR.py` verifies Lemma R for every I/O labelling with ≤ 12 points on one circle, with 0 failures. For crossing (non-planar) O-matchings it fails already at 4 points.

### 2.2 Proof of Lemma 5

**Points and the two alternating matchings.**
- Every cubic vertex w on C has its two C-edges coloured 1 and 3, and one *transverse* edge t_w of colour 2.
  - This holds because C ⊆ F13 consists of whole F13-components and v-loops (Lemma 4b).
- **On each Z_i** (even length, colours alternating), B₁ is the set of colour-1 edges and B₃ the set of colour-3 edges.
- **On X = v w₁ … w_{2p} v** (with e₁ = vw₁ and e₃ = w_{2p}v, both of colour 1, so X has length 2p + 1), split v into two adjacent points: a next to w₁, and b next to w_{2p}. The cyclic sequence a, w₁, …, w_{2p}, b carries:
  - B₁ = {aw₁, w₂w₃, …, w_{2p}b}: the colour-1 edges of X, with e₁ at a and e₃ at b;
  - B₃ = {w₁w₂, …, w_{2p−1}w_{2p}} ∪ {ba}: the colour-3 edges of X, plus a *virtual* arc through v.

**Ends.**
- Each point carries one end: w carries t_w, a carries e₂, and b carries o, where o = e₄ for the "H family" and o = e₀ for the "F12 family".
- e₂ lies in R, between the two R-corners at v. e₀ and e₄ lie outside R̄, in D₀.
- Label each point I or O according to the side its end enters. The labels are the same for both families, because the transverse edges are common to H and F12 (both contain M₂).

**Off-C paths.** Let S ∈ {H, F12}.
- Every vertex off C has both its S-edges off C.
- Every w on C has exactly one S-edge off C, namely t_w. (The other S-edge at w — colour 3 for H, colour 1 for F12 — lies on C.)
- At v, the S-edges off C are e₂ and o.
- So S − C is a disjoint union of paths pairing the ends, plus f_S cycles disjoint from C. A path's interior avoids C, so it stays on one side. This gives a pairing N^S of the points: I with I, and O with O within one disc D_i.

**(P-i) The I-parts coincide.** R contains no vertex (every vertex lies on F13) and no F13-edge. So each I-path is a single colour-2 edge, i.e. the I-pairings of H and F12 are the same family Σ_I of colour-2 edges in R.

**(P-ii) The O-parts are non-crossing.** The O-paths into D_i are disjoint arcs in a closed disc with ends on its boundary C_i, so they pair the O-points of C_i non-crossingly. On X, the only O-point at v is b, so the cyclic order is well defined. **This is the step that uses that the far side of X is a disc.**

**Loop counts.** The four Tait subgraphs give:

- (L1) λ(B₃, N^H) = k(H) − f_H. H meets C in M₃ ∩ C = B₃, and H passes v from e₂ to e₄, which is the virtual arc ba.
- (L2) λ(B₁, N^H) = k(HΔC) − f_H + [p(HΔC) = (e₁e₂)(e₃e₄)]. HΔC = (H − C) ∪ (M₁ ∩ C) has v-degree 4. In B₁ ∪ N^H, a joins e₁ to e₂ and b joins e₃ to e₄, so the cycles of B₁ ∪ N^H are the curves of HΔC smoothed at v as (e₁e₂)(e₃e₄). This smoothing gives one more curve than the number of components iff it agrees with the pairing.
- (L3) λ(B₃, N^F) = k(F12ΔC) − f_F. F12ΔC passes v from e₀ to e₂, which is the virtual arc.
- (L4) λ(B₁, N^F) = k(F12) − f_F + [p(F12) = (e₁e₂)(e₃e₀)] = k(F12) − f_F + 1, since c has Lock1 (Lemma 2).

**Conclusion.**
- By (P-i), (P-ii) and Lemma R (with Σ_I the colour-2 edges in R, and Σ_O realised by the O-paths), λ(B₃, N^H) + λ(B₁, N^H) ≡ λ(B₃, N^F) + λ(B₁, N^F).
- Substituting (L1)–(L4) and cancelling f_H and f_F (each appears twice):

  k(H) + k(HΔC) + [p(HΔC) = (e₁e₂)(e₃e₄)] ≡ k(F12ΔC) + k(F12) + 1.

- By Lemma 0, p(HΔC) is one of the two non-crossing pairings. So [p(HΔC) = (e₁e₂)(e₃e₄)] = 1 − [p(HΔC) = (e₁e₄)(e₂e₃)], and Lemma 5 follows. ∎

**A remark on v.** v is the only vertex of degree 4 in any Tait subgraph. Lemma 5 works because v lies on C and is resolved explicitly.

For a Kempe move on curves *not* through v, the same argument needs a correction term for the pairings of v in the two other subgraphs. With Lemma 2 this gives:

> **Remark 7 [unproved, data-supported].** A Kempe swap of a component containing no link vertex preserves N + L1 + L2 (mod 2), where L1 and L2 are the lock indicators. This is checked on 281,230 link-free moves with 0 failures (`ti_moves.py`).

The uncorrected statement "N mod 2 is preserved" is **false**: it fails on 111,912 of those moves.

(Status after review: no proof of Remark 7 is written; it was labelled [hand] in error. The independent review re-checked it on 19,448 link-free moves on fresh spheres with 0 failures; N alone changes parity in 8,024 of them. A proof along the lines of Lemma 5 looks feasible — ∂R′ is a union of S_i-cycles avoiding v, and v becomes an off-C degree-4 vertex in two subgraphs — but nothing downstream should rely on it until it is written. Cross-reference: `TrackC/README.md` §6.4 notes that both Remark 7 and Theorem 6 would follow from one conjectured per-state identity, the mod-4 chain-count formula F (0 failures on 71k sphere states, fails on the torus), together with a local, planarity-free lemma W.)

## 3. The rigid case in the chord model (restatement asked for in the brief)

For a rigid DL state, H is a Hamiltonian cycle through v, drawn as a circle. The colour-1 edges are non-crossing chords inside and outside (the TrackH chord model), and F12 and F13 are connected figure-eights with pairings (e₀e₃)(e₁e₂) and (e₁e₃)(e₀e₄). X and Y are the two loops of F13.

π switches 1 ↔ 3 on X, and in π(c)'s frame:
- H′ = F12 Δ X = H Δ Y;
- F12′ = X ∪ Y;
- F13′ = H Δ X.

RI says it is impossible that **H Δ Y is a single cycle, H Δ X is connected, and H Δ X pairs (e₁e₄)(e₂e₃)**. Lemma 5 gives the reason: for rigid c,

  k(H Δ X) + k(H Δ Y) ≡ [p(H Δ X) = (e₁e₄)(e₂e₃)] (mod 2),

so the three conditions together would give 1 + 1 ≡ 1.

This matches the TrackH observations:
- When π(c) is DL, H Δ Y has an extra cycle.
- When π(c) is Tait-rigid, it is never DL (13,719 of 17,059 instances to N = 15).

The model counts (kHX, kHY, type) are listed in `out/chordstar.log`; every row obeys the congruence.
