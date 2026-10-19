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

## Stage 8 spec (20:35Z, before any code): an independent 6-relay class R6x on top of s7 (L2 + argsA43noT + RSST-D)
Not read: Studio's Job 31 spec.
- **Geometry.** A degree-6 vertex x with link L = (n0..n5), its own wheel word, non-R6. For a five at n_i, the
  two spokes next to x are n_{i+1} and n_{i-1}. The other common neighbour of x and n_{i+1} is n_{i+2}, and of x and
  n_{i-1} it is n_{i-2}. The fan is n_{i+3}. Seen from the five v with 6-spoke l_k: (n1..n5) = (l_{k+1}, h_k, f_k,
  h_{k-1}, l_{k-1}).
- **Pull g.** Each five v pays g[kg] to each 6-neighbour x. The key is kg = (n1, c(n2), c(n3), c(n4), n5) with
  exact spokes and small/big classes c for the hats and the fan (what v reads; exact hats would make the sender
  enumeration 5^9 per word). Canonical form: min(kg, reversed kg).
- **Split h (the 6 decides from its exact link).** x pays h[kh] to the big n_j, with kh = L rotated to start at
  n_j, canonical min over the two reading directions from n_j.
- **Conservation, one equality per canonical non-R6 6-word L:** sum over five positions i of g[kg_i(L)] = sum over
  big positions j of h[kh_j(L)]. If L has no big, its fives' g are forced to 0. So x passes on exactly what it
  receives and never goes negative.
- **Sender rows** (every small/big assignment of the hats and fans next to v's 6-spokes, coupled through non-R6
  6-wheels, as in S-lite B mode): sum of y over big roots + sum over 6-spokes of g[kg] >= 1 - t.
- **Receiver rows** (u, letter U): the y-load, plus for each link 6 w_j the bounded inflow M[sig_j] with
  sig_j = (U, w_{j+1}, s_j, s_{j-1}, w_{j-1}) canonical under its reflection. M[sig] >= h[kh(U, w_{j+1}, s_j, p,
  s_{j-1}, w_{j-1})] for every p that keeps that 6-wheel non-R6. This is the conservative max over the unseen
  private p_j, as in S-lite. Then x terms, all <= d - 6 + t. It is in jsep's window (c = 6 position), so the
  separator stays exact.
- **Checks.** Orientation test on kg, kh, sig. Exact certificate check from the signed HiGHS duals, rows re-derived
  from their labels: weights rationalised, rescaled so t's reduced cost is 0, sign of every other reduced cost
  checked, x caps priced. Upper: every sender assignment, every conservation row, jsep3 exhaustive receivers with
  the window inflow = max_p h, tail DP + Karp.
- **Pre-registered.** Guess: below 11/47 (the targets 55677 and 56687 have 6-spokes whose 6s also touch bigs).
  Kill line (lead's): 11/47 with a valid lower bound means the 6-relay alone does not help on this registry.

## Stage 8 result (20:43Z): R6x (6-relay) + L2 on argsA43noT + RSST-D: **t* = 18/79 = 0.227848** [E, both sides, own checkers]
- `prelay.py` (`solveR / lowerR / upperR / orientR`). 6,915 sender rows, 102 g keys, 4,760 h keys, 994 conservation
  equalities (every non-R6 6-word with a five), 975 inflow signatures, 4,760 M rows. Orientation test: 3,125 kg/sig
  + 15,625 L x 6 kh cases, 0 mismatches. Separator vs row value (`dbg`): equal at every d in every iteration.
- `s8.log`: 25 iterations, 377 s (warm from s7/s6/s2x rows). The last pass adds 0 rows; tail DP; Karp 0.5063, d0 11.7.
- `lowerR` (exact, signed duals, rows re-derived, rescaled so t's reduced cost is 0): **VALID 18/79**. Negative
  control: dropping one conservation row gives INVALID (2 negative reduced costs). `upperR`: FEASIBLE (sender rows
  0 violated, conservation |in - out| <= 1e-9 on all 994 words, d = 7..17 exhaustive 0 violated, tail, Karp).
- Below s7's 11/47 = 0.2340, so the kill line is not met: **the 6-relay helps on this registry**. 50 g keys are
  used; the largest are fives sending ~0.136 into a 6 whose spokes are 6 and 7.
- Dual (36 rows): receivers d = 7 8566655/6656656 (10/79), d = 8 75657565/66665655 (0.0591), d = 7 8558655/6665666
  and d = 8 76565565/56865865 (4/79), d = 8 75657565/55655565 (0.0211) and /66555555 (0.0084). Senders 55667,
  55687, 66678 (10/79), 56687 (four assignments, 6/79 + 2/79 x 3), 55668, 56667 (4/79), 66868, 55868 (2/79).
  9 conservation rows and 10 M rows.
- The targets: receiver 7565765/6855555 and sender 55677 have left the dual; 56687 stays.
- Files: sol_s8.json, cert_s8.json, lower_s8.log, upper_s8.log, rows_s8.txt.

## Stage 9-10 (21:05Z): corrected registry (twoeng at 30f86cd4: k3x 378 D / 383 C, drop44 removed)
- Args: P2's `s9/argsA44.txt` (= argsA with the k3x lines pointing at s9/k3x_*_30f86cd4; md5 equal to
  `git show 30f86cd4:` of out/job30/k3x_D.out and k3x_C.cfast; 378 D=true, 383 C-REDUCIBLE) + k42map_C_cons, plus
  rpat=rpatD.txt. No k43_kills_* files. Pattern counts by d: 7: 9,530, 8: 4,458, 9: 1,233, 10: 1,023, 11: 347; kinds
  D 15,413, C 1,429, RPAT 158.
- The 16 drop44 names (`drop44_names.txt` = the k43 names absent from the 30f86cd4 k3x). `s9/chk_drop.py`: 0 of 16
  loaded under argsA44; 16 of 16 under the old argsA43noT, so s8 did contain them.
- **s8 re-check on argsA44:** `upperR` FEASIBLE at 18/79 (still an upper bound). `lowerR` INVALID: 6 of its receiver
  rows are now forbidden by the new k44/k45 patterns (e.g. d = 7 8558655/6665666, 8566655/6656656).
- **s10 = R6x + L2 on argsA44 + RSST-D: t* = 217/1129 = 0.192205** [E, both sides, own checkers]. 51 iterations,
  719 s. `lowerR`: VALID 217/1129 (43 rows). `upperR`: FEASIBLE (senders, 994 conservation rows, d = 7..17
  exhaustive, tail, Karp d0 = 11.7).
- s10 dual: receivers d = 7 7765556/6575766 (0.1488), 7766556/6566575 (0.1399), d = 9 656565665/665666566
  (0.0345), and small weights on d = 7 7765556/6575765, 7765566/6596665, d = 9 656566556/755656665,
  656656665/665555555. Senders 55767 (0.1488), 66669 (0.1089), 55667 (0.101 + 0.030 + 0.009), 55757 (0.0788),
  57667 (0.0744 + 0.0044), 56696 (0.0434), 56669, 55696, 56667, 56967 (small). 23 conservation/M rows.

## Stage 11 pre-registration (21:10Z, before any code)
- s11a hypothesis: exact letters in the relay's pull keys (g key (n1..n5) all exact: the hats n2, n4 and the fan n3,
  which s10 read as small/big) drop t* below 217/1129. Kill line: converges to 217/1129 with a valid lower bound.
- Construction (full refinement, no partial): the fan of each 6-spoke appears only in that spoke's term and in that
  6's wheel condition. So for each spoke context m = (n1, n2, n4, n5) (canonical under reflection), add m <= g[(n1,
  n2, f, n4, n5)] for every fan f that leaves the wheel (5, n1, n2, f, n4, n5) non-R6. Sender rows: every exact
  assignment of the hats next to 6-spokes (at most 5^5 per word) that admits a non-R6 fan at every 6-spoke:
  sum y + sum_k m_k >= 1 - t. This is LP-equivalent to enumerating all hats x fans (min over the independent fans).
  Upper check uses the min over fans directly. Conservation rows use exact g keys.
- s11b (only if time): second-generation relay (6 -> neighbouring 6 -> big), pre-registered separately before
  any code.

## Stage 11b pre-registration and spec check (21:20Z): second-generation relay 6 -> 6 -> big [hand, not built]
- Rule as asked: a 6 x may pass part of what it holds to a neighbouring 6 x', which passes it on like any relay 6.
  Conservation stays exact at both 6s.
- Obstruction [hand]: x' must pass on exactly what it receives, so the amount on edge x -> x' can depend only on
  what both x and x' see. That is the edge's two common neighbours n_{j-1}, n_{j+1} (and x' = 6 itself); x does not
  see x''s link, and x' does not see x's.
  - That information is the same unordered pair from both ends, so the type of x -> x' equals the type of x' -> x.
  - With a 6-6 edge type tau, every 6 pays h6[tau] out along each such edge and receives h6[tau] in: the net is 0 on
    every 6 and every edge. The class collapses to s10 (it self-pairs, like L2 on a symmetric big-big edge).
- Making it non-trivial needs a type read from more than the shared pair, so the receiving 6 must bound an inflow
  it cannot see. Exact conservation then fails (only a <= version is possible, and a 6 may not go below 0). The
  sound version is a 6-centred row family over the 6's 2-ball (its link plus each 6-neighbour's link), with its own
  separator. That is not buildable in the remaining time, so s11b is not run.
- Pre-registered expectation for a shared-information 6 -> 6 relay: t* = s10's value exactly, by the argument above.

