# The lock-parity lemma: statement and hand proof for formalisation

Track F, 7 Oct 2026. **Hand proof (unreviewed), data-checked.** It is written for Track C to formalise against the existing `QuarterFloor` / `QuarterPairDuality` API.

## Summary

- The lemma splits into two parts:
  1. a **purely combinatorial parity identity (Theorem P)**. It holds on every triangulated closed surface: orientable or not, any genus, no planarity;
  2. the **existing formal Kempe duality at the hole (Theorem D)**, which is the only place the sphere is used.
- Lock parity (Theorem LP) is P plus D.
- Consequence for LPC: "every unfilled state of the class obeys lock parity" is *exactly* "the two Kempe dualities of Theorem D hold at every unfilled state of the class". So LPC is the class-level statement "local Kempe duality at the hole ⇒ a filled state". It is planarity localised to the two lock chains at the hole, not a new topological invariant. See §5. In π-language (§5.2): LPC ⇔ no Kempe class is a union of all-DL π-cycles.

## 1. Setting and notation

- **The graph.** G is a finite simple graph on vertex type V. 𝓕 is a finite set of 3-element vertex sets ("faces") such that:
  - (F1) every face is a triangle of G (its three vertices are pairwise adjacent);
  - (F2) every edge {u,v} of G lies in exactly two faces.

  Any triangulation of a closed surface gives such a pair. For a `SphericalMap` with `M.Triangulated`, 𝓕 is the set of faces of the map.
- **The hole.** h ∈ V has exactly five neighbours x₀, …, x₄ (`Pent G h`: `adj_h`, `adj_cyc`, `inj`, `only`), with indices mod 5. We also need:
  - (F3) the faces containing h are exactly {h, x_t, x_{t+1}} for t ∈ ℤ/5.

  (F3) is the "link is the 5-cycle x₀…x₄ in rotation order" hypothesis. On a triangulated map it follows from `Pent` together with the rotation at h.
- **The colouring.** c : V → Fin 4 is proper on G − h: adjacent vertices other than h get different colours (`ProperOff G h c`; the value c(h) is never used). We assume `RepeatAt P c j` and write:
  - α = c(x_j) = c(x_{j+2}), μ = c(x_{j+1}), A = c(x_{j+3}), B = c(x_{j+4}).
  - In Lean, `RepeatAt` (QuarterFloor.lean) already contains the six disequalities that make α, μ, A, B pairwise distinct, i.e. the state is unfilled with repeat pair {j, j+2}. This is needed: if μ = A, say, then K_{αA} = K_{αμ} and the case table of Step 4 is wrong.
- **Standing graph hypotheses.** G is simple and loopless, V is finite (`Fintype V`, `DecidableEq V`), and `Pent` gives x₀, …, x₄ pairwise distinct, adjacent to h, consecutive ones adjacent, and no other neighbour of h.
- **Components.** For colours p ≠ q and v ∈ V − h with c(v) ∈ {p,q}, K_{pq}(v) is the vertex set of the component of v in the subgraph of G − h induced on colours {p,q}. This is exactly `{w | (pairGraph G h c p q).Reachable v w}`. Note h ∉ K_{pq}(v).
- **Boundary.** For X ⊆ V − h, δ(X) is the set of edges of **G** with exactly one end in X. *Edges from X to h count.*
- **Odd vertices.** odd(G) = {v ≠ h : deg_G v is odd}, with the degree taken in **G**. So a link vertex's degree includes its edge to h, and h itself is never in X.

  By the handshake identity (Step 1 below), |X ∩ odd(G)| ≡ |δ(X)| (mod 2). So "odd number of odd-degree vertices" and "odd boundary" are the same condition, and the boundary form is the one to formalise.
  - *Warning:* with degrees taken in G − h, the identity changes and the lemma becomes vacuous for K_{αA}: the parity is then 1 always.
  - Degrees in the 2-coloured subgraph are useless: they always sum to an even number over a component.
- **Locks.** As in `QuarterFloor`:
  - Lock1 ⇔ x_{j+3} ∈ K_{μA}(x_{j+1});
  - Lock2 ⇔ x_{j+4} ∈ K_{μB}(x_{j+1}).

