# Check of paper §3 ("What is compiled in Lean") against the Lean source

- **By:** Math review worker (low priority), 2026-10-06
- **Paper:** `SolvingFrameworkPlan/docs/reports/VHE-paper/main.tex` lines 163–276, plus the Lean statements in §1 and the abstract. Severn/Long Table draft (`messages/2026-10-06/2026-10-06_1244_severn_...paper-sections-2-7-draft.md`).
- **Source read:** `/Users/fulkanjou/mathlib4-planemap` (read only; nothing built, edited or staged). Local `master` is at `bcff6cd`. All 73 files in `Mathlib/Combinatorics/SimpleGraph/PlaneMap/` on remote branch `current` (`8299419`, confirmed with `gh api`), and `PlaneMap.lean`, are byte-identical to the local files (git blob hashes).
- **Hashes:** all 117 cited or audited sources in the local tree match the latest recorded hashes (`audit-101/SHA256SUMS-sources`, then `L4-P/run1/SHA256SUMS-sources`, then the authors-header and copyright-header edit lists). 0 differ.
- **Audits used:** `docs/reports/Lean105ModuleAudit.md` (manifest `audit-101/manifest.json`, 105 modules) and `longtable/audit/L4-P/REPORT.md` (manifest `run1/manifest.json`, 116 modules).
- **Scope of this check:** each declaration's name, signature and audit membership, and whether the prose matches it. This check does not cover the proofs; the kernel and the audits cover those.

**Overall result.** Every declaration named in §3 exists with the namespace the paper gives, except that the names in item 9 are given without their namespaces. Every result labelled `[compiled]` is in the stated audits. The two results in "Built, not audited" are in neither audit. No result is stated more strongly than its Lean statement allows, except in the minor cases listed below. The required corrections are 1 (provenance of the published files), 2 (the scope of "the vacancy modules") and 11 (the summary sentence on the belt). The others are precision edits.

## Per-claim table

| Paper claim | Declaration (file:line) | Exists | 105 | 116 | Prose matches? |
|---|---|---|---|---|---|
| Thm M3 | `SimpleGraph.VacancyShortFill.short_fill` (VacancyShortFill.lean:419), `optimal_short` (:461) | yes | yes | yes | yes |
| Thm L3 | `SimpleGraph.VacancyThreeMoveObstruction.first_is_slide` (:32), `first_pair_contains_slide_colour` (:67) | yes | yes | yes | yes (item 4) |
| Thm L4 | `SimpleGraph.VacancyLemmaL4.l4a` (:202), `l4b` (:353), `l4b_le` (:371), `l4c` (:384) | yes | **no** | yes | yes (item 5) |
| Thm mobility (a) | `SimpleGraph.SphericalMap.vacancy_mobility_general` (VacancyMobilityGeneral.lean:121) | yes | yes | yes | yes (item 6) |
| Thm mobility (b) | `SimpleGraph.SphericalMap.vacancy_mobility_triangulated` (VacancyMobilityTriangulated.lean:122) | yes | yes | yes | yes, with the caveat already in the paper |
| `Approach` | `SimpleGraph.VacancyMobility.Approach` (VacancyMobility.lean:58) | yes | yes | yes | yes |
| Thm lift | `SimpleGraph.VacancyCliqueLift.interior_fill_lift` (VacancyCliqueLift.lean:226), `protected_fill_lift` (VacancyProtectedLift.lean:50) | yes | yes | yes | yes |
| Belt walk | `SimpleGraph.TwoPoleBeltWalk.belt_unequal_at` (TwoPoleBeltAllRoots.lean:31) | yes | yes | yes | yes (item 7) |
| Thm P | `SimpleGraph.TheoremPPole.theoremP` (TheoremPPoleNoSingleton.lean:114) | yes | **no** | yes | yes (item 8) |
| Belt all holes | `SimpleGraph.TwoPoleBeltPoleHole.belt_theorem_all_holes` (**TwoPoleBeltPoleB.lean**:129) | yes | no | no | yes |
| VacancyAt / VacancyHyp | `SimpleGraph.VacancyHyp.VacancyAt` (TwoPoleBeltVacancyHypDef.lean:33), `SimpleGraph.VacancyHyp.VacancyHyp` (:39) | yes | no | no | item 9 |
| vacancyHyp_belt | `SimpleGraph.TwoPoleBeltVacancyHyp.vacancyHyp_belt` (TwoPoleBeltVacancyHyp.lean:38) | yes | no | no | item 9 |
| Five Colour | `SimpleGraph.SphericalMap.five_color_theorem` (FiveColorTheorem.lean:30), `SimpleGraph.PlaneMap.five_color_theorem` (:54) | yes | yes | yes | yes (item 10) |

