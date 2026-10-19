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
* C4 `ConfigOccW.contract_reducer` [**OPEN, the only `sorry`**]: contracting `X` in `T` gives a
  spherical map `T'` of smaller support and a vertex map `π` that keeps every edge of the deleted
  map `G`, identifies exactly along `X`, and keeps every other configuration edge.
* C5 (global loop-freeness) is not a lemma here: it is the occurrence field `XRingSimple` (no ring
  position touched by `X` is revisited by the face walk), proved for simple rings
  (`occursCX_of_configOcc`). Local loop-freeness is `admissibleX` (decide, per key).
* C6 `CEntry.colorable`, `four_color_of_unavoidableC` [PROVED from C1–C4].

**Axioms.** No new `axiom`. One `sorry` (C4). Inherits the `native_decide` axioms of the D chain;
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
    ∀ j, (runGoodRefT mt cf)[j]! = true → GoodT mt cf (ringColourings cf.r)[j]! := by
  have hI := mkIndex_spec (ringColourings cf.r)
  unfold runGoodRefT
  refine forIn_range_bind 0 ((ringColourings cf.r).size + 1) _ _ _
    (fun _ (st : Array Bool × Nat × Array Nat × Nat) =>
      OuterInv mt cf (ringColourings cf.r) st.1 st.2.1 st.2.2.1)
    (fun (res : Array Bool) => ∀ j, res[j]! = true → GoodT mt cf (ringColourings cf.r)[j]!)
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
      dsimp only
      have ht := hR cols.size ha _ (Array.getElem_mem hi)
      cases hc : eqR.contains (cf.ringAdj[cols.size]![i], cols.size)
      · exact cond_ne_true hc (ht.2 hc)
      · exact cond_eq_true hc (ht.1 hc)
    have hint : (cf.intAdj[cols.size]!).all (fun b => b >= cols.size ||
        (if eqI.contains (b, cols.size) || eqI.contains (cols.size, b) then
          cols[b]! == lam cols.size else cols[b]! != lam cols.size)) = true := by
      rw [Array.all_eq_true]
      intro i hi
      dsimp only
      rw [Bool.or_eq_true]
      by_cases hb : cf.intAdj[cols.size]![i] < cols.size
      · right
        have ht := hI cols.size ha _ (Array.getElem_mem hi) hb
        rw [hcols _ hb]
        cases hc : (eqI.contains (cf.intAdj[cols.size]![i], cols.size) ||
            eqI.contains (cols.size, cf.intAdj[cols.size]![i]))
        · exact cond_ne_true hc (ht.2 hc)
        · exact cond_eq_true hc (ht.1 hc)
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
    rw [heq, col_code _ (fun t => (g _).isLt) _ _ ht]
    have : (⟨ringSeq ρ c t % 4, Nat.mod_lt _ (by decide)⟩ : Fin 4) = c (ρ t) :=
      Fin.ext (Nat.mod_eq_of_lt (c (ρ t)).isLt)
    rw [this]
  apply CG.extCAux_complete cf eqR eqI _ (CG.lamN fun a => g (lam a)) (CG.lamN_lt _)
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

variable {r m : ℕ} {ι : Fin m → Fin n} {intAdj : Fin m → Fin m → Bool} {ringAdj : Fin m → ℕ → Bool}

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

/-! ## C4: the contracted reducer (open) -/

/-- **C4 (OPEN, the one `sorry` of this file): contracting `X` gives a smaller reducer.**

Statement. Let `cf` occur in `T` (deleted map `G`, face-walk ring `ρ`, interior `ι`), exactly
(`OccExact`), with `X = eqR ∪ eqI` locally admissible (`admissibleX`) and globally simple
(`XRingSimple`). Then there are a spherical map `T'` on the same vertex type and a vertex map `π`
(the quotient by the X-components; the merged-away vertices become isolated) with
* `T'` of strictly smaller support (`|X| ≥ 1` real edges are contracted);
* every edge of `G` kept (`π` is injective on the non-interior vertices of a class: each
  X-component meets at most one ring vertex, by the distinct ring labels and `XRingSimple`);
* each listed ring–interior edge: identified if in `eqR`, kept otherwise;
* each listed interior edge: identified if in `eqI` (either orientation), kept otherwise.

What the proof needs (estimate 1,000–2,500 lines for general X, 300–500 for one interior edge):
(i) edge contraction on `SphericalMap` (merge the rotations of the two ends, delete the
contracted edge and the digons it creates at its two incident triangles; `Fills` is preserved),
iterated over the ≤ 4 edges of `X`, or equivalently refilling the ring face of `G` with the
contracted configuration (Job 25 `split`/`RingFace.chordMap`, `growBefore_fills`,
`Sep5Star.starMap`); (ii) the support count; (iii) the label argument above: X-edges join equal
labels, so an X-component has one label, so a kept edge never becomes a loop. -/
theorem ConfigOccW.contract_reducer (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleX cf eqR eqI lbl = true) {ι : Fin cf.m → Fin n}
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
  sorry

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
    ConfigOccW.contract_reducer (Conf.of18 e.cf) e.eqR e.eqI e.lbl e.hadm O hex hs
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

/-- **The hypothesis is a theorem** (modulo C4). -/
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
four-colourable. Open links: `Unavoidable R` and C4 (`ConfigOccW.contract_reducer`). -/
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
  decide

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
  hsym := by decide
  hloop := by decide
  hrr := by decide

end CGlue
end SimpleGraph.SphericalMap

#print axioms DCheck.S1T.runGoodRefT_sound
#print axioms DCheck.CG.extCAux_complete
#print axioms SimpleGraph.SphericalMap.ConfigOccW.colorable_of_cReducible18
#print axioms SimpleGraph.SphericalMap.CGlue.CEntry.colorable
#print axioms SimpleGraph.SphericalMap.CGlue.four_color_of_unavoidableC
