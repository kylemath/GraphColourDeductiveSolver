module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyProtectedLift

/-!
# A short filling bridge through an easy neighbouring vacancy

All moves below are the actual component swaps and singleton slides of
`VacancyShortFill`. Geometry is an explicit premise: this file does not assert
the planar degree-four extension or degree-five mobility theorem.
-/

@[expose] public section
namespace SimpleGraph.VacancyEasyNeighbour
open VacancySlide VacancyShortFill VacancyCliqueLift

variable {V C : Type*} (G : SimpleGraph V)

/-- A fill already present, or one actual whole-component swap yielding a fill. -/
def OneSwapAt [DecidableEq C] (h : V) (c : V → C) : Prop :=
  Target G h c ∨ ∃ d, KempeStep G h c d ∧ Target G h d

/-- The chosen neighbouring hole can always be filled by at most one actual swap.
For degree four in a spherical triangulation this is a separate geometric theorem. -/
def EasyAt [DecidableEq C] (u : V) : Prop :=
  ∀ c : V → C, ProperOff G u c → OneSwapAt G u c

/-- An actual optional Kempe prefix makes the chosen neighbour singleton. -/
def SlideAccess [DecidableEq C] (h u : V) (c : V → C) : Prop :=
  UniqueAt G h u c ∨ ∃ d, KempeStep G h c d ∧ UniqueAt G h u d

theorem one_swap_pure [DecidableEq C] {h : V} {c : V → C}
    (fill : OneSwapAt G h c) : PureFill G h c 1 := by
  rcases fill with target | ⟨d,step,target⟩
  · exact ⟨0,by decide,c,.nil c,target⟩
  · exact ⟨1,le_rfl,d,.cons step (.nil d),target⟩

/-- A singleton apex leading to an easy hole has a two-swap replacement at the
original hole, even when the auxiliary slide would enter a protected set. -/
theorem singleton_easy [DecidableEq V] [DecidableEq C] {h u : V} {c : V → C}
    (proper : ProperOff G h c) (adj : G.Adj h u) (unique : UniqueAt G h u c)
    (easy : EasyAt (C := C) G u) : PureFill G h c 2 := by
  have nextProper := properOff_slide G proper unique
  rcases easy (slide h u c) nextProper with target | ⟨d,step,target⟩
  · have path : MixedPath G 1 (h,c) (u,slide h u c) :=
      .cons (.slide adj unique) (.nil _)
    exact pureFill_mono G (short_fill G proper (by decide) path target) (by decide)
  · have path : MixedPath G 2 (h,c) (u,d) :=
      .cons (.slide adj unique) (.cons (.kempe step) (.nil _))
    exact short_fill G proper (by decide) path target

/-- Prefixing an actual Kempe move increases a pure bound by at most one. -/
theorem prepend_kempe [DecidableEq C] {h : V} {c d : V → C} {bound : Nat}
    (step : KempeStep G h c d) (fill : PureFill G h d bound) :
    PureFill G h c (bound+1) := by
  obtain ⟨n,hn,e,path,target⟩ := fill
  exact ⟨n+1,Nat.add_le_add_right hn 1,e,.cons step path,target⟩

/-- Optional actual Kempe preparation followed by a singleton slide to an easy
neighbour gives three pure swaps at the original hole. -/
theorem mobility_easy [DecidableEq V] [DecidableEq C] {h u : V} {c : V → C}
    (proper : ProperOff G h c) (adj : G.Adj h u)
    (access : SlideAccess G h u c) (easy : EasyAt (C := C) G u) : PureFill G h c 3 := by
  rcases access with unique | ⟨d,step,unique⟩
  · exact pureFill_mono G (singleton_easy G proper adj unique easy) (by decide)
  · exact prepend_kempe G step
      (singleton_easy G (kempe_proper G proper step) adj unique easy)

/-- The exact logical form used by a geometric mobility alternative. -/
theorem mobility_alternative_easy [DecidableEq V] [DecidableEq C]
    {h u : V} {c : V → C} (proper : ProperOff G h c) (adj : G.Adj h u)
    (alternative : OneSwapAt G h c ∨ SlideAccess G h u c)
    (easy : EasyAt (C := C) G u) : PureFill G h c 3 := by
  rcases alternative with fill | access
  · exact pureFill_mono G (one_swap_pure G fill) (by decide)
  · exact mobility_easy G proper adj access easy

