# Night Lean audit: do the definitions say what the hand mathematics says?

Adversarial definition audit, 7 October 2026 (written 02:15 MDT). I did not recompile anything. I read the Lean files in
`StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`: QuarterFloor, QuarterRotation, NoFrozen, QuarterRotationPlanar, QuarterPi, QuarterWinding, QuarterFloorH, QuarterFloorHBridge, QuarterSigmaExit and QuarterSigmaGroups. I also read the library definitions they rest on (`VacancySlide.ProperOff`, `VacancyShortFill.{Missing, Target, Active, pairGraph, Whole, swap, KempeStep}`, `SphericalCompletion.Triangulated`, `VacancyIcosahedral.IcoBall`, `VacancyMobility.FiveLink`).

I compared them with these hand sources: NightEulerHole §3, MathQuarterFloorBijections (QFB) §0–§2, NightFloorAtEasyHoles, NightF5Review, NightFloorR53 §5, the night log's Job E, and, after the coordinator's mid-task note, the Studio's `picyc.cpp` (`--sigc`/`--jobe`) and `witness-sigC-p26-70869-h11.json`.

## Summary

| # | item | verdict |
|---|---|---|
| 1 | `Pent` | PASS (orientation note) |
| 2 | `RepeatAt`, `Lock1`, `Lock2`, `DoublyLocked`, classification | PASS |
| 3 | `SingletonAt`, `Target` | PASS |
| 4 | `KempeStep`, `KempeEquiv`, `kclass` | PASS (symmetry true but not formalised) |
| 5 | `piMove`, `lam`, `lam_eq` | PASS |
| 6 | `QuarterFloorConj` (labelled vs. up to renaming) | PASS |
| 7 | `IcoBallP`, `TripleBallP`, `quarterFloor_of_fiveLink` | PASS |
| 8 | `sigmaLink`, `sigmaGroup`, `SigmaC` | definitions PASS; **scope of `SigmaC` FAIL** (it is stated with no hole family, and is false in general) |
| 9 | vacuity and trivialities | PASS (one missing sanity witness, recommended) |

No definition makes a proved theorem vacuous or trivial. The one real problem concerns scope, not proofs. `SigmaC P` is stated for every pentagonal hole, while the hand Conjecture σC is restricted to R5³ holes, and the universal form is refuted by the Studio's Job F witness (§8).

---

## 1. `Pent` — PASS

- **What it says.** `Pent` has the fields `adj_h : ∀ i, Adj h (x i)`, `only : ∀ v, Adj h v → ∃ i, v = x i` and `inj : Injective x`. Together they make the neighbour set of `h` exactly `{x 0, …, x 4}`, five distinct vertices, so `deg h = 5`.
- **The 5-cycle.** `adj_cyc : ∀ i, Adj (x i) (x (i+1))` makes the five vertices a 5-cycle in index order. Chords are not excluded, which is correct: the theorems are proved without needing an induced link.
- **Tie to the rotation.** `Pent` itself is graph-only. On a `SphericalMap`, NoFrozen's `rotation_nbrs` proves (with a private copy in QuarterRotationPlanar and QuarterPi) that the rotation neighbours of the dart `h → x (j+1)` are `{x j, x (j+2)}`, for every `j`.
  - The rotation at `h` is a single 5-cycle (`rotation.cyclic`), so it has no 2-cycles. Hence the `Pent` order **is** the embedding's cyclic order, up to one global reversal.
  - So on a sphere no `Pent` exists whose order differs from the rotation order other than by a reflection.
- **Effect of a reflection.** A reflected `Pent` swaps the roles of R₊₃ and R₊₂ (and of M2 and M3). π, λ and σ are then the mirrored moves.
  - Every proved theorem holds for an arbitrary `Pent`, so for both orientations, and none is false or vacuous for either.
  - The hand data were also run in both orientations (F5, σC).
  - The one orientation-sensitive object is `SigmaC P`: it is a statement about one orientation. See §8: the Job F counterexample is in the plantri orientation only.
- **Graph-only files.** QuarterFloor and QuarterRotation hold for any `Pent` in any graph. Planarity enters only through `rotation_nbrs`/`alternating_walks_intersect`, as their docstrings say. QuarterFloorHBridge rebuilds `P'` from `exists_rotation_link`, so F5 is applied in rotation order. Its conclusion (`QuarterFloorConj`) does not mention `P` at all.

## 2. Repeat pattern and locks — PASS

