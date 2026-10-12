# Audit J14: the 7–8 Oct Lean modules and the frozen challenges

**Verdict: PASS, with three wording notes for the paper. None of them blocks the PASS.**

- **From:** Independent audit (a fresh session that wrote none of this code)
- **Date:** 2026-10-08, run 09:0x–09:30 MDT on the Mac Studio
- **Scope:**
  - nine modules under `StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`: `FrameNoFrozen`, `FrameScope`, `FrameWit22Map`, `FrameWit22`, `QuarterLockParity`, `ChainCount`, `ChainMod4`, `TutteSides`, `ChainF`;
  - the four `Challenges/` Lean files and their two JSON configs;
  - the paper's (`docs/reports/VHE-paper/main.tex`) prose for every result labelled \lab{built}$^\dagger$.
- **Procedure:** J12/J13 (`backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit-8/run_j12.sh`, `audit/j13/run_j13.sh`), extended in two ways:
  - a check that each statement is non-vacuous on an actual library map;
  - a review of how the challenges are bridged to the library.
- **Commit:** `ad0fd00b7ce8ade05024bdc5df76fd6ca0c3cdd8` (`main`). `git status` reports no changes in `StudioMathLean/`, `Challenges/` or the paper, so the working tree that was compiled is that commit.
- **Base:** `~/mathlib4-planemap-build`, at Mathlib `300d0e5` with the PlaneMap files added and no other tracked file modified (`git diff --stat` is empty), Lean `v4.35.0-rc3`.
- **What this audit did not touch:** no Lean file, paper file or commit was modified. All outputs are in `out/`. The audit's own Lean files are `NonVacuity.lean` and `ChallengeNonVacuity.lean`; they are not part of the library.

## 1. Build and axiom checks

| Check | Result |
|---|---|
| Clean rebuild with `StudioMathLean/check.sh` into a fresh scratch directory (copy-on-write clone of the base `.olean` tree; all 91 Studio modules compiled from source, in order, `nice -n 10`) | **exit 0**; 91 `==` lines; 0 errors; 0 `sorry` warnings; 15 min 41 s wall (`out/check-sh.txt`, `out/check-sh-time.txt`) |
| `Challenges/check.sh` on the same scratch directory | **exit 0**. Exactly two warnings, the expected `declaration uses 'sorry'` for `RStarFrameChallenge.main` and for `FourColorSphericalMapChallenge.main` (`out/challenges-check-sh.txt`) |
| Every `#print axioms` line in both logs (330 + 4), parsed by script, wrapped lines included | every set ⊆ {`propext`, `Classical.choice`, `Quot.sound`}; no `sorryAx`, `Lean.ofReduceBool` or `Lean.trustCompiler` |
| `shasum -a 256 -c SHA256SUMS` in `StudioMathLean/` | 40 OK, exit 0. All nine audited modules are listed in it (`out/shasum-c.txt`) |
| Escape-hatch grep, whole folder: `sorry\|admit\|native_decide\|axiom\|unsafe\|implemented_by\|extern\|opaque\|ofReduceBool\|trustCompiler` | 47 matches, all in docstrings ("sorry-free, no new axioms", "the sphere axiom `fills`") (`out/grep-all.txt`) |
| Extended grep over the 13 files in scope (adds `csimp`, `debug`, `elab`, `macro`, `syntax`, `run_cmd`, `#eval`, `initialize`, `instance`, `local`, `set_option`) | Nothing affects soundness (`out/grep-scope.txt`):<br>• `set_option maxHeartbeats 0` / `maxRecDepth 8192` in `FrameWit22Map`, and `synthInstance.maxSize 1000` in `QuarterLockParity`: resource limits only;<br>• two instances: `DecidableRel` on the concrete witness graph (through a decided `adj_iff`), and `Fintype (SE G τ)` in `TutteSides`;<br>• `Classical.decRel` for degrees in the challenge;<br>• the two challenge `main`s are `by sorry` by design. |
| Per-module audit copies (J12 procedure: each source, plus the statement prints of §2, plus the per-file axiom sweep), `ulimit -t 1800` (`run_audit.sh`, `rerun2.sh`) | see the table below |
| Negative control: a planted `theorem auditPlanted : (1:ℕ) = 2 := sorry` in a copy of `ChainF` | **caught**: `nonstandard: 1; [(auditPlanted, sorryAx)]` |

