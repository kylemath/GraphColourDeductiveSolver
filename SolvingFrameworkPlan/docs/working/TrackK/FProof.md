# Conjecture F (mod-4 chain-count formula): proof [hand, unreviewed; every step data-checked]

Track K, 8 Oct 2026. Notation follows `TrackC/README.md` §6.4, `TrackI/RigidIsolation.md` and `TrackF/LockParity.md`. Data: `scripts/tk_tables.py` (exhaustive finite tables) and `scripts/tk_check.py` (logs `scripts/tk_check.log`, `scripts/tk_check_x6.log`).

**Result.** F is **true as stated** on the sphere, and the proof is short:
1. The no-hole case F0 is a mod-4 repackaging of **Tutte's parity theorem** for 4-colourings of plane triangulations (as given in "The Last Temptation of William T. Tutte", arXiv:1912.07205, Thm 1/Thm 3), together with Fisk's degree.
2. The hole case reduces to F0 by **filling the pentagon with the two diagonals x₁x₃, x₁x₄** from the μ-vertex. The colouring stays proper. The two new edges are exactly the two lock edges, so they merge chains iff the locks fail. That merging is where the term 2(L1 + L2) comes from. The three new faces all have the same Tait orientation, and that orientation is `hand`.

Theorem D, Lemma 2 and the Jordan arguments at h are **not** used. The only planar input is Proposition 1(b) below, applied to one map. On the torus exactly that step changes, and the failure of F is then predicted exactly (§5).

## 0. Setting and conventions

- A **sphere triangulation (map sense)** is a loopless multigraph cellularly embedded in the oriented S², with every face bounded by 3 distinct vertices.
  - Parallel edges are allowed (needed for T° in §3).
  - Each face is a triangle, and no edge has the same face on both sides, because a 3-walk on 3 distinct vertices has 3 distinct edges.
- n = number of vertices. Euler's formula gives F = 2n − 4 faces and E = 3n − 6 edges.
- c is a proper 4-colouring with colours in ℤ₂² = {0, 1, 2, 3} (xor).
- For an oriented face (u, v, w), its **Tait triple** is (c u ⊕ c v, c v ⊕ c w, c w ⊕ c u), and the face is **cw** if the triple is a cyclic shift of (1, 2, 3). This is exactly `cwcount` in `tc_mod4.py`.
- For colours X ≠ Y:
  - p(X,Y) is the number of components of the subgraph induced on c⁻¹{X,Y}, the XY-chains;
  - e(X,Y) is the number of edges coloured {X,Y}, counted with multiplicity;
  - |X| = |c⁻¹(X)|.
- N = Σ over the six pairs of p. The three partitions are P_i = {XY | ZW}.

**Fisk's degree.** Fix the orientation of the tetrahedron Δ³ on {0,1,2,3} in which the oriented triangle (a, b, c) is *positive* iff the permutation (d, a, b, c) is even, where d is the fourth colour. For a colour triangle t and an oriented face f with colour set t, put σ(f) = ±1 according to whether f's colour triple is positive. Let d_t = Σ_{f coloured t} σ(f).

## 1. Three finite facts (exhaustive: `tk_tables.py`, 0 mismatches)

- **(T1)** A face is cw ⇔ its colour triple is positive. (24 ordered triples.)
- **(T2)** For distinct α, μ, A, B, `hand` = [(α⊕μ, α⊕A, α⊕B) is a cyclic shift of (1,2,3)] equals the cw indicator of each of the oriented triples (μ, α, A), (μ, A, B), (B, α, μ). (24 role assignments × 3 faces.)
- **(T3)** Across an edge coloured xy, the faces read (x, y, z) and (y, x, w), and σ is equal on both ⇔ z ≠ w. (48 cases.)

## 2. The no-hole case F0

**Lemma 0 (degree; any closed oriented triangulated surface).** d_t is the same number d for all four colour triangles t. Moreover, cw − ccw = 4d and cw = F/2 + 2d.

*Proof.*
- Let t = xyz and t′ = xyw share the edge xy of Δ³. Every face coloured t or t′ contains exactly one edge coloured xy.
- So d_t + (−d_{t′}) can be split over the xy-coloured edges e. Let f, f′ be the two faces at e; they read e as (x, y) and (y, x) respectively.
  - If both have third colour z, T3 gives σ(f) = −σ(f′), so they cancel in d_t.
  - If the third colours are z and w, T3 gives σ(f) = σ(f′), so they contribute equally to d_t and d_{t′}.
  - (Both third colours w is symmetric.)
- Hence d_t = d_{t′}. The four triangles of Δ³ are connected through shared edges, so all d_t are equal.
- By T1, cw − ccw = Σ_f σ(f) = Σ_t d_t = 4d, and cw + ccw = F. ∎

**Lemma 0′.** d ≡ deg(A) := Σ_{c(a)=A} deg a (mod 2), for any colour A.

