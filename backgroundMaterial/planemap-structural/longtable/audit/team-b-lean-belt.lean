module
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyShortFillTeamB
public import Mathlib.Data.ZMod.Basic
public import Mathlib.Tactic

@[expose] public section
namespace SimpleGraph.TwoPoleBeltTeamB
open VacancySlide VacancyShortFillTeamB

inductive Vertex (n : ℕ)
  | a | b | u (i : ZMod n) | v (i : ZMod n)
  deriving DecidableEq

def RawAdj {n : ℕ} : Vertex n → Vertex n → Prop
  | .a, .u _ | .u _, .a | .b, .v _ | .v _, .b => True
  | .u i, .u j | .v i, .v j => j = i + 1 ∨ i = j + 1
  | .u i, .v j | .v j, .u i => j = i ∨ j + 1 = i
  | _, _ => False

def graph (n : ℕ) : SimpleGraph (Vertex n) where
  Adj x y := x ≠ y ∧ RawAdj x y
  symm := ⟨by
    intro x y h
    refine ⟨h.1.symm,?_⟩
    cases x <;> cases y <;> simp_all [RawAdj,eq_comm,or_comm]⟩
  loopless := ⟨fun _ h => h.1 rfl⟩

variable {n : ℕ}

lemma rawAdj_symm {x y : Vertex n} (h : RawAdj x y) : RawAdj y x := by
  cases x <;> cases y <;> simp_all [RawAdj,eq_comm,or_comm]

lemma u_a (i : ZMod n) : (graph n).Adj (.u i) .a := by simp [graph,RawAdj]
lemma v_b (i : ZMod n) : (graph n).Adj (.v i) .b := by simp [graph,RawAdj]
lemma u_v (i : ZMod n) : (graph n).Adj (.u i) (.v i) := by simp [graph,RawAdj]
lemma u_v_prev (i : ZMod n) : (graph n).Adj (.u i) (.v (i-1)) := by simp [graph,RawAdj]

lemma plus_one_ne [Fact (1 < n)] (i : ZMod n) : i + 1 ≠ i := by
  intro h
  have : (1 : ZMod n) = 0 := by linear_combination h
  exact one_ne_zero this
lemma minus_one_ne [Fact (1 < n)] (i : ZMod n) : i - 1 ≠ i := by
  intro h
  have : (1 : ZMod n) = 0 := by linear_combination -h
  exact one_ne_zero this

/-- Actual complete five-neighbour description, with no assumed local move table. -/
lemma neighbors_u [Fact (1 < n)] (i : ZMod n) (x : Vertex n) :
    (graph n).Adj (.u i) x ↔
      x = .a ∨ x = .u (i+1) ∨ x = .v i ∨ x = .v (i-1) ∨ x = .u (i-1) := by
  cases x with
  | a => simp [graph,RawAdj]
  | b => simp [graph,RawAdj]
  | u j =>
    simp only [graph,RawAdj,Vertex.u.injEq,ne_eq,reduceCtorEq,false_or]
    constructor
    · rintro ⟨hne,h | h⟩
      · exact Or.inl h
      · right; linear_combination -h
    · rintro (rfl | h)
      · exact ⟨(plus_one_ne i).symm,Or.inl rfl⟩
      · subst j
        exact ⟨(minus_one_ne i).symm,Or.inr (by ring)⟩
  | v j =>
    simp only [graph,RawAdj,ne_eq,reduceCtorEq,not_false_eq_true,true_and,
      Vertex.v.injEq,or_false,false_or]
    constructor
    · rintro (h | h)
      · exact Or.inl h
      · right; linear_combination h
    · rintro (rfl | rfl)
      · exact Or.inl rfl
      · exact Or.inr (by ring)

lemma neighbors_v [Fact (1 < n)] (i : ZMod n) (x : Vertex n) :
    (graph n).Adj (.v i) x ↔
      x = .b ∨ x = .v (i-1) ∨ x = .u i ∨ x = .u (i+1) ∨ x = .v (i+1) := by
  cases x with
  | a => simp [graph,RawAdj]
  | b => simp [graph,RawAdj]
  | u j =>
    simp only [graph,RawAdj,ne_eq,reduceCtorEq,not_false_eq_true,true_and,
      Vertex.u.injEq,or_false,false_or]
    constructor
    · rintro (h | h)
      · exact Or.inl h.symm
      · exact Or.inr h.symm
    · rintro (rfl | rfl)
      · exact Or.inl rfl
      · exact Or.inr rfl
  | v j =>
    simp only [graph,RawAdj,Vertex.v.injEq,ne_eq,reduceCtorEq,false_or]
    constructor
    · rintro ⟨hne,h | h⟩
      · exact Or.inr h
      · left; linear_combination -h
    · rintro (h | rfl)
      · subst j
        exact ⟨(minus_one_ne i).symm,Or.inr (by ring)⟩
      · exact ⟨(plus_one_ne i).symm,Or.inl rfl⟩

