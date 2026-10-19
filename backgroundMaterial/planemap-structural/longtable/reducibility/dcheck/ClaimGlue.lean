import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame
import SepAll
import DCheckOccWalk

/-!
# Claim glue: reducibility + unavoidability ⇒ four-colourable (Long Table, 19 Oct 2026)

The step the 24 Oct gate text lists as "not formalized": turning the compiled reducibility
results into a colourability theorem, so that once the discharging LP reaches `t* ≤ 0` the claim
is complete up to the hypotheses named below.

**What is proved here, from existing results only (no `sorry`, no new `axiom`).**
* `MinimalCounterexample.noSep`, `MinimalCounterexample.noShortSep`: a minimal counterexample
  that is a triangulation has no separating triangle (F1, `colorable_of_separating_triangle`) and
  no separating 3-, 4- or non-trivial 5-cycle (B2, `colorable_of_short_separating_cycle`, Job 25).
* `DEntry.colorable`: an occurrence of a D-reducible registry entry reduces
  (`ConfigOccW.colorable_of_dReducible18`, checker soundness Jobs 19/23 plus the face-walk ring
  of Job 26, rings `≤ 19`).
* `MinimalCounterexample.avoids`: a minimal counterexample contains no configuration of the
  registry `R` (D entries unconditionally; C entries given `CGlue`).
* `four_color_of_unavoidable`: `Unavoidable R → CGlue R.C → ∀ M : SphericalMap n,
  M.graph.Colorable 4`, and `four_color_of_unavoidable_planeMap` for the library's plane maps.
* `four_color_of_unavoidable_D`: the same with a D-only registry, with no `CGlue` hypothesis.

**Hypotheses (the only open links).**
* `Unavoidable R`: every internally 6-connected triangulation (`Internally6`: connected,
  triangulated, minimum degree 5, no separating triangle, no separating 3/4-cycle, no separating
  5-cycle except around one vertex) contains an occurrence of some entry of `R`. This is what the
  discharging LP (`t* ≤ 0`) supplies, together with the appearance → occurrence bridge (Job 26
  step (iii)); `unavoidable_of_appears` records that split.
* `CGlue R.C`: soundness of C-reducibility (an occurrence of a C entry in a triangulation whose
  smaller maps are colourable makes it colourable). The C computations are in Lean
  (`C66666.lean`, `CWheels.lean`, `native_decide`), but the C-reduction glue (contracting the
  reducer and pulling the colouring back to the ring) is not formalized. A registry with no C
  entries needs no `CGlue` (`cGlue_nil`).

An occurrence (`OccursW`) is the reduction-ready one: a deleted map `G` of strictly smaller
support whose face walk is the ring (`ConfigOccW`, folds and pinches allowed). Orientation needs
no separate case: `T.mirror` has the same graph, and the orientation lives in `G`'s rotation. The
per-key rotation occurrences `K<ii>.Occ` (occ24) give `OccursW` through their `configOcc` and
`occursW_of_configOcc`.
-/

namespace SimpleGraph.SphericalMap.ClaimGlue
open VacancySlide VacancyShortFill VacancyIcosahedral VacancyCliqueLift SimpleGraph.SphericalMap
  DCheck DCheck.R2

variable {n : ℕ}

/-! ## Minimal counterexample -/

/-- Every spherical map of smaller support is four-colourable. -/
def SmallerColorable (T : SphericalMap n) : Prop :=
  ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
    N.graph.Colorable 4

/-- A minimal counterexample: not four-colourable, while every map of smaller support is. -/
structure MinimalCounterexample (T : SphericalMap n) : Prop where
  not_colorable : ¬ T.graph.Colorable 4
  smaller : SmallerColorable T

/-- No separating cycle of length `≤ 5` in the B2 sense: a cycle of length `3..5` with a
non-isolated vertex off it on each side (two on each side for length 5). -/
def NoShortSepCycle (T : SphericalMap n) : Prop :=
  ∀ (r : ℕ) (ρ : ℕ → Fin n) (c : T.Face → ZMod 2), Cyc T r ρ → r ≤ 5 → CycPotential T r ρ c →
    BothSides T r ρ c → (r = 5 → BothSides2 T r ρ c) → False

/-- The class the discharging argument works in: internally 6-connected triangulations of
minimum degree five. -/
structure Internally6 (T : SphericalMap n) : Prop where
  pos : 0 < n
  connected : T.graph.Connected
  triangulated : T.Triangulated
  minDeg : ∀ x, 5 ≤ T.graph.degree x
  noSep : NoSep T
  noShortSep : NoShortSepCycle T