The two "built, not audited" results are untracked in the local checkout and absent from branch `current`, as the paper says.

## Signatures (quoted from the source)

```lean
-- VacancyShortFill.lean
def KempeStep [DecidableEq C] (h : V) (c d : V → C) : Prop :=
  ∃ a b S, a ≠ b ∧ Whole G h c a b S ∧ d = swap c a b S
def PureFill [DecidableEq C] (h : V) (c : V → C) (bound : Nat) : Prop :=
  ∃ n, n ≤ bound ∧ ∃ d, PurePath G h n c d ∧ Target G h d
theorem short_fill ... {n : Nat} {t : V × (V → C)} (hc : ProperOff G h c)
    (hn : n ≤ 2) (path : MixedPath G n (h,c) t)
    (filled : Target G t.1 t.2) : PureFill G h c n
theorem optimal_short ... (hc : ProperOff G h c) (hn : n ≤ 2) (optimal : MixedOptimal G h c n) :
    PureOptimal G h c n

-- VacancyThreeMoveObstruction.lean
theorem first_is_slide (hc : ProperOff G h c) (no_pure : ¬ PureFill G h c 3)
    (path : MixedPath G 3 (h,c) t) (filled : Target G t.1 t.2) :
    ∃ u, G.Adj h u ∧ UniqueAt G h u c ∧ MixedPath G 2 (u,slide h u c) t
theorem first_pair_contains_slide_colour (hc : ProperOff G h c)
    (no_pure : ¬ PureFill G h c 3) (adj : G.Adj h u) (unique : UniqueAt G h u c)
    (hab : a ≠ b) (whole : Whole G u (slide h u c) a b S)
    (second : KempeStep G u (swap (slide h u c) a b S) d)
    (filled : Target G u d) : c u = a ∨ c u = b

-- VacancyLemmaL4.lean
theorem l4a (hc : ProperOff G h c) (no_pure : ¬ PureFill G h c 3)
    (adj : G.Adj h u) (unique : UniqueAt G h u c) (hρ : c u ≠ ρ)
    (hS : Whole G u (slide h u c) (c u) ρ S) (hh : h ∉ S)
    (second : KempeStep G u (swap (slide h u c) (c u) ρ S) d) (filled : Target G u d) :
    (∀ v, G.Adj h v → v ∉ S) ∧ (∃ v ∈ S, G.Adj u v ∧ c v = ρ) ∧
    (∃ x, G.Adj h x ∧ c x = ρ ∧ (pairGraph G h c (c u) ρ).Reachable u x) ∧
    (∀ v ∈ S, (pairGraph G h c (c u) ρ).Reachable u v) ∧
    (∃ y, G.Adj u y ∧ c y = ρ ∧ y ∉ S ∧ (pairGraph G u (slide h u c) (c u) ρ).Reachable h y ∧
      ∃ x, G.Adj h x ∧ c x = ρ ∧ (pairGraph G u (slide h u c) (c u) ρ).Reachable y x)
theorem l4b [Finite V] (hc : ProperOff G h c) (adj : G.Adj h u) (unique : UniqueAt G h u c)
    (hρ : c u ≠ ρ) (hS : Whole G u (slide h u c) (c u) ρ S) (hh : h ∈ S)
    (hno : ∀ y ∈ S, G.Adj u y → c y ≠ ρ) :
    PureFill G h c (rhoComps G h c (c u) ρ).ncard ∧
    (rhoComps G h c (c u) ρ).ncard ≤ (rhoNbr G h c ρ).ncard
theorem l4c [Finite V] (hc : ProperOff G h c)
    (no_pure : ¬ PureFill G h c (max 3 (rhoNbr G h c ρ).ncard)) (adj ...) (unique ...) (hρ ...)
    (hS : Whole G u (slide h u c) (c u) ρ S) (second : KempeStep ...) (filled : Target G u d) :
    ∃ y, G.Adj u y ∧ c y = ρ ∧ (pairGraph G u (slide h u c) (c u) ρ).Reachable h y

-- VacancyMobility.lean (namespace SimpleGraph.VacancyMobility)
structure FiveLink (h : V) where
  port : Fin 5 → V
  injective : Function.Injective port
  neighbours : ∀ v, G.Adj h v ↔ ∃ i, v = port i
def Approach (h : V) (c : V → Fin 4) (u : V) : Prop :=
  ∃ d, (d=c ∨ KempeStep G h c d) ∧ ProperOff G h d ∧ G.Adj h u ∧ UniqueAt G h u d

-- VacancyMobilityGeneral.lean (namespace SimpleGraph.SphericalMap)
theorem vacancy_mobility_general {h : Fin n} (L : FiveLink M.graph h)
    {c : Fin n → Fin 4} (hc : ProperOff M.graph h c)
    (ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)))
    (rot : ∀ i : Fin 5, M.rotation.next ⟨(h,L.port i),_⟩ = ⟨(h,L.port (i+1)),_⟩) :
    PureFill M.graph h c 1 ∨ ∀ u, M.Adj h u → Approach M.graph h c u
-- VacancyMobilityTriangulated.lean
theorem vacancy_mobility_triangulated (htri : M.Triangulated) {h : Fin n}
    (L : FiveLink M.graph h) {c : Fin n → Fin 4} (hc : ProperOff M.graph h c) :
    PureFill M.graph h c 1 ∨ ∀ u, M.Adj h u → Approach M.graph h c u
-- SphericalCompletion.lean:32
def Triangulated (M : SphericalMap n) : Prop := ∀ d : M.Dart, M.rotation.faceLength (M.faceOf d) = 3

-- VacancyCliqueLift.lean / VacancyProtectedLift.lean
def Boundary (A F : Set V) : Prop := F ⊆ A ∧ ∀ u v, u ∈ A → v ∉ A → G.Adj u v → u ∈ F
def Clique (F : Set V) : Prop := ∀ u v, u ∈ F → v ∈ F → u ≠ v → G.Adj u v
theorem interior_fill_lift (bd : Boundary G A F) (cl : Clique G F) {g : V → C}
    (path : InteriorPath G A F n s t) (eq : ∀ v, v ∈ A → g v = s.2 v)
    (proper : ProperOff G s.1 g) (filled : Target (sideGraph G A) t.1 t.2) :
    ∃ e, MixedPath G n (s.1,g) (t.1,e) ∧ ProperOff G t.1 e ∧ Target G t.1 e
theorem protected_fill_lift (same hypotheses) :
    ∃ e, ProtectedPath G A F n (s.1,g) (t.1,e) ∧ ProperOff G t.1 e ∧ Target G t.1 e

-- TwoPoleBeltAllRoots.lean (namespace SimpleGraph.TwoPoleBeltWalk; G n := TwoPoleBelt.graph n)
theorem belt_unequal_at (hn : 5 ≤ n) (h : Vertex n) (hb : IsBelt h)
    (c : Vertex n → Colour) (hc : ProperOff (G n) h c) (hab : c a ≠ c b) :
    ∃ k t, VacancyPotential.Path SlideStep k (h,c) t ∧ k ≤ 2*n ∧ Filled t ∧
      ProperOff (G n) t.1 t.2 ∧ IsBelt t.1 ∧ t.2 a = c a ∧ t.2 b = c b

-- TheoremPPoleNoSingleton.lean (namespace SimpleGraph.TheoremPPole)
theorem theoremP (hn : 5 ≤ n) [NeZero n] (c : Vertex n → Colour) (hc : PR n c) :
    ∃ k, k ≤ 3 * ((jset c).card - 2) + n ∧
      ∃ d, VacancyShortFill.PurePath (graph n) a k c d ∧ Good d
-- PR n c := ProperOff (graph n) a c ; Good d := ∃ x, ∀ i j, d (u i) = x → d (u j) = x → i = j
-- jset c = ring indices i with c (u i) = c b

-- TwoPoleBeltPoleB.lean (namespace SimpleGraph.TwoPoleBeltPoleHole) — NOT AUDITED
theorem belt_theorem_all_holes (hn : 5 ≤ n) (h : Vertex n) (c : Vertex n → Colour)
    (hc : ProperOff (graph n) h c) :
    ∃ k, k ≤ 6 * n ∧ ∃ t : State n, VacancyShortFill.MixedPath (graph n) k (h, c) t ∧
      Filled t ∧ ProperOff (graph n) t.1 t.2

-- TwoPoleBeltVacancyHypDef.lean (namespace SimpleGraph.VacancyHyp) — NOT AUDITED
def VacancyAt (G : SimpleGraph V) (B : ℕ) (h : V) : Prop :=
  ∀ c : V → Fin 4, ProperOff G h c → ∃ k, k ≤ B ∧ ∃ t, MixedPath G k (h, c) t ∧
      Target G t.1 t.2 ∧ ProperOff G t.1 t.2
def VacancyHyp (G : SimpleGraph V) : Prop :=
  ∀ h, ∀ c : V → Fin 4, ProperOff G h c → ∃ k t, MixedPath G k (h, c) t ∧
      Target G t.1 t.2 ∧ ProperOff G t.1 t.2
-- TwoPoleBeltVacancyHyp.lean (namespace SimpleGraph.TwoPoleBeltVacancyHyp) — NOT AUDITED
theorem vacancyHyp_belt (hn : 5 ≤ n) : VacancyHyp (graph n)

-- FiveColorTheorem.lean
theorem SphericalMap.five_color_theorem (M : SphericalMap n) : M.graph.Colorable 5
theorem PlaneMap.five_color_theorem (M : PlaneMap n) : M.graph.Colorable 5
```

