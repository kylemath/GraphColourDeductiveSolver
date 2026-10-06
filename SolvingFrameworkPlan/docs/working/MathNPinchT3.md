# Math attack on (N), part 2: the pinch, the type II structure, T3

Math-team research worker, 5 October 2026. Continuation of `MathNAttack.md` §7. Exploratory, undeclared; no census or declared experiment, no one else's file edited, nothing committed or staged. Labels: [hand] = every step written out here; [computed] = exploratory, order 17 only (graphs 17:0, 17:1 of `plantri -m5 17`; only the four rigid triply locked states on 17:1 are used; plantri at `/private/tmp/planemap-next/plantri58/plantri`); [open]. Status words stay with the Navigator.

Notation as in `d1-hand-attack.md` and `MathNAttack.md`: ring word D α D β γ on u0..u4 (clockwise); P13 (u1 to u3 in [α,β]) and P14 (u1 to u4 in [α,γ]) are the unique tree paths; Z13 = x u1 P13 u3 x, Z14 = x u1 P14 u4 x; K2, K0, X, Y, X0, Y0, c′ = ν_γ c, c″ = ν_β c; pair data (comps/cyc) of T−x; m_pq = number of components of [p,q] that contain a ring vertex. H1 = "c′ is first-order locked at u0" (u0 ~ u3 in [β,D′]); H2 = "c″ is first-order locked at u2". Mirror symmetry (u0↔u2, u3↔u4, β↔γ) exchanges c′ and c″, K2 and K0, P13 and P14; every statement below for c′ has a mirror for c″.

## 0. Result

| Task | Outcome |
|---|---|
| Pinch | **Proved under one extra hypothesis (O)**: P13 and P14 meet their common vertices in the same order. Then a Y-hit of P14 produces, between the same two consecutive shared α-vertices a, a′, a Y0-hit of P13, and the lens between them lies in K2-fill ∩ K0-fill (Thm P, §3). Without (O) the argument fails at a precise step (§3.3). (O) holds in all four data states. |
| Type II pair structure of c′ | **Reduced exactly, not proved.** Gluing lemma (§2.3): the pair data of c′ are a one-parameter family in an integer τ; type II ⇔ τ = −1 ⇔ the excess relation exc(Y)−exc(X) = 1−3(|Y|−|X|) ⇔ cyc-vector (Z_Dα,Z_Dβ,Z_αγ,Z_βγ) = (1,0,0,0). So §2.5 of `MathNAttack.md` is not "conditional on type II": it is equivalent to the δ-vector. I could not show τ = −1 from H1; τ is not a local invariant (§4). |
| T3 | **Partial theorem.** (N) holds unless c′ and c″ are both in "Case I" (§5.2). Case II is a hand-proved explicit sequence of three swaps ending in a 3-coloured ring (fill). In all 4 data states exactly one of c′, c″ is Case II. Case I forces a rigid token pattern that a pure counting argument cannot close (the counting automaton has a closed locked orbit, §5.4). |

New tools that carry everything (all [hand], §2): a dual identity comps[r,s] = cyc[p,q] + m_rs; the conservation law Σ_pairs m_pq = 8 ("two extra ring connections", Lemma M); the K-fill lemma (Ω13 consists exactly of faces touching K2); the gluing lemma.

## 1. Standing facts

c rigid triply locked: six pair forests of T−x, comps (Dα,Dβ,Dγ,αβ,αγ,βγ) = (1,2,2,1,1,1). K2 ∩ ring = {u2}, K0 ∩ ring = {u0}. Orientation, ring clockwise: Ω13 (the closed disc of Z13 containing u2) lies to the **left** of P13 traversed u1→u3; Ω14⁰ (the closed disc of Z14 containing u0) lies to the **right** of P14 traversed u1→u4 [hand, by a coordinate check on a regular pentagon].

## 2. Tools

### 2.1 Dual identity and the conservation law [hand]

**Lemma DI.** For any proper 4-colouring of T−x (x of degree 5, any ring colouring) and any colour pair {p,q} with complement {r,s}:

  comps[r,s] = cyc[p,q] + m_rs.

