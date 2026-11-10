import HC2o126Rot
import C2o126Glue

/-!
# ST-125 (route (i), M4): 2.126 closed

Studio, 10 Nov. This links Opus's occurrence glue (`HC2o126_00`, `COccHC2o126_00`, `HC2o126Rot`: ST125_glue2o126,
MD5SUMS cf0a1534, copied byte-identical) to `colorable_2o126` / `colorable_mirror_2o126` (CGlueM / CGlueMerge /
C2o126Glue).

`HC2o126_00.cf` and `cf2o126` are the same literal (check_literals_c: 1 entry, 0 mismatches, mutant caught), and
`rotS` and `rot2o126` are the same literal.
-/

namespace SimpleGraph.SphericalMap
open CGlue

variable {n : ℕ}

theorem rotS_eq_rot2o126 : HC2o126_00.rotS = rot2o126 := rfl

theorem cf_eq_cf2o126 : HC2o126_00.cf = cf2o126 := rfl

/-- **2.126 is reducible in the occurrence form produced by the glue.** A walk-form occurrence of rsst003_2o126 (the
ring may fold and pinch) in a triangulation whose smaller maps are 4-colourable makes the map 4-colourable. -/
theorem colorable_of_occ_2o126 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 4 → Fin n} (h : HC2o126_00.Occ T ring int) (IH : ClaimGlue.SmallerColorable T) :
    T.graph.Colorable 4 := by
  obtain ⟨G, hO, -⟩ := HC2o126_00.configOcc htri h
  rw [← HC2o126_00.intAdjOf_eq, ← HC2o126_00.ringAdjOf_eq] at hO
  have hR := HC2o126_00.rotOccS_of_occ h
  rw [rotS_eq_rot2o126] at hR
  exact colorable_2o126 htri hO hR IH

/-- The mirror case: an occurrence in `T.mirror`. -/
theorem colorable_of_mirror_occ_2o126 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 4 → Fin n} (h : HC2o126_00.Occ T.mirror ring int) (IH : ClaimGlue.SmallerColorable T) :
    T.graph.Colorable 4 := by
  obtain ⟨G, hO, -⟩ := HC2o126_00.configOcc (mirror_triangulated htri) h
  rw [← HC2o126_00.intAdjOf_eq, ← HC2o126_00.ringAdjOf_eq] at hO
  have hR := HC2o126_00.rotOccS_of_occ h
  rw [rotS_eq_rot2o126] at hR
  exact colorable_mirror_2o126 htri hO hR IH

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.colorable_of_occ_2o126
#print axioms SimpleGraph.SphericalMap.colorable_of_mirror_occ_2o126