## Corrections (owner edits main.tex; numbered for reply)

**1. Required: the published files are not byte-identical to the audited ones (lines 168, 182).**
Both audits hashed and built the sources *before* the header edits. After the audits, the `Authors:` line was changed in 29 files (12:06; `audit-101/SHA256SUMS-authors-header-edit.txt`). A 5-line copyright header was then added to 52 files (12:31; `SHA256SUMS-copyright-header-edit.txt`), including `VacancyLemmaL4` and the 8 `TheoremPPole*`. Math rebuilt the 52 files (`lake build`, exit 0) and diffed each one: only comment lines were added. That rebuild was not an audit. Commit `8299419` is the post-edit state. Suggested sentence after line 182: "After both audits, only the comment header lines of some files were changed (author and copyright lines). The edited files were rebuilt, but not re-audited, and their new hashes are recorded beside the audit." The `% VERIFY` on line 182 can be closed: `gh api` returns `8299419c645c…` for `current`. Branch `current` also holds `FiveColorDemo.lean`, which is not in either audit, and the four PlaneMap notes. So "holds the audited modules" is true, but the branch holds other files too.

**2. Required: "the vacancy modules work on an arbitrary simple graph and an arbitrary colour type" (line 189) is too broad.**
This is true of `VacancySlide`, `VacancyShortFill`, `VacancyThreeMoveObstruction`, `VacancyLemmaL4`, `VacancyCliqueLift` and `VacancyProtectedLift`. It is false for the following:
- mobility uses `Fin 4` and `SphericalMap n` (and `Approach` itself has `c : V → Fin 4`);
- all belt results use `Colour := Fin 4` on `TwoPoleBelt.graph n`;
- `VacancyAt` and `VacancyHyp` fix `Fin 4`.