/-- An actual slides-only path; the hole labels are total colours as in VacancySlide. -/
inductive SlidePath : (Vertex n × (Vertex n → Fin 4)) →
    (Vertex n × (Vertex n → Fin 4)) → ℕ → Prop
  | nil (s) : SlidePath s s 0
  | cons {r u c t k} : (graph n).Adj r u → UniqueAt (graph n) r u c →
      SlidePath (u,slide r u c) t k → SlidePath (r,c) t (k+1)

lemma SlidePath.proper {s t : Vertex n × (Vertex n → Fin 4)} {k : ℕ}
    (p : SlidePath s t k) (hc : ProperOff (graph n) s.1 s.2) :
    ProperOff (graph n) t.1 t.2 := by
  induction p with
  | nil => exact hc
  | cons adj unique p ih => exact ih (properOff_slide (graph n) hc unique)


/-- The first doubled-0 opening really fills in one slide on the actual belt graph. -/
lemma doubled_zero_I_short [Fact (1 < n)] (i : ZMod n) (c : Vertex n → Fin 4)
    (ha : c .a = 0) (hb : c .b = 1)
    (hup : c (.u (i+1)) = 1) (hvi : c (.v i) = 2)
    (hvm : c (.v (i-1)) = 0) (hum : c (.u (i-1)) = 3)
    (hvp : c (.v (i+1)) = 0) :
    UniqueAt (graph n) (.u i) (.v i) c ∧
      Target (graph n) (.v i) (slide (.u i) (.v i) c) := by
  constructor
  · intro w hw heq
    rcases (neighbors_u i w).mp hw with rfl | rfl | rfl | rfl | rfl
    · simp [ha,hvi] at heq
    · simp [hup,hvi] at heq
    · rfl
    · simp [hvm,hvi] at heq
    · simp [hum,hvi] at heq
  · refine ⟨3,?_⟩
    intro w hw
    rcases (neighbors_v i w).mp hw with rfl | rfl | rfl | rfl | rfl
    · simp [slide,hb]
    · simp [slide,hvm]
    · simp [slide,hvi]
    · simp [slide,hup,plus_one_ne i]
    · simp [slide,hvp]

lemma doubled_zero_I_short_path [Fact (1 < n)] (i : ZMod n) (c : Vertex n → Fin 4)
    (hc : ProperOff (graph n) (.u i) c)
    (ha : c .a = 0) (hb : c .b = 1)
    (hup : c (.u (i+1)) = 1) (hvi : c (.v i) = 2)
    (hvm : c (.v (i-1)) = 0) (hum : c (.u (i-1)) = 3)
    (hvp : c (.v (i+1)) = 0) :
    ∃ t, SlidePath (.u i,c) t 1 ∧
      ProperOff (graph n) t.1 t.2 ∧ Target (graph n) t.1 t.2 := by
  obtain ⟨hu,ht⟩ := doubled_zero_I_short i c ha hb hup hvi hvm hum hvp
  refine ⟨(.v i,slide (.u i) (.v i) c),?_,?_,ht⟩
  · exact SlidePath.cons (u_v i) hu (SlidePath.nil _)
  · exact properOff_slide (graph n) hc hu


lemma offset_ne (i : ZMod n) (k : ℕ) (hk : 0 < k) (hkn : k < n) :
    i + (k : ZMod n) ≠ i := by
  intro h
  have hzero : (k : ZMod n) = 0 := by linear_combination h
  have hdvd : n ∣ k := (ZMod.natCast_eq_zero_iff k n).mp hzero
  exact (not_le_of_gt hkn) (Nat.le_of_dvd hk hdvd)

lemma u_next [Fact (1 < n)] (i : ZMod n) : (graph n).Adj (.u i) (.u (i+1)) := by
  exact (neighbors_u i _).mpr (Or.inr (Or.inl rfl))
lemma v_next [Fact (1 < n)] (i : ZMod n) : (graph n).Adj (.v i) (.v (i+1)) := by
  exact (neighbors_v i _).mpr (Or.inr (Or.inr (Or.inr (Or.inr rfl))))

lemma forced_zero (rho tau x : Fin 4) (hr0 : rho ≠ 0) (hr1 : rho ≠ 1)
    (ht0 : tau ≠ 0) (ht1 : tau ≠ 1) (hrt : rho ≠ tau)
    (hx1 : x ≠ 1) (hxr : x ≠ rho) (hxt : x ≠ tau) : x = 0 := by
  fin_cases rho <;> fin_cases tau <;> fin_cases x <;> simp_all
lemma allowed_one_rho (rho tau x : Fin 4) (hr0 : rho ≠ 0) (hr1 : rho ≠ 1)
    (ht0 : tau ≠ 0) (ht1 : tau ≠ 1) (hrt : rho ≠ tau)
    (hx0 : x ≠ 0) (hxt : x ≠ tau) : x = 1 ∨ x = rho := by
  fin_cases rho <;> fin_cases tau <;> fin_cases x <;> simp_all

