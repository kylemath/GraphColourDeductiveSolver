# P: own fast LP engine (jsep2 row generation) for the K = 2 bound (18 Oct 2026, from 17:55Z) [E when converged + checked]

## Pre-registration (17:57Z, before any run)
- Question: can jcheck2's `solve` with jsep2 as exact separator reach TRUE convergence (no violated receiver row at
  any d = 7..17, Karp/relaxed tail to d = 30, checked by `upper`) on (1) round-13 args, (2) + Job 30 run-A kills
  (x = 0, then L2 x), (3) + rule T, faster than Studio's 25-66 min per iteration?
- Guess: (1) reproduces 7/27 in < 15 iterations, < 20 min; (2) x = 0 stays 7/27 (the kills only bite through
  transfers, per H/G); with L2 it lands near Studio's 0.228 lower bound or slightly above; (3) rule T lowers it
  further but not to <= 0 (explore's first-order floor ~0.054 at (6,6)).
- Plan-changer: (1) fails to give 7/27 -> a semantics mismatch, stop and report it before any new stage;
  (2) x = 0 already < 7/27 -> the kills act directly; (3) t*_T <= 0 -> drop everything, verify exactly.
- Every value below is reported as [lower] unless the converged primal passes `jcheck2 upper` and the dual passes
  `jcheck lower`.

## Stage 1 (18:08Z): round-13 args reproduce t* = 7/27 [E, both sides]
- `pcheck.py solve2` (jcheck2 copy + `psolve.py`; separator `bin/jsep3` = jsep2 + mode 2: the K = 300 most violated
  DISTINCT rows per d, exhaustive with cut max(thr, K-th best); highspy warm-started re-solves). Args
  studio/lp-upper feascheck.args, excl = hr1_or1, warm tight_13 (1,369 admitted). **33 iterations, 319 s**, last
  iteration adds 0 rows at every d = 7..17; 14,370 rows (`s1.log`).
- Dual: 10/27 sender 55667, 5/27 55767, 2/27 77777, 10/27 receiver d = 7 5675765/6577575 (= j28_13).
  `jcheck.py lower` (J's, unmodified): VALID t >= 7/27 (`lower_s1.log`). `jcheck2.py upper` (J's, unmodified) on the
  primal: FEASIBLE, 342 senders, d = 7..17 exhaustive, d = 18..30 DP, Karp lambda 0.5035 (`upper_s1.log`).
- Studio's equivalent validation (t0val) took 339 iterations.

## Stage 2a (18:10Z): run-A kills, x = 0: t* = 7/27 [E, both sides]
- Registry `argsA.txt` = feascheck.args + out/job30/addA_dfast18.out + k3x_D.out (3 D) + k3x_C.cfast (11 C, incl. the
  ring-16 n1 kills f7_.557657_.56.77. and f7_5567567_56.77.6) + `k42map_C_cons.cfast` (round 42's 10 conservative C
  windows on w2/w4 frames; the 2 broad-X RSST 126.8168 windows left out). 24 new d = 7 patterns (9,344).
  RSST-D (158 raw sep3 patterns, loop/studio/rsstD) NOT loaded (other encoding; patterns only lower t*, and Studio's
  rD1 left 7/27 unchanged).
- 21 iterations, 208 s, warm from tight_13 + stage-1 rows. t dipped to 0.2314 at iteration 0 (the kills remove
  warm binders) and climbed back to 7/27.
- Dual: 10/27 senders 55667 + 5/27 55767 + 2/27 77777 + 10/27 receiver d = 7 7576556/7767566 (row R again; the old
  representative's filling is killed, another filling of the same row survives). `jcheck lower nox`: VALID 7/27;
  `jcheck2 upper`: FEASIBLE. Without `nox` the certificate fails on x[1526] (-20/27): an L2 transfer can relieve R.

## Bug found in J's rule-T key functions (18:30Z) [E] -- affects `jcheck2.py upper` in rule-T mode only
- `ykey`/`tkey` in J_lp_checker/jcheck.py and jcheck2.py: after `if rv < raw: raw, ... = rv, ...` the next line
  `if raw == rv:` is then always true, so every reflected key also gets the palindrome flag/side swap. Effect: e.g.
  raw (7,8,9,7,6) side e becomes ((7,6,7,9,8), 0, 1, 'e') -- a flag on a non-6 spoke. With the bug: 1,377 Y and 453
  T keys, 174 T keys that no receiver can ever take in (free charge dumping: unsound for an upper check). Fixed in
  `pcheck.py` (`elif`): **1,356 Y + 444 T, equal to Studio and G**, every T key is an inflow candidate, and the
  orientation test (key read both ways, 12,500 raw/flag cases, Y and T) gives 0 mismatches. J's y/x-only results
  (7/27 checks) are unaffected; J's T path was never used on a real solution. **Any T-mode check must use
  P_own_lp/pcheck.py, not J's jcheck2.py.**
- Rule-T inflow in the LP: one auxiliary M_b >= T[k] for every inflow candidate k of root letter b (279 rows), and
  each inflow slot charges M_b: the conservative max of G's spec as linear rows (lazy argmax completions stalled).

## Stage 2b (18:37Z): run-A registry + L2 (xcap 3): **t* = 1/4 exactly** [E, both sides]
- `solve2 xon xcap=3 xpen=1e-3`: the LP runs with cost 1e-3 per unit x until no row is violated, then the cost is set
  to 0 and the loop goes on until a pass adds 0 rows. Without the penalty (`s2x_run1.log`, 12 iterations, 17 min)
  x ballooned and violations fell slowly (13 -> 4). With it: 32 iterations, 362 s (plus warm rows from run 1), 50,723
  rows, 6,355 columns. The last pass adds 0 rows at d = 7..17. Tail: relaxed DP holds at d = 18..30, Karp lambda 0.5086.
- Dual (`cert_s2x.json`): 1/4 sender 55688, 1/4 sender 66668, 1/8 sender 55858, 1/8 sender 58668, 1/4 receiver
  d = 8 85556565/65866655. No x enters the certificate. `jcheck.py lower` (x coefficients ON): VALID t >= 1/4.
  `jcheck2.py upper` (x path): FEASIBLE; d = 7, 8, 9 tight (0.0); d = 10 -0.009; Karp d0 = 11.7.
- Below 7/27 = 0.2593. Studio's run A (smaller registry: 3 D + 9 C) is at a lower bound of 0.2281 after 8 iterations.
  Not the same registry: ours adds the 2 ring-16 n1 kills and round 42's 10 conservative k42map windows.

## Stage 3a (18:40Z): run-A registry + rule T (option B), x = 0: **t*_T = 1/4 exactly** [E, both sides]
- `solveT` (1,077 deduplicated sender rows over coupled flag assignments, 1,356 Y + 444 T, 279 M rows), warm from
  stages 1-2. 27 iterations, 608 s on 1 thread (in parallel with 2b). The last pass adds 0 rows; tail DP holds; Karp
  lambda 0.5521, d0 = 12.8.
- Dual (`cert_s3.json`): the same five rows as 2b: 1/4 senderT 55688, 1/4 66668, 1/8 55858, 1/8 58668 (flags all
  0), 1/4 receiver d = 8 85556565/65866655. `pcheck.py lowerT` (exact; sender rows re-derived from word + flag bits,
  receivers re-derived, M rows checked against the inflow candidates): VALID t >= 1/4. `pcheck.py upper` (fixed keys,
  T mode, exhaustive d = 7..17): FEASIBLE; d = 7-10 tight.
- So rule T and L2 each take R's 7/27 row away and both stop at the same d = 8 wall at 1/4. The new binder is u of
  degree 8, link 85556565 (an 8 plus three and two fives), s-word 65866655, held up by the sender rows 55688/66668/
  55858/58668.

## Stage 3b (18:50Z): run-A registry + rule T + L2 (Job 30 B's model class): **t* = 1/4 exactly** [E, both sides]
- `solveT xon xcap=3 xpen=1e-3`, warm from all earlier rows: 20 iterations, 215 s, 54,972 rows, 7,846 columns; the
  last pass adds 0 rows; tail DP and Karp (lambda 0.5208, d0 = 12.0) hold.
- Dual: the same five rows (senders 55688, 66668 at 1/4; 55858, 58668 at 1/8; receiver d = 8 85556565/65866655 at
  1/4). `lowerT xon`: VALID 1/4. `pcheck upper` (T + x): FEASIBLE, d = 7..10 tight.
- Reading [I]: the d = 8 row is reached by neither T nor L2. Its fives read only sender rows whose bigs are 8s, so
  the next lever is a kill of 85556565/65866655 (or of its senders' frames) or a rule that sends past an 8.

## Control (18:59Z): Studio's exact run-A registry + L2 converges to **1/4** [E, both sides]
- `argsA_studio.txt` = feascheck.args + addA + k3x_D (3 D) + the 9 C that were loaded at A's launch
  (`k3x_C_runA9.cfast`, which is k3x_C.cfast without the two ring-16 n1 windows). 21 iterations, 256 s. Same
  five-row dual. J's `jcheck lower` (x on): VALID 1/4. J's `jcheck2 upper`: FEASIBLE.
- So Studio's run A (lower bound 0.2281 at iteration 8) should converge to exactly 1/4. Neither the ring-16 kills
  nor round 42's windows move the optimum.

## Summary and guess check
| stage | registry / model | t* | status | time |
|---|---|---|---|---|
| 1 | round 13, x = 0 | 7/27 | lower + upper | 33 it, 319 s |
| 2a | + run-A kills, ring-16, k42 cons, x = 0 | 7/27 | lower + upper | 21 it, 208 s |
| 2b | same + L2 (xcap 3) | 1/4 | lower + upper | 32 it, 362 s (+ 17 min unpenalised start) |
| ctrl | Studio's run-A registry + L2 | 1/4 | lower + upper | 21 it, 256 s |
| 3a | 2a + rule T (option B), x = 0 | 1/4 | lower + upper (own T checker) | 27 it, 608 s, 1 thread |
| 3b | 2a + rule T + L2 | 1/4 | lower + upper (own T checker) | 20 it, 215 s |
- Guesses: (1) right (7/27 in < 15 min). (2) right for x = 0 (7/27). For L2, "near 0.228" was wrong: it is 1/4.
  (3) "T lowers further, not to <= 0" was half wrong: T gives 1/4 on its own, and T + L2 stays at 1/4.
- The 1/4 wall is the d = 8 row 85556565/65866655 with senders 55688, 66668 (1/4 each) and 55858, 58668 (1/8 each).
  Stage 4 (S-lite, Q_rule_class) was not built for lack of time. Sender 66668 binds with both T flags 0 (z small), so
  S-lite's fan route O through the 6 is the one candidate that could reach it.
- Caveats: floats in the primal (tight rows at d = 7-10 sit at 0.0). RSST-D's 158 raw patterns are not loaded in
  stages 1-3 (lead's correction: leaving them out keeps the upper side but not the lower; see stage 4a). The rule-T upper check is P's (J's code with the key fix), not an independent
  second engine for T.

## Stage 4a (19:15Z): + RSST-D (158 raw sep3 patterns), rule T + L2: **t* = 1/4** [E, both sides]
- `rpat=rpatD.txt` (Studio's loop/studio/rsstD/out/rpatD.txt): decoded as d, k, then (five position i, 20-bit mask
  over (w_{i+1}, s_i, s_{i-1}, w_{i-1}) x 5 letter bits, wlp3.mask), w_i = 5 implied; expanded over all 2d
  symmetries. Loaded 158 new patterns (27 / 55 / 76 at d = 7 / 8 / 9). They are active: of stage 3b's generated
  rows, 152 of 1,790 (d = 7), 251 of 2,212 (d = 8) and 1,413 of 1,946 (d = 9) are now forbidden.
- No RSST-D pattern forbids the binder 85556565/65866655 (`admissible` = None) or R's 7576556/7767566.
- solveT xon + rpat (`s4a.log`): 11 iterations, 156 s, the same five-row dual, so t* = 1/4.
  `lowerT xon rpat`: VALID 1/4. `pcheck upper nomax rpat`: FEASIBLE (342 senders; d = 7..17 exhaustive, 0
  violated; d = 18..30 DP; Karp lambda 0.5417, d0 = 12.5) (`upper_s4a.log`). The per-d max-load printout is slow
  at d >= 15 with the RSST patterns (`upper_s4a_partial.log`), so this check skips it.

## Stage 4b (19:30Z): S-lite (rule T + fan route O) + L2 + RSST-D: **t* = 1/4** [E, both sides, own checkers]
- `pslite.py` (Q_rule_class spec; option B small/big). Flags per 6-spoke F = 2[A big] + [O big]. Keys Y(raw, Fa,
  Fe) and S(raw, Fa, Fe, side, pos), canonical under (B,e,c,b,a) with the flag pair and side swapped together (also
  in the palindromic case). Senders: every small/big class of each hat next to a 6-spoke and each 6-spoke's fan,
  coupled through non-R6 6-wheels: 3,312 sender rows, 2,409 Y, 1,188 S_A, 1,188 S_O. Receiver inflow at a link 6
  w_j: I1 (s_j = 5, root w_{j+1}), I2 (mirror), I3 (p_j = 5 allowed by the 6-wheel, roots s_j / s_{j-1}, u = fan).
  Each slot charges the max over its candidate keys (36 signatures, 2,376 M rows, every S key receivable).
  Conservative: max over the unseen letters (p_j, m, n, far flag), with I1/I2/I3 maximised separately.
- Validation. (i) Orientation test: 50,000 raw/flag cases x sides x pos, 0 mismatches. (ii) Fan off (`nofan`)
  reproduces rule T exactly: 1,077 rows, 1,356 Y, 444 S_A, 444 M rows. Its LP gives 1/4 (`s4b0.log`, 33 iterations,
  1 thread; lowerS VALID), with an alternative five-row dual. (iii) Plant S_O > 0.3 + `dbg`: the separator's window
  value equals the generated row's value on the top violator at d = 7 and 8 in every iteration (`splant.log`).
- Full run (`s4b.log`): fan on, xon xcap 3, rpat, warm stages 3b/4a/2b: 35 iterations, 468 s on 2 threads. The last pass
  adds 0 rows; tail DP holds; Karp lambda 0.5773, d0 = 13.6. `lowerS xon rpat`: VALID 1/4 (`lower_s4b.log`).
  `upperS rpat`: FEASIBLE: senders, d = 7..17 exhaustive, tail, all S > 0 keys receivable (`upper_s4b.log`).
- Dual: 1/4 sender 55688 (flags 0), 1/4 sender 66668 with hats all small and fans (0,1,1,0), 1/8 55858, 1/8 58668,
  1/4 receiver d = 8 85556565/65866655. In 66668 the 8 sits between two 6-spokes whose hats and fans are all small
  (only the two far 6s have big fans, and those reach no big root), so that five has no T or O route and pays only u.
- Reading [I]: the 1/4 wall is u = 8 with five link fives (w1, w2, w3, w5, w7; their words 55688 twice, 55858,
  58668, 66668), whose only big neighbours are u, w0 = 8 and s2 = 8. The certificate pairs u's row with those five
  sender rows. To go further: a kill of
  85556565/65866655 (it takes no RSST-D pattern), or a route out of 66668 that reads small hats and fans (rule C, or
  6-decides relays), or option-F letters.

## Stage 5 spec (19:40Z, before any run)
**(a) Exact letters (S-lite_F).** Same geometry as 4b. Each read target letter is kept as an exact class in
{5,6,7,8,9+} instead of small/big. Flag of a 6-spoke side F = (c(A), c(O)); a non-6 spoke gets (-1,-1); with the fan
off, c(O) = -1. Keys and canonicalisation are as in 4b (tuples compare lexicographically; the reflection swaps
(Fa, Fe) and the side, the palindrome takes the lexicographic min, pos is unchanged). Orientation test is required.
- Senders enumerate only the target slots some key reads: h_j and f_{j+1} for a 6 at l_{j+1}, h_{j-1} and f_{j-1}
  for a 6 at l_{j-1}, j a big root. The coupling is existential over the unread hats and fans: each 6-spoke wheel
  (5, l_{k+1}, h_k, f_k, h_{k-1}, l_{k-1}) must be non-R6 for some letters agreeing with the read classes. Route
  A / O pays iff the target letter is >= 7.
- Inflow signatures now carry the receiver's own letter (u is the A or O target): I1/I2 ('A', B, c(U), c(O)) and
  I3 ('O', B, b, c(A), c(U)); the M_sig rows are over all candidate keys.
- Pre-registered guess: t* = 1/4, unchanged. Hand reason: in u's row every target letter that w5's (66668) keys read
  is fixed (A = w7 = 5, O = s6 = 5; A = w3 = 5, O = s3 = 6), and so are w7's and w3's u-side flags. The exact
  assignment that u's row shows is realisable (u's row is admissible), so each certificate row stays a genuine row
  with the same coefficients.
- Plan-changer: t* < 1/4 means the certificate needed a small/big merge of two exact letters; report at once.
**(b) Small-hat route (route C, hat(x, y)).** For the binding five w5 = 66668 in u's row, x in {w4, w6}, the C
targets are p4 and p6 (the privates of w4 and w6). The row allows p4 in 5..9 and p6 in 6..9: (8,5,5,5,6,5) is R6,
the other letters are not (`r6.py`). So the adversary can keep C small. w0 and s2 lie at distance >= 3 from w5 along
non-big paths. Within the 2-ball of w5 the only big vertex the row forces is u.
- **Obstruction claim [hand]:** no sender-2-ball rule (routes A, O, C through any 6-spoke) gives w5 a route in
  u's worst case. u -> w0 by L2 is self-paired: the edge's side codes read (5,6,5)/(5,5,6) from both ends, so
  x_in = x_out at u.
- So (b) is not built. The levers left are a kill of 85556565/65866655 (exact s-word, privates open), or a transfer
  type that tells u from w0 using letters outside the current side codes (u's 5-five link).

## Stage 5a (19:45Z): exact letters (T_F, fan off) + L2 + RSST-D: **t* = 1/4** [E, lower; upper by inclusion]
- `pslite.py exact nofan`. Senders enumerate only the read target slots; coupling is existential over the unread
  ones (in B mode this reproduces 4b's counts exactly: 3,312 / 2,409 / 1,188 / 1,188 and 1,077 / 1,356 / 444).
  Exact, fan off: 14,766 sender rows, 3,048 Y, **2,007 T (= G's full-letter count)**, 9 signatures, every key
  receivable. Orientation test (exact, fan on): 1,953,125 cases, 0 mismatches. Exact with the fan on would need
  612,951 sender rows; not run.
- 32 iterations, 311 s. Dual: the same 5 rows (exact flags 5 everywhere). `lowerS exact nofan xon rpat`: VALID 1/4.
  Upper: the 4a primal is feasible in this larger class (the exact keys take their small/big values). Kill line
  (LOG O4) met: **exact letters are dead for this binder**, as pre-registered.

## Stage 6 (19:57Z): + explore round 43's C kill of the d = 8 binder: argsA + L2: **t* = 5/21 = 0.2381** [E, both sides]
- f8_...55565_...5.... (ring 10, C on two engines, conservative X I0-I1; loop/k43/kills.txt on
  origin/claude/project-thread-nh6pv2, f1f71335) as cpat `k43_C.cfast` (`argsA6.txt`). It forbids
  85556565/65866655 (and 65866555).
- `solve2 xon xcap=3 xpen=1e-3`: 51 iterations, 530 s. J's `jcheck lower`: VALID t >= 5/21. J's `jcheck2 upper`:
  FEASIBLE (342 senders, d = 7..17 exhaustive, DP to 30, Karp d0 = 11.7); d = 7, 8, 9 tight, d = 10 -0.048.
- Dual (25 rows, broad): receivers d = 7 8556855/7565666 (4/63), 8567655/6655656, 8655675/5866555,
  7557656/8585665 (1/63); d = 8 75565756/75666565, 76565565/56568565, 75656575/56665555, 76556565/58565765,
  85556565/66866665 (2/63 each). The same link 85556565 survives with s-word 66866665. Senders 56687 (8/63), 55667
  (6/63), 55668, 66668 (4/63), 55687, 55778, 55787, 56667, 56686, 56688, 56858, 56867, 58668, 66678 (2/63), 55868,
  66667 (1/63).

## Stage 6t (20:05Z / 20:11Z): T + L2 + RSST-D + k43 [E, both sides]
| run | registry | t* | lower | upper | time |
|---|---|---|---|---|---|
| s6t | argsA6 (one k43 C window) + RSST-D | 14/59 = 0.237288 | lowerT VALID (19 rows) | FEASIBLE | 30 it, 293 s |
| s6t43 | argsA43 = argsA + all of k43 (184 D `k43_kills_df.out`, 198 C `k43_kills_cf.cfast`, from c5a71dc0) + RSST-D | **11/47 = 0.234043** | lowerT VALID (24 rows) | FEASIBLE (d0 = 11.8) | 18 it, 186 s |
- s6t43 dual: receivers d = 7 7565765/6855555 (4/47); 8566655/6656656, 7557565/6566666, 8558655/6665666,
  7557656/6565665, d = 8 76565565/57765865 (2/47); d = 8 75657565/66656665 and /55655565 (1/47). Senders 56687
  (6/47), 55677 under flags 0 and 1 (4/47 each), 55667, 55668, 55687, 56667, 66667, 66677, 66678, 67768 (2/47), 55868
  (1/47); M rows on T keys (7,6,5,5,7), (7,6,6,6,6), (7,5,6,6,6), (8,6,7,7,6), (7,6,6,6,8).

## Stage 5a on the k43 registry (20:19Z) and the no-T baseline s7 (20:29Z) [E, both sides]
- s5a43 (exact letters, T_F + L2 + RSST-D + k43): 25 iterations, 274 s, **11/47**. `lowerS` VALID 11/47, 26 rows,
  the same receivers and senders as s6t43 with exact flags. The upper bound follows by inclusion (s6t43's primal).
  So exact letters are dead on the new binders too.
- s7 (`argsA43noT.txt` + rpat, L2, no rule T): 37 iterations, 363 s, **11/47**. `pcheck lower` (J's cmd_lower + rpat
  loader): VALID. `pcheck upper nomax`: FEASIBLE. Dual: 55677 (8/47), 56687 (6/47), receiver d = 7
  7565765/6855555 (4/47), and the same remaining rows as s6t43 (d = 7 8567655/6655656 replaces 8566655/6656656).
  **Rule T adds nothing over L2 on this registry.**
