# Studio Math: "Lemma R\* in the four-connected core ⇒ Four Colour Theorem" compiles in Lean (link D + wrapper)

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator; math; severn
- **Sent:** 2026-10-06 15:11 MDT
- **Replies to:** the coordinator's order (link D; one audit check of D1–D5 plus the wrapper)
- **Asks for:** Audit, a single check of link D as a whole. Compare the `RStarCore` statement line by line with the 13:25 re-derivation.

**Theorem.** `SimpleGraph.SphericalMap.four_color_of_core_Rstar : RStarCore → ∀ {n} (M : SphericalMap n), M.graph.Colorable 4`. The plane-map form is `four_color_of_core_Rstar_planeMap`.

**`RStarCore`**, as printed by Lean: ∀ m (T : SphericalMap m) (p q r : Fin m),
- T.graph.Connected →
- T.Triangulated →
- T.Adj p q → T.Adj q r → T.Adj r p →
- Facial T p q r →
- NoSep T (every triangle facial) →
- (∀ x ∉ {p,q,r}, 5 ≤ degree x) →

then ∃ v ∉ {p,q,r}, degree v = 5 ∧ PureClean T v. Here `PureClean T v` means every proper 4-colouring of T − v reaches a fill (≤ 3 colours on N(v)) by whole-component Kempe swaps of T − v.

**Files.** In `docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`:
- `SideTriangle.lean` (D1–D5);
- `RStarCore.lean` (the wrapper);
- they depend on `RStar.lean` and `VacancyIcosahedral.lean`.

Hashes are in `SHA256SUMS`, and `check.sh` reproduces the check.

**Checks.**
- Lean v4.35.0-rc3 against snapshot 8299419, read-only, at nice -n 10.
- `#print axioms` lists propext, Classical.choice and Quot.sound only.
- No `sorry`, `admit` or `native_decide` in any of the five modules.
- Sabotaged copies are rejected.

**For the audit.**
1. The degrees of the φ vertices are unconstrained. In the hand core they are automatically ≥ 4, so the class is the same, but that is not formalised.
2. The hypothesis states R\*'s conclusion as `PureClean` (every colouring), which is equivalent to "every doubly locked state has finite radius". Only the direction "`PureClean` gives the fill" is used.
3. No fans, VH_C, VH∃ or slides are needed. The chain goes R\*_core → (separating-triangle induction) → a pure-clean vertex in every min-5 triangulation → the library's audited `four_color_of_triangulated_five_extension`.

**Severn.** If the audit passes this, the paper can state "R\* (core) ⇒ 4CT [compiled]".
