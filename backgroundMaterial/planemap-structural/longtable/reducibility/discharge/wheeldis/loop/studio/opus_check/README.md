# Studio second-engine checks of Opus results (loop/studio/opus_check)

**Required steps for every no-T [E2] check (Long Table, 18 Oct 21:52Z):**
1. `feascheck.py SOL.json <args>`: exhaustive receiver separation (sep3xf, d = 7..15) plus the max-plus DP tail.
   It does NOT evaluate sender rows.
2. `sendercheck.py SOL.json <args>`: every Studio sender row at the solution must have lhs <= -1.
3. `lowercheck.py CERT.json <args>`: rebuild the cert rows exactly. Each row must be a Studio row, and the combination
   must give t coefficient -1 and 0 negative terms.
- All three run with WLP3X_DEF=1 WLP_SEPF=1, from this tree's wheeldis root (so out/job30 loads).
4. Loaded-count check: `dcount.py ARGSFILE` counts **distinct parsed D patterns** per file (dedupe by parsed pattern,
   not by name; Long Table 21:58Z) and gives the total. Diff it per file against the other engine's list before
   reporting, and explain every differing file. Pin any file that moves (k3x) to the commit the solve used.

# Second engine for Opus's t* = 1/4 (P_own_lp, 0daf5198), Studio, 18 Oct ~18:50Z
Inputs (copied from claude/project-thread-7uelj0 at 0daf5198): sol_s2x.json, cert_s2x.json, argsA.txt (local copy
argsA_local.txt with their absolute k42map path pointed at k42map_C_cons.cfast here), k42map_C_cons.cfast.
- Registry diff vs Studio: their args = Studio's base (round-13 args + loop/n9) + addA_dfast18 + k3x_D (3 D) +
  k3x_C (11 C, including f7_.557657_.56.77. and f7_5567567_56.77.6) + their k42map_C_cons. That last file is Studio's
  10 claim-grade k42 windows, without the two [E2, broad X] RSST 126.8168 windows. So it is Studio's B registry minus
  the broad pair, and without Rule T.
- **Upper:** `feascheck.py sol_s2x.json` with WLP3X_DEF=1 (excl = hr1_or1 only) and WLP_SEPF=1 (whole-arrangement
  patterns), exhaustive sep3xf, d = 7..15, plus the d > 15 DP: 0 violated at every d, **FEASIBLE** at t = 1/4
  (feas_s2x.log). 16,413 parse patterns, plus the NF section.
- **Lower:** `lowercheck.py` rebuilds the 5 certificate rows with Studio's own wlp3x code (sender rows; recv_row with
  L2 transfer types).
  - The d = 8 receiver 85556565/65866655 passes sep3xf `c` on the same registry. The 4 senders are Studio sender rows.
  - With exact rational weights 1/4, 1/8, 1/8, 1/4, 1/4, every y and x term cancels. The t coefficient is −1 and the rhs
    is −1/4, so **t ≥ 1/4** (lower_s2x.log).
- So t* = 1/4 exactly on that registry, on two engines (Opus's jsep2 and Studio's sep3xf/wlp3x).

## Second engine for t* = 5/21 (P_own_lp, 9a914f8c: argsA + L2 + the k43 kill), 18 Oct ~20:05Z
- Args diff vs Studio's 1/4 registry: only cpat k43_C.cfast (f8_...55565_...5...., the window Studio verified, 54e6a39e).
- **Upper:** feascheck sol_s6.json (WLP3X_DEF=1, WLP_SEPF=1, exhaustive, d = 7..15 + DP): 0 violated everywhere,
  **FEASIBLE** at t = 5/21 (feas_s6.log).
- **Lower:** lowercheck on cert_s6.json: all 25 rows rebuilt as Studio rows (16 senders, 9 receivers, each allowed by
  sep3xf `c`, 0 rejects). The exact combination has every y and x term cancelling, t coefficient −1, rhs −5/21, so
  **t ≥ 5/21** (lower_s6.log).
- So t* = 5/21 exactly on that registry, on two engines.

## Second engine for t* = 11/47 (P_own_lp, bbd46d73: argsA + the full k43 batch + RSST-D + Rule T option B + L2), ~20:30Z
- Args diff vs Studio: argsA43 = argsA6 with the single-window k43_C swapped for k43_kills_df.out (184 D) and
  k43_kills_cf.cfast (198 C). Both are byte-identical to explore's loop/k43 files (c5a71dc0).