/-- **F1 for a minimal counterexample.** No separating triangle. -/
theorem MinimalCounterexample.noSep {T : SphericalMap n} (hT : MinimalCounterexample T)
    (htri : T.Triangulated) : NoSep T := by
  by_contra hns
  simp only [NoSep, not_forall] at hns
  obtain ⟨x, y, z, hxy, hyz, hzx, hnf⟩ := hns
  exact hT.not_colorable (colorable_of_separating_triangle htri hxy hyz hzx hnf hT.smaller)

/-- **B2 for a minimal counterexample.** No separating 3- or 4-cycle, and no separating 5-cycle
other than one around a single vertex (Birkhoff; Job 25). -/
theorem MinimalCounterexample.noShortSep {T : SphericalMap n} (hT : MinimalCounterexample T) :
    NoShortSepCycle T := by
  intro r ρ c C hr hc hs h5
  exact hT.not_colorable (colorable_of_short_separating_cycle C hr hc hs h5 hT.smaller)

/-! ## Registry entries and their soundness -/

/-- Reduction-ready occurrence of a `DCheck.Conf` in `T`: deleting the interior `ι` gives a map
`G` of strictly smaller support whose face walk `ρ` is the configuration's ring. -/
def OccursC (cf : DCheck.Conf) (T : SphericalMap n) : Prop :=
  ∃ (G : SphericalMap n) (ρ : ℕ → Fin n) (ι : Fin cf.m → Fin n),
    ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf) ∧ supportSize G < supportSize T

/-- The same for a `DCheck18.Conf` (the checker used for rings up to 19). -/
def OccursW (cf : DCheck18.Conf) (T : SphericalMap n) : Prop :=
  ∃ (G : SphericalMap n) (ρ : ℕ → Fin n) (ι : Fin cf.m → Fin n),
    ConfigOccW T G cf.r cf.m ρ ι (intAdjOf (Conf.of18 cf)) (ringAdjOf (Conf.of18 cf)) ∧
      supportSize G < supportSize T

/-- A simple-ring occurrence (`ConfigOcc`, as produced by the per-key `configOcc`) is a
reduction-ready one. -/
theorem occursW_of_configOcc (cf : DCheck18.Conf) {T G : SphericalMap n} {ρ : ℕ → Fin n}
    {ι : Fin cf.m → Fin n}
    (O : ConfigOcc T G cf.r cf.m ρ ι (intAdjOf (Conf.of18 cf)) (ringAdjOf (Conf.of18 cf)))
    (hlt : supportSize G < supportSize T) : OccursW cf T :=
  ⟨G, ρ, ι, O.toW, hlt⟩

/-- A D-reducible registry entry: the configuration with its checker verdict and the side
facts the soundness theorem needs (each closed by `decide`/`native_decide` per key). -/
structure DEntry where
  cf : DCheck18.Conf
  hD : DCheck18.dReducible cf = true
  hr2 : 2 ≤ cf.r
  hr : cf.r ≤ 19
  hsym : ∀ a b, intAdjOf (Conf.of18 cf) a b = true → intAdjOf (Conf.of18 cf) b a = true
  hloop : ∀ a, intAdjOf (Conf.of18 cf) a a = false

/-- **D-soundness, per entry.** An occurrence of a D entry in a map whose smaller maps are all
colourable makes it colourable. -/
theorem DEntry.colorable (e : DEntry) {T : SphericalMap n} (h : OccursW e.cf T)
    (IH : SmallerColorable T) : T.graph.Colorable 4 := by
  obtain ⟨G, ρ, ι, O, hlt⟩ := h
  obtain ⟨cG⟩ := IH n G (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
  exact ConfigOccW.colorable_of_dReducible18 (T := T) (G := G) e.cf e.hD e.hr2 e.hr e.hsym
    e.hloop O (c := fun x => cG x) (fun _ _ huv _ _ => cG.valid huv)

/-- A C-reducible registry entry. Only the configuration is recorded here; its C certificate is
a `native_decide` fact in `C66666.lean`/`CWheels.lean` style, which `CGlue` would consume. -/
structure CEntry where
  cf : DCheck.Conf

/-- **Open link: C-glue.** Soundness of C-reducibility for the listed entries. Not formalized. -/
def CGlue (Cs : List CEntry) : Prop :=
  ∀ e ∈ Cs, ∀ (n : ℕ) (T : SphericalMap n), T.Triangulated → OccursC e.cf T →
    SmallerColorable T → T.graph.Colorable 4

/-- With no C entries there is nothing to assume. -/
theorem cGlue_nil : CGlue [] := by
  intro e he
  simp at he

/-- The registry `R`: D-reducible and C-reducible configurations. -/
structure Registry where
  D : List DEntry
  C : List CEntry

/-- `T` contains an occurrence of some configuration of `R`. -/
def Registry.Contains (R : Registry) (T : SphericalMap n) : Prop :=
  (∃ e ∈ R.D, OccursW e.cf T) ∨ (∃ e ∈ R.C, OccursC e.cf T)

/-- **Unavoidability of `R`** (to be supplied by the discharging LP at `t* ≤ 0`): every
internally 6-connected triangulation contains a configuration of `R`. -/
def Unavoidable (R : Registry) : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), Internally6 T → R.Contains T

