# Classical reductions for the minimal-counterexample frame (F1–F4), written for Lean

Math worker, 6 October 2026. Mode: hand only (battery rule). **Nothing was run on this machine.** Web pages were read; no PDF was decoded.

Labels:
- **[cited: S]**: a fact read from source S (list in §7).
- **[hand]**: derived here by hand, unreviewed.
- **[hand, sketch]**: an outline with named gaps.
- **[spec]**: a specification for a Studio script, not yet written or run.

Context: the frame in `messages/2026-10-06/…_minimal-counterexample-frame.md` and `…_hybrid-frame-diamond-subsumes-our-local-results.md`. The Lean vocabulary follows `messages/2026-10-06/…_how-Vacancy-Lean-states-the-fill.md` and the read-only tree `/Users/fulkanjou/mathlib4-planemap` (PlaneMap directory `Mathlib/Combinatorics/SimpleGraph/PlaneMap/`, abbreviated `PM/` below).

## Summary

| Item | Statement | Status here | Smaller graph used | Planarity input | Lean cost |
|---|---|---|---|---|---|
| F1a | min degree ≥ 5 | [hand]; **already in Lean** (`four_color_extension`, wrapper in `SphericalFourContact.lean`) | T − x | `alternating_walks_intersect` (exists) | none new |
| F1b | every triangle is a face (no separating triangle) | [hand], complete | two spanning subgraphs of T | J1 sector lemma, J3 face lemma | small |
| F2 | every 4-cycle has a chord (no separating 4-cycle) | [hand], complete, all cases written | two spanning subgraphs; in one case one of them plus one chord | J1, J3, J5 crossing, J6 vacated face + `split_fills` | medium |
| F3 | Birkhoff diamond is reducible | [hand] full 31-row table; **D-reducible**, closure depth 5; agrees with [cited] | T − (4 interior vertices); **no contraction** | J1 + J5 only | medium, then a decidable table |
| F3′ | RSST 2.122 is reducible | definition [cited: data file]; **D-reducible** per the data file (empty contract) [cited]; table not done by hand | T − (4 interior vertices) | as F3 | spec for script + certificate |
| F4 | internally 6-connected (Birkhoff's 5-ring theorem) | statement [cited]; proof [hand, sketch] | needs **hub insertion and vertex identification** | J1, J5, new map surgery | large |

Three things matter most:
- **D-reducibility needs no map surgery.** For F3 and F3′ the smaller graph is a spanning subgraph of T, so `subgraph_closed` and the support-size induction already supply its colouring. The only planarity fact needed is the ring-crossing lemma J5, which reduces to one generalisation (J1) of the existing `closed_walk_separates`.
- **[hand] By-product (§4.2):** configuration 2.122 is a degree-5 vertex whose link contains three consecutive vertices of degrees 5, 6, 5. So in the R\*_min class, **(5,5,6,5,6) and (5,6,5,6,6) are also excluded**, besides the diamond classes. (5,5,6,6,6), (5,6,6,6,6) and (6⁵) are not excluded by it.
- F2 is fully hand-proved. It needs one small map construction, a chord inserted into a vacated face. F4 needs real new infrastructure; §5 gives a finite-check route.

---

## 0. Conventions and the Lean form of "minimal counterexample"

### 0.1 Carriers
- `M : SphericalMap n` (`PM/SphericalMap.lean`): `graph : SimpleGraph (Fin n)`, `rotation : RotationSystem graph`, `fills : rotation.Fills`.
- `M.Triangulated` (`PM/SphericalCompletion.lean`): every face has length 3.
- A colouring is `c : Fin n → Fin 4`. It is proper on a graph H if `H.Adj u v → c u ≠ c v`. `H.Colorable 4` is Mathlib's.
- **Kempe vocabulary** (`PM/VacancyShortFill.lean`): `pairGraph G h c a b`, `Whole G h c a b S`, `swap c a b S`, `KempeStep`. Properness is preserved by `properOff_swap` and `kempe_proper`.
  - In a reduction we apply them to G := G′ (the outside graph). The parameter h is any vertex that is isolated in G′, for example an interior vertex of the deleted configuration. Excluding an isolated vertex changes no component.
- `next` means `M.rotation.next` on darts at a vertex (as in `closed_walk_separates`). `walkEdgeCoeff X e ∈ ZMod 2` is the parity of uses of edge e by walk X (`PM/SphericalFiveColor.lean`).

### 0.2 Minimal counterexample
**Definition 0.1 (IH(k)).** For every m and every `N : SphericalMap m` with `Nat.card N.graph.support < k`, `N.graph.Colorable 4`.

**Definition 0.2 (MinCex T).** `T : SphericalMap n` with 0 < n, `T.graph.Connected`, `T.Triangulated`, `∀ x, 5 ≤ T.graph.degree x` (so the support is all of `Fin n`), IH(n), and `¬ T.graph.Colorable 4`.

**Lemma 0.3 [hand; the Lean proof pattern exists].** If some SphericalMap is not 4-colourable, then some T satisfies MinCex.
- *Proof.* Choose a non-4-colourable M with s = `Nat.card M.graph.support` least, so IH(s) holds.
  - If some x in the support has degree ≤ 4: by `isolate_closed` and `isolate_support_card_lt`, M with x isolated has smaller support, so it is colourable. Then `four_color_extension` colours M, a contradiction.
  - So every support vertex has degree ≥ 5. `exists_supportTransport` gives N on `Fin s` with full support, the same adjacency and the same degrees. N is not colourable (it is isomorphic to M on the support, and isolated vertices are free).
  - `exists_triangulated_completion_min_five` gives T ⊇ N on `Fin s`, connected, triangulated, minimum degree ≥ 5. T is not colourable, since a colouring of T colours N. Its support is `Fin s`, and IH(s) holds.
- This is the first half of `four_color_of_triangulated_five_extension` (`PM/SphericalFourContact.lean`), stopped before the gate.

**Proposed gate (replaces `TriangulatedFiveExtension` for this frame):**
```lean
def MinimalFrameGate : Prop :=
  ∀ (n : ℕ) (T : SphericalMap n), 0 < n → T.graph.Connected → T.Triangulated →
    (∀ x, 5 ≤ T.graph.degree x) →
    (∀ m (N : SphericalMap m), Nat.card N.graph.support < n → N.graph.Colorable 4) →
    T.graph.Colorable 4
```
Every reduction below is a lemma with the hypotheses of this gate plus one structural hypothesis (a non-facial triangle, a chordless 4-cycle, a diamond, …), and the conclusion `T.graph.Colorable 4`.

### 0.3 Three generic lemmas
**Lemma 0.4 (Sub) [hand].** Assume IH(n) and `T : SphericalMap n` with full support. Let `H ≤ T.graph` with some x such that H has no edge at x. Then `H.Colorable 4`.
- *Proof.* `subgraph_closed T H` gives `N : SphericalMap n` with `N.graph = H`. Its support ⊆ `Fin n` \ {x}, so its cardinality is < n. Apply IH(n).

**Lemma 0.5 (Glue) [hand].** Let V = A ⊔ S ⊔ B, with no T-edge between A and B. Let c₁ be proper on T[A ∪ S] and c₂ proper on T[B ∪ S], with c₁ = c₂ on S. Then c, equal to c₁ on A ∪ S and to c₂ on B, is proper on T.
- *Proof.* An edge uv of T has both ends in A ∪ S, or both in B ∪ S, because there are no A–B edges. In the first case c = c₁ on both ends. In the second, c = c₂ on both ends, since c₁ = c₂ on S.

**Lemma 0.6 (Perm) [hand].** Let S be finite and κ, κ′ : S → Fin 4 with κ(s) = κ(t) ↔ κ′(s) = κ′(t) for all s, t. Then there is π ∈ Perm (Fin 4) with κ′ = π ∘ κ.
- *Proof.* Define π₀ on the image of κ by π₀(κ(s)) = κ′(s). It is well defined by (→) and injective by (←). Extend the injection to a bijection of Fin 4 (`Equiv.extendSubtype` or similar).
- π ∘ c is proper whenever c is proper, so colourings may be renamed freely.

---

## 1. Planarity interface (the only places where the sphere is used)

### J1. Sector lemma (generalises `closed_walk_separates`) [hand]
**Statement.** Let `M : SphericalMap n`, X a closed walk, u a vertex, and e, e′ darts at u with e′ = nextʲ e (1 ≤ j < deg u). Assume:
- (i) e.snd ∉ X.support and e′.snd ∉ X.support;
- (ii) Σ over 0 < i < j of `walkEdgeCoeff X (edge (nextⁱ e))` = 1 in ZMod 2.

Then there is no walk from e.snd to e′.snd whose support avoids X.support.

**Proof.**
- `walkEdgeCoeff_is_face_sum X` gives c : Face → ZMod 2 with coeff(edge d) = c(face d) + c(face d.symm) for every dart d. This is the `hc` of `closed_walk_separates`.
- *Step relation.* For each dart d at u, c(face (next d)) = c(face d.symm). This is `face_of_face_next` exactly as `hface12` is derived. So c(face(next d)) = c(face d) + coeff(edge d).
- *Sweep.* Iterating from d = e to nextʲ⁻¹ e gives c(face e′) = c(face e) + Σ_{0 ≤ i < j} coeff(nextⁱ e).
  - The i = 0 term is coeff(edge e) = 0. This is `walkEdgeCoeff_zero_of_not_mem_support`, since e.snd ∉ X.support (by (i)).
  - So c(face e′) = c(face e) + 1 by (ii).
- *Walk.* Suppose q is a walk from e.snd to e′.snd avoiding X. `face_coeff_eq_along_disjoint_walk X c hc q _ e.symm e′.symm` gives c(face e.symm) = c(face e′.symm).
- *Close.* c(face e.symm) = c(face e) + coeff(e) = c(face e), and likewise for e′. So c(face e) = c(face e′), contradicting the sweep.

`closed_walk_separates` is the case j = 2. `alternating_walks_intersect` is its corollary for X = a hub loop.

### J2. Wedges
Let C = (r₀, …, r_{k−1}) be a cycle of T (distinct vertices, r_t ~ r_{t+1}, indices mod k, k ≥ 3).
- At r_t let d⁺ and d⁻ be the darts to r_{t+1} and r_{t−1}.
- The **left wedge** L_t is the set of heads of nextⁱ d⁺ for 0 < i < j_t, where nextʲᵗ d⁺ = d⁻.
- The **right wedge** R_t is the set of the remaining heads, other than r_{t±1}.

**Lemma J2 [hand].** If C passes r_t exactly once (true for a cycle), y ∈ L_t, z ∈ R_t, and y, z ∉ C, then no walk from y to z avoids C.
- *Proof.* Apply J1 with X = C, e = dart to y, e′ = dart to z. The sweep from e to e′ passes d⁻ (coefficient 1) and no other edge of C at r_t, because C uses only d⁺ and d⁻ at r_t, each once. So the sum is 1.

### J3. Faces of a triangulation [hand]
If `T.Triangulated` and next(u→x) = (u→y), then u, x, y are the three vertices of a face, and x ~ y. This is `neighbor_rotation_adj` in `PM/RotationSystem.lean`; `vacancy_mobility_triangulated` uses it.

Consequences:
- **(F-a)** Each edge xy lies in exactly two faces.
- **(F-b)** A triangle {u, x, y} is a face iff y is the next or the previous neighbour after x at u.
- **(F-c)** The face to the left of the directed edge r_t → r_{t+1} is {r_t, r_{t+1}, w}. Its third vertex w is the first element of L_{t+1} and the last element of L_t; for the right side, R in place of L. If L_t is empty, then w = r_{t−1}.
- **(F-d)** Consecutive elements of a wedge are adjacent, by J3. So each wedge spans a walk in T.

### J4. The two sides of a non-facial triangle or a chordless cycle [hand]
**Setting.** C is a cycle with k = 3 that is not a face, or with k ≥ 4 and no chord (no edge r_s r_t with s, t non-consecutive). T is triangulated and connected.

**Lemma J4.**
- (a) Every wedge L_t and R_t is non-empty and disjoint from C.
- (b) Let In be the set of vertices joined to ⋃_t L_t by a walk avoiding C, and Out the same for ⋃_t R_t. Then V = C ⊔ In ⊔ Out, with no edge between In and Out.
- (c) In and Out are connected, and every r_t has a neighbour in In (in L_t) and one in Out (in R_t).

**Proof.**
- (a), emptiness. If L_t = ∅ then next d⁺ = d⁻, so r_{t−1} ~ r_{t+1} and {r_{t−1}, r_t, r_{t+1}} is a face (J3).
  - For k = 3 this says C is a face, which is excluded.
  - For k ≥ 4 it gives a chord, which is excluded.
- (a), disjointness. Wedge vertices are neighbours of r_t other than r_{t±1}. A wedge vertex on C would be a chord (k ≥ 4) or one of r_{t±1} (k = 3).
- (c), connectivity of In. Each L_t is connected by (F-d).
  - L_t and L_{t+1} share the vertex w_t of (F-c). Here w_t ∉ C: for k = 3, w_t ∈ C would make C a face; for k ≥ 4 it would make w_t r_t or w_t r_{t+1} a chord.
  - So ⋃ L_t is connected avoiding C, and In is connected. The same holds for Out.
- (b), covering. For x ∉ C, take a walk from x to C (T is connected) and cut it at its first vertex on C, say r_t. Its previous vertex y is a neighbour of r_t not on C, so y ∈ L_t ∪ R_t. Hence x ∈ In ∪ Out.
- (b), disjointness. If x ∈ In ∩ Out, then by connectivity there is a walk avoiding C from some y ∈ L_t to some z ∈ R_s.
  - Using the walk inside ⋃ L through the w's, move the start to some y′ ∈ L_s.
  - This contradicts J2 at r_s.
- (b), no In–Out edge. Such an edge would put its Out end in In.

**Definitions used below.**
- A **separating triangle** is a non-facial triangle.
- A **separating 4-cycle** is a chordless 4-cycle. By J4 both of its sides are non-empty, so this agrees with the frame's wording.

### J5. Ring crossing for an outside graph [hand]
**Setting (ring datum).**
- Ring r : Fin k → V injective (k ≥ 4) with r_t ~ r_{t+1}.
- Interior K ⊆ V \ ran r. Every T-neighbour of a K-vertex lies in K ∪ ran r. T[K] is connected.
- For every t, L_t = N(r_t) ∩ K and L_t ≠ ∅ (the "inner wedge is the interior").
- **Outside graph** G′ := T with every edge incident to K deleted (a spanning subgraph).
- F2 uses this with K = In (or K = Out, with the orientation reversed). F3 and F3′ use it with K = the configuration's interior.

**Lemma J5.** Let a, c, b, d be ring indices in strictly increasing cyclic order. If P is a walk in G′ from r_a to r_b and Q is a walk in G′ from r_c to r_d, then P and Q share a vertex.

**Proof.** Suppose P and Q are vertex-disjoint.
- **Step 1 (segment reduction).**
  - Let s₀ = a, s₁, …, s_m = b be the ring indices that P visits, in order. Removing c and d from the cycle Z_k leaves two open arcs U ∋ a and U′ ∋ b. No s_i is c or d, since P ∩ Q = ∅.
  - Take the first i with s_{i+1} ∈ U′. Then s_i ∈ U, so (s_i, s_{i+1}) interleaves (c, d), and s_i, s_{i+1} are not cyclically consecutive.
  - The piece P₁ of P between these two visits is a **segment**: a single chord edge, or a path whose interior avoids ran r ∪ K (G′ has no K-edges).
  - Apply the same step to Q with respect to (s_i, s_{i+1}) to get a segment Q₁.
  - Rename: P₁ goes from r_{a′} to r_{b′}, Q₁ from r_{c′} to r_{d′}, with a′ < c′ < b′ < d′ cyclically. P₁ ∩ Q₁ = ∅.
- **Step 2.** Let X be the closed walk P₁ followed by the ring arc from r_{b′} back to r_{a′} through r_{c′}. It does not contain r_{d′}.
  - At u = r_{c′}, X uses exactly the two ring darts, each once. P₁ avoids r_{c′}, because r_{c′} ∈ Q.
  - Let e′ be the dart from r_{c′} to some z ∈ L_{c′} ⊆ K.
  - Let e be the first dart of Q₁, ending at q₁. Here q₁ ∉ K, and q₁ ≠ r_{c′±1} (it is interior to a segment, or it is r_{d′}, which is not consecutive to c′). So e lies in the right wedge.
  - Sweeping from e′ to e crosses exactly one ring dart, so condition (ii) of J1 holds.
  - Neither z nor q₁ is on X: z ∈ K; q₁ ∈ Q₁ is off P₁ and off the arc.
- **The connecting walk.** Go from z through K to some z′ ∈ L_{d′} (T[K] is connected), then to r_{d′}, then back along Q₁ to q₁.
  - Its vertices lie in K, are r_{d′}, or are interior to Q₁. All of them are off X.
  - J1 forbids this walk, a contradiction.

**Corollary J5′ (non-crossing of Kempe components) [hand].** Let c be proper on G′, and θ = {α,β}|{γ,δ} a split of the four colours. Let S₁ be an αβ-component of G′, and S₂ either a different αβ-component or any γδ-component. Then the ring indices in S₁ and those in S₂ do not interleave.
- *Proof.* S₁ ∩ S₂ = ∅: distinct components of one pair graph are disjoint, and the two pair graphs use disjoint colours. Walks in `pairGraph` are walks in G′. Apply J5.
- *In Lean.* The component is `{v | (pairGraph G′ h c α β).Reachable s v}`, with h ∈ K.

### J6. Vacated face and chord insertion (needed only in F2, case 2) [hand]
**Setting.** C is a chordless 4-cycle with sides In and Out (J4).
- Erase every edge with an end in Out, one edge at a time. Keep the rotation each time: this is `eraseEdge` of `PM/SphericalDelete.lean`, and Fills is preserved by `fills_eraseRotation`.
- Call the result N, with `N.graph = T[In ∪ C]` as a spanning graph.

**Claim.** In N the four darts r_t → r_{t+1} (orientation chosen so that In is on the left) form one face orbit.
- *Proof.* In N the rotation at r_t is that of T with the darts into R_t removed. R_t ⊆ Out because C is chordless.
- So in N the successor of d⁻ at r_t is d⁺. With the face permutation `faceNext d = next d.symm` (`face_next_apply`), this gives faceNext(r_{t−1} → r_t) = (r_t → r_{t+1}).

**Chord insertion.** Hence for i ∈ {0, 1} the darts a = (r_i → r_{i+1}) and b = (r_{i+2} → r_{i+3}) lie on one face of N, and r_i ≁ r_{i+2} (chordless). `split_fills` (`PM/RotationSplitFills.lean`) gives a SphericalMap with graph `T[In ∪ C] + r_i r_{i+2}`. Its support avoids Out ≠ ∅.

**Lean cost.** One lemma describing `next` after a batch of `eraseEdge`s ("the next surviving dart"), plus the face-orbit computation above. Small to medium.

---

## 2. F1 [hand]

**Theorem F1.** If MinCex T, then:
- (a) every vertex has degree ≥ 5 (built into MinCex, by Lemma 0.3);
- (b) every triangle of T is a face.

**F1(a), proof of the degree-4 step** (already in Lean as `four_color_extension`).
- Let deg x = 4 with link x₀x₁x₂x₃ in rotation order. Colour T − x by IH. If the link uses ≤ 3 colours, colour x. Otherwise let c(x₀) = α and c(x₂) = β.
- If x₀ and x₂ lie in different αβ-components of T − x, swap the component of x₀. Then x₀ and x₂ both have colour β, and α is free at x.
- Otherwise there is an αβ-walk x₀ ⇝ x₂ avoiding x. Every γδ-walk x₁ ⇝ x₃ avoiding x meets it (`alternating_walks_intersect`), which is impossible since the colour sets are disjoint. So swap the γδ-component of x₁, and γ is free.
- Degree ≤ 3 is immediate.

**F1(b), proof.**
- Let Δ = {a, b, c} be a non-facial triangle. J4 gives V = Δ ⊔ In ⊔ Out, both sides non-empty, with no In–Out edge.
- Lemma 0.4 with x ∈ Out colours H₁ = T[In ∪ Δ] by c₁. With x ∈ In it colours H₂ = T[Out ∪ Δ] by c₂.
- Δ is a clique, so c₁ and c₂ are injective on Δ. Lemma 0.6 gives π with π ∘ c₂ = c₁ on Δ.
- Lemma 0.5 glues c₁ and π ∘ c₂. So T is colourable, a contradiction.

**Use in the frame.** The frame uses F1(b) as follows. For deg v = 5 with link x₀..x₄, an edge x_i x_{i+2} would make {v, x_i, x_{i+2}} a triangle. It is not a face, because by (F-b) the faces at v are {v, x_j, x_{j+1}}.

---

## 3. F2: every 4-cycle has a chord [hand, complete]

**Theorem F2.** If MinCex T, then every 4-cycle of T has a chord.

**Setup.**
- Let C = r₀r₁r₂r₃ be chordless. Then F1(b) and J4 give sides In and Out, both non-empty and connected, with every r_t adjacent to both.
- Let G_in = T[In ∪ C] and G_out = T[Out ∪ C] (spanning subgraphs). Since C is chordless, every edge of T lies in G_in or G_out.
- J5 applies to G_out with K = In, and to G_in with K = Out.

**Patterns.**
- For a proper c on either side, let e₀₂ = [c(r₀) = c(r₂)] and e₁₃ = [c(r₁) = c(r₃)]. The pattern is the pair (e₀₂, e₁₃), written TT, TF, FT or FF.
- Every proper colouring of the 4-cycle has one of these, and the 4-cycle has exactly 4 colourings up to permutation, one per pattern:
  - TT: 1212
  - TF: 1213
  - FT: 1232
  - FF: 1234
- Count check [hand]: P(k) = (k−1)⁴ + (k−1) gives 1 + 2 + 1 = 4 classes.
- By Lemma 0.6, colourings with equal patterns differ by a permutation.

**Lemma F2.1 (two-pattern lemma) [hand].** Let S be a side, c proper on S, and Σ(c) the set of patterns of colourings reachable from c by Kempe swaps in S. Then Σ(c) contains a **bit-fixed pair**: all patterns with e₀₂ = b, or all patterns with e₁₃ = b, for some b.

Proof by the pattern of c, writing c on (r₀, r₁, r₂, r₃) and using J5′ for "crossing". Two components in a statement below are whole components (`Whole`).

| Start pattern | Colouring | Test | If the test holds | Otherwise (by J5′) | Pair obtained |
|---|---|---|---|---|---|
| TT | (α,γ,α,γ) | r₁ and r₃ in different γδ-components | swap r₁'s: (α,δ,α,γ) is TF | r₀ and r₂ in different αβ-components; swap r₀'s: (β,γ,α,γ) is FT | {TT,TF} (e₀₂=T) or {TT,FT} (e₁₃=T) |
| TF | (α,γ,α,δ) | r₁, r₃ in different γδ-components | swap: (α,δ,α,δ) is TT | r₀, r₂ in different αβ-components; swap: (β,γ,α,δ) is FF | {TF,TT} (e₀₂=T) or {TF,FF} (e₁₃=F) |
| FT | (α,γ,β,γ) | r₀, r₂ in different αβ-components | swap: (β,γ,β,γ) is TT | r₁, r₃ in different γδ-components; swap: (α,δ,β,γ) is FF | {FT,TT} (e₁₃=T) or {FT,FF} (e₀₂=F) |
| FF | (α,γ,β,δ) | r₀, r₂ in different αβ-components | swap: (β,γ,β,δ) is TF | r₁, r₃ in different γδ-components; swap: (α,δ,β,δ) is FT | {FF,TF} (e₁₃=F) or {FF,FT} (e₀₂=F) |

In every row, the swapped component contains no other ring vertex, because the two ring vertices of the other class have colours outside the swapped pair.

**Lemma F2.2 [hand].** Two bit-fixed pairs that fix different bits meet, in the pattern (b, b′). Two that fix the same bit with different values are disjoint.

**Proof of F2.**
- Colour G_in by c_in and G_out by c_out (Lemma 0.4; In and Out are non-empty). Let P_in ⊆ Σ(c_in) and P_out ⊆ Σ(c_out) be the pairs from F2.1.
- **Case 1: P_in ∩ P_out ≠ ∅.** Pick a common pattern p, and colourings c′_in ∈ Kempe(c_in) and c′_out ∈ Kempe(c_out) with pattern p. Kempe swaps preserve properness on their side (`kempe_proper`). Lemma 0.6 renames c′_out to agree with c′_in on C, and Lemma 0.5 glues them. Contradiction.
- **Case 2: the pairs are disjoint.** By F2.2 they fix the same bit, say the bit of the diagonal {r_i, r_{i+2}}, with opposite values.
  - Let S be the side whose pair has that bit = T (equal), and S′ the other side, whose pair is "bit = F", i.e. **all** patterns with c(r_i) ≠ c(r_{i+2}).
  - Recolour S: by J6 (chord r_i r_{i+2} drawn in the face vacated by S′), S + r_i r_{i+2} is a SphericalMap of smaller support. IH colours it by c″_S, with c″_S(r_i) ≠ c″_S(r_{i+2}).
  - So the pattern of c″_S lies in P_{S′} ⊆ Σ(c_{S′}). Finish as in Case 1, with c″_S restricted to S.

**Remarks.**
- Case 2 is where an extra construction is needed. Kempe moves on both unmodified sides do not suffice in general: a side may have all reachable colourings with r₀ = r₂, and the other side all with r₀ ≠ r₂. No elementary argument excludes that. [hand]
- The chord is the only map surgery in F1–F3.

---

## 4. F3 and F3′: the Birkhoff diamond and RSST 2.122

### 4.1 Source data [cited: RSST `unavoidable.conf`, format from `FC/ftpinfo.html`]
The RSST data file lists each configuration as follows:
- an identifier;
- a line `n r a b`: n = vertices of the free completion, r = ring size, a = |C|, b = |C′|;
- a line `k` followed by 2k integers: the k edges of the contract X;
- the adjacency list (second column = degree in the free completion);
- coordinates.

Vertices 1..r are the ring, in order; r+1..n are the configuration.

First entry (the Birkhoff diamond):
```
0.7322
10   6      16       0
 0
 1  4    2  7 10  6
 2  4    3  8  7  1
 3  3    4  8  2
 4  4    5  9  8  3
 5  4    6 10  9  4
 6  3    1 10  5
 7  5    2  8  9 10  1
 8  5    2  3  4  9  7
 9  5    8  4  5 10  7
10  5    9  5  6  1  7
```
Second entry:
```
2.122
11   7      39       0
 0
 1  4    2  8 11  7
 2  3    3  8  1
 3  4    4  9  8  2
 4  3    5  9  3
 5  4    6 10  9  4
 6  4    7 11 10  5
 7  3    1 11  6
 8  6    2  3  9 10 11  1
 9  5    3  4  5 10  8
10  5    9  5  6 11  8
11  5   10  6  7  1  8
```
(Coordinate lines omitted.)

**Reading [hand inference from the format].**
- For both entries **k = 0, so the contract is empty**. The configurations are listed as D-reducible: no contraction, and the reducer is just the deletion.
- a is the number of ring colourings (up to permutation) that extend to the configuration. **Our hand count for the diamond gives 16** (§4.4), which agrees with a = 16. For 2.122, a = 39 of 91 (§4.6).
- Separately [cited: Steinberger, arXiv:0905.0043, §1 as rendered by ar5iv]: the Birkhoff diamond is described as the first and smallest reducible configuration. For it, the set of ring colourings that do not extend has **no non-empty consistent subset**, which is D-reducibility. Steinberger also notes that Birkhoff originally used a reducer graph A′; RSST's data needs none.

### 4.2 The configurations in the frame's words
- **Diamond.** Interior {7,8,9,10}. 7 ~ 9 is the central edge. 8 and 10 are the common neighbours, and 8 ≁ 10. All four have degree 5. Ring neighbours:
  - N_R(7) = {1,2}
  - N_R(8) = {2,3,4}
  - N_R(9) = {4,5}
  - N_R(10) = {5,6,1}

  Rotations (from the file): 7: (2,8,9,10,1); 8: (2,3,4,9,7); 9: (8,4,5,10,7); 10: (9,5,6,1,7). This is the frame's "two adjacent degree-5 vertices with two non-adjacent common neighbours of degree 5".
- **2.122.** Interior {8,9,10,11}. Degrees: deg 8 = 6, deg 9 = deg 10 = deg 11 = 5. Edges 8~9, 8~10, 8~11, 9~10, 10~11; 9 ≁ 11. So it is a diamond on central edge 8–10 with the hub 8 of degree 6. Ring neighbours:
  - N_R(8) = {1,2,3}
  - N_R(9) = {3,4,5}
  - N_R(10) = {5,6}
  - N_R(11) = {6,7,1}

  **Equivalent description [hand].** A degree-5 vertex v (= 10) whose link (9, 5, 6, 11, 8) contains three consecutive vertices 11, 8, 9 of degrees 5, 6, 5.
- **Consequence for R\*_min [hand].** A degree-5 vertex whose link has a cyclically consecutive triple of degrees (5, 6, 5) contains 2.122. This assumes the occurrence lemma of §4.3, which uses F1 and F2. So, besides the diamond classes:
  - (5,5,**6**,5,6) is excluded: positions 1, 2, 3 are 5, 6, 5.
  - (5,**6**,5,6,6) is excluded: positions 0, 1, 2.
  - (5,5,6,6,6), (5,6,6,6,6) and (6⁵) are **not** excluded by 2.122.
  - Degree "6" means exactly 6.

### 4.3 Occurrence in a minimal counterexample (diamond) [hand]
**Hypothesis (frame).** a, b adjacent, deg a = deg b = 5, with common neighbours c, d, c ≁ d, and deg c = deg d = 5. Rename them 7 = a, 9 = b, 8 = c, 10 = d.

**Derivation of the full occurrence**, for T satisfying MinCex, F1 and F2:
- (O1) T has no separating triangle (F1b). So 7 and 9 have exactly two common neighbours: a third one w would give a non-facial triangle {7, 9, w}. These two are the rotation-neighbours of 9 at 7 (F-b).
- (O2) By J3 the faces at 7 are triangles on consecutive link vertices. So the link of 7 in rotation order is (r₂, 8, 9, 10, r₁) for two new vertices r₁, r₂. In the same way 8, 9, 10 give r₃, r₄ (from 8), r₅ (from 9) and r₆ (from 10). The faces on each interior edge are identified by (F-a), which is how the file's rotations arise.
- (O3) The ring vertices are outside K (link entries are distinct, and 8 ≁ 10). Consecutive ring vertices are adjacent (consecutive link entries, J3). At each r_t the interior neighbours form the inner wedge: for example, at r₁ the faces {r₁, r₂, 7}, {r₁, 7, 10} and {r₁, 10, r₆} make r₂, 7, 10, r₆ consecutive in rotation.
- (O4) **The ring map is injective.** Consecutive ring vertices are distinct (loopless). For a non-consecutive pair with u = r_i = r_j:

| Pair | Contradiction |
|---|---|
| (1,5) | 10 is adjacent to both, so 10 has < 5 distinct neighbours |
| (2,4) | 8 is adjacent to both, same argument |
| (1,3) | triangle {u,7,8}; faces on 78 are {7,8,2} and {7,8,9}; u ≠ r₂ (adjacent to it), u ≠ 9; so non-facial, against F1b |
| (1,4) | triangle {u,7,8}; same as (1,3) |
| (2,5) | triangle {u,7,9}; faces on 79 are {7,9,8} and {7,9,10}; u ∉ K |
| (2,6) | triangle {u,7,10}; faces on 7–10 are {7,10,1} and {7,10,9}; u ≠ r₁ (adjacent) |
| (3,5) | triangle {u,8,9}; faces on 89 are {8,9,4} and {8,9,7}; u ≠ r₄ (adjacent) |
| (4,6) | triangle {u,9,10}; faces on 9–10 are {9,10,5} and {9,10,7}; u ≠ r₅ (adjacent) |
| (3,6) | 4-cycle (u,8,7,10). Its chords would be u7 or 8–10. 8 ≁ 10 by hypothesis. u ∉ N(7) = {r₁,r₂,8,9,10}, since u = r₃ ≠ r₂ (adjacent) and r₃ ≠ r₁ by case (1,3). So it is chordless, against F2 |

- (O5) All T-neighbours of K are in K ∪ R (degrees are exactly 5). T[K] is connected, and every ring vertex has a K-neighbour. **So the ring datum of J5 holds.**

The same derivation for 2.122 is a [spec] item: the Studio can generate it mechanically from the file. RSST prove a general version of (O4) for all configurations; their exact statement was not read here.

### 4.4 Reduction for the diamond (precise)
1. **Delete** K = {7,8,9,10}. G′ := T with all edges at K erased. Nothing is contracted and no edge is added.
2. **Colour** G′ by Lemma 0.4 (x = 7). Let κ = c|ring, a proper colouring of the 6-cycle (ring edges are in G′).
3. **If κ extends** (table below), colour K and glue (Lemma 0.5, with A = K, S = ring, B = rest). Otherwise apply the Kempe moves of §4.5 inside G′ (h = 7 in `pairGraph`). This reaches a colouring of G′ whose ring colouring extends, after at most 5 moves (rounds).

**Ring-6 colourings up to permutation [hand].**
- P(k) = (k−1)⁶ + (k−1) gives a₂ = 1, a₃ = 10, a₄ = 20 colourings with exactly 2, 3, 4 colours: **31 in total**.
- Canonical form: colours renamed in order of first appearance (positions 1..6).

**Extension test.** Write A = col 7, B = col 8, C = col 9, D = col 10. The constraints are:
- A ∉ {k₁, k₂}
- B ∉ {k₂, k₃, k₄}
- C ∉ {k₄, k₅}
- D ∉ {k₅, k₆, k₁}
- A, C, B pairwise distinct; A, C, D pairwise distinct (B = D is allowed, since 8 ≁ 10).

In the table, "ext" gives (A, B, C, D), each checked against all five neighbours. **E = the 16 colourings that extend.** "bad" means none exists; the forced choices are shown.

| # | κ (1..6) | extends? | witness / obstruction |
|---|---|---|---|
| 1 | 121212 | bad | A,C ∈ {3,4} distinct ⇒ {A,C} = {3,4}; B ∈ {3,4} clashes |
| 2 | 121213 | bad | B ∈ {3,4}, A ∈ {3,4}, C ∈ {3,4} ⇒ clash |
| 3 | 121232 | ext | (3,4,1,4) |
| 4 | 121234 | ext | (4,3,1,2) |
| 5 | 121312 | ext | (3,4,2,4) |
| 6 | 121313 | ext | (3,4,2,4) |
| 7 | 121314 | bad | B = 4 ⇒ A = 3 ⇒ C = 2 ⇒ D ∈ {2,3} \ {3,2} = ∅ |
| 8 | 121323 | ext | (3,4,1,4) |
| 9 | 121324 | bad | B = 4, D = 3 ⇒ A ∉ {1,2,3,4} |
| 10 | 121342 | bad | B = 4, D = 3 ⇒ A has no colour |
| 11 | 121343 | ext | (3,4,1,2) |
| 12 | 123123 | bad | B = D = 4, A = 3 ⇒ C ∈ {3,4} \ {3,4} |
| 13 | 123124 | bad | B = 4, D = 3 ⇒ A ∈ {3,4} clashes |
| 14 | 123132 | ext | (3,4,2,4) |
| 15 | 123134 | bad | B = 4, D = 2, A = 3 ⇒ C ∈ {2,4} clashes |
| 16 | 123142 | bad | B = 4, D = 3 ⇒ A has no colour |
| 17 | 123143 | bad | B = 4, D = 2, A = 3 ⇒ C ∈ {2,3} clashes |
| 18 | 123212 | bad | {A,C} = {3,4} forced; D ∈ {3,4} clashes |
| 19 | 123213 | ext | (3,1,4,2) |
| 20 | 123214 | ext | (3,1,4,2) |
| 21 | 123232 | ext | (3,4,1,4) |
| 22 | 123234 | ext | (3,1,4,2) |
| 23 | 123242 | bad | D = 3 ⇒ A = 4 ⇒ C = 1 ⇒ B ∈ {1,4} clashes |
| 24 | 123243 | ext | (4,1,3,2) |
| 25 | 123412 | ext | (4,1,2,3) |
| 26 | 123413 | ext | (4,1,3,2) |
| 27 | 123414 | ext | (4,1,3,2) |
| 28 | 123423 | bad | B = 1, D = 4 ⇒ {A,C} = {2,3}; A = 3 ⇒ C = 2 ∉ {1,3} |
| 29 | 123424 | bad | B = 1, D = 3 ⇒ {A,C} = {2,4}; A = 4 ⇒ C = 2 ∉ {1,3} |
| 30 | 123432 | ext | (3,1,2,4) |
| 31 | 123434 | bad | B = 1, D = 2 ⇒ {A,C} = {3,4}; C ∈ {1,2} clashes |

**|E| = 16, agreeing with a = 16 in the data file.** Bad: 15 colourings.

### 4.5 Kempe closure (D-reducibility) for the diamond [hand]
**Moves.** Fix a split θ of {1,2,3,4} into two pairs, A-class and B-class. Every ring position belongs to one class.
- By J5′, the ring positions met by the components of the two pair graphs form a **non-crossing partition into class-pure blocks**. Consecutive same-class positions are always in one block, since ring edges are in G′.
- Swapping whole components flips any union of blocks. Swaps in one class leave both classes' components unchanged, so swaps can be sequenced.

**Rule.** κ becomes good in round i+1 if, for some θ, **in every case of the component structure**, some union of blocks flips κ into a colouring in good_i (up to permutation). good₀ = E.

Three case schemes are used. Each is exhaustive by J5′.
- **(S-2)** Each class has exactly two runs, alternating A₁, B₁, A₂, B₂ around the ring:
  - *either* A₁ and A₂ are in one component (then B₁ and B₂ are in different ones), and the available flips are B₁ or B₂;
  - *or* A₁ and A₂ are in different components, and the available flips are A₁ or A₂.
  - The test is: (flip B₁ or flip B₂ good) **and** (flip A₁ or flip A₂ good).
- **(S-3)** Classes alternate ABABAB (3 singleton runs each). Every possible structure refines one of five maximal ones:
  - M1: the A's together, the B's singletons;
  - M2: the B's together, the A's singletons;
  - M3a/b/c: one A-pair {i, i+2} together, the opposite A alone, the B between the pair alone, and the other two B's together.
  - In every maximal structure some singleton, or a union of blocks, must flip to good.

Flips are written (positions changed → new colouring → canonical form → status).

**Round 1** (into good₁ = E ∪ {#1, #2, #10, #18, #31}):
- **#1 121212**, θ = {13|24}, scheme S-3 (A = odd positions, B = even).
  - Singleton flips: pos 2 → 141212 → 121313 (E); pos 1 → 321212 → 123232 (E).
  - M1 and M3a contain the singleton {2}. M2 and M3b contain the singleton {1}.
  - M3c = A{1,5}, A{3}, B{6}, B{2,4}: flip {3} and {6} → 123214 (E).
- **#2 121213**, θ = {14|23}, S-3 (A = 1,3,5; B = 2,4,6).
  - Flip {2} → 131213 → 121312 (E). This serves M1 and M3a.
  - Flip {1} → 421213 → 123234 (E). This serves M2 and M3b.
  - M3c: flip {3} → 124213 → 123214 (E).
- **#10 121342**, θ = {14|23}, S-3 (A = 1,3,5; B = 2,4,6). All six singleton flips are good:
  - 1 → 123412
  - 3 → 123432
  - 5 → 121312
  - 2 → 121234
  - 4 → 121232
  - 6 → 121343

  Every maximal structure has a singleton.
- **#18 123212**, θ = {13|24}, S-3 (A = 1,3,5; B = 2,4,6).
  - B-singleton flips: 2 → 123414, 4 → 123412, 6 → 123214, all E. These serve M1 and M3a/b/c.
  - M2 has no B-singleton: flip {1} → 323212 → 121232 (E).
- **#31 123434**, θ = {13|24}, S-3. All six singleton flips are good:
  - 1 → 121313
  - 3 → 121343
  - 5 → 123414
  - 2 → 123232
  - 4 → 123234
  - 6 → 123432

**Round 2** (adds #7, #23):
- **#7 121314**, θ = {14|23}, S-2. A-class (1,4) = runs {5,6,1} and {3}; B-class (2,3) = {2} and {4}.
  - B-runs separate: flip {2} → 131314 → 121213 (#2, good₁).
  - B-runs joined: flip {3} → 124314 → 123413 (E).
- **#23 123242**, θ = {14|23}, S-2. (1,4)-class: {1} and {5}; (2,3)-class: {2,3,4} and {6}.
  - {1} and {5} separate: flip {1} → 423242 → 123212 (#18, good₁).
  - {1} and {5} joined: flip {6} → 123243 (E).

**Round 3** (adds #9, #15, #16, #29):
- **#9 121324**, θ = {12|34}, S-2. (3,4)-class: {4} and {6}; (1,2)-class: {1,2,3} and {5}.
  - Separate: flip {4} → 121424 → 121323 (E).
  - Joined: flip {5} → 121314 (#7, good₂).
- **#15 123134**, θ = {13|24}, S-2. (2,4)-class: {2} and {6}; (1,3)-class: {3,4,5} and {1}.
  - Separate: flip {2} → 143134 → 123132 (E).
  - Joined: flip {1} → 323134 → 121314 (#7).
- **#16 123142**, θ = {12|34}, S-2. (3,4)-class: {3} and {5}; (1,2)-class: {6,1,2} and {4}.
  - Separate: flip {3} → 124142 → 123132 (E).
  - Joined: flip {4} → 123242 (#23, good₂).
- **#29 123424**, θ = {13|24}, S-2. (1,3)-class: {1} and {3}; (2,4)-class: {2} and {4,5,6}.
  - Separate: flip {1} → 323424 → 121323 (E).
  - Joined: flip {2} → 143424 → 123242 (#23).

**Round 4** (adds #13, #17, #28):
- **#13 123124**, θ = {13|24}, S-2. (1,3)-class: {1} and {3,4}; (2,4)-class: {2} and {5,6}.
  - (1,3)-runs joined: flip {2} → 143124 → 123142 (#16, good₃).
  - (1,3)-runs separate: flip {1} → 323124 → 121324 (#9, good₃).
- **#17 123143**, θ = {12|34}, S-2. (1,2)-class: {1,2} and {4}; (3,4)-class: {3} and {5,6}.
  - (1,2)-runs joined: flip {3} → 124143 → 123134 (#15, good₃).
  - (1,2)-runs separate: flip {4} → 123243 (E).
- **#28 123423**, θ = {13|24}, S-2. (1,3)-class: {6,1} and {3}; (2,4)-class: {2} and {4,5}.
  - (1,3)-runs joined: flip {2} → 143423 → 123243 (E).
  - (1,3)-runs separate: flip {3} → 121423 → 121324 (#9).

**Round 5** (adds #12):
- **#12 123123**, θ = {12|34}, S-2. (3,4)-class: {3} and {6}; (1,2)-class: {1,2} and {4,5}.
  - Separate: flip {3} → 124123 → 123124 (#13, good₄).
  - Joined: flip {4,5} (1↔2) → 123213 (E).

**Result [hand].** All 31 colourings are good by round 5:
- 16 extend directly;
- round 1: 5; round 2: 2; round 3: 4; round 4: 3; round 5: 1.

**The Birkhoff diamond is D-reducible.** This agrees with [cited: Steinberger §1; RSST data, empty contract].

**Why the induction closes.** Every flip is a finite sequence of `KempeStep`s in G′ (one per component), so the result is again proper on G′. By induction on the round, any colouring of G′ reaches one whose ring colouring is in E. Then K is coloured (Lemma 0.6 renames the witness) and glued (Lemma 0.5).

### 4.6 F3′: 2.122 — reduction and Studio spec
**Reduction.** As in §4.4, delete K = {8,9,10,11}. The data file's contract is empty, so it is D-reducible [cited: data file; reading per §4.1].

**Count [hand].** P(k) = (k−1)⁷ − (k−1) gives a₃ = 21 and a₄ = 70. So there are **91 ring-7 colourings up to permutation**, and the file says a = 39 extend.

**Studio script [spec]** (exploratory, < 1 CPU-second; hashed package per the coordinator rule):
1. **Input.** Parse entries 0.7322 and 2.122 from `unavoidable.conf` (save the fetched file with its SHA-256). Ring = vertices 1..r in order; interior = r+1..n with the adjacency lists.
2. **Ring colourings.** Enumerate all proper κ : Z_r → {0..3} and canonicalise by first appearance. Expect 31 (r = 6) and 91 (r = 7). Also keep the raw lists (732 and 2184) for the Lean table.
3. **Extension.** κ extends iff some σ : interior → {0..3} is proper on interior edges and on interior–ring edges (brute force, 4⁴ = 256). **Expect 16 and 39**; a mismatch is a stop condition.
4. **Closure.** Set good = E. Repeat until no change: for each bad κ and each θ of the 3 splits:
   - compute the class word;
   - enumerate **all** set partitions π of the ring positions (Bell(7) = 877) that are class-pure, non-crossing, and put consecutive same-class positions in the same block;
   - κ passes θ if every π has a union of blocks F with canon(flip(κ, F)) ∈ good.

   Mark κ good at the current round if some θ passes. Record (round, θ, and for each **maximal** π the chosen F and the target's index).
5. **Outputs.**
   - the per-colouring certificate (JSON);
   - the round histogram;
   - D-reducible yes/no.

   **Regression:** the diamond must reproduce §4.5 (rounds 5/2/4/3/1, depth 5). Different θ choices are allowed, but every colouring must be good, with depth ≤ 5.
6. **Independent check.** A second implementation should use RSST's own formulation (signed matchings on one class), or simply re-verify the certificate entries without re-searching.

**How Lean consumes it.**
- **(A) Reflection checker (preferred).**
  - Define `Config` (ring size r, interior size m, adjacency as `Bool` tables) and a computable `dredCheck : Config → Bool` that runs step 4 over raw colourings `Fin r → Fin 4`. Raw colourings avoid canonical forms; permutation-closure is then automatic.
  - Prove once: `dredCheck K = true → ∀ T, Occurrence K T → IH → T.graph.Colorable 4`.
  - Instances: `by decide`, or `by rfl` on a structurally recursive `Bool` function. This is Gonthier's approach in Coq.
  - The soundness proof needs J5′ (generic in K), Lemmas 0.4–0.6, and `kempe_proper`.
- **(B) Certificate table.** Include the JSON as a Lean list. A checker validates each entry locally: it extends, or for its θ every listed structure has a flip to an earlier-round entry. Also prove a **generic** completeness lemma: the listed structures are the maximal ones (for r ≤ 7 this is itself a `decide` over 877 partitions).
- `native_decide` would be fastest but adds the compiler to the trusted base. That is a team policy call; Mathlib proper disallows it.
- **Occurrence.** `Occurrence K T` packages (O2)–(O5): an injective ring map, an injective interior map, adjacency agreement, inner wedges, and K's neighbourhood closed in K ∪ ring.
  - A separate lemma derives it from the frame's degree pattern, as in §4.3. That lemma uses F1 and F2.
  - For 2.122 the Studio can emit the (O4) case list (pairs of ring positions with the triangle or 4-cycle each identification creates), which a hand reviewer then checks.

---

## 5. F4: internal 6-connectivity (Birkhoff's 5-ring theorem)

**Statement [cited: R. Thomas, FC page, "known since 1913"; Birkhoff 1913, not opened].** Let T be a minimal counterexample (MinCex). If C is a 5-cycle of T and V \ C = In ⊔ Out with no In–Out edge, then |In| ≤ 1 or |Out| ≤ 1. With min degree 5 and no separating triangle, |In| = 1 means In = {v}, with C the link of v.

**Ring-5 colourings [hand].** P(k) = (k−1)⁵ − (k−1) gives 5 + 5 = **10 classes**:
- **T_s** (3 colours), for s ∈ Z₅: (c at s; a, b, a, b at s+1..s+4). Its equal pairs are {s+1, s+3} and {s+2, s+4}.
- **F_j** (4 colours), for j ∈ Z₅: r_j = r_{j+2}, and the other three positions get distinct colours.

**Forcing graphs** for colouring one side Y when the other side X has |X| ≥ 2. Each has smaller support.
- **Hub:** X replaced by one vertex adjacent to all of C. This forces a T_s.
- **Identification** r_j ≡ r_{j+2} through X's face. This forces F_j, T_{j−1} or T_{j−2}.
- **Chord** r_j r_{j+2} in X's face. This forces r_j ≠ r_{j+2}.

**Kempe step from T_s [hand]** (scheme S-2 of §4.5 applied to ring 5):
- With θ = {a,d}|{b,c}: the side reaches T_{s+4} or F_{s+2}.
- With θ = {b,d}|{a,c}: it reaches T_{s+1} or F_{s+1}.

**Proof outline [hand, sketch].**
- Colour Out with a hub in In's place: c_out = T_s, whose reachable set is described above. Colour In with a hub, an identification or a chord in Out's place, chosen from what Out reaches.
- Close every case as in F2 (pairs that must meet). Unlike F2, the case tree for ring 5 has not been completed here, and identifications seem unavoidable.

**Finite-check route [spec].**
- Call a set Σ of the 10 classes *consistent* if for each κ ∈ Σ and each θ there is a structure (as in §4.5) all of whose flips stay in Σ.
- The reachable set of any side is consistent and non-empty.
- Theorem F4 follows from a finite check over the 2¹⁰ subsets: for every consistent Σ_out meeting the hub set {T_s}, there is a forcing f such that every consistent Σ_in meeting Φ_f meets Σ_out.
- Both sides may also be re-forced, which turns the check into a two-move game. The Studio can run this in seconds and emit a certificate that Lean checks by `decide`.
- **Whether it passes with only these three forcings is untested.**

**Lean cost (assessment).**
- *New map surgery:*
  - hub insertion: a new vertex in a face, joined to all 5 ring vertices (repeated `split` from an isolated label, which needs a bridge step; `RotationBridgeFills.lean` may help);
  - vertex identification across a face: a new `RotationMerge` with a Fills proof comparable to `split_fills`.
- *Combinatorics:* J5 (shared with F3), the finite certificate, and the glue. Estimate: the largest of the four items; identification alone is comparable to the existing split/Fills development.
- **Recommendation.** Formalise F1, F3 and F3′ first (no surgery), then F2 (one chord insertion).
  - Keep F4 as a hypothesis of R\*_min until the gate needs it.
  - In this frame F4 is used only to restrict the R\*_min class (Theorem U shapes), not in the fan argument, which needs only F1(b).

---

## 6. What is proved here, what is assumed

**Proved [hand]:**
- J1, J2, J4 and J5 (modulo the Lean wording);
- F1(b) and F2 (complete case analysis);
- the diamond's occurrence lemma (O1)–(O5);
- the 31-row extension table and the 5-round Kempe closure;
- the counts 31 and 91;
- the (5,6,5) consequence of 2.122.

**Cited:**
- the RSST data entries and the file format;
- the empty contract of both entries;
- Steinberger's statement that the diamond's non-extending set has no consistent subset;
- Birkhoff's 5-ring theorem.

**Not done:**
- the ring-7 table for 2.122 (Studio spec, §4.6);
- the F4 case tree (§5);
- reading RSST's paper text (its PDF did not decode here), Birkhoff 1913, and Tilley's tables.

**Checks a reviewer should make first:**
- the J5 Step-2 sweep parity;
- rows 7, 12, 28 and 29 of §4.4;
- round 5 of §4.5.

---

## 7. Sources
- RSST data file `unavoidable.conf`, `https://thomas.math.gatech.edu/OLDFTP/four/unavoidable.conf` (entries 0.7322 and 2.122; fetched 2026-10-06). Format: `https://thomas.math.gatech.edu/FC/ftpinfo.html`.
- R. Thomas, *The Four Color Theorem*, `https://thomas.math.gatech.edu/FC/fourcolor.html` (minimal counterexamples internally 6-connected; data location).
- J. Steinberger, "An unavoidable set of D-reducible configurations", arXiv:0905.0043 (read via ar5iv): definitions of D- and C-reducibility, the closure algorithm, and the Birkhoff diamond (paraphrased here).
- Robertson–Sanders–Seymour–Thomas, *J. Combin. Theory Ser. B* 70 (1997) 2–44 (`thomas.math.gatech.edu/PAP/fc.pdf`; fetched but not decodable here).
- J. A. Tilley, "Kempe-locking configurations", *Mathematics* 6(12):309 (2018), arXiv:1809.02807. Its text, as read through ar5iv, contains no ring-colouring table.
- G. D. Birkhoff, "The reducibility of maps", *Amer. J. Math.* 35 (1913) 115–128 (not opened).
- Lean references: `PM/FiveColorSeparation.lean` (`closed_walk_separates`, `alternating_walks_intersect`, `face_coeff_eq_along_disjoint_walk`), `PM/SphericalDelete.lean` (`subgraph_closed`, `isolate_closed`, `eraseEdge`), `PM/SupportTransport.lean`, `PM/SphericalCompletion.lean`, `PM/RotationSplitFills.lean` (`split_fills`), `PM/VacancyShortFill.lean` (`pairGraph`, `Whole`, `swap`, `kempe_proper`), `PM/FourColorExtension.lean`, `PM/SphericalFourContact.lean`.
