import RSSTKillRotCore
import RSSTD9Sound

/-!
# ST-120 B5: soundness of the rotation-respecting checkers (`checkDegPR`, `checkDegRotPR`, `checkDegHiR`)

Copies of `checkLink_sound` / `checkLinks_mem` / `checkDegP_sound` / `checkDegRotP_sound` / `checkDegHi_sound` with
`reqOfR` (= rotation test, then `reqOf`) and conclusion `KillsRot`.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

theorem checkLinkR_sound (parts : List Part) (hP : ∀ p ∈ parts, p.fanExact = true) (KL : List ConfR) (d : Nat)
    (link : List Nat) (c : LinkCert)
    (h : checkLinkPR parts KL d link c = true) (W : UWin) (hW : RealShape W) (hd : W.d = d) (hl : W.link = link)
    (hd30 : d ≤ 30) (hpos : 0 < (loHiP parts W).2) : KillsRot KL W := by
  unfold checkLinkPR at h
  simp only [Bool.and_eq_true] at h
  obtain ⟨hcode, hdfs⟩ := h
  have hvs : ∀ p ∈ c.order.map (fun v => (v, classesOf v
      ((instIn parts (tagW d link)).filter (· != .no) ++ (instOut parts (tagW d link)).filter (· != .no)))),
      5 ≤ sigmaW W p.1 ∧ sigmaW W p.1 ≤ 9 := by
    intro p hp
    obtain ⟨v, hv, rfl⟩ := List.mem_map.1 hp
    have := List.all_eq_true.1 hcode v hv
    unfold isCode at this; rw [Nat.ble_eq] at this
    exact sigmaW_range hW v this
  rcases dfs_sound _ (sigmaW W) _ _ _ _ hdfs hvs with hle | ⟨R, hR, hsat⟩
  · exfalso
    rw [sum_filter_no _ _ possI_no, sum_filter_no _ _ sureI_no] at hle
    have := hi_eq hW (by omega) parts hP
    rw [hd, hl] at this
    unfold hiSymP at this
    simp only [tagW] at this hle
    omega
  · obtain ⟨ke, hke, hR⟩ := List.mem_filterMap.1 hR
    rcases hK : KL[ke.1]? with _ | K
    · rw [hK] at hR; cases hR
    · rw [hK] at hR
      simp only at hR
      rw [← hd, ← hl] at hR
      unfold reqOfR at hR
      split_ifs at hR with hrot
      refine ⟨K, List.mem_of_getElem? hK, ke.2, ?_⟩
      unfold checkEmbRot
      rw [reqOf_sound (by omega) K.1 ke.2 R hR hsat, Bool.true_and]
      exact hrot

theorem checkLinksR_mem (parts : List Part) (KL : List ConfR) (d : Nat) :
    ∀ (ls : List (List Nat)) (cs : List LinkCert), checkLinksPR parts KL d ls cs = true →
      ∀ l ∈ ls, ∃ c, checkLinkPR parts KL d l c = true := by
  intro ls
  induction ls with
  | nil => intro _ _ l hl; simp at hl
  | cons a ls ih =>
    intro cs h l hl
    cases cs with
    | nil =>
      simp only [checkLinksPR, Bool.and_eq_true] at h
      rcases List.mem_cons.1 hl with rfl | hl
      · exact ⟨_, h.1⟩
      · exact ih [] h.2 l hl
    | cons c cs =>
      simp only [checkLinksPR, Bool.and_eq_true] at h
      rcases List.mem_cons.1 hl with rfl | hl
      · exact ⟨_, h.1⟩
      · exact ih cs h.2 l hl

theorem checkDegPR_sound (parts : List Part) (KL : List ConfR) (d : Nat) (cert : List LinkCert)
    (h : checkDegPR parts KL d cert = true) :
    ∀ W : UWin, RealShape W → W.d = d → 0 < (loHiP parts W).2 → KillsRot KL W := by
  intro W hW hd hpos
  unfold checkDegPR at h
  simp only [Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨⟨⟨hP, h5⟩, h30⟩, hl⟩ := h
  have hP' : ∀ p ∈ parts, p.fanExact = true := fun p hp => List.all_eq_true.1 hP p hp
  have hmem : W.link ∈ allWords d := by
    have := allWords_mem W.link hW.2.2.2.2.1
    rwa [hW.2.1, hd] at this
  obtain ⟨c, hc⟩ := checkLinksR_mem parts KL d _ cert hl W.link hmem
  exact checkLinkR_sound parts hP' KL d W.link c hc W hW hd rfl h30 hpos

theorem checkDegRotPR_sound (parts : List Part) (KL : List ConfR) (d : Nat) (cert : List LinkCert)
    (h : checkDegRotPR parts KL d cert = true) :
    ∀ W : UWin, RealShape W → W.d = d → isRotMin W.link = true → 0 < (loHiP parts W).2 → KillsRot KL W := by
  intro W hW hd hrot hpos
  unfold checkDegRotPR at h
  simp only [Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨⟨⟨hP, h5⟩, h30⟩, hl⟩ := h
  have hP' : ∀ p ∈ parts, p.fanExact = true := fun p hp => List.all_eq_true.1 hP p hp
  have hmem : W.link ∈ (allWords d).filter isRotMin := by
    have := allWords_mem W.link hW.2.2.2.2.1
    rw [hW.2.1, hd] at this
    exact List.mem_filter.2 ⟨this, hrot⟩
  obtain ⟨c, hc⟩ := checkLinksR_mem parts KL d _ cert hl W.link hmem
  exact checkLinkR_sound parts hP' KL d W.link c hc W hW hd rfl h30 hpos

theorem checkDegHiR_sound (parts : List Part) (KL : List ConfR) (d : Nat) (cert : List LinkCert)
    (h : checkDegHiR parts KL d cert = true) :
    ∀ W : UWin, RealShape W → W.d = d → isRotMin W.link = true → 0 < (loHiP parts W).2 → KillsRot KL W := by
  intro W hW hd hrot hpos
  unfold checkDegHiR at h
  simp only [Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨⟨⟨⟨⟨⟨hP, hws⟩, hA⟩, h9⟩, h30⟩, htab⟩, hl⟩ := h
  have hP' : ∀ p ∈ parts, p.fanExact = true := fun p hp => List.all_eq_true.1 hP p hp
  have hlen : W.link.length = W.d := hW.2.1
  have hmem : W.link ∈ linkSurv (cTab parts) d := by
    unfold linkSurv
    have hb := hiP_le_pbound hA htab hW (by omega)
    have := mem_search htab hW.2.2.2.2.1 (by omega) (by rw [hlen]; omega) hrot W.link.length [] (by simp) (by simp)
    rwa [hlen, hd] at this
  obtain ⟨c, hc⟩ := checkLinksR_mem parts KL d _ cert hl W.link hmem
  exact checkLinkR_sound parts hP' KL d W.link c hc W hW hd rfl h30 hpos

#print axioms checkDegPR_sound
#print axioms checkDegRotPR_sound
#print axioms checkDegHiR_sound

end SimpleGraph.SphericalMap.RSSTSeed
