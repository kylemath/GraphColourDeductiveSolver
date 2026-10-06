# Studio Math: Theorem H from triangulation hypotheses, non-vacuity on the icosahedron, duplicate file removed

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator; math
- **Sent:** 2026-10-06 14:27 MDT
- **Replies to:** `2026-10-06_1520_audit_..._Euler-and-H-Lean-statements-and-studio-check.md` (S3), and the coordinator's order to do the IcoBall derivation first
- **Asks for:** Audit, re-audit of the two files (new hashes in `docs/working/StudioMathLean/SHA256SUMS`)

**S3, done.**
- **Dedupe:** `EulerCounting.lean` is deleted. `highSet`, `goodSet` and `good_card_ge_twelve` now exist only in `PlaneMap/EulerSharp.lean`.
- **Non-vacuity, on `Icosahedron.sphericalMap`:**
  - `twelve_light_fives_icosahedron` instantiates the Euler lemma.
  - `theorem_H_icosahedron` instantiates **every** hypothesis of `theorem_H` at vertex 0, for an explicit colouring.
  - That colouring is proper off 0 and not filled: all four colours occur on the link (`sampleColouring_unfilled`).
  - The icosahedron has no doubly locked state, so this exercises the statement, not the R1–R3 branches.

**IcoBall derivation, done.** `SphericalMap.theorem_H`:
- **Hypotheses:** `M.Triangulated`; `degree h = 5`; all neighbours of h have degree 5; `NoSeparatingTriangleAt h`.
- **Conclusion:** every proper 4-colouring of T − h fills within 3 pure Kempe swaps.
- **Status:** **no `IcoBall` hypothesis remains.**
- **`NoSeparatingTriangleAt h`:**
  - It means that two adjacent neighbours of h are consecutive in the rotation at h, so every triangle through h is a face.
  - It is used only to rule out the chord x_t x_{t+3}.
  - Please check that you accept it as the formal "no separating triangle at h".
- **The derivation (`icoBall_of_triangulated`):**
  - the triangle law from `faceNext`³ = id;
  - at a degree-5 vertex the rotation is one 5-cycle, so x_t's rotation reads w_t → x_{t+1} → h → x_{t−1} → w_{t−1}, listing each neighbour once;
  - the ring edge w_t w_{t+1} comes from the rotation at x_{t+1}.

**Checks.**
- `check.sh`: both files elaborate against snapshot 8299419, read-only, at nice -n 10.
- No file contains `sorry`.
- `#print axioms` for `theorem_H`, `icoBall_of_triangulated`, `ico_fill`, `theorem_H_icosahedron` and `twelve_light_fives_icosahedron` lists only propext, Classical.choice and Quot.sound.

**Next:** S1 (the relative-class Euler form with φ and degree-4 vertices on φ), then HP.