- **`RepeatAt P c j`.** It requires `c(x j) = c(x (j+2))`, and the three other link colours distinct from that colour and from each other. That is exactly the link `(α, μ, α, A, B)` at `j..j+4`, i.e. "unfilled with repeat pair {j, j+2}".
  - It also implies that the link edges are properly coloured: `x(j+2)x(j+3)` is `α ≠ A`, and `x(j+4)x j` is `B ≠ α`.
- **`Lock1`.** `m = x(j+1)` reaches `a = x(j+3)` in `pairGraph G h c μ A`.
- **`Lock2`.** `m` reaches `b = x(j+4)` in `pairGraph … μ B`.
  - `pairGraph` is the two-colour graph of `G − h` (`Active` excludes `h`), as QFB §0 requires.
- **`DoublyLocked`.** `RepeatAt ∧ Lock1 ∧ Lock2`. ✓
- **Classification (QuarterPi).**
  - `classify`: every `ProperOff` state is `RepeatAt` for some `j` or `SingletonAt` for some `i`, by `decide` over all 5-cycle colourings (`classify5`).
  - `rep_unique`: the repeat index is unique, and this needs no properness.
  - `rep_not_target`: `RepeatAt` excludes `Target`.
  - So every proper unfilled state is `RepeatAt` for exactly one `j`. ✓
- **Hex, R₊₃ and R₊₂.**
  - `Rot3Def`/`Rot2Def` are QFB's "x_j ∉ K" and "x_{j+2} ∉ K′", with the components seeded at `x(j+2)` and `x j` exactly as in QFB §1.
  - `kempe_hex` carries no properness hypothesis. That is harmless: the Hex lemma is topological, so the statement is stronger.

## 3. Filled states — PASS

- **`Target G h c`** is `∃ x, ∀ v ∼ h, c v ≠ x`, i.e. some colour is missing on the link: "filled". It ignores `c h`.
- **`SingletonAt P c i`** is `Target ∧ ∀ k ≠ i, c(x k) ≠ c(x i)`.
  - `filled_shape` derives the link `(W, X, Y, X, Y)` from it, with `Z = zcol` the fourth colour. So it is exactly "filled with singleton at i".
  - `single_unique` (needs `ProperOff`) gives uniqueness. `classify` gives existence for proper filled states.
- `SingletonAt` alone does not force properness of the link. It is only ever used with `ProperOff` in hand.

## 4. `KempeStep`, `KempeEquiv`, `kclass` — PASS (one formalisation gap)

- **`KempeStep G h c d`** is `∃ a b S, a ≠ b ∧ Whole G h c a b S ∧ d = swap c a b S`, where `Whole` means `S` is exactly the `pairGraph`-component of an active seed. This is "swap one whole Kempe component of G − h".
- **`KempeEquiv`** is `ReflTransGen KempeStep`. `kclass M h c₀` is the set of `ProperOff` states `d` with `KempeEquiv c₀ d`.
- **Symmetry.** `KempeStep` is symmetric as a relation, so forward reachability is the true class.
  - Given `Whole c a b S`, the lemmas `pairGraph_swap`/`pairGraph_swap_same` give `pairGraph (swap c a b S) a b = pairGraph c a b`.
  - `active_swap_iff` keeps the seed active. So `Whole (swap c a b S) a b S` holds.
  - `swap_swap` / `swap_swap_self` / `kswap_inv` give `swap (swap c a b S) a b S = c`. Hence `KempeStep d c`.
  - **This symmetry lemma is not stated anywhere.** No proved theorem needs it: `piMove_bijOn_class` only uses forward steps `d → π d` and `d → π⁻¹ d`. But the *reading* of `kclass` as "the Kempe class" depends on it.
  - **Fix (recommended, small):** add to QuarterFloor
    `theorem kempeStep_symm : KempeStep G h c d → KempeStep G h d c` (proof: the four lemmas above), and
    `theorem kempeEquiv_symm : KempeEquiv c d → KempeEquiv d c` (by `ReflTransGen` induction).
- **Invariants of a class.**
  - Properness is preserved (`properOff_swap`, `properOff_of_kempeEquiv`).
  - `h` is never in a swapped set: the seed is active, hence `≠ h`, and `h` is isolated in `pairGraph`. So `c h` is constant on a class.

## 5. π and λ — PASS

The `piMove` case table matches NightEulerHole §3 and QFB §2 row by row:

