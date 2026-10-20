# Opus team on the remaining gap (18 Oct 2026, from 08:35Z) [exploratory, engine level]

Kyle (08:34Z): "assign an opus agent team to attack the remaining gap from all angles and make a run for the link".
Log in EXPLORE-LOG.md style, newest first. This file and `opus/*/` are the team's; COORDINATOR-STATE.md is not edited here.

## What the gap and the link are (my reading, 08:45Z)

- **The gap.** K <= 1 meets the claim rule. For K >= 2 (degree-5 senders with two or more big neighbours) the
  discharging LP has t* = 7/27 > 0 exactly on the full registry; charge-sharing (L2) gave no gain. The binders are
  d = 7 receiver rows whose windows at ring <= 16 are neither D nor C. H7 (README §7.1) shows the deeper reason: the
  defect D3 has net charge +1 and contains no configuration of the programme's R_opt, so **no local rule of any kind
  closes against R_opt**. The gap is the reducible set, not the rule class.
- **The link.** The step that would join the K <= 1 result to a full proof: a reducible set and rule class for which
  the K >= 2 LP reaches t* <= 0. Nothing in the state file names "link" as a specific step; the nearest is Job 26
  ("the last link from the LP to the Lean chain"), which is a soundness bridge, not the gap.

## Round O1 (08:50Z-): four angles in parallel

Pre-registered before any probe ran.

| angle | question | guess | plan-changer |
|---|---|---|---|
| A, RSST in the defects | Does each H7/K4/Job 28 defect (D1-D3, E1, E2, K4 survivors) contain one of RSST's 633 configurations? | Yes for all: RSST's theorem forces a configuration near any positive vertex of a locally 6-connected patch | Yes: the H7 obstruction is an artefact of R, and R + RSST is the candidate link. No: a patch error, or a gap in applying RSST locally |
| B, RSST forbids LP rows | How many free tight rows (7/27 binders, HARD28-like 49) are forbidden by an RSST configuration inside the row's fixed patch? | Few: a d = 7 row fixes little beyond u's link and second ring, and most RSST configurations need exact degrees further out | Many: rerun the LP with RSST patterns (lower bound plus a feasibility upper bound) |
| C, kc at ring 17-20 | Do the binders' untested windows at ring 17-20 turn D now that kc makes ring 18-19 a matter of minutes? | A minority (10-20%) turn D; ring 17 was 0 of 6 | A binder dies: the ring <= 16 supply limit in GATE-K2 §3-4 no longer binds |
| D, RSST rules vs the LP's rule class | Do RSST's 32 rules lie in a rule class the LP optimises over? If so, R + RSST makes the LP feasible by RSST's theorem | Mostly yes (class (a), sender 2-ball), with gaps at ">= d" degree letters and RSST's degree >= 12 hand argument | Yes with small gaps: the link is concrete and costable |

### O1 results so far

- **D (09:00Z): RSST's rules sit outside every LP rule class** (`D_rsst_rules/FINDINGS.md`) [cited, from Gonthier's
  fourcolor `theories/proof/discharge.v:73-140`]. The 32 rules are 38 parts, each moving 1/10 LP unit from a sender of
  degree 5..8 to a receiver >= 6, reading the sender's 2-ball over {5,6,7,8,9+}. Only rule 2 fits (a)/(c) whole; 6-senders,
  6-receivers and 7->8+ transfers fit nowhere. So RSST's theorem does not make the present LP feasible once RSST's
  configurations are added. The guaranteed hybrid is Gonthier's proof re-encoded; mixing "own rules for K <= 1, RSST's
  for the rest" voids both certificates (RSST's 5s pay their 6s). Gonthier's discharging covers degree >= 12 by a
  computed cap, not by hand. Guess check: "mostly class (a)" was wrong.
- **A (09:05Z): every H7 defect contains RSST configurations, D-reducible ones among them** (`A_rsst_defects/FINDINGS.md`)
  [E]. D1 25 hits (11 D), D2 21 (6 D), D3 15 (7 D; #110 at ring 10, four 5s and two 7s, wholly inside the cluster), E1 20
  (11 D), E2 21 (11 D). All 50 D hits re-extracted and D by dfast; all 59 C hits are cfast C-candidates (|X| <= 4).
  453 of 453 sampled K = 3 / K = 4 defect candidates contain an RSST D configuration (rings 8-11). Controls: icosahedron
  hits only the diamond; pure 6-sea none. Reading [I]: H7's "no local rule closes against R_opt" is a fact about R_opt's
  shape (wheels and u-centred configurations), not about reducibility. Adding RSST's 249 D configurations (already
  Lean-checked in `dcheck/`) to R removes every known defect. It does not by itself close the LP: the rules must see
  these configurations within radius 2 of a 5. Guess check: right.
- **B (09:25Z): RSST's 633 as receiver patterns leave t* = 7/27 exactly** (`B_rsst_rows/FINDINGS.md`) [E]. A row
  fixes only the slots its 5-senders read. On the certificate row d = 7 5675765/6577575, 0 of 633 fit the fixed slots;
  only 128.136 (C, ring 11) fits, and only with s1 = 5 or s4 = 5, slots no sender reads, so the 16 fillings with
  s1, s4 >= 6 stay RSST-free. Elsewhere RSST does reach the receiver (74 configurations fit a d = 7 row's fixed slots,
  44 D, mostly fans around u) and forbids many non-binding rows: 920 of 1,385 tight_13 rows, 6 of 7 old binders, but
  only 2 of 49 HARD28-like. LP with 387 RSST patterns added: 7/27 with the same certificate; upper bound from the
  existing feascheck, since patterns only lower t*. Lever dropped. Guess check: "few" was right for the binders.
- **F (09:50Z): the 16 fillings with s1, s4 >= 6 stay RSST-free** (`F_free_slots/FINDINGS.md`) [E]. On the fixed
  patch none of the 16 contains an RSST configuration. With one more ring (the six privates of the non-5 link
  vertices at 5..9+) every filling gains hits, but each hit needs a private at 5 or 6, and all six privates at 7 is
  RSST-free for all 16. So RSST does not forbid the row even under a receiver-2-ball rule class. 6 u-centred kc windows
  at rings 13-14 without s1, s4: not D. The explore thread (round 34 part C) covers these fillings with u-centred
  windows; it killed the 9 fillings with a 5 at s1 or s4 by D at ring 13 on two engines.
- **E (10:05Z): a rule through the 6s voids the 7/27 certificate in all 16 open fillings, LP effect not computed**
  (`E_rule_change/FINDINGS.md`) [hand, plus a restricted LP]. **Rule T:** a five with big neighbour u and a
  6-neighbour x adjacent to u sends tau to z, the other common neighbour of u and x, when z is big (here
  w0 -> w1 -> w2 and w6 -> w5 -> w4; both z are 7s). Inflow into u comes only from a five in an s-slot between a link
  6 and a link big, i.e. s1 or s4, so none in the open fillings; the reflection swapping u and w2 maps w0 (a 5) to
  s1 (>= 6), so it escapes self-pairing. Row: t >= (0.7 - tau0 - tau6)/2.7. Open risk: the load lands on w2/w4 and
  may rebind near 1/4. Rule H (lone five sends past two consecutive 6s) acts only when s1 = 5, already killed;
  restricted LP with H: t >= 1/5, not converged, new binder d = 7 5568586/5755756, lower bound only, no gain claimed.
  Within 2-ball rules that send only to adjacent bigs, w6 and w3 self-pair, giving a 3/17 floor for this row.
- **Explore's review of rule T (via the coordinator, 09:22Z), accepted in part.** (a) T helps only if the five pays u
  less when z is big, so it is a sender-2-ball rule, not an additive tau. H7 floors that class at 1/21 against R_opt,
  but only via D3, and D3 contains RSST #110 (D, ring 10; angle A), so the floor does not hold against R_opt + RSST's
  D set. (b) A restricted LP over the 7/27-tight rows is under-separated exactly where T moves load: no restricted run
  is claimed.
- **G (10:30Z): rule T written as a sender-2-ball rule for a sep3x/wlp3x job** (`G_ruleT_lp/FINDINGS.md`) [E counts
  only, no LP]. Y[r, za, ze] replaces y[r] and T[r, za, ze, side] pays big z. Reading z as small/big costs 1,356 Y +
  504 T and 1,194 sender rows (today 942 y, 342 rows). The outflow at u uses the 7-letter window sep3x already
  resolves; the inflow at z is a per-transition weight on (w_j, s_j, w_{j+1}), sound for an upper bound. The exact bound
  needs 625 DP states (about 5x per build). Validation: T = 0 must reproduce 7/27 and the j28_13 dual. Note [I]: L2's
  u -> w2 transfer already reads (6, 5, s1) against (6, s1, 5), so once the s1 = 5 kill enters L2 (explore's proposed
  sep3x state extension), L2 alone may already make this move. Run that first; T is the fallback.
- **Cross-checks from the explore thread (via the coordinator, 09:41-09:44Z).** D3 contains RSST #110 on explore's
  own containment code (vertices 1, 2, 6, 7, 16, 17, all inside Y); kc D with ext 496 = RSST's count, so D on two
  engines with our dfast. H7's 1/21 floor is now logged as R_opt-specific. D1, D2, E1, E2 rest on our engines only.
  Explore round 36: w2/w4 absorb at most T = 0.1506 at first order, so rule T's gain through this row floors near
  t = 0.155 (hand second-order argument; independent check H running). Job 30 (Studio): part A puts the s1/s4 = 5
  kill into L2 with non-five s-letters; part B (rule T) runs only if A holds 7/27. RSST-D (158 patterns) is in the
  LP and t* stays 7/27 exactly, matching angle B.
- **H (10:55Z): explore's rule-T floor t >= 11/71 = 0.1549 at (6,6) checked independently and holds**
  (`H_floor_check/FINDINGS.md`) [hand + frame.py]. It is a floor for the whole rule-T class, not first order, unless
  w2/w4 can pass charge on (L2 transfer) or one of four arrangements is killed. So Job 30's order is right: part A
  (L2 with the s1/s4 = 5 kill) is what can go below 0.155; rule T alone cannot.
- **C (10:00Z): no window inside R's fixed patch kills any of the 16 open fillings** (`C_kc_ring17/FINDINGS.md`,
  `fillings_opus.txt`) [E, kc; D windows also dfast]. 1,350 windows on 2 cores. Windows not centred on u (connected
  subsets of u, w0-w6, s0-s6 at exact degrees): with s1, s4 >= 6, 0 D of 1,131 at rings 6-16 (every subset at ring
  <= 14 run). The 9 D windows found (rings 11-12, both engines) all use a five at s1 or s4, i.e. the 9 fillings explore
  had already killed. R's 4 B-fixed windows at u (rings 11, 16, 17, 17) are all not D. 1,644 untested windows at
  rings 15-20 listed in `untested_r15_20.txt`. Reading [I]: killing the open fillings needs vertices outside R's
  patch, case-split by degree, which is what explore's round 37 did (w2's link, C at ring 13). Guess check: "10-20%
  of binder windows D at ring 17-20" was wrong (0 of 7 at ring 16-17).
