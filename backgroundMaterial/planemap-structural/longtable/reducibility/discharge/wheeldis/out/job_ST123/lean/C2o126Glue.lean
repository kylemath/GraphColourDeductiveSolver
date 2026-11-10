import CGlueMerge
import RotFacialSlot
import C2o126HC
import DCheckMirror

/-! # C2o126Glue: 2.126 is C-reducible in a minimal counterexample (ST-123 M3, 10 Nov 2026)

The three occurrence facts of `xGraph_labels_merge` (CGlueMerge) come from decidable checks with soundness proofs:
- `coherB` gives `RingCoh`. Folds across classes are excluded by `exclB`/`cycEx` (`excl_sound`, `cycEx_sound`).
- `foldSafeX` (CGlue, its D1 half) gives `RingD1`. Kept ring neighbours do not fold into a class.
- `chordB` gives `NoClassChord`. A chord `ρ s ~ ρ t` inside a star with centre `c` closes a triangle at `ι c`. By
  NoSep and `RotOcc.common_nbr_ring_slot`, `ρ t` is then a rotation neighbour of slot `inr s` in `rot c`, which
  `slotSafe` excludes (`NbrInj`, `ringOff`).

The per-key checks for 2.126 are by `decide +kernel`. The C verdict is `cf2o126_hC` (`native_decide`, C2o126HC).

**Main theorem** `colorable_2o126`: a face-walk occurrence of 2.126 (folds allowed) with the interior rotation
`rot2o126`, in a triangulation whose smaller maps are colourable, makes it colourable. `colorable_mirror_2o126`
handles the mirror image. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ} {T G : SphericalMap n} {ρ : ℕ → Fin n}

/-! ## `RingCoh` from `coherB` -/

/-- Touched positions with different labels are excluded from folding (by `exclB` or `cycEx`). -/
def coherB (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) : Bool :=
  (List.range cf.r).all fun s => (List.range cf.r).all fun t =>
    !touchedB eqR s || !touchedB eqR t || lbl.getD (cf.m + s) 0 == lbl.getD (cf.m + t) 0 ||
      exclB cf s t || cycEx cf s t

