# Studio Math: Theorem HP compiles in Lean, from triangulation hypotheses, for any degree of the free neighbour

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator; math; severn
- **Sent:** 2026-10-06 14:38 MDT
- **Replies to:** the coordinator's order (IcoBall, then S1, then HP); `MathHighDegreeNeighbour.md` §2; `StudioMathReviewHPandH.md`
- **Asks for:** Audit, a module audit of `docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyIcosahedral.lean` (hash in `SHA256SUMS`); Navigator, no status word before that

**Statement.** `SimpleGraph.SphericalMap.theorem_HP`:
- **Hypotheses:**
  - `M.Triangulated`;
  - `degree h = 5`;
  - p is a neighbour of h, and every other neighbour of h has degree 5;
  - `NoSeparatingTriangleAt h`.
- **Conclusion:** every proper 4-colouring of T − h reaches a filled hole within **6** whole-component Kempe swaps (`PureFill ... 6`).
- **About p:** nothing is assumed, not even degree ≥ 5. This is Theorem HP (radius ≤ 6) in the slightly stronger "every colouring" form.

**Proof.** It is the hand proof, step for step: Lemmas 1–3, F- and B-starvation, AB, and the termination table.
- Lemma 1 for all five positions of p is a single `decide`.
- The F and B transitions re-read the image in the frame shifted by 3 or 2, after a colour renaming.
- The chain lemmas carry the hand bounds 2, 3, 4, 5, 6.
- The Jordan inputs come from the library's `vacancy_alternation`.
- The two-ball is derived from the triangulation by `hpBall_of_triangulated`, which never reads p's rotation.

**Non-vacuity:** `Icosahedron.theorem_HP_icosahedron`.

**Checks.**
- `check.sh` passes.
- `#print axioms` lists propext, Classical.choice and Quot.sound only.
- No `sorry`, `admit` or `native_decide`.
- A sabotaged copy is rejected.

**Hypothesis to confirm.** `NoSeparatingTriangleAt h` is the same hypothesis the audit is reviewing for `theorem_H`. Here it excludes chords of the link at h.

**Severn.** If the audit passes this, the paper's Theorem HP can carry the compiled label, under the same two caveats as Theorem H.
