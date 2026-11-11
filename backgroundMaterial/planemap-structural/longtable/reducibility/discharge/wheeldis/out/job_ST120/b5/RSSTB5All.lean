import RSSTDeg56K768
import RSSTDeg7
import RSSTDeg8
import RSSTDegHi
import RSSTDeg15

/-!
# ST-127: B5 assembled — 79 parts (71 + N2), kill list K768 (582 proved + 2.126 + 185 substitutes)

Every real-shaped word whose link word is rotation-least and whose `hi` (B4's `loHiP rsstParts79`) is positive has a
K768 configuration embedded; with `seed_of_B5_79` (RSSTRot) every `Internally6` triangulation has a vertex whose word
contains one. Degrees: 5, 6 (`checkDegP`, all words), 7, 8 (`checkDegRotP`), 9..14 (`checkDegHi`), ≥ 15 (`B5_ge15_79`).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap

theorem B5_79 : ∀ W : UWin, RealShape W → isRotMin W.link = true → 0 < (loHiP rsstParts79 W).2 → Kills k768 W := by
  intro W hW hrot hpos
  have h5 := hW.1
  by_cases h15 : 15 ≤ W.d
  · exact B5_ge15_79 k768 W hW h15 hpos
  interval_cases hd : W.d
  · exact checkDegP_sound rsstParts79 k768 5 cert5 deg5_check79_768 W hW hd hpos
  · exact checkDegP_sound rsstParts79 k768 6 cert6 deg6_check79_768 W hW hd hpos
  · exact B5_deg7_rot W hW hd hrot hpos
  · exact B5_deg8_rot W hW hd hrot hpos
  · exact B5_deg9_rot W hW hd hrot hpos
  · exact B5_deg10_rot W hW hd hrot hpos
  · exact B5_deg11_rot W hW hd hrot hpos
  · exact B5_deg12_rot W hW hd hrot hpos
  · exact B5_deg13_rot W hW hd hrot hpos
  · exact B5_deg14_rot W hW hd hrot hpos

/-- **The RSST seed (B5 into B4)**: every `Internally6` triangulation has a vertex `u` and a link listing `w` whose
window word contains a configuration of K768. -/
theorem seed_79 {n : ℕ} {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) :
    ∃ u w, IsLink T u (T.graph.degree u) w ∧ Kills k768 (wordOf T u w) :=
  seed_of_B5_79 hT (Kills k768) B5_79

#print axioms B5_79
#print axioms seed_79

end SimpleGraph.SphericalMap.RSSTSeed