Per-module sweep (`out/audit_*.out`):

| module | exit | errors | sorry warnings | sweep | verdict |
|---|---|---|---|---|---|
| FrameNoFrozen | 0 | 0 | 0 | 5 constants, nonstandard 0 | PASS |
| FrameScope | 0 | 0 | 0 | 14 constants, nonstandard 0 | PASS |
| FrameWit22Map | 0 | 0 | 0 | 45 constants, nonstandard 0 | PASS |
| FrameWit22 | 0 | 0 | 0 | 10 constants, nonstandard 0 | PASS |
| QuarterLockParity | 0 | 0 | 0 | 59 constants, nonstandard 0 | PASS |
| ChainCount | 0 | 0 | 0 | 22 constants, nonstandard 0 | PASS |
| ChainMod4 | 0 | 0 | 0 | 66 constants, nonstandard 0 | PASS |
| TutteSides | 0 | 0 | 0 | 45 constants, nonstandard 0 | PASS |
| ChainF | 0 | 0 | 0 | 27 constants, nonstandard 0 | PASS |
| RStarFrameBridge | 0 | 0 | 0 | 25 constants, nonstandard 0 | PASS |
| FourColorBridge | 0 | 0 | 0 | 7 constants, nonstandard 0 | PASS |
| RStarFrameChallenge | 0 | 0 | 1 (`main`) | 169 constants, nonstandard 1 = `(main, sorryAx)` | as designed |
| FourColorSphericalMapChallenge | 0 | 0 | 1 (`main`) | 36 constants, nonstandard 1 = `(main, sorryAx)` | as designed |
| ChainF_negcontrol | 0 | 0 | 1 | 28 constants, nonstandard 1 | control caught |

The first attempt at the `QuarterLockParity` and `ChainMod4` copies stopped at the audit's own appended `#print` lines, which named `VacancyShortFill.*` without the `SimpleGraph.` prefix. Both copies were rerun with the names corrected (`rerun2.sh`, recorded in `out/times.txt`). The module sources compiled cleanly in both runs.

File hashes (sha256, first 16 hex digits):

| file | hash |
|---|---|
| FrameNoFrozen | `0ea9c2605a44ef69` |
| FrameScope | `0e73057796f87645` |
| FrameWit22Map | `4a685445e2d43287` |
| FrameWit22 | `4200c810f91d726b` |
| QuarterLockParity | `956a1956aad1d9b0` |
| ChainCount | `ba3184b2c4f2e27d` |
| ChainMod4 | `8c9cc08879d56c9b` |
| TutteSides | `278a9ee9f8133c36` |
| ChainF | `6d87b43da336a860` |
| RStarFrameChallenge | `7238b76777f6a3b9` |
| RStarFrameBridge | `b9c337b701b970be` |
| FourColorSphericalMapChallenge | `0f3ee0d1c250d84b` |
| FourColorBridge | `2ac532501066ce98` |

## 2. Statement audit: Lean against the paper's prose

The audit read each statement and every definition it depends on in the source, and checked them against the compiled prints in `out/audit_*.out`:
- `Pent`, `RepeatAt`, `Lock1`, `Lock2`, `DoublyLocked`, `DLState`, `piMove`, `kcomp`;
- `boundaryCard`, `oddCount`, `pairGraph`, `Active`, `ProperOff`, `Whole`, `Triangulated`;
- `chainCount`, `nChains`, `RigidAt`, `ChainParityLaw`;
- `fxor`, `isCW`, `FaceAvoids`, `cwAt`, `cwDarts`, `cwCount`, `linkInner`, `LinkBalanced`, `handB`, `handS`, `StarHyp`;
- `ChainFormulaF`, `ConjectureF`, `chainSpace`, `gammaM`, `NoFrozenFrame`, `LinkTipsClean`, `RStarFrame`.

The dictionary is the paper's §5 frame. The link reads (α, β, α, γ, δ) at x0..x4. Lean's frame j has (α, μ, A, B) = (c x_j, c x_{j+1}, c x_{j+3}, c x_{j+4}), so μ = β, A = γ and B = δ.