/-- Properness forces the next lower zero and the lookahead branch in doubled-0 II. -/
lemma doubled_zero_II_forced (hn : 5 ≤ n) (i : ZMod n) (c : Vertex n → Fin 4)
    (hc : ProperOff (graph n) (.u i) c) (rho tau : Fin 4)
    (hr0 : rho ≠ 0) (hr1 : rho ≠ 1) (ht0 : tau ≠ 0) (ht1 : tau ≠ 1) (hrt : rho ≠ tau)
    (ha : c .a = 0) (hb : c .b = 1)
    (hup : c (.u (i+1)) = tau) (hvi : c (.v i) = rho) :
    c (.v (i+1)) = 0 ∧ (c (.u (i+2)) = 1 ∨ c (.u (i+2)) = rho) := by
  let : Fact (1 < n) := ⟨by omega⟩
  have hupne : (Vertex.u (i+1) : Vertex n) ≠ .u i := by simp
  have hunne : (Vertex.u (i+2) : Vertex n) ≠ .u i := by
    simpa using offset_ne i 2 (by omega) (by omega)
  have hv0 : c (.v (i+1)) = 0 := by
    apply forced_zero rho tau _ hr0 hr1 ht0 ht1 hrt
    · have h := hc (v_b (i+1)) (by simp) (by simp)
      simpa [hb] using h
    · have h := hc (v_next i).symm (by simp) (by simp)
      simpa [hvi] using h
    · have h := hc (u_v (i+1)).symm (by simp) hupne
      simpa [hup] using h
  refine ⟨hv0,?_⟩
  apply allowed_one_rho rho tau _ hr0 hr1 ht0 ht1 hrt
  · have h := hc (u_a (i+2)) hunne (by simp)
    simpa [ha] using h
  · have h := hc (u_next (i+1)).symm (by simpa [add_assoc,one_add_one_eq_two] using hunne) hupne
    simpa [hup,add_assoc,one_add_one_eq_two] using h


/-- Doubled-0 II always has its first slide; the finite palette forces fill or a second legal slide. -/
lemma doubled_zero_II_first (hn : 5 ≤ n) (i : ZMod n) (c : Vertex n → Fin 4)
    (hc : ProperOff (graph n) (.u i) c) (rho tau : Fin 4)
    (hr0 : rho ≠ 0) (hr1 : rho ≠ 1) (ht0 : tau ≠ 0) (ht1 : tau ≠ 1) (hrt : rho ≠ tau)
    (ha : c .a = 0) (hb : c .b = 1)
    (hup : c (.u (i+1)) = tau) (hvi : c (.v i) = rho)
    (hvm : c (.v (i-1)) = 0) (hum : c (.u (i-1)) = 1) :
    UniqueAt (graph n) (.u i) (.u (i+1)) c ∧
    (Target (graph n) (.u (i+1)) (slide (.u i) (.u (i+1)) c) ∨
      UniqueAt (graph n) (.u (i+1)) (.u (i+2)) (slide (.u i) (.u (i+1)) c)) := by
  let : Fact (1 < n) := ⟨by omega⟩
  obtain ⟨hv0,hbranch⟩ := doubled_zero_II_forced hn i c hc rho tau hr0 hr1 ht0 ht1 hrt ha hb hup hvi
  have hunne : (Vertex.u (i+2) : Vertex n) ≠ .u i := by
    simpa using offset_ne i 2 (by omega) (by omega)
  constructor
  · intro w hw heq
    rcases (neighbors_u i w).mp hw with rfl | rfl | rfl | rfl | rfl
    · rw [ha,hup] at heq; exact (ht0 heq.symm).elim
    · rfl
    · rw [hvi,hup] at heq; exact (hrt heq).elim
    · rw [hvm,hup] at heq; exact (ht0 heq.symm).elim
    · rw [hum,hup] at heq; exact (ht1 heq.symm).elim
  · rcases hbranch with hb1 | hbr
    · right
      intro w hw heq
      have hlook : slide (.u i) (.u (i+1)) c (.u (i+2)) = 1 := by
        rw [slide_away _ _ _ hunne,hb1]
      rw [hlook] at heq
      rcases (neighbors_u (i+1) w).mp hw with rfl | rfl | rfl | rfl | rfl
      · simp [slide,ha] at heq
      · congr 1; ring
      · simp [slide,hv0] at heq
      · simp [slide,hvi,hr1] at heq
      · simp [slide,hup,ht1] at heq
    · left
      refine ⟨1,?_⟩
      intro w hw
      rcases (neighbors_u (i+1) w).mp hw with rfl | rfl | rfl | rfl | rfl
      · simp [slide,ha]
      · simpa only [add_assoc,one_add_one_eq_two,slide_away _ _ _ hunne,hbr] using hr1
      · simp [slide,hv0]
      · simp [slide,hvi,hr1]
      · simp [slide,hup,ht1]


