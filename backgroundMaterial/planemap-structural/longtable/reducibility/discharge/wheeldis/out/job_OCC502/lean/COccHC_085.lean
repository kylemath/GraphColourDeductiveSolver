import COccBridge
import HC_085

/-! Bridge test (Long Table, 19 Oct 2026): the occ24 key `HC_085`'s rotation occurrence `Occ` gives
`RotOcc` with the rotation read off its own `Nx` fields, hence `OccExact`, `NbrInj` and `ApexFacts`.
Only `int_inj`, `disj`, `deg` and the `Nx` fields of `Occ` are used (no `ring_inj`). -/

namespace SimpleGraph.SphericalMap.HC_085
open VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ}

/-- The rotation at each interior vertex, as `Occ` states it. -/
def rot : Fin 8 → List (Fin 8 ⊕ ℕ) := ![[.inr 0, .inl 4, .inl 1, .inl 3, .inr 5, .inl 5, .inl 6], [.inr 3, .inl 3, .inl 0, .inl 4, .inr 2], [.inr 9, .inr 10, .inr 11, .inl 6, .inl 7], [.inr 3, .inr 4, .inr 5, .inl 0, .inl 1], [.inr 0, .inr 1, .inr 2, .inl 1, .inl 0], [.inr 6, .inr 7, .inl 7, .inl 6, .inl 0, .inr 5], [.inl 0, .inl 5, .inl 7, .inl 2, .inr 11, .inr 0], [.inr 7, .inr 8, .inr 9, .inl 2, .inl 6, .inl 5]]

theorem rot_ok : rotOK (DCheck.Conf.of18 cf) rot = true := by
  native_decide

theorem rotOcc_of_occ {T : SphericalMap n} {ring : Fin 12 → Fin n} {int : Fin 8 → Fin n}
    (h : Occ T ring int) : RotOcc T (ρOf ring) int rot where
  ιinj := h.int_inj
  disj := fun t a => h.disj _ a
  deg := fun a => by rw [h.deg a]; fin_cases a <;> rfl
  nx := by
    intro a k hk
    fin_cases a
    · replace hk : k < 7 := hk
      interval_cases k
      · exact h.r0_0
      · exact h.r0_1
      · exact h.r0_2
      · exact h.r0_3
      · exact h.r0_4
      · exact h.r0_5
      · exact h.r0_6
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r1_0
      · exact h.r1_1
      · exact h.r1_2
      · exact h.r1_3
      · exact h.r1_4
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r2_0
      · exact h.r2_1
      · exact h.r2_2
      · exact h.r2_3
      · exact h.r2_4
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r3_0
      · exact h.r3_1
      · exact h.r3_2
      · exact h.r3_3
      · exact h.r3_4
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r4_0
      · exact h.r4_1
      · exact h.r4_2
      · exact h.r4_3
      · exact h.r4_4
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r5_0
      · exact h.r5_1
      · exact h.r5_2
      · exact h.r5_3
      · exact h.r5_4
      · exact h.r5_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r6_0
      · exact h.r6_1
      · exact h.r6_2
      · exact h.r6_3
      · exact h.r6_4
      · exact h.r6_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r7_0
      · exact h.r7_1
      · exact h.r7_2
      · exact h.r7_3
      · exact h.r7_4
      · exact h.r7_5

/-- **Falsification test, passed**: `Occ` gives the three local facts. -/
theorem local_facts_of_occ {T : SphericalMap n} {ring : Fin 12 → Fin n} {int : Fin 8 → Fin n}
    (h : Occ T ring int) :
    OccExact T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    NbrInj (DCheck.Conf.of18 cf).r (ρOf ring) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    ApexFacts T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) :=
  ⟨(rotOcc_of_occ h).occExact rot_ok, (rotOcc_of_occ h).nbrInj rot_ok,
    (rotOcc_of_occ h).apexFacts rot_ok cf_sym⟩

/-! ## Registry glue (s74_leanglue/gen_occ_kc.py)

`Occ` in the registry's own terms: the D occurrence `ClaimGlue.OccursW` and entry `ClaimGlue.DEntry`, and the C
occurrence `CGlue.OccursCXR` / `CGlue.OccursCXF` of any C entry whose configuration is `cf`. A registry Conf literal for
this kc line (gen_hd.py's `<PFX>Confs.get ⟨i, _⟩`, gen_ccover3.py's `cf` field) is equal to `cf` by `rfl`. -/