| case | Lean | hand |
|---|---|---|
| `U_j`, `Lock2` | `rot3`: swap the `{c x_j, c x_{j+3}} = {α,A}`-component of `x_{j+2}` | R₊₃ ✓ |
| `U_j`, `¬Lock2` | `phiBinv`: swap the `{μ,B}`-component of `x_{j+4}` | φ_B⁻¹ ✓ |
| `F_i`, `M3Short` | `phiA`: swap the `{Y,Z}`-component of `x_{i+2}` | φ_A ✓ |
| `F_i`, `¬M3Short` | `tau`: swap the `{W,X}`-component of `x_{i+3}` | τ ✓ |

- **Short and long bits.**
  - `M3Short` is "x_{i+2} ≁ x_{i+4} in {Y,Z}", QFB's M3 (short).
  - `M2Short` is "x_{i+1} ≁ x_{i+3} in {X,Z}", QFB's M2 (short).
  - The inverse moves (`rot2`, `phiAinv` = `{μ,A}` of `m`, `phiB` = `{X,Z}` of `x_{i+1}`, `tauInv` = `{W,Y}` of `x_{i+2}`) match QFB §1–§2.
- **λ values.** `lam` is +1 / −1 / −1 / −3 in the same four cases, and `lam_table` restates this.
- **`lam_eq`.** `λ = 1 − 2[F c] − 2[F πc]`, checked against the table:
  - U→U gives 1 − 0 − 0 = **+1**;
  - U→F gives 1 − 0 − 2 = **−1**;
  - F→U gives 1 − 2 − 0 = **−1**;
  - F→F gives 1 − 2 − 2 = **−3**.
  - The image types come from the proved `*_spec` lemmas, so the identity is not circular.
- **σ.** `sigma` (2j+1 on U_j, 2i+4 on F_i) matches the token sum.
- **The `choose` branches.** `piMove` uses `hr.choose`/`hs.choose`, which is harmless by uniqueness. The final `else c` branch is reached only off `ProperOff`.
- **Counting identities.** QuarterWinding's U is `¬Target`, which on proper states is "unfilled". ✓

## 6. `QuarterFloorConj` — PASS

- **Statement.** `4 · #{c ∈ class(c₀), Target c} ≥ #class(c₀)` for every proper `c₀`, i.e. F ≥ |class|/4. Classes are counted via `Nat.card` of subtypes, and `card_class` shows these equal the `kclass` finsets.
- **The extra coordinate `c h`.** `V → Fin 4` carries a junk value at `h`, but it is constant on a class (§4), and `Target` ignores it. So the labelled counts are exactly the counts of proper colourings of G − h in the class.
- **Renaming invariance.** For a permutation ρ of the colours, applied off `h`:
  - "rename by a transposition (a b)" is the product of the swaps of all `{a,b}`-components, each a `KempeStep`, and finitely many since `V` is finite. So every class is closed under renaming.
  - `Target` is renaming-invariant.
  - With a `Pent`, every proper state uses at least 3 colours on the link (an odd cycle). So S₄ acts freely and every orbit has size 24.
  - Hence labelled F/|class| equals the up-to-renaming ratio, as QFB §0 says.
- **Fine print.** `QuarterFloorConj` itself does not assume a `Pent`. For a hole with a bipartite G − h the orbit sizes could vary, but every theorem that proves or uses the floor has a `Pent` in scope. No fix is needed.

## 7. `IcoBallP`, `TripleBallP`, degree — PASS

- **`IcoBallP P w`.** It says the neighbours of `x t` are exactly `h, x(t−1), x(t+1), w(t−1), w t`, with `w t ∼ w(t+1)` and every `w t` off the link and off `h`.
  - These five are distinct: `w(t−1) ≠ w t` follows from `ring`. So `deg x t = 5`, with the hand's ring structure.
  - It is the library `IcoBall` restated in `Pent` coordinates.
  - It does **not** require the five `w t` to be pairwise distinct (the hand hypothesis does). That makes the formal hypothesis weaker and the theorem stronger, which agrees with NightF5Review §4 ("IcoBall distinctness is not needed").
