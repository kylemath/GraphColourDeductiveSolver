import DCheck
/-!
# DCheckSound: what `dReducible C = true` must imply, and the combinatorial core (exploratory)

The checker `DCheck.run` is imperative (loops, progress pointers). Its soundness splits into
three parts. This file proves part (S2) and states (S1) and (S3) with `sorry`.

* **(S1) loop correctness [sorry]:** `dReducible cf = true` implies every canonical proper ring
  colouring satisfies the declarative closure predicate `Good cf` below (the least set containing
  the extendable codes and closed under the consistent-matching rule). This is a loop invariant
  for `run`: (a) `good[i] = true → Good cf ks[i]`; (b) progress pointer `prog[3i+θ-1] = p` means
  every matching with index `< p` has a flip into the current good set, hence (monotonicity) into
  `Good cf`; (c) `ringColourings r` lists exactly the canonical proper codes and the `HashMap`
  `index` is a bijection onto them.
* **(S2) the combinatorial core [PROVED below, `good_sound`]:** for any family `P` of ring codes
  ("codes realised by a proper colouring of the outside map `G`") that is closed under renaming and
  satisfies the Kempe-matching property `KempeMatching`, every `Good` code realised by `P` leads to
  a realised code that extends into the interior.
* **(S3) the geometric lemma [sorry, project-level]:** in the project's terms
  (`SimpleGraph.SphericalMap`, `RingReduce.ConfigOcc`, `ProperOff`, `pairGraph`), the set
  `P := {ring code of c | c proper on G off the hole}` satisfies `KempeMatching`. Content: for a
  colouring `c` and a pairing `θ`, the θ-classes `{x, x⊕θ}` give Kempe chains of `G`; their
  traces on the ring are the faces of a non-crossing perfect matching of the transitions
  (non-crossing is `RingChains.chains_noncrossing`/`chains_noncrossing_same`, from
  `RingJordan.face_alternating_walks_meet`); swapping any set of chains (whole components of
  `pairGraph G.graph hole c a (a⊕θ)`) is again proper (`RingReduce.flip_in/flip_out/flip_other`
  are the per-vertex facts). What is NOT in the repo yet: (i) "every pair of ring arcs in one face
  of the matching is in ONE chain" — the converse of non-crossing, i.e. the existence of the
  matching (chains_noncrossing gives only that chains do not cross; one must still build the
  matching from the chain partition: pair each transition with the next transition along the
  boundary of its chain, a purely combinatorial non-crossing-partition lemma); (ii) swapping a
  set of components simultaneously (only single swaps are used by the generated certificates).
* **(S4) glue [exists]:** `RingReduce.ConfigOcc.colorable_of_ext` turns an extendable realised
  ring code into `T.graph.Colorable 4`.

The final target, in project terms (not compiled here: the project build is not on this machine;
it would live in a module importing `RingReduce` and this file):

```
theorem ConfigOcc.colorable_of_dReducible (cf : DCheck.Conf) (hD : DCheck.dReducible cf = true)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true)
    (O : ConfigOcc T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4
```
with `intAdjOf cf a b := decide (b.val ∈ cf.intAdj[a]!)`, `ringAdjOf cf a t := decide (t ∈ cf.ringAdj[a]!)`.
"Reducible" (no minimal counterexample contains `cf`) then follows exactly as for the diamond:
the caller supplies `hc` from minimality of `T` (the map `G` is smaller).
-/
namespace DCheck

/-- θ-transitions of the ring code `k`: ring edges `(v, v+1)` whose ends lie in different
θ-classes. -/
def transitions (r k th : Nat) : Array Nat :=
  (Array.range r).filter fun v =>
    let x := col k v ^^^ col k ((v + 1) % r)
    x != 0 && x != th

/-- Arc of ring vertex `v` (arc `j` runs from transition `j` (exclusive) to `j+1`). -/
def arcOf (T : Array Nat) (v : Nat) : Nat := ((T.filter (· < v)).size + T.size - 1) % T.size

