# Exploration log (newest first; protocol in EXPLORE-LOOP.md) [exploratory, engine level]

## Rounds 4-5 (16 Oct 2026, 07:40-08:50Z): stepped up, four parallel streams

Kyle asked for more effort, so four gaps ran at once: three workers plus this thread. Each stream has a FINDINGS.md
under `wheeldis/loop/`.

**R (G2, rules; `loop/rules/FINDINGS.md`, LP only).**
- **Question.** Can a richer rule class beat the 5/17 bound at d = 7?
- **Answer.** No. The 5/17 dual certificate rests on two receiver arrangements, R1 (link 5567576, s 5755556) and
  R2 (link 5576576, s 5756656), with weights 1:2.
  - Their shared 7s are mirror images over the union of both arrangements.
  - So no rule that sees only that union can separate them. Classes (b) and (c) both stay at 5/17.
  - The lever is reducibility of R1 and R2, not the rule class. This corrects README §6.1's reading.
- On the HARD d = 7 rows, class (c) lowers the floor from 11/39 to 1/5. Its certificate uses A1402, A1308 and A2581.

**R follow-up: are the certificate arrangements reducible?** (`loop/cert_bf.py`, `loop/rules/cert_bf*.{txt,out}`)
- **Yes, for four of the five.** Every B-fixed S was built and run through dfast (24 configurations, rings 11-16).

| arrangement | B-fixed S that are D (ring) | not D |
|---|---|---|
| R1 | (0,4) r12, (1,4) r13, (0,1,4) r13 | (0,1) r11 |
| R2 | (0,4) r13, (0,1,4) r15 | (0,1) r12, (1,4) r15 |
| A1402 | (0,1,4) r15 | 3 others |
| A2581 | (0,2,5) r14 | 3 others |
| A1308 | none of 7 tested | (0,1,4) at ring 16 pending |

- So the 5/17 certificate falls once these configurations are forbidden, and so does most of the 1/5 one.
- Job 28 did not see this: it tries the smallest-ring S first, which is (0,1) here and is not D. It should try the
  largest S first.

**A (G1, lemma A; `loop/lemmaA/FINDINGS.md`).**
- **Question.** Is lemma A ("a 7 with >= k fives carries a reducible B-fixed configuration") true as a finite
  statement over every neighbourhood?
- **Answer. No, not as a blanket lemma.**

| case | D at ring <= 14 | rest |
|---|---|---|
| k = 5, degrees <= 7 | 252 of 291 | 39 misses, all on link 5557557, with untested ring 15-16 candidates |
| k = 4, outer 8 / 9+ allowed | ~3% | candidates mostly at ring >= 17, ~10^6 CPU-h |
| k = 3 | 290 of 421 instances | 87 with none at ring <= 15 |

- Round 1's 186/186 came from 6-sea defect patches, whose neighbourhoods are mostly 6s.
- So K = 2 stays defect- and LP-driven, as in Job 28.
- By-product: 29 of 40 k = 5 hits reduce to one ring-9 kernel. It is u = 7 with fives at w0, w1, w2, and
  s0 = 5, s1 = 7, s2 = 5. It is cheap to put in Lean.

**E (G4/G7, appears; `loop/appears/FINDINGS.md`).**
- **Is "non-simple ring ⇒ killed" in defect_check2 sound?** Not as a rule. A census graph (p25#6000) has an
  unrepairable chord and no short separating cycle.
- **Does it ever fire?** Not on a 1/20 sample of the 418,551 K <= 4 candidates: all 352,886 non-simple rings there
  were repaired by the fill. A full rerun is in progress.
- **B2 for receiver-centred configurations.** It extends to the interior (hand sketch).
- **Rings.** In 38,872 census graphs, 11,187 (u, S) rings stay non-simple after the fill. They are chords and folds;
  there are no pinches.
- So "appears" needs one of two things: PinchWalk extended to arcs of length 1-2, or the plan listing the filled
  variants.

**K = 5 defects (G8; this thread; `loop/defectr.cpp`, `loop/defectr2.cpp`, `loop/k5hunt.sh`, `loop/export_keys.py`).**
- **New tools.**
  - `defectr` is a randomised `defectc`.
  - `defectr2` also prunes inside the DFS whenever a 7 has a reducible receiver-centred key (8,827 keys at d = 7).
  - Validation at K = 3: the pruning removes 3,840 leaves; defect_check2 kills 3,833 of them and leaves 7 open. The 7
    are pinched cases, which the key test ignores.
- **Without pruning.** About 950 K = 5 candidates were sampled. All were killed by plain receiver-centred
  configurations.
- **With pruning.** About 660 randomised seeds (centres 5 and 7, strict tables) produced 0 R_opt survivors.
- **Guided.** All 15 extensions of D3 to K = 5 are killed.
- **Conditional on A3.** Complete K = 5 runs (centres 5 and 6, 45 min cap) have produced 0 leaves so far.
- **Caveat.** These are samples, not a complete search. All defect searches use degrees 5-7 only, so clusters with a
  vertex of degree >= 8 are untested (new gap G9).

**What changes.**
1. Give Job 28 the B-fixed sets of R1, R2, A1402 and A2581, which are D now, as forbidden patterns and re-solve. Order
   gen28 variants largest S first.
2. Drop "K = 2 = lemma A" from the plan wording. Keep the ring-9 kernel as a Lean candidate.
3. In defect_check2, make an unrepaired non-simple ring "open" instead of "killed".

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