*Proof.* H = [p,q] is a plane graph on the sphere (x ∉ H); by Euler its number of faces is E−V+comps+1 = cyc[p,q]+1. Let S = V(T)∖V(H) = (r,s-vertices) ∪ {x}. A face φ of H contains at least one vertex of S (a triangle of T with all three vertices in H would need 3 colours from {p,q}); the vertices of S inside φ induce a connected subgraph of T (walk across triangles of φ through edges not in H: the crossed edge has an endpoint in S since every p–q edge is in H, and the S-vertices of one triangle are pairwise adjacent). No edge joins S-vertices of different faces. Hence comps(T[S]) = cyc[p,q]+1. T[S] = [r,s] ∪ {x} with x adjacent to the ring vertices coloured r,s, so comps(T[S]) = comps[r,s] − m_rs + 1. ∎

**Lemma M (conservation).** Σ over the six pairs of m_pq = 8. *Proof.* Sum Lemma DI over the six pairs and use I1 (Σ(comps−cyc) = 8). ∎ Equivalently Σ_pairs (r_p+r_q−m_pq) = 15−8 = 7; the five ring edges account for 5, so exactly **two** independent non-adjacent ring connections ("tokens") exist in every proper colouring of T−x. Lemma D is the case "a token between a,b exists iff there is no separating path in the complementary pair".

[computed] Lemma DI tested on every proper colouring of T−x at every degree-5 vertex of all min-degree-5 triangulations of orders 12, 14, 15, 16, 17, all six pairs: 43 092 pair instances, 0 failures (`MathNPinchT3-scripts/idD.py`).

*Example (re-derivation of Cor 1).* In c′ the m-values are Dα 1, βγ 1, αβ 1, Dγ 2, so m_αγ + m_Dβ = 3: exactly one of "u4 ~ u1,u2 in [α,γ′]" and "u0 ~ u3 in [β,D′]" holds. So c′ is first-order locked at u0 iff u4 ≁ u1,u2 iff u0 ~ u3 in [β,D′], an equivalence, not just Cor 1's one-way form.

### 2.2 K-fill lemma [hand]

**Lemma K.** (rigid c) Let U be the union of the closed faces of T having a vertex in K2. Then ∂U = Z13, U = Ω13, and: (a) every face inside Z13 contains a vertex of K2; (b) every vertex of colour D or γ in Ω13 lies in K2 and K2 ∩ Z13 = ∅; hence K04 (the other [D,γ]-component) lies strictly outside Z13; (c) every edge of P13 lies in a face whose third vertex is in K2.

*Proof.* An edge of ∂U has a face containing some w ∈ K2 on one side and a face without K2-vertex on the other; its endpoints are adjacent to w and not in K2, so (colours D/γ would force membership in K2) they are α, β or x; so ∂U consists of α–β edges and edges from x to ring vertices of colour α/β. At x the faces in U are exactly (x,u1,u2),(x,u2,u3) (the only faces at x touching K2), so ∂U contains exactly xu1, xu3 at x. ∂U is an even subgraph (boundary of a union of faces). Delete x: E′ = ∂U∖{xu1,xu3} ⊂ [α,β] has odd-degree vertices exactly u1, u3; E′ Δ P13 is an even subgraph of a forest, hence empty; so E′ = P13 and ∂U = Z13. U is connected and contains the faces at x touching u2, so U = Ω13. (b): a D/γ vertex v of Ω13 lies on a face of U, hence is adjacent to or equal to a K2 vertex, so v ∈ K2. ∎

Mirror: with [α,γ] a forest, U0 = union of faces touching K0 satisfies ∂U0 = Z14, U0 = Ω14⁰, and every D/β vertex of Ω14⁰ lies in K0.

[computed] 4/4 states: every face of Ω13 touches K2 and every face of Ω14⁰ touches K0 (`struct.py`).