*Proof.* Every face has at most one A-vertex. The faces with an A-vertex are counted by Σ_{c(a)=A} (number of face corners at a) = deg(A). The others are exactly the faces coloured t = (other three colours). So t-faces = F − deg(A). Also d = d_t ≡ #t-faces (mod 2), and F is even. ∎

**Proposition 1 (sphere).** For each partition P_i = {XY | ZW}, let k_i be the number of cycles of the Tait 2-factor S_i. S_i consists of the dual edges of T-edges whose ends lie in different classes of P_i; every face has colours 2 + 1 across P_i, so S_i is 2-regular in the cubic dual. Then:
- (a) 2 p(X,Y) − k_i = |X| + |Y| − e(X,Y); in particular k_i ≡ |X| + |Y| + e(X,Y) (mod 2);
- (b) p(X,Y) + p(Z,W) = k_i + 1.

*Proof.*
- As in `RigidIsolation.md` Lemma 1 (the region/chain bijection holds on any surface), the regions of S² − S_i correspond bijectively to the XY- and ZW-chains. The region R_Q of a chain Q is the union of the open dual faces of Q's vertices and the open dual edges of Q's edges. So R_Q deformation retracts onto the embedded graph Q, and χ(R_Q) = |V(Q)| − |E(Q)|.
- **Jordan input.** S_i is a disjoint union of k_i simple closed curves on S². By Jordan–Schoenflies and induction (exactly the region-tree argument of review fix G1), they cut S² into k_i + 1 regions. Each region R is S² minus b_R disjoint closed discs, where b_R is the number of curves in its frontier, so χ(R) = 2 − b_R. This gives (b).
- Every curve has an XY-region on one side and a ZW-region on the other, because an S_i-edge separates two classes of P_i. So Σ_{Q an XY-chain} b_Q = k_i.
- Summing χ over XY-chains: 2 p(X,Y) − k_i = Σ_Q (|V(Q)| − |E(Q)|) = |X| + |Y| − e(X,Y). This is (a). ∎

(a) − (b) is Tutte's identity p(X,Y) − p(Z,W) = |X| + |Y| − e(X,Y) − 1.

**Theorem F0 (sphere).** N ≡ n + 1 + d (mod 2); equivalently 2N ≡ cw + n (mod 4).

*Proof.*
- By (b), N = Σ_i (k_i + 1) = 3 + Σ_i k_i.
- Fix a colour A and write each partition as {AX | ··}, X ≠ A. By (a), Σ_i k_i ≡ Σ_{X≠A} (|A| + |X| + e(A,X)) = 3|A| + (n − |A|) + deg(A) ≡ n + deg(A).
- So N ≡ n + 1 + deg(A) ≡ n + 1 + d, by Lemma 0′.
- By Lemma 0, cw = F/2 + 2d = n − 2 + 2d. So cw + n = 2(n − 1 + d) ≡ 2(n + 1 + d) ≡ 2N (mod 4). ∎

## 3. The hole: Conjecture F

**Setting.** T is a triangulated sphere, h has degree 5, and the link is x₀ … x₄ in the rotation order at h. That is, the faces at h are (h, x_t, x_{t+1}) in the orientation used for cw; this is `oriented_link` in `tc_mod4.py`. c is unfilled with frame j, and indices are relative to j, so the colours are (α, μ, α, A, B). The locks are L1 = [x₃ ∈ K_{μA}(x₁)] and L2 = [x₄ ∈ K_{μB}(x₁)] in T − h (LockParity §1). N = N(T − h), and cw counts the faces avoiding h.

**The filled map T°.**
- Delete h. The star of h becomes a pentagonal face with boundary x₀x₁x₂x₃x₄, oriented as the link.
- Add the diagonals x₁x₃ and x₁x₄ inside it, as new edges even if T already has an edge x₁x₃ or x₁x₄ (then T° has a parallel pair).
- T° is a sphere triangulation in the sense of §0 with n − 1 vertices. Its new faces (x₁, x₂, x₃), (x₁, x₃, x₄) and (x₄, x₀, x₁) carry the orientation of the pentagon.
- The colours on the new edges are μ–A and μ–B, so c is proper on T°.

**Step 1 (chains).** Only the μA- and μB-subgraphs gain an edge. Adding an edge between u and w lowers the component count by one iff u and w were in different components. So

  N(T − h) = N(T°) + (1 − L1) + (1 − L2).

**Step 2 (faces).** T° has the faces of T that avoid h, plus three new faces coloured (μ, α, A), (μ, A, B) and (B, α, μ). By T2 each new face is cw iff `hand` = 1, so

  cw(T°) = cw + 3·hand.

**Step 3.** Apply F0 to T°: 2N(T°) ≡ cw(T°) + (n − 1) (mod 4). Then:

  2N = 2N(T°) + 4 − 2L1 − 2L2 ≡ cw + 3·hand + (n − 1) + 2(L1 + L2) ≡ cw + (n − 1) − hand + 2(L1 + L2)  (mod 4),