def NonpolePair (rho tau : Fin 4) : Prop :=
  rho ≠ 0 ∧ rho ≠ 1 ∧ tau ≠ 0 ∧ tau ≠ 1 ∧ rho ≠ tau

def DoubledZeroII (i : ZMod n) (c : Vertex n → Fin 4) (rho tau : Fin 4) : Prop :=
  NonpolePair rho tau ∧ c .a = 0 ∧ c .b = 1 ∧
    c (.u (i+1)) = tau ∧ c (.v i) = rho ∧ c (.v (i-1)) = 0 ∧ c (.u (i-1)) = 1

/-- The nonfilling branch returns the actual doubled-0 II word two indices ahead. -/
lemma doubled_zero_II_return (hn : 5 ≤ n) (i : ZMod n) (c : Vertex n → Fin 4)
    (hc : ProperOff (graph n) (.u i) c) (rho tau : Fin 4)
    (hword : DoubledZeroII i c rho tau) (hb1 : c (.u (i+2)) = 1) :
    ∃ d rho' tau', d = slide (.u (i+1)) (.u (i+2)) (slide (.u i) (.u (i+1)) c) ∧
      SlidePath (.u i,c) (.u (i+2),d) 2 ∧
      ProperOff (graph n) (.u (i+2)) d ∧ DoubledZeroII (i+2) d rho' tau' := by
  let : Fact (1 < n) := ⟨by omega⟩
  obtain ⟨⟨hr0,hr1,ht0,ht1,hrt⟩,ha,hb,hup,hvi,hvm,hum⟩ := hword
  obtain ⟨hv0,_⟩ := doubled_zero_II_forced hn i c hc rho tau hr0 hr1 ht0 ht1 hrt ha hb hup hvi
  have h2 : (Vertex.u (i+2) : Vertex n) ≠ .u i := by
    simpa using offset_ne i 2 (by omega) (by omega)
  have h3 : (Vertex.u (i+3) : Vertex n) ≠ .u i := by
    simpa using offset_ne i 3 (by omega) (by omega)
  have h31 : (Vertex.u (i+3) : Vertex n) ≠ .u (i+1) := by
    intro heq
    have heq' := Vertex.u.inj heq
    have hh : (i+1)+(2 : ZMod n) = i+1 := by linear_combination heq'
    exact offset_ne (i+1) 2 (by omega) (by omega) hh
  let q := c (.v (i+2))
  let p := c (.u (i+3))
  have hq0 : q ≠ 0 := by
    have hh := hc (v_next (i+1)).symm (by simp) (by simp)
    simpa [q,hv0,add_assoc,one_add_one_eq_two] using hh
  have hq1 : q ≠ 1 := by
    have hh := hc (v_b (i+2)) (by simp) (by simp)
    simpa [q,hb] using hh
  have hp0 : p ≠ 0 := by
    have hh := hc (u_a (i+3)) h3 (by simp)
    simpa [p,ha] using hh
  have hp1 : p ≠ 1 := by
    have edge := u_next (i+2)
    have heq : (i+2)+1 = i+3 := by ring
    rw [heq] at edge
    have hh := hc edge.symm h3 h2
    simpa [p,hb1] using hh
  have hpq : p ≠ q := by
    have hh := hc (u_v_prev (i+3)) h3 (by simp)
    simpa [p,q,show i+3-1 = i+2 by ring] using hh
  let c1 := slide (.u i) (.u (i+1)) c
  let d := slide (.u (i+1)) (.u (i+2)) c1
  have hc1 : ProperOff (graph n) (.u (i+1)) c1 := by
    have hh := (doubled_zero_II_first hn i c hc rho tau hr0 hr1 ht0 ht1 hrt ha hb hup hvi hvm hum).1
    exact properOff_slide (graph n) hc hh
  have unique1 : UniqueAt (graph n) (.u i) (.u (i+1)) c :=
    (doubled_zero_II_first hn i c hc rho tau hr0 hr1 ht0 ht1 hrt ha hb hup hvi hvm hum).1
  have unique2 : UniqueAt (graph n) (.u (i+1)) (.u (i+2)) c1 := by
    intro w hw heq
    have hlook : c1 (.u (i+2)) = 1 := by
      dsimp [c1]
      rw [slide_away _ _ _ h2,hb1]
    rw [hlook] at heq
    rcases (neighbors_u (i+1) w).mp hw with rfl | rfl | rfl | rfl | rfl
    · simp [c1,ha] at heq
    · congr 1; ring
    · simp [c1,hv0] at heq
    · simp [c1,hvi,hr1] at heq
    · simp [c1,hup,ht1] at heq
  refine ⟨d,q,p,rfl,?_,properOff_slide (graph n) hc1 unique2,?_,?_,?_,?_,?_,?_,?_⟩
  · have edge2 : (graph n).Adj (.u (i+1)) (.u (i+2)) := by
      have edge := u_next (i+1)
      have heq : (i+1)+1 = i+2 := by ring
      rw [heq] at edge
      exact edge
    exact SlidePath.cons (u_next i) unique1 (SlidePath.cons edge2 unique2 (SlidePath.nil _))
  · exact ⟨hq0,hq1,hp0,hp1,hpq.symm⟩
  · simp [d,c1,slide,ha]
  · simp [d,c1,slide,hb]
  · have heq : i+2+1 = i+3 := by ring
    rw [heq]
    dsimp [d,c1]
    rw [slide_away _ _ _ h31,slide_away _ _ _ h3]
  · simp [d,c1,slide,q]
  · have heq : i+2-1 = i+1 := by ring
    simp [d,c1,slide,hv0,heq]
  · have heq : i+2-1 = i+1 := by ring
    rw [heq]
    dsimp [d,c1]
    rw [slide_at,slide_away _ _ _ h2,hb1]