- **H round 2 (10:15Z): after explore's round-37 kill, the provable rule-T floor through R drops to t >= 1/21**
  (`H_floor_check/FINDINGS2.md`) [hand + sep3 c-check]. w2/w4's own rows give no floor (c = 1/5 at link 7665675);
  five e now routes to s2 through e' = 6, and the chain through s2's best surviving frame (5765557 / 7575757, c2 =
  7/10) gives 1/21. A lower bound only; true floor between 1/21 and explore's first-order 0.122.
- **I (10:30Z): rule S, a 6-relay generalising T and H, gives e a sound unpaired route, but onto a 7/27-tight big**
  (`I_route_e/FINDINGS.md`). On frame 7665675, x4's T inflow through y can self-pair with e's, restoring 11/71 [hand];
  this conflicts with H round 2's 1/21 (which dropped x4's inflow) and is being reconciled. Rule H's route to the
  forced big b lands on tight rows (cap 0 at first order). Kill target: u at (6,6) + w2 frame + b's tight row.
- **H round 3 (10:45Z): reconciled, the rule-T floor through R at (6,6) is 1/21** (I's self-pairing needs e''s
  6-wheel c6_566577, which is C in Job 17, or 2.122). `H_floor_check/floor.py` recomputes the floor from a kill
  list; the formula is in FINDINGS2.md.
- **Floor after explore's round 38 (11:00Z): the hand chain gives no positive floor** (`floor.py` with
  `H_floor_check/kills_r38.txt`: round 37's window plus round 38's five C windows). Surviving non-dominated s1 = 6 w2
  frames: 7667575 / 5557777 (c = 2/5, T <= 3/5 + 7/5 t) and 7665775 / 5555577 (c = 1/5); floor -1/11. So no
  y-independent obstruction to rule T through R is left from this method; explore's first-order t >= 0.054 at (6,6)
  is the only remaining estimate, and Job 30 part B is the real test.