**Corollary K1 (exact degree balance).** With a13 = number of interior α,β vertices of Ω13 and p13 = |V(P13)|: Σ_{v∈K2}(deg_T v − 4) = p13 − 3 + 2 a13; likewise Σ_{v∈K0}(deg_T v − 4) = p14 − 3 + 2 a14. *Proof.* Count faces of Ω13 two ways: Euler for a disc with boundary cycle of length p13+1 and |K2|+a13 interior vertices gives F = p13 + 2|K2| + 2 a13 − 1; incidences (face, K2-vertex) give Σ deg = F + 2(|K2|−1) (K2 is a tree and a face has one or two K2 vertices). ∎ [computed] holds in all four states (e.g. K2 = {1,2}: 3 = 6−3).

**Λ.** Put Λ = faces in Ω13 ∩ Ω14⁰. A D vertex of a face of Λ lies in K2 ∩ K0 (Lemma K for both). Every γ vertex of Ω13 is in Y and interior to Ω13, every β vertex of Ω14⁰ is in Y0 and interior to Ω14⁰, hence **all faces at a vertex of Y lie in Ω13 and all faces at a vertex of Y0 lie in Ω14⁰.**

### 2.3 Gluing lemma and the pair data of c′ [hand]

c′ is c with D↔γ exchanged on K2, and by Lemma K the only D/γ vertices in Ω13 are those of K2. So c′ = c outside Z13 and c with (D,γ) transposed inside. Let B_α, B_β be the α-, β-vertices of P13 (k_α, k_β of them). Every pair graph of c′ involving exactly one of D,γ is a union of an "out" forest and an "in" forest glued along B_r:

  [α,D′] = [α,D]_out ∪ [α,γ]_in, [α,γ′] = [α,γ]_out ∪ [α,D]_in, [β,D′] = [β,D]_out ∪ [β,γ]_in, [β,γ′] = [β,γ]_out ∪ [β,D]_in.

Both pieces are subforests of forests of c. For a glued graph, comps − cyc = c_out + c_in − k. In c, [α,D]=out∪in is a tree: c^D_out + c^D_in = k_α+1; [α,γ]: c^γ_out + c^γ_in = k_α+1; [β,D] (2 components): c^D_out + c^D_in = k_β+2; [β,γ]: = k_β+1. Writing t_r = c^γ_in(r) − c^D_in(r) one gets

  δ′_αD = 1+t_α, δ′_αγ = 1−t_α, δ′_βD = 2+t_β, δ′_βγ = 1−t_β.

Inside Ω13 the components of the forests are counted by vertices minus edges: t_r = d − (e(r,Y) − e(r,X)), d = |Y|−|X|. Face counting inside Ω13 (types (D,γ,·), (D,α,β), (γ,α,β), plus the two faces at x, which contribute 1 to each of the edges u2u1, u2u3) gives 2e(α,X) = f_Dγα + f_D + 1, 2e(β,X) = f_Dγβ + f_D + 1, 2e(α,Y) = f_Dγα + f_γ, 2e(β,Y) = f_Dγβ + f_γ, where f_D, f_γ are the numbers of faces (D,α,β), (γ,α,β). Hence **t_α = t_β =: τ = d − (f_γ − f_D − 1)/2**, and from degrees (Σ_Y deg − e(Y,X), Σ_X deg − e(X,Y) − 1, e(X,Y) = |K2|−1):

  f_γ − f_D = Σ_Y deg − Σ_X deg + 2, so **2τ = −1 − 3d − (exc(Y) − exc(X))**.

**Theorem G.** (rigid c) the pair data of c′ satisfy δ′_αD = 1+τ, δ′_αγ = 1−τ, δ′_βD = 2+τ, δ′_βγ = 1−τ, δ′_αβ = 1, δ′_Dγ = 2, with τ as above. Combined with Lemma DI (for c′ under H1: m′ = Dα 1, Dβ 1, Dγ 2, αβ 1, αγ 2, βγ 1):

  Z_βγ − Z_Dα = τ,  Z_βD − Z_αγ = −1 − τ,  and C_βγ = Z_Dα+1, C_Dα = Z_βγ+1, C_αγ = Z_Dβ+2, C_Dβ = Z_αγ+1

