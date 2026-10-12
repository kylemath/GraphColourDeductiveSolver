import Challenges.FourColorSphericalMapChallenge
import Challenges.RStarFrameBridge

/-!
# Anti-drift bridge for the four-colour challenge

* `mainStatement_iff`: `FourColorSphericalMapChallenge.MainStatement` is the statement
  `∀ n (M : SimpleGraph.SphericalMap n), M.graph.Colorable 4` about the project's maps.
* `mainStatement_of_RStarFrame`: the project's `four_color_of_RStarFrame` proves
  `RStarFrame → MainStatement`.
* `mainStatement_of_rStarFrameChallenge`: the frozen R\* challenge implies the frozen
  four-colour challenge.
-/

namespace FourColorBridge

open SimpleGraph SimpleGraph.SphericalMap

variable {n : ℕ}

theorem fills_toLib {G : SimpleGraph (Fin n)}
    (R : FourColorSphericalMapChallenge.RotationSystem G) (h : R.Fills) :
    (⟨R.next, R.next_fst, R.cyclic⟩ : SimpleGraph.RotationSystem G).Fills := by
  intro φ hφ
  obtain ⟨c, hinv, hc⟩ := h φ hφ
  have key : ∀ d e, (⟨R.next, R.next_fst, R.cyclic⟩ : SimpleGraph.RotationSystem G).FaceRelation
      d e → c d = c e := by
    intro d e hde
    induction hde with
    | refl => rfl
    | step d => exact (hinv d).symm
    | symm _ ih => exact ih.symm
    | trans _ _ ih1 ih2 => exact ih1.trans ih2
  refine ⟨fun f => Sum.elim (Quotient.lift c (fun a b hab => key a b hab))
    (fun _ => (0 : ZMod 2)) f, ?_⟩
  intro d
  exact hc d

theorem fills_ofLib {G : SimpleGraph (Fin n)} (R : SimpleGraph.RotationSystem G)
    (h : R.Fills) :
    (⟨R.next, R.next_fst, R.cyclic⟩ : FourColorSphericalMapChallenge.RotationSystem G).Fills := by
  intro φ hφ
  obtain ⟨c, hc⟩ := h φ hφ
  exact ⟨fun d => c (R.faceOf d), fun d => congrArg c (R.face_of_face_next d), fun d => hc d⟩

/-- Challenge map to library map (same graph, same rotation). -/
def toLib (M : FourColorSphericalMapChallenge.SphericalMap n) : SimpleGraph.SphericalMap n :=
  ⟨M.graph, ⟨M.rotation.next, M.rotation.next_fst, M.rotation.cyclic⟩,
    fills_toLib _ M.fills⟩

/-- Library map to challenge map (same graph, same rotation). -/
def ofLib (M : SimpleGraph.SphericalMap n) : FourColorSphericalMapChallenge.SphericalMap n :=
  ⟨M.graph, ⟨M.rotation.next, M.rotation.next_fst, M.rotation.cyclic⟩,
    fills_ofLib _ M.fills⟩

/-- **Anti-drift check.** The frozen statement is four-colourability of the project's maps. -/
theorem mainStatement_iff : FourColorSphericalMapChallenge.MainStatement ↔
    ∀ (n : ℕ) (M : SimpleGraph.SphericalMap n), M.graph.Colorable 4 :=
  ⟨fun H n M => H n (ofLib M), fun H n M => H n (toLib M)⟩

/-- **`RStarFrame` implies the frozen four-colour statement.** -/
theorem mainStatement_of_RStarFrame (hR : RStarFrame) :
    FourColorSphericalMapChallenge.MainStatement :=
  mainStatement_iff.2 fun _ M => four_color_of_RStarFrame hR M

/-- The frozen R\* challenge implies the frozen four-colour challenge. -/
theorem mainStatement_of_rStarFrameChallenge (h : RStarFrameChallenge.MainStatement) :
    FourColorSphericalMapChallenge.MainStatement :=
  mainStatement_of_RStarFrame (RStarFrameBridge.mainStatement_iff.1 h)

end FourColorBridge

#print axioms FourColorBridge.mainStatement_iff
#print axioms FourColorBridge.mainStatement_of_RStarFrame
#print axioms FourColorBridge.mainStatement_of_rStarFrameChallenge