using −2L ≡ 2L and 3 ≡ −1 (mod 4). This is **F**. ∎

**Remarks.**
- In degree language, F says **N + L1 + L2 ≡ n + d(c on T°) (mod 2)**. Here d(c on T°) is Fisk's degree of the filled colouring; note `hand` = 1 iff the pentagon maps positively, by T1–T2.
- Any proper triangulation of the pentagon would do; the fan from x₁ is the only one whose diagonals are the lock edges. That is why L1 and L2 appear.
- With Track C's Lemma W (Δcw ≡ 2 m_h(K) mod 4; a sketch, unreviewed), F gives Theorem 6 and Remark 7 by the bookkeeping of `TrackC/README.md` §6.4. So **Route Q now needs W reviewed, nothing else**. This is an independent second proof of Theorem 6 that avoids Lemma R, the disc structure and Theorem D.
- Lean shape: Proposition 1 in primal form is Tutte's identity (faces of T[X∪Y] ↔ ZW-chains). Two ways to use it:
  - allow parallel edges in T° (the map library must then accept a multigraph map), or
  - avoid T° by adding the two diagonals only at the level of the pair graphs (Step 1 is purely graph-theoretic) and proving Tutte's identity for T° directly. I have not worked out the second route.

## 4. Data (every step separately; `tk_check.py`)

Steps checked per state:

| step | claim |
|---|---|
| S1 | N(T − h) = N(T°) + 2 − L1 − L2 |
| S2 | cw(T°) = cw + 3·hand |
| S3 | k_i ≡ \|X\| + \|Y\| + e(X,Y), per partition |
| S4 | r_i := p(X,Y) + p(Z,W) = k_i + 1 |
| S5 | the four d_t are equal, cw − ccw = 4d, deg(A) ≡ d |
| S6 | F0 on T° |
| S7 | F (residue from `tc_mod4.residue`) |
| S8 | torus prediction of §5 |

Results with the default scale (`tk_check.log`). The larger run is in `tk_check_x6.log`, recorded in README.

| family | states | parallel-diagonal states | failures |
|---|---|---|---|
| no hole, random spheres n = 8–34 | 2,400 colourings | — | 0 (F0, N ≡ n+1+d, S3–S5) |
| hole, spheres min deg 5 | 12,078 | 272 | 0 in S1–S7 |
| hole, spheres min deg 3 | 11,569 | 5,837 | 0 in S1–S7 |
| hole, Census29 frame class 22–32 | 6,003 | 0 | 0 in S1–S7 |
| torus (no hole / hole) | 360 / 2,192 | — / 1,345 | S1–S3, S5: 0; S8: 0; F itself fails on 248 / 1,137 |

## 5. Why F fails on the torus

Everything except Proposition 1(b) survives on any closed orientable surface of genus g:
- the finite tables;
- Lemma 0 (local);
- Lemma 0′ (F = 2n − 4 + 4g is even);
- Proposition 1(a) mod 2;
- Steps 1–2 of §3 (local).

For 1(a): a region R is a genus-g_R surface with b_R boundary curves, so χ(R) = 2 − 2g_R − b_R, and 2p(X,Y) − 2Σ g_R − k_i = |X| + |Y| − e(X,Y). Hence **Σ_i k_i ≡ n + d on every orientable surface.**

What breaks is the region count. Σ_R χ(R) = 2 − 2g gives r_i = k_i + 1 − g + G_i, with G_i = Σ_R g_R. On the torus, G_i ∈ {0, 1}: G_i = 1 iff one region of S_i carries the handle, which I expect to mean that every curve of S_i is contractible (not checked separately). Redoing §2–3:

  2N − cw − (n − 1) + hand − 2(L1 + L2) ≡ 2G  (mod 4),  G = G₁ + G₂ + G₃ computed in T°,

for every genus. On the sphere G = 0, which is F. On the torus, F holds iff an even number of the three Tait 2-factors are "all contractible". Data: residue = 2G on all 2,192 hole states and 360 no-hole colourings (S8, 0 failures), with G = 0 / 1 / 2 on 340 / 1,137 / 715 hole states. That accounts for the observed ~50% failure rate.

So the planarity in F, and through F + W in Theorem 6, is exactly this: **each of the three Tait 2-factors cuts the surface into k_i + 1 planar regions.** For any one 2-factor, that is Euler plus Jordan.

## 6. Literature

- Tutte's parity theorem (Thm 1 of arXiv:1912.07205) is J_A(f) = 2|A| − deg(A) + n − 3, where J_A is the signed chain count Σ_{X≠A} p(A,X) − Σ p(other pairs).
- The paper also records deg(f) ≡ deg(A) (mod 2), via Fisk's view of a colouring as a simplicial map to ∂Δ³.
- J_A ≡ N (mod 2), so F0 mod 2 is that theorem; the mod-4 form adds Lemma 0.
- I found no prior statement of the hole version F; the fill-in reduction appears to be new here.