- **`TripleBallP P w j`.** The same neighbour lists, for `x j, x(j+1), x(j+2)` only, plus the three ring edges and `x(j+4) ∼ w(j+4)`, `x(j+3) ∼ w(j+2)`. That is exactly Lemma 3′'s "x₀, x₁, x₂ have degree 5", and `IcoBallP.triple` derives it.
- **`R3At`.** `DoublyLocked` plus the outer ring (B, A, B, μ, A), which is the hand's R3.
- **The degree in `quarterFloor_of_fiveLink`.** Its hypothesis `M.graph.degree (P.x i) = 5` is `SimpleGraph.degree` of the `SphericalMap`'s graph, so it is the true graph degree.
  - With `M.Triangulated`, the bridge derives `IcoBallP` (via `chain5`, `exists_rotation_link`), or else a link 5-clique, a vacuous branch that is impossible on a sphere anyway.
  - No separating-triangle hypothesis is assumed. This agrees with NightF5Review §5.4.

## 8. σ-links, σ-groups, `SigmaC`

**Definitions vs. hand and Studio: PASS.**
- **`sigSwap P c j`.** `kswap` of the `{c x_j, c x_{j+1}} = {α, μ}`-component of `x_{j+1}`, which is σ in NightFloorR53 / NightFloorAtEasyHoles.
- **`DDStep c`.** `DLState c ∧ DLState (π c)`.
- **`DDEnd c`.** `DDStep c ∨ DDStep (π⁻¹ c)`, an endpoint of a DD step.
- **`sigmaLink c d`.** `DDEnd c ∧ ∃ j, DoublyLocked c j ∧ d = sigSwap c j`. So σ is taken from DD-step endpoints only, at the endpoint's own repeat index. ✓
- **`sigmaGroup c₀ c`.** The `EqvGen` class of `c`, inside `kclass c₀`, under "d = π c or σ-link c d".
  - π is a permutation of the finite class, so π-steps generate exactly the π-cycles.
  - `EqvGen` makes σ-links undirected.
  - So a σ-group is a connected component of the graph on π-cycles with an edge Z–Z′ whenever σ sends a DD endpoint on Z into Z′. That is NightFloorR53 §5 verbatim.
  - The restriction to the class is harmless, since σ is a Kempe step (`sigmaLink_mem_kclass`).
- **The Studio's test (`picyc.cpp`, `--sigc`/`--jobe`, lines 235–258).**
  - Its endpoints are `kind[k]==2` (DL) with `kind[π k]==2 || kind[π⁻¹ k]==2`, i.e. `DDEnd`.
  - Its σ floods from `link[(j+1)]` in colours `{al, mu}` and swaps, i.e. `sigSwap` at the state's repeat `j`.
  - It union-finds the π-cycles of the cycles of `k` and of `σ(k)`, and fails a group when Σw > 0.
  - The Studio unions over all states of the hole rather than per class. That is equivalent, because σ and π never leave a class.
  - It counts states up to renaming. π and σ commute with renaming and S₄ acts freely, so each labelled σ-group maps onto a quotient group with constant fibre size. **The sign of Σλ is the same in both.**
  - **So the Studio tested exactly the formal `sigmaGroup`.**
- **Consequence.** The witness `p26 #70869`, hole 11, has `P = (4, 10, 20, 12, 5)` in plantri rotation order and link degrees (5,6,5,6,6). Its group of two π-cycles has Σw = +1, i.e. Σλ = +5 up to renaming, and a positive multiple of 5 labelled.
  - That witness is a counterexample to the formal `SigmaC P` for that `P` on the corresponding `SphericalMap`.
  - This is computational. It is not checked in Lean.
  - The mirrored `P` is not refuted: the Studio found no positive cycle there.

**Scope of `SigmaC`: FAIL (docstring and statement scope, not a proof error).**
- **The mismatch.**
  - `SigmaC P` has no hypothesis on the hole. Its docstring says "Every σ-group of every Kempe class has Σλ ≤ 0", and the module header calls it "Conjecture σC".
  - The hand Conjecture σC (NightFloorR53 §5) is stated **at R5³ holes**: a triangulation with no separating triangle and three cyclically consecutive degree-5 link vertices.
  - The pattern (5,6,5,6,6) is not R5³, so the hand conjecture survives the witness. The formal universal reading does not.