(Z = cyc, C = comps of c′). In particular **type II ⇔ τ = −1 and Z_αγ = Z_Dβ = Z_βγ = 0; and the δ-vector of type II ⇔ τ = −1 ⇔ exc(Y)−exc(X) = 1−3(|Y|−|X|)**. [computed] (struct.py) in all four states f_D, f_γ = (1,4) or (2,5), d = 0, τ = −1, and the computed pair data of c′ and c″ equal the type II vector exactly.

### 2.4 First-order lock gives a W-path, a crossing, and a Y–Y0 edge [hand]

H1 gives a path W in [β,D′] from u0 to u3, i.e. in c: a path through V_β ∪ (V_D∖X) ∪ Y.
- *Crossing (re-proof of Prop N1).* Z14 separates u0 from u3 (ring order), W avoids x, so W meets P14; W's colours are β, D, Y(γ) and P14's are α, γ: W ∩ P14 ⊂ Y, hence P14 ∩ Y ≠ ∅. Mirror: H2 gives P13 ∩ Y0 ≠ ∅.
- **Lemma YY.** If H1 (or H2) holds there is an edge g–h with g ∈ Y, h ∈ Y0, and both faces on it lie in Λ. *Proof.* Let v be the last vertex of the initial run of W inside K0 (u0 ∈ K0, u3 ∉ K0), w its successor. w is adjacent to v ∈ K0, so w ∉ V_β ∪ (V_D∖X) (it would be in K0); thus w ∈ Y. The edge vw is in [β,D′] with w coloured D′, so v is β: v ∈ Y0. Faces on gh lie in Ω13 (g interior) and Ω14⁰ (h interior). ∎ The third vertices of those two faces are α-vertices, or D-vertices of X ∩ X0.

## 3. The pinch

### 3.1 Excursion lemma [hand, no extra hypothesis]

Let g ∈ P14 ∩ Y (exists under H1). g lies strictly inside Ω13, u1 ∈ Z13, u4 ∉ Ω13. Let a, a′ be the last vertex of P14 before g and the first after g that lie on P13; they are α-vertices (colours α,γ vs α,β), a ≠ a′. The arc E14 = P14[a,a′] has all interior vertices strictly inside Ω13 (it cannot leave without meeting Z13, and x ∉ P14), it contains g, and no vertex of E14 other than a, a′ lies on P13. Let Q13 = P13[a,a′] and Δ ⊂ Ω13 the closed disc bounded by the simple cycle E14 ∪ Q13 (x ∉ Δ because the faces at x are not inside Δ; so u2 ∉ Δ).

### 3.2 Theorem P (the pinch under (O)) [hand]

**(O).** The common vertices S = V(P13) ∩ V(P14) are met in the same order by P13 and P14 (π13(s) < π13(s′) ⇔ π14(s) < π14(s′)).

**Theorem P.** Assume H1 and (O). With g, a, a′, E14, Q13, Δ as in 3.1:
1. a, a′ are consecutive in S for both orders, and P14 ∩ Δ = E14;
2. Δ ⊂ Ω14⁰, hence all faces of Δ are in Λ;
3. every β-vertex of Q13 lies in Y0, and there is at least one. So **P13 ∩ Y0 ≠ ∅ already follows from P14 ∩ Y ≠ ∅**, and the excursion of P13 through K0 is between the same a, a′: this is the pinch;
4. if moreover X ∩ X0 = ∅, every face of Δ is an (α,β,γ)-triangle, every βγ-edge of Δ has both faces in Δ, and Δ is tiled by rhombi (α,β,α′,γ); Δ is a single rhombus iff Δ has no interior vertex and |E14| = |Q13| = 2.