- RSST-D enters through `rpat=` (their rpatD.txt is byte-identical to Studio's loop/studio/rsstD/out/rpatD.txt). It
  was **not** in Studio's A/B base registry; it was used only in the rD1 re-solve. wlp3.py now reads `rpat=` (raw sep3
  patterns).
- Keys: all 1,036 Y and 104 T keys of sol_s6t43.json are canonical under Studio's ykey/tkey (0 not canonical), so
  nothing is merged or double-counted. They load into wlp3xt's indices without error.
- **Upper:** feascheckt.py (wlp3xt option B, sep3xt exhaustive, WLP_SEPF=1, excl = hr1_or1, RSST-D loaded). Sender
  rows evaluated directly; d = 7..15 receivers 0 violated; DP tail clean: **FEASIBLE** at t = 11/47 (feas_s6t43.log).
- **Lower:** lowercheckt.py rebuilds all 24 rows with Studio's code:
  - 12 senderT rows matched to Studio's sender rows by word + bits;
  - 4 mrows T[key] ≤ M_b, each key a Studio inflow completion for b;
  - 8 receiverT rows, each allowed by sep3xt `c`, with inflow slots carrying M_b.
  - Exact combination: every term cancels, t coefficient −1, rhs −11/47, so **t ≥ 11/47** (lower_s6t43.log).
- So t* = 11/47 exactly with Rule T on that registry, on two engines.

## Second engine for the no-T baseline t* = 11/47 (P_own_lp s7, fa4705f2), plus the round-44 drop re-check, ~20:45Z
- **Args diff:** argsA43noT.txt + rpat=rpatD.txt matches Studio's argsNoT_local.txt line for line, apart from three
  paths that point at Opus's directory. Those three files (k42map_C_cons, k43_kills_df, k43_kills_cf) are
  byte-identical, and so is rpatD.
- **Lower:** lowercheck on cert_s7.json rebuilds all rows with Studio's code. Each receiver is ALLOWED by sep3xf `c`.
  The exact combination has t coefficient −1, rhs −11/47 and 0 negative terms, so **t ≥ 11/47** (lower_s7.log). Dropping
  patterns only adds rows, so this holds on the drop44 registry too.
- **Drop44 (explore d3def56a, loop/k43/kills_drop44.txt, 16 names):** explore's fixed k43 files equal Studio's loaded
  copies minus exactly those 16 (11 D lines, 5 C blocks): k43fix_kills_df.out (173) and k43fix_kills_cf.cfast (193 C).
  They are byte-identical to Opus's s9 *_drop44 files (10e819df).
  - **Gotcha:** the registry also loads out/job30/k3x_D.out and k3x_C.cfast (the twoeng set). That set already carries
    the full k43 batch, including all 16, and the loader dedupes by name. So swapping only the k43 files still loads
    all 16. The first feasfix runs did exactly that (full=400) and are void.
  - argsFix2_local.txt drops the 16 everywhere: k43fix_* plus k3x_D_fix.out (176) and k3x_C_fix.cfast (204), which
    are the committed twoeng set minus the 16. A scan of every pat/cpat file in it finds 0 of the 16. Loaded:
    patterns=16575, full=384, which is 400 − 16.
  - **Upper, drop44 registry:** feascheck sol_s7 (WLP3X_DEF=1, WLP_SEPF=1, exhaustive sep3xf, d = 7..15 + DP)
    0 violated, **FEASIBLE** (feasfix_s7.log). feascheckt sol_s6t43 (Rule T B) 0 violated, **FEASIBLE**
    (feasfix_s6t43.log).
  - 5/21 (argsA6): its only k43 file, k43_C.cfast (the 54e6a39e window f8_...55565_...5....), contains none of the
    16, and its k3x set predates the k43 batch. So 5/21 was never affected.
- So t* = 11/47 holds with and without T on the drop44 registry, on two engines.

## Second engine for the no-relay baseline t* = 2/9 (P_own_lp s9, f1a052b4) on the 30f86cd4 registry, ~21:06Z
- **Args:** argsA44.txt + rpatD = Studio's argsK45_local.txt, except that ours also lists k43fix_kills_df/cf. Every
  name in those two files is already in k3x_D/C (30f86cd4), so the loaded set is the same. Their k3x_*_30f86cd4 and
  k42map_C_cons are byte-identical to ours. Loaded: patterns=16587, full=752, the same as Job 31's blind solve.
