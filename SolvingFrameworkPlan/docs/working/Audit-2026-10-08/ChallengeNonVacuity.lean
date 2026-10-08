import Challenges.RStarFrameBridge
import Challenges.FourColorBridge
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameWit22

/-! Audit 2026-10-08: the frozen R* statement's hypotheses are satisfiable (by the library's
order-22 witness, transported with the bridge), so `RStarFrameChallenge.MainStatement` is not
vacuous; and the frozen four-colour statement quantifies over a non-empty class. -/

open RStarFrameBridge

theorem audit_frozen_class_nonempty : ∃ (m : ℕ) (T : RStarFrameChallenge.SphericalMap m), 0 < m ∧
    T.graph.Connected ∧ T.Triangulated ∧ (∀ x, 5 ≤ T.graph.degree x) ∧ T.NoSep ∧
    RStarFrameChallenge.DiamondFree T ∧ RStarFrameChallenge.Conf2122Free T := by
  obtain ⟨hm, hc, ht, hd, hn, hD, hC⟩ := SimpleGraph.FrameWit22.frameClass
  exact ⟨22, ofLib SimpleGraph.FrameWit22.sphericalMap, hm, hc, (triangulated_iff _).2 ht,
    fun x => (degree_eq _ x).symm ▸ hd x, (noSep_iff _).2 hn, (diamondFree_iff _).2 hD,
    (conf2122Free_iff _).2 hC⟩

theorem audit_frozen_4ct_nonempty : Nonempty (FourColorSphericalMapChallenge.SphericalMap 22) :=
  ⟨FourColorBridge.ofLib SimpleGraph.FrameWit22.sphericalMap⟩

#print axioms audit_frozen_class_nonempty
#print axioms audit_frozen_4ct_nonempty
