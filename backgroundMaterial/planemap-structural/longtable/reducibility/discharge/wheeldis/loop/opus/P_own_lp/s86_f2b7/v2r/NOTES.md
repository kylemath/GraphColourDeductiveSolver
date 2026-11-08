# v2r running log (KEYSPEC v2 receiver realisation rows, engine eng_v2)

## Setup (2026-11-08)
- eng_v2 = cp -a eng_p1r (md5s of eng_p1r sources/binaries at copy time: eng_md5_at_copy.txt); run artifacts (rows_/sol_/cert_ k86*) removed from the copy.
- New: eng_v2/v2r.py (exec'd by pcheck.py after p1r.py; flag v2r).  Edited: eng_v2/prelay2.py (solveR2 recv/warm/sepround, lowerR2),
  eng_v2/edge56.py (dualexport receiverV2), eng_v2/pcheck.py (exec line, commands v2restricted / v2rtest).
- Row id ('receiverV2', d, link, apex, rho), rho = x_0 y_0 ... x_{d-1} y_{d-1}; x_j = w_j's private next to s_j (W6b a_j, edge56 pin(j,1)),
  y_j = w_j's private next to s_{j-1} (W6b b_{j-1}, pin(j,0)); 5: (s_{j-1}, s_j); 6: (p, p).  Domains = p1r_domains (unchanged).
- W6r's engine (r5lib etc.) is not on the shared drive, so k2b cannot be run here; unit checks use test_vectors.json, p1r_core
  (already = W6b's 64 changes) and brute force; the cross-engine check is the restricted LP vs W6b's numbers.

## Design decisions
- Separator check: MV2 = max h over sig2_keys (rule columns), q7m_write = max q over the masked pairs (rule columns), l3q_Qeff =
  max(LP lQ column, max lq over the mask) >= max lq; keys at current coefficients >= p1_r >= IN(K; rho) with ks >= 0.  So masked value >=
  v2 value pointwise (superset holds).  Under v2r no d = 7 / 8 envelope column exists in the LP (they only came from masked d = 7 / 8 rows),
  so lQ there is exactly max lq.  BUT jsepf mode 2 returns the K most masked-violated distinct classes; phantoms (masked-violated,
  v2-satisfied, e.g. receivers already in the LP) can fill the top-K, so the list is a superset only below the cap.  Mitigation: every
  round the DP re-scans all known d = 7 / 8 receivers (v2rescan=1), and the log flags CROWDED rounds (cap reached with phantoms).
- W6b's v2base_all (0.0012527) > mask (0.0012438) on the GL5 cert is not an error: in a RESTRICTED LP the envelope columns M / Q / lQ are
  bounded below only by the cert's own mrow rows, so a masked row can be weaker there than its exact-base split; KEYSPEC2 4.5 (v2 <= mask)
  is a statement about the full family (all mrow rows), not about a restricted row subset.

## Validation step 1 (unit; v2rtest on the GL5 p1_00 cert def2afcc, keys 16fi 56d144d5, K3g)
- (a) W6b test_vectors.json: 24 / 24 reproduced (OUT, IN max / min, v2 = max IN - OUT, by the DP with one key; builder IN at the DP argmax
  = DP value).  log v2r/logs/v2rtest_b2_GL5.log.
- (b) all 692 d = 7 / 8 receiver rows of the cert: per-key DP max / min IN and OUT = p1r_core (which reproduces W6b's 64 changes) on all
  152,240 (row, key) pairs; at 2 random points per row (random column values, random key amounts incl. negative) the DP max = the value of
  the rebuilt row at the argmax (v2r_best check) and v2r_row(label, rho) (lowerR2's rebuild) = the assembled row; 138,400 random realisations
  never exceed the DP max; exhaustive enumeration (builder on every realisation) = DP max on the 108 points whose product has <= 1500
  realisations (93,642 realisations); keymode cur / p1r rows carry exactly the masked row's key terms.  PASS, 0 failures (124 s).
  First run had a harness bug (random column values read for the ks columns instead of the key amounts; fixed in the test, not the engine).

## Validation step 2 (restricted LP on the GL5 p1_00 cert def2afcc: 3035 rows, 692 d = 7 / 8 receivers; keys 16fi; K3g; xcap=3; HiGHS
## incremental LP, tolerances 1e-10; seed point eng_p1r/sol_k86GL5_p1.json; v2r/rlp_queue.sh, logs v2r/logs/rlp_<mode>.log)
- mask (cert rows as masked rows, current keys): t = 0.001243775191 (scipy highs / ds / ipm 0.00124377519061); W6b 0.0012437751906. Match.
- p1r (cert's own model): t = 0.001233311856; W6b 0.0012333118559. Match.
- First v2 attempt crashed (IndexError): the DP point lambda read columns created by rows added in the same pass (beyond the solved
  vector).  Fixed in cmd_v2restricted (such columns read 0, as solveR2's sepround already did).  Not a row-builder issue.
- v2p1rkeys (realisation rows, base exact, keys at the p1_r coefficient): t = 0.001233311856 (scipy 0.00123331185593) after 18 LP solves,
  5048 realisation rows over 692 receivers (1 to 18 per receiver); = p1r = W6b p1r_enc 0.0012333118559.  Match.
- v2 (KEYSPEC v2 exact rows): t = -0.076947399076 after 17 LP solves, 4790 realisation rows over 692 receivers (1 to 15 per receiver,
  median ~7), 174 s; W6b v2all -0.0769473990760.  Match (11 digits).  Key amounts at the optimum = W6b's list (gk02_24 = cg12_76_0 = KS = 3,
  gk03_33 2.967698, gk00_58 2.664032, w6b16f_v04 2.571544, ...; cg12_58_1 here vs cg12_58_2 there at the same 2.094928: tie).
  Cutting-plane path: t = -3.13 after the seed rows, -0.0780 at it 10, converged at it 16; DP pass over 692 receivers 0.6-1.1 s.
- Coordinator 8 Nov: launch_k86GV1.sh uses args_A97_F_W13K3gB5b.txt (5e399535) instead of K5a; gate stays on GL5 def2afcc; keep
  test processes < 2.5 GB RSS, one at a time.  (restricted LP RSS ~0.6 GB.)
- v2curkeys (base exact jointly, keys at the current masked coefficients): t = 0.001252703507 (scipy 0.00125270350674) after 20 LP solves,
  5042 realisation rows; W6b v2base_all 0.0012527035067.  Match.  So all five restricted-LP models reproduce W6b to >= 10 digits.

## Validation step 3 (lowerR2 on the v2 restricted-LP dual v2r/rlp/cert_rlp_v2.json, md5 00affcfc: 1834 rows, 997 receiverV2)
- 3a exactbasis (exbmu=0 exbtol=1e-10, xcap=3, flag v2r): dual LP bound -0.076947399076; exact elimination of 2190 equations 2138 s;
  exact cert v2r/rlp/cert_rlp_v2_exb.json (md5 168d0b94, 1816 rows: 980 receiverV2, 393 senderR2, 341 cons2, 54 mrowR2, 34 receiverR2
  d >= 9, 14 mrowQ), rechecked from the file with norepair, every receiverV2 row rebuilt from its id by v2r_row:
  LOWER-R2: VALID  t >= -7400...8514/9617...8839 = -0.076947399076 (exact = the float optimum to 12 digits).
- 3c (the planted bug inside exactbasis) dropped: it only re-certifies the wrong rows (another ~40 min of exact elimination).
- 3b planted bug v2bug=p1p2 (the rebuild swaps every 7's two privates: q key, both lq letters and every IN slot reading them) on the
  exact cert, norepair: LOWER-R2 "VALID t >= -1.091284781" instead of -0.076947399.  The rebuilt rows no longer cancel: the mismatched
  q columns happen to keep rc >= 0, the mismatched lq / ks columns (capped at 3) are priced at their caps, so lowerR2 reports a far
  lower bound rather than INVALID.  The cert does not certify its value; on a lane cert (t1 > 0) the same bug shows as a collapsed bound.
- Controls: the v2 exact cert WITHOUT the v2r flag: INVALID (980 "receiverV2 ROW WITHOUT THE v2r FLAG"); the mask-mode dual (masked
  d = 7 / 8 receiverR2 rows) under v2r: INVALID (670 "MASKED d = 7 / 8 RECEIVER ROW IN A v2r CERT").

## Spec + test vectors
- V2ROW_SPEC.md written; 5 test vectors from the v2 dual (v2rshow -> V2ROW_vectors.json md5 b4b3eed4).  spec_check.py re-derives the key
  OUT / IN counts (from the spec's two position tables), the 6 / 7 copy terms (h2_of / qkey / lq formulas) and the full rows from the
  spec text alone, no engine code: PASS on all 5 (18 / 6 / 3 / 20 / 17 keys with IN or OUT, rows of 34 / 15 / 30 / 38 / 36 entries).

## Smoke of the k86GV1 setup (small warm set: the GL5 p1_00 cert's 692 d = 7 / 8 + 42 d >= 9 receivers and 441 cons2 rows; K3gB5b args,
## 16fik keys, GL6 flags + v2r, v2seed = GL5 p1 sol, v2rescan=1, v2inner=3 (warm re-solves), maxit=1; log v2r/logs/smoke_GV1.log)
- setup fine (asserts pass with p1r + v2r together); warm: 678 canonical d = 7 / 8 receivers seeded with 678 realisation rows,
  5.35 ms per receiver (v2r_struct + DP), warm total 15 s.
- phase 1 t1 = -0.4693 (tiny warm set); 3 inner rounds added 598 / 634 / 595 realisation rows; warm re-solves 41 / 49 / 49 s against
  ~7 s for the first (presolved) solve -> v2innercold=1 (default) now clears the solver before each inner re-solve.  t1 -> -0.4507.
- one separation round (1599 s, nearly all cons2 at this loose point): d = 7 listed 300 (K cap), v2-violated 300, phantoms 0 (159 new
  rows; duplicates are separator classes that map to the same canonical receiver); d = 8 listed 300 / violated 300 / 103 new; rescan of
  678 known receivers: 568 violated, 568 rows; 1278 DP calls at 5.11 ms.  Final dual cert contains receiverV2 rows.  RSS peak 2.08 GB.
- 3b' planted bug v2bug=h6 (every 6's h key built with its two outer links w_{j+2}, w_{j-2} swapped) on the exact cert, norepair:
  LOWER-R2: INVALID (239 h columns with negative reduced cost; h is uncapped).

## Smoke 2 (same small warm set, v2inner=4 with cold re-solves (clearSolver), nosep; log v2r/logs/smoke2_GV1.log)
- inner re-solves 12 / 15 / 17 / 21 s (warm ones were 41-49 s); t1 -0.4693 -> -0.4693 -> -0.4373 -> -0.3616; RSS peak 1.95 GB.
- launch_k86GV1.sh: v2inner=${V2INNER:-4} (V2INNER=0 = exactly GL6 flags + v2r).

## Misc (end of build)
- dualexport under v2r (smoke cert): DUALEXPORT 1816 rows incl. 980 receiverV2 (type, d, link, apex, rho, privates, ks = IN - OUT).
- eng_p1r md5 recheck against eng_md5_at_copy.txt: only eng_p1r/prelay2.py differs, changed 06:39 by another agent (cmd_upperR2
  "s86 tighten" SMIN sender-min logging; also in eng/prelay2.py).  Not ported to eng_v2: upperR2 only, the lower lane does not use it.
- Estimates for k86GV1 (full GL6 warm list, ~174k R lines, ~150k distinct d = 7 / 8 receivers): seeding ~13 min (5 ms per DP);
  rescan of every known d = 7 / 8 receiver ~13 min per round; GL6 phase 1 ~1780 s cold, so v2inner=4 adds up to 4 x (~25-30 min cold
  re-solve + ~13 min DP) per lext iteration.  The restricted LP needed 17 cutting-plane rounds, i.e. ~17 lext iterations with
  V2INNER=0 (~30-40 h) against ~4-5 with v2inner=4.  Memory ~5-5.3 GB at start like GL6, growing with the realisation rows (~7 per
  binding receiver in the restricted LP); start with MemAvailable >= 6 GB.