lemma natCast_inj_below {j k : ℕ} (hj : j < n) (hk : k < n)
    (heq : (j : ZMod n) = (k : ZMod n)) : j = k := by
  have hv := congrArg ZMod.val heq
  simpa [ZMod.val_natCast_of_lt hj,ZMod.val_natCast_of_lt hk] using hv

/-- The fixed original cap excludes the last two possible upper-hole indices. -/
lemma doubled_zero_II_cap (hn : 5 ≤ n) (j : ℕ) (hj : j ≤ n-2)
    (c : Vertex n → Fin 4) (rho tau : Fin 4)
    (hc : ProperOff (graph n) (.u (j : ZMod n)) c)
    (hw : DoubledZeroII (j : ZMod n) c rho tau)
    (hcapu : c (.u ((n-1 : ℕ) : ZMod n)) = 1)
    (hcapv : c (.v ((n-1 : ℕ) : ZMod n)) = 0) : j+3 < n := by
  let : Fact (1 < n) := ⟨by omega⟩
  obtain ⟨⟨hr0,hr1,ht0,ht1,hrt⟩,ha,hb,hup,hvi,hvm,hum⟩ := hw
  by_contra hsmall
  have cases : j = n-3 ∨ j = n-2 := by omega
  rcases cases with hj | hj
  · have hj2 : j+2 = n-1 := by omega
    obtain ⟨hz,_⟩ := doubled_zero_II_forced hn (j : ZMod n) c hc rho tau hr0 hr1 ht0 ht1 hrt ha hb hup hvi
    have edge := v_next ((j : ZMod n)+1)
    have hpro := hc edge (by simp) (by simp)
    have heq : ((j : ZMod n)+1)+1 = ((n-1 : ℕ) : ZMod n) := by
      calc
        _ = ((j+2 : ℕ) : ZMod n) := by simp [Nat.cast_add,add_assoc,one_add_one_eq_two]
        _ = _ := by rw [hj2]
    rw [hz,heq,hcapv] at hpro
    exact hpro rfl
  · have hj1 : j+1 = n-1 := by omega
    have heq : (j : ZMod n)+1 = ((n-1 : ℕ) : ZMod n) := by
      rw [← Nat.cast_one,← Nat.cast_add,hj1]
    rw [heq,hcapu] at hup
    exact ht1 hup.symm

lemma SlidePath.append {s t w : Vertex n × (Vertex n → Fin 4)} {k m : ℕ}
    (p : SlidePath s t k) (q : SlidePath t w m) : SlidePath s w (k+m) := by
  induction p with
  | nil => simpa using q
  | cons adj unique p ih =>
    have hh := SlidePath.cons adj unique (ih q)
    simpa [Nat.add_assoc,Nat.add_comm,Nat.add_left_comm] using hh


