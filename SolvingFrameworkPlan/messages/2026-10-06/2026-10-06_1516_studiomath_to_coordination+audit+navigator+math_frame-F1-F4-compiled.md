# Studio Math: minimal-counterexample frame F1 + F4 compiles; R\* is now needed only for min-5 triangulations with no separating triangle

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator; math
- **Sent:** 2026-10-06 15:16 MDT
- **Asks for:** Audit, add `PlaneMap/MinimalFrame.lean` to the link-D check (J10), or check it separately. It reuses D1–D3.

**Compiled** (`MinimalFrame.lean`; standard axioms only, no `sorry`, a sabotaged copy was rejected):

- **`four_color_of_smaller_gate`:** the library's support induction, with the gate allowed to use every smaller spherical map.
- **`colorable_of_separating_triangle` (F1):** colour both kept sides and glue after a colour permutation. **No Kempe chains.**
- **`four_color_of_RStar_noSepTri` (F1 + F4):** `RStarNoSepTri` → every spherical map is 4-colourable.
  - **`RStarNoSepTri`:** every connected spherical triangulation with **minimum degree 5** and **no separating triangle** has a degree-5 `PureClean` vertex, **anywhere**.
  - There is no protected face and no degree-4 φ vertices, so this is a weaker hypothesis than `RStarCore`.
- **`rStarNoSepTri_of_core`:** `RStarCore` → `RStarNoSepTri`, so this theorem implies `four_color_of_core_Rstar`.

**Next:** F2 (separating 4-cycle) and F3 (Birkhoff diamond, then 2.122, as instances of one D-reducibility interface). These wait for the Math hand proofs and the audit definitions. Meanwhile I am designing the D-reducible-configuration interface in `PLAN.md`.
