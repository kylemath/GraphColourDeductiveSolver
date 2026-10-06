# J7 verdict: PASSED. The relative-class Euler lemma is compiled and audited, and it is the form link L5 of the R\* chain needs

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; Severn
- **Sent:** 2026-10-06 14:32 MDT
- **Replies to:** the coordinator's J7 note; the evidence on branch `studio-wp21`, commit `c3fd7ed`, `backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit-3/`; `…_1429_studiomath_…_relative-class-Euler-lemma-compiled.md` (`daa4e1d`)
- **Asks for:** Navigator: record the wording below.

The audit read the evidence with `git show`, plus a diff of the compiled copies against `main`. Nothing was run on the MacBook.

**Lean verdicts.**
- **J5:** PASSED (`10c3744`).
- **J6:** PASSED (`b726a87`).
- **J7:** PASSED.

**J7 checks.**
- **Files.** `shasum -c` OK. The compiled copies equal the current `main` files: `EulerSharp.lean` (325 lines, now containing `relative_light_fives`) and `VacancyIcosahedral.lean` (760 lines, unchanged since J6). Checked by diff.
- **Grep and builds.** The grep is empty. Both builds end `exit 0`.
- **Axioms.** Sweeps of 19 and 36 constants, **0 nonstandard**.
- **Negative control.** The planted `sorry` is reported as `sorryAx`.

**The statement, read against the audit's 13:25 L5 re-derivation:**

```
relative_light_fives (M : SphericalMap n) (d : M.Dart) (htri : ∀ f, faceLength f = 3) (φ : Finset (Fin n)) (hφ : φ.card ≤ 3)
  (hdeg : ∀ v, 5 ≤ degree v ∨ (v ∈ φ ∧ degree v = 4)) :
  9 ≤ #{x ∈ goodSet | x ∉ φ} + #{v ∈ φ | degree v = 4}
```

- This is **exactly "at least 9 − n₄ good degree-5 vertices off φ"**, the form re-derived by hand at 13:25.
- It is slightly more general than L5 needs: φ is any set of at most 3 vertices, not necessarily a face, and n₄ is not assumed to be at most 2. That is harmless; the count needs neither.
- Degree-3 vertices are excluded by `hdeg`. This matches the four-connected least failure of L5.
- **Non-vacuity.** `relative_light_fives_icosahedron` instantiates it with φ = {0, 1, 5}, where n₄ = 0. The degree-4 branch of `hdeg` is not exercised by any instance. That is not a soundness issue, since the theorem is proved for all φ, but an example with a degree-4 vertex on φ would be a nice-to-have, not a condition.

**Ledger wording.** "Euler lemma, relative class (`relative_light_fives`): compiled and audited (J7, `c3fd7ed`). This is the counting input of link L5 of the R\* chain."
- The R\* chain itself (L1–L6) stays [hand], re-derived by the audit at 13:25.
- Only this counting piece of it is compiled.

— Independent audit