/-- How `Unavoidable` splits: the LP gives "some key of `R` appears" (`Appears`, the census
notion), and the appearance → occurrence bridge (Job 26 step (iii)) gives the occurrence. -/
theorem unavoidable_of_appears (R : Registry) (Appears : ∀ {m : ℕ}, SphericalMap m → Prop)
    (hLP : ∀ (m : ℕ) (T : SphericalMap m), Internally6 T → Appears T)
    (hBridge : ∀ (m : ℕ) (T : SphericalMap m), Internally6 T → Appears T → R.Contains T) :
    Unavoidable R := by
  intro m T hT
  exact hBridge m T hT (hLP m T hT)

/-! ## The claim -/

/-- **A minimal counterexample contains no configuration of `R`.** D entries by the compiled
D-soundness; C entries by `CGlue`. -/
theorem MinimalCounterexample.avoids (R : Registry) (hC : CGlue R.C) {T : SphericalMap n}
    (hT : MinimalCounterexample T) (htri : T.Triangulated) : ¬ R.Contains T := by
  rintro (⟨e, -, h⟩ | ⟨e, he, h⟩)
  · exact hT.not_colorable (e.colorable h hT.smaller)
  · exact hT.not_colorable (hC e he n T htri h hT.smaller)

/-- A minimal counterexample that is a connected triangulation of minimum degree five is
internally 6-connected. -/
theorem MinimalCounterexample.internally6 {T : SphericalMap n} (hT : MinimalCounterexample T)
    (hn : 0 < n) (hconn : T.graph.Connected) (htri : T.Triangulated)
    (hdeg : ∀ x, 5 ≤ T.graph.degree x) : Internally6 T :=
  ⟨hn, hconn, htri, hdeg, hT.noSep htri, hT.noShortSep⟩

/-- **Claim glue.** If `R` is unavoidable and its C entries are sound, every spherical map is
four-colourable. -/
theorem four_color_of_unavoidable (R : Registry) (hU : Unavoidable R) (hC : CGlue R.C)
    {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4 := by
  refine four_color_of_smaller_gate (fun m T hm hconn htri hdeg IH => ?_) M
  by_contra hcol
  have hT : MinimalCounterexample T := ⟨hcol, IH⟩
  exact hT.avoids R hC htri (hU m T (hT.internally6 hm hconn htri hdeg))

/-- **Claim glue, D-only registry**: no C-glue hypothesis. -/
theorem four_color_of_unavoidable_D (Ds : List DEntry) (hU : Unavoidable ⟨Ds, []⟩)
    {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4 :=
  four_color_of_unavoidable ⟨Ds, []⟩ hU cGlue_nil M

/-- The same for the library's plane maps. -/
theorem four_color_of_unavoidable_planeMap (R : Registry) (hU : Unavoidable R)
    (hC : CGlue R.C) {n : ℕ} (M : PlaneMap n) : M.graph.Colorable 4 :=
  four_color_of_unavoidable R hU hC (SphericalMap.ofPlaneMap M)

end SimpleGraph.SphericalMap.ClaimGlue

#print axioms SimpleGraph.SphericalMap.ClaimGlue.four_color_of_unavoidable
#print axioms SimpleGraph.SphericalMap.ClaimGlue.four_color_of_unavoidable_D
#print axioms SimpleGraph.SphericalMap.ClaimGlue.MinimalCounterexample.avoids