## 2. Statements

**Theorem P (parity identity; any surface).** Under (F1)–(F3), properness off h and `RepeatAt P c j`:

- (P1) |δ(K_{αA}(x_{j+2}))| is odd ⇔ x_j ∉ K_{αA}(x_{j+2});
- (P2) |δ(K_{αB}(x_{j+2}))| is odd ⇔ x_j ∉ K_{αB}(x_{j+2});
- (P3) |δ(K_{αμ}(x_{j+2}))| is odd. Note that x_j, x_{j+1} ∈ K_{αμ}(x_{j+2}) always, via the link path x_{j+2} x_{j+1} x_j.

**Theorem D (Kempe duality at the hole; sphere; already formal).** For a triangulated spherical map with `RepeatAt P c j`:

- (D2) Lock2 ⇔ x_j ∉ K_{αA}(x_{j+2}).
  - ⇒ is `not_reach_alpha_A_of_lock2` (public in NoFrozen.lean; a private copy in QuarterRotationPlanar.lean is the lemma behind `rot3Def_of_lock2`). Hypotheses: `RepeatAt P c j`, `Lock2 P c j`, `P : Pent M.graph h` for a `SphericalMap` M.
  - ⇐ is the contrapositive of `reach_alpha_A_of_not_lock2` (QuarterPairDuality.lean). Hypotheses: `M.Triangulated`, `RepeatAt`, `¬ Lock2`.
- (D1) Lock1 ⇔ x_j ∉ K_{αB}(x_{j+2}).
  - ⇒ is `not_reach_alpha_B_of_lock1` (NoFrozen.lean; private copy behind `rot2Def_of_lock1`).
  - ⇐ is the contrapositive of `reach_alpha_B_of_not_lock1` (QuarterPairDuality.lean).

Here K_{αB} is `pairGraph … (c (x j)) (c (x (j+4)))`, i.e. {α, B}, which matches the Lean statements. Lean states reachability from x_j to x_{j+2}; reachability is symmetric.

**Theorem LP (lock parity; sphere).**
- Lock2 ⇔ |δ(K_{αA}(x_{j+2}))| is odd ⇔ K_{αA}(x_{j+2}) contains an odd number of vertices of odd G-degree.
- Lock1 ⇔ the same for K_{αB}(x_{j+2}).
- K_{αμ}(x_{j+2}) always has odd boundary.

*Proof.* Theorem P combined with Theorem D. ∎

**Suggested Lean names.** `card_boundary_mod_two` (Step 1), `boundary_eq_mixed_faces` (Step 2), `outer_mixed_parity` (Step 3), `parity_alphaA`, `parity_alphaB`, `parity_alphaMu` (Step 4), `lock2_iff_odd_boundary`, `lock1_iff_odd_boundary`.

## 3. Proof of Theorem P

Fix X = K_{pq}(x_{j+2}) for one of the pairs {p,q} = {α,A}, {α,B} or {α,μ}, and let {r,s} be the complementary pair.

**Step 1 (handshake).** Σ_{v∈X} deg_G v = 2·e(G[X]) + |δ(X)|. Hence |δ(X)| ≡ |X ∩ odd(G)| (mod 2).

**Step 2 (mixed faces).** Call a face *mixed* if it has one or two of its three vertices in X.
- A face with 0 or 3 vertices in X contains no δ-edge.
- A face with 1 or 2 vertices in X contains exactly 2 δ-edges (a triangle).
- By (F2), counting pairs (δ-edge, face containing it) gives 2|δ(X)| = 2·#mixed faces.

So |δ(X)| = #mixed faces.

