import RSSTOrient
import RSSTTri

/-!
# ST-120 B4 M2: the bridge from a real window to B2's `UWin` / `HubView`

Studio, 10 Nov. For a vertex `u` of `T` with a link listing `w` (`IsLink`), `wordOf T u w : UWin` is the word read off
`T` (letters `min deg 9`), drawn as in spec §2 / §6:
* `link[i] = letter w_i`, `apex[i] = letter s_i` (`s_i = apexV T w i`);
* `priv[i]`: for `deg w_i ≤ 8` the letters of `rot(w_i)[3..D-3]` (the privates, from the `s_{i-1}` side); for a 9+ link
  vertex `[letter y_i, 9, letter x_i]` with `y_i = rot(w_i)[3]`, `x_i = rot(w_i)[D-3]` and the drawn middle held at 9+
  (spec §6; it is never read at a constrained position).

The real hub view (`realView T h y`, the spec's §3.3 read on `T` itself): spoke `t` is `x = rot(h)[t]` counted from the
anchor `y`; its hat is `rot(x)[2]` and its fans are `rot(x)[3..deg x - 3]`, both read in `rot(x)` from `h` (in `rot(x)`
the order is `h, S[t-1], hat, fans…`, M1 / `nx_tri`).

**M2 main lemmas** (`approxU`, `approxW`): every spoke view B2 builds from the word (`UWin.viewU`, `UWin.viewW` at a hub
`w_i` with `deg ≤ 8`) *approximates* the real spoke view at the same rotation index (`Approx`, RSSTTri): the spoke letter
is right, the hat is unknown (ring 3) or right, and the fans are pointwise unknown (ring 3) or right, except that nothing
is claimed for the fans of a 9+ spoke (those are where the drawn middle sits; no part reads them, RSSTTri `Sub.Good`).
This is the precise form of "every position B2 reads denotes the intended real vertex with the right letter"; the
per-position facts are the `letter_*` / `seg_*` lemmas below. Ring-3 positions are `none` in B2 and are left unknown.
`rsst_parts_local` is not needed for soundness (it is what makes the hub-`w_i` fits OPEN-free).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap

variable {n : ℕ}

/-- The letter of a vertex: its degree, with 9 for 9+ (spec §2). -/
noncomputable def letterOf (T : SphericalMap n) (v : Fin n) : ℕ := min (T.graph.degree v) 9

/-- The drawn privates of `w_i` (spec §2, §6). -/
noncomputable def privL (T : SphericalMap n) (u : Fin n) (w : ℕ → Fin n) (i : ℕ) : List ℕ :=
  if T.graph.degree (w i) ≤ 8 then
    (List.range (T.graph.degree (w i) - 5)).map fun k => letterOf T (rotNbr T (w i) u (3 + k))
  else [letterOf T (rotNbr T (w i) u 3), 9, letterOf T (rotNbr T (w i) u (T.graph.degree (w i) - 3))]

/-- **The word of `u`** read off `T` along the link listing `w`. -/
noncomputable def wordOf (T : SphericalMap n) (u : Fin n) (w : ℕ → Fin n) : UWin where
  d := T.graph.degree u
  link := (List.range (T.graph.degree u)).map fun i => letterOf T (w i)
  apex := (List.range (T.graph.degree u)).map fun i => letterOf T (apexV T w i)
  priv := (List.range (T.graph.degree u)).map fun i => privL T u w i

/-- The real view of spoke `x` from hub `h` (spec §3.3 on `T`). -/
noncomputable def realSpoke (T : SphericalMap n) (h x : Fin n) : SpokeView where
  spoke := letterOf T x
  hat := letterOf T (rotNbr T x h 2)
  fans := (List.range (T.graph.degree x - 5)).map fun k => letterOf T (rotNbr T x h (3 + k))

/-- The real hub view of `h` from anchor `y` (`rot(h)` read with `T.rotation.next` from `y`). -/
noncomputable def realView (T : SphericalMap n) (h y : Fin n) : HubView :=
  (List.range (T.graph.degree h)).map fun t => realSpoke T h (rotNbr T h y t)

/-! ## Letters -/

section
variable {T : SphericalMap n}

theorem letterOf_le8 {x : Fin n} (h : T.graph.degree x ≤ 8) : letterOf T x = T.graph.degree x :=
  min_eq_left (by omega)

theorem letterOf_ge9 {x : Fin n} (h : 9 ≤ T.graph.degree x) : letterOf T x = 9 := min_eq_right h

theorem npriv_le8 {D : ℕ} (h5 : 5 ≤ D) (h : D ≤ 8) : npriv D = D - 5 := by
  unfold npriv; split_ifs <;> omega

theorem letterOf_eq9 {x : Fin n} (h : ¬ T.graph.degree x ≤ 8) : letterOf T x = 9 := letterOf_ge9 (by omega)

/-- The general form of a spoke approximation. -/
theorem approx_mk {h x : Fin n} {sp : ℕ} {H : Option ℕ} {N : ℕ} {F : ℕ → Option ℕ}
    (hs : sp = letterOf T x) (hh : H = none ∨ H = some (letterOf T (rotNbr T x h 2)))
    (hf : letterOf T x = 9 ∨ (N = T.graph.degree x - 5 ∧
      ∀ k, k < N → F k = none ∨ F k = some (letterOf T (rotNbr T x h (3 + k))))) :
    Approx ⟨sp, H, (List.range N).map F⟩ (realSpoke T h x) := by
  refine ⟨hs, hh, ?_⟩
  rcases hf with h9 | ⟨hN, hF⟩
  · exact Or.inl h9
  · refine Or.inr ⟨by simp [realSpoke, hN], fun k z hz => ?_⟩
    simp only [realSpoke, List.getElem?_map] at hz
    have hk : k < T.graph.degree x - 5 := by
      by_contra hk; rw [List.getElem?_eq_none (by simp; omega)] at hz; simp at hz
    rw [List.getElem?_range hk] at hz
    simp only [Option.map_some, Option.some.injEq] at hz
    simp only [List.getElem?_map, List.getElem?_range (show k < N by omega), Option.map_some, Option.some.injEq]
    rcases hF k (by omega) with e | e
    · exact Or.inl e
    · exact Or.inr (by rw [e, hz])

/-- Fans that are all unknown. -/
theorem approx_unknown_fans {h x : Fin n} (hx5 : 5 ≤ T.graph.degree x) {sp : ℕ} {H : Option ℕ}
    (hs : sp = letterOf T x) (hh : H = none ∨ H = some (letterOf T (rotNbr T x h 2))) :
    Approx ⟨sp, H, (List.range (npriv sp)).map fun _ => none⟩ (realSpoke T h x) := by
  refine approx_mk hs hh ?_
  by_cases hD : T.graph.degree x ≤ 8
  · right
    refine ⟨by rw [hs, letterOf_le8 hD, npriv_le8 hx5 hD], fun k _ => Or.inl rfl⟩
  · left; exact letterOf_eq9 hD

end

/-! ## The word's accessors -/

section
variable {T : SphericalMap n} {u : Fin n} {d : ℕ} {w : ℕ → Fin n}

theorem word_d (hL : IsLink T u d w) : (wordOf T u w).d = d := hL.deg

theorem word_linkL (hL : IsLink T u d w) {m : ℕ} (hm : m < d) : (wordOf T u w).linkL m = letterOf T (w m) := by
  simp [UWin.linkL, wordOf, List.getD_eq_getElem?_getD, hL.deg, hm]

theorem word_apexL (hL : IsLink T u d w) {m : ℕ} (hm : m < d) :
    (wordOf T u w).apexL m = letterOf T (apexV T w m) := by
  simp [UWin.apexL, wordOf, List.getD_eq_getElem?_getD, hL.deg, hm]

theorem word_priv (hL : IsLink T u d w) {m : ℕ} (hm : m < d) : (wordOf T u w).priv.getD m [] = privL T u w m := by
  simp [wordOf, List.getD_eq_getElem?_getD, hL.deg, hm]

theorem apexV_mod (hL : IsLink T u d w) (i : ℕ) : apexV T w (i % d) = apexV T w i := by
  unfold apexV
  have e : w (i % d + 1) = w (i + 1) := by rw [← hL.per_mod (i % d + 1), ← succ_mod_mod, hL.per_mod]
  rw [hL.per_mod, e]

theorem idx_of (hL : IsLink T u d w) (b : ℕ) (δ : ℤ) (k : ℕ) (c : ℤ) (h : (k : ℤ) = b + δ + d * c) :
    (wordOf T u w).idx b δ = k % d := by
  unfold UWin.idx
  rw [word_d hL]
  have : ((b : ℤ) + δ) % (d : ℤ) = (k : ℤ) % (d : ℤ) := by rw [h, Int.add_mul_emod_self_left]
  rw [this, ← Int.natCast_mod, Int.toNat_natCast]

theorem letter_u (b : ℕ) : (wordOf T u w).letter b .u = some (letterOf T u) := rfl

theorem letter_w (hL : IsLink T u d w) (hd : 0 < d) (b : ℕ) (δ : ℤ) (k : ℕ) (c : ℤ)
    (h : (k : ℤ) = b + δ + d * c) : (wordOf T u w).letter b (.w δ) = some (letterOf T (w k)) := by
  show some ((wordOf T u w).linkL ((wordOf T u w).idx b δ)) = _
  rw [idx_of hL b δ k c h, word_linkL hL (Nat.mod_lt _ hd), hL.per_mod]

theorem letter_seg (hL : IsLink T u d w) (b : ℕ) (δ : ℤ) (k : ℕ) (c : ℤ)
    (h : (k : ℤ) = b + δ + d * c) (j : ℕ) :
    (wordOf T u w).letter b (.seg δ j) = ((wordOf T u w).segL (k % d))[j]? := by
  show ((wordOf T u w).segL ((wordOf T u w).idx b δ))[j]? = _
  rw [idx_of hL b δ k c h]

theorem letter_segR (hL : IsLink T u d w) (b : ℕ) (δ : ℤ) (k : ℕ) (c : ℤ)
    (h : (k : ℤ) = b + δ + d * c) (j : ℕ) :
    (wordOf T u w).letter b (.segR δ j) =
      (let s := (wordOf T u w).segL (k % d); if j < s.length then s[s.length - 1 - j]? else none) := by
  show (let s := (wordOf T u w).segL ((wordOf T u w).idx b δ); if j < s.length then s[s.length - 1 - j]? else none) = _
  rw [idx_of hL b δ k c h]

variable (hT : ClaimGlue.Internally6 T) (hL : IsLink T u d w)
include hT hL

theorem rot2_eq (k : ℕ) : rotNbr T (w k) u 2 = apexV T w (k + d - 1) := by
  have d5 := hL.d5 hT
  have := (window_oriented hT hL).at2 (k + d - 1)
  rwa [show k + d - 1 + 1 = k + d by omega, hL.per] at this

/-- **seg of an exact link vertex**: `seg_k = rot(w_k)[2..D-2]` (`s_{k-1}`, the privates, `s_k`). -/
theorem segL_exact (k : ℕ) (hD : T.graph.degree (w k) ≤ 8) :
    (wordOf T u w).segL (k % d) =
      (List.range (T.graph.degree (w k) - 3)).map fun j => letterOf T (rotNbr T (w k) u (2 + j)) := by
  have d5 := hL.d5 hT
  have hd : 0 < d := by omega
  have hm := Nat.mod_lt k hd
  have h5 := hT.minDeg (w k)
  have O := window_oriented hT hL
  unfold UWin.segL
  rw [word_d hL, word_linkL hL hm, word_priv hL hm, word_apexL hL hm, word_apexL hL (Nat.mod_lt _ hd),
    show (k % d + d - 1) % d = (k + d - 1) % d by
      rw [show k % d + d - 1 = (k % d + (d - 1)) by omega, show k + d - 1 = k + (d - 1) by omega, Nat.add_mod,
        Nat.mod_mod, ← Nat.add_mod],
    apexV_mod hL, apexV_mod hL, hL.per_mod, letterOf_le8 hD, npriv_le8 h5 hD, ← rot2_eq hT hL, ← O.atL2 k]
  unfold privL
  rw [hL.per_mod, if_pos hD, List.take_of_length_le (by simp)]
  obtain ⟨D', hD'⟩ : ∃ D', T.graph.degree (w k) = D' + 5 := ⟨T.graph.degree (w k) - 5, by omega⟩
  rw [hD', show D' + 5 - 3 = (D' + 1) + 1 by omega, show D' + 5 - 5 = D' by omega,
    show D' + 5 - 2 = 2 + (D' + 1) by omega, List.range_succ, List.range_succ_eq_map]
  simp only [List.map_append, List.map_cons, List.map_map, List.map_nil, List.singleton_append, List.cons_append,
    Nat.add_zero]
  congr 2
  apply List.map_congr_left
  intro j _
  simp only [Function.comp, Nat.succ_eq_add_one]
  congr 2; omega

/-- **seg of a 9+ link vertex**, drawn as an 8: `[s_{k-1}, y_k, 9, x_k, s_k]`. -/
theorem segL_big (k : ℕ) (hD : ¬ T.graph.degree (w k) ≤ 8) :
    (wordOf T u w).segL (k % d) =
      [letterOf T (rotNbr T (w k) u 2), letterOf T (rotNbr T (w k) u 3), 9,
        letterOf T (rotNbr T (w k) u (T.graph.degree (w k) - 3)),
        letterOf T (rotNbr T (w k) u (T.graph.degree (w k) - 2))] := by
  have d5 := hL.d5 hT
  have hd : 0 < d := by omega
  have hm := Nat.mod_lt k hd
  have O := window_oriented hT hL
  unfold UWin.segL
  rw [word_d hL, word_linkL hL hm, word_priv hL hm, word_apexL hL hm, word_apexL hL (Nat.mod_lt _ hd),
    show (k % d + d - 1) % d = (k + d - 1) % d by
      rw [show k % d + d - 1 = (k % d + (d - 1)) by omega, show k + d - 1 = k + (d - 1) by omega, Nat.add_mod,
        Nat.mod_mod, ← Nat.add_mod],
    apexV_mod hL, apexV_mod hL, hL.per_mod, letterOf_eq9 hD, ← rot2_eq hT hL, ← O.atL2 k]
  unfold privL
  rw [hL.per_mod, if_neg hD]
  rfl

theorem seg_get_exact (k : ℕ) (hD : T.graph.degree (w k) ≤ 8) (j : ℕ) (hj : j < T.graph.degree (w k) - 3) :
    ((wordOf T u w).segL (k % d))[j]? = some (letterOf T (rotNbr T (w k) u (2 + j))) := by
  rw [segL_exact hT hL k hD, List.getElem?_map, List.getElem?_range hj]; rfl

theorem seg_zero (k : ℕ) : ((wordOf T u w).segL (k % d))[0]? = some (letterOf T (rotNbr T (w k) u 2)) := by
  by_cases hD : T.graph.degree (w k) ≤ 8
  · rw [seg_get_exact hT hL k hD 0 (by have := hT.minDeg (w k); omega)]
  · rw [segL_big hT hL k hD]; rfl

theorem seg_one (k : ℕ) : ((wordOf T u w).segL (k % d))[1]? = some (letterOf T (rotNbr T (w k) u 3)) := by
  by_cases hD : T.graph.degree (w k) ≤ 8
  · rw [seg_get_exact hT hL k hD 1 (by have := hT.minDeg (w k); omega)]
  · rw [segL_big hT hL k hD]; rfl

theorem segR_one (k : ℕ) :
    (let s := (wordOf T u w).segL (k % d); if 1 < s.length then s[s.length - 1 - 1]? else none) =
      some (letterOf T (rotNbr T (w k) u (T.graph.degree (w k) - 3))) := by
  have h5 := hT.minDeg (w k)
  by_cases hD : T.graph.degree (w k) ≤ 8
  · simp only [segL_exact hT hL k hD, List.length_map, List.length_range]
    rw [if_pos (by omega), List.getElem?_map, List.getElem?_range (by omega)]
    simp only [Option.map_some]
    congr 3; omega
  · rw [segL_big hT hL k hD]; rfl

/-! ## Rotations of the window vertices, read from a neighbouring hub -/

theorem rot_u_link (i k : ℕ) : rotNbr T u (w i) k = w (i + k) := by
  induction k with
  | zero => rw [rotNbr_zero (hL.adj i)]; rfl
  | succ k ih => rw [← rotNbr_add (hL.adj i) k 1, ih, hL.step]; rfl

/-- `rot(w_j)` read from `w_{j+1}`: `w_{j+1}, u, w_{j-1}, s_{j-1}, …` -/
theorem rot_prev (j k : ℕ) (hk : 1 ≤ k) : rotNbr T (w j) (w (j + 1)) k = rotNbr T (w j) u (k - 1) := by
  have O := window_oriented hT hL
  have h5 := hT.minDeg (w j)
  rw [← O.atL1 j, rotNbr_add (hL.adj j).symm, show T.graph.degree (w j) - 1 + k = (k - 1) + T.graph.degree (w j) by
    omega, O.per]

/-- `rot(w_{i+1})` read from `w_i`: `w_i, s_i, p_{i+1}.1, …` -/
theorem rot_next (i k : ℕ) : rotNbr T (w (i + 1)) (w i) k = rotNbr T (w (i + 1)) u (1 + k) := by
  have O := window_oriented hT hL
  rw [← O.at1 i, rotNbr_add (hL.adj (i + 1)).symm]

/-- `rot(s_j)` read from `w_{j+1}`: `w_{j+1}, w_j, x_j (= rot(w_j)[D-3])`. -/
theorem rot_apex2 (j : ℕ) :
    rotNbr T (apexV T w j) (w (j + 1)) 2 = rotNbr T (w j) u (T.graph.degree (w j) - 3) := by
  have O := window_oriented hT hL
  have h5 := hT.minDeg (w j)
  have hadj : T.Adj (apexV T w j) (w (j + 1)) := nx_adj_left (O.apexRot j)
  rw [← rotNbr_add hadj 1 1, rotNbr_one_of_nx (O.apexRot j)]
  have a := (O.arc j (T.graph.degree (w j) - 3)).2
  rw [show T.graph.degree (w j) - 3 + 1 = T.graph.degree (w j) - 2 by omega, O.atL2] at a
  exact rotNbr_one_of_nx a

/-! ## M2: the views B2 builds approximate the real views -/

/-- **M2 at hub `u`.** Spoke `t` of `UWin.viewU` (the spoke `w_t`) approximates the real view of `w_t` from `u`. -/
theorem approxU {t : ℕ} (ht : t < d) :
    ∃ x, (wordOf T u w).viewU[t]? = some x ∧ Approx x (realSpoke T u (w t)) := by
  have d5 := hL.d5 hT
  have hd : 0 < d := by omega
  have h5 := hT.minDeg (w t)
  refine ⟨_, by rw [UWin.viewU, List.getElem?_map, List.getElem?_range (by rw [word_d hL]; exact ht)]; rfl, ?_⟩
  have hsp : (wordOf T u w).letter 0 (uSpokePos t) = some (letterOf T (w t)) :=
    letter_w hL hd 0 t t 0 (by push_cast; ring)
  simp only [hsp, Option.getD_some]
  refine approx_mk rfl ?_ ?_
  · right
    show (wordOf T u w).letter 0 (.seg t 0) = _
    rw [letter_seg hL 0 t t 0 (by push_cast; ring), seg_zero hT hL]
  · by_cases hD : T.graph.degree (w t) ≤ 8
    · right
      refine ⟨by rw [letterOf_le8 hD, npriv_le8 h5 hD], fun k hk => Or.inr ?_⟩
      rw [letterOf_le8 hD, npriv_le8 h5 hD] at hk
      show (wordOf T u w).letter 0 (.seg t (k + 1)) = _
      rw [letter_seg hL 0 t t 0 (by push_cast; ring), seg_get_exact hT hL t hD (k + 1) (by omega)]
      congr 3; omega
    · left; exact letterOf_eq9 hD

/-- **M2 at hub `w_i`** (`deg w_i ≤ 8`). Spoke `t` of `UWin.viewW i` approximates the real view of `rot(w_i)[t]`
(read from `u`) from `w_i`. -/
theorem approxW {i : ℕ} (hi : i < d) (hD : T.graph.degree (w i) ≤ 8) {t : ℕ} (ht : t < T.graph.degree (w i)) :
    ∃ x, ((wordOf T u w).viewW i)[t]? = some x ∧ Approx x (realSpoke T (w i) (rotNbr T (w i) u t)) := by
  have d5 := hL.d5 hT
  have hd : 0 < d := by omega
  have O := window_oriented hT hL
  have hDi := hT.minDeg (w i)
  have hn : (wordOf T u w).linkL i = T.graph.degree (w i) := by rw [word_linkL hL hi, letterOf_le8 hD]
  refine ⟨_, by rw [UWin.viewW, hn, List.getElem?_map, List.getElem?_range ht]; rfl, ?_⟩
  -- the previous link index `j = i - 1`
  set j := i + d - 1 with hj
  have hwi : w i = w (j + 1) := by rw [show j + 1 = i + d by omega, hL.per]
  -- spokes on the hub's own seg
  have spoke_seg : ∀ t, 2 ≤ t → t + 1 < T.graph.degree (w i) →
      (wordOf T u w).letter i (.seg 0 (t - 2)) = some (letterOf T (rotNbr T (w i) u t)) := by
    intro t h2 h3
    rw [letter_seg hL i 0 i 0 (by push_cast; ring), seg_get_exact hT hL i hD (t - 2) (by omega)]
    congr 3; omega
  rcases (show t = 0 ∨ t = 1 ∨ (2 ≤ t ∧ t + 1 < T.graph.degree (w i)) ∨ t + 1 = T.graph.degree (w i) by omega)
    with h0 | h1 | ⟨h2, h3⟩ | hl
  · -- t = 0: the spoke is u
    subst h0
    simp only [wSpokePos, wHatPos, wFanPos, ↓reduceIte, UWin.fanCount, letter_u, Option.getD_some]
    rw [O.at0]
    refine approx_mk rfl (Or.inr ?_) (Or.inr ⟨by rw [word_d hL, hL.deg], fun k _ => Or.inr ?_⟩)
    · rw [letter_w hL hd i 2 (i + 2) 0 (by push_cast; ring), rot_u_link hT hL]
    · rw [letter_w hL hd i (3 + k) (i + (3 + k)) 0 (by push_cast; ring), rot_u_link hT hL]
  · -- t = 1: the spoke is w_{i-1}
    subst h1
    have hn1 : ¬ (1 + 1 = T.graph.degree (w i)) := by omega
    simp only [wSpokePos, wHatPos, wFanPos, hn1, ↓reduceIte, one_ne_zero, UWin.fanCount]
    have hsp : (wordOf T u w).letter i (.w (-1)) = some (letterOf T (w j)) :=
      letter_w hL hd i (-1) j 1 (by rw [hj]; push_cast [show 1 ≤ i + d by omega]; ring)
    simp only [hsp, Option.getD_some]
    rw [hwi, O.at1 j]
    have hj5 := hT.minDeg (w j)
    refine approx_mk rfl (Or.inr ?_) ?_
    · rw [letter_w hL hd i (-2) (i + d - 2) 1 (by push_cast [show 2 ≤ i + d by omega]; ring),
        rot_prev hT hL j 2 (by omega)]
      have := O.at1 (i + d - 2)
      rw [show i + d - 2 + 1 = j by omega] at this
      rw [this]
    · by_cases hDj : T.graph.degree (w j) ≤ 8
      · right
        refine ⟨by rw [letterOf_le8 hDj, npriv_le8 hj5 hDj], fun k hk => Or.inr ?_⟩
        rw [letterOf_le8 hDj, npriv_le8 hj5 hDj] at hk
        rw [letter_seg hL i (-1) j 1 (by rw [hj]; push_cast [show 1 ≤ i + d by omega]; ring),
          seg_get_exact hT hL j hDj k (by omega), rot_prev hT hL j (3 + k) (by omega)]
        congr 3; omega
      · left; exact letterOf_eq9 hDj
  · -- 2 ≤ t ≤ D-2: a vertex of the hub's own seg
    have ht0 : t ≠ 0 := by omega
    have ht1 : t ≠ 1 := by omega
    have htl : ¬ (t + 1 = T.graph.degree (w i)) := by omega
    simp only [wSpokePos, wHatPos, wFanPos, ht0, ht1, htl, ↓reduceIte, UWin.fanCount]
    rw [spoke_seg t h2 h3]
    simp only [Option.getD_some]
    have hx5 := hT.minDeg (rotNbr T (w i) u t)
    by_cases h2' : t = 2
    · subst h2'
      simp only [↓reduceIte]
      refine approx_unknown_fans hx5 rfl (Or.inr ?_)
      rw [letter_segR hL i (-1) j 1 (by rw [hj]; push_cast [show 1 ≤ i + d by omega]; ring), segR_one hT hL,
        hwi, O.at2 j, rot_apex2 hT hL]
    · simp only [h2', ↓reduceIte]
      exact approx_unknown_fans hx5 rfl (Or.inl rfl)
  · -- t = D-1: the spoke is w_{i+1}
    have ht0 : t ≠ 0 := by omega
    have ht1 : t ≠ 1 := by omega
    have ht2 : t ≠ 2 := by omega
    simp only [wSpokePos, wHatPos, wFanPos, ht0, ht1, ht2, hl, ↓reduceIte, UWin.fanCount]
    have hsp : (wordOf T u w).letter i (.w 1) = some (letterOf T (w (i + 1))) :=
      letter_w hL hd i 1 (i + 1) 0 (by push_cast; ring)
    simp only [hsp, Option.getD_some]
    rw [show t = T.graph.degree (w i) - 1 by omega, O.atL1 i]
    have hk5 := hT.minDeg (w (i + 1))
    refine approx_mk rfl (Or.inr ?_) ?_
    · rw [letter_seg hL i 1 (i + 1) 0 (by push_cast; ring), seg_one hT hL, rot_next hT hL]
    · by_cases hDk : T.graph.degree (w (i + 1)) ≤ 8
      · right
        refine ⟨by rw [letterOf_le8 hDk, npriv_le8 hk5 hDk], fun k hk => Or.inr ?_⟩
        rw [letterOf_le8 hDk, npriv_le8 hk5 hDk] at hk
        rw [letter_seg hL i 1 (i + 1) 0 (by push_cast; ring), seg_get_exact hT hL (i + 1) hDk (k + 2) (by omega),
          rot_next hT hL]
        congr 3; omega
      · left; exact letterOf_eq9 hDk

end

end SimpleGraph.SphericalMap.RSSTSeed