/-- Fully derived cap termination for the doubled-0 II walk, with an actual slide budget. -/
theorem doubled_zero_II_terminates (hn : 5 ≤ n) (j : ℕ) (hj : j ≤ n-2)
    (c : Vertex n → Fin 4) (rho tau : Fin 4)
    (hc : ProperOff (graph n) (.u (j : ZMod n)) c)
    (hw : DoubledZeroII (j : ZMod n) c rho tau)
    (hcapu : c (.u ((n-1 : ℕ) : ZMod n)) = 1)
    (hcapv : c (.v ((n-1 : ℕ) : ZMod n)) = 0) :
    ∃ k t, k ≤ n-j ∧ SlidePath (.u (j : ZMod n),c) t k ∧
      ProperOff (graph n) t.1 t.2 ∧ Target (graph n) t.1 t.2 := by
  let : Fact (1 < n) := ⟨by omega⟩
  generalize heq : n-j = m
  induction m using Nat.strong_induction_on generalizing j c rho tau with
  | h m ih =>
    have hsmall : j+3 < n := doubled_zero_II_cap hn j hj c rho tau hc hw hcapu hcapv
    obtain ⟨⟨hr0,hr1,ht0,ht1,hrt⟩,ha,hb,hup,hvi,hvm,hum⟩ := hw
    have hword : DoubledZeroII (j : ZMod n) c rho tau :=
      ⟨⟨hr0,hr1,ht0,ht1,hrt⟩,ha,hb,hup,hvi,hvm,hum⟩
    obtain ⟨unique1,hnext⟩ := doubled_zero_II_first hn (j : ZMod n) c hc rho tau
      hr0 hr1 ht0 ht1 hrt ha hb hup hvi hvm hum
    rcases hnext with hfill | unique2
    · refine ⟨1,(.u ((j : ZMod n)+1),slide (.u (j : ZMod n)) (.u ((j : ZMod n)+1)) c),?_,?_,?_,hfill⟩
      · omega
      · exact SlidePath.cons (u_next _) unique1 (SlidePath.nil _)
      · exact properOff_slide (graph n) hc unique1
    · obtain ⟨hv0,hbranch⟩ := doubled_zero_II_forced hn (j : ZMod n) c hc rho tau
        hr0 hr1 ht0 ht1 hrt ha hb hup hvi
      have hb1 : c (.u ((j : ZMod n)+2)) = 1 := by
        rcases hbranch with hb1 | hbr
        · exact hb1
        · have hedge : (graph n).Adj (.u ((j : ZMod n)+1)) (.v (j : ZMod n)) := by
            apply (neighbors_u _ _).mpr
            right; right; right; left
            congr 1; ring
          have hne : (Vertex.u ((j : ZMod n)+2) : Vertex n) ≠ .u (j : ZMod n) := by
            simpa using offset_ne (j : ZMod n) 2 (by omega) (by omega)
          have same : slide (.u (j : ZMod n)) (.u ((j : ZMod n)+1)) c (.v (j : ZMod n)) =
              slide (.u (j : ZMod n)) (.u ((j : ZMod n)+1)) c (.u ((j : ZMod n)+2)) := by
            rw [slide_away _ _ _ (by simp),slide_away _ _ _ hne,hvi,hbr]
          have impossible := unique2 hedge same
          cases impossible
      obtain ⟨d,rho',tau',hd,path,hproper,hword'⟩ := doubled_zero_II_return hn
        (j : ZMod n) c hc rho tau hword hb1
      have cap0 : (Vertex.u ((n-1 : ℕ) : ZMod n) : Vertex n) ≠ .u (j : ZMod n) := by
        intro he
        have hnat := natCast_inj_below (by omega : n-1 < n) (by omega : j < n) (Vertex.u.inj he)
        omega
      have cap1 : (Vertex.u ((n-1 : ℕ) : ZMod n) : Vertex n) ≠ .u ((j : ZMod n)+1) := by
        intro he
        have he' := Vertex.u.inj he
        have hcast : (j : ZMod n)+1 = ((j+1 : ℕ) : ZMod n) := by simp [Nat.cast_add]
        rw [hcast] at he'
        have hnat := natCast_inj_below (by omega : n-1 < n) (by omega : j+1 < n) he'
        omega
      have hcapu' : d (.u ((n-1 : ℕ) : ZMod n)) = 1 := by
        rw [hd]
        simp [slide,cap0,cap1,hcapu]
      have hcapv' : d (.v ((n-1 : ℕ) : ZMod n)) = 0 := by
        rw [hd]
        simp [slide,hcapv]
      have hsum : (j : ZMod n)+2 = ((j+2 : ℕ) : ZMod n) := by simp [Nat.cast_add]
      rw [hsum] at path hproper hword'
      have hm' : n-(j+2) < m := by omega
      obtain ⟨k,t,hk,hpath,hpt,htt⟩ := ih (n-(j+2)) hm' (j+2) (by omega)
        d rho' tau' hproper hword' hcapu' hcapv' rfl
      refine ⟨2+k,t,?_,path.append hpath,hpt,htt⟩
      omega


/-- All doubled-0 II starts at u_0 fill in at most n actual slides. -/
theorem doubled_zero_II_u0 (hn : 5 ≤ n) (c : Vertex n → Fin 4) (rho tau : Fin 4)
    (hc : ProperOff (graph n) (.u 0) c) (hw : DoubledZeroII 0 c rho tau) :
    ∃ k t, k ≤ n ∧ SlidePath (.u 0,c) t k ∧
      ProperOff (graph n) t.1 t.2 ∧ Target (graph n) t.1 t.2 := by
  have hcap : ((n-1 : ℕ) : ZMod n) = -1 := by
    rw [Nat.cast_sub (by omega : 1 ≤ n),ZMod.natCast_self,Nat.cast_one]
    ring
  have hcapu : c (.u ((n-1 : ℕ) : ZMod n)) = 1 := by
    rw [hcap]
    simpa only [zero_sub] using hw.2.2.2.2.2.2
  have hcapv : c (.v ((n-1 : ℕ) : ZMod n)) = 0 := by
    rw [hcap]
    simpa only [zero_sub] using hw.2.2.2.2.2.1
  simpa only [Nat.cast_zero, Nat.sub_zero] using doubled_zero_II_terminates hn 0 (by omega) c rho tau (by simpa using hc) (by simpa using hw) (by simpa using hcapu) (by simpa using hcapv)