/-- `Occ` gives the reduction-ready D occurrence of `cf`. -/
theorem occursW_of_occ {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n}
    (h : Occ T ring int) : ClaimGlue.OccursW cf T := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  rw [← intAdjOf_eq, ← ringAdjOf_eq] at O
  exact ⟨G, ρOf ring, int, O, hlt⟩

/-- The D registry entry, from a checker verdict on any `c = cf` (gen_hd.py: `MODV.hD_i` with `hc := rfl`). -/
def dEntryOf {c : DCheck18.Conf} (hD : DCheck18.dReducible c = true) (hc : c = cf) : ClaimGlue.DEntry where
  cf := c
  hD := hD
  hr2 := by subst hc; decide
  hr := by subst hc; decide
  hsym := by subst hc; exact cf_sym
  hloop := by subst hc; exact cf_loop

/-- **Per-key D reduction, registry form.** -/
theorem colorable_of_occ_entry {c : DCheck18.Conf} (hD : DCheck18.dReducible c = true) (hc : c = cf)
    {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n}
    (h : Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  (dEntryOf hD hc).colorable (show ClaimGlue.OccursW c T by rw [hc]; exact occursW_of_occ htri h) IH

/-- The same for an occurrence of the mirror image (`Occ` in `T.mirror`, same graph). -/
theorem colorable_of_mirror_occ_entry {c : DCheck18.Conf} (hD : DCheck18.dReducible c = true) (hc : c = cf)
    {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n}
    (h : Occ T.mirror ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  colorable_of_occ_entry hD hc (T := T.mirror) (mirror_triangulated htri) h IH

/-- `Occ` gives the C occurrence in the rotation format of any C entry on `cf`. -/
theorem occursCXR_of_occ (e : CGlue.CEntry) (he : e.cf = cf) {T : SphericalMap n} (htri : T.Triangulated)
    {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : Occ T ring int) : CGlue.OccursCXR e T := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  rw [← intAdjOf_eq, ← ringAdjOf_eq] at O
  first
  | (unfold CGlue.OccursCXR; rw [he]; exact ⟨G, ρOf ring, int, rot, O, rotOcc_of_occ h, rot_ok⟩)
  | (cases e; dsimp only at he; subst he; exact ⟨G, ρOf ring, int, rot, O, rotOcc_of_occ h, rot_ok⟩)
  | (cases e; subst he; exact ⟨G, ρOf ring, int, rot, O, rotOcc_of_occ h, rot_ok⟩)

/-- `Occ` gives the fold-safe C occurrence (`OccExact`, `NbrInj`, `ApexFacts` derived) of any C entry on `cf`. -/
theorem occursCXF_of_occ (e : CGlue.CEntry) (he : e.cf = cf) {T : SphericalMap n} (htri : T.Triangulated)
    {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : Occ T ring int) : CGlue.OccursCXF e T :=
  (occursCXR_of_occ e he htri h).toF

/-- **Per-key C reduction, registry form** (a fold-safe C entry on `cf`, e.g. `XRData.toCEntryF`). -/
theorem colorable_of_occ_centry (e : CGlue.CEntryF) (he : e.cf = cf) {T : SphericalMap n}
    (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n}
    (h : Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  e.colorable htri (occursCXF_of_occ e.toCEntry he htri h) IH

/-- The same for an occurrence of the mirror image. -/
theorem colorable_of_mirror_occ_centry (e : CGlue.CEntryF) (he : e.cf = cf) {T : SphericalMap n}
    (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n}
    (h : Occ T.mirror ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  colorable_of_occ_centry e he (T := T.mirror) (mirror_triangulated htri) h IH

end SimpleGraph.SphericalMap.HC_085

#print axioms SimpleGraph.SphericalMap.HC_085.local_facts_of_occ

#print axioms SimpleGraph.SphericalMap.HC_085.occursW_of_occ
#print axioms SimpleGraph.SphericalMap.HC_085.dEntryOf
#print axioms SimpleGraph.SphericalMap.HC_085.colorable_of_occ_entry
#print axioms SimpleGraph.SphericalMap.HC_085.colorable_of_mirror_occ_entry
#print axioms SimpleGraph.SphericalMap.HC_085.occursCXR_of_occ
#print axioms SimpleGraph.SphericalMap.HC_085.occursCXF_of_occ
#print axioms SimpleGraph.SphericalMap.HC_085.colorable_of_occ_centry
#print axioms SimpleGraph.SphericalMap.HC_085.colorable_of_mirror_occ_centry
