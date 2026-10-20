import ClaimGlue
import C66666
import CContract

/-!
# CGlue: soundness of C-reducibility (Long Table, 19 Oct 2026, draft)

`ClaimGlue.lean` proves "reducible registry + `Unavoidable R` ⇒ 4-colourable" with the C entries
behind an explicit hypothesis `CGlue R.C`. This file replaces that hypothesis by a theorem,
`CEntry.colorable`, with no `sorry` (C4a, the contraction geometry, is in `CContract.lean`).
Scope: `SolvingFrameworkPlan/docs/working/CGLUE-SCOPE.md`; write-up: `CGLUE-DRAFT.md`.

**What a C entry certifies** (cfast / `C66666.lean`, `CWheels.lean`). For a contraction set
`X = eqR ∪ eqI` (`eqR`: ring–interior edges `(t, a)`; `eqI`: interior edges `(b, a)`), every ring
colouring that extends to the contracted configuration (`extCAux`) is in the good set of the
D-closure. Here that closure is `Ref.runGoodRefT`, the loop of `Ref.runRefT` (Job 23) verbatim,
returning the final `good` array; the verdict is `cReducible18 cf eqR eqI` (`native_decide`, per key).

**Proof plan (pieces as in the scope).**
* C1 `S1T.runGoodRefT_sound` [PROVED]: a good bit is `GoodT` (the `OuterInv` invariant of Job 23).
* C2 `CG.extCAux_complete`, `CG.extCAux_canon` [PROVED]: an interior colouring meeting the X
  constraints makes `extCAux` accept the canonical code of the ring colouring.
* C3 `ConfigOccW.colorable_of_goodT`, `ConfigOccW.colorable_of_cReducible18` [PROVED]: the D tail
  (`good_soundT` + `FaceWalk.kempeMatching` + `colorable_of_ext`) from a `GoodT` realised code.
* C4 `ConfigOccW.contract_reducer` [PROVED from C4a]: contracting `X` in `T` gives a spherical map
  `T'` of smaller support and a vertex map `π` that keeps every edge of the deleted map `G`,
  identifies along `X`, and keeps every other listed configuration edge. It splits into
  - C4a `contract_subgraph` [PROVED: `CContract.contract_subgraph_gen`]: contracting a subgraph of
    a spherical map is a smaller spherical map (pure map geometry, no configuration data; any
    spherical map, no triangulation needed);
  - C4b `ConfigOccW.xGraph_labels` [PROVED]: the label argument (no kept edge inside an X-component).
* C5 (global loop-freeness) is not a lemma here: it is the occurrence field `XRingSimple` (no ring
  position touched by `X` is revisited by the face walk), proved for simple rings
  (`occursCX_of_configOcc`). Local loop-freeness is `admissibleX` (decide, per key).
* C6 `CEntry.colorable`, `four_color_of_unavoidableC` [PROVED from C1–C4].
* C6, one interior edge (`CEntry1`: `eqR = []`, `eqI = [p0]`): `CEntry1.colorable`, `cGlueX1`,
  `four_color_of_unavoidableC1` [PROVED; an earlier special case, now subsumed by C6].

**Axioms.** No new `axiom`, no `sorry`. Inherits the `native_decide` axioms of the D chain;
per-key `hC` adds one each.
-/

/-! ## C1: the good bits of the D-closure are `GoodT` -/

namespace DCheck
namespace Ref

