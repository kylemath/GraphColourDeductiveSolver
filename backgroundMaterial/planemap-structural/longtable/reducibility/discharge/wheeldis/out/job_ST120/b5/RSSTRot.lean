import RSSTCheckSound
import RSSTRulesN2

/-!
# ST-127 (b): rotation canonicalisation, and `seed_of_B5` for any part list (79 parts included)

Studio, 11 Nov. B4's `eval_sound` holds for **every** link listing `w` of `u`. Shifting the listing (`k ↦ w (k + r)`)
rotates the link word, so a vertex with positive final charge has a listing whose word has the *least rotation* of its
link word (`isRotMin`, by the numeric key `wkey`, = lexicographic order on letters 5..9). Hence the checker need only
replay one link word per rotation class (`checkDegRotP`), and `seed_of_B5P_rot` turns that into B4's conclusion.
`seed_of_B5P` is the same wrapper with B4's `hB5` shape for `loHiP parts` (e.g. `rsstParts79`).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap

/-! ## Rotations of a word -/

def rotL (r : Nat) (L : List Nat) : List Nat := (List.range L.length).map fun k => L.getD ((k + r) % L.length) 0

def wkey (L : List Nat) : Nat := L.foldl (fun a x => 10 * a + x) 0

/-- `L` is the least of its rotations (by `wkey`). -/
def isRotMin (L : List Nat) : Bool := (List.range L.length).all fun s => Nat.ble (wkey L) (wkey (rotL s L))

theorem rotL_length (r : Nat) (L : List Nat) : (rotL r L).length = L.length := by simp [rotL]