theorem ringCoh_of_coherB (cf : Conf) {eqR : List (ℕ × ℕ)} {lbl : List ℕ} {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hNI : NbrInj cf.r ρ (ringAdjOf cf)) (hCN : CommonNbr T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hloop : ∀ a, intAdjOf cf a a = false) (htri : T.Triangulated)
    (hNS : ClaimGlue.NoShortSepCycle T) (h : coherB cf eqR lbl = true) :
    RingCoh cf eqR lbl ρ := by
  intro s t hs ht ⟨a, ha⟩ ⟨b, hb⟩ he
  simp only [coherB, List.all_eq_true, List.mem_range] at h
  have h1 := h s hs t ht
  simp only [Bool.or_eq_true, Bool.not_eq_true', beq_iff_eq] at h1
  rcases h1 with (((h1 | h1) | h1) | h1) | h1
  · exact absurd (touchedB_of_mem ha) (by simp [h1])
  · exact absurd (touchedB_of_mem hb) (by simp [h1])
  · exact h1
  · by_contra hne
    have hst : s ≠ t := fun e => hne (by rw [e])
    exact excl_sound cf O hex hNI hCN hs ht hst h1 he
  · exact absurd he (cycEx_sound cf O hex hCN hloop htri hNS hs ht h1)

/-! ## `RingD1` from `foldSafeX` -/

theorem ringD1_of_foldSafeX (cf : Conf) {eqR eqI : List (ℕ × ℕ)} {lbl : List ℕ}
    {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hNI : NbrInj cf.r ρ (ringAdjOf cf)) (hCN : CommonNbr T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hloop : ∀ a, intAdjOf cf a a = false) (htri : T.Triangulated)
    (hNS : ClaimGlue.NoShortSepCycle T) (hsafe : foldSafeX cf eqR eqI lbl = true) :
    RingD1 cf eqR lbl ρ := by
  intro a s t hat h hsr ht hst htc hlt hρ
  simp only [foldSafeX, Bool.and_eq_true, List.all_eq_true, Array.all_eq_true, List.mem_range,
    Bool.or_eq_true, beq_iff_eq, Bool.not_eq_true', bne_iff_ne, ne_eq] at hsafe
  obtain ⟨i, hi, hsi⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hat)
  have hD1 := ((hsafe a.val a.isLt).1 i hi)
  rw [hsi] at hD1
  obtain ⟨b, hb⟩ := htc
  have htt : touchedB eqR t = true := touchedB_of_mem hb
  rcases hD1 with hD1 | hD1
  · rw [h] at hD1; exact Bool.false_ne_true hD1
  · rcases hD1 t ht with (((h1 | h1) | h1) | h1) | h1
    · exact absurd htt (by simp [h1])
    · exact h1 hlt
    · exact hst h1
    · exact excl_sound cf O hex hNI hCN hsr ht hst h1 hρ
    · exact cycEx_sound cf O hex hCN hloop htri hNS hsr ht h1 hρ

/-! ## `NoClassChord` from `chordB` -/

/-- A rotation slot of `c` that cannot be the vertex `ρ t`: an interior slot (`ringOff`), or a ring slot `p ≠ t`
listed at `c` (`NbrInj`). -/
def slotSafe (cf : Conf) (c : Fin cf.m) (t : ℕ) : Fin cf.m ⊕ ℕ → Bool
  | .inl _ => true
  | .inr p => !(p == t) && decide (p ∈ cf.ringAdj[c.val]!) && decide (p < cf.r)

/-- For touched positions `s ≠ t` with one label: some centre `c` lists `t`, and both rotation neighbours of slot
`inr s` in `rot c` are safe for `t`. -/
def chordB (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ)
    (rot : Fin cf.m → List (Fin cf.m ⊕ ℕ)) : Bool :=
  (List.range cf.r).all fun s => (List.range cf.r).all fun t =>
    !touchedB eqR s || !touchedB eqR t || s == t ||
      lbl.getD (cf.m + s) 0 != lbl.getD (cf.m + t) 0 ||
      (List.finRange cf.m).any fun c => decide (t ∈ cf.ringAdj[c.val]!) &&
        (List.range (rot c).length).any fun j =>
          decide ((rot c).getD j (.inr 0) = .inr s) &&
          slotSafe cf c t ((rot c).getD ((j + 1) % (rot c).length) (.inr 0)) &&
          slotSafe cf c t ((rot c).getD ((j + (rot c).length - 1) % (rot c).length) (.inr 0))

theorem slotSafe_sound {cf : Conf} {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hNI : NbrInj cf.r ρ (ringAdjOf cf)) (c : Fin cf.m) {t : ℕ} (ht : t < cf.r)
    (hct : ringAdjOf cf c t = true) {q : Fin cf.m ⊕ ℕ} (hq : slotSafe cf c t q = true) :
    slotV ρ ι q ≠ ρ t := by
  cases q with
  | inl e => exact fun h => O.ringOff t e h.symm
  | inr p =>
    simp only [slotSafe, Bool.and_eq_true, Bool.not_eq_true', beq_eq_false_iff_ne,
      decide_eq_true_eq] at hq
    obtain ⟨⟨hpt, hpc⟩, hpr⟩ := hq
    intro h
    exact hpt (hNI c p t (decide_eq_true hpc) hct hpr ht h)

theorem noClassChord_of_chordB {cf : Conf} {eqR : List (ℕ × ℕ)} {lbl : List ℕ}
    {ι : Fin cf.m → Fin n} {rot : Fin cf.m → List (Fin cf.m ⊕ ℕ)} (R : RotOcc T ρ ι rot)
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hNI : NbrInj cf.r ρ (ringAdjOf cf)) (htri : T.Triangulated) (hns : NoSep T)
    (h : chordB cf eqR lbl rot = true) : NoClassChord T cf eqR lbl ρ := by
  intro s t hs ht ⟨a, ha⟩ ⟨b, hb⟩ hl hadj
  simp only [chordB, List.all_eq_true, List.mem_range] at h
  have h1 := h s hs t ht
  simp only [Bool.or_eq_true, Bool.not_eq_true', beq_iff_eq, bne_iff_ne, ne_eq,
    List.any_eq_true, Bool.and_eq_true, decide_eq_true_eq, List.mem_range] at h1
  rcases h1 with (((h1 | h1) | h1) | h1) | ⟨c, -, hct, j, hj, ⟨hjs, hs1⟩, hs2⟩
  · exact absurd (touchedB_of_mem ha) (by simp [h1])
  · exact absurd (touchedB_of_mem hb) (by simp [h1])
  · subst h1; exact T.graph.ne_of_adj hadj rfl
  · exact h1 hl
  · have hct' : ringAdjOf cf c t = true := decide_eq_true hct
    rcases R.common_nbr_ring_slot htri hns c hj hjs (hex.2 c t ht hct') hadj with hw | hw
    · exact slotSafe_sound O hNI c ht hct' hs1 hw.symm
    · exact slotSafe_sound O hNI c ht hct' hs2 hw.symm

/-! ## 2.126 -/

/-- The free-completion rotation of 2.126 at I0..I3, from the kc line: I0 `R0 R1 R2 I1 I2 I3`, I1 `R2 R3 R4 I2 I0`,
I2 `R4 R5 R6 I3 I0 I1`, I3 `R6 R7 R0 I0 I2`. These are consistent with one planar drawing (ROUTE_I_PLAN §0); the other
orientation is `colorable_mirror_2o126`. -/
def rot2o126 : Fin 4 → List (Fin 4 ⊕ ℕ) :=
  ![[.inr 0, .inr 1, .inr 2, .inl 1, .inl 2, .inl 3], [.inr 2, .inr 3, .inr 4, .inl 2, .inl 0],
    [.inr 4, .inr 5, .inr 6, .inl 3, .inl 0, .inl 1], [.inr 6, .inr 7, .inr 0, .inl 0, .inl 2]]

theorem rot2o126_ok : rotOK (Conf.of18 cf2o126) rot2o126 = true := by decide +kernel

theorem cf2o126_coh : coherB (Conf.of18 cf2o126) eqR2o126 lbl2o126 = true := by decide +kernel

theorem cf2o126_chord : chordB (Conf.of18 cf2o126) eqR2o126 lbl2o126 rot2o126 = true := by
  decide +kernel

/-- Sabotage: with R1 and R2 swapped in the rotation at I0 (so R0 and R2 become rotation neighbours there), `chordB`
refuses. The check is not vacuous. -/
def rot2o126bad : Fin 4 → List (Fin 4 ⊕ ℕ) :=
  ![[.inr 0, .inr 2, .inr 1, .inl 1, .inl 2, .inl 3], [.inr 2, .inr 3, .inr 4, .inl 2, .inl 0],
      [.inr 4, .inr 5, .inr 6, .inl 3, .inl 0, .inl 1], [.inr 6, .inr 7, .inr 0, .inl 0, .inl 2]]

theorem cf2o126_chord_sabotage : chordB (Conf.of18 cf2o126) eqR2o126 lbl2o126 rot2o126bad = false := by
  decide +kernel

/-- **2.126 reduces.** A face-walk occurrence (folds and pinches allowed) with interior rotation `rot2o126`, in a
triangulation whose smaller maps are all four-colourable, makes it four-colourable. -/
theorem colorable_2o126 {ι : Fin 4 → Fin n} (htri : T.Triangulated)
    (O : ConfigOccW T G 8 4 ρ ι (intAdjOf (Conf.of18 cf2o126)) (ringAdjOf (Conf.of18 cf2o126)))
    (R : RotOcc T ρ ι rot2o126) (IH : ClaimGlue.SmallerColorable T) : T.graph.Colorable 4 := by
  by_contra hcol
  have hmc : ClaimGlue.MinimalCounterexample T := ⟨hcol, IH⟩
  have hns : NoSep T := ClaimGlue.MinimalCounterexample.noSep hmc htri
  have hNS := ClaimGlue.MinimalCounterexample.noShortSep hmc
  have hex := R.occExact rot2o126_ok
  have hNI := R.nbrInj rot2o126_ok
  have hCN := commonNbr_of_apex hns hex (R.apexFacts rot2o126_ok CGlue.cf2o126_sym)
  have hlab := ConfigOccW.xGraph_labels_merge (Conf.of18 cf2o126) eqR2o126 eqI2o126 lbl2o126
    cf2o126_admM CGlue.cf2o126_loop O
    (ringCoh_of_coherB _ O hex hNI hCN CGlue.cf2o126_loop htri hNS cf2o126_coh)
    (ringD1_of_foldSafeX _ O hex hNI hCN CGlue.cf2o126_loop htri hNS cf2o126_fold)
    (noClassChord_of_chordB R O hex hNI htri hns cf2o126_chord)
  exact hcol (CGlue.e2o126C.colorable_of_loopFree O hex hlab IH)

/-- The same for an occurrence in the mirror image (`T.mirror`, same graph). -/
theorem colorable_mirror_2o126 {ι : Fin 4 → Fin n} (htri : T.Triangulated)
    (O : ConfigOccW T.mirror G 8 4 ρ ι (intAdjOf (Conf.of18 cf2o126)) (ringAdjOf (Conf.of18 cf2o126)))
    (R : RotOcc T.mirror ρ ι rot2o126) (IH : ClaimGlue.SmallerColorable T) : T.graph.Colorable 4 :=
  colorable_2o126 (T := T.mirror) (mirror_triangulated htri) O R IH

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.ringCoh_of_coherB
#print axioms SimpleGraph.SphericalMap.ringD1_of_foldSafeX
#print axioms SimpleGraph.SphericalMap.slotSafe_sound
#print axioms SimpleGraph.SphericalMap.noClassChord_of_chordB
#print axioms SimpleGraph.SphericalMap.rot2o126_ok
#print axioms SimpleGraph.SphericalMap.cf2o126_coh
#print axioms SimpleGraph.SphericalMap.cf2o126_chord
#print axioms SimpleGraph.SphericalMap.cf2o126_chord_sabotage
#print axioms SimpleGraph.SphericalMap.colorable_2o126
#print axioms SimpleGraph.SphericalMap.colorable_mirror_2o126