## Stage 11a result (21:16Z): exact pull keys: **t* = 217/1129, unchanged** [E, both sides, own checkers] -- kill line met
- `solveR gexact`. Pull keys exact (1,411 g keys, equal to the g keys in the conservation rows). 290 spoke contexts
  m, with 1,411 m <= g rows (one per allowed fan). 47,046 sender rows over exact hats. 35 iterations, 490 s.
- `lowerR gexact`: VALID 217/1129 (68 rows, 20 of them m <= g). `upperR gexact` (sender rows with the min over
  fans): FEASIBLE (senders, conservation, d = 7..17 exhaustive, Karp d0 = 11.7).
- Dual: the same receivers as s10 (d = 7 7765556/6575766 0.1488, 7766556/6566575 0.1399, d = 9 656565665/665666566
  0.0345, plus small ones). The senders split by exact hats: 55767 [7,7], 55757, 55667 [6,5,6] / [9,6,7] /
  [9,5,6] / [6,9,7], 57667 [7,6,7] / [6,5,6], 56696, 66669 [5,5,5,5,5] / [5,6,5,6,6] / [5,6,5,5,5] /
  [6,5,6,5,5], 56669, 56667, 56967, 55696.
- Refined: all of n2, n3, n4 (both hats and the fan), not a subset. **Exact letters in the relay pull do not
  help on this registry.**

## Stage 12 pre-registration + spec (21:25Z, before any code): 6-centred relay R6x2 (keys read the 6's 2-ball)
- Hypothesis: t* < 217/1129 on argsA44 + RSST-D + L2 + R6x2. Kill line: it stays at 217/1129.
- 6-centred arrangement of a 6 x: link L = (n0..n5) and apexes s_i = the other common neighbour of n_i and
  n_{i+1} (besides x). That is x's 2-ball: a d = 6 "receiver arrangement".