/-- The A-rho terminal branch consists of two actual singleton slides. -/
theorem a_rho_two_slide_fill (hn : 5 ≤ n) (j : ZMod n)
    (c : Vertex n → Fin 4) (rho tau : Fin 4) (hp : NonpolePair rho tau)
    (hc : ProperOff (graph n) (.v (j+1)) c)
    (ha : c .a = 0) (hb : c .b = 1)
    (houter : c (.u (j+1)) = tau) (hmid : c (.u j) = 1)
    (hinner : c (.u (j-1)) = rho) (htrail : c (.u (j+2)) = rho)
    (hfront : c (.v j) = rho) (hzero : c (.v (j-1)) = 0)
    (hback : c (.v (j+2)) = 0) :
    ∃ t, SlidePath (.v (j+1),c) t 2 ∧
      ProperOff (graph n) t.1 t.2 ∧ Target (graph n) t.1 t.2 := by
  let : Fact (1 < n) := ⟨by omega⟩
  obtain ⟨hr0,hr1,ht0,ht1,hrt⟩ := hp
  have hplus : j+1 ≠ j := plus_one_ne j
  have hminus : j-1 ≠ j+1 := by
    intro heq
    apply offset_ne (j-1) 2 (by omega) (by omega)
    linear_combination -heq
  have htwo : j+2 ≠ j+1 := by
    have h := plus_one_ne (j+1)
    convert h using 1; ring
  have hnext : (j+1)+1 = j+2 := by ring
  have hprev : (j+1)-1 = j := by ring
  let c1 := slide (.v (j+1)) (.u (j+1)) c
  let c2 := slide (.u (j+1)) (.u j) c1
  have unique1 : UniqueAt (graph n) (.v (j+1)) (.u (j+1)) c := by
    intro w edge heq
    rw [houter] at heq
    rcases (neighbors_v (j+1) w).mp edge with rfl | rfl | rfl | rfl | rfl
    · simp [hb,Ne.symm ht1] at heq
    · simp [hprev,hfront,hrt] at heq
    · rfl
    · simp [hnext,htrail,hrt] at heq
    · simp [hnext,hback,Ne.symm ht0] at heq
  have unique2 : UniqueAt (graph n) (.u (j+1)) (.u j) c1 := by
    intro w edge heq
    have hmid1 : c1 (.u j) = 1 := by simp [c1,hmid]
    rw [hmid1] at heq
    rcases (neighbors_u (j+1) w).mp edge with rfl | rfl | rfl | rfl | rfl
    · simp [c1,ha] at heq
    · simp [c1,hnext,htrail,hr1] at heq
    · simp [c1,houter,ht1] at heq
    · simp [c1,hprev,hfront,hr1] at heq
    · rw [hprev]
  have path : SlidePath (.v (j+1),c) (.u j,c2) 2 := by
    exact .cons ((u_v (j+1)).symm) unique1
      (.cons ((u_next j).symm) unique2 (.nil _))
  refine ⟨(.u j,c2),path,path.proper hc,tau,?_⟩
  intro w edge
  rcases (neighbors_u j w).mp edge with rfl | rfl | rfl | rfl | rfl
  · simp [c2,c1,slide,ha,Ne.symm ht0]
  · simp [c2,c1,slide,hmid,Ne.symm ht1]
  · simp [c2,c1,slide,hfront,hrt]
  · simp [c2,c1,slide,hzero,hminus,Ne.symm ht0]
  · simp [c2,c1,slide,hinner,hminus,hrt]

