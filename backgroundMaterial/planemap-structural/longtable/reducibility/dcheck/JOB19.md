# Job 19 (Studio): DCheckSound R2, project-level glue [exploratory]

Pre-registration, written 2026-10-15 00:26 MDT before any proof work.

**Target.** In a file that imports `RingReduce` (StudioMathLean PlaneMap) and `DCheckS1`/`DCheckS3`/`DCheckR1`:
```
theorem ConfigOcc.colorable_of_dReducible (cf : DCheck.Conf) (hD : DCheck.dReducible cf = true)
    (hr2 : 2 ≤ cf.r) (hr : cf.r ≤ 15)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true)
    (O : ConfigOcc T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4
```
(`cf.r ≤ 15` because DCheck's `matchTable` stops at p = 7; Job 23 lifts it.)

**Pieces.**
- (A) `extendsQ` soundness: a true backtracking result gives an interior colouring (`hint`, `hring`).
- (B) ring code of a colouring, `col (code c) t = c (ρ t)`, `code c < 4^r`.
- (C) realised codes are proper on the ring (`ring_proper`, `ring_proper_wrap`).
- (D) `canon r (code c) = code (σ ∘ c)` for some colour permutation σ (from `S1.cinv`).
- (E) **R2 proper:** `KempeMatching cf P` for P = codes of proper colourings of G off the hole. Arc chains satisfy
  `NCLabel` (from `chains_noncrossing(_same)`) and `ParityLabel`. With `nc_matching` and `matchTable_complete`, the
  flip of the selected chains is proper and has ring code `k ^^^ flipMask r k θ lab s`.
- (F) Assemble with `dReducible_sound` and `ConfigOcc.colorable_of_ext`.

**Hypothesis H19.** (A)–(F) go through using only the existing lemmas, with no new geometric input. The only
geometry is in `chains_noncrossing(_same)`.
**Kill.** A step that needs a geometric fact not already in the repo, for example that a Kempe chain meeting the ring
in two arcs of the same class must pass through the outside (it can't use the hole), or that `ProperOff` is too weak for
the flip. Report the missing statement exactly.
**Axiom budget.** propext, Classical.choice, Quot.sound, plus the existing native_decide axioms of R1 (`check4..8`).
