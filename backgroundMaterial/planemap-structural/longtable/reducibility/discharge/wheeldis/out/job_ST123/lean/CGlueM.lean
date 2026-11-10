import COccBridge

/-! # CGlueM: C glue for a contraction set whose classes meet the ring twice (ST-123 S0 + M1, 10 Nov 2026)

Plan: `W/out/job_ST123/ROUTE_I_PLAN.md` (committed 369223c54).

`admissibleX` (CGlue) ends with the clause "distinct ring positions have distinct labels". The configuration
2.126 = `rsst003_2o126` (ring 8, interior 4, `X = {R0-I0, R2-I0, R4-I2, R6-I2}`) fails it for every labelling,
because each X-star meets the ring twice. The plan found that the clause is used only inside C4b, the label
argument proving `XLoopFree`. It is not used in `contract_reducer_of`, which takes `hadm` and never reads it, nor in
the pull-back or the hC chain.

This file holds:
- `admissibleXM`: `admissibleX` without the last conjunct;
- the 2.126 literal, its labelling, and `decide` checks of the side facts;
- `contract_reducer_ofM`: CGlue's `contract_reducer_of` verbatim, with the `hadm` binder deleted;
- `CEntryM` and `CEntryM.colorable_of_contract`: the hadm-free copies of `CEntry` and its colouring wrapper.

`XLoopFree` stays a hypothesis here. It is proved in M2/M3 (`xGraph_labels_merge`).
Nothing in CGlue, CGlueU or COccBridge is changed. No `sorry`. No `native_decide`: the hC computation is in
`C2o126HC.lean`. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ} {T G : SphericalMap n} {ρ : ℕ → Fin n}

/-- **Local admissibility for merged classes**: `admissibleX` minus its last conjunct (distinct ring positions
have distinct labels). Two ring positions may therefore share a label; loop-freeness must then come from
elsewhere (`XLoopFree`). -/
def admissibleXM (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ) : Bool :=
  let L : ℕ → ℕ := fun i => lbl.getD i 0
  decide (1 ≤ eqR.length + eqI.length) && decide (eqR.length + eqI.length ≤ 4) &&
  decide (lbl.length = cf.m + cf.r) &&
  eqR.all (fun p => decide (p.2 < cf.m) && (cf.ringAdj[p.2]!).contains p.1) &&
  eqI.all (fun p => decide (p.2 < cf.m) && decide (p.1 < cf.m) && (cf.intAdj[p.2]!).contains p.1) &&
  (List.range cf.m).all (fun a =>
    (cf.ringAdj[a]!).all (fun t => decide (t < cf.r) &&
      (if eqR.contains (t, a) then L a == L (cf.m + t) else L a != L (cf.m + t))) &&
    (cf.intAdj[a]!).all (fun b => decide (b < cf.m) &&
      (if eqI.contains (b, a) || eqI.contains (a, b) then L a == L b else L a != L b)))