Suggested: "The modules for short fills, the three-move obstruction, Lemma L4 and the lifts work on …; the mobility and belt results use four colours." Also note that `ProperOff` lives in namespace `VacancySlide` (the comment on line 190 is right), not in `VacancyShortFill`.

**3. Line 168 and §1 line 41: "included in *the* module audit" versus two audits.** §1 says "the module audit", singular. §3 names two. Make §1 read "a module audit (Section 3)". Also, the 105-audit report states that hashes were re-verified *after* the rebuild, and it does not state a separate check before the build. The 116 audit states both. "Checked source hashes before and after the build" is exact only for the 116 audit. Suggested wording: "and checked that no source changed during the build."

**4. L3 (lines 199–203): matches.** Both theorems also assume `ProperOff G h c`, and (a) assumes a mixed path of *exactly* 3 moves. Part (b) assumes only a slide followed by two swaps filling at `u`, not a full three-move fill hypothesis. That is consistent with "any two-swap fill at u". No change needed. Optionally add "proper off its hole".

**5. L4 (lines 205–213): matches.** The paper's (a) gives items 1, 2 and 5 of the five conjuncts. It says it shortened the statement. `l4b` and `l4b_le` assume `[Finite V]` and do not need the two-swap-fill or no-pure-fill premise ("stronger than the hand statement" is correct, as the 116 report says). In `l4b`, r counts the `{σ,ρ}`-components of G−h (under c) through ρ-neighbours of h. The hand's r counts components of K1−h, and the paper uses the Lean meaning, which is correct. L4 is in the 116 audit only, not the 105. The text attributes it correctly.