**Step 3 (outer faces alternate).**
- *Outside neighbours.* If u ∈ X and v ∉ X, v ≠ h are adjacent, then c(v) ∈ {r,s}. If c(v) ∈ {p,q}, then v would be in X; and c(v) ≠ c(u).
- *Type of a boundary edge.* For such a δ-edge uv with u ∈ X, v ∉ X, v ≠ h, define its type τ(uv) := [c(u) = p] xor [c(v) = r] ∈ 𝔽₂. The labelling of the pairs is fixed once and for all per case:
  - X = K_{αA}: p = α, q = A, r = μ, s = B;
  - X = K_{αB}: p = α, q = B, r = μ, s = A;
  - X = K_{αμ}: p = α, q = μ, r = A, s = B.

  (Any labelling works, since changing it flips τ on every δ-edge, which flips each outer face's sum by 2 and Σ_{exits} τ by the number of exits, which is even because the exits are the edges where the closed link cycle x₀…x₄ crosses between X and its complement. The table uses the labelling above.)
- *Each outer mixed face contributes 1.* Let f be a mixed face not containing h ("outer"). Its two δ-edges have different types:
  - if two vertices u₁, u₂ of f are in X, they are adjacent, so {c(u₁), c(u₂)} = {p,q}. The two edges u₁v, u₂v then have types that differ in the first term;
  - if one vertex u is in X, the other two v₁, v₂ are adjacent and outside, so {c(v₁), c(v₂)} = {r,s}. The two types differ in the second term.

  So Σ_{δ-edges e ⊂ f} τ(e) ≡ 1 for every outer mixed face.
- *Sum over outer faces.* Summing over outer mixed faces: #outer mixed ≡ Σ_{outer f} Σ_{e⊂f} τ(e) = Σ_{e} τ(e) · #(outer faces containing e). The last sum runs over δ-edges not incident to h; edges at h lie only in faces containing h.
- By (F2), a δ-edge not incident to h lies in 2 outer faces, unless it is a link edge x_t x_{t+1}. A link edge lies in the h-face f_t = {h, x_t, x_{t+1}} and in exactly one outer face.

  Hence **#outer mixed faces ≡ Σ_{exits} τ(e) (mod 2)**, where the *exits* are the link edges x_t x_{t+1} with exactly one end in X.

**Step 4 (the star of h).**
- By (F3) the faces at h are f_t = {h, x_t, x_{t+1}}. Since h ∉ X, f_t is mixed iff x_t ∈ X or x_{t+1} ∈ X.
- Steps 1–3 give

  **|δ(X)| ≡ #{t : x_t ∈ X or x_{t+1} ∈ X} + Σ_{t : exactly one of x_t, x_{t+1} ∈ X} τ(x_t x_{t+1}) (mod 2),**

  which depends only on X ∩ {x₀..x₄} and the link colours.
- Which link vertices X can contain: only those with colours in {p,q}. Where X contains the outside end of an exit, its colour lies in {r,s}, as Step 3 requires.

Evaluate the formula in each case. Indices are relative to j.

| X | link ∩ X | mixed f_t (count) | exits (τ) | parity |
|---|---|---|---|---|
| K_{αA}, x_j ∉ X | x₂, x₃ | f₁, f₂, f₃ (3) | x₁x₂: u = x₂ = α, v = μ → 0; x₃x₄: u = A, v = B → 0 | 3 + 0 = **1** |
| K_{αA}, x_j ∈ X | x₀, x₂, x₃ | all five (5) | x₄x₀: α, B → 1; x₀x₁: α, μ → 0; x₁x₂ → 0; x₃x₄ → 0 | 5 + 1 = **0** |
| K_{αB}, x_j ∉ X (so x₄ ∉ X; x₀x₄ is an α–B edge) | x₂ | f₁, f₂ (2) | x₁x₂ → 0; x₂x₃: α, A → 1 | 2 + 1 = **1** |
| K_{αB}, x_j ∈ X (so x₄ ∈ X) | x₀, x₂, x₄ | all five (5) | x₀x₁ → 0; x₁x₂ → 0; x₂x₃ → 1; x₃x₄: u = x₄ = B, v = A → 0 | 5 + 1 = **0** |
| K_{αμ} (x₀, x₁ ∈ X always) | x₀, x₁, x₂ | f₄, f₀, f₁, f₂ (4) | x₄x₀: α, B → 1 (here r = A); x₂x₃: α, A → 0 | 4 + 1 = **1** |

Labelling as fixed in Step 3. Each row's link membership follows from three facts: x_{j+3} ∈ K_{αA}(x_{j+2}) and x_{j+1} ∈ K_{αμ}(x_{j+2}) by adjacency; a link vertex whose colour is not in {p,q} is not in X; and x_{j+4} ∈ K_{αB}(x_{j+2}) ⇔ x_j ∈ K_{αB}(x_{j+2}) since x_j x_{j+4} is an α–B edge (likewise x_j ∈ K_{αμ} via x_{j+1}).

∎ (P1–P3)

**What the proof uses.** Only (F1)–(F3), properness off h and RepeatAt. It uses no planarity, Jordan argument or orientability; finite double counting is the whole proof. For Lean: Step 2 is a `Finset.sum_comm` over (edge, face) incidences, and Step 3 is a second one weighted by τ. The case table is `decide` once the link memberships are fixed. The only facts needed to fix them are:
- x_{j+3} ∈ K_{αA}(x_{j+2}), by adjacency;
- x_{j+1}, x_{j+4} ∉ K_{αA}, by colour;
- x_{j+4} ∈ K_{αB}(x_{j+2}) ⇔ x_j ∈ K_{αB}(x_{j+2}), since x_j x_{j+4} is an α–B edge.

## 4. Data check

| check | where | count | failures |
|---|---|---|---|
| LP on the sphere | f66 `--lockparity` (all fullerenes C20–C46; IPR C60–C88; all 7,209 order-24 min-degree-5 triangulations; frame census 22–28; 86 frame witnesses) | 496,777,103 unfilled states | **0** |
| Theorem P on non-spherical surfaces | kclass2 / kclass3 `pid_bad` and the Python engine `lpc_detail.py` (torus ×2 sets, Klein bottle, projective plane, genus 2, non-orientable genus 3, the π-cycle search graphs) | every unfilled state at every degree-5 hole: 21,968,170 in the five random censuses, plus the torus18 set and 421 search graphs (README §8) | **0** |
| Theorem D off the sphere | kclass2 `dual_bad` | | fails massively: e.g. 1,664,226 violations in 3,862,132 unfilled torus states |

So the parity identity is universal, and the duality is the topological input. On the torus, the previously observed "lock parity fails" (TrackF README §0.3) is entirely failure of D.

## 5. Consequence for LPC

Because P holds on every surface, "state s obeys lock parity" ⇔ "s satisfies (D1) and (D2)". LPC therefore reads:

> **LPC.** At a degree-5 hole of a triangulated closed surface, a Kempe class of G − h in which every unfilled state satisfies the hole duality (Lock2 ⇔ x_j ∉ K_{αA}(x_{j+2}), Lock1 ⇔ x_j ∉ K_{αB}(x_{j+2})) contains a filled state.

- It is a statement about local Kempe duality, the same input that `rot3Def_of_lock2` / `rot2Def_of_lock1` and Lemma P use. It is not about an independent parity charge.
- On the sphere, D holds at every state, so LPC ⇔ PureClean at every hole ⇒ R\* ⇒ 4CT.

### 5.1 What a violation is (hand; any surface)

At a DL state (Lock1 and Lock2), a violation of (D2) means x_j ∈ K_{αA}(x_{j+2}) although Lock2 holds. Take a {μ,B}-path Q₁ from x_{j+1} to x_{j+4} and an {α,A}-path Q₂ from x_{j+2} to x_j. They are vertex-disjoint (disjoint colour pairs). Close them through h: C₁ = h x_{j+1} Q₁ x_{j+4} h and C₂ = h x_{j+2} Q₂ x_j h. Around h the four edges come in the cyclic order x_j (C₂), x_{j+1} (C₁), x_{j+2} (C₂), x_{j+4} (C₁), so C₁ and C₂ cross transversally at h and nowhere else: their ℤ/2 intersection number is 1. On the sphere this is impossible (this is `no_cross`); on another surface both cycles are non-separating. (D1) violations are the same with Q₁ a {μ,A}-path to x_{j+3} and Q₂ an {α,B}-path. So a lock-parity violation is exactly "a lock chain and a π-chain at h are a pair of crossing non-separating cycles".

### 5.2 LPC in terms of π (hand; any surface)

Let π = R₊₃ be the swap of K_{αA}(x_{j+2}) at an unfilled state s, **defined only when x_j ∉ K_{αA}(x_{j+2})**. Then:

1. π(s) is unfilled with repeat pair {j+3, j}: the link becomes (α, μ, A, α, B) at x_j..x_{j+4}.
2. The mirror map π̃ (swap of K_{αB}(x_j), defined iff x_{j+2} ∉ K_{αB}(x_j), i.e. iff ¬inB) satisfies π̃(π(s)) = s: in π(s) the {α, A}-component of x_{j+3} is exactly the component that was swapped. So π is injective where defined, with inverse π̃.
3. In a Kempe class with no filled state every unfilled state is DL. If Lock1 fails, swapping K_{μA}(x_{j+3}) (which then misses x_{j+1}) gives the link (α, μ, α, μ, B); if Lock2 fails, swapping K_{μB}(x_{j+4}) gives (α, μ, α, A, μ). Both are filled. This is Lemma A (`lemmaA_map`), and it uses no topology.
4. For a DL state, (D2) ⇔ x_j ∉ K_{αA}(x_{j+2}) ⇔ π(s) is defined, and (D1) ⇔ π⁻¹(s) is defined.

Hence in a targetless class the π-orbits are paths and cycles of DL states, and **the lock-parity violators are exactly the ends of the non-cyclic π-orbits** (a one-state orbit violates both D1 and D2; a longer path has one D1-violator at its start and one D2-violator at its end). Therefore

> **LPC ⇔ no Kempe class of G − h consists entirely of states on all-DL π-cycles.**

*Classes up to renaming.* The data work with colourings up to a permutation of the four colours. A permutation commutes with Kempe swaps and preserves filled / DL / lock parity / π, so a renaming-class is the union of the Kempe classes it contains, which are permutations of each other. LPC for one is LPC for all.

On the sphere π is always defined, so "PureClean fails at h" ⇔ "some Kempe class is a union of all-DL π-cycles". LPC thus says: the Kempe class of an all-DL π-cycle is never closed. *Data:* violators = path ends in all 21,571 targetless classes re-run with the second engine (README §8); every cycle-free targetless class has ≥ 1 violator by this argument.

- Falsification results on other surfaces: see TrackF/README §8.

## 6. Lean sketch

```lean
-- combinatorial, any triangulated surface (faces : Finset (Finset V), each edge in exactly two faces, star of h = the five f_t)
theorem parity_alphaA (hF : FaceData G h P faces) (hc : ProperOff G h c) (hr : RepeatAt P c j) :
    Odd (boundary G (kcomp G h c (c (P.x j)) (c (P.x (j+3))) (P.x (j+2)))).card ↔
      ¬ (pairGraph G h c (c (P.x j)) (c (P.x (j+3)))).Reachable (P.x (j+2)) (P.x j)
-- sphere
theorem lock2_iff_odd_boundary (htri : M.Triangulated) (P : Pent M.graph h) (hr : RepeatAt P c j) :
    Lock2 P c j ↔ Odd (boundary M.graph (kcomp … (P.x (j+2)))).card :=
  -- D2 : Lock2 ↔ ¬ Reach(x_{j+2}, x_j), from the two existing lemmas (Reachable.symm to match their orientation)
  (⟨fun hl hre => not_reach_alpha_A_of_lock2 P c j hr hl hre.symm,
    fun hn => by_contra fun hl => hn (reach_alpha_A_of_not_lock2 htri P hr hl).symm⟩ :
      Lock2 P c j ↔ ¬ (pairGraph …).Reachable (P.x (j+2)) (P.x j)).trans (parity_alphaA …).symm
```

`FaceData` must provide (F1)–(F3). For `SphericalMap` these come from `M.Triangulated` and the face/dart API. The hard part of the Lean work is likely constructing that face finset and proving (F2) from the dart structure. The parity argument itself is short.
