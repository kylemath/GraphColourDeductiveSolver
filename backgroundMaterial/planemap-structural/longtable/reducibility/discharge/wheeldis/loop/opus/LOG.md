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