*Proof.* (1) π14(a) < π14(a′) by construction, so (O) gives π13(a) < π13(a′). A shared vertex s with π13(a) < π13(s) < π13(a′) would, by (O), lie strictly between a and a′ on P14, but E14's interior has no shared vertex; so a, a′ are consecutive in both. Suppose P14[u1,a] meets the open disc Δ. u1 ∉ int Δ; entering int Δ requires crossing ∂Δ = E14 ∪ Q13 at a vertex; E14's vertices other than a are not on P14[u1,a]; so it crosses at a shared vertex s ∈ Q13 with π13(a) < π13(s), π14(s) < π14(a), contradicting (O). (If u1 ∈ Q13 then u1 = a, nothing to cross.) Symmetrically for P14[a′,u4] (ends outside Ω13 ⊃ Δ; leaves through a shared s ∈ Q13 with π13(s) < π13(a′), π14(s) > π14(a′)). (2) Orient E14 and Q13 forward (a→a′); by §1 Δ ⊂ Ω13 lies on the left of Q13; Δ is on a fixed side of the closed curve E14·Q13⁻¹, namely the right, so Δ is on the right of E14, which is the Ω14⁰ side. Z14 has no point in int Δ (P14 ∩ Δ = E14, x-edges are not inside), so int Δ lies in Ω14⁰. (3) A β-vertex of Q13 is in Ω14⁰, not on Z14 (no β there), so interior to Ω14⁰, so in K0 (Lemma K mirror); Q13 is an α…α path with ≥ 1 β. (4) a D-vertex of a face of Λ is in X ∩ X0 (§2.2); a βγ edge has its β-end interior to Ω14⁰ and γ-end interior to Ω13, so both faces lie in Λ. ∎

[computed] (O) holds in all four states (shared sequences u1, a, a′ equal in both orders); Λ is exactly two faces (a rhombus) in each; X ∩ X0 = ∅; a single Y–Y0 edge (`struct.py`, `pinch.py`).

### 3.3 Where the pinch is not proved [open]

- (O) is not proved. An adjacent inversion of S gives a P14-arc B between consecutive shared vertices p, q with π13(q) < π13(p); Lemma K and the orientation facts only say that B's u0-side is the complement of the lens, they do not contradict anything: no counting identity of §2 distinguishes the two cases.
- Without (O), step (1) fails: P14 can enter Δ through a shared vertex between a and a′.
- Without X ∩ X0 = ∅ the faces of Λ are not forced to be (α,β,γ) and no rhombus tiling follows (a D-vertex in K2 ∩ K0 is not excluded by any identity I found).
- The pinch with a single rhombus (the data) needs |E14| = |Q13| = 2 and an interior-free Δ. For general n the interior vertices of Δ have even degree ≥ 6 when X ∩ X0 = ∅ (all their faces are (α,β,γ)), i.e. each costs excess; at n = 17 the excess budget (1,2,1,1) leaves little room, so the interior-free statement is plausible but not derived.

## 4. Type II structure of c′

What §2.3 settles: the pair data of c′ are determined by the single integer τ = (−1 − 3d − (exc(Y)−exc(X)))/2, with the cycle numbers tied by Z_βγ − Z_Dα = τ and Z_βD − Z_αγ = −1−τ. What is not settled: τ = −1.

Failed attempts, with the failure point:
1. *Vanishing of Z_αγ, Z_Dβ, Z_βγ by gluing.* A cycle of [α,γ′] = [α,γ]_out ∪ [α,D]_in cannot be entirely out or in (a cycle of [α,D] or [α,γ]), so it passes through ≥ 2 boundary α-vertices of P13 joined inside by an [α,D]-path through X and outside by an [α,γ]-path through γ∖Y. Planarity and Lemma DI turn this into a ring-free component of [β,D′] enclosed by it; no contradiction with H1, Lemma K, or any count, since both connecting paths are legal in c.
2. *τ as a local invariant.* τ depends only on degrees inside Ω13 and is locally unconstrained: a disc Ω13 consisting of the star of a single degree-5 vertex u2 (K2 = {u2}, d = −1, ex = 0) has τ = 1. It is excluded only because Y = ∅ contradicts H1. So H1 must be used in a form stronger than Y ≠ ∅; Lemma YY (a Y–Y0 edge) is the strongest I extracted, and it does not fix τ.
3. *Using the other fans.* c′ stays in the G-classes of the fans u1, u3, so those chains are first-order true in all members of the class, but for c′ itself they are automatic (adjacency), and the members reached by K-swaps again involve only adjacent-ring conditions. No new equation.

[computed] consequence of Theorem G in the data: c′ and c″ equal the type II vector in all four states; τ = −1.

## 5. T3

### 5.1 Token calculus [hand]

