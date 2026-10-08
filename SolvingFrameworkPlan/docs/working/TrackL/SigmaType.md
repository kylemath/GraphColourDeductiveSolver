# The σ-type lemma: proof [hand, unreviewed; every step data-checked]

Track L, 8 Oct 2026. Notation follows `TrackJ/README.md` §1.1, `TrackI/RigidIsolation.md` and `TrackF/LockParity.md`. Data: `tl_sigma_check.py`, `tl_sigma_general.py` (logs in `out/`).

## 0. Statement

T is a triangulated sphere with n vertices, h a vertex of degree 5 with link x₀ … x₄, and a *state* is a proper 4-colouring of T − h up to renaming. At an unfilled state with frame j the link colours are (α, μ, α, A, B) at x_j … x_{j+4}. Pair graphs, in role order: αμ, AB, αA, μB, αB, μA. Partitions: P1 = {αμ | AB}, P2 = {αA | μB}, P3 = {αB | μA}. #XY is the number of components (chains) of the pair graph G[X,Y] of T − h. *Rigid* = DL with counts (1,1,2,1,2,1). π = swap of K_{αA}(x_{j+2}).

> **Lemma S (σ-type lemma).** Let u be a rigid state and c = π(u). Suppose (#α_cA_c, #μ_cB_c) = (2, 1) and P1(c) has exactly 3 chains. Then c has exactly 2 α_cμ_c-chains and exactly 1 A_cB_c-chain, and that A_cB_c-chain contains a cycle. (Roles are taken in c's own frame.)
>
> If c is DL, the first hypothesis is the same as "P2(c) has 3 chains", because #α_cA_c ≥ 2 by Theorem D (Lock2(c) ⇔ x′₀ ∉ K_{α_cA_c}(x′₂)).

> **Corollary S1.** At every in-shape state c (DL, N = 9, π(c) and π⁻¹(c) rigid), the extra chain Z is an α_cμ_c-chain. So on the sphere the Z-matching of Theorem J5 is σ.
>
> *Proof.* By Corollary J3, (#αA, #μB)(c) = (#αB, #μA)(π c) = (2, 1) and the extra chain is in P1, so P1(c) has 3 chains. Apply Lemma S with u = π⁻¹(c). By Lemma J1 the αμ_c link component is one of the two α_cμ_c-chains; the other is Z. ∎

> **Corollary S2 (one rigid neighbour suffices).** If c is DL with N(c) = 9 and π⁻¹(c) is rigid, and the extra chain is not in P2, then it is an α_cμ_c-chain. The mirror statement (π(c) rigid, extra chain not in P3) holds by the mirror symmetry x_t ↔ x_{2−t}, A ↔ B, which fixes α and μ.
>
> *Proof.* P3(c) = P2(π⁻¹c) has 3 chains (Lemma J2), so the extra chain is in P1, P2(c) has 3 chains, and Lemma S applies (c is DL). ∎

**Tait form.** Write H = H₀ ∪ C′ for the {2,3}-factor of c. Regions of S² − H correspond to P1-chains (TrackI Lemma 1). The side of H₀ containing e₃ holds the corners x₃, x₄, so it is the AB link chain. Lemma S says that this AB chain is the unicyclic one, i.e. the annulus between H₀ and C′. Equivalently: **the free {2,3}-cycle C′ lies on the e₃ side of H₀.** This is the form asked for in `TrackJ/README.md` §4.

## 1. Two ingredients

For colours X ≠ Y write χ(XY) := |X| + |Y| − e(X,Y). Here |X| counts the X-coloured vertices of T − h, and e(X,Y) counts the edges of T − h joining an X-vertex to a Y-vertex. So χ(XY) = #XY − β(XY), where β is the cycle rank of the pair graph. A connected graph has χ ≤ 1, with equality iff it is a tree.

**Lemma E (Euler balance; sphere; this is TrackH's H3).** At every unfilled state,

  Σ_{P1} χ = 2,  Σ_{P2} χ = 3,  Σ_{P3} χ = 3,

where Σ_{P} χ = χ(XY) + χ(ZW) for P = {XY | ZW}.

*Proof.*
- T − h has n − 1 vertices and (3n − 6) − 5 = 3n − 11 edges (Euler).
- Call an edge of T − h *crossing* for P if its ends lie in different classes of P. Then Σ_P χ = (n − 1) − (3n − 11) + #crossing.
- Every face of T has three distinct colours, so exactly two of its three edges cross P (two colours fall in one class, one in the other).
- T has 2n − 4 faces. The 2n − 9 faces avoiding h give 2(2n − 9) = 2·#(crossing non-link edges) + #(crossing link edges). This holds because a link edge x_t x_{t+1} lies in one face avoiding h, and every other edge of T − h lies in two such faces.
- With the link colours (α, μ, α, A, B), the crossing link edges are:

  | partition | crossing link edges | count | #crossing | Σχ |
  |---|---|---|---|---|
  | P1 | x₂x₃, x₄x₀ | 2 | 2n − 8 | 2 |
  | P2 | x₀x₁, x₁x₂, x₃x₄, x₄x₀ | 4 | 2n − 7 | 3 |
  | P3 | x₀x₁, x₁x₂, x₂x₃, x₃x₄ | 4 | 2n − 7 | 3 |

  ∎

Consequences used below (each chain has χ ≤ 1):
- If a partition has its minimal number of chains (2 for P1, 3 for P2 and P3), all its chains are trees.
- If P1 has 3 chains, their χ values are (1, 1, 0): two trees and one unicyclic chain.

  In particular, **rigid ⇒ all six pair graphs are trees/forests** (TrackJ §1.4).
- On a closed surface of Euler characteristic χ_S the same count gives Σ_{P1} χ = χ_S, and χ_S + 1 for P2 and P3, which is the general form of H3. On RP² a rigid state therefore has exactly one unicyclic chain in each partition.

**Lemma St (star identity; any graph).** Let p, q, r be three distinct colours, and let c′ be obtained from c by swapping p ↔ q on a component of G[p,q]. Then

  χ_{c′}(rp) + χ_{c′}(rq) = χ_c(rp) + χ_c(rq).

*Proof.* χ(rp) + χ(rq) = 2|r| + |p ∪ q| − e(r, p ∪ q). The swap fixes the r-vertices and the set of vertices coloured p or q. ∎

## 2. Proof of Lemma S

1. **The swap.** π(u) swaps α ↔ A (u's roles) on K = K_{αA}(x_{j+2}). By Lemma H0 / J2, the roles of c are (α_c, μ_c, A_c, B_c) = (α, B, μ, A) in u's colour names. Hence {μ, α} = α_cA_c (a P2 pair of c) and {μ, A} = A_cB_c (a P1 pair of c).
2. **Star identity** (r = μ, {p,q} = {α, A}):

   χ_c(α_cA_c) + χ_c(A_cB_c) = χ_u(αμ) + χ_u(μA).

3. **u is rigid.** #αμ(u) = 1 and #μA(u) = 1, and both are trees (Lemma E: minimal P1 and P3). So the right-hand side is 1 + 1 = 2.
4. **P2(c) = (2, 1).** By Lemma E its chains are trees, so χ_c(α_cA_c) = #α_cA_c = 2.
5. Hence **χ_c(A_cB_c) = 0.** The A_cB_c pair graph is nonempty (it contains x_{j+3}, x_{j+4} of c's frame), so it has a cycle.
6. **P1(c) has 3 chains,** so by Lemma E its χ values are (1, 1, 0). The A_cB_c chains are a sub-multiset of these with total 0, so they are exactly the unicyclic chain. Therefore #A_cB_c = 1 and #α_cμ_c = 2. ∎

**Remark (the other star identity).** The star identity at colour B (u's names), together with Lemma E, gives χ_c(α_cμ_c) = χ_c(α_cA_c). The hypothesis #α_cA_c = 2 is therefore exactly what selects the σ side. With #α_cA_c = 1 the identities alone would allow either side. That case cannot occur at a DL state, by Theorem D. In the census every hypothesis instance of Lemma S is DL (`tl_sigma_general.py`: 1,412 / 1,412).

**What is planar here.**
- For Corollary S1, the only planar input is Lemma E (|E(T)| = 3n − 6, plus "faces are triangles"). Lemmas St, J1, J2 and J3 hold in any graph, and there is no Jordan or band-surgery input.
- Corollary S2 also uses Theorem D, to get #α_cA_c ≥ 2.
- So in **any** graph with a hole, an in-shape state c is σ-type as soon as the sphere constants Σχ = (2, 3, 3) hold at c and at π⁻¹(c). This explains the TrackJ data:
- The 80 / 3,475 general-graph failures (TrackJ §1.4) must violate those constants at c or at π⁻¹(c). This is a logical consequence of the proof, not a separate check.
- The rung-(d2)/(d) examples satisfy only the H3 *balance* E₁ = E₂ + 1 = E₃ + 1, not the absolute values, yet they are σ-type anyway.

## 3. Data (every step separately)

`tl_sigma_check.py` covers the census frame 23–29 (every hole), plantri24 (1/10), and fullerene duals C20–C46 (1/2): 19,935 holes in all.

| step | claim | instances | failures |
|---|---|---|---|
| S0 | star identity across π: χ_c(αA)+χ_c(AB) = χ_u(αμ)+χ_u(μA), plus the second star identity (colour B) and J2 | 2,030,934 π-steps | 0 |
| S1 | rigid ⇒ χ-vector = (1,1,2,1,2,1) (forests) | 43,407 rigid states | 0 |
| S2 | P2 minimal ⇒ χ(αA), χ(μB) = (2,1); P3 minimal ⇒ χ(αB), χ(μA) = (2,1) | 658,961 / 660,096 | 0 |
| S3 | u rigid, c = π(u), P2(c) minimal ⇒ χ_c(AB) = 0 | 5,501 | 0 |
| S3′ | same, with N(c) = 9 ⇒ extra chain is αμ | 5,112 | 0 |
| S4 | in-shape ⇒ σ-type and χ-vector (2,0,2,1,2,1) | 1,657 in-shape states | 0 |
| Lemma S general form | u rigid, #P1(c) = #P2(c) = 3 ⇒ (#αμ, #AB)(c) = (2,1) (`tl_sigma_general.py`, frames 23–27 + plantri24 1/20) | 1,412 | 0 |

**Independent planar models** (exhaustive; no primal input):
- **Chord model of rigid u** (`tl_chord.py`, TrackI instances, ≤ 13 cubic vertices). Every rigid u whose π-image is DL with N = 9 and P1 extra has C′ on the σ side: 1 + 9 + 69 = 79 / 79. Here the side is computed from the embedding, by face tracing (Euler-checked).
- **F12 figure-eight model of c** (`tl_fig8.py` / `tl_ladder.py`, ≤ 15 cubic vertices). Every c with k(H) = 2, k(F13) = 1, DL and π⁻¹(c) rigid is σ-type: 1 + 9 + 69 + 503 = 582 / 582.
  - Dropping any one hypothesis (k(F13) = 1, or k(HΔX̃) = k(HΔỸ) = 1) produces both sides.

**Where the proof breaks: RP²** (`out/sigma_rp2.log`, 202 TrackH RP² test beds, 2,981 holes):
- S0 holds (0 / 208,843), as it must, since it holds in any graph.
- S1 and S2 fail at **every** instance: 2,573 / 2,573 rigid states and 101,221 / 101,221 P2-minimal states are not forests. This is Lemma E with χ_S = 1: one unicyclic chain per partition.
- S3 fails in 188 / 368 cases.
- So the proof does not apply on RP². Even so, the σ-type conclusion held in all 223 RP² cases with N(c) = 9 (5 of them in-shape). On RP², σ-type is unexplained and unproved.