- **Erratum and recheck (11:15Z).** G's tcount scripts gave reflected roots the wrong T side (Studio found it, 78ed61e7);
  fixed, T = 444 (small/big, equal to Studio's) and 2,007 (full letters). floor.py and I_route_e never used them.
  floor.py with conservative-X kills only (round 37's two cwin windows + f7_5566757 + f7_5667576, file
  `H_floor_check/kills_conservative_r38.txt`) and with all round 37-38 kills: both give no positive floor (-1/11),
  binding 7667575 / 5557777 at w2 and w4. (floor.py's "killed" count is of its dominance-ordered scan, not a total.)
- **Explore rounds 39-41 (via the coordinator, 11:00Z).** Round 39: R* + p5 = 7 (w6's rootings sharing one variable),
  0 D / 0 C on 16 windows at rings 16-17 including both ring-17 windows covering all 16 fillings; best leftover 608.
  That arrangement stands at ring <= 17. Round 40: kc -C2 vs cfast, 0 mismatches on 483. Round 41: kc -C over C's
  1,383 sub-patch windows of R* at ring <= 15, 1,131 done, all not D and not C.

## Round O2 (11:35Z-): checker and the last w2 frame

- J: an independent checker of the LP bound (dual certificate and its own exhaustive primal separation, T-aware),
  validated on 7/27, for Job 30 parts A and B. K: kill w2 frame 7696575 / 5555977 (s1 = 9, first-order binder after
  round 38) at rings 16-18, w2-centred and not, kc D and kc -C conservative, second engine on any hit.
- **Explore round 42 (11:43Z, commit 5da381a1, loop/k42/) ran our private split (i)** on its own containment code over
  250,000 cases, killers cut and checked on kc + dfast/cfast. Agrees with F: every hit needs a private at 5 or 6;
  all >= 7 is free for all 16 fillings; p1 = p5 = 6 with the rest 7 dies only at s1 = 6 (RSST 2.211701966). p5 = 5
  always dies (RSST 122.126, conservative two-engine), so w6's z-letter p5 >= 6 in R*. p1 = 5 dies only by RSST 2.126
  (C, broad X only), so conservatively p1 = 5 survives except at s1 = 7 with p2a = 5. Survivors: loop/k42/cases_cons.txt.
- **J's upper side waits on Studio's full-precision 7/27 solution** (Studio is pushing it, 11:43Z).
- **K (12:05Z): w2 frame 7696575 / 5555977 survives every window tested at rings 6-18** (`K_frame_kill/FINDINGS.md`)
  [E, kc D and kc -C conservative]. 819 windows (connected subsets of the frame's 13 known vertices, w2-centred and
  five-clusters); tested 351/351 at rings 6-14, 40/131 at 15, 21/143 at 16, 6/117 at 17, 1/62 at 18: 0 D, 0 C. Best C
  leftover rises with ring (1,162; 2,782; 6,402; 20,140). H-K dies by its kill line (0 hits of 28 at rings 16-18).
  Reading [I]: killing it needs letters beyond the frame, split into cases, like R* itself.
- **Spec review (12:25Z): Studio's rule T option F kill filter is sound with conditions C1-C5**
  (`F_spec_review/FINDINGS.md`). (a) no extra edges at distance 2: justified (small README fix); (b) the |K| split
  cap loses strength only, drop it; (c) unsplit privates of a 9: sound. Gap: the embed test is weaker than RSST's
  "appears" when K's interior has a cut vertex (only 3.3700806 among 24; its flip is also C, so no wrong deletion
  today); C1 requires a rotation check or re-cut verdicts.
- **M (12:50Z): all 163 sender-row deletions of Studio's built F filter confirmed independently**, all by
  k42_rsst025_xxxxxxx5; reflection-closed; rotation check redundant on 2-connected interiors; 0 of 200 sampled kept
  rows should have been deleted (`M_deleted_rows/`, appended to `F_spec_review/FINDINGS.md`).
- **N (14:55Z): independent UPPER check passes, so t* = 7/27 is now two-engine on both sides** (`J_lp_checker/`,
  jsep2.cpp / jcheck2.py, `upper2_studio_round13.log`) [E]. Studio's full-precision round-13 solution (IEEE doubles)
  violates no sender row (342) and no receiver row at d = 7..30, plus the Karp tail (lambda = 0.4938, covers d >=
  11.3). Max load minus (d - 6 + t): d = 7, 8, 9 tight (-2.6e-13, float noise; e.g. d = 7 link 9655675 s 5657566),
  d = 10 -0.111, d = 11 -0.667 and falling. The 10 missing d = 10 files cannot matter. 34 s on 3 threads (bitset
  pattern match, rotation symmetry break, tighter bound). Validated against the old jsep on d = 8..17 and a planted
  violation. Caveat: margins are floating point; an exact-rational recheck of the tight d = 7-9 rows is not done.

## Round O3 (18:00Z-): race (Kyle, 17:51Z: a second, sealed team on the same gap; first to a verified t* <= 0 for K = 2, or the largest verified drop, wins). Never read loop/teamB/.

- P: our own LP engine on jsep2 (exhaustive separation in seconds): validate 7/27 to true convergence, then run-A
  kills, L2 transfers, rule T; every value is a converged primal passing `jcheck2 upper` plus a dual passing
  `jcheck lower`, else a lower bound. Guess: rule T with the run-A kills lands near 0.15-0.2.
- Q: next rule class beyond T (rule S 6-relay, RSST-style 6-receivers/senders, asymmetric big-big transfers), ranked
  by gain per engine cost, spec ready for P's engine.
- **Q (19:15Z): next rule class spec** (`Q_rule_class/FINDINGS.md`): S-lite (rule T + fan route O, no engine cost)
  first, then P6 (link 6 privates as state). With round 42's letters, w2 can absorb T up to 0.796 at R*(6,6), so T
  alone leaves R*'s row with no floor; the new route targets (s1, p1, p5) are 7/27-tight at d = 7, so beyond T the
  gain at R* is second order. New self-pair found at s1 = 7 for route O.
- **P interim (19:20Z): with run-A's kills and L2 transfers, our own engine converges to t* = 1/4 exactly** [E, one
  engine family]. Stage 1 (round-13 args, x = 0) reproduces 7/27 in 33 iterations, 5.3 min. Stage 2 (run-A kills +
  ring-16 kills + round-42 conservative windows), x = 0: 7/27. With L2 (xcap 3): **t* = 1/4**, dual certificate
  1/4 55688 + 1/4 66668 + 1/8 55858 + 1/8 58668 + 1/4 receiver d = 8 85556565/65866655 (J lower VALID), primal
  feasible at d = 7..30 + Karp (J upper). Binder moved from d = 7 to d = 8. Caveat: the solver and the checker share
  jsep2, so a second engine (Studio's feascheck/sep3x) is needed before this counts. Also fixed a ykey/tkey
  palindrome-swap bug in J's keys (pcheck.py); counts now 1,356 Y + 444 T, equal to Studio's.
- **P (19:50Z): t* = 1/4 on our engine for run-A kills + L2, for run-A kills + rule T, and for both** (`P_own_lp/`)
  [E, our engine; lower = exact certificate check, upper = exhaustive d = 7..30 + Karp]. Validation 7/27 in 33
  iterations / 319 s, dual = j28_13. Run-A kills, x = 0: 7/27 (binder still R via filling 7576556/7767566).
  + L2 (xcap 3): 1/4. Studio's exact run-A registry + L2: 1/4 (so run A, at lower bound 0.228, should converge to 1/4).
  + rule T (option B), x = 0: 1/4. T + L2: 1/4. Binder at 1/4 in all: receiver d = 8 85556565/65866655 (1/4) with
  senders 55688, 66668 (1/4) and 55858, 58668 (1/8); rule-T flags 0; neither L2 nor T reaches it. Caveats: RSST-D's 158
  patterns not loaded, so 1/4 is an upper bound for the full registry (they could kill the d = 8 binder); T results
  checked by our pcheck (J's code with the ykey/tkey fix), not a separate engine; float primal.
- **P stage 4 (19:30Z): neither RSST-D nor S-lite moves the bound; t* = 1/4 stands** (`P_own_lp/FINDINGS.md` §4a-4b).
  4a: run-A registry + RSST-D's 158 patterns (all rotations/reflections; 27/55/76 at d = 7/8/9; they forbid 152/251/1,413
  generated rows) + T + L2 -> 1/4 [lower VALID, upper FEASIBLE d = 7..17 exhaustive + tail + Karp]. No RSST-D pattern
  forbids the d = 8 binder 85556565/65866655 or R's filling 7576556/7767566. 4b: S-lite (T + fan route O, I1-I3 inflows,
  conservative max over keys; orientation test 0/50k mismatches; fan-off reproduces T exactly) -> 1/4 [own checkers,
  share sender enumeration]. Why: binding sender 66668 has all hats and fans small next to the 8, so neither route A
  nor O exists. What can break 1/4: a reducible kill of 85556565/65866655, a small-hat/small-fan route (Q's route C,
  6-decided relays), or exact letters instead of small/big.
- **Two-engine (19:32Z, via coordinator): Studio reported at 18:48Z that t* = 1/4 exactly on its own LP engine as well
  as ours, and stopped run A as redundant.** So K = 2 is at 1/4 [E2]. Next: R (reducible kill of the d = 8 binder) and
  P stage 5 (exact letters, small-hat route); Studio's Job 31 (6-relay) is queued, complementary.

## Round O4 (pre-registered 19:35Z): exact letters at the d = 8 binder
Studio verdict (d64c8442, loop/studio/opus_check/README.md): sol_s2x passes both sides on Studio's engine, so
t* = 1/4 is [E2]. Long Table has given the reducible kill of 85556565/65866655 to the exploration loop, so we stopped
our agent R and have no output from it.
- **Hypothesis:** exact letters for the hat, fan and z letters (5, 6, 7, 8, 9+ in place of small/big) in rule T
  (+ L2, + S-lite if cheap) let the five 66668 next to the 8 pay a big vertex other than u, and drop t* below 1/4.
- **Kill line:** if exact-letter T + L2 on the run-A registry + RSST-D converges to 1/4 (lower VALID), exact
  letters are dead for this binder. Next would be a 6-decided relay (Studio's Job 31 class), not refining further.
- **P s6 (19:55Z): with explore's k43 kill (f8_...55565_...5...., C ring 10), argsA + L2 converges to t* = 5/21
  = 0.2381** [E, our engine; J lower VALID, J upper FEASIBLE d = 7..17 + Karp d0 = 11.7; 51 iterations, 530 s]. The
  dual is spread over 25 rows, max weight 0.127 (sender 56687). Receivers: d = 7 8556855/7565666 (4/63), 8567655/6655656,
  8655675/5866555, 7557656/8585665; d = 8 75565756/75666565, 76565565/56568565, 75656575/56665555, 76556565/58565765,
  85556565/66866665. Sent to Studio for a second-engine check.
  O4 result: exact letters (s5a, T + L2 + RSST-D, before the kill) converged at 1/4, lowerS VALID. **Kill line met:
  exact letters are dead for the old binder.**
- **Two-engine (20:02Z): Studio passes 5/21 on both sides** (68294ae5, loop/studio/opus_check/README.md).
  feascheck: 0 violated. lowercheck: all 25 certificate rows rebuild, exact cancellation. So t* = 5/21 for K = 2 is [E2].
  Studio has also run all 382 windows of the full k43 batch (c5a71dc0) through twoeng: 184 D + 198 C.
- **P s6t43 (20:15Z): T + L2 + RSST-D + the full k43 batch (184 D + 198 C) gives t* = 11/47 = 0.2340** [E, our
  engine; lowerT VALID, 24 rows; pcheck upper FEASIBLE d = 7..17 + DP to 30 + Karp d0 = 11.8; 18 iterations, 186 s].
  Top binder: receiver d = 7 7565765/6855555 (4/47). At 2/47: d = 7 8566655/6656656, 7557565/6566666, 8558655/6665666,
  7557656/6565665; d = 8 76565565/57765865. At 1/47: d = 8 75657565 with s-words 66656665 and 55655565. Senders: 56687
  (6/47), 55677 (4/47 under each flag setting), and others. Single-window s6t gives 14/59. Sent to Studio for a second check.
- **Two-engine (20:17Z): Studio passes 11/47 on both sides** (8f45fca8, loop/studio/opus_check/). Inputs are
  byte-identical. 1,036 Y + 104 T keys are canonical. feascheckt: 0 violated at d = 7..15, DP tail clean. All 24 cert rows
  rebuild, so t* = 11/47 with rule T is [E2]. Studio asked for a no-T baseline (argsA43 minus T) for its new LP class.
- **P s7 (20:30Z): without rule T (run-A + full k43 + RSST-D + L2, argsA43noT.txt), t* = 11/47** [E, our engine; lower
  VALID, upper FEASIBLE d = 7..17 + Karp; 37 iterations, 363 s]. **So rule T gains nothing over L2 on this registry.**
  Exact letters (s5a43, T_F + L2) also stay at 11/47: exact letters are dead here too. Binders as in s6t43, plus
  sender 55677 at 8/47. Sent to Studio as the Job 31 baseline.
- **Soundness flag (20:37Z, Long Table): 16 k43 names (k43/kills_drop44.txt) left w_i free between fixed s's, so they
  matched non-window rows.** They were loaded in s6, s6t43 and s7. Lower sides still stand; the upper (FEASIBLE) sides
  of 5/21 and 11/47 are **provisional** until re-checked without them. Studio is re-running feascheck. P2 is re-running
  our upper check on s7 minus drop44, and then the s9 solve (minus drop44 + k44 pats44 + round-45 D windows).
- **P2 drop44 recheck (20:50Z): 11/47 and 5/21 stand on our engine.** argsA43noT_drop is argsA43noT minus the 16
  names (11 D, 5 C, all d = 8; 4,341 -> 4,325 distinct d = 8 patterns). sol_s7 upper: FEASIBLE (0 violated d = 7..17,
  DP d = 18..30, Karp d0 11.78); cert_s7 lower: VALID. argsA6 never contained any of the 16, so 5/21 was unaffected (upper re-run:
  FEASIBLE). Files are in P_own_lp/s9/. Gotcha: the check needs root= the P/m wheeldis tree with out/job30/, or
  addA_dfast18/k3x files go missing silently and give a false INFEASIBLE at d = 7 (link 9655757).
- **P s8 (20:55Z): our own 6-relay class on the s7 registry gives t* = 18/79 = 0.2278, down from 11/47** [E, own
  checkers; lowerR VALID (fails as it should when a conservation row is dropped), upperR FEASIBLE d = 7..17 + DP + Karp
  d0 11.7; 25 iterations, 377 s]. Kill line not met. The class: fives pay g to 6-neighbours, keyed by the 6's link seen
  from the five (spokes exact, hats/fan small/big); the 6 pays h to its big neighbours, keyed by its exact link word;
  994 conservation equalities; receiver inflow is the max over the 6's unseen private. Built without reading Job 31.
  Binders: d = 7 8566655/6656656 (10/79), d = 8 75657565/66665655, 8558655/6665666, 76565565/56865865; senders 55667, 55687,
  66678 (10/79), 56687. Caveats: the checkers share key construction with the LP, and the registry still has the
  16 drop44 names (via k3x), so the upper needs a re-run on the corrected registry. Sent to Studio for a second check.
- **P2 s9 (21:00Z): main line (run-A + 30f86cd4 k3x = k43-drop44 + k44 + k45, RSST-D, L2, no T) gives t* = 2/9 =
  0.2222** [E, our engine; lower VALID exact; upper FEASIBLE d = 7..17 + DP + Karp]. All 8 receivers of the 11/47 dual are
  killed. New 6-row dual: senders 55667 (2/9), 56668 (2/9), 55767 (1/9), 58778 (1/9); receivers d = 7 8655675/5756585 (2/9),
  d = 8 75576556/78756665 (1/9). `P_own_lp/s9/FINDINGS.md`. Sent to Studio for a second check.
- **P s10 (21:15Z): our 6-relay class + L2 on argsA44 + RSST-D gives t* = 217/1129 = 0.1922** [E, own checkers;
  lowerR VALID with 43 rows; upperR FEASIBLE with all 994 conservation rows, d = 7..17 exhaustive, DP + Karp d0 11.7; 51
  iterations, 719 s]. Also s8 re-checked on argsA44: the upper is FEASIBLE at 18/79, but the lower is INVALID because six of
  its receivers are now killed. Binders: receivers d = 7 7765556/6575766 (0.149), 7766556/6566575 (0.140), and d = 9
  656565665/665666566 (0.035), plus smaller ones. Senders 55767 (0.149), 66669 (0.109), 55667, 55757, 57667, 56696. Sent to
  Studio for a second check.
- **Two-engine (21:07Z): Studio passes 2/9 (s9) on both sides** (d86b4a95; registry identical, 16,587 patterns;
  0 violated rows; all 6 cert rows rebuild). Main-line K = 2 is at 2/9 [E2]. The relay value 217/1129 waits on Studio's
  check, which comes after Job 31's blind solve.
- **P s11a (21:30Z): exact letters (both hats and the fan) in the relay's pull keys leave t* = 217/1129** [own checkers:
  lowerR gexact VALID with 68 rows; upperR gexact FEASIBLE]. **Kill line met: exact relay letters are dead.** Built as one m <= g
  variable per spoke context, so it is the same as enumerating all hats x fans (1,411 g keys, 47,046 sender rows). The
  binders are the same receivers as in s10.
  s11b (6 -> 6 second-generation relay): with exact conservation, the edge amount can depend only on the shared pair, so
  every 6-6 edge nets to zero and the class collapses to s10. A useful version needs 6-centred 2-ball types with their own
  separator, which is new engine work.
- **P2 s13 (21:45Z): main line (no T, L2) on Studio's aee20e3b registry (426 D / 422 C k3x + RSST-D) gives t* = 1/5**
  [E, our engine; lower VALID; upper FEASIBLE d = 7..17 + DP to 30 + Karp lambda 0.5333, d0 12.43; 38 iterations, 381 s]. Loaded:
  D 15,461, C 1,468, RPAT 158; 0 of the drop44 patterns; both 2/9 receivers forbidden. The dual has 4 rows: receiver d = 7
  7765556/6575765 (2/5), senders 55757, 55767, 57667 (1/5 each). Sent to Studio. Relay s13r is running.
- **P2 D-count reconciliation (22:05Z): the 339-pattern gap to Studio (15,800 vs 15,461) is fully explained** (`s13/dcount.txt`).
  - 329 are name duplicates that our parser maps to an earlier identical pattern (p-, e- and f-name spellings of the same
    pattern): eq_D7 59, eq_D8_k3 256, r_D10k5 2, b6 1, u1.pat 11.
  - 10 are the job28 r_5..r_8 files missing from our root. They add 5 distinct d = 10 patterns, and with them loaded
    (argsA46_r58) the s13 binder is still admissible.
  - So 1/5 holds from both sides on the full registry.
- **P2 s13r: the relay on aee20e3b gives 217/1129, unchanged from s10, with the same binders.**
- **P2 s14 (22:15Z): main line on 42c4c876 (+ job28 r_5..r_8) stays at t* = 1/5** [E, our engine; lower VALID; upper
  FEASIBLE d = 7..17 + DP + Karp]. The round 48 kills forbid the s13 binder, but a new 3-row dual appears at the same value:
  senders 66669 (3/5) and 56696 (1/5), and receiver d = 9 656566565/665656666 (1/5). Patterns: D 15,497, C 1,494, RPAT 158.
  s13r checks: lowerR VALID 217/1129, upperR FEASIBLE.
- **Two-engine (22:13Z): Studio passes s14 at 1/5** (32c82928; args byte-identical, dcount exact, all 3 rows rebuild). [E2]
- **P2 s14r (22:30Z): the relay class on 42c4c876 + r_5..r_8 gives t* = 19/102 = 0.1863**, down from 217/1129 [own
  checkers; lowerR VALID with 25 rows; upperR FEASIBLE, 0 sender and 0 conservation violations, d = 7..17 exhaustive, Karp
  d0 12.02; 53 iterations, 978 s].
  - Receivers: d = 7 7665566/6675666 (0.2353), d = 9 656565665/665666566 (0.0523), d = 10 6556656556/6665656665 (0.0163),
    and d = 9 656656665/665555555 (0.0131).
  - Senders: 55667, 66669, 55767, 56696, 56669, 55696.
  - Files are in `P_own_lp/s14/`.
- **P s12r (22:40Z): the reduced 6-centred relay (apex letters small/big) on argsA44 + RSST-D + L2 gives t* = 35/183 =
  0.19126**, below s10's 217/1129 on the same registry [own checkers. Lower VALID: 52 rows. Upper FEASIBLE: conservation
  holds on 1,424 6-links x 5^6 apex words, d = 7..17 exhaustive, Karp d0 11.94]. Kill line not met. V1 fallback
  reproduces 217/1129. The full exact-apex version is 158k x 91k rows and too slow for the window; its partial value is
  0.19101, not yet a bound.
  - Finding: sender 55757 has no 6-neighbour, so no 6-relay can reach it. Its row is y-only and tight.
  - 55767 and 57667 are reached by the 6-centred split.
  - Next (stage 13): a 7-centred analogue aimed at 55757, on the round 48 registry (s14/argsA47).
