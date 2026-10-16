# Exploration log (newest first; protocol in EXPLORE-LOOP.md) [exploratory, engine level]

## Round 13 (16 Oct 2026, 14:15Z-): receiver-free windows with a big link vertex (the 3/11 family)

**Pre-registered 14:15Z, before any build.**
- **Family.** The d = 7 arrangements tight at a 3/11-style optimum. These are the tight rows of my round-9 runs
  (`hr1_base`, `hr1_long`, `hr1_or1`) and the certificate receivers of Studio's rounds 9-11.
- **Configurations.** Like round 7's `ufree.py`, but S may contain fives whose non-u neighbours include link bigs:
  - S + N(S) - u, with 7/8 at exact degree and u on the ring with its degree free;
  - S has 2-4 fives in an arc of at most 5 link positions;
  - one D verdict forbids the window at every d = 7..17.
- **H-E7.** Windows of this kind that are D at ring <= 15 forbid at least half of the tight d = 7 arrangements.
- **Kill.** Under 10%.
- **Guess.** About 30%: the 575 windows with every s = 6 die, and the ones with s = 5 next to the 7 do not.

## Round 12 (16 Oct 2026, 13:50-14:10Z): H-AV, pair averaging between adjacent bigs

**Pre-registration.** Long Table's message of 13:47Z: pair rows charge(u) + charge(v) <= 2t take t* below 3/11;
kill if t* stays >= 3/11. I added no guess before computing.

**Result: H-AV dies, exactly for the pair-row model.** Details in `wheeldis/loop/av/FINDINGS.md`.
- Studio's round-11 certificate (`out/wlp3_j28_11.txt`) has two receivers, 5756575/6565666 and 5765756/5566666.
  Each can sit next to a consistent copy of itself (`pairs.py`).
- So the same dual combination, written with pair rows, certifies t >= 3/11 in the pair model.
- The same holds for Studio's round 10 and for the explore oracle certificate (`certpair.py`).
- This does not settle transfers that depend on both 2-balls (class b): the self-pair edge is oriented.

**Reading.** The 3/11 plateau is a family, the way 2/7 was lone fives. In the current pair every five is shared with
a link 7 (senders 56677 / 66677 / 56776). The proposed attack is the lone-five playbook: count the family, then use
edge-centred configurations (two adjacent 7s with their common fives).

## Round 11 (16 Oct 2026, 12:40Z-): binder coverage with degree 8 and deeper defects

**K-cap (H-K), withdrawn before any run.**
- The coordinator proposed forbidding arrangements with more than K letters >= 7.
- That is not sound: no lemma bounds the bigs in a receiver's 2-ball, and round 10 shows that dense arrangements
  complete to locally consistent defects.
- It would also delete 559 of the 562 tight rows at the 33/119 optimum. Only 3 have <= 2 bigs.

**Pre-registered 12:42Z.**
- **Binders.** The 4 that `b7f.out` does not forbid: 5575576/6666656, 5765575/7565777, 5567576/6755556 and
  5765756/5556666.
- **Question.** Do they complete to positive isolated defects that survive R_opt+, either at K = 4 with letter 8,
  or at K = 5 (capped)?
- **H-B8.** Every completion found dies to R_opt+.
- **Kill.** A completion survives with every configuration tested.
- **Guess.** The letter-8 K = 4 searches finish under the 20-minute cap for at most 2 of the 4. K = 5 is far from
  complete. Everything found dies, mostly at the centre.

**Round 11 result (13:46Z).** Details in `wheeldis/loop/b7/FINDINGS.md`.
- **K = 4 with letter 8** (20-minute cap): 1,634 leaves, complete for 5575576. All are killed by the existing
  registry, every one by a D, and they stay killed with `strict7`.
- **K = 5, letters 5-7** (10-minute cap): 423,160 leaves.
  - Checked: all of the two small sets and a 1/50 or 1/20 sample of the two large ones, 10,309 leaves in total.
  - All are killed, after 452 new dfast tests at ring <= 14 (216 D).
- **H-B8 survives** (the K = 5 part is sampled).
- **Guess check.** Only 1 of the 4 letter-8 searches finished, not "at most 2". Kills were mostly at the centre in
  round 10; I did not re-split them here.