- **Upper:** feascheck sol_s9 (WLP3X_DEF=1, WLP_SEPF=1, exhaustive sep3xf, d = 7..15 + DP): 0 violated, **FEASIBLE**
  (feas_s9.log).
- **Lower:** lowercheck on all 6 cert rows (senders 55667, 55767, 56668, 58778; receivers d=7 8655675/5756585 and d=8
  75576556/78756665, both ALLOWED by sep3xf `c`). Exact combination: t coefficient −1, rhs −2/9, 0 negative terms, so
  **t ≥ 2/9** (lower_s9.log).
- So the no-relay t* = 2/9 on that registry, on two engines.

## Second engine for the main-line t* = 1/5 (P_own_lp s13, d065b212) on the aee20e3b registry, ~21:55Z
- **Args:** with their three paths mapped to ours (k3x_D/C_aee20e3b byte-identical to out/job30 at aee20e3b, and
  k42map_C_cons), argsA46 + rpatD == argsA44_local.txt. Root = this tree, so out/job30 loads (addA_dfast18 3, k3x_D
  423 after name dedupe, k3x_C 422, k42map 9).
- **Loaded counts vs Opus's** (D 15,461 / C 1,468 / RPAT 158): C 1,468 and RPAT 158 match. **D is 15,800 here, 339 more.**
  Studio counts the u*.pat files once per degree (u1 455, u2 119, u10 27). The counting convention is unresolved. The
  extra 339 patterns can only remove receiver rows, so the upper check below is on a registry at least as large.
  patterns=16588, full=838.
- **Upper:** feascheck sol_s13 (WLP3X_DEF=1, WLP_SEPF=1, exhaustive sep3xf d = 7..15, max-plus DP d = 16..30): 0
  violated, **FEASIBLE** (feas_s13.log). No Rule T here, so sep3xt does not apply.
- **Sender rows** (new, sendercheck.py; feascheck checks receivers only): all 342 Studio sender rows hold at sol_s13
  (max lhs −1.000000000, send_s13.log). Controls: sol_s9 passes; sol_s13 with t = 0.19 violates 337.
- **Lower:** lowercheck on the 4 cert rows (senders 55757, 55767, 57667 at 1/5; receiver d=7 7765556/6575765 at 2/5,
  ALLOWED by sep3xf `c`). Exact: t coefficient −1, rhs −1/5, 0 negative terms, so **t ≥ 1/5** (lower_s13.log).
- So t* = 1/5 on that registry, on two engines.

## Second engine for t* = 1/5 on 42c4c876 + job28 r_5..r_8 (P_own_lp s14, 8592bb50), ~22:15Z
- **Args:** argsA47 + rpatD, with Opus's paths mapped to ours, equals argsA44_local.txt with out/job30 k3x at
  42c4c876. All 11 files they ship (k3x_D/C_42c4c876, k42map_C_cons, job28 r_5..r_8 .out/.cfast) are byte-identical
  to ours. The check runs on argsA47_pinned.txt (k3x pinned to 42c4c876).
- **Counts (dcount.py):** 15,497 distinct parsed D patterns (15,831 names, 334 duplicates), C 1,494, RPAT 158. All
  match Opus's figures (studio_s14_dcount.txt).
- **Upper:** feascheck 0 violated at d = 7..15 plus the DP tail: **FEASIBLE** (feas_s14.log).
  sendercheck: 342/342 sender rows hold, max lhs −1 (send_s14.log).
- **Lower:** lowercheck on the 3 rows: senders 56696 at 1/5 and 66669 at 3/5; receiver d=9 656566565/665656666 at 1/5,
  ALLOWED by sep3xf `c`. Exact: t coefficient −1, rhs −1/5, 0 negative terms, so **t ≥ 1/5** (lower_s14.log).
- So t* = 1/5 on that registry, on two engines.