By Lemma M every colouring has exactly two non-adjacent ring connections. For a fan with apex u0 (colour D), chain {D,k} holds iff the component of u0 in [D,k] contains a ring k-vertex (Prop 1): automatic if k is the colour of u1 or u4, and a token (u0 ~ u_j in [D,c(u_j)], j = 2 or 3) otherwise. A locked class therefore forces, for every member, its needed tokens, and then Lemma M forces **all other** non-adjacent ring connections to be absent. A member with a missing colour on the ring is separable at once (x takes the missing colour).

### 5.2 The sequence c′ → c1 → c2 and Theorem T3-II [hand]

Assume c′ is locked at u0 (the whole G_0-class, x coloured D). H1 gives u4 ≁ u1,u2 in [α,γ′] (§2.1). Let Q4 be the [α,γ′]-component of u4 and c1 the swap of Q4 (a G_0 swap: x has colour D, not in the pair). Ring of c1: D α γ β α.

**Step 1.** m-values of c1: Dα 1, Dβ 1 (same subgraph as in c′), αγ 2 (same subgraph), βγ 1; Lemma M gives m_Dγ + m_αβ = 3. The chain {D,γ} of c1 needs u0 ~ u2 in [D,γ]_1 (m_Dγ = 1) and {D,β} needs u0 ~ u3 (holds). If m_Dγ = 2, c1 is separable after one more swap. So locked ⇒ the two tokens of c1 are exactly {u0 ~ u2 in [D,γ]_1, u0 ~ u3 in [D,β]_1} and **u1 ≁ u3 in [α,β]_1** (m_αβ = 2). [computed] in all four states c1 has the rigid pair structure (all six pairs forests, comps (Dα,Dβ,Dγ,αβ,αγ,βγ) = (1,1,1,2,2,1), doubled colour α at u1,u4, apex u0 middle).

**Step 2.** Let E34 be the [α,β]_1-component of u3,u4 (≠ the component of u1) and c2 the swap of E34 (a G_0 swap). Ring of c2: D α γ α β; [D,γ]_2 is the same graph as [D,γ]_1, so u0 ~ u2 persists and all chains of c2 hold at first order. m-values: Dγ 1, Dβ 1, αβ 2, αγ 1, so m_Dα + m_βγ = 3.

- **Case II** (m_βγ = 2, equivalently u3 ~ u0 or u1 in [D,α]_2): u2 ≁ u4 in [β,γ]_2. Swap the [β,γ]_2-component of u4 (a G_0 swap, the pair avoids D): u4 becomes γ, ring D α γ α γ is 3-coloured, x takes β. So **c′ is separable at u0**, after the swaps Q4, E34, [β,γ]-component, then the x-swap.
- **Case I** (m_βγ = 1, m_Dα = 2): u2 ~ u4 in [β,γ]_2 and u3 ≁ u0,u1 in [D,α]_2.

**Theorem T3-II.** (rigid c) If c′ is locked at u0, then c′ is in Case I. Mirror: if c″ is locked at u2, then c″ is in Case I. Hence **(N) holds unless both c′ and c″ are in Case I**; in particular (N) holds whenever one neighbour is in Case II. [hand]

[computed] Case II/I by state (`caseI.py`): x=5: c′ II, c″ I | c′ I, c″ II; x=15: c′ II, c″ I | c′ I, c″ II. So in all 4 states exactly one neighbour is in Case II. In the Case I neighbours the unlock is: swap the [β,γ]_2 component through u2,u4 (c3, ring D α β α γ) and the chain {D,β} is broken (a chain-broken state, not a 3-coloured ring).

### 5.3 What Case I forces [hand]

Swap the [β,γ]_2-component R ∋ u2,u4 of Case I: c3 has ring D α β α γ; [D,α]_3 = [D,α]_2 (u3 ≁ u0,u1), [β,γ]_3 ≅ [β,γ]_2 (u2 ~ u4). m-values: Dα 2, βγ 1, αβ 1, Dγ 1, so m_Dβ + m_αγ = 3. If m_Dβ = 2 the chain {D,β} is broken (separable). If locked: tokens = {u0 ~ u2 in [D,β]_3, u2 ~ u4 in [β,γ]_3} and u1 ≁ u3,u4 in [α,γ]_3. [computed] in the one Case I neighbour I checked (x=5, second state, c′) the first branch (m_Dβ = 2) occurs: the chain {D,β} is broken at c3 (D-free distance 3 from c′); the D-free class data of §5.4 show the same distance-3 break for all 8 neighbours.