**6. Mobility (lines 216–225): matches. Two precision edits.**
(a) "a vertex with a five-port link": a `FiveLink` lists the *complete* neighbourhood injectively, so h has degree exactly 5. Say "a degree-5 vertex h with its neighbours listed as five ports (`FiveLink`)".
(b) `SphericalMap n` is a rotation system on `Fin n` whose even edge sets are face sums (`rotation.Fills`). It is not defined through an embedding or through Euler's formula. Define it in one sentence where it first appears.

The existing caveats are correct and should stay: the triangulated hypothesis is global (`∀ d : M.Dart, faceLength = 3`), the five-link is an input, and the theorem is not connected to Theorem A. Both are in the 105 audit.

**7. Belt walk (lines 236–243): matches.** The theorem also assumes `ProperOff (G n) h c` and concludes that the end state is proper off its hole. The path consists of **slides only** (`VacancyPotential.Path SlideStep`). Suggested: "every colouring proper off h whose poles…".

The degree claim on line 236 (belt vertices degree 5, poles degree n) is not itself a theorem. It follows from the exact neighbourhood lemmas `TwoPoleBelt.adj_u` and `adj_v` (TwoPoleBelt.lean), which need `n ≥ 5`, and from the edge definition for the poles. That is acceptable, but cite those lemmas rather than an audit message.

**8. Theorem P (lines 245–250): matches. One wording fix.** "every colouring c of G_n−a" should read "every colouring c proper off a" (`hc : PR n c`, where `PR n c := ProperOff (graph n) a c`). The rest is exact:
- the bound `3 * ((jset c).card - 2) + n` uses truncated subtraction;
- `Good` means "at most once";
- the theorem covers the pole-hole case only;
- the theorem has no no-singleton hypothesis.

