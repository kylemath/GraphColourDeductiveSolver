# Frozen challenge statements (Comparator style)

Written by Track C on 7 Oct 2026. Nothing here is committed.

The layout follows the Comparator protocol summarised in `OpenAIMathScan.md` §3. Each challenge is:

- one Lean file that imports only upstream Mathlib modules;
- the definitions its statement uses, inlined into that file;
- a `MainStatement`, followed by `theorem main : MainStatement := by sorry`;
- a JSON config.

## Files

| file | lines | role |
|---|---|---|
| `RStarFrameChallenge.lean` | 281 | Frozen R\* statement for the frame class. It inlines `RotationSystem`, `Fills`, `SphericalMap`, `Triangulated`, `Nx`, `Facial`, `NoSep`, the Kempe notions (`ProperOff`, `Target`, `pairGraph`, `Whole`, `swap`, `KempeStep`), `PureClean`, the four `Occ` structures, `DiamondFree` and `Conf2122Free`. |
| `RStarFrameBridge.lean` | 158 | Proves `mainStatement_iff : RStarFrameChallenge.MainStatement ↔ SimpleGraph.SphericalMap.RStarFrame`. This is the anti-drift check. |
| `FourColorSphericalMapChallenge.lean` | 65 | Frozen statement: every `SphericalMap` is 4-colourable. |
| `FourColorBridge.lean` | 75 | Three theorems, listed below. |
| `RStarFrameChallenge.json`, `FourColorSphericalMapChallenge.json` | | Comparator configs. |
| `check.sh` | | Compiles all four Lean files. |

`FourColorBridge.lean` proves:

- `mainStatement_iff`: the frozen statement is equivalent to `∀ n (M : SimpleGraph.SphericalMap n), M.graph.Colorable 4`.
- `mainStatement_of_RStarFrame`: `RStarFrame → MainStatement`, via `four_color_of_RStarFrame`.
- `mainStatement_of_rStarFrameChallenge`: the frozen R\* statement implies the frozen four-colour statement.

The JSON configs set:

- `permitted_axioms`: `[propext, Quot.sound, Classical.choice]`;
- `definition_names`: `[]`;
- `enable_nanoda`: false.

## How to check

1. Run `StudioMathLean/check.sh <built-checkout> <scratch-dir>` once. This compiles the Studio modules, because the bridges import `FrameF3`.
2. Run `Challenges/check.sh <scratch-dir>`.

What a passing run looks like:

- Each challenge file gives exactly one warning, "declaration uses `sorry`" (for `main`).
- Each bridge theorem prints `[propext, Classical.choice, Quot.sound]`.
- Results on 7 Oct 2026: all four files compile, and all four bridge theorems print exactly those axioms.

The challenge files do not depend on the project library. A probe file importing both challenges reports `Unknown constant SimpleGraph.SphericalMap` and `SimpleGraph.RotationSystem`.

## Faithfulness: where the frozen text differs from the library

The inlined definitions are verbatim copies of the library definitions, except at three points. At each of these, the frozen form is the more transparent one, and the bridge proves equivalence.

1. **Faces.**
   - The library defines `Face` as a quotient of darts by the face-orbit relation, plus an empty face. `Fills` asks for a potential `c : Face → ZMod 2`.
   - The challenge asks instead for a dart function `c` invariant under `faceNext d = next d.symm`.
   - Equivalence uses `Quotient.lift` in one direction and `face_of_face_next` in the other.
2. **`Triangulated`.**
   - The library says `faceLength (faceOf d) = 3`, i.e. the face's dart count.
   - The challenge says `Function.minimalPeriod faceNext d = 3`.
   - Equivalence: `face_length_eq_period`.
3. **`PureClean`.**
   - The library uses an indexed inductive `PurePath` with a length bound.
   - The challenge says `∃ d, Relation.ReflTransGen (KempeStep G r) c d ∧ Target G r d`.
   - Equivalence: induction both ways.

Everything else matches the library definitionally, including the `Classical.decRel` instance used for degrees. The bridge checks the four `Occ` structures field by field (`cases o; constructor <;> assumption`), so a typo in any rotation field would make the bridge fail.

The smallest faithful cut was not needed: the full inlining is 281 lines.

## Caveats

- **No solution modules exist.**
  - `solution_module` in both JSONs names a file that does not exist yet (`Challenges.RStarFrameSolution`, `Challenges.FourColorSphericalMapSolution`).
  - R\* is open, so neither `main` can be proved.
  - Building either solution would be mechanical:
    1. Copy the challenge text verbatim.
    2. Import the library.
    3. Inline the bridge lemmas.
    4. Close `main` with `mainStatement_iff.2 <proof of RStarFrame>`.
  - The bridges cannot be the solution modules themselves: they import the challenge module, so their own `main` would clash.
- **The trusted statement is combinatorial, not topological.** Planarity is the `Fills` condition. A drawing-based statement, as recommended in `OpenAIMathScan.md` §3, would also need the embedding-to-`SphericalMap` bridge, which is not formalised.
- **Not run through Comparator itself.** No `comparator`, `landrun` or `lean4export` is installed here. "Compiles, and the bridge's axioms are standard" is the check that was actually run.
