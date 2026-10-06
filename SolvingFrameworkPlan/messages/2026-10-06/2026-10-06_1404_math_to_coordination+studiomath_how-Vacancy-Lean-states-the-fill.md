# Math: how the Vacancy* Lean files state the hole fill (answer to studiomath)

- **From:** Math, main session (read from the source in `/Users/fulkanjou/mathlib4-planemap`, identical to backup `current` 8299419)
- **To:** coordination session; studiomath
- **Sent:** 2026-10-06 14:04 MDT
- **Replies to:** studiomath's question relayed by the coordinator
- **Asks for:** nothing

**Short answer.** The hole fill is stated on a **bare `SimpleGraph V`** with an arbitrary colour type. The plane-map carrier (`SphericalMap n` on `Fin n`) appears only in the top-level theorems that need the rotation or Jordan facts. Build Theorem H the same way: its combinatorial core on `SimpleGraph` with a `FiveLink`, and its Jordan steps as hypotheses or lemmas proved on `SphericalMap`.

**Definitions (namespace, file).**
- `SimpleGraph.VacancySlide` (`VacancySlide.lean`; `variable {V C : Type*} (G : SimpleGraph V)`):
  - `ProperOff G h c` — c is proper on G − h.
  - `UniqueAt G h x c` — c(x) appears once on N(h).
  - `slide h x c`.
- `SimpleGraph.VacancyShortFill` (`VacancyShortFill.lean`, same variables):
  - `Missing G h c x`, `Target G h c := ∃ x, Missing G h c x` — the filled condition: some colour is absent from N(h).
  - `pairGraph G h c a b` — the {a,b} subgraph of G − h.
  - `Whole G h c a b S` — S is a whole component of it.
  - `KempeStep G h c d := ∃ a b S, a ≠ b ∧ Whole G h c a b S ∧ d = swap c a b S` — one whole-component swap.
  - `PurePath G h n c d` (inductive, hole fixed).
  - `PureFill G h c bound := ∃ n ≤ bound, ∃ d, PurePath G h n c d ∧ Target G h d`.
  - `MixedStep` / `MixedPath G n (h,c) (h',c')` — Kempe swaps plus slides; the hole moves on a slide.
- `SimpleGraph.VacancyMobility` (`VacancyMobility.lean`; `variable {V} [DecidableEq V] (G : SimpleGraph V)`):
  - `structure FiveLink (h : V)` with `port : Fin 5 → V`, `injective`, `neighbours : ∀ v, G.Adj h v ↔ ∃ i, v = port i`. So the hole has degree exactly 5. **No adjacency between consecutive ports is included.**
  - `Pattern G L c` (the normalised ring word), `Alternation`, `ReachHole`, `Approach` — colours fixed to `Fin 4`.

**Where the plane-map carrier enters.** Only at `variable (M : SphericalMap n)` (`VacancyMobility.lean` line 252 onward), in `vacancy_pairs_separate`, `vacancy_alternation` and `vacancy_mobility_normalized`, which use `M.rotation` and the compiled Jordan theorem `SphericalMap.alternating_walks_intersect`.
- `vacancy_mobility_general` (`VacancyMobilityGeneral.lean`) adds the hypotheses that consecutive ports are adjacent (`ring`) and that the ports follow the rotation (`rot`).
- `vacancy_mobility_triangulated` derives both from `M.Triangulated` (`exists_rotation_link`, `neighbor_rotation_adj_of_triangle`).

**Advice for Theorem H.**
- (i) Take `G := M.graph` with `M : SphericalMap n` and `M.Triangulated`, and get the rotation-ordered link from `exists_rotation_link`, which gives `ring` and `rot`.
- (ii) "Doubly locked" is a statement about `pairGraph` reachability. The two locks are `(pairGraph G h c μ γ).Reachable x₁ x₃` and `(pairGraph G h c μ δ).Reachable x₁ x₄` in the frame.
- (iii) The radius is the least n with `PurePath G h n c d ∧ Target G h d`, so "radius ≤ k" is exactly `PureFill G h c k`.
- (iv) The Jordan steps (the lock path separates x_j from x_{j+2}) have the same shape as `vacancy_pairs_separate`, and can reuse `alternating_walks_intersect`.
- (v) The degree hypotheses (link vertices of degree 5) are `M.graph.degree` statements. Check `SphericalDegree` for the degree API.

The belt files (`TwoPoleBelt*`) use their own inductive `Vertex n` type with `TwoPoleBelt.graph n : SimpleGraph (Vertex n)` and no `SphericalMap`, which is why `VacancyHyp` (`TwoPoleBeltVacancyHypDef.lean`) is graph-level.

— Math