/-- `admissibleXM` is weaker than `admissibleX`. -/
theorem admissibleXM_of_admissibleX (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (h : admissibleX cf eqR eqI lbl = true) : admissibleXM cf eqR eqI lbl = true := by
  simp only [admissibleX, admissibleXM, Bool.and_eq_true] at h ⊢
  tauto

/-! ## 2.126 = rsst003_2o126 (kc line `loop/k44/rsst.txt:4`)

`rsst003_2o126 8 4 0,1,2;2,3,4;4,5,6;0,6,7 1,2,3;0,2;0,1,3;0,2`. The contraction set is
`X = {R0-I0, R2-I0, R4-I2, R6-I2}` (`loop/k44/rsst_verdicts_C2.txt:3`), in `(t, a)` form
`eqR = [(0,0),(2,0),(4,2),(6,2)]`, with `eqI = []`.

The labelling is `I0..I3 ↦ 0,1,2,3` and `R0..R7 ↦ 0,4,0,5,2,6,2,7`. The two classes {I0,R0,R2} and {I2,R4,R6}
get labels 0 and 2. -/

def cf2o126 : DCheck18.Conf :=
  { name := "rsst003_2o126", r := 8, m := 4,
    ringAdj := #[#[0, 1, 2], #[2, 3, 4], #[4, 5, 6], #[0, 6, 7]],
    intAdj := #[#[1, 2, 3], #[0, 2], #[0, 1, 3], #[0, 2]] }

def eqR2o126 : List (ℕ × ℕ) := [(0, 0), (2, 0), (4, 2), (6, 2)]
def eqI2o126 : List (ℕ × ℕ) := []
def lbl2o126 : List ℕ := [0, 1, 2, 3, 0, 4, 0, 5, 2, 6, 2, 7]

/-- S0: the merged-class admissibility holds. -/
theorem cf2o126_admM : admissibleXM (Conf.of18 cf2o126) eqR2o126 eqI2o126 lbl2o126 = true := by
  decide +kernel

/-- S0, sabotage: CGlue's `admissibleX` refuses 2.126 with this labelling. (It refuses every labelling, since
`L R0 = L I0 = L R2` is forced; this theorem checks only the one used here.) -/
theorem cf2o126_not_adm : admissibleX (Conf.of18 cf2o126) eqR2o126 eqI2o126 lbl2o126 = false := by
  decide +kernel

/-- S0: fold safety (the D1/D2 pairs are all excluded by `exclB`/`cycEx`). -/
theorem cf2o126_fold : foldSafeX (Conf.of18 cf2o126) eqR2o126 eqI2o126 lbl2o126 = true := by
  decide +kernel

/-! ## C4 without `hadm` -/

/-- **C4 from a contraction of the X-graph, without admissibility.** This is `ConfigOccW.contract_reducer_of`
(CGlue) verbatim, with the unused `hadm` binder deleted. -/
theorem ConfigOccW.contract_reducer_ofM (cf : Conf) (eqR eqI : List (ℕ × ℕ))
    (hloop : ∀ a, intAdjOf cf a a = false)
    (hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hlab : XLoopFree cf eqR eqI ρ ι G)
    (hcon : ∀ H : SimpleGraph (Fin n), H = xGraph cf eqR eqI ρ ι → H ≤ T.graph →
      (∃ x y, H.Adj x y) → ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
        Nat.card T'.graph.support < Nat.card T.graph.support ∧
        (∀ x y, H.Reachable x y → π x = π y) ∧
        (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y))) :
    ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
      Nat.card T'.graph.support < Nat.card T.graph.support ∧
      (∀ x y, G.Adj x y → T'.Adj (π x) (π y)) ∧
      (∀ (a : Fin cf.m) t, ringAdjOf cf a t = true →
        (eqR.contains (t, a.val) = true → π (ι a) = π (ρ t)) ∧
        (eqR.contains (t, a.val) = false → T'.Adj (π (ι a)) (π (ρ t)))) ∧
      (∀ a b : Fin cf.m, intAdjOf cf a b = true →
        ((eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true →
          π (ι b) = π (ι a)) ∧
        ((eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = false →
          T'.Adj (π (ι b)) (π (ι a)))) := by
  classical
  have hlt : ∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → t < cf.r :=
    fun a t hat => hrr a.val a.isLt t (of_decide_eq_true hat)
  have hXR : ∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → eqR.contains (t, a.val) = true →
      (xGraph cf eqR eqI ρ ι).Adj (ι a) (ρ t) := by
    intro a t hat h
    rw [xGraph, SimpleGraph.fromRel_adj]
    exact ⟨fun e => O.ringOff t a e.symm, Or.inl (Or.inl ⟨a, t, hat, h, rfl, rfl⟩)⟩
  have hXI : ∀ a b : Fin cf.m, intAdjOf cf a b = true →
      (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true →
      (xGraph cf eqR eqI ρ ι).Adj (ι b) (ι a) := by
    intro a b hab h
    rw [xGraph, SimpleGraph.fromRel_adj]
    refine ⟨fun e => ?_, Or.inr (Or.inr ⟨a, b, hab, h, rfl, rfl⟩)⟩
    have hba : b = a := O.ιinj e
    subst hba
    rw [hloop] at hab
    exact Bool.false_ne_true hab
  have hle : xGraph cf eqR eqI ρ ι ≤ T.graph := by
    intro x y hxy
    rw [xGraph, SimpleGraph.fromRel_adj] at hxy
    obtain ⟨-, h | h⟩ := hxy
    · rcases h with ⟨a, t, hat, -, rfl, rfl⟩ | ⟨a, b, hab, -, rfl, rfl⟩
      · exact hex.2 a t (hlt a t hat) hat
      · exact hex.1 a b hab
    · rcases h with ⟨a, t, hat, -, rfl, rfl⟩ | ⟨a, b, hab, -, rfl, rfl⟩
      · exact (hex.2 a t (hlt a t hat) hat).symm
      · exact (hex.1 a b hab).symm
  obtain ⟨hne, hnR, hnI, hnG⟩ := hlab
  obtain ⟨T', π, hcard, hπ, hkeep⟩ := hcon _ rfl hle hne
  refine ⟨T', π, hcard, fun x y hxy => hkeep x y ((O.hG x y).1 hxy).1 (hnG x y hxy),
    fun a t hat => ⟨fun h => hπ _ _ (hXR a t hat h).reachable,
      fun h => hkeep _ _ (hex.2 a t (hlt a t hat) hat) (hnR a t hat h)⟩,
    fun a b hab => ⟨fun h => hπ _ _ (hXI a b hab h).reachable,
      fun h => hkeep _ _ (hex.1 a b hab).symm (hnI a b hab h)⟩⟩

/-! ## C6 for merged-class entries (loop-freeness as a hypothesis) -/

namespace CGlue
open ClaimGlue (SmallerColorable)

/-- **A C entry with merged-class admissibility.** As `CEntry`, with `hadm : admissibleX` replaced by
`hadmM : admissibleXM`. -/
structure CEntryM where
  cf : DCheck18.Conf
  /-- contracted ring–interior edges `(t, a)` -/
  eqR : List (ℕ × ℕ)
  /-- contracted interior edges `(b, a)` -/
  eqI : List (ℕ × ℕ)
  /-- a label per interior vertex, then per ring position (ring labels may repeat) -/
  lbl : List ℕ
  hC : cReducible18 cf eqR eqI = true
  hadmM : admissibleXM (Conf.of18 cf) eqR eqI lbl = true
  hr2 : 2 ≤ cf.r
  hr : cf.r ≤ 19
  hsym : ∀ a b, intAdjOf (Conf.of18 cf) a b = true → intAdjOf (Conf.of18 cf) b a = true
  hloop : ∀ a, intAdjOf (Conf.of18 cf) a a = false
  hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r

/-- **C-soundness for a merged-class entry, given loop-freeness.** `CEntry.colorable_of_contract` (CGlue)
verbatim, calling `contract_reducer_ofM`. -/
theorem CEntryM.colorable_of_contract (e : CEntryM) {T G : SphericalMap n} {ρ : ℕ → Fin n}
    {ι : Fin e.cf.m → Fin n}
    (O : ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hex : OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hlab : XLoopFree (Conf.of18 e.cf) e.eqR e.eqI ρ ι G) (IH : SmallerColorable T)
    (hcon : ∀ H : SimpleGraph (Fin n), H = xGraph (Conf.of18 e.cf) e.eqR e.eqI ρ ι →
      H ≤ T.graph → (∃ x y, H.Adj x y) → ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
        Nat.card T'.graph.support < Nat.card T.graph.support ∧
        (∀ x y, H.Reachable x y → π x = π y) ∧
        (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y))) :
    T.graph.Colorable 4 := by
  obtain ⟨T', π, hcard, hGe, hR, hI⟩ :=
    ConfigOccW.contract_reducer_ofM (Conf.of18 e.cf) e.eqR e.eqI e.hloop e.hrr O hex hlab hcon
  obtain ⟨col⟩ := IH n T' hcard
  refine ConfigOccW.colorable_of_cReducible18 e.cf e.eqR e.eqI e.hC e.hr2 e.hr e.hsym e.hloop
    e.hrr O (c := fun x => col (π x)) (fun _ _ huv _ _ => col.valid (hGe _ _ huv))
    (fun a => col (π (ι a))) ⟨fun a t hat => ?_, fun a b hab => ?_⟩
  · exact ⟨fun h => congrArg col ((hR a t hat).1 h).symm,
      fun h => (col.valid ((hR a t hat).2 h)).symm⟩
  · exact ⟨fun h => congrArg col ((hI a b hab).1 h),
      fun h => col.valid ((hI a b hab).2 h)⟩

/-- The same with C4a `contract_subgraph` supplied: only loop-freeness remains. -/
theorem CEntryM.colorable_of_loopFree (e : CEntryM) {T G : SphericalMap n} {ρ : ℕ → Fin n}
    {ι : Fin e.cf.m → Fin n}
    (O : ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hex : OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hlab : XLoopFree (Conf.of18 e.cf) e.eqR e.eqI ρ ι G) (IH : SmallerColorable T) :
    T.graph.Colorable 4 :=
  e.colorable_of_contract O hex hlab IH (fun H _ hle hne => contract_subgraph T H hle hne)

/-- Side facts of 2.126 (all by `decide`). -/
theorem cf2o126_sym : ∀ a b, intAdjOf (Conf.of18 cf2o126) a b = true →
    intAdjOf (Conf.of18 cf2o126) b a = true := by decide +kernel
theorem cf2o126_loop : ∀ a, intAdjOf (Conf.of18 cf2o126) a a = false := by decide +kernel
theorem cf2o126_rr : ∀ a, a < cf2o126.m → ∀ t ∈ cf2o126.ringAdj[a]!, t < cf2o126.r := by decide +kernel

/-- 2.126 as a merged-class C entry, from its C verdict (supplied by `C2o126HC.lean`). -/
def e2o126 (hC : cReducible18 cf2o126 eqR2o126 eqI2o126 = true) : CEntryM where
  cf := cf2o126
  eqR := eqR2o126
  eqI := eqI2o126
  lbl := lbl2o126
  hC := hC
  hadmM := cf2o126_admM
  hr2 := by decide
  hr := by decide
  hsym := cf2o126_sym
  hloop := cf2o126_loop
  hrr := cf2o126_rr

end CGlue
end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.admissibleXM_of_admissibleX
#print axioms SimpleGraph.SphericalMap.cf2o126_admM
#print axioms SimpleGraph.SphericalMap.cf2o126_not_adm
#print axioms SimpleGraph.SphericalMap.cf2o126_fold
#print axioms SimpleGraph.SphericalMap.ConfigOccW.contract_reducer_ofM
#print axioms SimpleGraph.SphericalMap.CGlue.CEntryM.colorable_of_contract
#print axioms SimpleGraph.SphericalMap.CGlue.CEntryM.colorable_of_loopFree
#print axioms SimpleGraph.SphericalMap.CGlue.cf2o126_sym
#print axioms SimpleGraph.SphericalMap.CGlue.cf2o126_loop
#print axioms SimpleGraph.SphericalMap.CGlue.cf2o126_rr
#print axioms SimpleGraph.SphericalMap.CGlue.e2o126