- Pull g2 (five at n_i): s10's key (n_{i+1}, c(n_{i+2}), c(n_{i+3}), c(n_{i+4}), n_{i-1}) plus the apexes of the
  five's two edges at x: a_r = s_i, a_l = s_{i-1}. Canonical: min with the reflection (reversed letters, apexes
  swapped). From the five v with 6-spoke l_k: a_r = l_{k+2}, a_l = l_{k-2} (v's own link), so the sender rows read
  only v's 2-ball (hats and fan as small/big, as in s10).
- Split h2 (big at n_j): L rotated to n_j plus (s_j, s_{j-1}), canonical under the reflection about n_j.
- Conservation, exact, per 6-centred arrangement (L, s): sum_i g2 = sum_j h2. Required for all s in {5..9}^6 with no
  admissibility filter, which only restricts the class (sound). Separated by brute force per canonical L
  (5^6 apex words, numpy). Each violated (L, s) is added as an equality row.
- Receiver inflow at a link 6 x = w_j of u: x's link from u is (U, w_{j+1}, s_j, p_j, s_{j-1}, w_{j-1}), and the
  apexes of u's two edges at x are w_{j+2} and w_{j-2}, all in jsep's window except p_j. Inflow M[sig] with
  sig = (U, w_{j+1}, s_j, s_{j-1}, w_{j-1}, w_{j+2}, w_{j-2}) canonical, M >= h2 for every p_j that keeps the
  6-wheel non-R6. M rows are added lazily when a receiver row first uses a sig.
- Hand note: with exact conservation, a big's h2 can only usefully depend on an apex that a neighbouring five's g2
  or a neighbouring big's h2 also reads. Otherwise equality over all values of that apex forces it constant. So
  the new freedom is charge traded across a shared apex.
- Validations: (V1) apex mode off must reproduce 217/1129 (s10's class); (V2) orientation test on g2, h2, sig;
  (V3) planted check that separator value = row value.
- Stage 12 validations (21:45Z):
  - V2: orientR2 gives 0 mismatches in both modes. Checked: 78125 key/sig reflections, 46875 h reflections, and 20000 random physical rotations/reflections of cons2_coef.
  - V1: noapex (s10 keys) solveR2 gives t* = 0.192205491585 (sol/cert_s12v1).
    - LOWER-R2 VALID t >= 217/1129 (43 rows).
    - UPPER-R2 FEASIBLE: senders 0 violated. Conservation was checked on all 1424 canonical non-R6 6-links x 5^6 apex words: 0 off. d = 7..17 exhaustive: 0 violated. Karp d0 11.73.
  - V3: with the dbg flag (first full-run attempt), the separator value equals the row value at every d = 7..17 over 3 iterations. That attempt died on a dbg-only index bug (it read new columns), so it is not a result.
- Structure (s12_struct.txt): the full conservation system has 11.9M distinct rows and rank 69782. That is 67988 from h-blocks, since each h key fixes its 6-type, plus 1794 g-only.
- Solver change: per-L separation of conservation rows (2 rows per L per iteration) stalled the LP, at 30 s per iteration and growing.
  - Replaced it with a precomputed basis of actual (L, s) rows: QR with pivoting per 6-type, 92296 rows (cons2basis.json). Together they imply every (L, s) row.
  - Separation is kept as a check.
- 6-centred context question (coordinator), for senders 55677 and 56687 when the ring beyond them (hats and fans) is all big:
  - In s10 the 6 is a relay with 3-4 big neighbours.
  - 55677: its 6 sits between 5 and 7, key (5,1,1,1,7). Its g = 0 in s10; the row is met by y only (0.80779 = 1 - t, tight).
  - 56687: g(5,1,1,1,6) = 0 and g(6,1,1,1,8) = 0.0653, with y covering the rest; tight.
- s12 FULL (exact apex letters): the LP is large (158k rows, 91k columns) at 200-900 s per simplex re-solve. Still running (s12.log).
  - Partial LP value 0.191011236 at iterations 0-2 (17/89). This is NOT a bound: rows are still being generated.
  - The class contains s10's, so the eventual t* <= 217/1129.
- s12r REDUCED (the working version): the same R6x2 but with the two apex letters in g2 / h2 / sig read as small/big only (flag apexcls).
  - Size: 10750-row conservation basis; 393 g keys in senders; 934 initial M sigs.
  - Converged in 20 iterations (580 s): t* = 0.191256830601 = 35/183 (sol_s12r / cert_s12r).
  - LOWER-R2 VALID t >= 35/183 exactly (52 dual rows: 9 sender, 28 cons2, 11 mrow, 4 receiver).
  - UPPER-R2 FEASIBLE:
    - senders 0 violated;
    - conservation: all 1424 non-R6 6-links x 5^6 apex words, worst 5.6e-12;
    - d = 7..17 exhaustive: 0 violated;
    - Karp d0 11.94.
  - => s12r = 35/183 < 217/1129, verified both sides. The hypothesis holds for the reduced class; the kill line is not met.
  - Binders:
    - receivers: d=7 7765556/6575766 and 7766556/6566575; d=9 656565665/665666566 (same as s10);
    - senders: 55767, 66669, 55667 (x2), 55757, 57667, 56696, 55696.

## Stage 13 pre-registration + spec (22:50Z, before any solve): 7-centred split R7h (flag zh), as s15 on argsA47
- Hypothesis (Long Table's wording): the 7-centred class makes 55757-type sender rows non-tight, i.e. those with no 6-neighbour and ring 2 >= 7. It drops t* on argsA47 below s14r's 19/102.
- Kill line: 55757-type rows stay tight and t* is equal.
- Class: a big u splits what it gives each link five v by u's own 2-ball near v.
  - On top of y[root], a second transfer z[k] >= 0 from u to v.
  - k = (v's link read from u: U, n1, n2, n3, n4; c(hat_r), c(hat_l)), canonical under the reflection (n reversed, hats swapped).
  - hat_r is the common neighbour of u and n1 other than v (= w_{i+2} in u's row); hat_l = w_{i-2}. c is the small/big class.
  - The five sees both hats in its 2-ball (hat between l_j and l_{j+1} / l_{j-1}).
  - The big sees them in jsep's window (a, f at a five position). So z is exact on both sides and no max over unseen parts is needed.
- Sender rows: every small/big assignment of the hats next to v's big spokes and its 6-spokes. They are shared where one hat is next to both, and coupled with the 6-relay's non-R6 fan check as before.
  - Row: sum y + sum z + sum g >= 1 - t.
- Receiver rows: load = previous load + sum over link fives of z[k(i)] <= d - 6 + t.
  - The separator's class key for a five position now includes a and f.
- This is a refinement of y (z constant across hats = y), so t* <= the base relay's t* (s14r = 19/102 for s15; s12r47 for the combination).
- Validations: (V1) zh off reproduces s14r = 19/102 (P2's run, own code). (V2) Orientation test on zkey. (V3) The upper check at the solution, exhaustive.
- Runs:
  - s15 = s10-relay (noapex) + zh on argsA47.
  - s15c = reduced 6-centred (apexcls) + zh, if s15 is not worse.
- s12r47 (reduced 6-centred, apexcls, on argsA47; warm from s14r): t* = 21/113 = 0.185840708 < s14r 19/102 = 0.186274510.
  - LOWER-R2 VALID t >= 21/113 (46 rows).
  - UPPER-R2 FEASIBLE: senders 0; conservation worst 1.4e-14; d = 7..17 exhaustive 0; Karp d0 11.95.
  - Binders:
    - receivers: d=7 7665566/6675666, d=9 656565665/665666566, d=9 656656665/665555555;
    - senders: 66669 (two contexts), 55667 (two), 55767, 55696, 56696.
- Stage 13 V1: zh off, noapex on argsA47 (own code) gives 19/102 = 0.186274510, the same as P2's s14r. s15 is running.
- s15 (s10-mode relay + R7h z on argsA47): t* = 19/102, equal to s14r.
  - LOWER-R2 VALID 19/102 (25 rows). UPPER-R2 FEASIBLE (senders 0; conservation 9e-14; d = 7..17 exhaustive 0; Karp d0 13.23).
  - **Kill line met**: t is equal.
  - In the s15 primal, 55757 with an all-big ring 2 is still exactly at 1 - t (y7|5575 = 0.40686 x 2, z = 0). No 55757 row carries dual weight in the s14r, s15, s12r47 or s15c certificates; on argsA47 it is not what binds.
- s15c (reduced 6-centred + R7h): t* = 21/113, equal to s12r47.
  - LOWER-R2 VALID 21/113 (36 rows). UPPER-R2 FEASIBLE (conservation 8.7e-13; d = 7..17 exhaustive 0; Karp d0 12.84).
  - In this primal, 55757 all-big has slack 0.169 (y7|5575 = 0.4917). The primal is not unique, so this is not a forced property.
- Binder d=7 7665566/6675666 (u = 7):
  - s15: slack 0, dual 0.2353 (the largest weight). Load = y7|5566 0.65196 + y7|5576 0.32843 + z7556600 0.05882 + z7557600 0.07843 + M(75666) 0.06863 = 1 + t.
  - s15c: slack 0, dual 0.2301. Load = y7|5566 0.67257 + y7|5576 0.33628 + z7556600 0.03540 + z7557600 0.07080 + M7566657 0.07080.
  - s12r47: slack 0, dual 0.2478. Load = y 0.67920 + 0.33628 + M 0.09956 + 0.07080.
  - Nothing flows into u (all x = 0 here). What it gives: y and z to its two fives (w3, w4), and the 6-relay h to its link 6s.
- argsA50 (d43ba26a): P2's s17/argsA50.txt = argsA47 with k3x swapped; k3x md5 equal to git show d43ba26a out/job30 (510 D / 522 C); dcount newpat 15550. s12r50 launched (23:2xZ).

## Stage 14 pre-registration + spec (23:45Z, before any solve): 7-inflow R77 (flag q7), run st14q on argsA50 over s12r50
- Hypothesis: the receiver d=7 7665566/6675666 becomes non-tight and t* drops below s12r50.
- Kill line (Long Table): 7665566/6675666 stays tight at the same t*.
- Class: a big w sends to an adjacent 7 u the amount q[K] >= 0. K is u's whole link read from w (w first, u's neighbours in cyclic order), canonical under the reflection fixing w.
  - u's row (d = 7): u knows its link, so inflow is exact: load -= sum over big link positions j of q[K(link rotated at j)]. This is a function of the whole link, so it is not window-local.
    - jsep4 = jsep3 + a table (canonical 7-link -> total inflow) subtracted at the leaf. Pruning bounds ignore it (inflow >= 0 only lowers load), so the search stays exhaustive.
  - w's row (any d): w sees 5 of the 7 letters of u's link (its own letter, w_{i+1}, s_i, s_{i-1}, w_{i-1}). Outflow is Q[sig] >= q[K] for every completion of the 2 unseen letters (completions that make u's link RBIG are dropped, since such a 7 does not exist). This is window-local (c = 7 position).
  - No sender rows change. No conservation, since a big is not conservative: q is charged inside its own budget row.
  - The tail (d > 17, letter 9) has no inflow, only outflow Q, so it stays sound.
- Validations: (V1) q7 off reproduces s12r50. (V2) Orientation: random 7-links, inflow key in the sender-side completion set under both sender orientations, and inflow invariant under canonicalisation: 0 mismatches (102652 cases incl. earlier tests). (V3) dbg separator = row value, including the leaf bonus.
- s12r50 (reduced 6-centred, apexcls, argsA50 = d43ba26a): t* = 23/134 = 0.171641791.
  - LOWER-R2 VALID 23/134 (57 rows).
  - UPPER-R2 FEASIBLE: senders 0; conservation 3.9e-15; d = 7..17 exhaustive 0; Karp d0 12.20.
  - Binders:
    - receivers: d=7 7665566/6675666 (dual 0.194), d=7 7665666/6566565, d=7 7655666/6756666, d=10 6565656565/6655666666, d=10 6556656556/6665656665;
    - senders: 66669, 55667 (x3 contexts), 55767 (x2), 56669 (x2), 66667.
- s12r50 reproducibility: upperR2 re-run with current code (zh, q7 off; apexcls; consbasis given) FEASIBLE at 23/134 (upper_s12r50_recheck.log). cmd_s12r50.sh; engine snapshot + md5s in snap/ (s12r50_solve = engine at launch, s12r50_check = current).
- st14q (stage 14: R77 q7 + reduced 6-centred, argsA50): 84 iterations, 3076 s.
  - t* = 23/134, equal to s12r50.
  - LOWER-R2 VALID 23/134 (60 rows incl. 3 mrowQ). UPPER-R2 FEASIBLE (jsep4 with leaf inflow table, 200 links; senders 0; conservation 4.6e-13; d = 7..17 exhaustive 0; Karp d0 12.20).
  - V3 dbg: separator = row value to 5e-10 over 117 rows.
  - **Kill line met**: 7665566/6675666 (and its mirror 6665766) is still tight with dual 0.194. In the primal, q into it is 0: load = y 0.72015 + 0.41418 + h 0.03731.
  - Obstruction, read from the certificate: it puts weight 0.194 on Q[7|6666] >= q[7665566] and 0.045 each on Q[7|6666] >= q[7665666] and Q[7|5666] >= q[7655666].
    - The only possible sender, w0, is a 7 whose visible part of u is all 6s. The fives w3, w4 are exactly the 2 letters w0 cannot see.
    - So w0 must pay the same to every 7-neighbour with that view. w0 is itself a 7 in the same tight family (7665666/6566565 and 7655666/6756666 bind).
  - Next: a key the sender can see must include u's w3, w4. That means radius-3 information (a two-step relay through the 6s w2/w5, or jsep with a wider window).

## Stage 15 pre-registration + spec (00:50Z, before any code): 6 -> 7 pass-on V6 (flag v6), run st15 on argsA50 over s12r50
- Hypothesis: binder 7665566/6675666 becomes non-tight and t* < 23/134. Kill line: the row stays tight at 23/134.
- Class (added to the reduced 6-centred R6x2):
  - A 6 x next to a 7 u passes v[K] >= 0 to u.
  - K = x's link rotated at u, m = (U=7, n1, n2, n3, n4, n5), plus the two apexes of x's arrangement beyond the edges (u, n1) and (u, n5), read in 3 classes: 5 / 6 / big.
  - From u, with x = w_j: m = (7, w_{j+1}, s_j, p_j, s_{j-1}, w_{j-1}), and the apexes are w_{j+2}, w_{j-2}. For x = w2 next to 7665566 that is (7, w3=5, s2, p, s1, w1) with apexes w4 = 5 and w0, so the key sees both fives.
  - K is canonical under the reflection about u (as h2).
- Conservation per 6-centred arrangement (L, s), exact over all apex words: sum_i g2 + sum_{j: L_j = 7} v = sum_j h2.
  - The 6 still passes on exactly what it receives. The new rows are separated / basis-precomputed as before.
- Receiver u (d = 7 only, U = 7): load -= sum over link 6s of mV[sig]. sig = (7, w_{j+1}, s_j, s_{j-1}, w_{j-1}, cv(w_{j+2}), cv(w_{j-2})), canonical. mV <= v[K(p)] for every private p that keeps the 6-wheel non-R6.
  - That is the conservative MIN over the unseen p, since it is inflow. Window-local (c = 6 position, U = 7).
- Validations: (V1) v6 off = s12r50 (same code path). (V2) Orientation: reflection of the v key and sig, and invariance of the new conservation coefficients under physical rotation/reflection. (V3) dbg separator = row value.
- st15 run 1 (00:41Z) was killed by the container restart at 1998 s (LP value 1/6). Run 2 (restart, warm from run-1 rows) converged at 595 s: LP t* = 1/6.
  - LOWER-R2 VALID 1/6 (128 rows). **UPPER-R2 INFEASIBLE**: conservation is broken on 48 no-five 6-types (e.g. 666677, 666787; worst 0.066).
  - Cause, a soundness hole in my v6 build: the LP's conservation rows covered only the 994 6-types with a five (as in s12 mode). In s12 mode that is harmless, because a no-five 6's h2 only costs.
    - With v6, a no-five 6 next to a 7 could send v with no h coming in: free charge. The LP used it.
    - The upper check (all 1424 6-types) caught it.
  - Run 2's 1/6 IS still a valid lower bound for the sound class: its LP is a relaxation (fewer rows), and the cert checks exactly. So the sound st15 t* is in [1/6, 23/134].
  - Run 2's binder 7665566/6675666 had dual 0 and slack 0, paid in part by V inflow 2 x 0.02083 (via w2, w5). Moot, since the primal is unsound.
- Fix (st15f): in v6 mode, conservation over ALL 1424 canonical non-R6 6-types (solver init, per-L separation and basis). cons2basis_v6.json is rebuilt: 22126 rows.
  - s16_struct.txt regenerated: 1424 6-types; conservation rank 20147; h 18683; v 13869; V sigs 2850.
  - st15f launched 01:41Z (warm from runs 1 and 2). Kill-line clock (3 x 713 s) restarts here.
- **st15f (sound stage 15): t* = 23/134, equal to s12r50.** 9 iterations, 927 s, within the 2139 s limit.
  - LOWER-R2 VALID 23/134 (107 rows: 11 sender, 61 cons2, 16 mrowR2, 14 mrowV, 5 receiver).
  - UPPER-R2 FEASIBLE: senders 0; conservation over all 1424 6-types x 5^6 worst 3.2e-13; d = 7..17 exhaustive 0; Karp d0 12.20.
  - dbg separator = row value (< 5e-10).
  - **Kill line 1 met.** The binder 7665566/6665766 (the mirror of 6675666) is tight (slack 0), with dual 0.194, the same as s12r50.
    - Load = y7|5566 0.67537 + y7|5576 0.36317 + relay h 0.08209 + 0.05101. V inflow = 0.
  - Why (from the certificate): the 0.194 weight sits on mrowV V[7,5,6,6,6,5,7] <= v[7,5,6,5,6,6,5,7].
    - That is the completion p = 5 of the 6 at w2's private. In that completion the 6 x has a second five to pay. V is the min over p, so p = 5 sets V to 0.
    - Round-50 census: every binder completion with a five among the privates is reducible (D/C at ring <= 16). The arrangement that forces V = 0 does not occur in a minimal counterexample, but u's 2-ball cannot see that.
  - Sizes as in s16_struct.txt (regenerated). Engine snap/st15f, md5s snap/st15f_md5.txt, cmd_st15f.sh.

## Stage 16 pre-registration (02:10Z, not built): private-context pass-on
- Hypothesis: binder 7665566/6675666 becomes non-tight, so t* < 23/134. Kill line: it stays tight at 23/134.
- Idea (from the st15f certificate and the round-50 census): in V's min over the 6's private p_j, drop each p whose extended arrangement is reducible. The survivors in the binder are exactly: all six privates >= 6 and p51 >= 7.
  - Sound version: the receiver row carries a per-row candidate set, the kills taken from verified D/C patterns over u's 3-ball (the privates). That needs separation over privates as extra slots: jsep with d extra slots, or per-row pricing of V with pattern lookups.
  - Alternative from Long Table: the big privates (p51 >= 7, others >= 6) send toward u via the 6s at w2 and w5. That needs a 6 to pass on from its private big, which is already allowed (h from p to x when p is big, v from x to u).
  - What is missing is that v must be allowed to depend on p's class, and V must take the min only over the surviving p. So both routes need the kill information on privates.

## Stage 16 (A) pre-registration + falsifying sanity check (02:40Z): private filter from registry patterns — STOPPED at check 4
- Registry: s19/argsA52.txt (P2), i.e. 09d8ac38. k3x md5s equal `git show 09d8ac38` out/job30 (k3x_D 3ed293d9..., k3x_C 61cf5dc8...); dcount newpat 15855; rpat=rpatD.txt; drop44 names not in the args.
- Hypothesis: with V's min restricted to registry-allowed privates, binder 7665566/6675666 becomes non-tight and t* < 23/134.
  - Kill lines: (a) the binder stays tight at 23/134; (b) V stays 0 because the min moves to the census-survivor context.
- Filter (as specified in RELAY_SPEC 14): drop a private value p iff some registry item, with every slot it constrains known, forbids the arrangement. The items are:
  - R6 of the private's 6-wheel;
  - a registry wheel pattern of exact degree d, centred at a vertex of exact-degree letter (7 or 8) whose arrangement contains p.
  - In the binder those centres are w0 (7: link u, w1, s0, q1, q2, s6, w6; apexes w2, p1, ?, ?, ?, p6, w5) and s2 (7: link p2, w2, w3, s3, ?, ?, ?; apexes s1, u, w4, ?, ?, ?, ?).
- Sanity check 4 (s16_census.py, 9.8 min): over the binder's 15625 one-ring-out cases (p1, p2, p5, p6 = privates of the link 6s; q1, q2 = w0's unseen neighbours), the filter leaves **12320 survivors, not the census's 3072. FAIL, so stage 16 (A) stops here, as instructed.**
  - Killed 3305 cases:
    - 3080 first by C:f7_...5565_....... (s2-centred; in s19/k3x_C_09d8ac38.cfast), which kills p2 = 5 in all 3125 cases;
    - 225 by C:f7_.6655.._.5..... (w0-centred; k42map_C_cons.cfast).
  - Not killed: p5 = 5 (661/3125 killed, the same as for every other p5 value, i.e. only via other privates), p5 = 6, p1 = 5, p6 = 5, q1 = 5, q2 = 5.
  - The binding case in st15f is exactly p5 = 5 (mrowV V[7,5,6,6,6,5,7] <= v[7,5,6,5,6,6,5,7]: the 6 at w5 with private 5).
  - Why no registry pattern can drop it: p5's known neighbours are w5, s4, s5, all 6s. Every registry pattern is a wheel centred at a vertex of degree >= 7, and no exact-degree big vertex in u's 2-ball is adjacent to p5. The census kills of p5 come from RSST configurations (rsst180, ...), which need the configuration itself tested in the private's 3-ball frame. As loaded, rpatD has them only in u's own window.
- Next options:
  - (B) v keyed on the private's class: the fallback named by Long Table.
  - Port the 6 census configurations (after confirming each is in the conservative RSST 582 or in k3x) to a 3-ball containment test at a link-6 private.

## Stage 16 A′ pre-registration (before any solve): 3-ball containment filter, full forbidden set (spec: RELAY_SPEC 14′)
- Item 1 (registry). rsst025 (C2cons), rsst050 (D2), rsst052 (D2), rsst098 (D2) and rsst180 (C2cons) are all in the conservative 582. f7_...5565_....... is in k3x_C 09d8ac38. None is broad-X only, so none is dropped. Forbidden set = 582 + 1,427 twoeng names (all have kc lines).
- Check 4:
  - Full 3-ball test: **3,072 / 15,625**, exactly census50's number (`s16_check4full.py`).
  - LP-visible projection: 7,500 (`s16_check4.py`). The kills lost are rsst180 at w0's privates (no LP term reads them) and rsst052 at p11/p61 (it needs w_{j±3}).
  - The st15f blocking case p51 = 5 is kept (rsst050), and so are p51 = 6 (rsst098) and p21 = 5.
  - **Proceeding:** the gating number is reproduced by the full test. The LP uses its sound projection. Both numbers are reported.
- Validation 1 (filter off): the patched engine without `filt16` on st15f's cert/sol must give lower VALID 23/134 and upper FEASIBLE.
- Validation 2 (filter on): at the binder, rsst050 drops p51 = 5 and rsst098 drops p51 = 6 (mask 28 at M/V sig (7,5,6,6,6,5,7)), and rsst025 / rsst050 / f7_...5565_....... drop p21 = 5 (mask 30).
- Hypothesis: on argsA52 with filt16, t* < 23/134 and the binder is non-tight.
  - Kill line (a): binder 7665566/6675666 stays tight at 23/134.
  - Kill line (b): the min moves to the survivor context (all privates >= 6 and p51 >= 7).
  - Baseline: the same engine without filt16 on argsA52, run alongside.
- Runs: cmd_st16ap.sh; engine snap/st16ap (md5 snap/st16ap_md5.txt).
- Unknown-vertex check (Long Table): **PASS.** The rule is in RELAY_SPEC 14′.
  - Check 4 LP projection, strict matcher, unknowns coded 99, 5 and 7: 7,500 / 7,500 / 7,500, all the same set (md5 9b4d02bace5786cbf0f6c5c7c7434dbc).
  - The non-strict matcher at code 5 gives 3,072 (md5 f2582478...), which shows why the rule is needed. At codes 99 and 7 the non-strict matcher already gives 7,500, the same set.
  - Full kill tables regenerated strict at codes 5 and 7 are identical to s16ap/kill6 (U7 27a64538..., U8 = U9 6dc44bba...). st16ap is not void.
  - Strict matching is now the default in s16_filter.py (md5 1bd72e9d...); its output is identical to the snapshot.

## Stage 16 A′ result: **t* = 6/37 = 0.162162** on argsA52, verified on both sides
- **Filter on (st16ap2).**
  - Upper: UPPER-R2 FEASIBLE at 6/37 on sol_st16ap2.json. 0 senders violated; conservation over all 1424 6-types × 5^6, worst 7e-12; d = 7..17 exhaustive; Karp lambda 0.5135, d0 12.0.
  - Lower: LOWER-R2 VALID t >= 6/37 (211 rows) on cert_st16ap2L.json. This cert is from the unpenalised LP over the same rows, with nosep. Run 2's own cert came from the penalised LP and was INVALID.
  - Run history:
    - Run 1 (st16ap) reached 6/37 at iteration 17. After the x penalty was removed it did not settle in 19 more iterations, so I killed it.
    - Run 2 restarted from all rows with `keeppen` and stopped at the penalised fixed point, iteration 9, with 0 violated rows.
- **Baseline, filter off, same engine and registry (st16b0):** 6/35 = 0.171429, lower VALID (185 rows), upper FEASIBLE. The filter's own gain on argsA52 is therefore 6/35 → 6/37. The change from argsA50 to argsA52 alone took 23/134 to 6/35.
- **Kill lines.**
  - (a) Not met. t* falls below 23/134, and below the argsA52 baseline 6/35.
  - (b) Partly met, stated explicitly. The binder 7665566/6675666 is still tight in the upper solution (load = cap = 43/37) but has dual weight 0 in the exact cert. Its V is still 0.
  - On (b): the cert has mrowV V[7,5,6,6,6,5,7 | allowed 7,8,9] <= v[7,5,6,7,6,6,5,7] at weight 0.027. So at the binder's w5 signature the min has moved to p51 = 7, the survivor context.
- **New certificate support.**
  - Receivers: 7766556/6576576 (0.108), 7676556/7756595 (0.054), 9 655665556/756567565 (0.054), and six d = 7 rows at 0.027 or below.
  - Heaviest row: mrowR2 M[9,5,6,5,6,5,5 | allowed 5,7,8,9] (0.162).
  - 24 cert rows use masked (filtered) signatures.
- s17_struct.txt (blind) is written.
- Engine: snap/st16ap2, md5s in snap/st16ap2_md5.txt (outputs appended). Commands: cmd_st16ap.sh.

## Stage 17 pre-registration (05:30Z, before any solve): face pool F5 on 5-5-5 faces (flag `face5`), run st17f on s19/argsA52.txt over st16ap2
- **Why this class.** Long Table (round 51): the irreducible d = 7 family is "a 7 carrying a 5-5-5 face". The st16ap2L cert agrees. Of its 9 receivers, 7 contain two consecutive link fives w_i, w_{i+1} with apex s_i = 5: 7766556/6576576, 7676556/7756595, 9 655665556/756567565, 7665566/6765766, 7765556/6575966, 7665556/6675966 and 7766556/6566576. Only 7665666/6566655 and 7766566/6556655 lack one. 9 of its 13 sender rows (55669, 55667 x5, 55767 x3, 55759, 55769) are fives on such a face, since the word has two adjacent 5s. Every existing transfer is vertex-to-vertex and keyed on one vertex's 2-ball. So a face five whose own outside neighbours are poor (e.g. 55667 with small hats) cannot use a face-mate that has a big outside neighbour.
- **Rule F5 (five -> five across a 5-5-5 face).** Let F = (a, b, c) be a face of three fives. Around F lies a 6-ring: e_ab (the third vertex of the other face on edge ab), and likewise e_bc and e_ca; k_a (a's one outside neighbour adjacent to neither b nor c), and likewise k_b and k_c. Five a sends to its face-mate b the amount f[K] >= 0, where
  `K(a->b) = (e_ab exact letter, c2(k_a), c2(e_ca), c2(k_b), c2(e_bc), c2(k_c))`. c2 is small {5,6} = 0 / big = 1.
  - Both ends read K exactly. a's link is (b, e_ab, k_a, e_ca, c); its hats include k_b, e_bc and k_c. b's link is (a, e_ab, k_b, e_bc, c); its hats include k_a, e_ca and k_c. e_ab is a link letter at both ends; every other entry is a class, and each is either a link letter or a hat at each end.
  - The roles are defined by adjacency, not by orientation, so K is invariant under reflection.
  - One f per (directed face edge, face). A five on two 5-5-5 faces has a separate exchange on each.
- **Rows.** Only senderR2 changes. For a five v with word w, each consecutive pair of 5-spokes (k, k+1) gives a face. For that face, v's row gains `+ f[K(b->v)] + f[K(c->v)] - f[K(v->b)] - f[K(v->c)]`, with b = w_k and c = w_{k+1}. The row becomes `t + sum y + sum g2 + sum f_in - sum f_out >= 1`.
  - The hats enumerated are extended to H[k-1], H[k] and H[k+1], each as a small/big class, as for 6-spokes.
  - New admissibility (sound, restriction only): drop an assignment if, for a face-mate b = w_k, every completion of b's link (5, w_{k-1}, H[k-1], H[k], w_{k+1}) by letters in the hat classes is R5.
  - Receivers, cons2, mrowR2, mrowV, the separator and the tail are unchanged, because fives are not receivers.
- **Why it is sound.** In G every transfer is credited to b and debited from a with the same key, computed from b's view and a's view respectively. So the total charge is conserved without a new conservation row. Every five of G sits in one enumerated sender row, because the enumeration is exhaustive over admissible classes and the dropped assignments are R5 at a face-mate. **upperR2 checks this.** Its sender step enumerates the same rows (R2_sender_rows), now with the f terms read from the sol file's new field `f`. Every assignment must satisfy LHS >= 1 - t - EPS. Conservation (1,424 x 5^6), d = 7..17 exhaustive, and the tail are re-run unchanged. lowerR2 prices f through the generic ledger, so every f column needs reduced cost >= 0. With f = 0 and the flag off, the class is st16ap2's, so t*(st17f) <= 6/37 apart from the mate filter, which only shrinks the class.
- **Kill line (verbatim): "the rule fails if any 5-5-5-face 7 row stays tight at the optimum"**. It is checked with rowR2 at sol_st17f (slack) and cert_st17f (dual) on:
  - the binder 7665566/6675666;
  - 7655666/6756666;
  - 7655667/6756656;
  - every d = 7 receiver row in the final LP that has a 5-5-5 face (consecutive link fives with apex 5).
- **Progress:** t* < 6/37 = 0.162162 with LOWER-R2 VALID and UPPER-R2 FEASIBLE, both from the s17d engine. An LP value without both checks, or without convergence, is not a bound.
- **Validation:** the s17d engine with `face5` off must reproduce, on argsA52, the filter-off baseline st16b0: lower VALID 6/35 on cert_st16b0.json, and upper FEASIBLE on sol_st16b0.json.
- **Engine:** P_own_lp/s17d/ (prelay2.py is a copy of top-level 4f400216 plus face5; backup s17d/prelay2_st16ap2_backup.py).

## Stage 17 result (07:05Z): **face pool F5 is null on argsA52. t* = 6/37, and the kill line is met**
- **Validation (face5 off, s17d engine):** cert_st16b0.json gives LOWER-R2 VALID 6/35 (185 rows). sol_st16b0.json gives UPPER-R2 FEASIBLE at 6/35 (conservation worst 8.8e-14, d = 7..17 exhaustive with 0 violated). Logs: s17d/val_off_*.log. No regression.
- **face5 orientation and physical test:** over 95,622 random 5-5-5 faces, the f terms of the three fives' own views sum to 0, with 0 mismatches. A mutated key gives 57,406 mismatches, so the test bites. With face5 there are 7,830 sender rows (7,074 without).
- **Solve.**
  - Run 1 (st17f, keeppen) was stopped after iteration 0. Its LP over the warm rows alone already gave t = 6/37.
  - The exact unpenalised LP over the same rows (st17fL, nosep) gives **LOWER-R2 VALID t >= 6/37 (177 rows)** with face5 on. 28 f columns are positive in that LP, so the rule is used but buys nothing.
  - The face5 class contains st16ap2's class, and the mate filter only shrinks it. So st16ap2's primal (f = 0, UPPER FEASIBLE at 6/37) is feasible for it, and **t*(F5) = 6/37 exactly**. That is not progress.
- **Kill line ("the rule fails if any 5-5-5-face 7 row stays tight at the optimum"): MET.** rowR2 at sol_st17fL / cert_st17fL gives:
  - binder 7665566/6675666: slack 0, dual 0;
  - 7655666/6756666: slack 0.081, dual 0;
  - 7655667/6756656: slack 0, dual 0;
  - 7766556/6576576: slack 0, dual 0.054.
  - 8 of the cert's 10 receivers carry a 5-5-5 face: 7766556/6567566, 7676556/7756595, 7766556/6576576, 9 655665556/756567565, 7765556/6575966, 7665556/6675966, 7665566/6665766 and 7665566/6765766. The two without one are 7665666/6566655 and 7766566/6556655.
  - The binding senders are the same face fives as in st16ap2: 55669, 55667 x4, 55767 x3, 55759, 55769; also 57669 and 66667.
- Reading: pooling among the three fives of the face cannot help, because the face's 6-ring has the same bigs (u and the 7 across the other face edge) whichever five is paid. The deficit is the face's, not a single five's. Files: s17d/{prelay2.py, cmd_st17f.sh, cmd_st17fL.sh, st17f_run1.log, st17fL.log, lower_st17fL.log, kill_st17fL.log, sol_st17fL.json, cert_st17fL.json, engine_md5.txt}.

## Stage 18 pre-registration (06:56Z, before any solve): hat channel H5 (flag `hat5`, RELAY_SPEC 15), run st18h on s21/argsA54.txt over s21f
- **Rule.** A big b that is the hat of a five v (the other apex of the edge between two consecutive spokes x, y of v) sends r[K] >= 0 to v, at distance 2.
  - K = the canonical pair of side tuples. A five-spoke contributes (5, c2(nbr at b), letter(nbr at v)), a six-spoke (6, c2(nbr at b), c2(nbr opposite)), and a big spoke (letter).
  - The full specification and the table of who sees what are in RELAY_SPEC 15.
  - Base class: s21f (`xon apexcls filt16 killtab=s21/f/kill/kill6`, no v6).
- **Choice.** The pre-build screens are on s21/cf/cert_s21fL.json (lower 4/25), plus the argsA52 certs st17fL and st16ap2L.
  - Big ↔ big diamond: null for every key into a 7; at s21f only 9 ↔ 9 keys price negative. Not built.
  - Hat channel: negative reduced cost forced at row 55669 [1,0,0|0,0], weight 0.08. This is a face five with a big hat next to its face-mate (RELAY_SPEC 15). Built.
- **Soundness.** In G, b debits and v credits the same r[K]. RELAY_SPEC 15 tabulates that both ends compute K identically. The physical test gives 0 mismatches over 100k random diamonds; the broken-key control gives 15,898 (s18d/orient_hat5*.log).
  - upperR2 checks every sender row (all hat classes enumerated) and every d = 7..17 receiver exhaustively, with the outflow in the window, plus conservation and the tail.
  - lowerR2 prices r through the ledger.
- **Kill lines (Long Table):**
  - (1) the stage dies if t* does not go below 65/406;
  - (2) it dies if both 7665566/6675666 and 7655667/6756656 stay tight (rowR2 at the new solution);
  - (3) the coordinator's line also applies: "the rule fails if any 5-5-5-face 7 row stays tight at the optimum";
  - (4) stop if the solve runs past 3 x s21f's wall time (3 x 1771 s ≈ 90 min) without t moving.
- **Progress:** UPPER-R2 FEASIBLE on the new solution itself with t < 65/406 = 0.160099, together with the nosep LOWER-R2 VALID on the same rows. The s21f gap (lower 4/25, upper 65/406) is reported as it stands.
- **Regression:** with hat5 off, the s18d engine must reproduce 6/35 on argsA52 (lowerR2 on cert_st16b0.json, upperR2 on sol_st16b0.json).

## Stage 18 result (07:57Z): hat channel H5 on argsA54: **upper 17/107 = 0.158879, below s21f's 65/406, but Long Table's kill line (2) is met**
- **Tests.**
  - Physical key test: 100,000 random diamonds, 0 mismatches (s18d/orient_hat5.log).
  - Broken-key control: 15,898 mismatches (s18d/orient_hat5_brokenkey.log).
  - Regression with hat5 off, on argsA52: LOWER-R2 VALID 6/35 on cert_st16b0.json and UPPER-R2 FEASIBLE at 6/35 on sol_st16b0.json (s18d/val_off_*.log).
- **Solve st18h** (s21f recipe + hat5; 20,676 sender rows with all hats enumerated, against 7,074 for s21f):
  - The keeppen fixed point is t = 0.158878504673 = **17/107**: 21 iterations, 2,089 s, inside the 90-minute line. The warm-row LP started at 0.15875 and t rose as rows were added.
  - **UPPER-R2 FEASIBLE at 17/107 on sol_st18h.json** (the new solution itself): senders 0; conservation 1,424 x 5^6, worst 1.3e-13; d = 7..17 exhaustive, 0 violated; Karp λ = 0.5561, d0 = 13.16.
  - nosep LP over the same rows (st18hL): **LOWER-R2 VALID t >= 10/63 = 0.158730 (138 rows)**.
  - So t*(H5 on argsA54) is in [10/63, 17/107]. The s21f baseline was [4/25, 65/406].
  - 86 r columns are positive. The largest are r[6,0,1,6,1,0] 0.155, r[5,0,7,9] 0.153, r[5,0,9,9] 0.141 and r[5,0,8,9] 0.140. The second group are 5-spokes with a big spoke on the other side, i.e. a big hat sending to a five whose face-neighbour is a 5.
- **Kill lines.**
  - (1) t* below 65/406: **passed** (upper 17/107 < 65/406, both checks on our engine).
  - (2) "dies if both 7665566/6675666 and 7655667/6756656 stay tight": **MET.** Both have slack 0 at sol_st18h, and again at sol_st18hL. Their dual weight is 0 in both certs.
    - At sol_st18h: 7665566/6675666 = y7|5566 0.599 + y7|5576 0.312 + M 0.139 + M 0.109. 7655667/6756656 carries r[6007] 0.049 outflow.
  - (3) "any 5-5-5-face 7 row stays tight": met as well. The heaviest cert row is still 7665566/6765766, with dual 0.104 in the st18hL cert (0.083 at sol_st18h).
- **Cert support (st18hL).**
  - Receivers: 7665566/6765766 0.104; 9 655566556/759556565 0.055; 7676556/7759565 0.055; 10 6556655556/6665669665 0.022; 8 86555665/56576665 and 86566656/55566555 0.013.
  - Senders: face fives 55669, 55667, 55767 and 55959; also 56669, 56959 and 55686.
- Files: s18d/{prelay2.py, cmd_st18h.sh, st18h.log, sol_st18h.json, cert_st18h.json, st18hL.log, sol_st18hL.json, cert_st18hL.json, lower_st18hL.log, upper_st18h.log, kill_st18h.log, kill_st18hL.log, screen_*.py, engine_md5.txt}. RELAY_SPEC 15.

## Stage 19 oracle pre-registration (08:10Z, before any solve): W forbidden by assumption (flag `w19`), over st18h
- **W (the window that would have to be proved reducible).** Six vertices:
  - a vertex u of degree exactly 7;
  - a 5-5-5 face (w_i, w_{i+1}, s_i): two consecutive link fives of u and their apex, all of degree 5;
  - a link 6 of u next to the face, w_{i-1} or w_{i+2}, of degree exactly 6;
  - that 6's private p (its neighbour not adjacent to u) of degree exactly 5.
  - In the binder 7665566/6675666 these are the cases p2 = 5 and p5 = 5; the second is the st15f blocker.
- **Why this one.** It is the smallest window the binder rows suggest that is also visible to an LP term. A link 6's window (w_{j±2}, s_{j-2..j+1}) sees a face only when the face is next to it.
  - Probe on sol_st18h: in all four binders the face-adjacent 6s already have private 5 removed by the §14′ filter (masks 28/30), and the M values are flat over the allowed privates (0.1393 / 0.1090).
  - W generalises those filter kills to every U = 7 window with a face next to the 6. Over all 5^8 U = 7 windows, 6,225 have such a face. p = 5 is already killed in 2,856 of them, and W adds 3,369.
  - Privates of 6s farther from the face, and the 7's own privates, are not in any term's window, so they are not in W.
- **Use.** amask(U = 7, ...) additionally clears the bit for p = 5 when (w_{j+1}, w_{j+2}, s_{j+1}) = (5, 5, 5) or (w_{j-1}, w_{j-2}, s_{j-2}) = (5, 5, 5). Everything else is st18h (hat5, s21/argsA54.txt, §14′ filter with s21/f/kill/kill6).
- **Result type.** An oracle bound for the class "no W". It is not a theorem until W is proved reducible.
- **Kill lines:**
  - (1) the oracle upper bound does not go below 17/107;
  - (2) the binder moves to face rows with no private 5, and there is no gain.
  - Wall cap: 90 minutes of solve.
- **If the gain is real:** report the W instances the LP certificate needs (as patterns), the gain, and the new binders.

## Stage 19 oracle result (08:45Z): **W is null. The lower bound is unchanged at 10/63, and kill line (2) is met**
- **Regression.** With w19 off, the s19d engine on cert_st18hL gives LOWER-R2 VALID 10/63 (s19d/val_off_lower.log).
- **Oracle solve st19w** (st18h + w19):
  - keeppen fixed point: t = 197/1240 = 0.158870968 (9 iterations, 1,037 s);
  - **UPPER-R2 FEASIBLE at 197/1240 on sol_st19w.json**;
  - nosep (st19wL): **LOWER-R2 VALID t >= 10/63 (112 rows)**, the same lower bound as st18hL without the oracle.
  - The upper moves by 7.5e-6 (17/107 → 197/1240) inside the open gap [10/63, 17/107]. That is a better primal point, not a gain in t*: assuming W is reducible proves nothing below 10/63.
- **Binders (cert_st19wL).**
  - The heaviest receiver moves from 7665566/6765766 to 7766556/6567566 (0.101), a face row whose two face-adjacent 6s already have private 5 forbidden by W. Kill line (2) is met: the binder moves to face rows with no private 5, and there is no gain.
  - The other receivers are as in st18hL: 9 655566556/759556565 and 7676556/7759565 (0.058); 10 6556655556/6665669665; and d = 8 86555665/56586665, 86566656/55566555 and 85586556/66656565.
- **Why (rowR2 at sol_st19wL).** All four face rows have load exactly y7|5566 0.738 + y7|5576 0.421 = 1 + t, with M = 0 and no r. The rows are 7665566/6675666, 7655667/6756656, 7766556/6567566 and 7665566/6765766.
  - The 7's whole budget goes to its two face fives through y.
  - Those y values are set by the face fives' worst sender contexts in the cert. The heaviest is 55667 [0,0,0,1,0|1,0] (0.101); then 55667 [0,0,1,1,0|0,0], 55669 [0,0,1,0,0|0,0], 55767 [0,0,0,0,0|0] and 55769, all with at most two big hats. Nothing about the link 6s' privates enters.
  - **So a lemma that helps must forbid a face five's worst context**, i.e. a 5-5-5 face whose surrounding hats are mostly small (the listed sender contexts), and not a private of a link 6. That is a sender-side window, and Explore should test that one.
- Files: s19d/{prelay2.py (= s18d + w19), cmd_st19w.sh, st19w.log, sol_st19w.json, cert_st19w.json, st19wL.log, sol_st19wL.json, cert_st19wL.json, lower_st19wL.log, upper_st19w.log, kill_st19wL.log, val_off_lower.log, engine_md5.txt}.

## Stage 19b pre-registration (before any solve): sender-side oracle Wf (flag `wf19`, list s19e/Wf.txt), over st18h
- **Wf.** Five sender contexts of a five v, taken from the cert_st19wL support. With hat5 every context is its own row: each listed (word, bits) is the only context producing its coefficient row (checked by full enumeration), so forbidding the label forbids exactly that context.
- **Notation.**
  - The link w0..w4 is the canonical word, with exact letters.
  - H[k] is the class of the hat between w_k and w_{k+1} (0 = small {5,6}, 1 = big >= 7). F[k] is the class of the private of the 6-spoke w_k.
  - In every context, w0 = w1 = 5, so (v, w0, w1) is a 5-5-5 face. H0 is the vertex across the face edge w0 w1, i.e. the third vertex of the other face on that edge.

| # | word w0..w4 | big hats | small hats | fans | free vertices (small / big) |
|---|---|---|---|---|---|
| 1 | 5 5 6 6 7 | H3 (between 6 and 7) | H0 H1 H2 H4 | F2 big, F3 small | 5 small, 2 big |
| 2 | 5 5 6 6 7 | H2, H3 | H0 H1 H4 | F2, F3 small | 5 small, 2 big |
| 3 | 5 5 6 6 9 | H2 | H0 H1 H3 H4 | F2, F3 small | 6 small, 1 big; w4 is >= 9 |
| 4 | 5 5 7 6 7 | none | H0..H4 | F3 small | 6 small, 0 big |
| 5 | 5 5 7 6 9 | H2 | H0 H1 H3 H4 | F3 small | 5 small, 1 big; w4 is >= 9 |

- **What Explore would have to prove.** No context is a single configuration, because each small vertex is 5 or 6.
  - Each context is a family of 2^(#small) exact cases on its small vertices: 32 or 64. The big vertices can stay on the ring, unconstrained.
  - The common core of all five is the 5-5-5 face (v, w0, w1) with w3 = 6 and with H0, H1 and H4 small. These are the vertices around the face's edges at v.
  - **#4 (55767, everything small) is the most plausible single-family target.** Its interior is exactly v's closed 2-ball apart from the two 7s, and every free vertex has degree <= 6.
  - #3 and #5 contain a >= 9 spoke, which would have to sit on the ring.
- **Use.** In R2_sender_rows, skip any context in Wf (flag `wf19 wf=s19e/Wf.txt`). upperR2 and lowerR2 use the same enumeration, so the oracle class is consistent. Everything else is st18h (hat5, argsA54, §14′ filter); w19 is off.
- **Kill lines:**
  - (a) the lower bound stays at 10/63, or the upper does not drop below 17/107 by more than solver noise (1e-6);
  - (b) the binder only moves to the next-worst context of the same face, with a gain under 0.005.
  - Cap: 90 minutes of solve.
- **If the gain is real:** drop contexts one at a time to find the minimal window list; report it with the new t and the binders.

## Stage 19b result (09:40Z): **Wf is null. Lower 10/63 and upper 17/107 are both unchanged; kill lines (a) and (b) are met**
- **Run.** The first launch read a Wf.txt that my own edit had broken (context #1 missing). I killed it within a minute; it produced nothing usable, and its 08:45 error logs were overwritten. Re-run from 08:46Z with all 5 contexts: the log shows "wf19: 5 of 5 forbidden sender contexts skipped", leaving 20,671 sender rows.
- **st19f** (st18h + wf19):
  - keeppen fixed point: t = 0.158878504673 = **17/107**, exactly st18h's value (5 iterations, 970 s);
  - **UPPER-R2 FEASIBLE at 17/107** on sol_st19f.json;
  - nosep (st19fL): **LOWER-R2 VALID 10/63 (127 rows)**, unchanged.
  - Kill line (a) is met on both sides.
- **Where the weight went (cert_st19fL).** Mostly to sibling contexts of the same faces, at the same total.
  - Three are the forbidden context with only H0 flipped to big, i.e. the vertex across the face edge w0 w1 made big: 55667 [1,0,1,1,0|0,0], 55669 [1,0,1,0,0|0,0] and 55769 [1,0,1,0,0|0] (0.055 each).
  - The others are 55667 [0,0,0,0,0|1,1] (0.097, the 55667 face five with all hats small and both fans big) and 55767 [0,0,1,1,0|0] (0.058).
  - Receivers: 7766556/6576576 0.104; 9 655566556/759556565 and 7676556/7759565 0.055; 10 6556655556/6665669665.
  - Kill line (b) is met: the binder moves to the next contexts of the same face, with gain 0.
- **Reading.** The certificate is degenerate over the hat classes of the face's ring. For each face five there is a whole family of contexts (varying H0, and the fans or hats away from the 7) with the same dual value, and the LP rebuilds 10/63 from whichever members are left. Forbidding contexts one by one cannot work.
  - A lemma that helps must remove the face five's context **for every class of H0 and of the far hats at once**. In practice that means the 5-5-5 face next to the 7, with only w3 = 6 and the two near hats fixed: the whole family, not a small window. Long Table found no D/C kill for it at ring <= 16.
- Files: s19e/{Wf.txt, prelay2.py (= s19d + wf19), prelay2_st19_backup.py, cmd_st19f.sh, st19f.log, sol_st19f.json, cert_st19f.json, rows_st19f.txt, st19fL.log, sol_st19fL.json, cert_st19fL.json, lower_st19fL.log, upper_st19f.log, engine_md5.txt}.

## family.json README (s19e/family.json: the 5-5-5-face family, shared with Explore and Studio)
Built by s19e/mkfamily.py, run on the s19e engine (hat5 class, s21/argsA54.txt, killtab s21/f/kill/kill6), from the three 10/63 certs: st18hL, st19wL, st19fL.
- **`definition`.**
  - The face: two consecutive receiver link fives with apex 5, or two consecutive sender spokes w_k = w_{k+1} = 5.
  - The hat convention: H[k] = class of the hat between w_k and w_{k+1}, 0 = small {5,6} / 1 = big >= 7. F[k] = class of the private of the 6-spoke w_k, listed in spoke order.
  - The w3 condition.
  - `fixed_bits_per_word`: per sender word, the H/F bits that are equal across every sibling context in the certs, with null where they vary. Example: 55667 always has H4 = 0, i.e. the hat between the 7 and the face-mate is small.
- **`receivers`** (13 rows): every face receiver with weight in any of the three certs, plus the six Long Table named. Fields:
  - d, link, apex (as stored);
  - canonical: the min over the 2d rotations/reflections, with the apex word reflected as s'_i = s_{-i-1};
  - faces_at_i;
  - dual: weight per cert;
  - admissible_argsA54.
  - The named rows 7665566/6675666, 7655667/6756656 and 7655666/6756666 have no weight in these certs; they are tight with dual 0.
- **`senders`** (26 contexts): word, H, F, face_pairs, dual per cert, and `expansion`.
  - `expansion` lists every exact 5/6 choice of the small vertices, with big vertices left as {7,8,>=9}. Each case is checked for joint admissibility, i.e. one letter per vertex shared by all spokes:
    - every 6-spoke wheel (5, w_{k+1}, H[k], F[k], H[k-1], w_{k-1}) must be non-R6;
    - every five-spoke link (5, w_{k-1}, H[k-1], H[k], w_{k+1}) must be non-R5;
    - big vertices may take any of 7/8/9.
  - Each context also records `why_not`, `n_cases` and `n_admissible`.
- **Finding (important for stage 20).** 8 of the 26 contexts have no admissible exact completion; they carry 0.42 of the summed max dual weight. Every 5/6 choice of their small hats makes a five-spoke's link R5 or a 6-spoke's wheel R6. They are:
  - 55667 [0,0,0,0,0|1,1], 55667 [0,0,0,1,0|1,0], 55667 [0,0,1,1,0|0,0];
  - 55668 [0,0,0,0,0|1,0];
  - 55669 [0,0,0,0,0|1,0], 55669 [0,0,1,0,0|0,0];
  - 55676 [0,0,1,1,0|0,0];
  - 55686 [0,0,0,1,0|0,0].
  - The engine's class-level sender admissibility checks each 6-spoke against hat classes independently, so a shared hat can be 5 for one spoke and 6 for the next. It never checks five-spoke links at all. These contexts are therefore impossible but still in the LP.
  - Three of the five stage 19b contexts are among them, which is why 19b's siblings could rebuild the bound. Exact hat letters with joint admissibility (stage 20) remove them soundly, with no oracle.

## Stage 20 pre-registration (before any solve): exact hat letters in sender admissibility (flag `hatx`, RELAY_SPEC 16), run st20x on s22/argsA55.txt over s22h
- **Rule.**
  - Sender contexts must have one exact letter per hat, in its class and shared by the two spokes it touches, that makes every 6-spoke wheel non-R6 and every five-spoke link non-R5.
  - Keys are unchanged: they read hats only by class.
  - This is a sound restriction of the class (it drops R5/R6-containing contexts). It is not an oracle.
- **Soundness.** A dropped context contains a reducible wheel at a spoke in every exact completion. Both-ends table: RELAY_SPEC 16. Physical test: 0 mismatches over 199,707 readings, broken control 80,050 (s20d/orient_hatx*.log). upperR2 and lowerR2 use the same enumeration.
- **Regression:** with hatx off, the s20d engine must reproduce s22h = 16/101: lowerR2 on s22/hf/cert_s22hL.json and upperR2 on s22/hf/sol_s22h.json.
- **Kill lines:**
  - (1) the upper bound (on the solution itself) is not <= 0.1534, i.e. the gain is under 0.005 below 16/101;
  - (2) the face family stays tight and is paid only by y and M;
  - (3) the solve wall time exceeds 3 x s22h (about 50 min).
- **Progress:** upper FEASIBLE <= 0.1534 on the new solution, with the nosep lower VALID.
- **Report:** t, the binders, and whether r or g flows into the face rows.

## Stage 20 result (10:35Z): **hatx is null on argsA55. Lower 16/101 is unchanged; kill lines (1) and (2) are met**
- **Regression** (hatx off, s20d engine): LOWER-R2 VALID 16/101 on s22/hf/cert_s22hL.json and UPPER-R2 FEASIBLE at 16/101 on sol_s22h.json (s20d/val_off_*.log).
- **Tests:** 199,707 spoke readings, 0 mismatches; broken-key control 80,050 (s20d/orient_hatx*.log).
- **st20x.**
  - hatx drops 696 sender contexts with no jointly admissible exact hat letters, leaving 20,082 sender rows after dedupe (20,676 in s22h).
  - keeppen fixed point t = 0.158441558 (5 iterations; solve 09:39:29Z–10:07:30Z, ~28 min, inside the 50-minute line). That is slightly above 16/101 because of the x penalty; the s22h solution is still feasible in this smaller class.
  - **UPPER-R2 FEASIBLE at 0.158441558** on sol_st20x.json.
  - nosep (st20xL): **LOWER-R2 VALID 16/101 (106 rows)**, unchanged.
  - Kill line (1) is met: no gain, and the target was <= 0.1534.
- **Binders (cert_st20xL).**
  - Receivers: 7665566/6765766 0.092; 7676556/7759565 0.066; d = 9 655665556/657565955 and 655566556/757656565.
  - Senders: the face fives again, now as **jointly admissible** contexts, most with H0 big (the vertex across the face edge): 55667 [1,0,0,0,0|1,1] 0.086, 55667 [1,0,1,1,0|0,0], 55669 [1,0,1,0,0|0,0], 55769 [0,0,1,0,0|0] (0.066 each), and 55767 [0,0,0,0,0|0] 0.056. The last two have admissible all-small completions.
- **How the face rows are paid** (rowR2, s20d/kill_st20x.log).
  - Every face row is tight, at both solutions.
  - At sol_st20xL: load = r[506507] 0.023 + y7|5566 0.714 + y7|5576 0.421 = 1 + t.
  - At sol_st20x: y drops to 0.349 / 0.326, but r[506507] rises to 0.246 and M 0.143 / 0.095 still apply. r[506507] is the 7's **outflow** to the face's third five, the 7 being a hat of that five.
  - **Nothing flows into the face rows.** No r reaches the 7, g only goes to fives, and the 7 is only ever a payer. Kill line (2) is met in substance: the face 7 pays its two face fives and the face's third five through y, M and r, and the LP only moves charge among these.
- **Reading.** Exact hats remove the impossible contexts (family.json's 8), but the face family is genuinely admissible once H0 is big, and the bound holds there. The deficit of a 5-5-5 face next to a 7 is paid entirely by that 7 under every rule class tried (stages 17-20), so the family needs either a reducibility argument for the whole face family or a rule that brings charge into the 7 from outside its 2-ball.

## Stage 22 pre-registration (design-only, before the probe): face / balanced initial charge (RELAY_SPEC 18), no LP solve
- **Question.** Does re-basing the initial charge onto faces (balanced d-6 / 2len-6, or 6-d / 6-2len, or the Euler family vertex 6-(1+e/3)d with face charge e, or a shared charge on each 5-5-5 face) change t* for the current rule shapes (y, g, h, M, r, x)?
- **Equivalence check.** Write each re-basing as old charge + a fixed conservative local flow T. If T = 0, or T lies in the cone of existing columns, the LP is the same (null by construction). Any free face->corner rule composes to co-facial edge transfers; those in existing directions are spanned, and the reverse directions (big->five, 6->five, big->6) are screened exactly against cert_st20xL (16/101): a reverse column is profitable iff its forward column has reduced cost > 0.
- **Probe.** s22d/probe22.py (stage-20 engine copy, md5 in s22d/engine_md5.txt), on cert_st20xL and s19e/family.json only. Log: s22d/probe22.log.
- **Kill line (verbatim from the brief):** stop if the face family still binds at a value >= the current t*, which is 16/101 on 5fa0adb0.

## Stage 22 result (design-only): **the face / balanced re-basing is null by construction; the kill line is met**
- **Balanced charges (d-6 / 2len-6, or 6-d / 6-2len).** These give charge 0 to every face, because every face of a triangulation is a triangle. They are the current LP, or its sign mirror.
- **Euler family (vertex 6-(1+e/3)d, face e).** These are the only Euler-valid linear face charges on a triangulation (RELAY_SPEC 18.1). The family differs from the current charge by a fixed local flow (e/3 from each vertex to each incident face). Under the current rule shapes, with faces as transit, that flow composes to T = 0, so the LP and t* are unchanged.
- **Free face rules.** These compose to co-facial edge transfers. Their only new directions at existing keys are the reverses of y, g and h. On cert_st20xL, every y, g and h column has reduced cost exactly 0, so every reverse column has reduced cost 0 as well. Together with the unchanged primal this gives **t* = 16/101 exactly** (s22d/probe22.log; the run takes 3 s, with no LP).
- **5-5-5 shared charge.**
  - With faces as transit, the shared charge is again T = 0.
  - If faces are allowed to hold charge, the old cert gives a lower bound of t >= 144/1069 (0.1347). That is a normalisation artifact and not progress: at t <= 0 the faces hold nothing, so the zero crossing is that of the current LP (RELAY_SPEC 18.4).
- **Probe on family.json.** Under every re-basing, all 13 receivers and the 18 admissible sender contexts keep their rows. The face 7 row 7665566/6765766 stays tight at 1 + 16/101, so the 7 still goes negative and binds at 16/101. **The kill line is met.**
- **Not covered here.** The following are new channels or key refinements, not re-basings:
  - 5<->5 transfers on non-5-5-5 faces;
  - 6<->6 transfers;
  - keys finer than the existing ones.
- **Lead (outside §18).** Two r columns have reduced cost > 0 under cert_st20xL: r(5,0,6,7) at 2/303 and r(5,0,7,5,0,7) at 1/303. The second touches the d=9 row 655566556/757656565 and the face sender 55767. Their reverse would be a distance-2 transfer from the hat big to the five. That is not ruled out by this cert, and it was not built.

## Stage 23 pre-registration (before any solve): reverse hat channel rr (flag `hatrr`, RELAY_SPEC 15r), run st23r on s22/argsA55.txt over s22h
- **Rule.** A new column `rr[K] >= 0` under §15's key K, moving charge from the big hat b to the five v (b -> v). It has coefficient -1 in v's senderR2 row and -1 in b's receiverR2 load, i.e. exactly -r, so r becomes free in sign.
- **Soundness.** Both ends compute the same K (§15 table). Charge is conserved, as the physical test checks: for r and for rr, v's coefficient equals b's, and rr is -1 at v. Two controls: brokenkey, and brokensign (b gets +rr).
- **Regression:** with hatrr off, the s23d engine must reproduce s22h = 16/101: lowerR2 on s22/hf/cert_s22hL.json and upperR2 on s22/hf/sol_s22h.json.
- **Recipe.** The s22h recipe (s22/hf/cmd_s22h.sh) with `hatrr` added:
  - keeppen solve (xpen 1e-3);
  - nosep solve for the lower bound;
  - lowerR2 on the nosep cert, and upperR2 on the keeppen solution itself.
- **Kill lines:**
  - (1) the gain is under 0.005, i.e. the upper bound on the solution is not <= 0.1534;
  - (2) the rr columns enter with total weight under 1e-3.
- **Report:** t, both checks, the rr weight and where it flows, and whether anything reaches the face 7s.

## Stage 23 result: **the reverse hat channel rr is null on argsA55. t* = 16/101 exactly; kill line (1) is met**
- **Physical test** (s23d/orient_hatrr*.log). Over 100,000 diamonds there are 0 mismatches: keys agree, r and rr conserve charge, and rr points b -> v. The brokenkey control gives 15,898 mismatches; the brokensign control (b gets +rr) gives 100,000.
- **Regression** (hatrr off, s23d engine): LOWER-R2 VALID 16/101 on cert_s22hL (114 rows), and UPPER-R2 FEASIBLE at 16/101 on sol_s22h (s23d/val_off_*.log).
- **st23r** (keeppen, 10:50Z-11:35Z, about 45 min while sharing CPU with another job). Fixed point t = 0.158441558 after 10 iterations.
  - **UPPER-R2 on sol_st23r itself: INFEASIBLE (6).** All sender rows and every d = 7..17 receiver and the tail pass. The 6 failures are conservation on no-five 6-links, such as (6,7,9,7,6,8), with worst 0.0078.
  - **Cause: an engine gap, not rr.** Without v6, the solver separates conservation only over 6-words that contain a five. upperR2 checks all 1,424 words. Here h ended up positive on keys that are shared with no-five links. Earlier solutions happened to have h = 0 on those keys.
- **st23rL** (nosep): **LOWER-R2 VALID t >= 16/101 (115 rows)**, unchanged.
- **The class optimum.** sol_s22h (rr = 0) is UPPER-R2 FEASIBLE at 16/101 under the hatrr engine (s23d/upper_s22h_hatrr.log). So **t*(hatrr) = 16/101 exactly**: the gain is 0, below the 0.005 target, and kill line (1) is met.
- **rr weight.** Kill line (2) is not hit. rr enters with total 3.667 over 19 keys at sol_st23rL, and 3.790 over 29 keys at sol_st23r. It flows mostly on diamonds with one five-spoke (big Z1) and one big spoke: (5,1,6,8) 0.705, (5,1,5,9) 0.605, (5,1,5,8) 0.590, (5,1,6,9) 0.407. No rr key also carries r.
- **Face 7s** (s23d/kill_st23r.log, section 1 convention, load = inflow). rr does reach the face 7s, as an **outflow from the 7 to the face's third five**: rr[506507] = 0.0074 at sol_st23rL and 0.0039 at sol_st23r. This replaces st20xL's r[506507] = +0.023, which ran from that five into the 7. The face fives' y rises to compensate (y7|5566 0.714 -> 0.745), so the face rows stay tight at 1 + 16/101: 0.745 + 0.421 - 0.0074. The face fives have nowhere else to send, so whatever the 7 pushes out comes back through y.