## Round 10 (16 Oct 2026, 12:30Z-): do the d = 7 LP binders sit inside an isolated defect? (coordinator's suggestion)

**Pre-registered 12:30Z, before any matching.**
- **Binders.** 7 arrangements at d = 7: the 5 from the 33/119 baseline certificate (`wlp3_hr1_base.txt`) and the 2 from
  the oracle certificate (`wlp3_hr1_or1.txt`).
- **Question.** Can a binder's 2-ball (u = 7, link and s fixed, p slots free) be completed to an isolated positive
  defect (README §7 test G) centred at u?
  - K = 2 is impossible by inspection: every binder has an s letter that is not 6, at distance 2.
  - So the test is K = 3 (`loop/g9/g9_K3_c7.out`, complete, letters 5-8, CMIN 1) and K = 4 (`c7k4.txt`, partial).
- **H-B7.** No binder completes to a K = 3 leaf. Any K = 4 completion dies to R_opt+, like every K <= 4 defect so far.
- **What each answer means.**
  - No completion: the binders are not test-G obstructions near u. They are obstructions of the rooted-word rule
    class only, so a richer rule (README §7 classes a-c) or larger configurations could remove them.
  - A completion that survives R_opt+: a test-G defect. Then t* > 0 for every finite-reach rule, and H7 dies.
- **Limit.** Defects whose non-6 part reaches distance >= 4 from u are not covered (K >= 5).
- **Guess.** 0 completions at K = 3. At K = 4, a few completions, all killed by B-fixed configurations at other 7s.

**Round 10 result (12:30-13:00Z).** Details in `wheeldis/loop/b7/FINDINGS.md`.
- **K = 3:** no binder completes. That holds for all 7, letters 5-8.
- **K = 4** (letters 5-7, complete for these 2-balls, via `defectb7`, a defectc8 with the 2-ball fixed):
  - 5 binders complete, with 2,064 leaves in total. 5575576/6666656 and 5676575/6556666 have no completion.
  - All 2,064 die to R_opt+, every one by a D configuration, and they stay dead with `strict7`.
  - Kills: the existing registry gives 1,973. New dfast at rings 10-15 gives the rest: 105 D of 260 at ring <= 14,
    2 of 8 at ring 15.
- **By-product: 4 B-fixed D configurations that forbid binders directly** (`loop/b7/b7f.out`; rebuilt by gen28 and
  rerun with dfast):
  - **f7_5567576_56.75.7** (r15) forbids the heaviest baseline binder, 5675765/6575575 (dual 0.20). That binder's
    1,536 K = 4 completions all die to it at the centre.
  - f7_5656757_657.555 (r13) and f7_..65757_..6555. (r12) forbid 5675756/7555565.
  - f7_..55756_..6666. (r13) forbids the oracle binder 5676575/6556666.
- **Verdict: H-B7 survives.** Near u (K <= 4) the d = 7 binders are not test-G obstructions, and 3 of the 7 are now
  forbidden as patterns. I guessed a few K = 4 completions, all killed at other 7s; in fact most kills sit at the
  centre.
- **Not run:** K = 4 with letter 8; K >= 5.

## Rounds 8-9 (16 Oct 2026, 10:00-12:10Z): H-L3, then the two-step rule class (H-R1)

**Round 8, H-L3** ("the remaining lone-five arrangements cannot be killed from distance-2 data"): dies as worded.
Details and table in `wheeldis/loop/lone/FINDINGS.md`. The surviving completions of A1 (d = 10, link 5656556565,
every s = 6) have a big vertex p at distance 2 from u, reached from a lone five through a 6.

**Ring-16 batch (background, finished 11:05Z).** Receiver-free: 3 D of 20 (`u10.out`). B-fixed: 6 D of 29 (`b10.out`).
- Recount with every pattern so far (`lone10.txt`): d = 9 max 4 lone fives (2 arrangements), d = 10 max **5** (15),
  d = 11 max 6 (7), d = 12 clear.
