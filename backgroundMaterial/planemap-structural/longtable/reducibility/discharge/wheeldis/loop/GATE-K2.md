# K = 2 gate (24 Oct): evidence from the explore loop, 16 Oct 2026

Tags: **[E]** = engine level (dfast/cfast verdicts, LP optima from scipy/HiGHS; no Lean). **[I]** = inferred from E
results, not computed directly. Full record: `SolvingFrameworkPlan/docs/working/EXPLORE-LOG.md` (rounds 1-20).
All commits are on branch `claude/project-thread-nh6pv2`.

## 1. Where the LP stands [E]

| Job 28 round | t* | tight receiver rows |
|---|---|---|
| 1-2 | 5/17 = 0.2941 | 1,961 / 2,155 |
| 3-4 | 2/7 = 0.2857 | 1,706 / 2,506 |
| 9-11 | 3/11 = 0.2727 | 2,743 / 3,817 / 4,213 |
| 12 | 13/49 = 0.2653 | 3,181 (227 d = 7, 1,519 d = 8, 1,435 d = 9) |

- t* fell 0.029 in 12 rounds. Explore's own floors on the way: 33/119 (one-step baseline, round 9) and 3/11 (oracle).
- d = 7 tight family (617 distinct rows, explore + Studio round 12): 218 forbidden after rounds 14-15 (35.3%);
  399 free, of which 14 are HARD28 and 46 of 49 HARD28-like rows are still free. [E]
- d = 8 tight rows: 0 of 1,519 forbidden by any registry window (`loop/w2/cov8.txt`). [E]

## 2. Hypotheses tested today

| Round | Hypothesis | Verdict | Commit |
|---|---|---|---|
| 8 | H-L3: lone fives cannot be killed from distance-2 data | dies as worded; A1 (d = 10) dead to a ring-16 D [E] | 2c12c874, 62c1a03d |
| 9 | H-R1: a 5 -> 6 -> big rule lowers t* | dies [I]: binders move to d = 7, the oracle bound rests on a receiver with no lone five | 9d1ac1af |
| 10 | H-B7: d = 7 binders sit in no K <= 4 isolated defect | survives [E]: 0 K = 3 leaves; all 2,064 K = 4 leaves die; 3 binders forbidden by new B-fixed D | cc0817c3 |
| 11 | H-B8: same with letter 8 and K = 5 | survives [E, K = 5 sampled]: 1,634 + 10,309 leaves, all killed | 24707f27 |
| 11 | H-K: cap on bigs per receiver | withdrawn before running: unsound (no lemma), deletes 559 of 562 tight rows | 46947c6f |
| 12 | H-AV: pair-averaging rows beat 3/11 | dies [E]: the 3/11 certificates split into consistent self-pairs | 3986541d |
| 13 | H-E7: receiver-free windows with big link vertices | dies [E]: 0 D of 56 at ring <= 15 (d = 7 windows wrap) | 6495cd55 |
| 14 | H-W2: small B-fixed windows forbid >= 30% of the d = 7 family | survives, just [E]: 178 D of 636; 190 of 617 rows (30.8%) | d4d6de61 |
| 15 | H-W3: 8-relaxed windows reach HARD28 | neither bar, leans dead [E]: 23 D of 565; +28 rows; 0 HARD28 | 18892b89 |
| 16 | H-W4: small windows at d = 8/9 | ROUND16 | |
| 17 | H-W5: ring-17 windows for HARD28 | dies [E]: 0 D of 6 (dfast18; no cfast yet) | see log |
| 18 | H-LF: HARD28 rows are receiver-centring artefacts | leads, caveats [E]: 0 leaves at K = 3; 1,521 K = 4 leaves (capped) all killed, none at u | 39389e23 |
| 19 | H-B0: joint (u, v) pairs add kills | dies [E]: 0 joint kills in 10 built certificate pairs | f4398168 |
| 20 | H-L2: big-big transfers lower t* materially | dies [E, restricted LP]: t* = 7/27 = 0.2593 | 59fdb04f |

## 3. Supply forecast (after round 14; `loop/w2/FINDINGS.md`, commit cab4d473)

- Of 427 then-free d = 7 rows: 318 have an untested B-fixed S at ring <= 16 (supply), 61 wait on cfast, 48 are
  HARD28-like (every S at ring <= 16 tested, none D/C). [E]
- The supply is expensive: 549 of its 564 untested configurations are at ring 15-16. [E]
- At Studio's ~200 configurations per round the ring <= 16 supply lasts about 3 rounds; about a third of supply rows
  die, and afterwards about two thirds of today's free rows are HARD28-like. [I]
- At 0.029 per 12 rounds, the ring <= 16 supply runs out long before t* nears 0. [I]

## 4. Price of ring 17 (round 17)

- The 6 untested ring-17 exact windows of the HARD28 rows (covering 7 of the 14 free rows): **0 D of 6** [E].
- Cost: 4-7 minutes and about 25 MB per window on one core with `bin/dfast18` (`bin/dfast` stops at ring 16) [E].
- The HARD28 rows' other exact windows sit at ring 18-21. dfast's cost grows with ring size, and these are larger
  than 17. A ring 17-21 push over the 15 HARD28 rows is cheap per window but has a 0/6 D rate so far, and cfast on
  the 6 non-D windows is the next cheapest step. [I]

## 5. Structural findings

- **Kills sit at neighbouring 7s, not at u** (round 18) [E, capped search]. Where HARD28 rows complete to K = 4
  defects at all, every completion dies to a configuration centred at another 7: a link vertex of u (45%), ring 2
  (48%), ring 3 (7%). Bigger windows at u are not where these rows die.
- **Pair configurations add nothing** (round 19) [E]. A configuration centred at u or v lies in that centre's 2-ball,
  so joint (u, v) infeasibility needs ring repair; 0 joint kills seen.
- **Self-pairing caps 2-ball rules** [E, restricted LP]. Pair averaging (round 12) fails because each 3/11 binder is a
  consistent neighbour of itself. Big-big transfers (round 20) relieve 44 of 49 HARD28-like rows but stop at 7/27:
  the binding d = 7 rows fit as their own 7-neighbour, so the edge reads the same from both ends and any rule using
  the two 2-balls moves no net charge across it. Studio already has 3 of those 5 binders killed by B-fixed D and
  the other 2 at ring 15-16 in its queue.
- The 7-5-7 family with letters 5-7 is gone at ring <= 14; what survives carries exact 8s near S (round 14) [E].

## 6. Options left

- **A: targeted ring >= 17 at u.** Cost: see section 4; 15 HARD28 rows, their exact windows at ring 17-21. Round 18
  says these rows die at neighbouring 7s, so ring-17+ windows at u may not be the cheapest kill. [I]
- **A': configurations centred at u's neighbouring 7s** (round 18's kill sites) as patterns for d = 7 rows. Same
  engines; needs a non-receiver-centred pattern form in the LP. Not costed. [I]
- **C: narrow.** Stop at the current t* and state K = 2 as open with the evidence above. Costs nothing more; it leaves
  the gap between 13/49 (or 7/27 with transfers) and 0.
- **Ruled out today:** cap on bigs (unsound), pair rows, 5 -> 6 -> big rules, 2-ball edge transfers below 7/27.