- **What remains true.** `sigmaC_imp_quarterFloor` (an implication) and `sigmaC_of_icoBall` (the all-5 case, a genuine theorem) are unaffected.
- **Exact fix (docstrings; the coordinator asked me not to edit the Lean, so this is a recommendation).**
  - Replace the `SigmaC` docstring with:
    > `/-- The σ-group floor at the hole `P`: every σ-group of every Kempe class has `Σ λ ≤ 0`. **Not true in general**: it fails at plantri p26 #70869 (`plantri -m5 -c4 -a 26`, 1-based), hole 11, plantri orientation, link degrees (5,6,5,6,6), where a σ-group of two π-cycles has Σw = +1 (Studio Job F, `local-runs/27-studio-positive-config/witness-sigC-p26-70869-h11.json`). Conjecture σC (`NightFloorR53.md` §5) asserts it only at R5³ holes (spherical triangulation, no separating triangle, three cyclically consecutive degree-5 link vertices); the Studio also found 0 failures at every (5,5,5,5,6) hole, orders 24–26. Proved at all-5 holes (`sigmaC_of_icoBall`). -/`
  - In the module header, replace "**Conjecture `σC`**: `Σ λ ≤ 0` over every `σ`-group of every class" with "`SigmaC P`: the σ-group floor at the hole `P` (a per-hole property, false in general; Conjecture σC is the claim that it holds at R5³ holes)".
  - Optionally, to make the conjecture itself a formal object, add:
    ```lean
    def R5Cubed (P : Pent M.graph h) : Prop :=
      ∃ j : Fin 5, ∀ i : Fin 3, M.graph.degree (P.x (j + i)) = 5
    def SigmaCConj : Prop := ∀ (n : ℕ) (M : SphericalMap n) (h : Fin n) (P : Pent M.graph h),
      M.Triangulated → NoSeparatingTriangleAt … → R5Cubed P → SigmaC P
    ```
    The no-separating-triangle clause should use the library's `NoSeparatingTriangleAt`, or a global version; check the name before adding. Then cite `SigmaCConj` and keep `SigmaC P` as the per-hole predicate.
- **README / START-HERE wording:** "σC (Lean `SigmaC P`) is a per-hole statement. Proved at all-5 holes (`sigmaC_of_icoBall`). Conjectured at R5³ holes (and holding in the data at (5,5,5,5,6)). False in general: Job F witness p26 #70869 h11, pattern (5,6,5,6,6), one failing group in about 114M."
- **Orientation.** A full-fidelity statement should say that the conjecture is claimed for both orientations, i.e. for every `Pent` on the hole. The universally quantified `SigmaCConj` above does this automatically.

## 9. Vacuity and quirks — PASS

- **Every `Pent` hypothesis is satisfiable** on a triangulated `SphericalMap`: any vertex of the icosahedron. `IcoBallP` is satisfiable there too, and `TripleBallP` follows from it.
  - The library has `Icosahedron.graph`, `rotation` and `degree_five`, but no file builds a `Pent`, `Triangulated` or `IcoBallP` instance for it.
  - **Recommended sanity theorem (not required for correctness):** `example : ∃ P : Pent icosahedron.graph 0, ∃ w, IcoBallP P w`, plus `icosahedron.Triangulated`. That makes non-vacuity of F5 and the σ results machine-checked.
- **Hypotheses are not contradictory.**
  - `rot3_bijOn` (Lock2 ∧ Rot3Def) and the planar versions are consistent: the wheel and the icosahedron have such states.
  - `quarterFloor_of_fiveLink` has a vacuous *branch* (a link 5-clique, i.e. K₆ in a planar graph), but the theorem itself is not vacuous.
- **Nothing is trivial by a definitional quirk.**
  - `QuarterFloorConj` could only be trivial if classes were empty or `Target` were always true. Neither holds: `rep_not_target` exhibits unfilled states.
  - `lam` is not defined from `filledZ`. It is defined by the table, and `lam_eq` is proved through the `*_spec` image lemmas.
  - `sigmaGroup` is not the whole class by definition. A σ-link needs a DD endpoint.
- **Hygiene.** NoFrozen and QuarterRotation both declare `QuarterFloor.pairGraph_comm`, which forced private copies of the Jordan block in QuarterRotationPlanar and QuarterPi. The copies are faithful: same statements, same library lemma. Renaming one declaration would remove about 250 duplicated lines. This is cosmetic.

## Fixes, in priority order

1. **`SigmaC` docstrings and scope (§8):** the wording above, and optionally `R5Cubed` / `SigmaCConj`. This is the only item where a reader would currently be misled.
2. **`kempeStep_symm`, `kempeEquiv_symm` (§4):** a two-line justification that `kclass` is the Kempe class.
3. **Icosahedron `Pent`/`IcoBallP`/`Triangulated` witness (§9):** machine-checked non-vacuity.
4. Optional: rename one of the two `pairGraph_comm` declarations to allow co-import.