- **Two-engine (23:15Z): Studio's spec-only checker (written from RELAY_SPEC.md, 24c69bf8) passes s14r at 19/102.**
  Upper is FEASIBLE, including bounds, senders and conservation. Lower is VALID: all 25 rows rebuild, with reduced costs
  g[50016] = 2/17 and M[76667] = 8/17. **The relay line at 19/102 is [E2].** Note: the spec's by-d table (4.5) counts per kind;
  the union is 9,660/4,465/1,226.
- **P stage 13 (23:30Z), on argsA47 (own checkers, both sides):**
  - s12r47, the reduced 6-centred relay: **t* = 21/113 = 0.18584**, below s14r's 19/102.
  - s15, the s10 relay + 7-centred split: 19/102.
  - s15c, 6-centred + 7-centred: 21/113.
  - **Kill line met: the 7-centred split adds nothing.** 55757 has no dual weight in any of the certificates, so it is not what binds.
  - The top binder is still d = 7 7665566/6675666, at dual 0.23-0.25 with slack 0 in every run. u spends its whole budget as
    y/z to its fives w3, w4 and as relay h to its link 6s, and receives nothing (x = 0). Relieving it needs inflow into u from
    w0 or s2 (the 7s), or payment to w3 and w4 from their ring-2 side.
- **P2 s16 (23:40Z): main line on ab3f252b (argsA49) stays at t* = 1/5** [E, our engine; lower VALID; upper FEASIBLE,
  Karp lambda 0.5436]. 119 iterations, 2,067 s, with a long tail at the 1e-4 level after the x penalty came off. The new dual has
  3 rows: receiver d = 7 7665566/6665766 (2/5), senders 55667 (2/5) and 55767 (1/5). The receiver is a sibling of the relay's
  binder 7665566/6675666. It is still admissible under d43ba26a (argsA50, distinct D 15,550). s17 is running.