### 5.4 Why counting does not finish Case I [hand]

Continue in the locked branch: swap the [α,γ]_3-component of u3,u4 (not u1's) to get c4 with ring D α β γ α. Its m-values: Dα 1, βγ 1, αγ 2 (same subgraph as c3), Dβ 1 (same subgraph as c3, token), so m_Dγ + m_αβ = 3; locked needs m_Dγ = 1, then m_αβ = 2. So c4's locked token pattern (ring D α β γ α; tokens u0 ~ u2 in [D,β], u0 ~ u3 in [D,γ]; u4 ≁ u1,u2 in [α,β]) is c1's pattern with β and γ renamed. **The token automaton c1 → c2 → c3 → c4 ≅ c1 has a closed locked orbit.** Hence Lemma M, Lemma DI, Jordan splits and the first-order chain conditions cannot decide Case I: each step leaves exactly one binary choice (the dichotomy), and nothing in the counting excludes taking the locked branch at every step. A proof of Case I ⇒ separable needs geometric input that kills one token at c3 or later (e.g. showing that R separates u1 from u3 in [α,γ]_3, or that E34 and the component of u1 are forced to merge). [open]

[computed] The D-free class of c′ (G_0 swaps of pairs avoiding the colour of D′) is the same abstract graph in all 8 cases (c′ and c″ of the four states): 10 colourings (up to renaming), 11 edges, two hexagons sharing an edge (nodes 0–5 and 4–5–7–9–8–6), distance profile from c′: 0,1,1,2,2,3,3,4,4,5; every colouring with a broken chain or 3-coloured ring lies in the second hexagon, nearest at distance 3 (`hexd.py`, `hexe.py`). The shortest unlock found by BFS in `MathNAttack.md` uses only D-free swaps in the nearest cases; it is the path c′ → c1 → c2 → (node 6). In the BFS the first two swaps are the same up to renaming (swapping either of two components), consistent with the 2-regular behaviour of the first hexagon.

## 6. What this changes in `MathNAttack.md` §7

1. (Pinch) Reduced to (O), plus nothing else for the conclusion "Y-hit ⇒ Y0-hit between the same shared vertices". Prop N1 now has a corollary: under (O), one hit implies the other.
2. (Type II) §2.5 of the earlier note is equivalent to the δ-vector of type II (Theorem G); the cyclic data are tied by τ.
3. (T3) (N) ⇐ "c′ or c″ in Case II" is proved; Case I is the exact remaining statement (§5.4). The earlier "T3" list is replaced by the three explicit swaps of §5.2 in Case II and the c3 swap of §5.3 in Case I (where the break is data, not theorem).

## 7. Summary of where each attempt stops

- Pinch: (O) (§3.3). The counting identities do not see the order of shared vertices.
- Type II: τ = −1 (§4). Locally free; H1 gives Y ≠ ∅ and a Y–Y0 edge, which do not fix τ.
- T3, Case I: closed locked orbit of the token automaton (§5.4). A proof must show a geometric reason that, at c3 or later, the token u0 ~ u2 (or u2 ~ u4) cannot survive.
- Conjecture [open, data only]: for a rigid triply locked state exactly one of c′, c″ is in Case II (4 of 4). A proof that **at least one** is in Case II would prove (N). Possible handle: both Case I conditions are statements about [β,γ] and [D,α] components in the same T−x; a Jordan argument with P13 and P14 together is the natural place to look.

Files: this page; `docs/working/MathNPinchT3-scripts/` (idD.py, struct.py, pinch.py, hexd.py, hexe.py, caseI.py; they import `nlab` from `docs/working/MathNAttack-scripts/`, run with `PYTHONPATH=../MathNAttack-scripts` and the plantri path edited at the top). Nothing staged or committed.
