# J13 verdict: PASS. The 2.122 `Occ` witness (F3) and the `Occ`-free docstrings (F1) are compiled and audited

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math (local); Proof Navigator
- **Sent:** 2026-10-06 20:41 MDT
- **Replies to:**
  - Studio Math (local) 17:25 (`cd0fcfc`);
  - the coordinator's J13 request
- **Asks for:** Navigator: record F1 and F3 as done (§3).

## Chronology of the run

- At 17:2x the coordinator relayed that the user now allowed capped local compute (6 cores, 45 minutes per job). This session's permission check refused the run twice. The audit did not route it around.
- The user then said "Go ahead", and started the run in their own terminal at 20:37:12. It used the audit's script `audit/j13/run_j13.sh` (SHA-256 `ed6faa0e…64eccc`) and ended at 20:40:56. The audit read the outputs; they are copied verbatim to `audit/j13/out/`.

**Setup:**
- **Source.** `git archive cd0fcfc` of the Lean folder, a clean tree with no working-tree files.
- **Base.**
  - A copy-on-write clone of the 8299419 olean tree from `~/mathlib4-planemap` (HEAD `bcff6cd`); nothing was written there.
  - The one missing library olean, `SphericalFourContact`, was compiled into the clone first. Its source SHA-256 `499db737…` equals the 8299419 entry in `lean-8299419/SHA256SUMS-copied`, and it compiled with exit 0.
- **Caps.** Every Lean process ran with `ulimit -t 1800`, `nice 10` and `LEAN_NUM_THREADS=6`.

## 1. Results

| Check | Result |
|---|---|
| Commit | `cd0fcfc050d6…` |
| `check.sh`, all 24 modules in order | exit 0, 105 s; linter and deprecation warnings only |
| `shasum -c SHA256SUMS` | 24 OK, exit 0 |
| Escape-hatch grep | no match |
| Axiom sweep, `Conf2122Witness` | 52 constants, `nonstandard: 0` |
| Axiom sweep, `FrameF3` and `RStarSanity` | 5 and 14 constants, `nonstandard: 0` |
| Negative control (`theorem auditPlanted : Witness2122.sphericalMap.Conf2122Free := sorry`, appended to a copy of the witness) | `nonstandard: 1; [(auditPlanted, sorryAx)]`: **caught** |

## 2. Statements, printed by Lean

- `occ_C2122M : C2122M.Occ sphericalMap ![2,10,13,21,14,5,1] ![3,12,4,0]`.
- `occ_C2122P : C2122P.Occ sphericalMap ![13,10,2,1,5,14,21] ![3,0,4,12]`.
- `not_conf2122Free : ¬ sphericalMap.Conf2122Free`.
- `mem_class : 0 < 22 ∧ Connected ∧ Triangulated ∧ (∀ x, 5 ≤ degree x) ∧ NoSep`. These are exactly the hypotheses of `RStarNoSepTri`, as printed.
- An appended `example` combining `not_conf2122Free` and `mem_class` compiled.
- `#print C2122M.Occ` is unchanged from J12: `ring_inj`, `int_inj`, `disj`, `deg = ![6,5,5,5]`, and the 21 `Nx` rotation fields.
  - By hand: the interior labels (3, 12, 4, 0) have degrees (6, 5, 5, 5) in the file's `degT`, so the field matches.
- Axioms of all of these: `[propext, Classical.choice, Quot.sound]`.

**Docstring-only change.** `git diff 22ff272 cd0fcfc` touches only comments in `FrameF3` and `RStarSanity`, plus the module list in `check.sh`. The `RStarFrame`, `DiamondFree`, `Conf2122Free` and `four_color_of_RStarFrame` prints are identical to J12.

## 3. Verdict: PASS

- **F1 (wording): done.** The docstrings say `Occ`-free, and no statement changed.
- **F3 (non-vacuity): done.** RSST 2.122 `Occ` holds in both orientations on a compiled map that satisfies every hypothesis of `RStarNoSepTri`. So `Conf2122Free` excludes a real member of the class, as `DiamondFree` does with the icosahedron.
- **Still open:**
  - The witness graph is also excluded by `DiamondFree`; Studio Math notes 5 diamonds. So it does not separate the two exclusions.
  - The "appears → `Occ`" bridge is open; Studio Math's plan is in §4 of its 17:25 message, not reviewed here.
  - The claim stays "for spherical maps".

**Ledger line, for the Navigator:**
> F1 and F3 closed (J13, audit 20:41): `Conf2122Free` is non-vacuous on the R\* class, by a compiled order-22 witness.

— Independent audit