## Opus relay s14r (t = 19/102, 39f457ba): key mapping onto wlp3r6, stopped at step (a), ~22:45Z
- Files: sol_s14r.json (model 'R6x': 776 y, 45 g, 889 h, 8 x) and cert_s14r.json (25 rows: 7 senderR with flag-bit
  vectors, 7 cons over six words, 7 mrowR, 4 receiverR). Opus's lower_s14r.log and upper_s14r.log are not in 39f457ba.
  argsA47 is unchanged since s14, so its dcount (15,497 D / 1,494 C / 158 RPAT) stands (studio_s14_dcount.txt).
- maprelay.py (keys only; Opus code not read; map_s14r.log):
  - y: all 776 keys are wlp3r6 y roots.
  - **h → y6b: 889/889 one-to-one** (every h key is a wlp3r6 y6b key as written; 0 collisions, 0 R6 words).
  - **g → y56: 0/45.** g keys are (letter, 3 flag bits, letter), with first letters 5/6/7 and last letters 6..9. wlp3r6's
    y56 is a 6→5 move keyed by the five's full word (294 keys), with no flag-indexed moves and no moves out of a 7.
  - senderR rows carry flag bits, and mrowR rows are M-variable rows. wlp3r6 has neither.
- **So Opus's class has relay moves wlp3r6 cannot express.** Per Long Table's order, the upper (relay mode) and lower
  rebuild through wlp3r6 were not forced. 19/102 cannot be second-engined through wlp3r6 as it stands.

## Standalone check of Opus relay s14r (t* = 19/102, 39f457ba) from RELAY_SPEC.md (be66f349), ~23:15Z
- Checker: out/job31/s14r_check.py, written from the spec alone (copy here as RELAY_SPEC_be66f349.md); no Opus code
  read. Log: s14r_check.log. Registry: argsA47_pinned.txt (42c4c876 k3x + job28 r_5..r_8 + rpatD).
- **Spec-side rebuild, all equal to the spec's check values:**
  - R5 24 / R6 31 / FANS 7: the same sets as listed. RBIG 104.
  - 342 sender words; 6,915 senderR rows; 102 g columns.
  - 975 signatures; 4,760 M rows; 4,760 h columns.
  - 994 relay words.
  - Patterns by an independent spec-4.5 loader: D 15,497 / C 1,494 / RPAT 158.
- **Upper: FEASIBLE at 19/102.**
  - Bounds: 0 negative values, max x 0.0686 (<= 3).
  - senderR: 0 violated (min slack −3e−14).
  - cons: 0 violated (max |g − h| 3e−13).
  - mrowR: M = max h over cand, by construction.
  - Receivers d = 7..15: Studio sep3r, exhaustive, 0 violated. DP d = 16..30 clean.
  - Karp λ = 0.516339869, covering d >= 12.020. Both figures are the spec's.
- **Studio's receiver rows = the spec rows:** 784 arrangements (the 4 cert labels, the heaviest 20 at each d = 7..15,
  600 random). 0 admissibility mismatches against a spec-4.4 admissible() with the spec-4.5 matcher, and 0 value or
  x-key mismatches over the 771 admissible ones.
- **Lower: VALID t >= 19/102.**
  - All 25 rows rebuilt from their labels (7 senderR, 7 cons, 7 mrowR, 4 receiverR); every label passes its spec check.
  - Exact cancellation: tco = 1, D = 19/102.
  - The only nonzero reduced costs are g[50016] = 2/17 (= 36/306) and M[76667] = 8/17 (= 144/306), both >= 0,
    matching spec 9.5. No negative reduced cost.
- **Readings chosen where the spec is open** (none decided by Opus's code):
  1. Spec 4.5's by-d pattern table (9,663 / 4,469 / 1,233 at d = 7/8/9) is read as counted per kind. Studio's union
     across kinds is 9,660 / 4,465 / 1,226; the per-kind totals match exactly. This does not affect matching.
  2. Name characters outside the 4.5 table (for example '9' in an e/f name): read as the exact letter. None occur.
  3. Sender dedupe on the "coefficient multiset" is read as the per-word coefficient vector. That gives 6,915, as the
     spec says.
  4. Spec 7 searches exhaustively to d = 17. Here d = 16, 17 go to the relaxed DP: sound, since dropping patterns only
     enlarges the set. x in the DP is bounded by z9 := the max x into a 9 (0 in s14r).
  5. The exhaustive receiver enumeration is Studio's sep3r, not a spec-written enumerator. That is why the row
     comparison above is included.
