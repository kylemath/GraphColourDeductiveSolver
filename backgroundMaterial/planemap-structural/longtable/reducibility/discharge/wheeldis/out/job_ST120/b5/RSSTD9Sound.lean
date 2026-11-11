import RSSTD9Core

/-!
# ST-127 (2): soundness of the `d ≥ 9` check (`checkDegHi`)

1. `cview_W`: under `slotSigma`, the window slot entry (`slotEntryW`, the four link letters known) shows the same
   concrete spoke view as the plain slot entry, so `entry_eq` (RSSTDeg15) carries over.
2. `hub_boundW`: at `d ≥ 9`, hub `w_i` (letter `≤ 8`) sends at most `bnd tab (winAt W.link i)` units into `u`.
3. `hiP_le_pbound`: `hi ≤ 60 − 10d + Σ_i bnd(window_i)` = `pbound` of the full link word.
4. `mem_search`: a rotation-least word with positive `pbound` is found by `search` (the prune is monotone).
5. `checkDegHi_sound`.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

theorem idx_win {W : UWin} (hd : 5 ≤ W.d) {i : Nat} (hi : i < W.d) (j : Nat) (hj : j ≤ 4) :
    W.idx i ((j : Int) - 2) = (i + W.d + j - 2) % W.d := by
  unfold UWin.idx
  have h1 : ((i + W.d + j - 2 : Nat) : Int) = ((i : Int) + ((j : Int) - 2)) + (W.d : Int) := by omega
  have h2 : ((i : Int) + ((j : Int) - 2)) % (W.d : Int) = ((i + W.d + j - 2 : Nat) : Int) % (W.d : Int) := by
    rw [h1]; exact (Int.add_emod_right _ _).symm
  rw [h2, ← Int.natCast_mod, Int.toNat_natCast]

theorem link_lt100 {W : UWin} (hW : RealShape W) (m : Nat) : W.link.getD m 9 < 100 := by
  rw [List.getD_eq_getElem?_getD]
  cases h : W.link[m]? with
  | none => simp
  | some x => have := (hW.2.2.2.2.1 x (List.mem_of_getElem? h)).2; simp; omega

theorem winAt_get {W : UWin} (hW : RealShape W) {i : Nat} (hi : i < W.d) (j : Nat) (hj : j ≤ 4) :
    (winAt W.link i).getD j 9 = W.linkL (W.idx i ((j : Int) - 2)) := by
  have hd5 := hW.1
  rw [idx_win hd5 hi j hj]
  unfold winAt winIx UWin.linkL
  rw [hW.2.1]
  interval_cases j <;> rfl

theorem winAt_hub {W : UWin} (hW : RealShape W) {i : Nat} (hi : i < W.d) : (winAt W.link i).getD 2 9 = W.linkL i := by
  rw [winAt_get hW hi 2 (by norm_num)]
  congr 1
  rw [idx_win hW.1 hi 2 (by norm_num)]
  rw [show i + W.d + 2 - 2 = i + W.d by omega, Nat.add_mod_right, Nat.mod_eq_of_lt hi]

theorem cview_W {W : UWin} (hW : RealShape W) {i : Nat} (hi : i < W.d) (h5 : 5 ≤ W.linkL i) (h8 : W.linkL i ≤ 8) {t : Nat}
    (ht : t < W.linkL i) :
    cview (slotSigma W i) (slotEntry (W.linkL i) t) = cview (slotSigma W i) (slotEntryW (winAt W.link i) (W.linkL i) t) := by
  set L := W.linkL i with hL
  set σ := slotSigma W i with hσdef
  have hfix := slotSigma_fix W i
  have g : ∀ j, j ≤ 4 → σ ((winAt W.link i).getD j 9) = (winAt W.link i).getD j 9 := by
    intro j hj; apply hfix; rw [winAt_get hW hi j hj]; exact link_lt100 hW _
  by_cases t0 : t = 0
  · subst t0
    have hh : σ (slotHat 0) = (winAt W.link i).getD 4 9 := by
      rw [winAt_get hW hi 4 (by norm_num)]
      simp [σ, slotSigma, slotHat, wHatPos, UWin.letter, ← hL]
    have hr : hatRing3 L 0 = false := by simp [hatRing3]
    simp only [cview, slotEntry, slotEntryW, ite_true, hr, Bool.false_eq_true, ite_false, Option.map_some, hh, g 4 (by norm_num)]
  by_cases t1 : t = 1
  · subst t1
    have hs : σ (slotSp 1) = (winAt W.link i).getD 1 9 := by
      rw [winAt_get hW hi 1 (by norm_num)]
      simp [σ, slotSigma, slotSp, wSpokePos, UWin.letter, ← hL]
    have hh : σ (slotHat 1) = (winAt W.link i).getD 0 9 := by
      rw [winAt_get hW hi 0 (by norm_num)]
      simp [σ, slotSigma, slotHat, wHatPos, UWin.letter, ← hL]
    have hr : hatRing3 L 1 = false := by simp [hatRing3]
    simp only [cview, slotEntry, slotEntryW, show (1 : Nat) ≠ 0 by norm_num, ite_false, ite_true, hr,
      Bool.false_eq_true, Option.map_some, hs, hh, g 1 (by norm_num), g 0 (by norm_num)]
  by_cases tl : t + 1 = L
  · have hs : σ (slotSp t) = (winAt W.link i).getD 3 9 := by
      rw [winAt_get hW hi 3 (by norm_num)]
      have a1 : ¬ (100 + t < 100) := by omega
      have a2 : 100 + t < 120 := by omega
      simp only [σ, slotSigma, slotSp, a1, a2, ite_false, ite_true, show 100 + t - 100 = t by omega, ← hL]
      unfold wSpokePos; rw [if_neg t0, if_neg t1, if_pos tl]; rfl
    simp only [cview, slotEntry, slotEntryW, t0, t1, tl, ite_false, ite_true, hs, g 3 (by norm_num)]
  · simp only [slotEntry, slotEntryW, t0, t1, tl, ite_false]