theorem rotL_rotL (L : List Nat) (hd : 0 < L.length) (r s : Nat) :
    rotL s (rotL r L) = rotL ((r + s) % L.length) L := by
  apply List.ext_getElem
  · simp [rotL]
  · intro k h1 h2
    simp only [rotL, List.length_map, List.length_range] at h1 h2 ⊢
    simp only [List.getElem_map, List.getElem_range]
    have hk : (k + s) % L.length < L.length := Nat.mod_lt _ hd
    rw [getD_lt' _ _ _ (by simpa using hk)]
    simp only [List.getElem_map, List.getElem_range]
    congr 1
    rw [Nat.mod_add_mod, Nat.add_mod_mod]
    congr 1; ring

/-! ## The per-degree check over rotation classes -/

def checkDegRotP (parts : List Part) (KL : List Conf) (d : Nat) (cert : List LinkCert) : Bool :=
  parts.all Part.fanExact && Nat.ble 5 d && Nat.ble d 30 &&
    checkLinksP parts KL d ((allWords d).filter isRotMin) cert

theorem checkDegRotP_sound (parts : List Part) (KL : List Conf) (d : Nat) (cert : List LinkCert)
    (h : checkDegRotP parts KL d cert = true) :
    ∀ W : UWin, RealShape W → W.d = d → isRotMin W.link = true → 0 < (loHiP parts W).2 → Kills KL W := by
  intro W hW hd hrot hpos
  unfold checkDegRotP at h
  simp only [Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨⟨⟨hP, h5⟩, h30⟩, hl⟩ := h
  have hP' : ∀ p ∈ parts, p.fanExact = true := fun p hp => List.all_eq_true.1 hP p hp
  have hmem : W.link ∈ (allWords d).filter isRotMin := by
    have := allWords_mem W.link hW.2.2.2.2.1
    rw [hW.2.1, hd] at this
    exact List.mem_filter.2 ⟨this, hrot⟩
  obtain ⟨c, hc⟩ := checkLinks_mem parts KL d _ cert hl W.link hmem
  exact checkLink_sound parts hP' KL d W.link c hc W hW hd rfl h30 hpos

/-! ## The triangulation side -/

section
variable {n : ℕ}

theorem link_shift {T : SphericalMap n} {u : Fin n} {d : ℕ} {w : ℕ → Fin n} (hL : IsLink T u d w) (r : ℕ) :
    IsLink T u d (fun k => w (k + r)) where
  deg := hL.deg
  per i := by show w (i + d + r) = w (i + r); rw [show i + d + r = (i + r) + d by ring]; exact hL.per _
  adj0 := by simpa using hL.adj r
  step i := by show rotNbr T u (w (i + r)) 1 = w (i + 1 + r); rw [hL.step, show i + r + 1 = i + 1 + r by ring]

theorem word_shift {T : SphericalMap n} {u : Fin n} {w : ℕ → Fin n} (hL : IsLink T u (T.graph.degree u) w)
    (hd : 0 < T.graph.degree u) (r : ℕ) :
    (wordOf T u (fun k => w (k + r))).link = rotL r (wordOf T u w).link := by
  apply List.ext_getElem
  · simp [wordOf, rotL]
  · intro k h1 h2
    simp only [wordOf, rotL, List.length_map, List.length_range, List.getElem_map, List.getElem_range] at h1 h2 ⊢
    have hk : (k + r) % T.graph.degree u < T.graph.degree u := Nat.mod_lt _ hd
    rw [getD_lt' _ _ _ (by simpa using hk)]
    simp only [List.getElem_map, List.getElem_range]
    rw [hL.per_mod]

/-- **`seed_of_B5`, any well-shaped part list, rotation-canonical words only.** -/
theorem seed_of_B5P_rot (parts : List Part) (hP : ∀ p ∈ parts, p.wellShaped = true) {T : SphericalMap n}
    (hT : ClaimGlue.Internally6 T) (Kills : UWin → Prop)
    (hB5 : ∀ W : UWin, RealShape W → isRotMin W.link = true → 0 < (loHiP parts W).2 → Kills W) :
    ∃ u w, IsLink T u (T.graph.degree u) w ∧ Kills (wordOf T u w) := by
  obtain ⟨a, ha⟩ := (T.graph.degree_pos_iff_exists_adj ⟨0, hT.pos⟩).1 (by have := hT.minDeg ⟨0, hT.pos⟩; omega)
  obtain ⟨u, hu⟩ := exists_pos_final hT.triangulated ⟨(⟨0, hT.pos⟩, a), ha⟩ (tauP parts T)
  obtain ⟨w, hL⟩ := exists_link hT u
  have hd : 0 < T.graph.degree u := by have := hT.minDeg u; omega
  set L0 := (wordOf T u w).link with hL0
  have hlen : L0.length = T.graph.degree u := by simp [hL0, wordOf]
  obtain ⟨r0, hr0, hmin⟩ := Finset.exists_min_image (Finset.range (T.graph.degree u)) (fun r => wkey (rotL r L0))
    ⟨0, Finset.mem_range.2 hd⟩
  have hL' := link_shift hL r0
  refine ⟨u, _, hL', hB5 _ (wordOf_realShape hT hL') ?_ ?_⟩
  · rw [word_shift hL hd r0, ← hL0]
    unfold isRotMin
    apply List.all_eq_true.2
    intro s hs
    rw [Nat.ble_eq, rotL_rotL L0 (by omega) r0 s]
    apply hmin
    rw [Finset.mem_range, hlen]
    exact Nat.mod_lt _ (by omega)
  · exact lt_of_lt_of_le hu (eval_sound hT hL' parts hP).2

/-- **`seed_of_B5` for any well-shaped part list** (B4's `hB5` shape, against `loHiP parts`). -/
theorem seed_of_B5P (parts : List Part) (hP : ∀ p ∈ parts, p.wellShaped = true) {T : SphericalMap n}
    (hT : ClaimGlue.Internally6 T) (Kills : UWin → Prop)
    (hB5 : ∀ W : UWin, RealShape W → 0 < (loHiP parts W).2 → Kills W) :
    ∃ u w, IsLink T u (T.graph.degree u) w ∧ Kills (wordOf T u w) :=
  seed_of_B5P_rot parts hP hT Kills (fun W hW _ hpos => hB5 W hW hpos)

/-- The 79 parts (71 + N2). -/
theorem seed_of_B5_79 {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) (Kills : UWin → Prop)
    (hB5 : ∀ W : UWin, RealShape W → isRotMin W.link = true → 0 < (loHiP rsstParts79 W).2 → Kills W) :
    ∃ u w, IsLink T u (T.graph.degree u) w ∧ Kills (wordOf T u w) :=
  seed_of_B5P_rot rsstParts79 (fun p hp => List.all_eq_true.1 rsstParts79_wellShaped p hp) hT Kills hB5

end

#print axioms checkDegRotP_sound
#print axioms seed_of_B5P_rot
#print axioms seed_of_B5P
#print axioms seed_of_B5_79

end SimpleGraph.SphericalMap.RSSTSeed