- **P s12r50 (23:55Z): the reduced 6-centred relay on d43ba26a (argsA50, k3x md5 = d43ba26a, newpat 15,550) gives
  t* = 23/134 = 0.17164** [own checkers. Lower VALID: 57 rows. Upper FEASIBLE: conservation worst 3.9e-15, d = 7..17
  exhaustive, Karp d0 12.20]. Top binder: d = 7 7665566/6675666 (dual 0.194, slack 0). Others: d = 7 7665666/6566565 and
  7655666/6756666, and d = 10 6565656565/6655666666 and 6556656556/6665656665. Senders: 66669, 55667, 55767, 56669, 66667.
  Stage 14 (7 -> 7 inflow, keyed by u's whole link; new jsep4 subtracts a per-link inflow table at the leaf; the sender pays
  the max over u's 2 unseen letters) is pre-registered, and run st14q is in progress.
- **P2 s17 (00:05Z 19 Oct): main line on d43ba26a gives t* = 1/5, with the same 3-row dual as s16** [E, our engine; lower
  VALID; upper FEASIBLE]. Reflection check: 7665566/6665766 and 7665566/6675666 are the same arrangement (canonical
  5566766/5666667). Rows are not stored canonically, since jsep3 breaks only rotation and psolve dedupes by coefficient key.
  Duplicates are redundant and do not affect soundness: the lower check rebuilds rows from labels, and the upper check is
  exhaustive.
- **P2 s17r (00:15Z): the s10-mode relay on d43ba26a gives t* = 31/178 = 0.17416** [own checkers; lowerR VALID with 25 rows;
  upperR FEASIBLE]. Top binder: d = 7 7665566/6675666 at 0.2247 (canonical 5566766/5666667). Then d = 10
  6565656565/6655666666, d = 10 6556656556/6665656665, and d = 9 655666566/666555555. On the same registry the 6-centred
  s12r50 is lower, at 23/134 = 0.17164.
- **Two-engine (00:18Z 19 Oct):**
  - Studio passes s16 and s17 at 1/5 (96890972, be2f93b9).
  - Studio's spec-only checker passes s17r at 31/178 (d667219b). All 25 rows rebuild; the only nonzero reduced cost is M[76667] = 40/89.
  - **Relay line at 31/178 = 0.1742 is [E2].** s12r50 (23/134) is being checked from §12.
- **P stage 14 (00:30Z): 7 -> 7 inflow + reduced 6-centred on argsA50 gives st14q = 23/134** [own checkers, both sides].
  **Kill line met: the binder 7665566/6675666 stays tight (dual 0.194, q = 0).** Reason: the only sender, w0, cannot see
  u's fives w3 and w4, since those are the 2 letters of u's link it misses, and every other letter it sees is a 6. So it must pay all
  similar 7-neighbours equally, and w0 is itself a 7 of the tight family (7665666/6566565 and 7655666/6756666 bind too).
  Paying this row needs radius-3 information: a two-step relay through the 6s w2 and w5, or a wider separator window.
  New separator bin/jsep4 (per-link inflow at the leaf) is in P_own_lp.
- **Two-engine (01:06Z): Studio's spec-only checker (from §12) passes s12r50 at 23/134** (139b490e). Upper is FEASIBLE,
  with receivers swept exhaustively, cons2 checked on 1,424 x 64, and senders and mrowR2 passing. Lower is VALID on all 57 rows.
  **The relay line at 23/134 = 0.1716 is [E2], our best K = 2 value so far.**
- **P2 s18 (01:50Z): main line on b88ed8b7 (argsA51, distinct D 15,844) stays at t* = 1/5**, with the same 3-row dual as s17 (binder 5566766/5666667) [E, our engine; lower VALID; upper FEASIBLE]. s18r and s18c are running.
- **P st15 run 2 (01:45Z): LP t* = 1/6, but the upper check FAILED, so the primal is unsound.** Cause (our bug): v6 kept
  conservation only on the 994 6-types that contain a five. A 6 with no five next to a 7 could then pass charge to the
  7 with nothing coming in. upperR2 caught it: 48 6-types, worst error 0.066. The run-2 lower bound (VALID, 128 rows) still bounds
  the sound class from below, so sound st15 t* is in [1/6, 23/134]. Fix st15f: conservation now covers all 1,424 non-R6
  6-types in the solver, the separator and the basis (22,126 rows). s16_struct.txt and RELAY_SPEC §13 are updated, and §13 now
  states that V[sig] = min over candV of v. Running since 01:41Z.
- **P st15f (02:05Z): the sound 6 -> 7 pass-on on argsA50 gives t* = 23/134** [own checkers; lower VALID with 107 rows;
  upper FEASIBLE, conservation on all 1,424 x 5^6 words, worst 3.2e-13; 927 s]. **Kill line met: the binder stays tight**
  (dual 0.194, V = 0). Why: the weight sits on V[7,5,6,6,6,5,7] <= v[...], the case where the private of the 6 at w2 is a 5.
  That 6 then has a second five to pay, and u takes the min over the private it cannot see. Per the round-50 census that
  case is reducible, but u's 2-ball cannot rule it out. Stage 16 needs reducibility information on the privates (radius 3):
  either drop killed private values from V's min using verified 3-ball patterns in the separator, or key v on the private's
  class.
- **P2 s18r (02:10Z): the s10 relay on b88ed8b7 (argsA51) gives t* = 9/52 = 0.17308**, down from 31/178 [own checkers;
  lowerR VALID with 45 rows; upperR FEASIBLE]. Receivers: d = 7 7655667/6756656 (new, 0.0865), d = 7 7665566/6665766 (0.0865),
  d = 10 6565656565/6655666666 (0.0385), plus small ones. s19c (6-centred) and s19r on 09d8ac38 (argsA52, dcount 15,855) are running.
- **P stage 16 (A) stopped at Long Table's check 4 (02:40Z): the registry-only private filter does not reproduce the
  census.** On the binder's 15,625 one-ring-out cases it leaves 12,320 survivors; the census has 3,072. The binding case is
  p5 = 5, where all of the private's known neighbours are 6s. Every registry pattern is a wheel centred at degree >= 7,
  so none can be centred where it would see p5. The census kills of p5 come from whole RSST configurations (rsst180 and
  others), tested one ring beyond u's 2-ball. Nothing was solved. §14, s16_census.py and s16_census_kills.json are committed.
  Next: confirm that the 6 census configurations are in the conservative 582 / k3x, then port them as a containment test
  at a link-6 private (A'), or fall back to option B.
- **P2 s19c (02:40Z): the reduced 6-centred relay on 09d8ac38 (argsA52) gives t* = 6/35 = 0.17143**, below 23/134
  [own checkers; lowerR2 VALID with 91 rows; upperR2 FEASIBLE, conservation 1,424 x 5^6, worst 1.3e-13]. Main binder: still
  5566766/5666667 (0.2). Then d = 10 6565656565/6655666666, d = 9 655566556/757656565, and d = 7 7655566/6759676,
  7676556/7759565 and 7666566/5656656 (1/35 each). s19r is running.
- **P2 s19r (02:55Z): the s10 relay on argsA52 gives t* = 37/214 = 0.17290** [own checkers; lowerR VALID with 45 rows; upperR
  FEASIBLE]. Top binder: d = 7 7765566/6575666 (0.159, new). The d = 10 row 6565656565/6655666666 survives r10a and binds in
  s18r, s19c and s19r, so it is the next kill target.
- **Two-engine (03:00Z): Studio's spec-only checker passes s19c at 6/35 = 0.1714** (50150249). Upper FEASIBLE: receivers exhaustive, DP and Karp clean. Lower VALID: all 91 rows. **Relay line at 6/35 is [E2], our best so far.**
- **P2 s20c (03:15Z): the reduced 6-centred relay on 8e008f86 (argsA53, dcount 15,877) gives t* = 8/47 = 0.17021**
  [own checkers; lowerR2 VALID with 41 rows; upperR2 FEASIBLE]. Receivers: 5566766/5666667 (0.2021), d = 10 6565656565/6655666666
  (0.0532), d = 7 8665566/5675665 (new) and d = 8 76566656/65566556 (new, 0.0319 each). Senders: 66669, 55667, 55767, 55686, 55696.
- **P2 s20r (03:30Z): the s10 relay on argsA53 is unchanged at 37/214** [own checkers, both sides]. Top receiver: 7665566/6665766 (0.159). The d = 10 row 6565656565/6655666666 still binds in both relay classes.
- **Two-engine (03:31Z): Studio's §12 spec-only checker passes s20c at 8/47 = 0.1702** (38de2a15; dcount identical; receivers d = 7..15 exact; all 41 rows rebuild). **The relay line at 8/47 is [E2], our best so far.**
- **Two-engine (03:39Z): Studio passes s19r and s20r at 37/214** (72851550, spec-only). Nothing of ours is waiting on Studio.
- **P stage 16 A' interim (03:45Z).**
  - The census configs (rsst025, 050, 052, 098, 180) are all in the conservative 582. The f7_ census name is in k3x_C 09d8ac38.
  - Check 4, with the full 3-ball test, gives exactly 3,072 / 15,625.
  - The projection that LP terms can see (window w_{j+-2}, s_{j-2..j+1}) gives 7,500. That is a weaker filter, and still conservative. It keeps p51 = 5, p51 = 6 and p21 = 5.
  - Filter off reproduces 23/134 (st15f), and argsA52 gives 6/35 (st16b0).
  - The filtered solve st16ap is at LP 6/37, but it is unconverged and unchecked, so it is not a bound.

## Stage 16 A′: unknown-vertex soundness check (Long Table's request), 19 Oct
- Rule (now in RELAY_SPEC §14′): a pattern counts as matched only when every vertex it constrains lies inside the readable window. If any constrained vertex is unknown, there is no match.
- Check 4 strict (LP-visible projection), unknowns coded 99, 5 and 7: 7,500 survivors in every case, same set md5 9b4d02ba. Control: the non-strict matcher at code 5 gives 3,072 (f2582478), so the rule bites.
- Kill tables regenerated strict, with unknowns at 5 and at 7: byte-identical to the tables st16ap uses (U7 27a64538, U8 = U9 6dc44bba). st16ap stands.
- st16ap is at iteration 36 with LP t = 6/37. This is interim only: d=7 separation is still adding rows (max violation about 0.08).

## Stage 16 A′ result, 19 Oct ~05:20Z
- Filtered 6-centred relay: t* = 6/37 = 0.1622 on argsA52 (09d8ac38). Lower check VALID (cert_st16ap2L.json, 211 rows); upper check FEASIBLE (sol_st16ap2.json). Same engine with the filter off gives 6/35.
- The filter is the LP-visible projection of the 3-ball test (7,500 survivors on check 4; the full 3-ball test gives 3,072). Strict unknown rule passes.
- Kill line (a) not met. Kill line (b) partly met: the binder is tight in the solution but has dual weight 0; the mrowV at the binder's w5 now binds at p51=7 (the survivor context).
- Cert support: d=7 7766556/6576576, 7676556/7756595, d=9 655665556/756567565; heaviest row M[9,5,6,5,6,5,5].
- Studio's spec-only upper check is running. This is our engine only until it passes.

## s21c: registry 880d25c6 (Studio; kills the d=10 binder), 6-centred relay, filter off, 19 Oct ~05:40Z
- t* = 86/515 = 0.16699. Lower check VALID (136 rows); upper check FEASIBLE (worst conservation 1.1e-13, Karp d0 12.26). Previous unfiltered best: 8/47 on 8e008f86. Our engine only; Studio check pending.
- The d=10 binder 6565656565/6655666666 has dropped out of the dual. Main receiver is now d=7 7765566/6575666 (0.144).
- Next: filtered solve (filt16) on 880d25c6, with kill tables regenerated strict on 582 + 1474 configs.

## s21f: 880d25c6, 6-centred relay with the §14′ filter, 19 Oct ~06:30Z
- Kill tables regenerated strict on 2056 configs (582 + 1474): byte-identical to s16ap/kill6, since the 47 new names add no local kills. Check 4: 7,500 survivors at unknown codes 99, 5 and 7 (md5 9b4d02ba).
- Bracket 4/25 <= t* <= 65/406 (0.16000 to 0.16010), checked on both sides on our engine:
  - Upper FEASIBLE: sol_s21f.json, keeppen fixed point.
  - Lower VALID: cert_s21fL.json, unpenalised LP over the same rows.
- Gap 9.9e-5, not closed. The bound that counts is the upper one: t* <= 65/406. Studio check pending.
- Cert binders: d7 7665566/6765766 (0.144), d7 7676556/7759565, d9 655566556/759556565, d10 6556655556/6665669665.

## Stage 17: face pool (5→5 across a 5-5-5 face, flag face5), argsA52, 19 Oct ~07:00Z. KILLED (null)
- t* = 6/37 exactly, with lower VALID (cert_st17fL, 177 rows). The upper bound carries over from sol_st16ap2 (the rule class contains the old one). The LP uses the rule (28 transfers positive) and gains nothing.
- Filter-off regression check passes: reproduces 6/35.
- Kill line hit: binder 7665566/6675666 and 7655667/6756656 stay tight (slack 0).
- Why it fails: moving charge among the three fives cannot help, because the ring around the face holds the same big vertices whichever five is paid. Any fix needs charge from outside that ring.
- Files: P_own_lp/s17d/.

## Stage 18: hat channel (flag hat5, RELAY_SPEC §15), argsA54 + §14′ filter, 19 Oct ~08:30Z
- Rule: a five sends r[K] to a big hat of it (five → big; prose corrected ee11d33e, rows unchanged). K is read identically from both ends (§15 table). Physical test: 100k random triangulations, 0 mismatches; broken-key control gives 15,898. Regression check with the flag off: 6/35.
- Bracket 10/63 <= t* <= 17/107 = 0.15888, both checked on our engine:
  - Upper: sol_st18h, FEASIBLE on itself.
  - Lower: cert_st18hL, VALID, 138 rows.
- Below s21f's 65/406. Studio check pending.
- Long Table's kill line (2) is hit: 7665566/6675666 and 7655667/6756656 both stay tight, with no r flowing into the binder. The bound improves, but the face family is still unpaid.
- Worker's recommendation: for this family, use a reducibility lemma (a 7 with a 5-5-5 face plus a nearby 5) rather than another rule extension.

## s22f: 5fa0adb0 (kills the d=8 binder), 6-centred relay with §14′ filter, no hat5, 19 Oct ~08:50Z
- t* = 4/25 = 0.16 exactly. Lower VALID (90 rows); upper FEASIBLE on our engine. Studio check pending.
- This closes s21f's bracket, but the value is still above stage 18's 17/107 (hat5 on 880d25c6).
- Next: hat5 on 5fa0adb0.

## Stage 19 oracle: face 7 + adjacent link-6 private 5 forbidden by assumption (flag w19), stage 18 setup, 19 Oct ~09:00Z. NULL
- Lower stays exactly 10/63 (VALID, 112 rows). Upper 197/1240 is FEASIBLE but sits inside the old gap, so there is no gain in t*.
- Kill line (2) met: the binder moves to 7766556/6567566, a face row whose face-adjacent 6s already have private 5 forbidden.
- Why it is null:
  - In all four face rows, the 7's whole budget goes through y to its two face fives: y7|5566 + y7|5576 = 1 + t. The link-6 privates never enter.
  - The y values are set by the face fives' worst sender contexts: 55667, 55669, 55767, 55769, with at most two big hats.
  - So a useful lemma must be on the sender side: a 5-5-5 face with its hat ring mostly small.
- Files: P_own_lp/s19d/.

## s22h / s22c on 5fa0adb0, 19 Oct ~09:20Z
- s22h, hat5 + §14′ filter: t* = 16/101 = 0.15842 exactly. Lower VALID (114 rows), upper FEASIBLE (Karp d0 13.20). Our engine only; Studio check pending. Below 17/107.
- s22c, unfiltered: 86/515, unchanged.
- Binders: face rows on top (d7 7665566/6765766 0.112, 7676556/7759565 0.066). Senders: 55667, 55669, 55769.
- Next: s23h on 35aeebb8 (kills the d=9 binder).

## Stage 19b: sender-side oracle (5 worst face-five contexts forbidden, flag wf19), stage 18 setup, 19 Oct ~09:30Z. NULL
- Result: lower bound stays at 10/63 (VALID, 127 rows) and the upper bound stays at exactly 17/107. Both kill lines are hit.
- The weight moves to sibling contexts of the same face (H0 flipped to big, other hat or fan classes). The certificate is degenerate across the whole hat/fan family of a face five.
- Conclusion: no small lemma on the sender or receiver side can help. Stages 17, 18, 19 and 19b all say the 5-5-5-face family needs either a large reducibility argument (no D/C kill was found at ring ≤16) or a change of method.
- Files: P_own_lp/s19e/.

## s23h: 35aeebb8 (kills the d=9 binder), hat5 + §14′ filter, 19 Oct ~10:15Z
- t* = 98/619 = 0.15832 exactly. Lower VALID (105 rows), upper FEASIBLE (Karp d0 12.70). Our engine only; Studio check pending.
- Kill tables are still byte-identical to before; check 4 is unchanged at 7,500.
- Top binder is now d7 7766556/6567566 (0.120). The face family still dominates.

## Sender-side admissibility gap (Long Table / explore question), 19 Oct ~10:30Z
- The 4 contexts explore flagged (55667 [0,1,0,0,0][1,1], [0,1,0,1,0][0,0], [0,1,0,1,0][1,0]; 55758 [0,0,0,0,0]) are dead on OUR registries too (5fa0adb0 and 35aeebb8). Every completion of the sender 2-ball contains a registry config: f10 Birkhoff diamond at the 5-5-5 face, f7_...5565_, rsst006 and others.
- Our LP still keeps them as live sender rows. Cause: the sender filter only checks R6 per 6-spoke wheel and never applies registry configurations. Sender rows are registry-independent.
- In cert_s22hL, 0.297 of the 0.677 total sender dual weight sits on 2-ball-dead rows.
- Next: stage 21, a strict sender 2-ball containment filter. Scripts are in P_own_lp/sndchk/.

## Stage 20: exact hat letters for sender admissibility (flag hatx, §16), s22h setup on 5fa0adb0, 19 Oct ~10:45Z. NULL
- 696 impossible contexts dropped (20,082 sender rows remain). Lower stays exactly 16/101 (VALID); upper is FEASIBLE at 0.158442 (penalty point). No gain.
- Kill lines (1) and (2) both hit. The face rows stay tight; r[506507] is the 7 paying the face's third five, i.e. outflow.
- The face family is admissible once H0 (the vertex across the face edge) is big.
- Stage 21 (the sender 2-ball registry filter) is a different and stronger test, and it is running.

## Stage 22 (design only): balanced/face initial charge, 19 Oct ~11:00Z. NULL by construction
- In a triangulation every face is a triangle, so balanced charges reduce to the current vertex charge or its mirror.
- The Euler family 6-(1+e/3)d with face charge e, and 5-5-5 shared charge, are pure re-basings with T=0. Free face-to-corner rules reduce to edge transfers that are already spanned. The reverse columns have reduced cost 0 on cert_st20xL. §18 written.
- Probe on family.json: the face 7 still binds at 16/101. Kill line met.
- Open lead (not built): the reverse hat channel (big to five at distance 2). Two r columns have positive reduced cost on cert_st20xL.

## s24h stopped; s25 prep on 0125c46b, 19 Oct ~11:40Z
- s24h on 4b28f532 was stopped mid-solve on Long Table's change of plan. It was at iteration 16 with t = 2/13, unconverged and uncertified. Not a bound.
- s25 on 0125c46b (1,897 D / 838 C, dcount 16,937, includes the r7h kill of 7676556/7759565): argsA59 built. Strict kill tables are byte-identical again; check 4 = 7,500. Ready for the stage 21 production run.

## Stage 23: reverse hat rr (big → five at distance 2, flag hatrr, §15r), s22h setup, 19 Oct ~12:00Z. NULL
- t* = 16/101 exactly. Lower VALID (115 rows). Upper: sol_s22h is FEASIBLE under the hatrr engine. Gain 0.
- rr carries real weight: 3.7 total, on keys (5,1,6,8), (5,1,5,9) and similar. Whatever the face 7 pushes out returns through y, and every face row stays tight.
- Engine gap found: upperR2 on sol_st23r itself is INFEASIBLE (6 conservation rows on no-five 6-links, worst 0.0078). Without v6, solveR2 separates conservation only over 6-words that contain a five. Earlier claimed bounds are unaffected, because each passed upperR2 over all 1,424 types. Future solves must either separate on all 1,424 or check upperR2 on their own solution (as they do).

## Stage 21: sender 2-ball registry filter (flag s2b, §17), s22h setup on 5fa0adb0, 19 Oct ~12:20Z. NULL
- 894 of 26,280 hat5 contexts dropped; 19,916 sender rows remain. Every context decided exactly; 16,548 also enumerated literally (0 disagreements). Domain sizes are in sdrop_ctx.tsv.
- Controls:
  - empty registry: 0 dropped;
  - degree+1 shift: 0 dropped, a different set;
  - witness recheck: 340 checked, 0 failures.
- Explore cross-check: we drop none of explore's 10 survivors. We keep 4 of its 16 dead contexts, which need windows not yet in the registry.
- Result: lower stays exactly 16/101 (VALID, 113 rows); upper is FEASIBLE at 61/385. Gain 0, so the kill line is hit.
- Sender dual weight (0.677) moves to H0-big siblings, the same degeneracy as stage 19b. Weight on registry-dead rows is now 0. Weight on explore-dead-but-kept rows is 0.076 (55767).
- Files: P_own_lp/s21s/ (the worker was blocked from writing to the repo; the lead copied the files in).

## Stage 24 (design + pricing): second-neighbourhood big-big columns (§19), 19 Oct ~13:10Z
- Both ends can read only two families: D (big to big apex across a diamond) and O (big to the big private of a 6-spoke). Physical test: 0 mismatches; broken-key control: 119,502.
- Pricing, exact, against cert_s22hL and cert_st23rL: 3 D columns price negative, all 9+ to 9+, relieving the d=9/10 binders (smallest reduced cost −8/303). The D(7↔9) columns sit at exactly 0, and every O column is positive. Nothing prices into the face 7 rows.
- No solve was run; one needs Long Table's go, and the solveR2 conservation gap must be closed first.

## Stage 24 solve attempt on 0125c46b (argsA59), 19 Oct ~14:40Z. UNCONVERGED
- New engine flags: consall (conservation separated over all 1,424 types; fixes the §19.5 gap) and big2 (the D family). D row-sum test: 0 mismatches. Regression with both flags off: 16/101.
- Baseline st24b and st24d (with D) both hit the 90-min cap. Neither has an upper bound.
- Both lower bounds are VALID at 2/13 with the identical 34-row cert. All D reduced costs are >= 0 against it.
- Binders: face 7 7665567/6765756 (0.231) and two d=10 rows. The face 7 does not bind alone.
- Re-run needs: D capped with a penalty, solves run one at a time, a longer cap, and warm starts.

## st24b: hat5 + §14′ filter + consall on 0125c46b (argsA59), 19 Oct ~17:05Z
- t* = 2/13 = 0.15385 exactly on our engine. Upper FEASIBLE on sol_st24b itself (all 1,424 conservation types pass, worst 3.1e-13). Lower VALID (36 rows). Studio check pending.
- This is the new best, below 16/101 [E2 on 5fa0adb0]. The new registry kills (d9 face row, r7h) are what moved it.
- Stage 24 D columns (capped at 3): t* stays at exactly 2/13 (the cert is VALID in the big2 class; D = 0 is feasible). Gain 0, kill line met.
- Binders: face 7 7665566/6675676 (0.231) and two d=10 rows (0.038 each).

## s28q: pricing of l3q (borrowed-channel note, dc954db3), against cert_st24bL, 19 Oct ~18:50Z
- One column is negative: q̂(7,7,6,6,5) = −6/13. It sits only on the face binder 7665566/6675676 and confirms the hypothesis exactly.
- Controls pass. Mask off gives 0. With the side swapped, coefficients go to 0. Physical test: 0 mismatches; broken control: 95,996.
- The note's p5=5 rsst003 kill does not reproduce, though the survivor count (6,400) matches.
- Next: solve with V=7 only (20 columns), so only d=7 needs the wider view. Gain is likely capped by the d10 rows, which Studio's r52j/r52k kills address.

## s29: st24b engine re-solve on 7360eb92 (argsA60), 18:52–20:10Z 19 Oct
- Inputs: dcount 17,030 parsed D (expected 17,030). Kill tables U7 27a64538, U8 = U9 6dc44bba, byte-identical to s25.
- Upper: keeppen solve converged; UPPER-R2 FEASIBLE at t = 0.153144115. sol_s29 3ea9511a.
- Lower: nosep over the warm rows gives LOWER-R2 VALID, t >= 43/281 = 0.153025 (83 rows). cert_s29L fe5193b4.
- Gap 1.2e-4, so the value is not exact. It moves down from 2/13 = 0.153846 by about 7e-4.
- Binders (L dual): the face 7 7665566/6675676 at 0.214 dominates. The two d10 rows are gone (explore's r52j/r52k kills). Small mass sits on 8 76656566/56655565, 7 8658656/6675556 and 8 75765656/66565555.
- Caveat: 7360eb92 still contains the three suspect ring-merge C entries. The validity check runs in s30h on 0125c46b−3 and 7a3857a0.

## s30h / s30t: held-out C validity and T1 (87d218f6), 19 Oct ~21Z
- s30h: sol_st24b stays UPPER FEASIBLE at 2/13 on 0125c46b minus the 3 ring-merge C entries (f7_..56757_...5..., f7_..65757_..55..., f7_..65757_..65...). It is also FEASIBLE on Studio's held head 7a3857a0.
  - cert_st24bL is VALID on the −3 variant, so 2/13 is still exact on 0125c46b−3.
  - Kill npy are unchanged (27a64538 / 6dc44bba).
- s29 correction: sol_s29 is INFEASIBLE on 7a3857a0. 47 d=7 rows break (worst excess 0.0446, e.g. 7576565/6658557), and every one is matched only by f7_..56757_...5....
  - So the s29 upper of 0.153144 rested on the suspect entry and is withdrawn.
  - On 7a3857a0 we have 43/281 <= t* <= 2/13. cert_st24bL is INVALID there, because the r52k D entries kill 2 d10 rows; cert_s29L is VALID there.
- s30t (T1, D only, all C removed): UPPER INFEASIBLE. 2,231,823 canonical rows break at d=7..10, with worst excess 0.71 (9556665/6855557).
  - 1989 of a 2000-row sample are repaired by cpat C entries, chiefly f10_/f9_/f8_ and f7_...5566_.....5..
  - Conclusion: K=2 unavoidability needs C (CGlue), and the hypothesis is confirmed.

## s26r: ball census around the face binder 7665566/6675676 (0125c46b, 3,317-config kill set), 19 Oct ~21Z
- Survivors, strict §14′ matching:
  - radius 2: 6,144 of 15,625;
  - radius 3: about 4.8e22 of 6.9e22, counted exactly by frontier DP with 88 controls and 0 mismatches.
  - Every r2 survivor extends to r3.
- With all surroundings 5/6: 3 survive at r2 and 0 at r3. So the registry forces an extra big within distance 3 of u.
- Tight case: privates 666666 with exactly one big in ring 3. That big must be t, the ring-3 vertex next to s2, s3 and s4, and adjacent to the face five s3. There are 29 survivors each for t = 7, 8 and ≥9, listed in tight29.txt and onebig.log.
  - All-6 except t = 7 gives ball sum Σ(6−d) = −2, i.e. spare capacity.
  - So the ball holds enough charge. The obstruction is sharing: t, s2, s5 and u serve other fives too.
- Ball-sum maximum: +1 at r2 (p51 = p61 = 5) and +7 at r3 (8-heavy ring 2 with boundary fives).
- No ball-sum test can rule out radius ≥ 3 rules.
- Cone criterion: a flat-lattice cone with no registry configuration and total charge in [1,5] would kill every local rule. 3 SA searches found none; the best had 4 hits. Not exhaustive.
- Verdict: inconclusive, which supports the rule-side route. Rules should let t or s3 see past ring 3.

## s27o: conditional-floor oracle, iterated binder forbids (no l3q), 18:13–22:13Z 19 Oct
- Round 1 forbids 3 binder arrangements: t* = 2/13 exactly (lower VALID, upper FEASIBLE).
- Round 2 forbids 6: lower VALID 0.152564, upper ≤ 2/13.
- Round 3 forbids 28: pool-only lower 0.137, not separated.
- The binder moves to near-identical rows each round: 7665566 → 7765566 → 7766556, and the d10 weight moves to the same row via another arrangement.
- Kill line hit: forbidding single arrangements does not approach 0, so kills alone are not the route. Rows have to be killed by coefficient class, or paid by rules; l3q (s28q) already removes the face-7 binder.
- These are oracle numbers, not bounds.

## s32p: pricing next rule families against the l3q cert (47/320, 7360eb92), 445989dc
- Hypothesis (a drule-shaped 8-channel pays the d7-with-8 rows) is refuted: every column touching 8658656/6665555, 8658656/6665556 or 8568656/6655555 has rc ≥ 0. The d10 row is untouched.
- Negative families, all relieving d8 rows:
  - Z, five→big with a hat-class key: −9/160;
  - ZR, its reverse big→five: −9/160 and −1/40;
  - RR, big hat→five across a diamond: −7/160 and −3/80.
- Null families: YR, O5/O5F, D, O, the generalised LG l3q, and VG.
- No negative column relies on the suspect f7_..56757_...5....
- Spec: s32p/RELAY_SPEC_s22.md (Z±, RR). Next: a capped solve with l3q + zh + ZR + hatrr. Expect gain to stop at the d7 and d10 rows.

## s34b: pricing borrowed-channel round 2 against cert_s28A60L (47/320), 9b3d19c0 / 329cc27f
- (A) z6/l6r, a 6 relaying to an adjacent 6: 22 of 68 keys price negative, exactly as LT predicted.
  - Best: K=(5,5,5,7,5,5,5) at −13/20, then (5,5,6,7,6,7,5) at −21/40.
  - Shared-σ composites reach −141/160.
  - All four controls pass.
  - It is independent of the suspect entry.
  - Spec: s34b/RELAY_SPEC_s23.md. Folded into the stacked s33z solve.
- (C) l3q 7→8: dead (rc +7/160, +7/80, 0). The mask-drop control turns them negative.

## s28q l3q: validity and newest head (04176194)
- On 7a3857a0 (suspect entries held out): sol_s28A60 is UPPER FEASIBLE at 0.147857 and cert_s28A60L is LOWER VALID at 47/320. So the l3q result does not need the suspect entries.
- On 3cfd7f18 (argsA62, dcount 17,437), keeppen + nosep give:
  - **0.146667 = 11/75 ≤ t* ≤ 0.147790**, one engine;
  - q weight 0.073–0.087.
- Binders of the 11/75 cert, each at about −1/15 or less:
  - d10 6565656565/6556666666;
  - d8 75666556/66666565;
  - d7-with-8 rows 8658656/6665556 and 8658656/7665555;
  - d8 76656566/56655565.
  - The face 7 is gone.
- Provenance note in RELAY_SPEC_s21.md: l3q restates RSST rule 9 (drule9) as an own rule, and any claim must name it.

## [E2] l3q on 3cfd7f18: 11/75 ≤ t* ≤ 0.147790, 20 Oct 01:08Z
- Studio's spec-only check (495f335a, loop/studio/opus_check/s28q_verdict.md) CONFIRMS both bounds:
  - upper FEASIBLE at 0.147790407823;
  - lower VALID at exactly 11/75.
- Studio's own masks match tab62_±1 on all 5,000 entries, under reading (A) of §21.4.
- rpatD (158 RSST raw patterns) is passed on the command line by cmd_s28.sh (`rpat=$B/rpatD.txt`), not in argsA62.
- Best two-engine bound so far, down from 2/13 = 0.1538. Provenance: l3q restates RSST rule 9.

## s25c: whole-face cluster rule (own family, RELAY_SPEC_s20.md incl. §s25c-g), 0125c46b
- Pricing against cert_st24bL: level 1 (flag fy) has z(7,5,5,6,6;…) at rc −3/13; levels 2–3 are infeasible to lift. Far-side-6 variant: null. "t pays s3": −1/13 only when t ≥ 9.
- Physical both-end test: 0 mismatches over 179k pairs; broken control 25,794.
- g7 kills: of the 10 names, only g7_-..655.._..65..._...5...... is visible to the LP. It makes h(7,5,6,5,7,6,5,7) price at −3/13, and cert_st24bL becomes INVALID under g7.
- Solves hit the 3 h cap unconverged (box at load 10–13):
  - fy: t* ∈ [226/1531 = 0.14762, 2/13];
  - fy+g7: [6/43, 2/13] (partial rows).
  - No upper bound.
- fy is our own rule. It cuts the face-7 dual from 0.231 to 0.094 in cert_st25yL.

## l3q-only on A67 (main 2c97e14d out/job30, 2,555 D / 1,097 C, dcount 17,595), s33z/run_A67/q66, 20 Oct ~04:27Z
- keeppen converged: UPPER-R2 FEASIBLE at t = 0.128957775 (sol_q66 6dd8178d).
- nosep: LOWER-R2 VALID at t ≥ 55686/438047 = 0.127123 (cert_q66L 096a717b, 401 rows).
- **0.12712 ≤ t* ≤ 0.12896, one engine.** Down from [11/75, 0.14779], because explore's r54 kills removed the old binders.
- 8666655/5677657 does not bind: no dual, slack 0.078.
- Top binder is face-7 7766556/6576576 at −0.071 (19% of receiver weight). Next come d7 7666655, 7667565, 7656666, 7766555, 7665567, 9656775, 8666565 and d9 755666556, each at about −0.016.

## s33z stacked (l3q + zh + ZR + hatrr + l6r + pcell k3p #1 [E2 guard]) on A67 (main 2c97e14d, 2,555 D / 1,097 C), 20 Oct 07:25Z — keeppen xpen=1e-3
- keeppen converged at iter 9 after a warm restart: UPPER-R2 FEASIBLE at t = 0.125836450687.
  - Run 1 hit its 3 h cap when the iter-17 simplex stalled. New option `lpmax`: past the limit, re-solve with IPM, then simplex.
  - Solution sol_s33 is 5ecddc80. Every column is ≤ 0.85; the families z, zr, rr, lq and z6 are each ≤ 0.055.
- nosep (IPM + simplex polish): LOWER-R2 VALID at t ≥ 0.103861775 (cert_s33L 6811771a, 1,718 rows, exact fraction 2336/2337 digits).
  - Priced with `ucap=100`: 372 uncapped columns at about 1e-11 noise are priced at a cap of 100, costing 5.3e-9 in total.
  - The claim is therefore for the family with every column ≤ 100; the largest value in use is 0.85.
- **0.10386 ≤ t* ≤ 0.12584, one engine, A67. The gap is the x-penalty.**
  - xpen = 1e-3 on x, D, lq, z, zr, rr and z6, all capped at 3.
  - Running now: keeppen at xpen = 1e-5, warm (s33z/k2_A67.sh), then nosep, lower and upper again.
- l3q-only on the same head (entry above): [0.127123, 0.128958]. The stacked upper is 0.003121 below the l3q-only upper.
- e87 re-priced against this cert (s33z/e87/A67, pricer38s = s38e pricer on the s33z engine, masks rebuilt on A67, 31 d7 payee rows).
  - Best composite rc and projected gain at cap 1/2:

    | Family | Variant | rc | gain ≤ |
    |---|---|---|---|
    | E1 | (control, = engine x) | ≈ 0 | — |
    | E2 | full | −0.008554 | 0.0043 |
    | E2 | win | −0.006066 | 0.0030 |
    | E3 | full | −0.010092 | 0.0050 |
    | LG8 | full | −0.000028 | 0 |
  - Controls: E1 against x gives 0 mismatches; the physical test gives 0.
  - No composite touches 8666655. That row is in this cert only as payee 8666655/7777666, with dual 1634/5844141 ≈ 2.8e-4. There is no K2 relief to take.
  - To be re-priced on the xpen = 1e-5 cert before any e87 port.

## 20 Oct 09:22Z — [E2] l3q on A67 CONFIRMED by Studio
- Studio spec-only check d4a91750 (loop/studio/opus_check/s33z_verdict.md): UPPER FEASIBLE at 0.128957775395, LOWER VALID exactly 55686/438047; Karp λ 0.5539; 0 table diffs vs reg_A67.
- **New two-engine bound: 55686/438047 = 0.127123 <= t* <= 0.128958 [E2]** on A67 (main 2c97e14d out/job30, 2,555 D / 1,097 C, dcount 17,595), l3q only (RSST rule 9 restatement; claim must name the source). Previous [E2]: 11/75 = 0.146667.
- One engine since: l3q+rpatN (35 confirmed 2026-set configs) 636/5071 = 0.125419 <= t* <= 0.125956 (s39o/run_n). fy-only >= 2/15 > 0.128958, so the own whole-face rule alone is strictly worse than l3q.
- 09:30Z status of the xpen=1e-5 keeppen (k2_A67.sh, `lpmax=60`, so every LP effectively runs on IPM at about 3 to 4 min):
  - iter 3: t = 0.125000; max violation 1.7 on cons, 6.4 at d8; about 2,300 rows added per iteration, about 15 min per iteration.
  - Its 3 h cap ends at 11:44Z.
- If it converges: resume_s33.sh redoes L, N, U, X, C and B on the new solution.
- If it does not (k2_fallback.sh):
  - nosep over every row, K2's included, for a tighter lower (run_A67/lower_s33L2.log);
  - then N, U, X (minus-89), C (ccover) and B (8666655) on the converged xpen=1e-3 solution, sol_s33 5ecddc80.
- Not automatic:
  - a minus-89 re-solve if X is INFEASIBLE;
  - the e87 re-price on a new cert.

## s35f fy (our whole-face rule, RELAY_SPEC_s20 level 1) vs l3q on A63 = A67 (identical k3x, kill tables, dcount 17,595), 20 Oct
- **fy-only is strictly worse than l3q on A63 = A67, since 2/15 > 0.128958.** fy-only round 1 (s35f2, 5 h cap, unconverged): nosep LOWER-R2 VALID t ≥ 2/15 (cert r1_cert_s35fL 8f28c05d). Its upper on the nosep solution is INFEASIBLE, so there is no fy-only upper; the l3q-only upper on A67 is 0.128958 (sol_q66). Rounds 2–3 were stopped and their rows kept.
- **fy priced against the l3q cert s33z/run_A67/cert_q66L (t ≥ 55686/438047):** P_own_lp/s35f/fyq/pricer35.py rebuilds the cert with the s33z engine (q66 flags), adds fy z columns (sender +1 per big spoke, receiver +1 per link five; keys verbatim from s25c), and runs a lifting LP over all same-coefficient sender contexts (26,280 contexts undeduped; 78 used by the 66 cert senders).
  - 37 fy columns have rc < 0. The most negative is z(7,5,5,6,6; h 0,0,·,·,0) at rc = −31300/438047 = −0.0715, from senders 55667 00000|11 and 00100|00. Lifting does not help: the best lifting is still −0.0715.
  - Cross-check: the fy port of the l3q engine (fyq/eng = s33z/eng + port_fy.py) gives cert_q66L LOWER-R2 INVALID with the same 37 negatives. Without fy it gives VALID 55686/438047, and the fy upper on sol_q66 (z = 0) is FEASIBLE 0.128957775, unchanged.
- Gate (≥ 0.002) passed, so l3q+fy was re-solved warm on A67 (fyq/run_fyq.sh, nice 15, threads 2):
  - keeppen fyq1 hit the 5 h cap at iter 13, unconverged. Penalised t is 0.12744 and the worst d7/d8/d9 violations are about 0.04.
  - nosep fyqL, lowerR2 and upperR2 are running unattended. Results land in fyq/lower_fyqL.log, fyq/upper_*.log and fyq/run.log ("DONE" line).
  - No l3q+fy bound yet. The pricing shows only that the l3q cert does not survive fy, not by how much t* rises.

## Round s39o: off-centre matching (offc) and whole-window raw patterns (rpatN, rpatN2, rpatN3)
- Spec: P_own_lp/s39o/OFFC_SPEC.md. Spec delta for Studio: P_own_lp/s39o/RELAY_SPEC_s39o.md. Engine: s39o/eng (a copy of s33z/eng plus offc.py and the rpatN loader). s33z/eng is untouched; s28q and s33z keep separate pcheck.py copies.
- Controls:
  - flag off reproduces A67 q66 byte for byte (55686/438047 ≤ t* ≤ 0.128958);
  - offc fires on the 7 off-centre configurations of the d12 row 555555555555/757575757575;
  - the networkx physical test has 0 mismatches over 955,500 pairs, and its broken control has 8;
  - rpatN oracle: 0 mismatches over 45 rows.
- A67, l3q only (FQ), keeppen t:
  - (i) rpatN: 0.125956, with nosep lower 636/5071;
  - (ii) offc: 0.128330;
  - (iii) offc+rpatN: stopped unconverged, flat at 0.125896, as directed.
  - offc alone gains only 0.0006, so it is not used further.
- rpatN2 (6,053 configs, 2,059 patterns) and then rpatN3: the whole 2026 set loop/k51/nl51_kc.txt, 8,200 configs, two-engine D, 2,287 patterns, md5 e153fc41….
- **A74 (95ba762d), l3q + rpatN3: 20/183 = 0.109290 ≤ t* ≤ 1/9 = 0.111111.**
  - Upper: FEASIBLE. Lower: nosep VALID, 160 rows.
  - That is 0.0148 below rpatN's 0.125956 upper and 0.0178 below q66's upper.
  - 10 binders, 8 of them d7. Their canonical keys are in s39o/run_n3_A74/binders_canon.txt.
- Stacked F + rpatN2/rpatN3: still unconverged.
  - The A70 run timed out with t flat at 0.1001.
  - The run_s3_A74 run on A74 is still going: t 0.0985 at iter 15, about 10 min per iteration.
- RSST 2.126 and 8406.123 are absent from every solve.
- s39o addendum: RELAY_SPEC_s39o.md §39.6 now covers everything Studio needs to reproduce the A74 l3q + rpatN3 pair:
  - source nl51_kc.txt (md5 b9bc6e8b…);
  - rpatN3.txt (md5 e153fc41…): 2,288 lines, which is 1 header + 2,287 patterns, with counts by d and the build rule;
  - head 95ba762d, the flags and the warm-row provenance;
  - the cert and sol md5s.
- Why 8,200 configurations give 2,287 patterns (s39o/rpatN_funnel.py):
  - 53 have no vertex of degree ≥ 7;
  - 5,956 have a centre but don't fit one 1.5-ball window: non-centre vertices must be exact 5–8 neighbours or apexes;
  - 2,191 embed, giving 42,998 embeddings;
  - dihedral and automorphism dedup leaves 2,455 (configuration, pattern) pairs;
  - 168 patterns are shared by two configurations, which leaves 2,287.

## 20 Oct 19:02Z — s35f fyq (l3q+fy on A67) ended without a bound
- keeppen hit its 5 h cap (t ≈ 0.1274), and the nosep stage hit its 5 h cap without writing a cert, so lowerR2 had no input (lower_fyqL.log: FileNotFoundError). Superseded by s40f (l3q+fy+rpatN3 on A74+).

## 20 Oct 20:40Z — s41c: C-cover of the A74 l3q + rpatN3 upper (sol_q39n3A74, FEASIBLE at 1/9), for Long Table / Studio Lean planning
- Setup = s39o run39.sh V=n3 REG=A74 upper stage (FQ + rpatN3, registry A74 = main 95ba762d, 2,645 D / 1,156 C). s39o/eng already carries the s33z options (noC, noCw, vK, vfile; prelay2.py identical to s33z), so nothing was ported. Controls: the upper re-run unchanged matches run_n3_A74/upper.log line for line (timings stripped).
- New: s41c/eng = s39o/eng + `ckeep=FILE` (with noC noCw, keep only the named C entries: cpat names, C 7-wheels c7_<word>, studio17 C wheels). Control: ckeep = every C name + full tables reproduces the base upper exactly (s41c/ctl_ckeep_all_cmp.txt). s39o/eng untouched.
- All C out (noC noCw, kill6/l3q tables rebuilt D-only: s41c/noC, RSST D2 only, k3x_C empty): **453,642 violations** = 453,640 receiver rows (d7 305,475, d8 82,724, d9 64,319, d10 1,122) + 2 conservation cells (links 556577, 566577, which become non-R6 once the studio17 C 6-wheels go).
- Covers per row (s41c/vrows_cover_A74.txt.gz): cpat/C 7-wheel matching (ccover41.py = s33z ccover.py + ring/Lean/per-row output), plus table kills: 22 C names sit behind kill6/l3q table kills (4 k3x f7 entries + 18 RSST C2cons; tabnames.txt); one upper per name with D-only tables + that name's kills gives its rows (tabname.py, batch2.sh). 655 C entries cover >= 1 row. 3,303 rows (d7 2,685, d8 618) have no single cover: they die only under several table kills together.
- **Sole-cover set: 104 entries** (91 k3x_C, 9 RSST C2cons, 2 other cpat, 2 C 6-wheels); greedy (ties to Lean-proved, then k3x) adds 25; the joint-table rows needed 1 more (rsst217_2o211701966; found by adding table names one at a time, aug41.sh). **Cover: 130 entries** (s41c/ccover_A74.txt, sole_A74.txt, ckeep_A74.txt).
- **Check: only the 130 cover entries kept (cpat via ckeep, tables = D-only + the cover names' kills): UPPER-R2 FEASIBLE at t = 1/9** (upper_check_cover.log). Negative control, first sole entry f7_..56565_....... dropped: INFEASIBLE (20).
- Lean status (CXRing 96 = out/lean_cxring/2a4bc4cf/entries.txt, CXInt 345 = out/lean_cxint/95ba762d/entries.txt, CWheels.lean): 98 of 130 proved (CXInt 73, CXRing 23, CWheels 2). Every k3x_C cover entry at rings 9–13 and 15 is already in Lean; **the 20 k3x_C entries not in Lean are all ring 14** (3 more ring-14 ones are CXRing). Not in Lean: those 20, 10 RSST C2cons (rings 11–13, table kills only), e7_B56656._6B.66.._1111110 (r14, job27 part01.cfast) and f9_....5565B_....6655. (r12, job28 r_1.cfast).
- By ring: 9:1, 10:6, 11:23, 12:38, 13:37, **14:24 (3 Lean), 15:1 (Lean), 16:0**.
- RSST 2.126 and 8406.123 are verdict=none and absent throughout. CPU nice 10, threads 1.

## 20 Oct ~21:05Z — [E2] A67 upper rechecked without the 10 NO-C job27 entries
- Removed Studio rmsweep2 NO-C entries (e7_B55B565_/e7_B56B565_..._1111111, ring 12; 6 in part00, 4 in part01) by disabling their headers in filtered copies; d7 distinct patterns 9709 -> 9699 (non-vacuous).
- upperR2 on run_A67/sol_q66.json, same FQ flags and tables: **UPPER-R2 FEASIBLE at 0.128957775395**, all d=7..17 exhaustive 0 violated. The [E2] pair 55686/438047 <= t* <= 0.128958 stands without them. Log: s33z/run_A67/no10/.

## 20 Oct 22:02Z — [E2] l3q + rpatN3 on A74 CONFIRMED by Studio
- Studio spec-only check (loop/studio/opus_check/s39o_verdict.md, 545aa972, merge 2c139411): UPPER FEASIBLE at 1/9 (d=7..17, 0 violators, Karp λ 5/9), LOWER VALID exactly 20/183; Studio's own rpatN3 build = our 2,287 patterns; tables = reg_A74.
- **New two-engine bound: 20/183 = 0.109290 <= t* <= 1/9 = 0.111111 [E2]** on A74 (main 95ba762d), rules l3q (RSST rule 9 restatement) + rpatN3 (u-centred patterns from all 8,200 two-engine-D configurations of the 2026 set, nl51_kc.txt). Previous [E2]: 0.127123..0.128958.
- C cover (s41c): 130 C entries suffice for the upper; 32 not yet in Lean (20 ring-14, 10 RSST C, 2 old cpat), in Studio's CCover batch. The upper holds without the 129 ring-merge cpat entries.

## Round s40f: l3q + fy + rpatN3 on A74 (partial, K hit its 4 h cap)
- Engine `P_own_lp/s40f/eng` is s39o/eng with `s35f/fyq/port_fy.py` applied to prelay2.py. The result is identical to fyq's prelay2, md5 04d18faa….
  - pcheck.py also gains `exname=FILE`, which drops C entries by name.
- Controls on A74, fy off: lowerR2 on cert_q39n3A74L gives VALID 20/183, with a byte-identical log. upperR2 on sol_q39n3A74 gives FEASIBLE 1/9.
- fy pricing against cert_q39n3A74L (`s40f/pricer40.py` → `pricer40.out`): INVALID, with 4 negative z columns.
  - Most negative first: z(7,6,6,6,6;0,·,·,·,1) −10/183, then three at −2/183.
  - **None touches a cert receiver row, including all 5 face rows.**
  - The face rows' own fy keys have rc 2/183 or 0. At level 1, fy masks h2, the face apex's private t, which is what the face rows hinge on.
- K (`s40f/run40.sh`: warm from the n3 A74 rows, fyq1 rows and the q66 set; nice 5, threads 2, lpmax=300) hit the 4 h cap at iter 23.
  - t was flat at 2/19 = 0.105263 and the worst violations were still 0.4–1.1.
  - The IPM-fallback iterations gave violations up to 5, and at iter 17 separation took 5,000 s, d17 alone 3,275 s.
  - Rows are checkpointed in `s40f/run/rows_q40fy_partial.txt` (145,517 LP rows; run40.sh resumes).
  - No fy pair yet, so the kill line can't be evaluated.
- Heads: the coordinator moved the head A75 → A76 → A77 → A78 (b6dc7610) during K, which kept running on A74 under the head policy.
  - Registry `s33z/reg_A78` is built. The partial A76 and A77 preps were stopped and removed.
- Ring-merge hold-outs (`s40f/exname_rm128.txt`): 129 FAIL lines of out/job30/ringmerge_cpat_sweep.out, minus f9_....5565B_....6655. (kept), leaving 128.
  - e7_B56656._6B.66.._1111110 is not a FAIL line.
  - On A78, 128 entries are dropped: job27 part00 69, part01 59.
  - On A78 + exname, upperR2 on the A74 n3 sol (no fy) is still **FEASIBLE at 1/9**.
  - The n3 cert has 4 rows killed on A78, so a new lower is needed.
- PID 6187 (fyq A67 nosep) was not stopped; it ended at its own 5 h cap. RSST 2.126 and 8406.123 are absent from every solve.

## Round s43: fy cluster level 2 (fy2, face apex private t), built + priced on the A74 cert: kill line NOT passed
- Spec first: `P_own_lp/s43/RELAY_SPEC_s43.md` (sha ccb15e11), with results added in §43.6.
  - Faces are w_i = w_{i+1} = s_i = 5, and t_i is s_i's fourth neighbour. Lemma: h2 of both face fives is t_i.
  - A five in two faces is R5.
  - The z key unmasks h2 at faces. Receiver rows split into cells (c2(t) per face, R5-filtered at s_i, never empty).
  - The separator window holds the per-five UB. The new jsep6 couples the two face fives exactly at the leaf.
- Engine `s43/eng` = s40f/eng + `port_fy2.py` + jsep6, behind the flag `fy2` (needs `fy`).
- Control (a), fy2 off on A74:
  - lowerR2 on cert_q39n3A74L gives VALID 20/183, byte-identical log;
  - upperR2 on sol_q39n3A74 gives FEASIBLE 1/9, identical modulo timings.
- Control (b):
  - `phys43.py`: 253,282 (five, big) pairs on 67,603 explicit rotation systems, 0 mismatches. The broken-t control has
    18,353 mismatching rows.
  - `sep43chk.py`: jsep6 face coupling against an independent max over cells, 800 rows, 0 mismatches.
- Pricing against cert_q39n3A74L (`pricer43.out`): **the face-restricted lifting is feasible (rc 0)**.
  - All 5 face rows sit in their t-small cell. Every sender paying a face key has t small.
  - The face keys' rc are +2/183 or 0. The 4 negative columns are the sender-only ones from s40f (−10/183 and 3 × −2/183).
- Exploratory (`pricer43p.py`): unmasking the far-side 6's private as well (2P), and adding the visible 6 fan (2P+fan),
  leaves the face lifting feasible.
  - The cert pays each face row with fives of exactly that face five's context, so no five→big refinement can price
    negative there.
  - Moving the face rows needs a transfer out of the face 7, or exact letters.
- No solve was run: step 4 is gated on the kill line. CPU: nice 10, threads 1. s42a was untouched. RSST 2.126 and
  8406.123 are absent (no new patterns).