theorem slotW_bound {parts : List Part} {w : List Nat} {c : Nat} (hc : slotCheckW parts w c = true) (σ : Nat → Nat)
    (hσ : ∀ x, 100 ≤ x → 5 ≤ σ x ∧ σ x ≤ 9) :
    ((slotInsW parts w).map fun x => (x.eval σ).possI).sum ≤ c := by
  unfold slotCheckW at hc
  rcases dfs_sound _ σ _ _ [] [] hc (fun p hp => by
      obtain ⟨v, hv, rfl⟩ := List.mem_map.1 hp
      have := (List.mem_filter.1 hv).2
      unfold isCode at this; rw [Nat.ble_eq] at this
      exact hσ v this) with h | ⟨R, hR, -⟩
  · rw [sum_filter_no _ _ possI_no] at h; simp at h; omega
  · simp at hR

theorem winAt_mem {W : UWin} (hW : RealShape W) (i : Nat) : winAt W.link i ∈ allWords 5 := by
  have := allWords_mem (winAt W.link i) (by
    intro x hx
    unfold winAt winIx at hx
    simp only [List.map_cons, List.map_nil, List.mem_cons, List.not_mem_nil, or_false] at hx
    have g : ∀ m, 5 ≤ W.link.getD m 9 ∧ W.link.getD m 9 ≤ 9 := by
      intro m; rw [List.getD_eq_getElem?_getD]
      cases h : W.link[m]? with
      | none => simp
      | some y => simpa using hW.2.2.2.2.1 y (List.mem_of_getElem? h)
    rcases hx with rfl | rfl | rfl | rfl | rfl <;> exact g _)
  simpa [winAt, winIx] using this