- **A1 is dead**: its link contains the window 5565655 with s = 666666, the ring-16 receiver-free D configuration
  z_5565655_666666. So the six-lone-five counting bound at d = 10 (2/7) is gone. The counting bounds left are
  1/5 (d = 9), 1/6 (d = 10), 1/7 (d = 11).

**Round 9, H-R1, pre-registered 11:10Z before any LP run.**
- Coordinator wording: a 5 -> 6 -> big rule takes t* below 2/7 at d = 10. A1's death overtakes that, so it is tested
  against the new one-step baseline t_B.
- **Hypothesis.** A 5 -> 6 -> big rule lowers t* below t_B.
- **Definitions.** A lone five w_i has a *second-ring route* if a 6-neighbour has a neighbour at distance 2 from u that
  the arrangement leaves open (the p slot of a link 6, w_i-1 or w_i+1) or fixes as big. Routes that only reach
  third-ring vertices do not count.
- **Test.**
  - Baseline: wlp3s (stall 25) with every pattern so far (pats0, u*.pat, b*.out, out/job28/r_2-4, loop/g9 D outputs).
  - Oracle: forbid each binding lone arrangement in which every lone five has a second-ring route, as if the rule
    fully relieved it, and rerun.
  - The oracle ignores the load the rule puts on p, so it is optimistic for H-R1.
- **Kill.** Any of these kills H-R1:
  - the oracle's t equals t_B;
  - the oracle's new bound is set by an arrangement with a lone five that has no second-ring route;
  - the baseline binders are not lone arrangements at all.
- **Guess.** t_B is between 1/5 and 1/4 and is set at d = 9 (link 566565656, four lone fives, all on link 6s with p
  slots). H-R1 then survives the oracle. It still needs the p-small completions to be reducible.

**Round 9 result (11:05-12:10Z, over the 30-minute cap because each LP iteration takes about 40 s).**
- **Baseline** (`loop/lp/wlp3_hr1_base.txt`, stall stop): t* >= 0.2773 (33/119), so the guess was wrong.
  - The certificate is five **d = 7** receivers, each carrying 0 or 1 lone five; the largest dual is on
    5675765/6575575.
  - d = 10 has slack (load 4.11 against 4.28). d = 9 still had a violated row at the stop, so the true t* can be
    higher.
  - A stall-80 copy (`hr1_long`) stopped with the same certificate (33/119) after 80 flat iterations, still with
    violated rows at d = 8 and 9. So the separation is degenerate there, and the one-step t* is only known to be
    >= 33/119.
- **Relief against load at the binders.**
  - Each binder has at most 1 lone five that the rule could relieve.
  - Each also has 1-2 second-ring fives (an s = 5 next to a link 6) that would send z into u through that 6, plus
    open p slots.
  - So with one z per target class, the rule adds at least as much load as it removes.
- **Oracle** (`hr1_or1`): the 4 routed binders forbidden, warm start. Stall stop at t >= 3/11 (0.2727).
  - Its certificate is two d = 7 receivers: 5676575/6556666 (1 lone five, 2 inflow fives) and 5765756/5556666
    (**no lone five**, 2 inflow fives).
- **Verdict: H-R1 dies (inferred, not a solved two-step LP).**
  - The binders moved to d = 7.
  - The oracle's bound rests on a receiver with no lone five to relieve.
  - Every binder takes at least as much two-step inflow as it sheds.
  - The spec for a faithful LP is `wheeldis/loop/lone/TWOSTEP.md`. It is not worth building while the binders sit at
    d = 7, where Studio's certificate loop already works.
- **G9:** the centre-8 K = 3 search is complete. The remaining 1,429 ring-1 words gave 0 leaves, so all 376 die.

## Rounds 6-7 (16 Oct 2026, 08:35-10:00Z): the LP floor after the d = 7 certificate, and the lone-five family

**Certificate (G2).** A1308's S = (0,5) at ring 14 is C (cfast, |X| = 1; `loop/rules/cert_bf.cfast`). So every
arrangement in the 5/17 and 1/5 certificates now has a reducible B-fixed configuration: 4 D, 1 C.

