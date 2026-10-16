# Exploration log (newest first; protocol in EXPLORE-LOOP.md) [exploratory, engine level]

## Round 3 (16 Oct 2026, ~06:25Z): gap G3, is lemma B (7-wheel 5666567 C-reducible) real?

**Question.** E1/E2 (and D1/D2 under R_opt) die only to the cfast C-candidate 5666567. Does a second engine agree?
**Result: yes, two engines now.** `wheeldis/loop/kempe_w7_5666567.py` (+ `.out`) is written from textbook definitions
without reading dfast/cfast/Lean. It reproduces cfast exactly: 66,430 ring classes, 7,372 extend, D-closure 53,690
good and 12,740 bad (fixpoint after 19 levels). It cross-checks its coarsest-partition shortcut against brute force on
600 sampled classes (0 disagreements).
- X = {I0-I1, I0-I3, R2-I3} (|X| = 3; bigwheels.txt indexing) is admissible (no loop), and all 2,668 classes that
  extend after contraction are good. The |X| = 4 variant with R0-I2 added gives the same 2,668 classes and also works.
- cfast found 437 working X of size <= 4 on the defect-indexed copy, so the verdict does not hang on one X.
**Next.** Lean, as for CWheels.lean (Job 21). This wheel is cheap at ring 13. Then lemma B counts at the programme's standard.

## Round 1 (16 Oct 2026, 05:15-06:10Z, cloud thread "pace"): gap G1, what kills the defects near 7s?

**Question.** D1-D3 avoid R_opt but die to B-fixed configurations. Is there one simple family behind that?
**Guess.** Yes: 7s with many five-neighbours. D3's ten 7s have 4,4,3,3,3,3,2,2,1,1 fives.
**Would change the plan if:** assuming that family reducible leaves no K <= 4 defect. Then G1 reduces to one lemma
instead of a 5·10^5 CPU-h B-fixed enumeration.

**Probe 1a, sample** (`wheeldis/loop/bfsample.py`). Took every 7 in the R_opt-free K = 3 patches of charge >= 0 (all
centres; `bin/defectc ... 3 0`: 171 + 337 + 1,056 patches). Built every B-fixed configuration (u + S + all links of
S at exact degree, |S| >= 2). Ran dfast on 25 random ones per class at ring <= 14.

| fives at u | D fraction for \|S\| = 2 | for \|S\| = 3 | for \|S\| = 4 | for \|S\| = 5 |
|---|---|---|---|---|
| 2 | 8/25 | | | |
| 3 | 14/25 | 19/25 | | |
| 4 | 12/25 | 22/25 | 24/25 | |
| 5 | 15/25 | 22/25 | 21/25 | 24/25 |

**Probe 1b, per instance** (`loop/bfinst.py`, ring <= 15, largest S first, stop at the first D). This asks whether
every 7 with >= 3 fives has some D B-fixed configuration. After 150 distinct instances:

| fives at u | instances | some B-fixed config D at ring <= 15 |
|---|---|---|
| 3 | 90 | 81 (9 not) |
| 4 | 46 | 46 |
| 5 | 14 | 14 |

**Probe 1c, conditional defect search** (`loop/mktables.py` marks every 7-wheel with >= T fives as bad, then
`bin/defectc`, then `defect_check2.py` against the existing R_opt registry; 600 s cap per run):

| assumed reducible | K = 3 (complete, centres 5/6/7) | K = 4 (partial, capped) | survivors of R_opt |
|---|---|---|---|
| 7 with >= 3 fives | 2 / 22 / 0 candidates | c5 47, c6 107, c7 1,092 | **only E1 and E2** |
| 7 with >= 4 fives | 4 / 30 / 1 | running | none at K = 3 |

E1 and E2 are the two defects that die only to the 7-wheel C-candidate 5666567 (cfast, |X| = 4, triad).

**Reading.**
- Under (A) "every 7 with >= 3 five-neighbours carries a reducible configuration" and (B) "5666567 is C-reducible",
  no K <= 4 defect found so far survives. The K = 4 searches are partial.
- (A) holds on every 7 with 4 or 5 fives sampled (60/60). For exactly 3 fives it holds 81/90. The 9 misses are the
  next round.
- So G1 now looks like two lemmas, not an enumeration. H7b and Studio Job 28 (complete runs) are the confirmation.

**Next rounds.**
- R2: the 9 three-five misses. Do C, larger S with B >= 8 fixed, or ring 16 (dfast18) kill them?
- R3 (G3): an independent closure for 5666567, as abec3fca did for w66666.
- R4 (G2): forbidden-pattern LP with (A) as patterns at d = 7, to see whether a rule reaches t* <= 0.