theorem hub_boundW {parts : List Part} (hA : slotAll parts = true) {tab : Array Nat} (htab : tabOK parts tab = true)
    {W : UWin} (hW : RealShape W) (hd9 : 9 ≤ W.d) {i : Nat} (hi : i < W.d) (h8 : W.linkL i ≤ 8) :
    (parts.map fun p => if p.hub = W.linkL i then
      (p.fit3At (W.viewW i) (W.linkL i - 2)).possI else 0).sum ≤ (bnd tab (winAt W.link i) : Int) := by
  have hb6 := hub_bound hA hW hd9 hi h8
  have hmem := winAt_mem hW i
  have hent := List.all_eq_true.1 htab _ hmem
  have hw2 := winAt_hub hW hi
  simp only at hent
  rw [if_pos (by rw [hw2]; exact h8)] at hent
  unfold bnd
  rw [Nat.cast_min]
  rcases Bool.or_eq_true_iff.1 hent with h6 | hchk
  · rw [Nat.ble_eq] at h6
    exact le_min (by exact_mod_cast hb6) (le_trans hb6 (by exact_mod_cast h6))
  · refine le_min (by exact_mod_cast hb6) ?_
    have h5 : 5 ≤ W.linkL i := by
      have hm : W.link[i]? = some (W.linkL i) := by
        have hlt : i < W.link.length := by rw [hW.2.1]; exact hi
        unfold UWin.linkL; rw [getD_lt' _ _ _ hlt]; exact List.getElem?_eq_getElem hlt
      exact (hW.2.2.2.2.1 _ (List.mem_of_getElem? hm)).1
    have hA' := hA
    simp only [Bool.and_eq_true, slotAll] at hA'
    obtain ⟨⟨⟨⟨⟨-, -⟩, -⟩, -⟩, hfe⟩, hws⟩ := hA'
    have key := slotW_bound hchk (slotSigma W i) (slotSigma_range hW i)
    refine le_trans (le_of_eq ?_) key
    unfold slotInsW
    rw [List.map_map, sum_map_filter, hw2]
    congr 1
    apply List.map_congr_left
    intro p hp
    by_cases hh : p.hub = W.linkL i
    · have hpe := List.all_eq_true.1 hfe p hp
      have hgood := (wellShaped_spec (List.all_eq_true.1 hws p hp)).2.2.2.2.2
      simp only [hh, beq_self_eq_true, ite_true, Function.comp]
      rw [symFit_eval (slotSigma_fix W i) p hpe]
      congr 1
      apply fit3At_congr
      · simp only [UWin.viewW, slotViewW, hw2, List.length_map, List.length_range]
      · intro t h1 _ s hs
        have ht : t < W.linkL i := by simpa [UWin.viewW] using h1
        rw [entry_eq hW hd9 hi h5 h8 ht s (hgood s hs), cview_W hW hi h5 h8 ht]
        simp only [slotViewW, hw2, List.getElem_map, List.getElem_range]
    · have : (p.hub == W.linkL i) = false := by simpa using hh
      simp [hh, this]

theorem winIx_lt {d : Nat} (hd : 0 < d) (i : Nat) : (winIx d i).all (· < d) = true := by
  unfold winIx; simp only [List.map_cons, List.map_nil, List.all_cons, List.all_nil, Bool.and_true,
    Bool.and_eq_true, decide_eq_true_eq]
  exact ⟨Nat.mod_lt _ hd, Nat.mod_lt _ hd, Nat.mod_lt _ hd, Nat.mod_lt _ hd, Nat.mod_lt _ hd⟩

theorem pb_full (tab : Array Nat) {L : List Nat} (hd : 0 < L.length) (i : Nat) :
    pb tab L.length L i = bnd tab (winAt L i) := by
  unfold pb winAt; rw [if_pos (winIx_lt hd i)]

/-- `hi ≤ 60 − 10d + Σ_i bnd(window_i)` at `d ≥ 9`. -/
theorem hiP_le_pbound {parts : List Part} (hA : slotAll parts = true) {tab : Array Nat}
    (htab : tabOK parts tab = true) {W : UWin} (hW : RealShape W) (hd9 : 9 ≤ W.d) :
    (loHiP parts W).2 ≤ pbound tab W.d W.link := by
  rw [loHiP_eq]
  show 10 * (6 - (W.d : Int)) + inX parts W Tri.possI - outX parts W Tri.sureI ≤ _
  have hout : outX parts W Tri.sureI = 0 := by unfold outX; rw [if_neg (by omega)]
  have hlen : W.link.length = W.d := hW.2.1
  have hin : inX parts W Tri.possI ≤ ((List.range W.d).map fun i => (pb tab W.d W.link i : Int)).sum := by
    unfold inX
    apply List.sum_le_sum
    intro i hi
    have hi' := List.mem_range.1 hi
    have hpb : pb tab W.d W.link i = bnd tab (winAt W.link i) := by
      rw [← hlen]; exact pb_full tab (by omega) i
    rw [hpb]
    split_ifs with h8
    · exact hub_boundW hA htab hW hd9 hi' h8
    · positivity
  unfold pbound
  rw [hout]; linarith

theorem getD_take {L : List Nat} {k x : Nat} (hx : x < k) : (L.take k).getD x 9 = L.getD x 9 := by
  simp only [List.getD_eq_getElem?_getD, List.getElem?_take, if_pos hx]

theorem pb_mono {parts : List Part} {tab : Array Nat} (htab : tabOK parts tab = true) {L : List Nat}
    (hlet : ∀ x ∈ L, 5 ≤ x ∧ x ≤ 9) (hd : 0 < L.length) (k i : Nat) :
    pb tab L.length L i ≤ pb tab L.length (L.take k) i := by
  rw [pb_full tab hd]
  have hbnd6 : ∀ w, bnd tab w ≤ 6 := fun w => Nat.min_le_left _ _
  unfold pb
  split_ifs with h1 h2
  · apply le_of_eq; congr 1
    unfold winAt
    apply List.map_congr_left
    intro x hx
    rw [getD_take]
    have := List.all_eq_true.1 h1 x hx
    simp at this; exact this.1
  · -- a 9+ hub: its table entry is 0
    obtain ⟨hik, h9⟩ := h2
    have hik' : i < k := by simp at hik; omega
    rw [getD_take hik'] at h9
    have hw : winAt L i ∈ allWords 5 := by
      have := allWords_mem (winAt L i) (by
        intro y hy
        unfold winAt winIx at hy
        simp only [List.map_cons, List.map_nil, List.mem_cons, List.not_mem_nil, or_false] at hy
        have g : ∀ m, 5 ≤ L.getD m 9 ∧ L.getD m 9 ≤ 9 := by
          intro m; rw [List.getD_eq_getElem?_getD]
          cases h : L[m]? with
          | none => simp
          | some z => simpa using hlet z (List.mem_of_getElem? h)
        rcases hy with rfl | rfl | rfl | rfl | rfl <;> exact g _)
      simpa [winAt, winIx] using this
    have hent := List.all_eq_true.1 htab _ hw
    have hil : i < L.length := by simp at hik; omega
    have h2' : (winAt L i).getD 2 9 = 9 := by
      unfold winAt winIx
      simp only [List.map_cons, List.map_nil]
      show L.getD ((i + L.length + 2 - 2) % L.length) 9 = 9
      rw [show i + L.length + 2 - 2 = i + L.length by omega, Nat.add_mod_right, Nat.mod_eq_of_lt hil]; exact h9
    simp only [h2', show ¬ (9 ≤ 8) by norm_num, ite_false, beq_iff_eq] at hent
    unfold bnd; rw [hent]; simp
  · exact hbnd6 _

theorem mem_search {parts : List Part} {tab : Array Nat} (htab : tabOK parts tab = true) {L : List Nat}
    (hlet : ∀ x ∈ L, 5 ≤ x ∧ x ≤ 9) (hd : 0 < L.length) (hpos : 0 < pbound tab L.length L) (hrot : isRotMin L = true) :
    ∀ f P, P.length + f = L.length → P = L.take P.length → L ∈ search tab L.length f P := by
  intro f
  induction f with
  | zero =>
    intro P hl hP
    rw [search]
    have hPL : P = L := by rw [hP, show P.length = L.length by omega, List.take_length]
    subst hPL
    rw [if_neg (by omega)]
    simp [hrot]
  | succ f ih =>
    intro P hl hP
    rw [search]
    have hge : pbound tab L.length L ≤ pbound tab L.length P := by
      unfold pbound
      have : ∀ i ∈ List.range L.length, (pb tab L.length L i : Int) ≤ (pb tab L.length P i : Int) := by
        intro i _; rw [hP]; exact_mod_cast pb_mono htab hlet hd _ i
      linarith [List.sum_le_sum this]
    rw [if_neg (by omega)]
    simp only [List.mem_flatMap]
    have hk : P.length < L.length := by omega
    refine ⟨L[P.length], ?_, ih _ (by simp; omega) ?_⟩
    · have := hlet _ (List.getElem_mem hk); simp; omega
    · have e1 : L.take (P.length + 1) = L.take P.length ++ [L[P.length]] := by
        rw [List.take_succ, List.getElem?_eq_getElem hk]; rfl
      rw [List.length_append, List.length_singleton, e1, ← hP]

/-- **B5 for one degree `d ≥ 9`**, any part list (checked by `checkDegHi`), rotation-least words. -/
theorem checkDegHi_sound (parts : List Part) (KL : List Conf) (d : Nat) (cert : List LinkCert)
    (h : checkDegHi parts KL d cert = true) :
    ∀ W : UWin, RealShape W → W.d = d → isRotMin W.link = true → 0 < (loHiP parts W).2 → Kills KL W := by
  intro W hW hd hrot hpos
  unfold checkDegHi at h
  simp only [Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨⟨⟨⟨⟨⟨hP, hws⟩, hA⟩, h9⟩, h30⟩, htab⟩, hl⟩ := h
  have hP' : ∀ p ∈ parts, p.fanExact = true := fun p hp => List.all_eq_true.1 hP p hp
  have hlen : W.link.length = W.d := hW.2.1
  have hb := hiP_le_pbound hA htab hW (by omega)
  have hmem : W.link ∈ linkSurv (cTab parts) d := by
    unfold linkSurv
    have := mem_search htab hW.2.2.2.2.1 (by omega) (by rw [hlen]; omega) hrot W.link.length [] (by simp) (by simp)
    rwa [hlen, hd] at this
  obtain ⟨c, hc⟩ := checkLinks_mem parts KL d _ cert hl W.link hmem
  exact checkLink_sound parts hP' KL d W.link c hc W hW hd rfl h30 hpos

#print axioms checkDegHi_sound

end SimpleGraph.SphericalMap.RSSTSeed