`theoremP_fill_or_singleton` (:126) carries the hand's premise, unused. It could be named as the hand-shaped corollary, but this is optional. Audited in 116 only.

**9. Built, not audited (lines 253–263): content correct, names incomplete.**
- Give the namespaces for the definitions and theorem: `SimpleGraph.VacancyHyp.VacancyAt`, `SimpleGraph.VacancyHyp.VacancyHyp`, and `SimpleGraph.TwoPoleBeltVacancyHyp.vacancyHyp_belt`.
- State that both definitions fix **four colours** (`Fin 4`).
- The comment on line 259 is right that `belt_theorem_all_holes` is in file `TwoPoleBeltPoleB.lean`, while its namespace is `TwoPoleBeltPoleHole`. Fine as written.
- The same module also proves `vacancyAt_belt : VacancyAt (graph n) (6*n) h`, the bounded form. Mention it, since the paper quotes the 6n bound.
- It also proves `vacancyHyp_sphericalMap_of_iso`: any `SphericalMap m` whose graph is isomorphic to `G_n` satisfies `VacancyHyp`. This supports the sentence "No spherical-map realisation of G_n exists yet". The transfer is proved, but no such map is constructed.
- Status confirmed: none of `TwoPoleBeltEqualPoles`, `TwoPoleBeltPoleHole`, `TwoPoleBeltPoleB`, `TwoPoleBeltVacancyHypDef` or `TwoPoleBeltVacancyHyp` is in either manifest. All are untracked locally and absent from `current`.

**10. Five Colour (lines 268–273): label `[compiled]` is right, and the scope sentence is right. Delete the CONFLICT comment.**
`FiveColorTheorem` is in both manifests (Math 12:54 item 3 agrees). Add one clause: a `PlaneMap` is a connected rotation system *generated* by attaching vertices at corners and inserting edges within a face (`PlaneMap.lean`, `inductive PlaneMap`). This makes "graphs presented as plane maps" concrete. The comment on line 270 cites `MathlibTest/PlaneMapFiveColor` as the reason it is audited. The stronger reason is that `Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem` itself is in both manifests.

**11. Required: the summary on line 275 overstates the belt results.** "The belt results concern the explicit graph G_n with mixed paths and a moving hole" is true only of the two *unaudited* results. Of the compiled belt results:
- `belt_unequal_at` uses **slides only** (the hole moves, no swaps);
- `theoremP` uses **pure swaps at a fixed hole** (the pole a) and concludes only `Good`, not a fill.

Suggested: "the belt results concern the explicit graph G_n: the unequal-pole walk uses slides only, Theorem P uses swaps at the fixed pole hole, and the all-holes theorem (not audited) uses mixed paths with a moving hole." The phrase "the mobility theorem assumes every face is a triangle" is true of form (b) only. Form (a) instead assumes the ring and rotation hypotheses.

**12. Minor.**
- Line 182: the library is the folder `PlaneMap/` plus the file `SimpleGraph/PlaneMap.lean` (the `PlaneMap` type) and 6 `Coloring/*` modules in the audit. Say "under `Mathlib/Combinatorics/SimpleGraph/`".
- Line 225: "fills in one swap" means at most one swap (`PureFill … 1`). Say "within one swap".
- Line 197: "So ℓ≤2 implies κ=ℓ" is `optimal_short`, which is correct.
- Earlier audit counts (line 178): 83 (ShortFillLeanReport), 85 (ThreeMoveLeanReport), 95 (BeltLeanReport) and 97 then 99 (MathVHCoreAdvance) are all confirmed in those reports.
- The abstract's list of compiled results omits Lemma L4 and Theorem P. This is optional, since "results on a two-pole belt family" covers P.

**Not checked.** No Lean build or `#check` was run, because the source text and the audit manifests were enough. The proofs and the hand texts were not checked against each other beyond the 116 report's "Do the statements match" section.