| # | Theorem (paper location) | Verdict | Notes |
|---|---|---|---|
| 1 | `rStarFrame_of_no_allDL_orbit`, `four_color_of_no_allDL_orbit_frame` (§3, "Frozen orbits") | **PASS** | `NoFrozenFrame` uses exactly the seven `RStarFrame` hypotheses. Its conclusion is: ∃ v of degree 5, ∃ `Pent` at v, and every proper colouring of T−v has some forward π-iterate that is not `DLState`. On a finite class permuted by π (`piMove_bijOn_class`, already compiled), the forward orbit is the whole orbit, so this is the prose "no π-orbit consists only of doubly locked states". The conclusions are `RStarFrame` and 4-colourability of every `SphericalMap`. Standard axioms. |
| 2 | `no_555_run`, `no_565_run` (§3, "Scope") | **PASS** | Hypotheses: `Triangulated`, `NoSep`, `DiamondFree` (resp. `Conf2122Free`), deg h = 5, and `LinkTipsClean P j`. Minimum degree 5 is not assumed, as the paper says. Conclusion: not all of the degrees (5,5,5) (resp. (5,6,5)) at x_j, x_{j+1}, x_{j+2}. Non-vacuous: `LinkTipsClean P j` holds for all j at vertex 0 of the frame-class witness, and `no_555_run` is instantiated there (`NonVacuity.lean`, `tips`, `no555_inst`). |
| 3 | `frameClass_nonempty` (§3) | **PASS** | Its statement has exactly the seven hypotheses of `RStarFrame`, in the same order (compare the prints). The order-22 witness is a genuine `SphericalMap`: `Fills` holds by a linear certificate checked by kernel `decide`, with no `native_decide`, and `Triangulated` holds by the face-period table. `DiamondFree` and `Conf2122Free` use a sound necessary condition: every `Occ` has an edge int0~int2 with two distinct common neighbours int1, int3 of the right degrees, extracted from the `Occ`'s own `Nx` fields, and `decide` shows that no such quadruple exists. |
| 4 | `lock2_iff_odd_boundary`, `lock2_iff_odd_oddCount`, `lock1_iff_odd_boundary`, `lock1_iff_odd_oddCount`, `alphaMu_odd_boundary`, `alphaMu_odd_oddCount` (Thm LP) | **PASS** | `Lock2` (the {μ,B}-path from x_{j+1} to x_{j+4}, the paper's L2) holds iff odd `boundaryCard M.graph (kcomp … α A x_{j+2})`, i.e. the paper's K_{αγ}(x2). `Lock1` (L1) corresponds to K_{αδ}(x2), and K_{αβ}(x2) always has odd boundary. `boundaryCard` counts darts of T (not T−v) with exactly one end in K, so "edges to v included" is exact. `oddCount` uses degree in T. Hypotheses: `Triangulated`, `Pent`, `ProperOff`, `RepeatAt` (unfilled). The surface-general part (`parity_alphaA/B/Mu`) assumes only a face successor with `(φ d).fst = d.snd`, φ³ = 1 and the star hypothesis, which matches "every oriented triangulated surface, no planarity". Instantiated at a genuine doubly locked state (`lp_inst`). |
| 5 | `eight_le_nChains`, `rigidAt_iff` (§5, "Chain counts") | **PASS** | `nChains` sums `chainCount` (components of the {p,q}-graph of T−h that contain an active vertex) over the six unordered pairs. `RigidAt` = `DoublyLocked` with counts (αμ, AB, αA, μB, αB, μA) = (1,1,2,1,2,1), i.e. the paper's αβ, γδ, αγ, βδ, αδ, βγ = 1,1,2,1,2,1. Both theorems assume only `Triangulated` + `Pent` + `DoublyLocked`, which is weaker than the prose (`ProperOff` is not even needed). Instantiated (`eight_inst`). |
| 6 | `lemmaW`, `cw_piMove` (§5, after Thm F) | **PASS (statement); wording note W1** | `cwCount` = the number of faces avoiding h whose Tait triple (c u⊕c w, c w⊕c z, c z⊕c u), read along `faceNext`, is a cyclic shift of (1,2,3). `fxor` is XOR on Fin 4 ≅ Z₂², which matches the prose. `lemmaW` is surface-general but carries a hypothesis `LinkBalanced` (boundary term β = 0). `lemmaW_linkFree` gives Δcw ≡ 0 for link-free swaps on any triangulated rotation system. `cw_piMove` (Δcw ≡ 2 at π of a DL state) is stated and proved **only on a `SphericalMap`**: it uses sphere duality (`lock2_iff_not_reach_alphaA`) to show x_j ∉ K. See W1. |
| 7 | `conjectureF` (Thm F) | **PASS** | `ConjectureF`: ∀ n, M, h, P : `Pent`, `Triangulated` → no isolated vertex → `ChainFormulaF`. That is, ∀ c, j with `ProperOff` and `RepeatAt`: 2·N ≡ cw + (n−1) − [`handS`] + 2([L1]+[L2]) in ZMod 4, where n is the number of vertices of M (h included). This matches the prose exactly. `handS` reads η along the face orientation: `handB` if `faceNext (h→x0)` ends at x1, its negation otherwise. Reversing the link swaps A and B, and because α⊕μ, α⊕A, α⊕B are the three distinct non-zero elements, this negates the cyclic-shift test, so `handS` is the paper's η. Connectivity is not assumed (γ cancels). Instantiated at a genuine unfilled (in fact doubly locked) state of the witness (`F_inst`, `conjF_inst`). |
| 8 | `tutte_sides`, `euler_tri` (cited inside Thm F's paragraph) | **PASS** | `tutte_sides`: `Triangulated`, no isolated vertex, a dart `d0`, and every face has a corner off τ, give \|S_τ\| + #τ-chains + γ = #τ + #(¬τ)-chains. `euler_tri`: \|E\| + 6γ = 3n. Planarity enters only through `Fills` (`face_side`). This matches "no topology beyond the library's planarity condition". |
| 9 | `chainParityLaw_sphere` (Thm law) | **PASS** | `ChainParityLaw M P`: ∀ c with `ProperOff` and `DLState`, Odd(N(πc)+N(c)) ↔ `DLState (πc)`. Hypotheses: `Triangulated`, no isolated vertex, `Pent`, which is exactly the prose. Non-vacuous: instantiated at the explicit doubly locked state below (`law_inst`). Script corroboration: N(c) = N(πc) = 12 there, the sum is even, and πc is not DL, consistent with the law. |
| 10 | `rigid_isolation` (§5) | **PASS; wording note W2** | `¬ RigidAt P (π c) j'` for every j', given `ProperOff c` and `RigidAt P c j`. This is the prose's first clause. The follow-on "so no Kempe class consists only of rigid states" is a one-line corollary with `piMove_bijOn_class`, and is not itself a compiled statement. Rigid states were not exhibited in Lean: proving exact chain counts of a concrete state was out of scope. The hypothesis is the conjunction `DoublyLocked` + six counts, and `DoublyLocked` is shown satisfiable. |
| 11 | `remark7` (§5) | **PASS; note W3** | Hypotheses: `ProperOff c`, `RepeatAt P c j` (c unfilled, frame j), and X a `Whole` {p,q}-component (p ≠ q, active seed) containing no x_i. Conclusion: (N + [L1] + [L2]) mod 2 is the same for c and for `swap c p q X`, with locks read in the same frame j (the swap fixes the link). The paper's "a swap of a component that meets no link vertex" assumes an unfilled state implicitly, from the section's setup. |
| 12 | `mainStatement_iff` (both bridges), `mainStatement_of_RStarFrame`, `mainStatement_of_rStarFrameChallenge` (§3) | **PASS** | See §4. |

## 3. Non-vacuity: hypotheses that cannot be met?

The question was whether `Triangulated` + no isolated vertex + `Pent` (+ `RepeatAt` / `DoublyLocked`) can be unsatisfiable, which would make Theorems F, law, LP and Lemma 3 trivially true. They can be met. `NonVacuity.lean` compiles with exit 0, and every instance prints `[propext, Classical.choice, Quot.sound]`. It works on the frame-class witness `FrameWit22.sphericalMap` (order 22):

- `P : Pent sphericalMap.graph 0` with link `![1,2,3,4,5]`, proved by `decide`.
- `hiso`: no isolated vertex. `deg0`: vertex 0 has degree 5.
- `c = ![0,3,2,1,0,1,0,1,0,2,3,1,2,3,1,3,2,3,0,2,0,0]`:
  - `ProperOff` and `RepeatAt P c 2` hold by `decide`;
  - `Lock1` holds by the explicit {0,3}-path 4-10-18-17-21-15-6-1;
  - `Lock2` holds by the explicit {0,2}-path 4-12-20-19-18-9-8-2;
  - so `DoublyLocked P c 2`. The state was found by `finddl22.py` and the paths by `paths.py`. Lean rechecks every edge and colour.
- At this state Lean instantiates:
  - `chainFormulaF` and `conjectureF`;
  - `chainParityLaw_sphere`;
  - `eight_le_nChains`;
  - `lock2_iff_odd_boundary`;
  - `cw_piMove`.
- `LinkTipsClean P j` holds for all j, and `no_555_run` is instantiated.

A side observation: a search over all proper colourings of the icosahedron at hole 0 found no doubly locked state at all, so the icosahedron cannot serve as a DL witness. The order-22 frame member can.

`ChallengeNonVacuity.lean` (exit 0, standard axioms) shows two more things:
- The frozen `RStarFrameChallenge.MainStatement` has satisfiable hypotheses. The library witness, transported by `ofLib` and the bridge lemmas, meets all seven of the frozen predicates.
- The frozen four-colour statement quantifies over a non-empty type.

## 4. Challenge bridges: no definitional escape hatch

| Item | Verdict | Notes |
|---|---|---|
| The frozen files import only upstream Mathlib | PASS | Imports: `SimpleGraph.Dart`, `Finite`, `Coloring.Vertex`, `Connectivity.Connected`, `ZMod.Basic`, `Dynamics.PeriodicPts.Defs`, `Logic.Relation`, `Fin.VecNotation`. The base checkout has no modified tracked upstream file. |
| The frozen text says what the paper says | PASS | The audit read it line by line:<br>• `SphericalMap` = graph + rotation (single cycle at each vertex) + `Fills`, i.e. every even edge set is a coboundary of a `faceNext`-invariant dart potential;<br>• `Triangulated` = minimal period of `faceNext` is 3;<br>• `NoSep` = every triangle is facial;<br>• `PureClean` = every `ProperOff` colouring reaches `Target` by `ReflTransGen KempeStep`, where `KempeStep` swaps one `Whole` component of the {a,b}-graph of T−h with a ≠ b;<br>• the four `Occ` structures carry injectivity, disjointness, degrees and the full rotation at each interior vertex;<br>• the four-colour `MainStatement` = ∀ n M, `M.graph.Colorable 4` with Mathlib's `Colorable`. |
| `RStarFrameBridge.mainStatement_iff : MainStatement ↔ RStarFrame` | PASS | A genuine iff, both directions, on the *same* graph and rotation (`toLib`, `ofLib`, with `ofLib_toLib = rfl`). Every predicate is related by a proved lemma:<br>• `triangulated_iff`, via `face_length_eq_period`;<br>• `noSep_iff`, `degree_eq` and `kempeStep_iff`, by `Iff.rfl`/`rfl`, so the challenge's `Classical.decRel` degree instance agrees definitionally with the library's;<br>• `pureClean_iff`, by induction both ways between `PurePath` and `ReflTransGen`;<br>• the four `Occ` iffs field by field, both directions;<br>• `fills_toLib`/`fills_ofLib`, by quotient lift and `face_of_face_next`.<br>Because the result is an iff proved in Lean, a drift in either text would break the build. Nothing has to be trusted beyond the frozen text itself. |
| `FourColorBridge.mainStatement_iff` | PASS | Frozen statement ↔ `∀ n (M : SimpleGraph.SphericalMap n), M.graph.Colorable 4`, through the same graph and rotation. |
| `mainStatement_of_RStarFrame`, `mainStatement_of_rStarFrameChallenge` | PASS | These compose `four_color_of_RStarFrame` (audited in J12) with the two iffs. Standard axioms. |
| Comparator configs | PASS, with the caveats already disclosed | `permitted_axioms` = the standard three. `solution_module` names files that do not exist, `definition_names` is empty, and Comparator / lean4export / landrun were not run. `Challenges/README.md` and the paper both say so. Neither challenge is a proof of anything: both `main`s are `sorry`, and that is by design. |

## 5. Wording notes for the paper (non-blocking)

- **W1 (§5, the paragraph after Thm F).** The paper says lemma W is "valid on every oriented triangulated surface" and that it covers π at a doubly locked state, citing `lemmaW` and `cw_piMove`. In Lean the surface-general statements are:
  - `lemmaW`, under the link-balance hypothesis `LinkBalanced`;
  - `lemmaW_linkFree`, for link-free swaps.

  The π statement `cw_piMove` is compiled **on `SphericalMap` only**: its proof uses the sphere duality (D2) to place x_j outside the swapped component. Suggested text: "a local lemma W (`lemmaW`, `lemmaW_linkFree`), valid on every oriented triangulated surface, says that every swap of a component meeting no link vertex leaves cw unchanged mod 4; on the sphere, π at a doubly locked state changes cw by 2 mod 4 (`cw_piMove`)". Alternatively, keep the current text and cite `lemmaW_linkFree` as well.
- **W2 (§5, rigid isolation).** "so no Kempe class consists only of rigid states" is a trivial corollary (`rigid_isolation` + `piMove_bijOn_class`), but it is not itself a named compiled theorem. It is acceptable as written. A stricter reading would mark that clause \lab{hand}, or add the two-line corollary to `ChainF.lean`.
- **W3 (§5, Remark 7).** The Lean statement assumes the state is unfilled (`RepeatAt`, needed for L1 and L2 to be defined) and reads the locks in the same frame before and after. Both are implicit in the section's setup. Optional: write "at an unfilled state".

Other prose checks, all accurate:
- the scope sentences ("specific to the sphere", "minimum degree 5 is not needed", "no topology beyond `Fills`");
- the status-table footnote's "91 of 91 modules, standard axioms" (reproduced here independently);
- "SHA256SUMS 40/40" in `CoordinatorPlan.md` (reproduced here).

## 6. Verdict and ledger line

**PASS.** The nine 7–8 Oct modules and the four challenge files rebuild from scratch with exit 0, with no `sorry` outside the two intended challenge `main`s. Every axiom set is within {`propext`, `Classical.choice`, `Quot.sound`}, the planted control is caught, and the statements say what the paper says (wording notes W1–W3 aside). The hypotheses of Thm F, the chain-parity law, Lemma 3, lock parity and `no_555_run` are met by an actual frame-class `SphericalMap` at a doubly locked state. The bridges pin both frozen statements to the library by proved iffs.

**Suggested ledger line (for the Navigator):**
> Compiled and audited (J14, 8 Oct): `NoFrozenFrame → RStarFrame → 4CT for spherical maps`; frame class non-empty (order 22); `no_555_run`/`no_565_run`; lock parity (Thm LP); Lemma 3 (`eight_le_nChains`, `rigidAt_iff`); Conjecture F (`conjectureF`, via `tutte_sides`/`euler_tri`); chain-parity law; rigid isolation; Remark 7; frozen R\* and 4CT challenges with proved anti-drift bridges. All are on triangulated `SphericalMap`s (combinatorial; the embedding bridge is not formalised). R\*, LPC, NRC and N1 stay open.

**Paper:** the \lab{built}$^\dagger$ labels on these items can become \lab{compiled} once the Navigator records the line. W1 should be applied in the same edit.

## Files

- `run_audit.sh`, `rerun2.sh`: the audit's per-module run (J12 procedure).
- `NonVacuity.lean`, `ChallengeNonVacuity.lean`: the audit's non-vacuity checks.
- `finddl22.py`, `paths.py`, `chains.py`: search for the DL state, its Kempe paths, and the chain-count corroboration (any Python 3).
- `out/`:
  - `check-sh.txt`, `challenges-check-sh.txt`, `check-sh-time.txt`;
  - `shasum-c.txt`, `grep-all.txt`, `grep-scope.txt`;
  - `audit_*.out`, `NonVacuity.out`, `ChallengeNonVacuity.out`, `times.txt`.

To reproduce:
1. `StudioMathLean/check.sh ~/mathlib4-planemap-build <fresh-dir>`
2. `Challenges/check.sh <fresh-dir>`
3. Edit `SP`/`W` in `run_audit.sh` to point at `<fresh-dir>`, then run it.