/-- `runRefT`'s loop, verbatim, returning the final `good` array. Index `i` refers to
`(ringColourings cf.r)[i]`. -/
def runGoodRefT (mt : Array (Array (Array Nat))) (cf : Conf) : Array Bool := Id.run do
  let r := cf.r
  let ks := ringColourings r
  let N := ks.size
  let index := mkIndex ks
  let mut good : Array Bool := ks.map (extendsQ cf)
  let ext := (good.filter id).size
  let mut reached := ext
  let mut prog : Array Nat := Array.replicate (3 * N) 0
  let mut depth := 0
  for _ in [0:N + 1] do
    let (prog', new) := iLoopT mt r ks index good prog
    prog := prog'
    if new.isEmpty then break
    good := setLoop new good
    reached := reached + new.size
    depth := depth + 1
  return good

end Ref

namespace S1T
open DCheck.Ref DCheck.S1

variable {mt : Array (Array (Array Nat))}

/-- **C1.** Every good bit of `runGoodRefT` is a `GoodT` code (`runRef_sound`'s invariant, with the
counting part dropped). -/
theorem runGoodRefT_sound (cf : Conf) :
    ∀ j : Nat, (runGoodRefT mt cf)[j]! = true → GoodT mt cf (ringColourings cf.r)[j]! := by
  have hI := mkIndex_spec (ringColourings cf.r)
  unfold runGoodRefT
  refine forIn_range_bind 0 ((ringColourings cf.r).size + 1) _ _ _
    (fun _ (st : Array Bool × Nat × Array Nat × Nat) =>
      OuterInv mt cf (ringColourings cf.r) st.1 st.2.1 st.2.2.1)
    (fun (res : Array Bool) => ∀ j : Nat, res[j]! = true → GoodT mt cf (ringColourings cf.r)[j]!)
    ?_ (fun x hx => hx.2.1) ?_
  · refine ⟨by simp, fun j hj => ?_, Nat.le_refl _, ?_⟩
    · by_cases hjs : j < (ringColourings cf.r).size
      · rw [getElem!_pos _ j (by simpa using hjs)] at hj
        rw [getElem!_pos _ j hjs]
        exact GoodT.base _ (by simpa using hj)
      · rw [getElem!_neg _ j (by simpa using hjs)] at hj
        cases hj
    · intro i th _ _ _ q hq
      rw [replicate_zero_get] at hq
      omega
  · intro _ ⟨good, reached, prog, depth⟩ _ _ ⟨hsz, hG, hcnt, hP⟩
    dsimp only at hsz hG hcnt hP ⊢
    have hit := iLoop_spec cf (ringColourings cf.r) (mkIndex (ringColourings cf.r)) good prog
      hI hG hP
    generalize iLoopT mt cf.r (ringColourings cf.r) (mkIndex (ringColourings cf.r)) good prog = res
      at hit ⊢
    obtain ⟨p', new⟩ := res
    obtain ⟨hP', hN, hPw⟩ := hit
    dsimp only at hP' hN hPw ⊢
    split
    · simp only [stepOK_done]
      exact hG
    · simp only [stepOK_yield]
      have hs := setFold_spec new.toList good hPw
        (fun j hj => ⟨by have := (hN j hj).1; omega, (hN j hj).2.1⟩)
      rw [setLoop_eq]
      refine ⟨by rw [hs.1, hsz], fun j hj => ?_, ?_, hP'⟩
      · rcases hs.2.2 j hj with h | h
        · exact hG j h
        · exact (hN j h).2.2
      · rw [hs.2.1, Array.length_toList]; omega

end S1T

/-! ## The C verdict -/

/-- **The C verdict** (computational half, `native_decide` per key): every ring colouring that
extends after contracting `X` is good in the D-closure for the table `mt`. Same shape as the
`…_extX_reached` theorems of `C66666.lean`/`CWheels.lean`, with `runGoodRefT` for `runGood`. -/
def cReducibleT (mt : Array (Array (Array Nat))) (cf : Conf) (eqR eqI : List (Nat × Nat)) : Bool :=
  let ks := ringColourings cf.r
  let good := Ref.runGoodRefT mt cf
  (List.range ks.size).all fun i => !(extCAux cf eqR eqI ks[i]! cf.m #[]) || good[i]!

theorem cReducibleT_spec (mt : Array (Array (Array Nat))) (cf : Conf) (eqR eqI : List (Nat × Nat)) :
    cReducibleT mt cf eqR eqI = (List.range (ringColourings cf.r).size).all fun i =>
      !(extCAux cf eqR eqI (ringColourings cf.r)[i]! cf.m #[]) || (Ref.runGoodRefT mt cf)[i]! :=
  rfl

/-- The verdict for rings `≤ 19` (`DCheck18` encoding, table 10, as `dReducible18`). -/
def cReducible18 (cf : DCheck18.Conf) (eqR eqI : List (Nat × Nat)) : Bool :=
  cReducibleT (matchTableN 10) (Conf.of18 cf) eqR eqI

/-- C1 + verdict: a canonical ring colouring accepted by `extCAux` is `GoodT`. -/
theorem cReducibleT_good (mt : Array (Array (Array Nat))) (cf : Conf) (eqR eqI : List (Nat × Nat))
    (hC : cReducibleT mt cf eqR eqI = true) (k : Nat) (hk : k ∈ ringColourings cf.r)
    (hext : extCAux cf eqR eqI k cf.m #[] = true) : GoodT mt cf k := by
  obtain ⟨i, hi, rfl⟩ := Array.mem_iff_getElem.1 hk
  have e := getElem!_pos (ringColourings cf.r) i hi
  rw [cReducibleT_spec, List.all_eq_true] at hC
  have h := hC i (List.mem_range.2 hi)
  rw [← e] at hext
  rw [hext, Bool.not_true, Bool.false_or] at h
  have := S1T.runGoodRefT_sound (mt := mt) cf i h
  rwa [e] at this

/-! ## C2: the X constraints make `extCAux` accept -/

namespace CG
open DCheck.R2

theorem cond_eq_true {c : Bool} {u v : Nat} (h : c = true) (e : u = v) :
    (if c = true then u == v else u != v) = true := by
  subst h; simp [e]

theorem cond_ne_true {c : Bool} {u v : Nat} (h : c = false) (e : u ≠ v) :
    (if c = true then u == v else u != v) = true := by
  subst h; simp [e]

/-- **C2 (completeness of `extCAux`).** An interior colouring `lam` (colours `< 4`) that meets the
X constraints against the ring code `k` (equal across a contracted edge, different across every other
listed edge) makes `extCAux` accept, from any prefix of `lam`. -/
theorem extCAux_complete (cf : Conf) (eqR eqI : List (Nat × Nat)) (k : Nat) (lam : Nat → Nat)
    (hlt : ∀ a, lam a < 4)
    (hR : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!,
      (eqR.contains (t, a) = true → col k t = lam a) ∧
      (eqR.contains (t, a) = false → col k t ≠ lam a))
    (hI : ∀ a, a < cf.m → ∀ b ∈ cf.intAdj[a]!, b < a →
      ((eqI.contains (b, a) || eqI.contains (a, b)) = true → lam b = lam a) ∧
      ((eqI.contains (b, a) || eqI.contains (a, b)) = false → lam b ≠ lam a)) :
    ∀ f (cols : Array Nat), cols.size + f = cf.m → (∀ i, i < cols.size → cols[i]! = lam i) →
      extCAux cf eqR eqI k f cols = true := by
  intro f
  induction f with
  | zero => intro cols _ _; rfl
  | succ f ih =>
    intro cols hsz hcols
    have ha : cols.size < cf.m := by omega
    have hpush : extCAux cf eqR eqI k f (cols.push (lam cols.size)) = true := by
      apply ih
      · simp only [Array.size_push]; omega
      · intro i hi
        simp only [Array.size_push] at hi
        by_cases h : i < cols.size
        · rw [push_get_lt _ _ _ h]; exact hcols i h
        · rw [show i = cols.size by omega, push_get_eq]
    have hring : (cf.ringAdj[cols.size]!).all (fun t => if eqR.contains (t, cols.size) then
        col k t == lam cols.size else col k t != lam cols.size) = true := by
      rw [Array.all_eq_true]
      intro i hi
      have ht := hR cols.size ha _ (Array.getElem_mem hi)
      rcases Bool.eq_false_or_eq_true (eqR.contains ((cf.ringAdj[cols.size]!)[i], cols.size)) with hc | hc
      · exact cond_eq_true hc (ht.1 hc)
      · exact cond_ne_true hc (ht.2 hc)
    have hint : (cf.intAdj[cols.size]!).all (fun b => b >= cols.size ||
        (if eqI.contains (b, cols.size) || eqI.contains (cols.size, b) then
          cols[b]! == lam cols.size else cols[b]! != lam cols.size)) = true := by
      rw [Array.all_eq_true]
      intro i hi
      rw [Bool.or_eq_true]
      by_cases hb : (cf.intAdj[cols.size]!)[i] < cols.size
      · right
        have ht := hI cols.size ha _ (Array.getElem_mem hi) hb
        rw [hcols _ hb]
        rcases Bool.eq_false_or_eq_true (eqI.contains ((cf.intAdj[cols.size]!)[i], cols.size) ||
            eqI.contains (cols.size, (cf.intAdj[cols.size]!)[i])) with hc | hc
        · exact cond_eq_true hc (ht.1 hc)
        · exact cond_ne_true hc (ht.2 hc)
      · left; exact decide_eq_true (by omega)
    have hx : lam cols.size ∈ [0, 1, 2, 3] := by
      rcases (by have := hlt cols.size; omega :
          lam cols.size = 0 ∨ lam cols.size = 1 ∨ lam cols.size = 2 ∨ lam cols.size = 3)
        with h | h | h | h <;> simp [h]
    simp only [extCAux, List.any_eq_true]
    exact ⟨lam cols.size, hx, by simp only [Bool.and_eq_true]; exact ⟨⟨hring, hint⟩, hpush⟩⟩

/-- An interior colouring on `Fin m`, as a sequence (`0` past `m`). -/
def lamN {m : Nat} (lam : Fin m → Fin 4) (a : Nat) : Nat :=
  if h : a < m then (lam ⟨a, h⟩).val else 0

theorem lamN_of_lt {m : Nat} (lam : Fin m → Fin 4) {a : Nat} (h : a < m) :
    lamN lam a = (lam ⟨a, h⟩).val := dif_pos h

theorem lamN_lt {m : Nat} (lam : Fin m → Fin 4) (a : Nat) : lamN lam a < 4 := by
  unfold lamN
  split
  · exact (lam _).isLt
  · decide

end CG
end DCheck

/-! ## C2 (map form), C3: the D tail -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ} {T G : SphericalMap n} {ρ : ℕ → Fin n}

/-- The constraints of `X = (eqR, eqI)` on a colouring `c` of the deleted map (read on the ring
`ρ`) and an interior colouring `lam`: equal across a contracted edge, different across every other
listed edge. These are exactly the constraints `extCAux` checks. -/
def XCompat (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (ρ : ℕ → Fin n) (c : Fin n → Fin 4)
    (lam : Fin cf.m → Fin 4) : Prop :=
  (∀ (a : Fin cf.m) t, ringAdjOf cf a t = true →
    (eqR.contains (t, a.val) = true → c (ρ t) = lam a) ∧
    (eqR.contains (t, a.val) = false → c (ρ t) ≠ lam a)) ∧
  (∀ a b : Fin cf.m, intAdjOf cf a b = true →
    ((eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true → lam b = lam a) ∧
    ((eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = false → lam b ≠ lam a))

/-- **C2, map form.** X-compatible colourings make `extCAux` accept the canonical ring code
(the renaming of `canon_rename` is applied to `lam` too). -/
theorem extCAux_canon (cf : Conf) (eqR eqI : List (ℕ × ℕ))
    (hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r) (ρ : ℕ → Fin n) (c : Fin n → Fin 4)
    (lam : Fin cf.m → Fin 4) (hX : XCompat cf eqR eqI ρ c lam) :
    extCAux cf eqR eqI (canon cf.r (code (ringSeq ρ c) cf.r)) cf.m #[] = true := by
  obtain ⟨g, hg, heq⟩ := canon_rename cf.r (ringSeq ρ c) (ringSeq_lt ρ c)
  have hcol : ∀ t, t < cf.r →
      col (canon cf.r (code (ringSeq ρ c) cf.r)) t = (g (c (ρ t))).val := by
    intro t ht
    have e1 : (⟨ringSeq ρ c t % 4, Nat.mod_lt _ (by decide)⟩ : Fin 4) = c (ρ t) :=
      Fin.ext (Nat.mod_eq_of_lt (c (ρ t)).isLt)
    rw [heq, col_code (fun t => (g ⟨ringSeq ρ c t % 4, Nat.mod_lt _ (by decide)⟩).val)
      (fun _ => Fin.isLt _) cf.r t ht]
    exact congrArg (fun x => (g x).val) e1
  refine CG.extCAux_complete cf eqR eqI _ (CG.lamN fun a => g (lam a)) (CG.lamN_lt _) ?_ ?_
    cf.m #[] (by simp) (by simp)
  · intro a ha t ht
    have hx := hX.1 ⟨a, ha⟩ t (decide_eq_true ht)
    rw [hcol t (hrr a ha t ht), CG.lamN_of_lt _ ha]
    exact ⟨fun h => congrArg (fun x => (g x).val) (hx.1 h),
      fun h e => hx.2 h (hg (Fin.ext e))⟩
  · intro a ha b hb hba
    have hx := hX.2 ⟨a, ha⟩ ⟨b, by omega⟩ (decide_eq_true hb)
    rw [CG.lamN_of_lt _ ha, CG.lamN_of_lt _ (show b < cf.m by omega)]
    exact ⟨fun h => congrArg (fun x => (g x).val) (hx.1 h),
      fun h e => hx.2 h (hg (Fin.ext e))⟩

variable {m : ℕ}

/-- **C3, the D tail from a good code.** If the canonical ring code of a colouring of `G` (proper
off the hole) is in the D-closure `GoodT`, then `T` is 4-colourable. (`ConfigOccW.colorable_of_dReducibleT`
with `dReducible_soundT` replaced by `good_soundT` at that one code.) -/
theorem ConfigOccW.colorable_of_goodT (N : ℕ) (hN : N ≤ 10) (cf : Conf) (hrN : cf.r < 2 * N)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true)
    (hloop : ∀ a, intAdjOf cf a a = false)
    {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c)
    (hgood : GoodT (matchTableN N) cf (canon cf.r (code (ringSeq ρ c) cf.r))) :
    T.graph.Colorable 4 := by
  classical
  let P : ℕ → Prop := fun k => ∃ c : Fin n → Fin 4, ProperOff G.graph O.hole c ∧
    k = code (ringSeq ρ c) cf.r
  have hcanon : ∀ k, P k → P (canon cf.r k) := by
    rintro k ⟨c1, hc1, rfl⟩
    obtain ⟨g, hg, heq⟩ := canon_rename cf.r (ringSeq ρ c1) (ringSeq_lt ρ c1)
    refine ⟨fun v => g (c1 v), fun u v huv hu hv h => hc1 huv hu hv (hg h), ?_⟩
    rw [heq]
    apply code_congr
    intro t _
    simp only [ringSeq]
    congr 3
    exact Nat.mod_eq_of_lt (c1 (ρ t)).isLt
  have hKM := FaceWalk.kempeMatching O.ring O.hole O.ring_ne_hole cf N hN rfl hrN
  obtain ⟨k', ⟨c', hc', rfl⟩, hext⟩ :=
    good_soundT (matchTableN N) cf P hcanon hKM _ hgood (hcanon _ ⟨c, hc, rfl⟩)
  obtain ⟨out, hsz, hlo, hok⟩ := extendsQ_sound cf _ hext
  let lam : Fin cf.m → Fin 4 := fun a => ⟨out[a.val]!, hlo a.val (by rw [hsz]; exact a.isLt)⟩
  refine O.colorable_of_ext hc' 1 (fun t => c' (ρ t)) (fun t _ => rfl) lam ?_ ?_ hsym
  · intro a b hab heq
    have hlam : out[a.val]! = out[b.val]! := congrArg Fin.val heq
    rcases Nat.lt_trichotomy b.val a.val with hlt | heq' | hgt
    · exact (hok a.val a.isLt).2 b.val (by simpa [intAdjOf] using hab) hlt hlam.symm
    · have : a = b := Fin.ext heq'.symm
      subst this; rw [hloop] at hab; exact Bool.false_ne_true hab
    · exact (hok b.val b.isLt).2 a.val (by simpa [intAdjOf] using hsym a b hab) hgt hlam
  · intro a t ht hat heq
    have := (hok a.val a.isLt).1 t (by simpa [ringAdjOf] using hat)
    apply this
    rw [col_code _ (ringSeq_lt ρ c') _ _ ht]
    simp only [ringSeq]
    exact (congrArg Fin.val heq).symm

/-- **C1–C3 assembled (rings `2 ≤ r ≤ 19`).** A C-reducible configuration occurring with face-walk
ring, plus a colouring `c` of `G` (proper off the hole) and an interior colouring `lam` that meet
the X constraints, make `T` 4-colourable. The pair `(c, lam)` is what a colouring of the
contracted map gives (C4). -/
theorem ConfigOccW.colorable_of_cReducible18 (cf : DCheck18.Conf) (eqR eqI : List (ℕ × ℕ))
    (hC : cReducible18 cf eqR eqI = true) (hr2 : 2 ≤ cf.r) (hr : cf.r ≤ 19)
    (hsym : ∀ a b, intAdjOf (Conf.of18 cf) a b = true → intAdjOf (Conf.of18 cf) b a = true)
    (hloop : ∀ a, intAdjOf (Conf.of18 cf) a a = false)
    (hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r)
    {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf (Conf.of18 cf)) (ringAdjOf (Conf.of18 cf)))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) (lam : Fin cf.m → Fin 4)
    (hX : XCompat (Conf.of18 cf) eqR eqI ρ c lam) : T.graph.Colorable 4 := by
  have hext := extCAux_canon (Conf.of18 cf) eqR eqI hrr ρ c lam hX
  have hprop : ∀ i, i < cf.r →
      col (code (ringSeq ρ c) cf.r) i ≠ col (code (ringSeq ρ c) cf.r) ((i + 1) % cf.r) := by
    intro i hi
    rw [col_code _ (ringSeq_lt ρ c) _ _ hi,
      col_code _ (ringSeq_lt ρ c) _ _ (Nat.mod_lt _ (by omega))]
    simp only [ringSeq]
    intro h
    by_cases hi1 : i + 1 < cf.r
    · rw [Nat.mod_eq_of_lt hi1] at h; exact O.ring_proper hc i (Fin.ext h)
    · rw [show (i + 1) % cf.r = 0 by rw [show i + 1 = cf.r by omega, Nat.mod_self]] at h
      exact O.ring_proper_wrap hc i (by omega) (Fin.ext h)
  have hmem : canon cf.r (code (ringSeq ρ c) cf.r) ∈ ringColourings cf.r :=
    canon_mem cf.r _ hr2 hprop (code_lt _ (ringSeq_lt ρ c) _)
  have hgood := cReducibleT_good (matchTableN 10) (Conf.of18 cf) eqR eqI hC _ hmem hext
  exact ConfigOccW.colorable_of_goodT 10 (by decide) (Conf.of18 cf)
    (by show cf.r < 2 * 10; omega) hsym hloop O hc hgood

/-! ## Admissibility (local, decidable) and the occurrence conditions (global) -/

/-- **Local admissibility of `X = eqR ∪ eqI`** (cfast's local checks, `decide` per key), certified
by a node labelling `lbl` (interior vertex `a` ↦ `lbl[a]`, ring position `t` ↦ `lbl[m + t]`):
* `1 ≤ |X| ≤ 4`, and `X` consists of listed configuration edges;
* every listed ring neighbour is a position `< r`;
* every X-edge joins equal labels and every other listed edge joins different labels (so the labels
  are constant on X-components and no edge outside `X` becomes a loop: this subsumes "sparse");
* distinct ring positions have distinct labels (each X-component meets the ring at most once; the
  three registry entries with an X-component through two ring vertices fail this).
Gonthier's triad condition for `|X| = 4` is not needed: it serves to derive global
loop-freeness from the ring's chordlessness, which here is the occurrence field `XRingSimple`. -/
def admissibleX (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ) : Bool :=
  let L : ℕ → ℕ := fun i => lbl.getD i 0
  decide (1 ≤ eqR.length + eqI.length) && decide (eqR.length + eqI.length ≤ 4) &&
  decide (lbl.length = cf.m + cf.r) &&
  eqR.all (fun p => decide (p.2 < cf.m) && (cf.ringAdj[p.2]!).contains p.1) &&
  eqI.all (fun p => decide (p.2 < cf.m) && decide (p.1 < cf.m) && (cf.intAdj[p.2]!).contains p.1) &&
  (List.range cf.m).all (fun a =>
    (cf.ringAdj[a]!).all (fun t => decide (t < cf.r) &&
      (if eqR.contains (t, a) then L a == L (cf.m + t) else L a != L (cf.m + t))) &&
    (cf.intAdj[a]!).all (fun b => decide (b < cf.m) &&
      (if eqI.contains (b, a) || eqI.contains (a, b) then L a == L b else L a != L b))) &&
  (List.range cf.r).all (fun s => (List.range cf.r).all (fun t =>
    s == t || L (cf.m + s) != L (cf.m + t)))

/-- **C5, as an occurrence condition.** A ring position touched by `X` is visited once by the face
walk. With admissibility this rules out every global loop of the contraction (a folded ring could
otherwise merge two X-components, or an X-component with a ring vertex it is not contracted to). -/
def XRingSimple (eqR : List (ℕ × ℕ)) (r : ℕ) (ρ : ℕ → Fin n) : Prop :=
  ∀ t a, (t, a) ∈ eqR → t < r → ∀ s, s < r → ρ s = ρ t → s = t

/-- The listed adjacencies are adjacencies of `T` (the occurrence is exact, as Gonthier's
embeddings are). `ConfigOccW.nbr` gives only the converse; contraction needs this direction, since
it must contract real edges and keep every listed edge outside `X`. -/
def OccExact (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (ι : Fin m → Fin n)
    (intAdj : Fin m → Fin m → Bool) (ringAdj : Fin m → ℕ → Bool) : Prop :=
  (∀ a b, intAdj a b = true → T.Adj (ι a) (ι b)) ∧
  (∀ a t, t < r → ringAdj a t = true → T.Adj (ι a) (ρ t))

/-- `XRingSimple` is vacuous when `X` has no ring–interior edge: such entries (921 of the 1,010 on
Studio head 3cfd7f18) need no ring condition beyond the D occurrence's (folds and pinches allowed). -/
theorem xRingSimple_nil (r : ℕ) (ρ : ℕ → Fin n) : XRingSimple [] r ρ := by
  intro t a h
  simp at h

/-- **Bridge to `OccExact` from rotation facts.** If every listed neighbour of each interior vertex
occurs in the rotation of `T` at that vertex, as in the per-key rotation occurrences (`occ24`'s
`Occ`: "the rotation of `T` at every interior vertex is the free-completion rotation") and in
Job 26's 2-ball embedding, then the occurrence is exact. -/
theorem occExact_of_nx {r : ℕ} {ι : Fin m → Fin n} {intAdj : Fin m → Fin m → Bool}
    {ringAdj : Fin m → ℕ → Bool}
    (hI : ∀ a b, intAdj a b = true → ∃ u, Nx T (ι a) u (ι b))
    (hR : ∀ a t, t < r → ringAdj a t = true → ∃ u, Nx T (ι a) u (ρ t)) :
    OccExact T r ρ ι intAdj ringAdj :=
  ⟨fun a b h => (hI a b h).elim fun _ hu => nx_adj_right hu,
    fun a t ht h => (hR a t ht h).elim fun _ hu => nx_adj_right hu⟩

/-! ## C4: the contracted reducer

C4 is split into two lemmas and an assembly, all proved:
* C4a `contract_subgraph` (PROVED, geometry; `CContract.contract_subgraph_gen`): contracting the
  components of a subgraph `H ≤ T` with an edge gives a smaller spherical map that keeps every edge
  between components;
* C4b `ConfigOccW.xGraph_labels` (PROVED, combinatorics): the X-graph has an edge, and no listed
  edge outside `X` and no edge of `G` joins two vertices of one X-component (the label argument);
* `ConfigOccW.contract_reducer` (PROVED from C4a + C4b): the reducer in the form `CEntry.colorable` uses. -/

/-- **C4a: contraction of a subgraph of a spherical map** (proved in `CContract.lean`).
Contracting each connected component of `H ≤ T` (with at least one edge) to one vertex gives a
spherical map `T'` on the same vertex type (merged-away vertices isolated) with smaller support,
and a vertex map `π` that is constant on `H`-components and keeps every edge of `T` between
different components. Proof: `contract_edge'` (one edge, any spherical map: chords `a w i` added in
the faces at `b`, the edges `b w i` erased, `b` isolated), iterated by strong induction on the
support (`contract_all`). -/
theorem contract_subgraph (T : SphericalMap n) (H : SimpleGraph (Fin n))
    (hH : H ≤ T.graph) (hne : ∃ x y, H.Adj x y) :
    ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
      Nat.card T'.graph.support < Nat.card T.graph.support ∧
      (∀ x y, H.Reachable x y → π x = π y) ∧
      (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y)) :=
  contract_subgraph_gen T H hH hne

/-- The X-graph of an occurrence: the contracted edges `ι a – ρ t` (`eqR`) and `ι a – ι b` (`eqI`),
among the listed adjacencies. -/
def xGraph (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (ρ : ℕ → Fin n) (ι : Fin cf.m → Fin n) :
    SimpleGraph (Fin n) :=
  SimpleGraph.fromRel fun x y =>
    (∃ (a : Fin cf.m) (t : ℕ), ringAdjOf cf a t = true ∧ eqR.contains (t, a.val) = true ∧
      x = ι a ∧ y = ρ t) ∨
    (∃ a b : Fin cf.m, intAdjOf cf a b = true ∧
      (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true ∧ x = ι a ∧ y = ι b)

theorem ite_beq_spec {p : Prop} [Decidable p] {u v : ℕ}
    (h : (if p then u == v else u != v) = true) : (p → u = v) ∧ (¬ p → u ≠ v) := by
  by_cases hp : p
  · rw [if_pos hp] at h; exact ⟨fun _ => by simpa using h, fun h' => absurd hp h'⟩
  · rw [if_neg hp] at h; exact ⟨fun h' => absurd h' hp, fun _ => by simpa using h⟩

/-- The X-component label of a vertex: `lbl[a]` at `ι a`, `lbl[m + t]` at a ring vertex `ρ t`
touched by `eqR`, and a fresh value elsewhere. -/
noncomputable def xLabel (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n)
    (ι : Fin cf.m → Fin n) (v : Fin n) : ℕ ⊕ ℕ := by
  classical
  exact if h : ∃ a : Fin cf.m, ι a = v then .inl (lbl.getD (Classical.choose h).val 0)
    else if h' : ∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v then
      .inl (lbl.getD (cf.m + Classical.choose h') 0)
    else .inr v.val

theorem xLabel_int (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n)
    {ι : Fin cf.m → Fin n} (hinj : Function.Injective ι) (a : Fin cf.m) :
    xLabel cf eqR lbl ρ ι (ι a) = .inl (lbl.getD a.val 0) := by
  have h : ∃ a', ι a' = ι a := ⟨a, rfl⟩
  unfold xLabel
  rw [dif_pos h, hinj (Classical.choose_spec h)]

theorem xLabel_ring (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) {ρ : ℕ → Fin n}
    {ι : Fin cf.m → Fin n} (hoff : ∀ t a, ρ t ≠ ι a) (hs : XRingSimple eqR cf.r ρ) (t : ℕ)
    (ht : t < cf.r) (htouch : ∃ a, (t, a) ∈ eqR) :
    xLabel cf eqR lbl ρ ι (ρ t) = .inl (lbl.getD (cf.m + t) 0) := by
  have h0 : ¬ ∃ a : Fin cf.m, ι a = ρ t := fun ⟨a, ha⟩ => hoff t a ha.symm
  have h' : ∃ t', t' < cf.r ∧ (∃ a, (t', a) ∈ eqR) ∧ ρ t' = ρ t := ⟨t, ht, htouch, rfl⟩
  unfold xLabel
  rw [dif_neg h0, dif_pos h']
  obtain ⟨ht', ⟨a', ha'⟩, he⟩ := Classical.choose_spec h'
  rw [← hs _ a' ha' ht' t ht he.symm]

theorem xLabel_fresh (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n)
    (ι : Fin cf.m → Fin n) (v : Fin n) (h0 : ¬ ∃ a : Fin cf.m, ι a = v)
    (h1 : ¬ ∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v) :
    xLabel cf eqR lbl ρ ι v = .inr v.val := by
  unfold xLabel
  rw [dif_neg h0, dif_neg h1]

/-- **No loops after contraction** (the conclusion of C4b): the X-graph has an edge, and none of
its components contains both ends of a listed edge outside `X` or of an edge of `G`. -/
def XLoopFree (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (ρ : ℕ → Fin n) (ι : Fin cf.m → Fin n)
    (G : SphericalMap n) : Prop :=
  (∃ x y, (xGraph cf eqR eqI ρ ι).Adj x y) ∧
  (∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → eqR.contains (t, a.val) = false →
    ¬ (xGraph cf eqR eqI ρ ι).Reachable (ι a) (ρ t)) ∧
  (∀ a b : Fin cf.m, intAdjOf cf a b = true →
    (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = false →
    ¬ (xGraph cf eqR eqI ρ ι).Reachable (ι b) (ι a)) ∧
  (∀ x y, G.Adj x y → ¬ (xGraph cf eqR eqI ρ ι).Reachable x y)

/-- **C4b: the label argument.** Under local admissibility and `XRingSimple`, the X-graph
has an edge, and its components never contain both ends of a listed edge outside `X` or of an edge
of `G`.

Proof: unpack `admissibleX` with `List.all_eq_true`. Put
`Λ (ι a) = lbl[a]`, `Λ (ρ t) = lbl[m + t]` for a ring position `t` touched by `eqR` (well defined by
`XRingSimple`), and `Λ v = B + v` otherwise, with `B` above every label. `Λ` is constant along
X-edges (X-edges join equal labels), hence on X-components (`Reachable` induction). A listed edge
outside `X` joins different labels; a `G`-edge joins two different ring vertices, which get distinct
ring labels or a fresh value. -/
theorem ConfigOccW.xGraph_labels (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleX cf eqR eqI lbl = true) (hloop : ∀ a, intAdjOf cf a a = false)
    {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hs : XRingSimple eqR cf.r ρ) :
    (∃ x y, (xGraph cf eqR eqI ρ ι).Adj x y) ∧
    (∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → eqR.contains (t, a.val) = false →
      ¬ (xGraph cf eqR eqI ρ ι).Reachable (ι a) (ρ t)) ∧
    (∀ a b : Fin cf.m, intAdjOf cf a b = true →
      (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = false →
      ¬ (xGraph cf eqR eqI ρ ι).Reachable (ι b) (ι a)) ∧
    (∀ x y, G.Adj x y → ¬ (xGraph cf eqR eqI ρ ι).Reachable x y) := by
  classical
  simp only [admissibleX, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    Array.all_eq_true, List.mem_range, Bool.or_eq_true, beq_iff_eq] at hadm
  obtain ⟨⟨⟨⟨⟨⟨hA1, -⟩, -⟩, hAR⟩, hAI⟩, hAm⟩, hArg⟩ := hadm
  set H := xGraph cf eqR eqI ρ ι with hH
  set Λ := xLabel cf eqR lbl ρ ι with hΛ
  -- the label facts at listed ring and interior edges
  have hRing : ∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → t < cf.r ∧
      (eqR.contains (t, a.val) = true → lbl.getD a.val 0 = lbl.getD (cf.m + t) 0) ∧
      (¬ eqR.contains (t, a.val) = true → lbl.getD a.val 0 ≠ lbl.getD (cf.m + t) 0) := by
    intro a t hat
    obtain ⟨i, hi, rfl⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hat)
    have := (hAm a.val a.isLt).1 i hi
    exact ⟨this.1, ite_beq_spec this.2⟩
  have hInt : ∀ a b : Fin cf.m, intAdjOf cf a b = true →
      ((eqI.contains (b.val, a.val) = true ∨ eqI.contains (a.val, b.val) = true) →
        lbl.getD a.val 0 = lbl.getD b.val 0) ∧
      (¬ (eqI.contains (b.val, a.val) = true ∨ eqI.contains (a.val, b.val) = true) →
        lbl.getD a.val 0 ≠ lbl.getD b.val 0) := by
    intro a b hab
    obtain ⟨i, hi, hb⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hab)
    have := (hAm a.val a.isLt).2 i hi
    rw [hb] at this
    exact ite_beq_spec this.2
  have htouch : ∀ (a : Fin cf.m) t, eqR.contains (t, a.val) = true → ∃ a', (t, a') ∈ eqR :=
    fun a t h => ⟨a.val, by simpa using h⟩
  -- Λ is constant along X-edges, hence on X-components
  have hadj : ∀ x y, H.Adj x y → Λ x = Λ y := by
    have one : ∀ x y, ((∃ (a : Fin cf.m) (t : ℕ), ringAdjOf cf a t = true ∧
        eqR.contains (t, a.val) = true ∧ x = ι a ∧ y = ρ t) ∨
        (∃ a b : Fin cf.m, intAdjOf cf a b = true ∧
          (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true ∧
          x = ι a ∧ y = ι b)) → Λ x = Λ y := by
      rintro x y (⟨a, t, hat, h, rfl, rfl⟩ | ⟨a, b, hab, h, rfl, rfl⟩)
      · obtain ⟨htr, heq, -⟩ := hRing a t hat
        rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj,
          xLabel_ring cf eqR lbl O.ringOff hs t htr (htouch a t h), heq h]
      · rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj, xLabel_int cf eqR lbl ρ O.ιinj,
          (hInt a b hab).1 (by simpa using h)]
    intro x y hxy
    rw [hH, xGraph, SimpleGraph.fromRel_adj] at hxy
    rcases hxy.2 with h | h
    · exact one x y h
    · exact (one y x h).symm
  have hreach : ∀ x y, H.Reachable x y → Λ x = Λ y := by
    rintro x y ⟨p⟩
    induction p with
    | nil => rfl
    | cons h _ ih => exact (hadj _ _ h).trans ih
  -- Λ at a vertex off the interior
  have hoffL : ∀ v, (∀ a, v ≠ ι a) →
      (∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v ∧ Λ v = .inl (lbl.getD (cf.m + t) 0)) ∨
      Λ v = .inr v.val := by
    intro v hv
    by_cases h1 : ∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v
    · obtain ⟨t, ht, htc, rfl⟩ := h1
      exact Or.inl ⟨t, ht, htc, rfl, xLabel_ring cf eqR lbl O.ringOff hs t ht htc⟩
    · exact Or.inr (xLabel_fresh cf eqR lbl ρ ι v (fun ⟨a, ha⟩ => hv a ha.symm) h1)
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- an X-edge exists
    by_cases hR0 : eqR = []
    · have hI0 : eqI ≠ [] := by
        intro h; rw [hR0, h] at hA1; simp at hA1
      obtain ⟨⟨b, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqI hI0
      obtain ⟨⟨ha, hb⟩, hc⟩ := hAI _ hp
      have hab : intAdjOf cf ⟨a, ha⟩ ⟨b, hb⟩ = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ι ⟨b, hb⟩, ?_⟩
      rw [hH, xGraph, SimpleGraph.fromRel_adj]
      refine ⟨fun e => ?_, Or.inl (Or.inr ⟨⟨a, ha⟩, ⟨b, hb⟩, hab, by simp [hp], rfl, rfl⟩)⟩
      have := O.ιinj e
      rw [← this, hloop] at hab
      exact Bool.false_ne_true hab
    · obtain ⟨⟨t, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqR hR0
      obtain ⟨ha, hc⟩ := hAR _ hp
      have hat : ringAdjOf cf ⟨a, ha⟩ t = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ρ t, ?_⟩
      rw [hH, xGraph, SimpleGraph.fromRel_adj]
      exact ⟨fun e => O.ringOff t _ e.symm,
        Or.inl (Or.inl ⟨⟨a, ha⟩, t, hat, by simp [hp], rfl, rfl⟩)⟩
  · -- a listed ring edge outside X
    intro a t hat h hr
    have e := hreach _ _ hr
    obtain ⟨htr, -, hne⟩ := hRing a t hat
    rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj] at e
    rcases hoffL (ρ t) (fun b => O.ringOff t b) with ⟨t', ht', htc, he, hl⟩ | hl
    · rw [← hΛ, hl] at e
      have : t = t' := hs t' _ htc.choose_spec ht' t htr he.symm
      subst this
      exact hne (fun h' => by rw [h] at h'; exact Bool.false_ne_true h') (Sum.inl_injective e)
    · rw [← hΛ, hl] at e
      exact Sum.inl_ne_inr e
  · -- a listed interior edge outside X
    intro a b hab h hr
    have e := hreach _ _ hr
    rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj, xLabel_int cf eqR lbl ρ O.ιinj] at e
    exact (hInt a b hab).2 (by simpa using h) (Sum.inl_injective e).symm
  · -- an edge of G
    intro x y hxy hr
    have e := hreach _ _ hr
    obtain ⟨-, hx, hy⟩ := (O.hG x y).1 hxy
    have hne : x ≠ y := G.graph.ne_of_adj hxy
    rcases hoffL x hx with ⟨s, hs', -, rfl, hlx⟩ | hlx <;>
      rcases hoffL y hy with ⟨t, ht', -, rfl, hly⟩ | hly <;> rw [hlx, hly] at e
    · have hst : s ≠ t := fun h => hne (by rw [h])
      rcases hArg s hs' t ht' with h | h
      · exact hst h
      · exact (by simpa using h : lbl.getD (cf.m + s) 0 ≠ lbl.getD (cf.m + t) 0) (Sum.inl_injective e)
    · exact Sum.inl_ne_inr e
    · exact Sum.inr_ne_inl e
    · exact hne (Fin.ext (Sum.inr_injective e))

/-- **C4 from a contraction of the X-graph** (proved from `hcon` and C4b). Let `cf` occur in
`T` exactly (`OccExact`), with `X = eqR ∪ eqI` locally admissible and globally simple. Then there
are a spherical map `T'` of smaller support and a vertex map `π` that keeps every edge of `G`,
identifies each listed edge in `X` and keeps each other listed edge. -/
theorem ConfigOccW.contract_reducer_of (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleX cf eqR eqI lbl = true)
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

/-- **C4: contracting `X` gives a smaller reducer** (proved from C4a and C4b). -/
theorem ConfigOccW.contract_reducer (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleX cf eqR eqI lbl = true)
    (hloop : ∀ a, intAdjOf cf a a = false)
    (hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hs : XRingSimple eqR cf.r ρ) :
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
          T'.Adj (π (ι b)) (π (ι a)))) :=
  ConfigOccW.contract_reducer_of cf eqR eqI lbl hadm hloop hrr O hex
    (ConfigOccW.xGraph_labels cf eqR eqI lbl hadm hloop O hs)
    (fun H _ hle hne => contract_subgraph T H hle hne)

/-- The X-graph of a single interior edge `p0 = (b, a)`: every edge is `ι a – ι b`. -/
theorem xGraph_one_edge (cf : Conf) (p0 : ℕ × ℕ) (ρ : ℕ → Fin n) (ι : Fin cf.m → Fin n)
    {x y : Fin n} (h : (xGraph cf [] [p0] ρ ι).Adj x y) :
    ∃ a b : Fin cf.m, (b.val, a.val) = p0 ∧ s(x, y) = s(ι a, ι b) := by
  rw [xGraph, SimpleGraph.fromRel_adj] at h
  obtain ⟨-, h⟩ := h
  rcases h with (⟨a, t, -, hc, -, -⟩ | ⟨a, b, -, hc, rfl, rfl⟩) |
      (⟨a, t, -, hc, -, -⟩ | ⟨a, b, -, hc, rfl, rfl⟩)
  · simp at hc
  · simp only [List.contains_cons, List.contains_nil, Bool.or_false, Bool.or_eq_true,
      beq_iff_eq] at hc
    rcases hc with hc | hc
    · exact ⟨a, b, hc, rfl⟩
    · exact ⟨b, a, hc, Sym2.eq_swap⟩
  · simp at hc
  · simp only [List.contains_cons, List.contains_nil, Bool.or_false, Bool.or_eq_true,
      beq_iff_eq] at hc
    rcases hc with hc | hc
    · exact ⟨a, b, hc, Sym2.eq_swap⟩
    · exact ⟨b, a, hc, rfl⟩

/-- Any two edges of a single-interior-edge X-graph are the same edge. -/
theorem xGraph_one (cf : Conf) (p0 : ℕ × ℕ) (ρ : ℕ → Fin n) (ι : Fin cf.m → Fin n)
    {x y x' y' : Fin n} (h : (xGraph cf [] [p0] ρ ι).Adj x y)
    (h' : (xGraph cf [] [p0] ρ ι).Adj x' y') : s(x, y) = s(x', y') := by
  obtain ⟨a, b, hab, e⟩ := xGraph_one_edge cf p0 ρ ι h
  obtain ⟨a', b', hab', e'⟩ := xGraph_one_edge cf p0 ρ ι h'
  have ha : a = a' := Fin.ext (congrArg Prod.snd (hab.trans hab'.symm))
  have hb : b = b' := Fin.ext (congrArg Prod.fst (hab.trans hab'.symm))
  rw [e, e', ha, hb]

/-! ## C5 for folded rings: fold-safe entries (no `XRingSimple`)

A fold (`ρ p = ρ q` for positions `p ≠ q`) can only create a loop if it identifies a kept ring
neighbour `s` of an X-component with the component's ring vertex `t` (D1), or the ring vertices
`t`, `t'` of two X-components joined by a kept interior edge (D2). `foldSafeX` (decidable, per key)
checks that every such pair is excluded by `exclB`. A pair is excluded when the positions are
consecutive on the ring (`G`-adjacent, so distinct); or when one interior vertex sees both (`NbrInj`:
the listed neighbours of an interior vertex are distinct vertices of `T`, which the true degree
gives); or when two adjacent interior vertices see them. In that last case the common vertex would
close a triangle with the interior edge. With no separating triangle the triangle is facial, so the
vertex is a configuration apex of that edge (`ApexFacts`), and `NbrInj` at both ends gives `p = q`.
This is option (a) for cycles of length 3. Pairs that need a cycle of length 4 or 5 are excluded by
`cycEx` (see "Folds excluded by a short cycle" below), using `NoShortSepCycle`.

Status (19 Oct 2026): with one label per X-component, `foldSafeX` holds for all 89 ring-X entries
(`CGLUE-XRING-ENTRIES.txt`). 85 need only the triangle rule. Four need the short-cycle rule:
`f7_..57556_...65..`, `f7_..57556_...66..` and `f7_5675767_.5.....` (4-cycles), and
`f9_..5565675_......5..` (4- and 5-cycles; `cfF9_fold`). -/

/-- Ring position `t` is touched by `eqR`. -/
def touchedB (eqR : List (ℕ × ℕ)) (t : ℕ) : Bool := eqR.any (fun p => p.1 == t)

/-- Positions `p` and `q` cannot be folded together (see the section docstring). -/
def exclB (cf : Conf) (p q : ℕ) : Bool :=
  q == (p + 1) % cf.r || p == (q + 1) % cf.r ||
  (List.range cf.m).any (fun c => decide (p ∈ cf.ringAdj[c]!) &&
    (decide (q ∈ cf.ringAdj[c]!) ||
      (cf.intAdj[c]!).toList.any (fun a => decide (a < cf.m) && decide (q ∈ cf.ringAdj[a]!))))

/-! ### Folds excluded by a short cycle (option (a), cycles of length 4 and 5)

If `ρ p = ρ q` and an interior path `c₀ … c_{k-1}` (`2 ≤ k ≤ 4`) runs from a neighbour of `p` to a
neighbour of `q`, then `ρ p, ι c₀, …, ι c_{k-1}` is a cycle of `T` of length `k + 1 ≤ 5`. Take a path
edge `c_j c_{j+1}` whose ends have no common ring neighbour. The two faces on that edge have apexes
that are common neighbours of its ends, so by `CommonNbr` and `nbr` they are interior vertices
adjacent to both. If none of these lies on the path, the two apexes are off the cycle and lie on
opposite sides of it, since the cycle's potential changes across the edge. For `k = 4` each apex
also has an interior neighbour off the path, which lies on the same side (`side_step_cyc`). Then
`NoShortSepCycle` is contradicted, so `ρ p ≠ ρ q`. The certificate is checked by `cycCertB`,
and `cycEx` searches all interior paths of 2 to 4 vertices. -/

/-- A short-cycle certificate for excluding the fold `ρ p = ρ q`. -/
def cycCertB (cf : Conf) (p q : ℕ) (path : List ℕ) (j : ℕ) : Bool :=
  decide (2 ≤ path.length) && decide (path.length ≤ 4) && decide path.Nodup &&
  path.all (fun i => decide (i < cf.m)) &&
  decide (p ∈ cf.ringAdj[path.getD 0 0]!) && decide (q ∈ cf.ringAdj[path.getD (path.length - 1) 0]!) &&
  (List.range (path.length - 1)).all (fun i => decide (path.getD (i + 1) 0 ∈ cf.intAdj[path.getD i 0]!)) &&
  decide (j + 1 < path.length) &&
  (cf.ringAdj[path.getD j 0]!).toList.all (fun s => !decide (s ∈ cf.ringAdj[path.getD (j + 1) 0]!)) &&
  (cf.intAdj[path.getD j 0]!).toList.all (fun e => !decide (e ∈ cf.intAdj[path.getD (j + 1) 0]!) ||
    (!decide (e ∈ path) && (decide (path.length < 4) ||
      (cf.intAdj[e]!).toList.any (fun f => decide (f < cf.m) && !decide (f ∈ path)))))

/-- One step of the path enumeration. -/
def extendP (cf : Conf) (ps : List (List ℕ)) : List (List ℕ) :=
  ps.flatMap (fun p => (cf.intAdj[p.getLast!]!).toList.map (fun x => p ++ [x]))

/-- Candidate interior paths with 2 to 4 vertices. -/
def candP (cf : Conf) : List (List ℕ) :=
  let p1 := (List.range cf.m).map (fun c => [c])
  let p2 := extendP cf p1
  let p3 := extendP cf p2
  p2 ++ p3 ++ extendP cf p3

/-- Search for a short-cycle certificate. -/
def cycEx (cf : Conf) (p q : ℕ) : Bool :=
  (candP cf).any (fun path => (List.range 3).any (fun j => cycCertB cf p q path j))

/-- **Fold safety** (decidable, per key): every D1 and D2 pair is excluded. -/
def foldSafeX (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ) : Bool :=
  let L : ℕ → ℕ := fun i => lbl.getD i 0
  (List.range cf.m).all (fun a =>
    (cf.ringAdj[a]!).all (fun s => eqR.contains (s, a) ||
      (List.range cf.r).all (fun t =>
        !touchedB eqR t || L (cf.m + t) != L a || s == t || exclB cf s t || cycEx cf s t)) &&
    (cf.intAdj[a]!).all (fun b => eqI.contains (b, a) || eqI.contains (a, b) ||
      (List.range cf.r).all (fun t => (List.range cf.r).all (fun t' =>
        !touchedB eqR t || !touchedB eqR t' || L (cf.m + t) != L a || L (cf.m + t') != L b ||
          t == t' || exclB cf t t' || cycEx cf t t'))))

/-- The listed ring neighbours of each interior vertex are distinct vertices of `T`. This follows
from the true degree (`T.degree (ι a)` equals the number of listed neighbours) with `nbr` and
`OccExact`. -/
def NbrInj (r : ℕ) (ρ : ℕ → Fin n) (ringAdj : Fin m → ℕ → Bool) : Prop :=
  ∀ c p q, ringAdj c p = true → ringAdj c q = true → p < r → q < r → ρ p = ρ q → p = q

/-- The apex of a facial triangle on a listed interior edge is a configuration vertex adjacent to both
ends. This follows from the rotation of `T` at the interior vertices being the configuration's rotation
(`occ24`'s `Occ`, Job 26's 2-ball embedding). -/
def ApexFacts (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (ι : Fin m → Fin n)
    (intAdj : Fin m → Fin m → Bool) (ringAdj : Fin m → ℕ → Bool) : Prop :=
  ∀ c a, intAdj c a = true → ∀ w, Facial T (ι c) (ι a) w →
    (∃ e, w = ι e) ∨ ∃ p, p < r ∧ w = ρ p ∧ ringAdj c p = true ∧ ringAdj a p = true

/-- Every common neighbour in `T` of the two ends of a listed interior edge is a configuration
vertex adjacent to both. -/
def CommonNbr (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (ι : Fin m → Fin n)
    (intAdj : Fin m → Fin m → Bool) (ringAdj : Fin m → ℕ → Bool) : Prop :=
  ∀ c a, intAdj c a = true → ∀ w, T.Adj (ι c) w → T.Adj (ι a) w →
    (∃ e, w = ι e) ∨ ∃ p, p < r ∧ w = ρ p ∧ ringAdj c p = true ∧ ringAdj a p = true

/-- With no separating triangle, apex facts give common-neighbour facts. -/
theorem commonNbr_of_apex {r : ℕ} {ι : Fin m → Fin n} {intAdj : Fin m → Fin m → Bool}
    {ringAdj : Fin m → ℕ → Bool} (hns : NoSep T) (hex : OccExact T r ρ ι intAdj ringAdj)
    (hA : ApexFacts T r ρ ι intAdj ringAdj) : CommonNbr T r ρ ι intAdj ringAdj :=
  fun c a h w h1 h2 => hA c a h w (hns _ _ _ (hex.1 c a h) h2 h1.symm)

/-- **Excluded pairs do not fold.** -/
theorem excl_sound (cf : Conf) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hNI : NbrInj cf.r ρ (ringAdjOf cf)) (hCN : CommonNbr T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    {p q : ℕ} (hp : p < cf.r) (hq : q < cf.r) (hpq : p ≠ q) (h : exclB cf p q = true) :
    ρ p ≠ ρ q := by
  intro he
  simp only [exclB, Bool.or_eq_true, beq_iff_eq, List.any_eq_true, List.mem_range,
    Bool.and_eq_true, decide_eq_true_eq] at h
  simp only [List.any_eq_true, Array.mem_toList_iff, Bool.and_eq_true,
    decide_eq_true_eq] at h
  rcases h with (h | h) | ⟨c, hc, hcp, h⟩
  · have a := O.ring.adj p
    rw [← per_mod' O.ring.per (p + 1), ← h, ← he] at a
    exact G.graph.ne_of_adj a rfl
  · have a := O.ring.adj q
    rw [← per_mod' O.ring.per (q + 1), ← h, he] at a
    exact G.graph.ne_of_adj a rfl
  · have hcp' : ringAdjOf cf ⟨c, hc⟩ p = true := decide_eq_true (by simpa using hcp)
    rcases h with hcq | ⟨a, ha, ham, haq⟩
    · exact hpq (hNI ⟨c, hc⟩ p q hcp' (decide_eq_true (by simpa using hcq)) hp hq he)
    · have hca : intAdjOf cf ⟨c, hc⟩ ⟨a, ham⟩ = true := decide_eq_true (by simpa using ha)
      have haq' : ringAdjOf cf ⟨a, ham⟩ q = true := decide_eq_true (by simpa using haq)
      have h1 := hex.2 ⟨c, hc⟩ p hp hcp'
      have h2 := hex.2 ⟨a, ham⟩ q hq haq'
      rw [← he] at h2
      rcases hCN _ _ hca (ρ p) h1 h2 with ⟨e, he'⟩ | ⟨p', hp', he', hc', ha'⟩
      · exact O.ringOff p e he'
      · have e1 := hNI _ p' p hc' hcp' hp' hp he'.symm
        have e2 := hNI _ p' q ha' haq' hp' hq (he'.symm.trans he)
        exact hpq (e1.symm.trans e2)

/-- The side of a cycle propagates along an edge off the cycle. -/
theorem side_step_cyc {r : ℕ} {ρ' : ℕ → Fin n} {c : T.Face → ZMod 2} (C : Cyc T r ρ')
    (hc : CycPotential T r ρ' c) {x y : Fin n} (hx : ¬ OnCyc r ρ' x)
    (hy : ¬ OnCyc r ρ' y) (hxy : T.Adj x y) {b : ZMod 2} (h : OnSide T c b x) :
    OnSide T c b y := by
  intro e he
  let d : T.Dart := ⟨(x, y), hxy⟩
  have h0 := cycInd_off' C d hx
  have hp := hc d
  rw [h0] at hp
  have hd : c (T.faceOf d) = b := h d rfl
  have key : ∀ u v : ZMod 2, 0 = u + v → v = u := by decide
  have hs : c (T.faceOf d.symm) = b := (key _ _ hp).trans hd
  rw [side_constC' C hc hy e d.symm he rfl]
  exact hs

/-- **The two apexes of a cycle edge lie on opposite sides** (when both are off the cycle). -/
theorem apex_sides {r : ℕ} {ρ' : ℕ → Fin n} {c : T.Face → ZMod 2} (C : Cyc T r ρ')
    (hc : CycPotential T r ρ' c) (k : ℕ) {w1 w2 : Fin n}
    (h1 : Nx T (ρ' k) (ρ' (k + 1)) w1) (h2 : Nx T (ρ' (k + 1)) (ρ' k) w2)
    (o1 : ¬ OnCyc r ρ' w1) (o2 : ¬ OnCyc r ρ' w2) :
    ∃ b, OnSide T c b w1 ∧ OnSide T c (b + 1) w2 := by
  obtain ⟨a1, e1⟩ := h1
  obtain ⟨a2, e2⟩ := h2
  let d : T.Dart := ⟨(ρ' k, ρ' (k + 1)), a1⟩
  have s1 := onSide_of_dartC' C hc o1 (T.rotation.faceNext (T.rotation.next d))
    (by rw [RotationSystem.face_next_fst]; exact e1)
  rw [faceNext_face, faceOf_next] at s1
  have s2 := onSide_of_dartC' C hc o2 (T.rotation.faceNext (T.rotation.next d.symm))
    (by rw [RotationSystem.face_next_fst]; exact e2)
  rw [faceNext_face, faceOf_next, Dart.symm_symm] at s2
  have hp := hc d
  rw [show cycInd T r ρ' (RotationSystem.edgeOfDart d) = 1 from cycInd_cycle' C k] at hp
  have key : ∀ u v : ZMod 2, 1 = u + v → u = v + 1 := by decide
  refine ⟨_, s1, ?_⟩
  rw [← key _ _ hp]
  exact s2

theorem succ_mod_cases (t K : ℕ) (hK : 1 < K) :
    ((t + 1) % K = t % K + 1 ∧ t % K + 1 < K) ∨ ((t + 1) % K = 0 ∧ t % K + 1 = K) := by
  have hlt := Nat.mod_lt t (by omega : 0 < K)
  rw [Nat.add_mod, Nat.mod_eq_of_lt hK]
  by_cases h : t % K + 1 < K
  · exact Or.inl ⟨Nat.mod_eq_of_lt h, h⟩
  · have e : t % K + 1 = K := by omega
    exact Or.inr ⟨by rw [e, Nat.mod_self], e⟩

/-- **Short-cycle exclusion is sound** in a triangulation with no short separating cycle. -/
theorem cyc_sound (cf : Conf) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hCN : CommonNbr T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hloop : ∀ a, intAdjOf cf a a = false) (htri : T.Triangulated)
    (hNS : ClaimGlue.NoShortSepCycle T)
    {p q : ℕ} (hp : p < cf.r) (hq : q < cf.r) {path : List ℕ} {j : ℕ}
    (h : cycCertB cf p q path j = true) : ρ p ≠ ρ q := by
  classical
  intro he
  simp only [cycCertB, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range,
    Bool.or_eq_true, Bool.not_eq_true', decide_eq_false_iff_not, List.any_eq_true,
    Array.mem_toList_iff] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨hk2, hk4⟩, hnd⟩, hm⟩, hp0⟩, hqk⟩, hcons⟩, hj⟩, hring⟩, hint⟩ := h
  set k := path.length with hk
  set P : ℕ → ℕ := fun i => path.getD i 0 with hP
  have gd : ∀ i (hi : i < k), path.getD i 0 = path[i] := fun i hi => by
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi, Option.getD_some]
  have hPmem : ∀ i, i < k → P i ∈ path := fun i hi => by
    simp only [hP, gd i hi]; exact List.getElem_mem hi
  have hPm : ∀ i, i < k → P i < cf.m := fun i hi => hm _ (hPmem i hi)
  have hPinj : ∀ i i', i < k → i' < k → P i = P i' → i = i' := fun i i' hi hi' e =>
    (hnd.getD_inj hi hi').1 e
  let ιN : ℕ → Fin n := fun i => if h : i < cf.m then ι ⟨i, h⟩ else ρ p
  have hιN : ∀ i (hi : i < k), ιN (P i) = ι ⟨P i, hPm i hi⟩ := fun i hi => dif_pos _
  let ρ' : ℕ → Fin n := fun t => if t % (k + 1) = 0 then ρ p else ιN (P (t % (k + 1) - 1))
  have hK : 1 < k + 1 := by omega
  -- adjacencies
  have aInt : ∀ i, i + 1 < k → T.Adj (ιN (P i)) (ιN (P (i + 1))) := fun i hi => by
    rw [hιN i (by omega), hιN (i + 1) hi]
    exact hex.1 _ _ (decide_eq_true (hcons i (by omega)))
  have aFirst : T.Adj (ρ p) (ιN (P 0)) := by
    rw [hιN 0 (by omega)]; exact (hex.2 _ p hp (decide_eq_true hp0)).symm
  have aLast : T.Adj (ιN (P (k - 1))) (ρ p) := by
    rw [hιN (k - 1) (by omega), he]; exact hex.2 _ q hq (decide_eq_true hqk)
  have C : Cyc T (k + 1) ρ' := by
    refine ⟨by omega, fun t => ?_, fun t => ?_, fun s t hs ht e => ?_⟩
    · simp only [ρ', Nat.add_mod_right]
    · rcases succ_mod_cases t (k + 1) hK with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · simp only [ρ', h1, Nat.add_eq_zero_iff, one_ne_zero, and_false, if_false]
        by_cases h0 : t % (k + 1) = 0
        · rw [if_pos h0, h0]; exact aFirst
        · rw [if_neg h0, show t % (k + 1) + 1 - 1 = (t % (k + 1) - 1) + 1 by omega]
          exact aInt _ (by omega)
      · simp only [ρ', h1, if_true]
        rw [if_neg (by omega), show t % (k + 1) - 1 = k - 1 by omega]
        exact aLast
    · simp only [ρ', Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at e
      by_cases hs0 : s = 0 <;> by_cases ht0 : t = 0
      · omega
      · rw [if_pos hs0, if_neg ht0, hιN _ (by omega)] at e; exact absurd e (O.ringOff _ _)
      · rw [if_neg hs0, if_pos ht0, hιN _ (by omega)] at e; exact absurd e.symm (O.ringOff _ _)
      · rw [if_neg hs0, if_neg ht0, hιN _ (by omega), hιN _ (by omega)] at e
        have := hPinj _ _ (by omega) (by omega) (congrArg Fin.val (O.ιinj e))
        omega
  -- off the cycle
  have off : ∀ e : Fin cf.m, e.val ∉ path → ¬ OnCyc (k + 1) ρ' (ι e) := by
    rintro e he' ⟨t, ht, hte⟩
    simp only [ρ', Nat.mod_eq_of_lt ht] at hte
    by_cases ht0 : t = 0
    · rw [if_pos ht0] at hte; exact O.ringOff _ _ hte
    · rw [if_neg ht0, hιN _ (by omega)] at hte
      have := congrArg Fin.val (O.ιinj hte)
      exact he' (this ▸ hPmem _ (by omega))
  -- the edge
  have hu : ρ' (j + 1) = ιN (P j) := by
    simp only [ρ', Nat.mod_eq_of_lt (show j + 1 < k + 1 by omega)]; rw [if_neg (by omega)]; rfl
  have hv : ρ' (j + 1 + 1) = ιN (P (j + 1)) := by
    simp only [ρ', Nat.mod_eq_of_lt (show j + 1 + 1 < k + 1 by omega)]; rw [if_neg (by omega)]; rfl
  set ci : Fin cf.m := ⟨P j, hPm j (by omega)⟩
  set ci' : Fin cf.m := ⟨P (j + 1), hPm (j + 1) hj⟩
  have huv : intAdjOf cf ci ci' = true := decide_eq_true (hcons j (by omega))
  rw [hιN j (by omega)] at hu
  rw [hιN (j + 1) hj] at hv
  -- apexes are interior common neighbours
  have apex : ∀ w, T.Adj (ι ci) w → T.Adj (ι ci') w →
      ∃ e : Fin cf.m, w = ι e ∧ ¬ OnCyc (k + 1) ρ' (ι e) ∧
        (k = 4 → ∃ f : Fin cf.m, f ≠ e ∧ T.Adj (ι e) (ι f) ∧ ¬ OnCyc (k + 1) ρ' (ι f)) := by
    intro w h1 h2
    rcases hCN ci ci' huv w h1 h2 with ⟨e, rfl⟩ | ⟨p', -, rfl, hc1, hc2⟩
    · have he1 : intAdjOf cf ci e = true := by
        rcases O.nbr ci _ h1 with ⟨b, hb, hb'⟩ | ⟨t, -, ht, -⟩
        · rwa [O.ιinj hb]
        · exact absurd ht.symm (O.ringOff _ _)
      have he2 : intAdjOf cf ci' e = true := by
        rcases O.nbr ci' _ h2 with ⟨b, hb, hb'⟩ | ⟨t, -, ht, -⟩
        · rwa [O.ιinj hb]
        · exact absurd ht.symm (O.ringOff _ _)
      rcases hint e.val (of_decide_eq_true he1) with hn | ⟨hn, hf⟩
      · exact absurd (of_decide_eq_true he2) hn
      refine ⟨e, rfl, off e hn, fun h4 => ?_⟩
      rcases hf with hf | ⟨f, hf, hfm, hfp⟩
      · omega
      refine ⟨⟨f, hfm⟩, fun hfe => ?_, hex.1 _ _ (decide_eq_true hf), off _ hfp⟩
      have := hloop e
      rw [← hfe] at this
      simp only [intAdjOf, decide_eq_false_iff_not] at this
      exact this (by simpa [← hfe] using hf)
    · exact absurd (of_decide_eq_true hc2) (hring p' (of_decide_eq_true hc1))
  -- the two apexes
  obtain ⟨c, hc⟩ := exists_cycPotential' C
  have n1 : Nx T (ρ' (j + 1)) (ρ' (j + 1 + 1)) (T.rotation.next ⟨(ρ' (j + 1), ρ' (j + 1 + 1)), C.adj (j + 1)⟩).snd :=
    ⟨C.adj (j + 1), rfl⟩
  have n2 : Nx T (ρ' (j + 1 + 1)) (ρ' (j + 1))
      (T.rotation.next ⟨(ρ' (j + 1 + 1), ρ' (j + 1)), (C.adj (j + 1)).symm⟩).snd :=
    ⟨(C.adj (j + 1)).symm, rfl⟩
  generalize (T.rotation.next ⟨(ρ' (j + 1), ρ' (j + 1 + 1)), C.adj (j + 1)⟩).snd = w1 at n1
  generalize (T.rotation.next ⟨(ρ' (j + 1 + 1), ρ' (j + 1)), (C.adj (j + 1)).symm⟩).snd = w2 at n2
  have n1' := n1
  have n2' := n2
  rw [hu, hv] at n1' n2'
  obtain ⟨e1, rfl, o1, x1⟩ := apex w1 (nx_adj_right n1') (nx_adj_left (nx_tri htri n1').2)
  obtain ⟨e2, rfl, o2, x2⟩ := apex w2 (nx_adj_left (nx_tri htri n2').2) (nx_adj_right n2')
  obtain ⟨b, s1, s2⟩ := apex_sides C hc (j + 1) n1 n2 o1 o2
  have a1 : T.Adj (ι e1) (ι ci) := (nx_adj_right n1').symm
  have a2 : T.Adj (ι e2) (ι ci') := (nx_adj_right n2').symm
  have zb : ∀ b' : ZMod 2, b' = b ∨ b' = b + 1 := by
    intro b'; generalize b = x; revert b' x; decide
  refine hNS (k + 1) ρ' c C (by omega) hc ?_ ?_
  · rcases zb 0 with h0 | h0 <;> rcases zb 1 with h1 | h1
    · exact absurd (h0.trans h1.symm) (by decide)
    · exact ⟨⟨_, _, o1, h0 ▸ s1, a1⟩, ⟨_, _, o2, h1 ▸ s2, a2⟩⟩
    · exact ⟨⟨_, _, o2, h0 ▸ s2, a2⟩, ⟨_, _, o1, h1 ▸ s1, a1⟩⟩
    · exact absurd (h0.trans h1.symm) (by decide)
  · intro h5 b'
    obtain ⟨f1, hf1, af1, of1⟩ := x1 (by omega)
    obtain ⟨f2, hf2, af2, of2⟩ := x2 (by omega)
    have t1 := side_step_cyc C hc o1 of1 af1 s1
    have t2 := side_step_cyc C hc o2 of2 af2 s2
    rcases zb b' with rfl | rfl
    · exact ⟨_, _, _, _, fun h => hf1 (O.ιinj h).symm, o1, s1, a1, of1, t1, af1.symm⟩
    · exact ⟨_, _, _, _, fun h => hf2 (O.ιinj h).symm, o2, s2, a2, of2, t2, af2.symm⟩

/-- `cycEx` is sound. -/
theorem cycEx_sound (cf : Conf) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hCN : CommonNbr T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hloop : ∀ a, intAdjOf cf a a = false) (htri : T.Triangulated)
    (hNS : ClaimGlue.NoShortSepCycle T)
    {p q : ℕ} (hp : p < cf.r) (hq : q < cf.r) (h : cycEx cf p q = true) : ρ p ≠ ρ q := by
  simp only [cycEx, List.any_eq_true] at h
  obtain ⟨path, -, j, -, h⟩ := h
  exact cyc_sound cf O hex hCN hloop htri hNS hp hq h

/-- The X-class of an interior vertex with label `l`: the ring vertex of the touched position with
that label, if any, and `l` otherwise. -/
noncomputable def kInt (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n) (l : ℕ) :
    Fin n ⊕ (ℕ ⊕ Fin n) := by
  classical
  exact if h : ∃ t, t < cf.r ∧ touchedB eqR t = true ∧ lbl.getD (cf.m + t) 0 = l then
    .inl (ρ (Classical.choose h)) else .inr (.inl l)

/-- The X-class of a vertex of `T`, constant on X-components even when the ring folds. -/
noncomputable def xKappa (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n)
    (ι : Fin cf.m → Fin n) (v : Fin n) : Fin n ⊕ (ℕ ⊕ Fin n) := by
  classical
  exact if h : ∃ a : Fin cf.m, ι a = v then kInt cf eqR lbl ρ (lbl.getD (Classical.choose h).val 0)
    else if ∃ t, t < cf.r ∧ touchedB eqR t = true ∧ ρ t = v then .inl v else .inr (.inr v)

theorem kInt_touched (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n)
    (hArg : ∀ s t, s < cf.r → t < cf.r → s = t ∨ lbl.getD (cf.m + s) 0 ≠ lbl.getD (cf.m + t) 0)
    {t : ℕ} (ht : t < cf.r) (htt : touchedB eqR t = true) :
    kInt cf eqR lbl ρ (lbl.getD (cf.m + t) 0) = .inl (ρ t) := by
  have h : ∃ t', t' < cf.r ∧ touchedB eqR t' = true ∧
      lbl.getD (cf.m + t') 0 = lbl.getD (cf.m + t) 0 := ⟨t, ht, htt, rfl⟩
  unfold kInt
  rw [dif_pos h]
  obtain ⟨h1, -, h3⟩ := Classical.choose_spec h
  rcases hArg _ t h1 ht with e | e
  · rw [e]
  · exact absurd h3 e

theorem kInt_cases (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n) (l : ℕ) :
    (∃ t, t < cf.r ∧ touchedB eqR t = true ∧ lbl.getD (cf.m + t) 0 = l ∧
      kInt cf eqR lbl ρ l = .inl (ρ t)) ∨ kInt cf eqR lbl ρ l = .inr (.inl l) := by
  unfold kInt
  by_cases h : ∃ t, t < cf.r ∧ touchedB eqR t = true ∧ lbl.getD (cf.m + t) 0 = l
  · rw [dif_pos h]
    obtain ⟨h1, h2, h3⟩ := Classical.choose_spec h
    exact Or.inl ⟨_, h1, h2, h3, rfl⟩
  · rw [dif_neg h]; exact Or.inr rfl

theorem xKappa_int (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n)
    {ι : Fin cf.m → Fin n} (hinj : Function.Injective ι) (a : Fin cf.m) :
    xKappa cf eqR lbl ρ ι (ι a) = kInt cf eqR lbl ρ (lbl.getD a.val 0) := by
  have h : ∃ a', ι a' = ι a := ⟨a, rfl⟩
  unfold xKappa
  rw [dif_pos h, hinj (Classical.choose_spec h)]

theorem xKappa_off (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n)
    (ι : Fin cf.m → Fin n) {v : Fin n} (hv : ∀ a, v ≠ ι a) :
    ((∃ t, t < cf.r ∧ touchedB eqR t = true ∧ ρ t = v) ∧ xKappa cf eqR lbl ρ ι v = .inl v) ∨
    ((¬ ∃ t, t < cf.r ∧ touchedB eqR t = true ∧ ρ t = v) ∧
      xKappa cf eqR lbl ρ ι v = .inr (.inr v)) := by
  have h0 : ¬ ∃ a : Fin cf.m, ι a = v := fun ⟨a, ha⟩ => hv a ha.symm
  unfold xKappa
  rw [dif_neg h0]
  by_cases h1 : ∃ t, t < cf.r ∧ touchedB eqR t = true ∧ ρ t = v
  · rw [if_pos h1]; exact Or.inl ⟨h1, rfl⟩
  · rw [if_neg h1]; exact Or.inr ⟨h1, rfl⟩

theorem touchedB_of_mem {eqR : List (ℕ × ℕ)} {t a : ℕ} (h : (t, a) ∈ eqR) : touchedB eqR t = true :=
  List.any_eq_true.2 ⟨(t, a), h, by simp⟩

/-- **C4b for folded rings.** Under local admissibility, fold safety, `NbrInj` and `CommonNbr`
(no `XRingSimple`), the contraction creates no loop. -/
theorem ConfigOccW.xGraph_labels_fold (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleX cf eqR eqI lbl = true) (hsafe : foldSafeX cf eqR eqI lbl = true)
    (hloop : ∀ a, intAdjOf cf a a = false) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hNI : NbrInj cf.r ρ (ringAdjOf cf)) (hCN : CommonNbr T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (htri : T.Triangulated) (hNS : ClaimGlue.NoShortSepCycle T) :
    XLoopFree cf eqR eqI ρ ι G := by
  classical
  have hX := hadm
  simp only [admissibleX, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    Array.all_eq_true, List.mem_range, Bool.or_eq_true, beq_iff_eq] at hadm
  obtain ⟨⟨⟨⟨⟨⟨hA1, -⟩, -⟩, hAR⟩, hAI⟩, hAm⟩, hArg⟩ := hadm
  have hArg' : ∀ s t, s < cf.r → t < cf.r →
      s = t ∨ lbl.getD (cf.m + s) 0 ≠ lbl.getD (cf.m + t) 0 := by
    intro s t hs ht
    rcases hArg s hs t ht with h | h
    · exact Or.inl h
    · exact Or.inr (by simpa using h)
  simp only [foldSafeX, Bool.and_eq_true, List.all_eq_true, Array.all_eq_true, List.mem_range,
    Bool.or_eq_true, beq_iff_eq, Bool.not_eq_true', bne_iff_ne, ne_eq] at hsafe
  set H := xGraph cf eqR eqI ρ ι with hH
  set κ := xKappa cf eqR lbl ρ ι with hκ
  have hRing : ∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → t < cf.r ∧
      (eqR.contains (t, a.val) = true → lbl.getD a.val 0 = lbl.getD (cf.m + t) 0) ∧
      (¬ eqR.contains (t, a.val) = true → lbl.getD a.val 0 ≠ lbl.getD (cf.m + t) 0) := by
    intro a t hat
    obtain ⟨i, hi, rfl⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hat)
    have := (hAm a.val a.isLt).1 i hi
    exact ⟨this.1, ite_beq_spec this.2⟩
  have hInt : ∀ a b : Fin cf.m, intAdjOf cf a b = true →
      ((eqI.contains (b.val, a.val) = true ∨ eqI.contains (a.val, b.val) = true) →
        lbl.getD a.val 0 = lbl.getD b.val 0) ∧
      (¬ (eqI.contains (b.val, a.val) = true ∨ eqI.contains (a.val, b.val) = true) →
        lbl.getD a.val 0 ≠ lbl.getD b.val 0) := by
    intro a b hab
    obtain ⟨i, hi, hb⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hab)
    have := (hAm a.val a.isLt).2 i hi
    rw [hb] at this
    exact ite_beq_spec this.2
  have hexcl := fun {p q : ℕ} => excl_sound cf O hex hNI hCN (p := p) (q := q)
  have hcyc := fun {p q : ℕ} => cycEx_sound cf O hex hCN hloop htri hNS (p := p) (q := q)
  -- κ is constant along X-edges, hence on X-components
  have hadj : ∀ x y, H.Adj x y → κ x = κ y := by
    have one : ∀ x y, ((∃ (a : Fin cf.m) (t : ℕ), ringAdjOf cf a t = true ∧
        eqR.contains (t, a.val) = true ∧ x = ι a ∧ y = ρ t) ∨
        (∃ a b : Fin cf.m, intAdjOf cf a b = true ∧
          (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true ∧
          x = ι a ∧ y = ι b)) → κ x = κ y := by
      rintro x y (⟨a, t, hat, h, rfl, rfl⟩ | ⟨a, b, hab, h, rfl, rfl⟩)
      · obtain ⟨htr, heq, -⟩ := hRing a t hat
        have htt : touchedB eqR t = true := touchedB_of_mem (by simpa using h)
        rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj, heq h, kInt_touched cf eqR lbl ρ hArg' htr htt]
        rcases xKappa_off cf eqR lbl ρ ι (v := ρ t) (fun b => O.ringOff t b) with ⟨-, e⟩ | ⟨hn, -⟩
        · exact e.symm
        · exact absurd ⟨t, htr, htt, rfl⟩ hn
      · rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj, xKappa_int cf eqR lbl ρ O.ιinj,
          (hInt a b hab).1 (by simpa using h)]
    intro x y hxy
    rw [hH, xGraph, SimpleGraph.fromRel_adj] at hxy
    rcases hxy.2 with h | h
    · exact one x y h
    · exact (one y x h).symm
  have hreach : ∀ x y, H.Reachable x y → κ x = κ y := by
    rintro x y ⟨p⟩
    induction p with
    | nil => rfl
    | cons h _ ih => exact (hadj _ _ h).trans ih
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- an X-edge exists (as in `xGraph_labels`)
    by_cases hR0 : eqR = []
    · have hI0 : eqI ≠ [] := by
        intro h; rw [hR0, h] at hA1; simp at hA1
      obtain ⟨⟨b, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqI hI0
      obtain ⟨⟨ha, hb⟩, hc⟩ := hAI _ hp
      have hab : intAdjOf cf ⟨a, ha⟩ ⟨b, hb⟩ = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ι ⟨b, hb⟩, ?_⟩
      rw [xGraph, SimpleGraph.fromRel_adj]
      refine ⟨fun e => ?_, Or.inl (Or.inr ⟨⟨a, ha⟩, ⟨b, hb⟩, hab, by simp [hp], rfl, rfl⟩)⟩
      have := O.ιinj e
      rw [← this, hloop] at hab
      exact Bool.false_ne_true hab
    · obtain ⟨⟨t, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqR hR0
      obtain ⟨ha, hc⟩ := hAR _ hp
      have hat : ringAdjOf cf ⟨a, ha⟩ t = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ρ t, ?_⟩
      rw [xGraph, SimpleGraph.fromRel_adj]
      exact ⟨fun e => O.ringOff t _ e.symm,
        Or.inl (Or.inl ⟨⟨a, ha⟩, t, hat, by simp [hp], rfl, rfl⟩)⟩
  · -- a listed ring edge outside X (D1)
    intro a s hat h hr
    have e := hreach _ _ hr
    obtain ⟨hsr, -, hne⟩ := hRing a s hat
    have hne' : lbl.getD a.val 0 ≠ lbl.getD (cf.m + s) 0 :=
      hne (fun h' => by rw [h] at h'; exact Bool.false_ne_true h')
    rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj] at e
    rcases xKappa_off cf eqR lbl ρ ι (v := ρ s) (fun b => O.ringOff s b) with ⟨-, hl⟩ | ⟨-, hl⟩
    · rw [hl] at e
      rcases kInt_cases cf eqR lbl ρ (lbl.getD a.val 0) with ⟨t, ht, htt, hlt, hk⟩ | hk
      · rw [hk] at e
        have hρ : ρ t = ρ s := Sum.inl_injective e
        have hst : s ≠ t := fun h' => hne' (by rw [← hlt, h'])
        -- the D1 check
        obtain ⟨i, hi, hsi⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hat)
        have hD1 := ((hsafe a.val a.isLt).1 i hi)
        rw [hsi] at hD1
        rcases hD1 with hD1 | hD1
        · rw [h] at hD1; exact Bool.false_ne_true hD1
        · rcases hD1 t ht with (((h1 | h1) | h1) | h1) | h1
          · exact absurd htt (by simp [h1])
          · exact h1 hlt
          · exact hst h1
          · exact hexcl hsr ht hst h1 hρ.symm
          · exact hcyc hsr ht h1 hρ.symm
      · rw [hk] at e; exact Sum.inr_ne_inl e
    · rw [hl] at e
      rcases kInt_cases cf eqR lbl ρ (lbl.getD a.val 0) with ⟨t, -, -, -, hk⟩ | hk <;>
        rw [hk] at e
      · exact Sum.inl_ne_inr e
      · exact (Sum.inl_ne_inr (Sum.inr_injective e))
  · -- a listed interior edge outside X (D2)
    intro a b hab h hr
    have e := hreach _ _ hr
    have hne : lbl.getD a.val 0 ≠ lbl.getD b.val 0 := (hInt a b hab).2 (by simpa using h)
    rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj, xKappa_int cf eqR lbl ρ O.ιinj] at e
    rcases kInt_cases cf eqR lbl ρ (lbl.getD a.val 0) with ⟨t, ht, htt, hlt, hka⟩ | hka <;>
      rcases kInt_cases cf eqR lbl ρ (lbl.getD b.val 0) with ⟨t', ht', htt', hlt', hkb⟩ | hkb <;>
      rw [hka, hkb] at e
    · have hρ : ρ t' = ρ t := Sum.inl_injective e
      have htt'' : t ≠ t' := fun h' => hne (by rw [← hlt, ← hlt', h'])
      obtain ⟨i, hi, hbi⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hab)
      have hD2 := ((hsafe a.val a.isLt).2 i hi)
      rw [hbi] at hD2
      rcases hD2 with (hD2 | hD2) | hD2
      · exact absurd h (by rw [hD2, Bool.true_or]; decide)
      · exact absurd h (by rw [hD2, Bool.or_true]; decide)
      · rcases hD2 t ht t' ht' with ((((((h1 | h1) | h1) | h1) | h1) | h1) | h1)
        · exact absurd htt (by simp [h1])
        · exact absurd htt' (by simp [h1])
        · exact h1 hlt
        · exact h1 hlt'
        · exact htt'' h1
        · exact hexcl ht ht' htt'' h1 hρ.symm
        · exact hcyc ht ht' h1 hρ.symm
    · exact Sum.inr_ne_inl e
    · exact Sum.inl_ne_inr e
    · exact hne (Sum.inl_injective (Sum.inr_injective e)).symm
  · -- an edge of G
    intro x y hxy hr
    have e := hreach _ _ hr
    obtain ⟨-, hx, hy⟩ := (O.hG x y).1 hxy
    have hne : x ≠ y := G.graph.ne_of_adj hxy
    rw [hκ] at e
    rcases xKappa_off cf eqR lbl ρ ι hx with ⟨-, hlx⟩ | ⟨-, hlx⟩ <;>
      rcases xKappa_off cf eqR lbl ρ ι hy with ⟨-, hly⟩ | ⟨-, hly⟩ <;> rw [hlx, hly] at e
    · exact hne (Sum.inl_injective e)
    · exact Sum.inl_ne_inr e
    · exact Sum.inr_ne_inl e
    · exact hne (Sum.inr_injective (Sum.inr_injective e))

/-! ## C6: registry entries, soundness, claim -/

namespace CGlue
open ClaimGlue (SmallerColorable MinimalCounterexample Internally6 DEntry OccursW)

/-- **A C-reducible registry entry.** The configuration, its contraction set `X = eqR ∪ eqI`, the
admissibility labelling, the C verdict and the side facts, each closed per key by
`native_decide` (`hC`) or `decide` (the rest). -/
structure CEntry where
  cf : DCheck18.Conf
  /-- contracted ring–interior edges `(t, a)` -/
  eqR : List (ℕ × ℕ)
  /-- contracted interior edges `(b, a)` -/
  eqI : List (ℕ × ℕ)
  /-- admissibility certificate: a label per interior vertex, then per ring position -/
  lbl : List ℕ
  hC : cReducible18 cf eqR eqI = true
  hadm : admissibleX (Conf.of18 cf) eqR eqI lbl = true
  hr2 : 2 ≤ cf.r
  hr : cf.r ≤ 19
  hsym : ∀ a b, intAdjOf (Conf.of18 cf) a b = true → intAdjOf (Conf.of18 cf) b a = true
  hloop : ∀ a, intAdjOf (Conf.of18 cf) a a = false
  hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r

/-- **C occurrence.** A face-walk occurrence (`ConfigOccW`, folds and pinches allowed) that is
exact and simple at the ring positions `X` touches. -/
def OccursCX (e : CEntry) (T : SphericalMap n) : Prop :=
  ∃ (G : SphericalMap n) (ρ : ℕ → Fin n) (ι : Fin e.cf.m → Fin n),
    ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    XRingSimple e.eqR e.cf.r ρ

/-- A simple-ring occurrence (`ConfigOcc`, as the per-key `configOcc` of occ24 produces) that is
exact is a C occurrence: `XRingSimple` is ring injectivity. -/
theorem occursCX_of_configOcc (e : CEntry) {T G : SphericalMap n} {ρ : ℕ → Fin n}
    {ι : Fin e.cf.m → Fin n}
    (O : ConfigOcc T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hex : OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf))) :
    OccursCX e T :=
  ⟨G, ρ, ι, O.toW, hex, fun _ _ _ ht s hs e => O.ring.inj s _ hs ht e⟩

/-- **Interior-only X: folds allowed.** For an entry with `eqR = []`, a C occurrence is just a D-style
face-walk occurrence (`ConfigOccW`: folded and pinched rings allowed) that is exact. -/
theorem occursCX_of_interior (e : CEntry) (hR : e.eqR = []) {T G : SphericalMap n}
    {ρ : ℕ → Fin n} {ι : Fin e.cf.m → Fin n}
    (O : ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hex : OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf))) :
    OccursCX e T :=
  ⟨G, ρ, ι, O, hex, by rw [hR]; exact xRingSimple_nil _ _⟩

/-- **C-soundness, per entry.** An occurrence of a C entry in a map whose smaller maps are all
colourable makes it colourable: colour the contracted map `T'` (smaller, C4), pull the colouring
back along `π` (it meets the X constraints), and run the D tail on its ring code (C1–C3). -/
theorem CEntry.colorable_of_contract (e : CEntry) {T G : SphericalMap n} {ρ : ℕ → Fin n}
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
    ConfigOccW.contract_reducer_of (Conf.of18 e.cf) e.eqR e.eqI e.lbl e.hadm e.hloop e.hrr O hex
      hlab hcon
  obtain ⟨col⟩ := IH n T' hcard
  refine ConfigOccW.colorable_of_cReducible18 e.cf e.eqR e.eqI e.hC e.hr2 e.hr e.hsym e.hloop
    e.hrr O (c := fun x => col (π x)) (fun _ _ huv _ _ => col.valid (hGe _ _ huv))
    (fun a => col (π (ι a))) ⟨fun a t hat => ?_, fun a b hab => ?_⟩
  · exact ⟨fun h => congrArg col ((hR a t hat).1 h).symm,
      fun h => (col.valid ((hR a t hat).2 h)).symm⟩
  · exact ⟨fun h => congrArg col ((hI a b hab).1 h),
      fun h => col.valid ((hI a b hab).2 h)⟩

/-- **C-soundness, per entry** (uses C4a `contract_subgraph`). -/
theorem CEntry.colorable (e : CEntry) {T : SphericalMap n} (h : OccursCX e T)
    (IH : SmallerColorable T) : T.graph.Colorable 4 := by
  obtain ⟨G, ρ, ι, O, hex, hs⟩ := h
  exact e.colorable_of_contract O hex
    (ConfigOccW.xGraph_labels _ e.eqR e.eqI e.lbl e.hadm e.hloop O hs) IH
    (fun H _ hle hne => contract_subgraph T H hle hne)

/-- **CGlue in ClaimGlue's form**, for this file's entries and occurrences. -/
def CGlueX (Cs : List CEntry) : Prop :=
  ∀ e ∈ Cs, ∀ (n : ℕ) (T : SphericalMap n), OccursCX e T → SmallerColorable T →
    T.graph.Colorable 4

/-- **The hypothesis is a theorem.** -/
theorem cGlueX (Cs : List CEntry) : CGlueX Cs :=
  fun e _ _ _ h IH => e.colorable h IH

/-! ### Single-interior-edge entries (special case, kept; subsumed by `CEntry.colorable`)

When `X` is one interior edge (`eqR = []`, `eqI = [p0]`), C4a is `contract_subgraph1`
(`CContract.lean`), proved for triangulations without separating triangles. A minimal
counterexample has none (`MinimalCounterexample.noSep`), so the soundness below needs only
`T.Triangulated`. -/

/-- A C entry whose contraction set is one interior edge. -/
structure CEntry1 extends CEntry where
  /-- the contracted interior edge `(b, a)` -/
  p0 : ℕ × ℕ
  hR : eqR = []
  hI : eqI = [p0]

/-- **C-soundness for a single-interior-edge entry** (no `sorry`). -/
theorem CEntry1.colorable (e : CEntry1) {T : SphericalMap n} (htri : T.Triangulated)
    (h : OccursCX e.toCEntry T) (IH : SmallerColorable T) : T.graph.Colorable 4 := by
  by_contra hcol
  have hns : NoSep T := MinimalCounterexample.noSep ⟨hcol, IH⟩ htri
  obtain ⟨G, ρ, ι, O, hex, hs⟩ := h
  refine hcol (e.toCEntry.colorable_of_contract O hex
    (ConfigOccW.xGraph_labels _ e.eqR e.eqI e.lbl e.hadm e.hloop O hs) IH (fun H hHx hle hne => ?_))
  obtain ⟨x, y, hxy⟩ := hne
  rw [e.hR, e.hI] at hHx
  subst hHx
  exact contract_subgraph1 T htri hns _ hle
    (fun p q hpq => xGraph_one (Conf.of18 e.cf) e.p0 ρ ι hpq hxy) ⟨x, y, hxy⟩

/-- **CGlue for single-interior-edge entries**, on triangulations. -/
def CGlueX1 (Cs : List CEntry1) : Prop :=
  ∀ e ∈ Cs, ∀ (n : ℕ) (T : SphericalMap n), T.Triangulated → OccursCX e.toCEntry T →
    SmallerColorable T → T.graph.Colorable 4

/-- **The hypothesis is a theorem** (no `sorry`). -/
theorem cGlueX1 (Cs : List CEntry1) : CGlueX1 Cs :=
  fun e _ _ _ htri h IH => e.colorable htri h IH

/-! ### Fold-safe entries (folded rings allowed; `XRingSimple` replaced by local facts)

`OccursCXF` drops `XRingSimple`. In its place it asks for `NbrInj` and `ApexFacts`, which are facts about
the configuration's own vertices and their listed neighbours. Soundness then needs a per-key check,
`foldSafeX` (decidable), and `T.Triangulated`, which gives `NoSep` and `NoShortSepCycle` for a minimal
counterexample. -/

/-- A C entry whose X-graph is fold-safe: every D1 and D2 fold is excluded, either by a length-3
cycle argument (`exclB`, using `NoSep`) or by a short cycle of length 4 or 5 whose sides are both
non-empty (`cycEx`, using `NoShortSepCycle`). -/
structure CEntryF extends CEntry where
  hfold : foldSafeX (Conf.of18 cf) eqR eqI lbl = true

/-- **C occurrence with folds allowed.** A face-walk occurrence that is exact, with distinct listed
ring neighbours and the configuration's own triangles on its interior edges. -/
def OccursCXF (e : CEntry) (T : SphericalMap n) : Prop :=
  ∃ (G : SphericalMap n) (ρ : ℕ → Fin n) (ι : Fin e.cf.m → Fin n),
    ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    NbrInj e.cf.r ρ (ringAdjOf (Conf.of18 e.cf)) ∧
    ApexFacts T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf))

/-- **C-soundness for fold-safe entries** (no `XRingSimple`, no `sorry`). -/
theorem CEntryF.colorable (e : CEntryF) {T : SphericalMap n} (htri : T.Triangulated)
    (h : OccursCXF e.toCEntry T) (IH : SmallerColorable T) : T.graph.Colorable 4 := by
  by_contra hcol
  have hns : NoSep T := MinimalCounterexample.noSep ⟨hcol, IH⟩ htri
  obtain ⟨G, ρ, ι, O, hex, hNI, hA⟩ := h
  exact hcol (e.toCEntry.colorable_of_contract O hex
    (ConfigOccW.xGraph_labels_fold _ e.eqR e.eqI e.lbl e.hadm e.hfold e.hloop O hex hNI
      (commonNbr_of_apex hns hex hA) htri (MinimalCounterexample.noShortSep ⟨hcol, IH⟩)) IH
    (fun H _ hle hne => contract_subgraph T H hle hne))

/-- **CGlue for fold-safe entries**, on triangulations. -/
def CGlueXF (Cs : List CEntryF) : Prop :=
  ∀ e ∈ Cs, ∀ (n : ℕ) (T : SphericalMap n), T.Triangulated → OccursCXF e.toCEntry T →
    SmallerColorable T → T.graph.Colorable 4

/-- **The hypothesis is a theorem** (no `sorry`). -/
theorem cGlueXF (Cs : List CEntryF) : CGlueXF Cs :=
  fun e _ _ _ htri h IH => e.colorable htri h IH

/-- A registry of D entries and fold-safe C entries. -/
structure RegistryF where
  D : List DEntry
  CF : List CEntryF

def RegistryF.Contains (R : RegistryF) (T : SphericalMap n) : Prop :=
  (∃ e ∈ R.D, OccursW e.cf T) ∨ (∃ e ∈ R.CF, OccursCXF e.toCEntry T)

def UnavoidableF (R : RegistryF) : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), Internally6 T → R.Contains T

/-- **Claim glue for D + fold-safe C registries, with no `sorry`.** The one open link is
`UnavoidableF R`. -/
theorem four_color_of_unavoidableCF (R : RegistryF) (hU : UnavoidableF R) {n : ℕ}
    (M : SphericalMap n) : M.graph.Colorable 4 := by
  refine four_color_of_smaller_gate (fun m T hm hconn htri hdeg IH => ?_) M
  by_contra hcol
  have hT : MinimalCounterexample T := ⟨hcol, IH⟩
  rcases hU m T (hT.internally6 hm hconn htri hdeg) with ⟨e, -, h⟩ | ⟨e, -, h⟩
  · exact hT.not_colorable (e.colorable h hT.smaller)
  · exact hT.not_colorable (e.colorable htri h hT.smaller)

/-- A registry of D entries and single-interior-edge C entries. -/
structure Registry1 where
  D : List DEntry
  C1 : List CEntry1

def Registry1.Contains (R : Registry1) (T : SphericalMap n) : Prop :=
  (∃ e ∈ R.D, OccursW e.cf T) ∨ (∃ e ∈ R.C1, OccursCX e.toCEntry T)

def Unavoidable1 (R : Registry1) : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), Internally6 T → R.Contains T

theorem MinimalCounterexample.avoids1 (R : Registry1) {T : SphericalMap n}
    (hT : MinimalCounterexample T) (htri : T.Triangulated) : ¬ R.Contains T := by
  rintro (⟨e, -, h⟩ | ⟨e, -, h⟩)
  · exact hT.not_colorable (e.colorable h hT.smaller)
  · exact hT.not_colorable (e.colorable htri h hT.smaller)

/-- **Claim glue for D + single-edge C registries, with no `sorry`.** The one open link is
`Unavoidable1 R`. -/
theorem four_color_of_unavoidableC1 (R : Registry1) (hU : Unavoidable1 R) {n : ℕ}
    (M : SphericalMap n) : M.graph.Colorable 4 := by
  refine four_color_of_smaller_gate (fun m T hm hconn htri hdeg IH => ?_) M
  by_contra hcol
  have hT : MinimalCounterexample T := ⟨hcol, IH⟩
  exact MinimalCounterexample.avoids1 R hT htri (hU m T (hT.internally6 hm hconn htri hdeg))

/-- A registry of D entries (`ClaimGlue.DEntry`) and C entries (this file). -/
structure Registry where
  D : List DEntry
  C : List CEntry

/-- `T` contains an occurrence of some configuration of `R`. -/
def Registry.Contains (R : Registry) (T : SphericalMap n) : Prop :=
  (∃ e ∈ R.D, OccursW e.cf T) ∨ (∃ e ∈ R.C, OccursCX e T)

/-- **Unavoidability of `R`** (the discharging LP at `t* ≤ 0` plus the appearance → occurrence
bridge, which for C entries must also give `OccExact` and `XRingSimple`). -/
def Unavoidable (R : Registry) : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), Internally6 T → R.Contains T

/-- **A minimal counterexample contains no configuration of `R`** (no `CGlue` hypothesis). -/
theorem MinimalCounterexample.avoids (R : Registry) {T : SphericalMap n}
    (hT : MinimalCounterexample T) : ¬ R.Contains T := by
  rintro (⟨e, -, h⟩ | ⟨e, -, h⟩)
  · exact hT.not_colorable (e.colorable h hT.smaller)
  · exact hT.not_colorable (e.colorable h hT.smaller)

/-- **Claim glue with C entries discharged.** If `R` is unavoidable, every spherical map is
four-colourable. The one open link is `Unavoidable R`. -/
theorem four_color_of_unavoidableC (R : Registry) (hU : Unavoidable R) {n : ℕ}
    (M : SphericalMap n) : M.graph.Colorable 4 := by
  refine four_color_of_smaller_gate (fun m T hm hconn htri hdeg IH => ?_) M
  by_contra hcol
  have hT : MinimalCounterexample T := ⟨hcol, IH⟩
  exact MinimalCounterexample.avoids R hT (hU m T (hT.internally6 hm hconn htri hdeg))

/-- The same for the library's plane maps. -/
theorem four_color_of_unavoidableC_planeMap (R : Registry) (hU : Unavoidable R) {n : ℕ}
    (M : PlaneMap n) : M.graph.Colorable 4 :=
  four_color_of_unavoidableC R hU (SphericalMap.ofPlaneMap M)

/-! ## Sanity instance: the 66666 wheel with Job 16's X = {R0-I1, I2-I3, I3-I4, I4-I5} -/

/-- `DCheck.w66666` in the `DCheck18` encoding. -/
def cf66666 : DCheck18.Conf :=
  { name := "66666", r := 10, m := 6,
    ringAdj := #[#[], #[9, 0, 1], #[1, 2, 3], #[3, 4, 5], #[5, 6, 7], #[7, 8, 9]],
    intAdj := #[#[1, 2, 3, 4, 5], #[0, 2, 5], #[0, 3, 1], #[0, 4, 2], #[0, 5, 3], #[0, 1, 4]] }

theorem cf66666_hC : cReducible18 cf66666 [(0, 1)] [(2, 3), (3, 4), (4, 5)] = true := by
  native_decide

/-- Labels: `I0` ↦ 100, `I1` ↦ 0 (= `R0`), `I2..I5` ↦ 101, `R t` ↦ `t`. -/
theorem cf66666_hadm : admissibleX (Conf.of18 cf66666) [(0, 1)] [(2, 3), (3, 4), (4, 5)]
    [100, 0, 101, 101, 101, 101, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = true := by
  native_decide

/-- Sabotage: the single contraction `X = {I0-I1}` is not certified for the 66666 wheel. -/
theorem cf66666_not_I0I1 : cReducible18 cf66666 [] [(0, 1)] = false := by
  native_decide

/-- The 66666 wheel as a C entry. -/
def e66666 : CEntry where
  cf := cf66666
  eqR := [(0, 1)]
  eqI := [(2, 3), (3, 4), (4, 5)]
  lbl := [100, 0, 101, 101, 101, 101, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  hC := cf66666_hC
  hadm := cf66666_hadm
  hr2 := by decide
  hr := by decide
  hsym := by native_decide
  hloop := by native_decide
  hrr := by native_decide

/-- The 66666 wheel's X is fold-safe. -/
theorem cf66666_fold : foldSafeX (Conf.of18 cf66666) [(0, 1)] [(2, 3), (3, 4), (4, 5)]
    [100, 0, 101, 101, 101, 101, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = true := by
  native_decide

/-- The 66666 wheel as a fold-safe C entry. -/
def e66666F : CEntryF := { e66666 with hfold := cf66666_fold }

/-- A ring-X entry whose folds need cycles of length 4 and 5: `f9_..5565675_......5..` with
X = {I0-I1, I0-I5, I1-I8, R4-I5}. -/
def cfF9 : DCheck18.Conf :=
  { name := "f9_..5565675_......5..", r := 14, m := 9,
    ringAdj := #[#[0, 1], #[7, 8], #[10, 11, 12], #[0, 12, 13], #[1, 2, 3], #[3, 4], #[4, 5, 6],
      #[6, 7], #[8, 9, 10]],
    intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 7, 8], #[0, 1, 3, 8], #[0, 2], #[0, 5], #[0, 4, 6],
      #[0, 5, 7], #[0, 1, 6], #[1, 2]] }

/-- The fold `ρ 8 = ρ 4` is not excluded by a triangle, but it is excluded by a short cycle (here
`ρ 4, I5, I0, I1, I8`, length 5, apexes on the edge `I0-I1`). -/
theorem cfF9_needs_cycle : exclB (Conf.of18 cfF9) 8 4 = false ∧ cycEx (Conf.of18 cfF9) 8 4 = true := by
  native_decide

/-- With the short-cycle rule the entry is fold-safe (labels: one per X-component). -/
theorem cfF9_fold : foldSafeX (Conf.of18 cfF9) [(4, 5)] [(1, 0), (5, 0), (8, 1)]
    [0, 0, 1, 2, 3, 0, 4, 5, 0, 6, 7, 8, 9, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18] = true := by
  native_decide

end CGlue
end SimpleGraph.SphericalMap

#print axioms DCheck.S1T.runGoodRefT_sound
#print axioms DCheck.CG.extCAux_complete
#print axioms SimpleGraph.SphericalMap.ConfigOccW.colorable_of_cReducible18
#print axioms SimpleGraph.SphericalMap.CGlue.CEntry.colorable
#print axioms SimpleGraph.SphericalMap.CGlue.four_color_of_unavoidableC
#print axioms SimpleGraph.SphericalMap.ConfigOccW.xGraph_labels
#print axioms SimpleGraph.SphericalMap.CGlue.e66666
#print axioms SimpleGraph.SphericalMap.contract_subgraph1
#print axioms SimpleGraph.SphericalMap.CGlue.CEntry1.colorable
#print axioms SimpleGraph.SphericalMap.CGlue.cGlueX1
#print axioms SimpleGraph.SphericalMap.CGlue.four_color_of_unavoidableC1
#print axioms SimpleGraph.SphericalMap.contract_subgraph
#print axioms SimpleGraph.SphericalMap.CGlue.cGlueX
#print axioms SimpleGraph.SphericalMap.CGlue.occursCX_of_interior
#print axioms SimpleGraph.SphericalMap.occExact_of_nx
#print axioms SimpleGraph.SphericalMap.ConfigOccW.xGraph_labels_fold
#print axioms SimpleGraph.SphericalMap.CGlue.CEntryF.colorable
#print axioms SimpleGraph.SphericalMap.CGlue.cGlueXF
#print axioms SimpleGraph.SphericalMap.CGlue.four_color_of_unavoidableCF
#print axioms SimpleGraph.SphericalMap.CGlue.e66666F
#print axioms SimpleGraph.SphericalMap.cyc_sound
#print axioms SimpleGraph.SphericalMap.CGlue.cfF9_fold
