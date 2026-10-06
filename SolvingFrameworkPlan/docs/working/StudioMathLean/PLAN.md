# Studio Math: Lean plan for the Euler lemma and Theorem H (6 Oct 2026)

Status (updated 1406 MDT): **Piece 1 compiled.** `EulerCounting.lean` (SHA-256 prefix 4a2f0fb67de7d1d6), theorem `StudioMath.good_card_ge_twelve`, no `sorry`, `#print axioms` = [propext, Classical.choice, Quot.sound]. Checked as a single file with Lean v4.35.0-rc3 against the read-only Mathlib oleans of `~/mathlib4-planemap-build` (Mathlib 300d0e5) via LEAN_PATH, at nice -n 10; nothing in that directory was written. Not yet audited. Pieces 2 and 3 not started.

## Finding from reading the library [hand, from source]
`SphericalMap.edge_card_bound` (PlaneMap/SphericalDegree.lean) gives only `E + 1 ≤ V_support + F`. For a triangulation (3F = 2E) this yields E ≤ 3V − 3, i.e. Σ(deg−6) ≤ −6. The accepted Euler lemma needs Σ(deg−6) = −12 (E = 3V − 6), because its threshold is 12. So the existing inequality is one step too weak: the library's current `exists_pos_degree_le_five` needs only Σ(deg−6) < 0. We need the full Euler identity V − E + F = 2 for a connected triangulation.

## Plan
1. **Piece 1: counting lemma** (`EulerCounting.lean`, compiled, `good_card_ge_twelve`). Pure `SimpleGraph` statement: min degree ≥ 5 and 2E + 12 ≤ 6V imply at least 12 degree-5 vertices with at most one neighbour of degree ≥ 12. Needs only Mathlib (handshake `sum_degrees_eq_twice_card_edges`, double counting). Can be built and checked in isolation with a single-file `lake env lean`, which is light.
2. **Piece 2: sharp Euler bound** for the `SphericalMap` carrier, all faces of length 3 and a connected graph: `2E + 12 ≤ 6V`. Two extra facts beyond `edge_card_bound`: rank(incidence) = V − 1 (connected graph) and dim ker(boundary) = 1 (dual connected, which follows from connectivity of the graph). Alternative: derive E ≤ 3V − 6 from a quadrangulation or girth argument. I have not chosen yet. This is the real work.
3. **Piece 3: Theorem H**, after the local combinatorics is stated: a `vacancy state` in the library's existing `SimpleGraph.Vacancy*` language (inspect `VacancySlide.lean` and `VacancyShortFill.lean`), hypothesis "the five link vertices have degree 5, rotation at v is the cyclic order, no chord in the link". The proof is a finite colour case analysis once the DL predicate and the swap are defined.

## Open decision for the coordinator
The hole-fill statements need the plane-map carrier (rotation, outer ring w_t) rather than a bare `SimpleGraph`. I will ask the Math team (Lean owner) how `Vacancy*` states it before writing Piece 3.