/-- A pure path has its original hole at every step, so it avoids any set not
containing that hole. No condition is imposed on colours of protected vertices. -/
theorem pure_path_protected [DecidableEq V] [DecidableEq C]
    {Z : Set V} {h : V} {c d : V → C} {n : Nat}
    (path : PurePath G h n c d) (outside : h ∉ Z) :
    ProtectedPath G Set.univ Z n (h,c) (h,d) := by
  induction path with
  | nil c => exact .nil (Set.mem_univ _) outside
  | cons step rest ih => exact .cons (.kempe step) (Set.mem_univ _) outside ih

/-- Explicit actual path, all-hole protection, proper endpoint and a missing
colour accompany any pure-fill bound. -/
theorem pure_fill_protected [DecidableEq V] [DecidableEq C]
    {Z : Set V} {h : V} {c : V → C} {bound : Nat}
    (proper : ProperOff G h c) (outside : h ∉ Z) (fill : PureFill G h c bound) :
    ∃ n, n ≤ bound ∧ ∃ d, PurePath G h n c d ∧
      ProtectedPath G Set.univ Z n (h,c) (h,d) ∧ ProperOff G h d ∧ Target G h d := by
  obtain ⟨n,hn,d,path,target⟩ := fill
  exact ⟨n,hn,d,path,pure_path_protected G path outside,path.proper G proper,target⟩

/-- The easy neighbouring hole may itself be protected: only the original hole
must lie outside the protected set in the constructed pure replacement. -/
theorem mobility_easy_protected [DecidableEq V] [DecidableEq C]
    {Z : Set V} {h u : V} {c : V → C}
    (proper : ProperOff G h c) (outside : h ∉ Z) (adj : G.Adj h u)
    (alternative : OneSwapAt G h c ∨ SlideAccess G h u c) (easy : EasyAt (C := C) G u) :
    ∃ n, n ≤ 3 ∧ ∃ d, PurePath G h n c d ∧
      ProtectedPath G Set.univ Z n (h,c) (h,d) ∧ ProperOff G h d ∧ Target G h d :=
  pure_fill_protected G proper outside
    (mobility_alternative_easy G proper adj alternative easy)

/-- Pigeonhole fill: three or fewer neighbours cannot display all four colours.
This theorem needs no properness or geometry. -/
theorem target_of_degree_le_three [Fintype V] [DecidableEq V] [DecidableRel G.Adj]
    (u : V) (degree : G.degree u ≤ 3) (c : V → Fin 4) : Target G u c := by
  classical
  have imageCard : ((G.neighborFinset u).image c).card ≤ 3 :=
    (show ((G.neighborFinset u).image c).card ≤ G.degree u from
      Finset.card_image_le).trans degree
  have fewer : ((G.neighborFinset u).image c).card <
      (Finset.univ : Finset (Fin 4)).card := by simpa using (show _ < 4 by omega)
  obtain ⟨a,_,missing⟩ := Finset.exists_mem_notMem_of_card_lt_card fewer
  refine ⟨a,?_⟩
  intro v adj eq
  exact missing (Finset.mem_image.mpr
    ⟨v,(by simpa [mem_neighborFinset] using adj),eq⟩)

theorem easy_of_degree_le_three [Fintype V] [DecidableEq V] [DecidableRel G.Adj]
    (u : V) (degree : G.degree u ≤ 3) : EasyAt (C := Fin 4) G u := by
  intro c _
  exact Or.inl (target_of_degree_le_three G u degree c)

/-- With at most three neighbours, the slide is terminal and one pure swap
suffices at the original hole. -/
theorem singleton_small [Fintype V] [DecidableEq V] [DecidableRel G.Adj]
    {h u : V} {c : V → Fin 4} (proper : ProperOff G h c) (adj : G.Adj h u)
    (unique : UniqueAt G h u c) (degree : G.degree u ≤ 3) : PureFill G h c 1 :=
  pureFill_one G (terminal_slide G proper adj unique
    (target_of_degree_le_three G u degree (slide h u c)))

/-- Optional Kempe preparation plus a terminal small-neighbour slide needs
at most two pure swaps. -/
theorem mobility_small [Fintype V] [DecidableEq V] [DecidableRel G.Adj]
    {h u : V} {c : V → Fin 4} (proper : ProperOff G h c) (adj : G.Adj h u)
    (access : SlideAccess G h u c) (degree : G.degree u ≤ 3) : PureFill G h c 2 := by
  rcases access with unique | ⟨d,step,unique⟩
  · exact pureFill_mono G (singleton_small G proper adj unique degree) (by decide)
  · exact prepend_kempe G step
      (singleton_small G (kempe_proper G proper step) adj unique degree)

end SimpleGraph.VacancyEasyNeighbour
