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

## Update 1429 MDT: relative-class Euler lemma (audit S1)

- `StudioMath.good_card_add_two_four`: the counting core with degree-4 vertices allowed, each costing two. It shows 12 ≤ good + 2·n₄. `good_card_ge_twelve` is now its corollary.
- `StudioMath.good_off_add_four`: let φ have at most 3 vertices, every vertex off φ degree ≥ 5, and every vertex on φ degree ≥ 4 (if 4, then it is on φ). Then 2E + 12 ≤ 6V implies **9 ≤ #(good off φ) + n₄**, where n₄ = #(degree-4 vertices on φ).
- `SphericalMap.relative_light_fives`: the same for spherical triangulations.
  - This is the audit's 13:25 repair: at least 9 − n₄ good vertices off φ, so ≥ 7 when n₄ ≤ 2.
  - It needs neither n₄ ≤ 2 nor 4-connectivity. φ is any vertex set of size ≤ 3; in the application it is the protected face.
- Non-vacuity: `Icosahedron.relative_light_fives_icosahedron`, with φ = {0,1,5} and n₄ = 0. **No instance with n₄ > 0 has been built.**
- `#print axioms`: propext, Classical.choice, Quot.sound only.

## Update 1427 MDT: the IcoBall derivation and non-vacuity (answers audit S3; derivation done)

- **Dedupe.** `EulerCounting.lean` is removed. Its content lives only in `PlaneMap/EulerSharp.lean`, so each declaration exists exactly once.
- **`SphericalMap.theorem_H`** in `PlaneMap/VacancyIcosahedral.lean`, now with **no `IcoBall` hypothesis**.
  - Hypotheses: `M.Triangulated`; `degree h = 5`; every neighbour of h has degree 5; `M.NoSeparatingTriangleAt h`.
  - Conclusion: every proper 4-colouring of T − h has `PureFill ... 3`.
  - `NoSeparatingTriangleAt h` means: if two neighbours u, v of h are adjacent, then they are consecutive in the rotation at h. On a triangulation, that is exactly the statement that every triangle through h is a face.
  - It is used only to exclude the chord x_t x_{t+3}, i.e. w_t = x_{t+3}.
- **`icoBall_of_triangulated`** derives `IcoBall` from those hypotheses.
  - Triangle law `nx_tri`: three `faceNext` steps close a face.
  - `orbit5` / `chain5`: at a degree-5 vertex the rotation is one 5-cycle of darts. So the rotation at x_t reads w_t → x_{t+1} → h → x_{t−1} → w_{t−1} and lists every neighbour exactly once.
- **Non-vacuity**, on the library's `Icosahedron.sphericalMap`:
  - `Icosahedron.theorem_H_icosahedron`: every hypothesis of `theorem_H` holds at vertex 0, for an explicit colouring `sampleColouring` that is proper off 0 and **not** already filled (`sampleColouring_unfilled`).
  - `Icosahedron.twelve_light_fives_icosahedron`: the hypotheses of the Euler lemma hold.
- **Axioms.** `#print axioms` for all of these lists propext, Classical.choice and Quot.sound only. No `sorry`.
- **Note.** The icosahedron has no doubly locked state, so the sample exercises the statement, not the R1–R3 branches.

## Compiled 1419 MDT (single-file checks, read-only against the built snapshot 8299419; not yet audited)

Reproduce with `check.sh`. Hashes are in `SHA256SUMS`. No file contains `sorry`. `#print axioms` lists only propext, Classical.choice and Quot.sound; `ring_cases` uses only propext. A deliberately broken copy was rejected, which confirms that the check really elaborates the proofs.

| file | main theorem | statement |
|---|---|---|
| (in `EulerSharp.lean`) | `StudioMath.good_card_ge_twelve` | finite simple graph, every degree ≥ 5, 2E + 12 ≤ 6V ⇒ ≥ 12 degree-5 vertices with ≤ 1 neighbour of degree ≥ 12 |
| `PlaneMap/EulerSharp.lean` | `SphericalMap.edge_card_bound_sharp` | any `SphericalMap` with a dart: E + 2 ≤ n + F (no connectivity hypothesis) |
| | `SphericalMap.twice_edges_add_twelve_le` | all faces of length 3 ⇒ 2E + 12 ≤ 6n |
| | `SphericalMap.twelve_light_fives` | **Euler lemma:** spherical triangulation (a dart, all faces of length 3), every vertex of degree ≥ 5 ⇒ ≥ 12 degree-5 vertices with ≤ 1 neighbour of degree ≥ 12. The file repeats the counting lemma so that it is self-contained. |
| `PlaneMap/VacancyIcosahedral.lean` | `SphericalMap.ico_fill` | **Theorem H:** hole h with `FiveLink` L in rotation order, and `IcoBall` (see below) ⇒ every proper 4-colouring of T − h has `PureFill ... 3` (a filled hole within ≤ 3 whole-component Kempe swaps) |
| | `VacancyIcosahedral.ico_fill_normalized` | the same on any `SimpleGraph`, for link word 0,1,0,2,3, given the library's `Alternation` |

**What `IcoBall` assumes, for the auditor.** `IcoBall G h L w` is an explicit hypothesis. It is not derived from "triangulation and degree 5". It requires:
- each `L.port t` has neighbour set exactly {h, port(t−1), port(t+1), w(t−1), w(t)};
- w(t) ~ w(t+1);
- w(t) is neither a port nor h.

In a triangulation with no separating triangle through h, these follow from the five link vertices having degree 5. That derivation is **not** formalised. The statement is therefore Theorem H over the local data, which is how `MathRadiusGeometry.md` states it. The conclusion is stronger than "radius ≤ 3 for doubly locked states": it covers every colouring.

**Not done:** Theorem HP; the derivation of `IcoBall` from triangulation and degree hypotheses; the R* links.