/-- The other A-rho branch makes four actual slides and returns a prepared zero. -/
theorem a_rho_four_slide_return (hn : 5 ≤ n) (j : ZMod n)
    (c : Vertex n → Fin 4) (rho tau : Fin 4) (hp : NonpolePair rho tau)
    (hc : ProperOff (graph n) (.v (j+1)) c)
    (ha : c .a = 0) (hb : c .b = 1)
    (houter : c (.u (j+1)) = tau) (hmid : c (.u j) = 1)
    (hinner : c (.u (j-1)) = tau) (htrail : c (.u (j+2)) = rho)
    (hfront : c (.v j) = rho) (hzero : c (.v (j-1)) = 0)
    (hback : c (.v (j+2)) = 0) (hfar : c (.v (j-2)) = rho) :
    ∃ d, SlidePath (.v (j+1),c) (.v (j-1),d) 4 ∧
      ProperOff (graph n) (.v (j-1)) d ∧
      d .a = 0 ∧ d .b = 1 ∧ d (.v (j-2)) = rho ∧
      d (.u (j-1)) = tau ∧ d (.u j) = rho ∧ d (.v j) = 0 := by
  let : Fact (1 < n) := ⟨by omega⟩
  obtain ⟨hr0,hr1,ht0,ht1,hrt⟩ := hp
  have hplus : j+1 ≠ j := plus_one_ne j
  have hminus : j-1 ≠ j+1 := by
    intro heq
    apply offset_ne (j-1) 2 (by omega) (by omega)
    linear_combination -heq
  have htwo : j+2 ≠ j+1 := by
    have h := plus_one_ne (j+1)
    convert h using 1; ring
  have hnext : (j+1)+1 = j+2 := by ring
  have hprev : (j+1)-1 = j := by ring
  let c1 := slide (.v (j+1)) (.u (j+1)) c
  let c2 := slide (.u (j+1)) (.u j) c1
  have unique1 : UniqueAt (graph n) (.v (j+1)) (.u (j+1)) c := by
    intro w edge heq
    rw [houter] at heq
    rcases (neighbors_v (j+1) w).mp edge with rfl | rfl | rfl | rfl | rfl
    · simp [hb,Ne.symm ht1] at heq
    · simp [hprev,hfront,hrt] at heq
    · rfl
    · simp [hnext,htrail,hrt] at heq
    · simp [hnext,hback,Ne.symm ht0] at heq
  have unique2 : UniqueAt (graph n) (.u (j+1)) (.u j) c1 := by
    intro w edge heq
    have hmid1 : c1 (.u j) = 1 := by simp [c1,hmid]
    rw [hmid1] at heq
    rcases (neighbors_u (j+1) w).mp edge with rfl | rfl | rfl | rfl | rfl
    · simp [c1,ha] at heq
    · simp [c1,hnext,htrail,hr1] at heq
    · simp [c1,houter,ht1] at heq
    · simp [c1,hprev,hfront,hr1] at heq
    · rw [hprev]
  let c3 := slide (.u j) (.v j) c2
  let c4 := slide (.v j) (.v (j-1)) c3
  have unique3 : UniqueAt (graph n) (.u j) (.v j) c2 := by
    intro w edge heq
    have hv : c2 (.v j) = rho := by simp [c2,c1,slide,hfront]
    rw [hv] at heq
    rcases (neighbors_u j w).mp edge with rfl | rfl | rfl | rfl | rfl
    · simp [c2,c1,slide,ha,Ne.symm hr0] at heq
    · simp [c2,c1,slide,hmid,Ne.symm hr1] at heq
    · rfl
    · simp [c2,c1,slide,hzero,hminus,Ne.symm hr0] at heq
    · simp [c2,c1,slide,hinner,hminus,Ne.symm hrt] at heq
  have unique4 : UniqueAt (graph n) (.v j) (.v (j-1)) c3 := by
    intro w edge heq
    have hz : c3 (.v (j-1)) = 0 := by
      simp [c3,c2,c1,slide,hzero,hminus]
    rw [hz] at heq
    rcases (neighbors_v j w).mp edge with rfl | rfl | rfl | rfl | rfl
    · simp [c3,c2,c1,slide,hb] at heq
    · rfl
    · simp [c3,c2,c1,slide,hfront,hr0] at heq
    · simp [c3,c2,c1,slide,hmid,hplus] at heq
    · simp [c3,c2,c1,slide,houter,ht0] at heq
  have edge4 : (graph n).Adj (.v j) (.v (j-1)) := by
    have h := (v_next (j-1)).symm
    have heq : j-1+1 = j := by ring
    rw [heq] at h
    exact h
  have path : SlidePath (.v (j+1),c) (.v (j-1),c4) 4 := by
    exact .cons ((u_v (j+1)).symm) unique1
      (.cons ((u_next j).symm) unique2
      (.cons (u_v j) unique3
      (.cons edge4 unique4 (.nil _))))
  have hfarne : j-2 ≠ j+1 := by
    intro heq
    apply offset_ne (j-2) 3 (by omega) (by omega)
    linear_combination -heq
  have hfarne' : j-2 ≠ j := by
    intro heq
    apply offset_ne (j-2) 2 (by omega) (by omega)
    linear_combination -heq
  refine ⟨c4,path,path.proper hc,?_,?_,?_,?_,?_,?_⟩
  · simp [c4,c3,c2,c1,slide,ha]
  · simp [c4,c3,c2,c1,slide,hb]
  · simp [c4,c3,c2,c1,slide,hfar,hfarne,hfarne']
  · simp [c4,c3,c2,c1,slide,hinner,hminus,minus_one_ne j]
  · simp [c4,c3,c2,c1,slide,hfront]
  · simp [c4,c3,c2,c1,slide,hzero,hminus]

end SimpleGraph.TwoPoleBeltTeamB