/-- XOR mask flipping (by `θ`) the regions `b+1` for the bits `b` of `s`, for the region labelling
`lab` of the arcs. -/
def flipMask (r k th : Nat) (lab : Array Nat) (s : Nat) : Nat :=
  let T := transitions r k th
  (List.range r).foldl (fun acc v =>
    let g := lab[arcOf T v]!
    if g != 0 && (s >>> (g - 1)) % 2 == 1 then acc ||| (th <<< (2 * v)) else acc) 0

/-- The declarative D-closure (least fixpoint). The witness `w` picks, for each matching, the
non-empty region set to flip (a function rather than `∃`, to keep the inductive non-nested). -/
inductive Good (cf : Conf) : Nat → Prop
  | base (k : Nat) : extendsQ cf k = true → Good cf k
  | step (k th : Nat) : 1 ≤ th → th ≤ 3 → (transitions cf.r k th).size ≠ 0 →
      (w : Array Nat → Nat) → (∀ lab ∈ matchTable[(transitions cf.r k th).size / 2]!, 0 < w lab) →
      (∀ lab ∈ matchTable[(transitions cf.r k th).size / 2]!,
        Good cf (canon cf.r (k ^^^ flipMask cf.r k th lab (w lab)))) →
      Good cf k

/-- The geometric input, abstracted: for a realised code and a pairing θ with transitions, the
outside Kempe chains realise SOME matching of the table, and every set of its regions can be
swapped (staying realised). -/
def KempeMatching (cf : Conf) (P : Nat → Prop) : Prop :=
  ∀ k th, P k → 1 ≤ th → th ≤ 3 → (transitions cf.r k th).size ≠ 0 →
    ∃ lab ∈ matchTable[(transitions cf.r k th).size / 2]!,
      ∀ s, P (k ^^^ flipMask cf.r k th lab s)

/-- **(S2) Combinatorial core.** -/
theorem good_sound (cf : Conf) (P : Nat → Prop)
    (hcanon : ∀ k, P k → P (canon cf.r k)) (hK : KempeMatching cf P) :
    ∀ k, Good cf k → P k → ∃ k', P k' ∧ extendsQ cf k' = true := by
  intro k hk
  induction hk with
  | base k h => exact fun hP => ⟨k, hP, h⟩
  | step k th h1 h3 hT w _ _ ih =>
    intro hP
    obtain ⟨lab, hlab, hflip⟩ := hK k th hP h1 h3 hT
    exact ih lab hlab (hcanon _ (hflip (w lab)))

/-- **(S1) Loop correctness of the checker** — NOT PROVED (statement only). -/
theorem run_sound (cf : Conf) (hD : dReducible cf = true) :
    ∀ k ∈ ringColourings cf.r, Good cf k := by
  sorry

/-- Every proper ring code has its canonical form in `ringColourings` — NOT PROVED. -/
theorem canon_mem (r k : Nat) (hr : 2 ≤ r)
    (hk : ∀ i, i < r → col k i ≠ col k ((i + 1) % r)) (hlt : k < 4 ^ r) :
    canon r k ∈ ringColourings r := by
  sorry

/-- (S1)+(S2): checker-level soundness relative to the geometric hypothesis. Proved from the two
`sorry`s above. -/
theorem dReducible_sound (cf : Conf) (hD : dReducible cf = true) (hr : 2 ≤ cf.r)
    (P : Nat → Prop) (hcanon : ∀ k, P k → P (canon cf.r k)) (hK : KempeMatching cf P)
    (hprop : ∀ k, P k → (∀ i, i < cf.r → col k i ≠ col k ((i + 1) % cf.r)) ∧ k < 4 ^ cf.r)
    (k : Nat) (hP : P k) : ∃ k', P k' ∧ extendsQ cf k' = true :=
  good_sound cf P hcanon hK _
    (run_sound cf hD _ (canon_mem cf.r k hr (hprop k hP).1 (hprop k hP).2)) (hcanon k hP)

end DCheck

#print axioms DCheck.good_sound
#print axioms DCheck.dReducible_sound
