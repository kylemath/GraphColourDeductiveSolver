import RSSTCheckCore
import RSSTEval

/-!
# ST-120 B5 M2: soundness of the certificate checker

Studio, 10 Nov. `checkDeg_sound`: if `checkDeg KL d cert = true` then every real-shaped word of degree `d` (B4's
`RealShape`) with `0 < hi` (B2's `UWin.loHi`, the 71 RSST parts) has a configuration of `KL` embedded (`Kills`).

Structure:
1. `SRes` algebra: `eval` commutes with `and`; `symTest` evaluates to B2's `Rng.test3`.
2. **Symbolic = concrete** (`symFit_eval`): for the tagged word `X` and a valuation `σ` of the codes,
   `(symFit p (tviewW X i) a).eval σ = p.fit3At ((X.mapL σ).viewW i) a` (and the same at hub `u`). This is B2's own
   code run on two words that differ only by `σ`.
2'. **Completeness of the grouping** (`tag_map`): every real-shaped word `W` *is* `(tagW W.d W.link).mapL (sigmaW W)`.
   So `hi W` is the symbolic `hi` of its link word evaluated at `sigmaW W` (`hi_eq`), and every link word is enumerated
   (`allWords_mem`).
3. Kills: `reqOf K d link e = some R` and `σ` meets `R` ⇒ `checkEmb K W e` (`reqOf_sound`).
4. The DFS (`dfs_sound`): simplification preserves the symbolic `hi`; `ub` bounds it; a node is closed only by `ub ≤ 0`
   or a met requirement; branching covers `5..9`.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

/-! ## 1. `SRes` -/

theorem SRes.eval_ofBool (σ : Nat → Nat) (b : Bool) : (SRes.ofBool b).eval σ = Tri.ofBool b := by
  cases b <;> rfl

theorem Tri.and_no (t : Tri) : t.and .no = .no := by cases t <;> rfl

theorem SRes.eval_and (σ : Nat → Nat) (x y : SRes) : (x.and y).eval σ = (x.eval σ).and (y.eval σ) := by
  cases x with
  | no => rfl
  | c a o =>
    cases y with
    | no => simp only [SRes.and, SRes.eval]; rw [Tri.and_no]
    | c b p =>
      simp only [SRes.and, SRes.eval, List.all_append, Bool.and_eq_true]
      by_cases ha : (a.all fun vr => vr.2.test (σ vr.1)) = true <;>
      by_cases hb : (b.all fun vr => vr.2.test (σ vr.1)) = true <;>
      simp only [ha, hb, and_self, and_true, and_false, true_and, false_and, ite_true, ite_false] <;>
      cases o <;> cases p <;> rfl

/-- Codes start at 100; a valuation fixes every letter below. -/
abbrev FixLow (σ : Nat → Nat) : Prop := ∀ x, x < 100 → σ x = x

theorem not_code {x : Nat} (h : isCode x = false) : x < 100 := by
  unfold isCode at h
  have : ¬ (100 ≤ x) := by
    intro hh
    have h2 : Nat.ble 100 x = true := Nat.ble_eq.mpr hh
    rw [h2] at h; cases h
  omega

theorem symTest_eval {σ : Nat → Nat} (hσ : FixLow σ) (r : Rng) (o : Option Nat) :
    (symTest r o).eval σ = r.test3 (o.map σ) := by
  unfold symTest
  by_cases hf : r.isFull = true
  · cases o <;> simp [hf, Rng.test3, SRes.sure, SRes.eval, Tri.ofBool]
  · have hf' : r.isFull = false := by simpa using hf
    cases o with
    | none => simp [hf', Rng.test3, SRes.opn, SRes.eval]
    | some x =>
      simp only [hf', Bool.false_eq_true, ite_false, Option.map_some, Rng.test3, Bool.false_or]
      cases hc : isCode x
      · simp only [Bool.false_eq_true, ite_false]; rw [SRes.eval_ofBool, hσ x (not_code hc)]
      · simp only [ite_true, SRes.eval, List.all_cons, List.all_nil, Bool.and_true, Tri.ofBool]
        cases r.test (σ x) <;> rfl

theorem fans_eval {σ : Nat → Nat} (hσ : FixLow σ) : ∀ (rs : List Rng) (fl : List (Option Nat)) (init : SRes),
    ((rs.zip fl).foldl (fun acc rx => acc.and (symTest rx.1 rx.2)) init).eval σ =
      (rs.zip (fl.map (Option.map σ))).foldl (fun acc rx => acc.and (rx.1.test3 rx.2)) (init.eval σ) := by
  intro rs
  induction rs with
  | nil => intro fl init; simp
  | cons r rs ih =>
    intro fl init
    cases fl with
    | nil => simp
    | cons f fl =>
      simp only [List.zip_cons_cons, List.foldl_cons, List.map_cons]
      rw [ih, SRes.eval_and, symTest_eval hσ]

/-! ## 2. Symbolic = concrete -/

/-- The concrete spoke view of a tagged spoke under `σ`. -/
def cview (σ : Nat → Nat) (x : TSpoke) : PSpokeView :=
  { spoke := σ x.sp, hat := x.hat.map σ, fans := (x.fansOf (x.fc (σ x.sp))).map (Option.map σ) }

theorem exact_not_full {r : Rng} (h : r.lo = r.hi) : r.isFull = false := by
  unfold Rng.isFull; rw [Bool.and_eq_false_iff]
  by_cases h5 : r.lo ≤ 5
  · right; rw [Bool.eq_false_iff, ne_eq, Nat.ble_eq]; omega
  · left; rw [Bool.eq_false_iff, ne_eq, Nat.ble_eq]; omega

theorem exact_test {r : Rng} (h : r.lo = r.hi) (x : Nat) : r.test x = true ↔ x = r.lo := by
  unfold Rng.test; rw [Bool.and_eq_true, Nat.ble_eq, Nat.ble_eq]; omega

theorem symSub_eval {σ : Nat → Nat} (hσ : FixLow σ) (s : Sub)
    (hs : s.fans.all Rng.isFull = true ∨ s.spoke.lo = s.spoke.hi) (x : TSpoke) :
    (symSub s x).eval σ = s.fit3 (cview σ x) := by
  unfold symSub Sub.fit3 cview
  simp only
  rw [SRes.eval_and, SRes.eval_and, symTest_eval hσ]
  -- the spoke part
  have hsp : (if s.spoke.isFull = true then SRes.sure
      else if isCode x.sp = true then SRes.c [(x.sp, s.spoke)] false else SRes.ofBool (s.spoke.test x.sp)).eval σ =
      Tri.ofBool (s.spoke.isFull || s.spoke.test (σ x.sp)) := by
    by_cases hf : s.spoke.isFull = true
    · simp [hf, SRes.sure, SRes.eval, Tri.ofBool]
    · have hf' : s.spoke.isFull = false := by simpa using hf
      simp only [hf', Bool.false_eq_true, ite_false, Bool.false_or]
      cases hc : isCode x.sp
      · simp only [Bool.false_eq_true, ite_false]; rw [SRes.eval_ofBool, hσ _ (not_code hc)]
      · simp only [ite_true, SRes.eval, List.all_cons, List.all_nil, Bool.and_true, Tri.ofBool]
        cases s.spoke.test (σ x.sp) <;> rfl
  rw [hsp]
  by_cases hfa : s.fans.all Rng.isFull = true
  · simp only [hfa, ite_true]; rfl
  · have hex : s.spoke.lo = s.spoke.hi := hs.resolve_left hfa
    simp only [hfa, Bool.false_eq_true, ite_false]
    -- the fan list read: equal to the concrete one unless the spoke test fails anyway
    have key : ∀ (A : Tri) (fl : List (Option Nat)), (σ x.sp = s.spoke.lo ∨ isCode x.sp = false) →
        x.fansOf (x.fc (if isCode x.sp = true then s.spoke.lo else x.sp)) = fl →
        (if (s.fans.length != fl.length) = true then SRes.no
          else (s.fans.zip fl).foldl (fun acc rx => acc.and (symTest rx.1 rx.2)) SRes.sure).eval σ =
        (if (s.fans.length != ((x.fansOf (x.fc (σ x.sp))).map (Option.map σ)).length) = true then Tri.no
          else (s.fans.zip ((x.fansOf (x.fc (σ x.sp))).map (Option.map σ))).foldl
            (fun acc rx => acc.and (rx.1.test3 rx.2)) Tri.sure) := by
      intro _ fl hor hfl
      have hfl' : fl = x.fansOf (x.fc (σ x.sp)) := by
        rw [← hfl]
        rcases hor with h | h
        · cases hc : isCode x.sp
          · rw [hσ _ (not_code hc)]; simp
          · simp [h]
        · rw [h, hσ _ (not_code h)]; simp
      subst hfl'
      rw [List.length_map]
      split_ifs
      · rfl
      · rw [fans_eval hσ]; rfl
    by_cases hok : σ x.sp = s.spoke.lo ∨ isCode x.sp = false
    · rw [key .sure _ hok rfl]
    · -- code spoke with a letter other than the exact spoke letter: both sides are `no`
      push_neg at hok
      have ht : s.spoke.test (σ x.sp) = false := by
        rw [Bool.eq_false_iff]; intro h; exact hok.1 ((exact_test hex _).1 h)
      rw [exact_not_full hex, ht]
      rfl

theorem foldl_eval (σ : Nat → Nat) (F : Nat → SRes) (G : Nat → Tri) :
    ∀ (L : List Nat), (∀ j ∈ L, (F j).eval σ = G j) → ∀ (init : SRes),
      (L.foldl (fun acc j => acc.and (F j)) init).eval σ = L.foldl (fun acc j => acc.and (G j)) (init.eval σ) := by
  intro L
  induction L with
  | nil => intro _ init; rfl
  | cons a L ih =>
    intro h init
    simp only [List.foldl_cons]
    rw [ih (fun j hj => h j (List.mem_cons_of_mem _ hj)), SRes.eval_and, h a List.mem_cons_self]

theorem rsstParts_fanExact : rsstParts.all Part.fanExact = true := by decide

theorem symFit_eval {σ : Nat → Nat} (hσ : FixLow σ) (p : Part) (hp : p.fanExact = true) (tv : List TSpoke)
    (a : Nat) : (symFit p tv a).eval σ = p.fit3At (tv.map (cview σ)) a := by
  unfold symFit Part.fit3At
  rw [List.length_map]
  split_ifs
  · rfl
  · rw [foldl_eval]
    · rfl
    intro j _
    rw [List.getElem?_map]
    rcases h1 : p.subs[j]? with _ | s
    · rfl
    · rcases h2 : tv[(a + j) % tv.length]? with _ | x
      · rfl
      · simp only [Option.map_some]
        apply symSub_eval hσ
        have hm := List.mem_of_getElem? h1
        have := List.all_eq_true.1 hp s hm
        simpa [Bool.or_eq_true, beq_iff_eq] using this

theorem getD_lt' {α : Type} (l : List α) (n : Nat) (a : α) (h : n < l.length) : l.getD n a = l[n] := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem h]; rfl

theorem getD_ge' {α : Type} (l : List α) (n : Nat) (a : α) (h : l.length ≤ n) : l.getD n a = a := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_none h]; rfl

/-! ### Words that differ by a valuation -/

/-- Apply `σ` to the apex and private letters. -/
def UWin.mapL (σ : Nat → Nat) (X : UWin) : UWin :=
  { d := X.d, link := X.link, apex := X.apex.map σ, priv := X.priv.map (·.map σ) }

theorem getD_map_fix {σ : Nat → Nat} (l : List Nat) (n a : Nat) (ha : σ a = a) :
    (l.map σ).getD n a = σ (l.getD n a) := by
  simp only [List.getD_eq_getElem?_getD, List.getElem?_map]
  cases l[n]? <;> simp [ha]

theorem segL_mapL {σ : Nat → Nat} (hσ : FixLow σ) (X : UWin) (m : Nat) :
    (X.mapL σ).segL m = (X.segL m).map σ := by
  have h9 : σ 9 = 9 := hσ 9 (by norm_num)
  have hp : (X.mapL σ).priv.getD m [] = (X.priv.getD m []).map σ := by
    simp only [UWin.mapL, List.getD_eq_getElem?_getD, List.getElem?_map]
    cases X.priv[m]? <;> simp
  simp only [UWin.segL, UWin.apexL, List.map_append, List.map_cons, List.map_nil, List.map_take]
  rw [hp]
  simp only [UWin.mapL, UWin.linkL]
  rw [getD_map_fix _ _ _ h9, getD_map_fix _ _ _ h9]

theorem letter_mapL {σ : Nat → Nat} (hσ : FixLow σ) (X : UWin) (hl : ∀ x ∈ X.link, x < 100) (b : Nat)
    (pos : WPos) : (X.mapL σ).letter b pos = (X.letter b pos).map σ := by
  have hlk : ∀ m, σ (X.linkL m) = X.linkL m := by
    intro m; apply hσ
    unfold UWin.linkL; rw [List.getD_eq_getElem?_getD]
    cases h : X.link[m]? with
    | none => simp
    | some x => simpa using hl x (List.mem_of_getElem? h)
  cases pos with
  | u => simp only [UWin.letter, Option.map_some, UWin.mapL]; rw [hσ]; omega
  | w δ => simp only [UWin.letter, Option.map_some]; rw [hlk]; rfl
  | seg δ k => simp only [UWin.letter]; rw [show (X.mapL σ).idx b δ = X.idx b δ from rfl, segL_mapL hσ,
      List.getElem?_map]
  | segR δ k =>
    simp only [UWin.letter]; rw [show (X.mapL σ).idx b δ = X.idx b δ from rfl, segL_mapL hσ, List.length_map]
    split_ifs <;> simp [List.getElem?_map]
  | ring3 => rfl

theorem viewW_mapL {σ : Nat → Nat} (hσ : FixLow σ) (X : UWin) (hl : ∀ x ∈ X.link, x < 100) (i : Nat) :
    (X.mapL σ).viewW i = (tviewW X i).map (cview σ) := by
  have h0 : σ 0 = 0 := hσ 0 (by norm_num)
  unfold UWin.viewW tviewW
  rw [List.map_map]
  apply List.map_congr_left
  intro t _
  simp only [Function.comp, cview, letter_mapL hσ X hl]
  have hg : ∀ o : Option Nat, (o.map σ).getD 0 = σ (o.getD 0) := by intro o; cases o <;> simp [h0]
  rw [hg]
  simp only [List.map_map]
  rfl

theorem viewU_mapL {σ : Nat → Nat} (hσ : FixLow σ) (X : UWin) (hl : ∀ x ∈ X.link, x < 100) :
    (X.mapL σ).viewU = (tviewU X).map (cview σ) := by
  have h0 : σ 0 = 0 := hσ 0 (by norm_num)
  unfold UWin.viewU tviewU
  rw [List.map_map]
  apply List.map_congr_left
  intro t _
  simp only [Function.comp, cview, letter_mapL hσ X hl]
  have hg : ∀ o : Option Nat, (o.map σ).getD 0 = σ (o.getD 0) := by intro o; cases o <;> simp [h0]
  rw [hg]
  simp only [List.map_map]
  rfl

/-! ### `hi` of a word as the symbolic `hi` of its link word -/

theorem sum_singleton_ite {α : Type} (c : Prop) [Decidable c] (x : α) (F : α → Int) :
    ((if c then [x] else []).map F).sum = if c then F x else 0 := by
  split <;> simp

theorem inX_sym {σ : Nat → Nat} (hσ : FixLow σ) (X : UWin) (hl : ∀ x ∈ X.link, x < 100) (parts : List Part)
    (hP : ∀ p ∈ parts, p.fanExact = true) (F : Tri → Int) :
    inX parts (X.mapL σ) F = ((instIn parts X).map fun x => F (x.eval σ)).sum := by
  unfold inX instIn
  rw [sum_map_flatMap]
  show ((List.range X.d).map _).sum = _
  congr 1
  apply List.map_congr_left
  intro i _
  rw [map_ite_nil_sum]
  show (if X.linkL i ≤ 8 then _ else 0) = _
  split_ifs
  · rw [sum_map_flatMap]
    congr 1
    apply List.map_congr_left
    intro p hp
    rw [sum_singleton_ite]
    show (if p.hub = X.linkL i then F (p.fit3At ((X.mapL σ).viewW i) (X.linkL i - 2)) else 0) = _
    rw [viewW_mapL hσ X hl, ← symFit_eval hσ p (hP p hp)]
  · rfl

theorem outX_sym {σ : Nat → Nat} (hσ : FixLow σ) (X : UWin) (hl : ∀ x ∈ X.link, x < 100) (parts : List Part)
    (hP : ∀ p ∈ parts, p.fanExact = true) (F : Tri → Int) :
    outX parts (X.mapL σ) F = ((instOut parts X).map fun x => F (x.eval σ)).sum := by
  unfold outX instOut
  simp only [show (X.mapL σ).d = X.d from rfl]
  rw [map_ite_nil_sum]
  split_ifs
  · rw [sum_map_flatMap]
    congr 1
    apply List.map_congr_left
    intro p hp
    rw [map_ite_nil_sum]
    split_ifs
    · rw [List.map_map, viewU_mapL hσ X hl]
      congr 1
      apply List.map_congr_left
      intro a _
      simp only [Function.comp]
      rw [symFit_eval hσ p (hP p hp)]
    · rfl
  · rfl

/-- The symbolic `hi` of a link word at a valuation. -/
def hiSymP (parts : List Part) (X : UWin) (σ : Nat → Nat) : Int :=
  10 * (6 - (X.d : Int)) + ((instIn parts X).map fun x => (x.eval σ).possI).sum -
    ((instOut parts X).map fun x => (x.eval σ).sureI).sum

theorem hi_mapL {σ : Nat → Nat} (hσ : FixLow σ) (X : UWin) (hl : ∀ x ∈ X.link, x < 100) (parts : List Part)
    (hP : ∀ p ∈ parts, p.fanExact = true) : (loHiP parts (X.mapL σ)).2 = hiSymP parts X σ := by
  rw [loHiP_eq]
  show 10 * (6 - ((X.mapL σ).d : Int)) + inX parts (X.mapL σ) Tri.possI - outX parts (X.mapL σ) Tri.sureI = _
  rw [inX_sym hσ X hl _ hP Tri.possI, outX_sym hσ X hl _ hP Tri.sureI]
  rfl

/-! ### 2'. Every real-shaped word is its tagged link word under `sigmaW` -/

theorem sigmaW_fix (W : UWin) : FixLow (sigmaW W) := by
  intro x hx; unfold sigmaW; simp [hx]

theorem npriv_le3 (L : Nat) : npriv L ≤ 3 := by
  unfold npriv; split_ifs <;> omega

theorem tag_map {W : UWin} (hW : RealShape W) (hd : W.d ≤ 30) : W = (tagW W.d W.link).mapL (sigmaW W) := by
  obtain ⟨h5, hlen, halen, hplen, -, -, hpriv⟩ := hW
  obtain ⟨d, link, apex, priv⟩ := W
  simp only at h5 hlen halen hplen hpriv hd ⊢
  simp only [UWin.mapL, tagW, UWin.mk.injEq, true_and]
  constructor
  · apply List.ext_getElem
    · simp [halen]
    · intro j h1 h2
      simp only [List.getElem_map, List.getElem_range, apexCode, sigmaW]
      have a1 : ¬ (100 + j < 100) := by omega
      have a2 : 100 + j < 200 := by omega
      simp only [a1, a2, ite_false, ite_true, show 100 + j - 100 = j by omega]
      rw [getD_lt' _ _ _ h1]
  · apply List.ext_getElem
    · simp [hplen]
    · intro i h1 h2
      have hi : i < d := by omega
      have hpl := (hpriv i hi).1
      simp only [UWin.linkL, getD_lt' _ _ _ h1] at hpl
      simp only [List.getElem_map, List.getElem_range]
      apply List.ext_getElem
      · simp [hpl]
      · intro k k1 k2
        simp only [List.length_map, List.length_range] at k2
        have hk3 : k < 3 := by have := npriv_le3 (link.getD i 9); omega
        simp only [List.getElem_map, List.getElem_range, privCode, sigmaW]
        have a1 : ¬ (200 + 3 * i + k < 100) := by omega
        have a2 : ¬ (200 + 3 * i + k < 200) := by omega
        simp only [a1, a2, ite_false, show (200 + 3 * i + k - 200) / 3 = i by omega,
          show (200 + 3 * i + k - 200) % 3 = k by omega]
        rw [getD_lt' _ _ _ h1, getD_lt' _ _ _ k1]

theorem sigmaW_range {W : UWin} (hW : RealShape W) (c : Nat) (hc : 100 ≤ c) : 5 ≤ sigmaW W c ∧ sigmaW W c ≤ 9 := by
  obtain ⟨-, -, -, hplen, -, hap, hpriv⟩ := hW
  have g : ∀ (l : List Nat) (n : Nat), (∀ x ∈ l, 5 ≤ x ∧ x ≤ 9) → 5 ≤ l.getD n 9 ∧ l.getD n 9 ≤ 9 := by
    intro l n hl
    rw [List.getD_eq_getElem?_getD]
    cases h : l[n]? with
    | none => simp
    | some x => simpa using hl x (List.mem_of_getElem? h)
  unfold sigmaW
  rw [if_neg (by omega)]
  split_ifs
  · exact g _ _ hap
  · apply g
    intro x hx
    by_cases hi : (c - 200) / 3 < W.d
    · exact (hpriv _ hi).2 x hx
    · rw [getD_ge' _ _ _ (by omega)] at hx; simp at hx

theorem hi_eq {W : UWin} (hW : RealShape W) (hd : W.d ≤ 30) (parts : List Part)
    (hP : ∀ p ∈ parts, p.fanExact = true) : (loHiP parts W).2 = hiSymP parts (tagW W.d W.link) (sigmaW W) := by
  have hl : ∀ x ∈ (tagW W.d W.link).link, x < 100 := by
    intro x hx; have := hW.2.2.2.2.1 x hx; omega
  have := hi_mapL (sigmaW_fix W) (tagW W.d W.link) hl parts hP
  rw [← tag_map hW hd] at this
  exact this

/-! ## 3. Kills -/

theorem vkind_s {d v i : Nat} (h : vkind d v = .s i) : i < d := by
  unfold vkind at h; split_ifs at h <;> simp only [VK.s.injEq, reduceCtorEq] at h; omega

theorem vkind_p {d v i k : Nat} (h : vkind d v = .p i k) : i < d ∧ k < 3 := by
  unfold vkind at h; split_ifs at h <;> simp only [VK.p.injEq, reduceCtorEq] at h; omega

theorem hostLetter_sym {W : UWin} (hd : W.d ≤ 30) (v : Nat) :
    hostLetter W v = match hostSym W.d W.link v with
      | .fixed y => some y
      | .var c => le8 (sigmaW W c)
      | .none => none := by
  unfold hostLetter hostSym
  cases hk : vkind W.d v with
  | u => rfl
  | w i => simp only [UWin.linkL]; cases le8 (W.link.getD i 9) <;> rfl
  | s i =>
    have := vkind_s hk
    have a1 : ¬ (100 + i < 100) := by omega
    have a2 : 100 + i < 200 := by omega
    simp only [apexCode, sigmaW, UWin.apexL, a1, a2, ite_false, ite_true, show 100 + i - 100 = i by omega]
  | p i k =>
    obtain ⟨hi, hk3⟩ := vkind_p hk
    have a1 : ¬ (200 + 3 * i + k < 100) := by omega
    have a2 : ¬ (200 + 3 * i + k < 200) := by omega
    by_cases hp : privOk (W.link.getD i 9) k = true
    · simp only [UWin.linkL, hp, ite_true, privCode, sigmaW, a1, a2, ite_false,
        show (200 + 3 * i + k - 200) / 3 = i by omega, show (200 + 3 * i + k - 200) % 3 = k by omega]
    · simp only [UWin.linkL, hp, Bool.false_eq_true, ite_false]
  | bad => rfl

theorem reqStep_all {W : UWin} (hd : W.d ≤ 30) (K : Conf) (e : List Nat) :
    ∀ (xs : List Nat) (R : List (Nat × Nat)), xs.foldr (reqStep K W.d W.link e) (some []) = some R →
      (∀ p ∈ R, sigmaW W p.1 = p.2) → xs.all (fun x => hostLetter W (e.getD x 0) == some (K.degOf x)) = true := by
  intro xs
  induction xs with
  | nil => intro _ _ _; rfl
  | cons x xs ih =>
    intro R h hs
    simp only [List.foldr_cons] at h
    rcases hacc : xs.foldr (reqStep K W.d W.link e) (some []) with _ | R0
    · rw [hacc] at h; simp [reqStep] at h
    · rw [hacc] at h
      simp only [reqStep] at h
      rw [List.all_cons, Bool.and_eq_true]
      have hl := hostLetter_sym (W := W) hd (e.getD x 0)
      cases hh : hostSym W.d W.link (e.getD x 0) with
      | fixed y =>
        rw [hh] at h hl
        simp only at h hl
        split_ifs at h with hy
        · simp only [Option.some.injEq] at h; subst h
          refine ⟨by rw [hl]; simpa using hy, ih R0 hacc hs⟩
      | var c =>
        rw [hh] at h hl
        simp only at h hl
        split_ifs at h with h8
        · simp only [Option.some.injEq] at h; subst h
          have hc := hs (c, K.degOf x) List.mem_cons_self
          refine ⟨?_, ih R0 hacc (fun p hp => hs p (List.mem_cons_of_mem _ hp))⟩
          rw [hl, hc]; simp [le8, h8]
      | none => rw [hh] at h; simp at h

theorem reqOf_sound {W : UWin} (hd : W.d ≤ 30) (K : Conf) (e : List Nat) (R : List (Nat × Nat))
    (h : reqOf K W.d W.link e = some R) (hs : ∀ p ∈ R, sigmaW W p.1 = p.2) : checkEmb K W e = true := by
  unfold reqOf at h
  split_ifs at h with hsh
  unfold checkEmb
  rw [hsh, Bool.true_and]
  exact reqStep_all hd K e _ R h hs

/-! ## 4. The DFS -/

theorem simp1_none {σ : Nat → Nat} {v : Nat} {S : List Nat} (hv : σ v ∈ S) {x : SRes} (h : simp1 v S x = none) :
    x.eval σ = .no := by
  cases x with
  | no => rfl
  | c cs o =>
    simp only [simp1] at h
    split_ifs at h with ha
    obtain ⟨cr, hcr, hc⟩ := List.any_eq_true.1 ha
    rw [Bool.and_eq_true, beq_iff_eq] at hc
    have hf : cr.2.test (σ cr.1) = false := by
      rw [hc.1]; have := List.all_eq_true.1 hc.2 _ hv; simpa using this
    simp only [SRes.eval]
    rw [if_neg]
    intro hall
    have := List.all_eq_true.1 hall cr hcr
    rw [hf] at this; cases this

theorem all_filter_of {α : Type} (l : List α) (q f : α → Bool) (h : ∀ x ∈ l, q x = false → f x = true) :
    (l.filter q).all f = l.all f := by
  induction l with
  | nil => rfl
  | cons a l ih =>
    have ih' := ih (fun x hx => h x (List.mem_cons_of_mem _ hx))
    rw [List.filter_cons, List.all_cons]
    cases hq : q a
    · simp only [Bool.false_eq_true, ite_false]; rw [ih', h a List.mem_cons_self hq, Bool.true_and]
    · simp only [ite_true, List.all_cons]; rw [ih']

theorem simp1_some {σ : Nat → Nat} {v : Nat} {S : List Nat} (hv : σ v ∈ S) {x y : SRes}
    (h : simp1 v S x = some y) : y.eval σ = x.eval σ := by
  cases x with
  | no => simp [simp1] at h
  | c cs o =>
    simp only [simp1] at h
    split_ifs at h with ha
    cases h
    simp only [SRes.eval]
    rw [all_filter_of]
    intro cr _ hq
    simp only [Bool.not_eq_false', Bool.and_eq_true, beq_iff_eq] at hq
    rw [hq.1]; have := List.all_eq_true.1 hq.2 _ hv; simpa using this

theorem sum_simp {σ : Nat → Nat} {v : Nat} {S : List Nat} (hv : σ v ∈ S) (F : Tri → Int) (hF : F .no = 0) :
    ∀ l : List SRes, ((l.filterMap (simp1 v S)).map fun x => F (x.eval σ)).sum = (l.map fun x => F (x.eval σ)).sum := by
  intro l
  induction l with
  | nil => rfl
  | cons a l ih =>
    rw [List.filterMap_cons]
    cases h : simp1 v S a with
    | none => simp only [List.map_cons, List.sum_cons]; rw [ih, simp1_none hv h, hF, zero_add]
    | some y => simp only [List.map_cons, List.sum_cons]; rw [ih, simp1_some hv h]

theorem simpR1_sat {σ : Nat → Nat} {v : Nat} {S : List Nat} (hv : σ v ∈ S) {R R' : List (Nat × Nat)}
    (h : simpR1 v S R = some R') (hs : ∀ p ∈ R', σ p.1 = p.2) : ∀ p ∈ R, σ p.1 = p.2 := by
  unfold simpR1 at h
  split_ifs at h with ha
  cases h
  intro p hp
  by_cases hpv : p.1 = v
  · have : ¬ ((p.1 == v && S != [p.2]) = true) := fun hh => ha (List.any_eq_true.2 ⟨p, hp, hh⟩)
    rw [hpv] at this ⊢
    simp only [beq_self_eq_true, Bool.true_and, bne_iff_ne, ne_eq, Decidable.not_not] at this
    rw [this] at hv; simpa using hv
  · exact hs p (List.mem_filter.2 ⟨hp, by simpa using hpv⟩)

theorem possI_le (t : Tri) : t.possI ≤ 1 := by cases t <;> decide
theorem sureI_nn (t : Tri) : 0 ≤ t.sureI := by cases t <;> decide
theorem possI_no : Tri.possI .no = 0 := rfl
theorem sureI_no : Tri.sureI .no = 0 := rfl

theorem sum_possI_le (σ : Nat → Nat) (l : List SRes) : (l.map fun x => (x.eval σ).possI).sum ≤ l.length := by
  induction l with
  | nil => simp
  | cons a l ih => simp only [List.map_cons, List.sum_cons, List.length_cons]; have := possI_le (a.eval σ); push_cast; omega

theorem certain_sure {σ : Nat → Nat} {x : SRes} (h : certain x = true) : x.eval σ = .sure := by
  unfold certain at h
  split at h
  · rfl
  · cases h

theorem sum_sureI_ge (σ : Nat → Nat) (l : List SRes) :
    ((l.filter certain).length : Int) ≤ (l.map fun x => (x.eval σ).sureI).sum := by
  induction l with
  | nil => simp
  | cons a l ih =>
    rw [List.filter_cons, List.map_cons, List.sum_cons]
    split_ifs with h
    · rw [List.length_cons, certain_sure h]; push_cast; have : Tri.sureI .sure = 1 := rfl; omega
    · have := sureI_nn (a.eval σ); omega

theorem coverOK_mem {cls : List (List Nat)} (h : coverOK cls = true) {l : Nat} (h5 : 5 ≤ l) (h9 : l ≤ 9) :
    ∃ S ∈ cls, l ∈ S := by
  unfold coverOK at h
  have hl : l ∈ [5, 6, 7, 8, 9] := by simp; omega
  obtain ⟨S, hS, hm⟩ := List.any_eq_true.1 (List.all_eq_true.1 h l hl)
  exact ⟨S, hS, by simpa using hm⟩

theorem dfs_sound (base : Int) (σ : Nat → Nat) :
    ∀ (vs : List (Nat × List (List Nat))) (ins outs : List SRes) (reqs : List (List (Nat × Nat))),
      dfs base vs ins outs reqs = true → (∀ p ∈ vs, 5 ≤ σ p.1 ∧ σ p.1 ≤ 9) →
      base + (ins.map fun x => (x.eval σ).possI).sum - (outs.map fun x => (x.eval σ).sureI).sum ≤ 0 ∨
        ∃ R ∈ reqs, ∀ p ∈ R, σ p.1 = p.2 := by
  intro vs
  induction vs with
  | nil =>
    intro ins outs reqs h _
    rw [dfs] at h
    split_ifs at h with h1 h2
    · left; have := sum_possI_le σ ins; have := sum_sureI_ge σ outs; omega
    · right; obtain ⟨R, hR, he⟩ := List.any_eq_true.1 h2
      exact ⟨R, hR, by rw [List.isEmpty_iff.1 he]; simp⟩
  | cons vc rest ih =>
    obtain ⟨v, cls⟩ := vc
    intro ins outs reqs h hvs
    rw [dfs] at h
    split_ifs at h with h1 h2
    · left; have := sum_possI_le σ ins; have := sum_sureI_ge σ outs; omega
    · right; obtain ⟨R, hR, he⟩ := List.any_eq_true.1 h2
      exact ⟨R, hR, by rw [List.isEmpty_iff.1 he]; simp⟩
    · simp only [Bool.and_eq_true] at h
      obtain ⟨hcov, hall⟩ := h
      obtain ⟨h5, h9⟩ := hvs (v, cls) List.mem_cons_self
      obtain ⟨S, hS, hvS⟩ := coverOK_mem hcov h5 h9
      have hsub := List.all_eq_true.1 hall S hS
      rcases ih _ _ _ hsub (fun p hp => hvs p (List.mem_cons_of_mem _ hp)) with hl | ⟨R', hR', hsat⟩
      · left
        rw [sum_simp hvS _ possI_no, sum_simp hvS _ sureI_no] at hl
        exact hl
      · right
        obtain ⟨R, hR, hRR⟩ := List.mem_filterMap.1 hR'
        exact ⟨R, hR, simpR1_sat hvS hRR hsat⟩

/-! ## The link and degree checks -/

theorem sum_filter_no (σ : Nat → Nat) (F : Tri → Int) (hF : F .no = 0) (l : List SRes) :
    ((l.filter (· != .no)).map fun x => F (x.eval σ)).sum = (l.map fun x => F (x.eval σ)).sum := by
  rw [sum_map_filter]
  congr 1
  apply List.map_congr_left
  intro x _
  by_cases hx : x = .no
  · subst hx; simp [SRes.eval, hF]
  · simp [hx]

theorem checkLink_sound (parts : List Part) (hP : ∀ p ∈ parts, p.fanExact = true) (KL : List Conf) (d : Nat)
    (link : List Nat) (c : LinkCert)
    (h : checkLinkP parts KL d link c = true) (W : UWin) (hW : RealShape W) (hd : W.d = d) (hl : W.link = link)
    (hd30 : d ≤ 30) (hpos : 0 < (loHiP parts W).2) : Kills KL W := by
  unfold checkLinkP at h
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
      exact ⟨K, List.mem_of_getElem? hK, ke.2, reqOf_sound (by omega) K ke.2 R hR hsat⟩

theorem checkLinks_mem (parts : List Part) (KL : List Conf) (d : Nat) :
    ∀ (ls : List (List Nat)) (cs : List LinkCert), checkLinksP parts KL d ls cs = true →
      ∀ l ∈ ls, ∃ c, checkLinkP parts KL d l c = true := by
  intro ls
  induction ls with
  | nil => intro _ _ l hl; simp at hl
  | cons a ls ih =>
    intro cs h l hl
    cases cs with
    | nil =>
      simp only [checkLinksP, Bool.and_eq_true] at h
      rcases List.mem_cons.1 hl with rfl | hl
      · exact ⟨_, h.1⟩
      · exact ih [] h.2 l hl
    | cons c cs =>
      simp only [checkLinksP, Bool.and_eq_true] at h
      rcases List.mem_cons.1 hl with rfl | hl
      · exact ⟨_, h.1⟩
      · exact ih cs h.2 l hl

theorem allWords_mem : ∀ (l : List Nat), (∀ x ∈ l, 5 ≤ x ∧ x ≤ 9) → l ∈ allWords l.length := by
  intro l
  induction l with
  | nil => intro _; simp [allWords]
  | cons a l ih =>
    intro h
    have ha := h a List.mem_cons_self
    have hl := ih (fun x hx => h x (List.mem_cons_of_mem _ hx))
    simp only [List.length_cons, allWords, List.mem_flatMap, List.mem_map]
    refine ⟨a, ?_, l, hl, rfl⟩
    simp; omega

/-- **B5 soundness for one degree, any part list** (whose parts pass `fanExact`, checked by `checkDegP`), against
B4's `loHiP parts`. -/
theorem checkDegP_sound (parts : List Part) (KL : List Conf) (d : Nat) (cert : List LinkCert)
    (h : checkDegP parts KL d cert = true) :
    ∀ W : UWin, RealShape W → W.d = d → 0 < (loHiP parts W).2 → Kills KL W := by
  intro W hW hd hpos
  unfold checkDegP at h
  simp only [Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨⟨⟨hP, h5⟩, h30⟩, hl⟩ := h
  have hP' : ∀ p ∈ parts, p.fanExact = true := fun p hp => List.all_eq_true.1 hP p hp
  have hmem : W.link ∈ allWords d := by
    have := allWords_mem W.link hW.2.2.2.2.1
    rwa [hW.2.1, hd] at this
  obtain ⟨c, hc⟩ := checkLinks_mem parts KL d _ cert hl W.link hmem
  exact checkLink_sound parts hP' KL d W.link c hc W hW hd rfl h30 hpos

/-- **B5 soundness for one degree** (the 71 RSST parts, B2's `UWin.loHi`). -/
theorem checkDeg_sound (KL : List Conf) (d : Nat) (cert : List LinkCert) (h : checkDeg KL d cert = true) :
    ∀ W : UWin, RealShape W → W.d = d → 0 < W.loHi.2 → Kills KL W := by
  intro W hW hd hpos
  rw [loHi_eq] at hpos
  exact checkDegP_sound rsstParts KL d cert h W hW hd hpos

/-- Kills are monotone in the kill list: a proof against a sub-list holds for any larger final list. -/
theorem Kills.mono {KL KL' : List Conf} (h : ∀ K ∈ KL, K ∈ KL') {W : UWin} (hk : Kills KL W) : Kills KL' W := by
  obtain ⟨K, hK, e, he⟩ := hk
  exact ⟨K, h K hK, e, he⟩

#print axioms checkDegP_sound
#print axioms checkDeg_sound

end SimpleGraph.SphericalMap.RSSTSeed
