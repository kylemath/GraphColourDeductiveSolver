import ClaimGlue
import C66666

/-!
# CGlue: soundness of C-reducibility (Long Table, 19 Oct 2026, draft)

`ClaimGlue.lean` proves "reducible registry + `Unavoidable R` ⇒ 4-colourable" with the C entries
behind an explicit hypothesis `CGlue R.C`. This file replaces that hypothesis by a theorem,
`CEntry.colorable`, modulo ONE named geometric gap (`ConfigOccW.contract_reducer`, C4 below).
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
  - C4a `contract_subgraph` [**OPEN, the only `sorry`**]: contracting a subgraph of a spherical
    map is a smaller spherical map (pure map geometry, no configuration data);
  - C4b `ConfigOccW.xGraph_labels` [PROVED]: the label argument (no kept edge inside an X-component).
* C5 (global loop-freeness) is not a lemma here: it is the occurrence field `XRingSimple` (no ring
  position touched by `X` is revisited by the face walk), proved for simple rings
  (`occursCX_of_configOcc`). Local loop-freeness is `admissibleX` (decide, per key).
* C6 `CEntry.colorable`, `four_color_of_unavoidableC` [PROVED from C1–C4].

**Axioms.** No new `axiom`. One `sorry` (C4a). Inherits the `native_decide` axioms of the D chain;
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

/-! ## C4: the contracted reducer

C4 is split into two open lemmas and a proved assembly:
* C4a `contract_subgraph` (OPEN, geometry): contracting the components of a subgraph
  `H ≤ T` with an edge gives a smaller spherical map that keeps every edge between components;
* C4b `ConfigOccW.xGraph_labels` (PROVED, combinatorics): the X-graph has an edge, and no listed
  edge outside `X` and no edge of `G` joins two vertices of one X-component (the label argument);
* `ConfigOccW.contract_reducer` (PROVED from C4a + C4b): the reducer in the form `CEntry.colorable` uses. -/

/-- **C4a (OPEN): contraction of a subgraph of a spherical map.** Contracting each connected
component of `H ≤ T` (with at least one edge) to one vertex gives a spherical map `T'` on the same
vertex type (merged-away vertices isolated) with smaller support, and a vertex map `π` that is
constant on `H`-components and keeps every edge of `T` between different components.

True because a contraction of connected subgraphs of a planar map is planar (a minor) and merges at
least two support vertices. What the proof needs: edge contraction on `SphericalMap` (merge the
rotations at the two ends, delete the contracted edge and the digons it leaves, keep `Fills`),
iterated over a spanning forest of `H` (in our use ≤ 4 edges); or, for the occurrence at hand,
refilling the ring face of `G` with the contracted configuration (Job 25 `split`/`RingFace.chordMap`,
`growBefore_fills`, `Sep5Star.starMap`). Estimate: 800–2,000 lines; one edge (87% of the registry):
300–500 lines. -/
theorem contract_subgraph (T : SphericalMap n) (H : SimpleGraph (Fin n))
    (hH : H ≤ T.graph) (hne : ∃ x y, H.Adj x y) :
    ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
      Nat.card T'.graph.support < Nat.card T.graph.support ∧
      (∀ x y, H.Reachable x y → π x = π y) ∧
      (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y)) := by
  sorry

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

/-- **C4: contracting `X` gives a smaller reducer** (proved from C4a and C4b). Let `cf` occur in
`T` exactly (`OccExact`), with `X = eqR ∪ eqI` locally admissible and globally simple. Then there
are a spherical map `T'` of smaller support and a vertex map `π` that keeps every edge of `G`,
identifies each listed edge in `X` and keeps each other listed edge. -/
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
  obtain ⟨hne, hnR, hnI, hnG⟩ := ConfigOccW.xGraph_labels cf eqR eqI lbl hadm hloop O hs
  obtain ⟨T', π, hcard, hπ, hkeep⟩ := contract_subgraph T _ hle hne
  refine ⟨T', π, hcard, fun x y hxy => hkeep x y ((O.hG x y).1 hxy).1 (hnG x y hxy),
    fun a t hat => ⟨fun h => hπ _ _ (hXR a t hat h).reachable,
      fun h => hkeep _ _ (hex.2 a t (hlt a t hat) hat) (hnR a t hat h)⟩,
    fun a b hab => ⟨fun h => hπ _ _ (hXI a b hab h).reachable,
      fun h => hkeep _ _ (hex.1 a b hab).symm (hnI a b hab h)⟩⟩

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

/-- **C-soundness, per entry.** An occurrence of a C entry in a map whose smaller maps are all
colourable makes it colourable: colour the contracted map `T'` (smaller, C4), pull the colouring
back along `π` (it meets the X constraints), and run the D tail on its ring code (C1–C3). -/
theorem CEntry.colorable (e : CEntry) {T : SphericalMap n} (h : OccursCX e T)
    (IH : SmallerColorable T) : T.graph.Colorable 4 := by
  obtain ⟨G, ρ, ι, O, hex, hs⟩ := h
  obtain ⟨T', π, hcard, hGe, hR, hI⟩ :=
    ConfigOccW.contract_reducer (Conf.of18 e.cf) e.eqR e.eqI e.lbl e.hadm e.hloop e.hrr O hex hs
  obtain ⟨col⟩ := IH n T' hcard
  refine ConfigOccW.colorable_of_cReducible18 e.cf e.eqR e.eqI e.hC e.hr2 e.hr e.hsym e.hloop
    e.hrr O (c := fun x => col (π x)) (fun _ _ huv _ _ => col.valid (hGe _ _ huv))
    (fun a => col (π (ι a))) ⟨fun a t hat => ?_, fun a b hab => ?_⟩
  · exact ⟨fun h => congrArg col ((hR a t hat).1 h).symm,
      fun h => (col.valid ((hR a t hat).2 h)).symm⟩
  · exact ⟨fun h => congrArg col ((hI a b hab).1 h),
      fun h => col.valid ((hI a b hab).2 h)⟩

/-- **CGlue in ClaimGlue's form**, for this file's entries and occurrences. -/
def CGlueX (Cs : List CEntry) : Prop :=
  ∀ e ∈ Cs, ∀ (n : ℕ) (T : SphericalMap n), OccursCX e T → SmallerColorable T →
    T.graph.Colorable 4

/-- **The hypothesis is a theorem** (modulo C4a). -/
theorem cGlueX (Cs : List CEntry) : CGlueX Cs :=
  fun e _ _ _ h IH => e.colorable h IH

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
four-colourable. Open links: `Unavoidable R` and C4a (`contract_subgraph`). -/
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

end CGlue
end SimpleGraph.SphericalMap

#print axioms DCheck.S1T.runGoodRefT_sound
#print axioms DCheck.CG.extCAux_complete
#print axioms SimpleGraph.SphericalMap.ConfigOccW.colorable_of_cReducible18
#print axioms SimpleGraph.SphericalMap.CGlue.CEntry.colorable
#print axioms SimpleGraph.SphericalMap.CGlue.four_color_of_unavoidableC
#print axioms SimpleGraph.SphericalMap.ConfigOccW.xGraph_labels
#print axioms SimpleGraph.SphericalMap.CGlue.e66666