**LP after forbidding them (`loop/lp/`).**
- `loopfast.py` is a local Job 28 loop that takes the largest S first. `wlp3s.py` is wlp3 with an early stop: once t
  has not risen for 25 iterations it stops, and the dual of the rows found so far is a valid certificate that t* is
  at least the printed t.
- Result: **t* >= 2/7** (5/17 before). A full run stayed at 2/7 for about 90 iterations before I stopped it.
- The 2/7 is carried by a single receiver: d = 10, link 5656556565.
  - All six of its fives are **lone**: u is their only neighbour of degree >= 7.
  - So 6(1 - t) <= 4 + t for any rule that moves charge from a 5 to its big neighbours. This is a counting
    obstruction, so only reducibility removes it.
  - Its ring-16 B-fixed sets are D, and so is a ring-14 one. The next round moved to a sibling arrangement.
- Long Table then gave the LP loop itself to Studio (loop28b), so this thread stopped its loop.

**Lone-five family (`loop/lone/`).**
- **Question.** Which arrangements have more than d - 6 lone fives and contain no forbidden pattern?
  - `lone.py` answers it with sep3, using weight 1 on lone rooted words.
  - Before this round the answer was non-empty for every d = 9..15: up to 4, 6, 7, 8, 8, 9, 10 lone fives.
  - d >= 16 is clear on the old patterns alone (checked up to d = 20; the maximum is floor(2d/3)).
- **Receiver-free configurations** (`ufree.py`).
  - The configuration is S plus all neighbours of S except u, at exact degree. u stays on the ring with its degree
    free, so the configuration is the same at every d.
  - **62 of them are D**, at rings 10-15. Examples: z_55655_5665 (r10); z_55655_6666 (r12), two adjacent five-pairs
    with a 6 between them and every s = 6; z_556556_66666 (r14).
  - As patterns for d = 7..17 (`u*.pat`), they clear d = 13, 14, 15.
  - What is left: d = 9: 3 arrangements, d = 10: ~59, d = 11: 13, d = 12: 2.
  - These went to Studio as wlp3 patterns.
- **B-fixed sets of lone fives** for the rest (`bfix.py`, `iter.sh`). At ring <= 15, 24 more configurations are D.
  - 48 arrangements are left: d = 9: 2, d = 10: 31, d = 11: 13, d = 12: 2.
  - Most of them are lone fives alternating with 6s (e.g. 5656565656 with every s = 6), or 556 blocks with every s = 6.
  - Ring 16 is running in the background: 20 receiver-free configurations, plus 29 B-fixed at d = 9, 11, 12. Studio
    covers d = 10 at ring 15-16.
- **Reading (a hypothesis, not checked).**
  - In a real map, a 6 next to a lone five whose other neighbours are all 6 is the Job 17 D 6-wheel 566666.
  - So these arrangements need a big vertex at distance 3, which an arrangement that records only w and s letters
    cannot see.
  - If ring 16 does not clear them, the LP needs either third-ring letters in the arrangement or rules that pass charge
    through a 6.

**G9, defects with an 8 or a big centre (`loop/g9/FINDINGS.md`).**
- Ring letters 5-8 at K <= 3: every leaf with an 8 dies to a D receiver-centred configuration. Centre 8 is partial and
  still running.
- Centres 9-12:
  - K = 2 has no leaves. With ring 2 all 6, a ring-2 vertex next to a five is a Job 17 D 6-wheel (566666 or 556666).
  - K = 3 (capped) gave 1,952 leaves. All die after 1,801 new ring <= 12 dfast runs.
- The LP's d = 10 arrangement cannot be completed to a K = 3 defect.

**G7 closed for K <= 4.** The full audit of all 418,551 candidates had 0 nosimple and 0 bf_nosimple kills.
defect_check2 now counts an unrepaired non-simple ring as open.

**Kernels.** Both ring-9 lemma-A kernels went to Studio as dfast lines (`loop/lemmaA/kern9.txt`). The first is
certified in Lean (dcheck/LemmaAKern9.lean, Studio).

**What changes.**
1. The LP's obstruction after d = 7 is the lone-five family at d = 9..12. It is a pure counting bound, so the lever is
   reducibility, not the rule class.
2. Receiver-free configurations are the efficient tool. One verdict covers every receiver degree.

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
