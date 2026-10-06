module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyIcosahedral
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalFourContact

/-!
# From pure-clean degree-five vertices to four colours

`PureClean T r`: every proper four-colouring of `T - r` reaches a filled hole at `r` by finitely
many whole-component Kempe swaps of `T - r` (the hand notion "every Kempe class at `r` contains a
fill", KD(r), equivalently "every doubly locked state at `r` has finite Kempe radius").

* `extend_of_pureClean`: a pure-clean vertex gives the extension `T - r` colourable →
  `T` colourable.
* `four_color_of_global_Rstar`: if **every** connected spherical triangulation of minimum degree
  five has a pure-clean degree-five vertex, every spherical map is four-colourable. This assumes
  the clean-vertex property for all such triangulations, not only for the four-connected
  relative-class core of Lemma R*; the core version needs the separating-triangle reduction.
* `pureClean_iff_locked`: the hypothesis may be checked only on colourings that do not fill
  within one swap.
* `pureClean_of_theorem_H`, `pureClean_of_theorem_HP`: Theorems H and HP give pure-clean vertices
  at holes of their classes. Not every triangulation has such a hole (the pentakis dodecahedron
  has only `(6^5)` holes), so these do not by themselves give a four-colour theorem.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral
variable {n : ℕ}

/-- Every proper colouring of `T - r` reaches a filled hole at `r` by pure Kempe swaps. -/
def PureClean (T : SphericalMap n) (r : Fin n) : Prop :=
  ∀ c : Fin n → Fin 4, ProperOff T.graph r c → ∃ m, PureFill T.graph r c m

/-- Pure Kempe paths preserve properness off the hole. -/
theorem properOff_of_purePath {G : SimpleGraph (Fin n)} {r : Fin n} {m : ℕ}
    {c d : Fin n → Fin 4} (p : PurePath G r m c d) (hc : ProperOff G r c) :
    ProperOff G r d := by
  induction p with
  | nil => exact hc
  | cons k _ ih =>
    obtain ⟨a, b, S, _, hS, rfl⟩ := k
    exact ih (properOff_swap G hc hS)

/-- A filled proper colouring of `G - r` extends to a colouring of `G`. -/
theorem colorable_of_target {G : SimpleGraph (Fin n)} {r : Fin n} {d : Fin n → Fin 4}
    (hd : ProperOff G r d) (ht : Target G r d) : G.Colorable 4 := by
  classical
  obtain ⟨x, hx⟩ := ht
  refine ⟨SimpleGraph.Coloring.mk (fun v => if v = r then x else d v) ?_⟩
  intro u v huv
  by_cases hu : u = r <;> by_cases hv : v = r
  · subst hu; subst hv; exact (huv.ne rfl).elim
  · subst hu; simp only [hv, ↓reduceIte]; exact fun e => hx huv e.symm
  · subst hv; simp only [hu, ↓reduceIte]; exact fun e => hx huv.symm e
  · simp only [hu, hv, ↓reduceIte]; exact hd huv hu hv

/-- **Link A.** A pure-clean vertex gives the degree-five extension. -/
theorem extend_of_pureClean (T : SphericalMap n) (r : Fin n) (hpc : PureClean T r) :
    (T.graph.induce {z | z ≠ r}).Colorable 4 → T.graph.Colorable 4 := by
  classical
  rintro ⟨c'⟩
  let c : Fin n → Fin 4 := fun v => if h : v ≠ r then c' ⟨v, h⟩ else 0
  have hc : ProperOff T.graph r c := by
    intro u v huv hu hv
    simp only [c, ne_eq, hu, hv, not_false_eq_true, ↓reduceDIte]
    exact c'.valid (by simpa using huv)
  obtain ⟨m, k, _, d, path, target⟩ := hpc c hc
  exact colorable_of_target (properOff_of_purePath path hc) target

/-- **Four colours from a global clean-vertex hypothesis.** If every connected spherical
triangulation of minimum degree five has a pure-clean vertex of degree five, every spherical
map is four-colourable. The hypothesis is stated for all such triangulations; see the module
docstring. -/
theorem four_color_of_global_Rstar
    (hR : ∀ (n : ℕ) (T : SphericalMap n), 0 < n → T.graph.Connected → T.Triangulated →
      (∀ x, 5 ≤ T.graph.degree x) → ∃ r, T.graph.degree r = 5 ∧ PureClean T r)
    (M : SphericalMap n) : M.graph.Colorable 4 :=
  four_color_of_triangulated_five_extension
    (fun n T hn hc ht hd => by
      obtain ⟨r, hr, hp⟩ := hR n T hn hc ht hd
      exact ⟨r, hr, extend_of_pureClean T r hp⟩) M

/-- **Link B.** It suffices to treat the colourings that do not fill within one swap (the
doubly locked states, in the hand terminology). -/
theorem pureClean_iff_locked (T : SphericalMap n) (r : Fin n) :
    PureClean T r ↔ ∀ c : Fin n → Fin 4, ProperOff T.graph r c →
      ¬ PureFill T.graph r c 1 → ∃ m, PureFill T.graph r c m := by
  constructor
  · exact fun h c hc _ => h c hc
  · intro h c hc
    by_cases h1 : PureFill T.graph r c 1
    · exact ⟨1, h1⟩
    · exact h c hc h1

/-- **Link C (Theorem H).** -/
theorem pureClean_of_theorem_H (T : SphericalMap n) (htri : T.Triangulated) {h : Fin n}
    (hdeg : T.graph.degree h = 5) (hlink : ∀ u, T.Adj h u → T.graph.degree u = 5)
    (hsep : T.NoSeparatingTriangleAt h) : PureClean T h :=
  fun _ hc => ⟨3, T.theorem_H htri hdeg hlink hsep hc⟩

/-- **Link C (Theorem HP).** -/
theorem pureClean_of_theorem_HP (T : SphericalMap n) (htri : T.Triangulated) {h p : Fin n}
    (hdeg : T.graph.degree h = 5) (hp : T.Adj h p)
    (hlink : ∀ u, T.Adj h u → u ≠ p → T.graph.degree u = 5)
    (hsep : T.NoSeparatingTriangleAt h) : PureClean T h :=
  fun _ hc => ⟨6, T.theorem_HP htri hdeg hp hlink hsep hc⟩

end SimpleGraph.SphericalMap

#print SimpleGraph.SphericalMap.PureClean
#check @SimpleGraph.SphericalMap.four_color_of_global_Rstar
#check @SimpleGraph.SphericalMap.pureClean_of_theorem_H
#check @SimpleGraph.SphericalMap.pureClean_of_theorem_HP
#print axioms SimpleGraph.SphericalMap.four_color_of_global_Rstar
#print axioms SimpleGraph.SphericalMap.pureClean_of_theorem_H
#print axioms SimpleGraph.SphericalMap.pureClean_of_theorem_HP

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if (env.getModuleIdxFor? c).isNone && !c.isInternal then
      n := n + 1
      for a in (← liftCoreM (Lean.collectAxioms c)) do
        if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)
  logInfo m!"file constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"
