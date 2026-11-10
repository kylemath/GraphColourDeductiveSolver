# Occurrence glue for 2.126 (route (i), M4)

Opus, 10 Nov 2026, about 21:25Z. This was requested by the Studio for `cf2o126` = rsst003.
The kc line is `rsst003_2o126 8 4 0,1,2;2,3,4;4,5,6;0,6,7 1,2,3;0,2;0,1,3;0,2`.

## Files (`glue/`, build in this order)

| module | made by | gives |
|---|---|---|
| `HC2o126_00.lean` | `gen_occ_kc.py one` (s74_leanglue, md5 9f93fcd7), unchanged | `Occ T ring int` (walk form: ring vertices may repeat), `configOcc : Occ → ∃ G, ConfigOccW T G 8 4 (ρOf ring) int intAdj ringAdj ∧ supportSize G < supportSize T`, `cf`, `intAdjOf_eq`, `ringAdjOf_eq` |
| `COccHC2o126_00.lean` | the same run, unchanged | `rot`, `rot_ok`, `rotOcc_of_occ : RotOcc T (ρOf ring) int rot`, plus the registry glue |
| `HC2o126Rot.lean` | `code/mkrotS.py` | `rotS` (the same literal as `rot2o126`), `rotS_ok` (by `decide +kernel`), `rotOccS_of_occ : RotOcc T (ρOf ring) int rotS` |

Imports are the same as the P17-P22 packs: OccToRing, MinimalFrame, DCheckR2D, DCheckTEq, DCheckMirror, DCheckOccWalk and COccBridge.

## Orientation

- The generator's `rot` has the **same orientation as `rot2o126`**; it is not the mirror.
- Its lists are cyclic shifts of yours, with different start slots:
  - I0 `R0 R1 R2 I1 I2 I3`
  - I1 `R3 R4 I2 I0 R2`
  - I2 `R5 R6 I3 I0 I1 R4`
  - I3 `I0 I2 R6 R7 R0`
- `HC2o126Rot.rotS` starts each list where `rot2o126` does (shifts I0 0, I1 4, I2 5, I3 2), so `rotS = rot2o126` by `rfl`.
- For `colorable_mirror_2o126`, apply the same lemmas to an `Occ T.mirror ring int`, using `configOcc (mirror_triangulated htri) h`.

## Checks (`checks/checks.log`)

- **Conf literal.** `check_literals_c.py` compares `cf2o126` (CGlueM.lean on origin/main) with `HC2o126_00.cf` field by field: rc 0. A mutated intAdj (I3 `[0,2]` changed to `[0,1]`) gives rc 1.
- **Rotation fields.** For every slot k, `mkrotS.py` checks in Python that the Occ field it uses, `r<a>_<(k+s) mod len>`, states `Nx T (int a) (slot S[k+1]) (slot S[k])`.
  - Identity regression: with the target set to the generated `rot`, it reproduces COccHC2o126_00's proof lines.
  - Negative test: a target with I1 in mirror order is refused.
- **No Lean here.** Nothing in this pack was compiled in this container.

## Link sketch (M4, not compiled)

```lean
theorem colorable_of_occ_2o126 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 4 → Fin n} (h : HC2o126_00.Occ T ring int) (IH : ClaimGlue.SmallerColorable T) :
    T.graph.Colorable 4 := by
  obtain ⟨G, hO, -⟩ := HC2o126_00.configOcc htri h
  rw [← HC2o126_00.intAdjOf_eq, ← HC2o126_00.ringAdjOf_eq] at hO
  exact colorable_2o126 htri hO (HC2o126_00.rotOccS_of_occ h) IH
```

`HC2o126_00.cf` and `cf2o126` are the same literal, and `rotS` and `rot2o126` are the same literal, so both unify by unfolding.
