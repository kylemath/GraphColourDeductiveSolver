# Job 30 (Studio, 18 Oct): receiver patterns with letters on non-five slots; Rule T (part B)

## Code (part A)
- sep3.cpp / sep3x.cpp → bin/sep3f, bin/sep3xf. New optional input section "NF" + lines "d k slot mask …".
  - Slot w_i = i and s_i = d + i, with a 5-bit letter set per slot. All 2d dihedral images are stored; under
    reflection w_i → w_{-i} and s_i → s_{-i-1}.
  - Checked at the leaf on the complete (w, s) word, and in the `c` command. Rows are still deduplicated by their
    variable/transfer signature, so a row survives iff some filling of it is pattern-free. The bound is untouched
    (patterns only remove leaves), so B&B stays exact.
  - d ≥ 16 DP and the Karp tail are unchanged: patterns exist only for d ≤ DMAXP.
- wlp3.py: `fullparse`/`dropped`. A name with a letter on a slot no link 5 reads goes to the new section (FULLP)
  instead of `parse`.
  - **Soundness note:** `parse` silently drops such letters, which weakens the pattern, so it forbids more than the
    configuration covers. Audit (`audit_drop.py`): 0 of the 16,411 loaded registry patterns are affected. Scanning
    every window file in out/ and loop/, only loop/k34 has such windows (3 names).
  - Such names now assert WLP_SEPF=1, so they can never again be loaded weakened.
- wlp3x.py and feascheck.py use the f-binaries when WLP_SEPF=1.

## Validation (part A)
- (b) Matcher, using sep `c` on row R's 25 (s1, s4) fillings:
  - With f7_5567576_5....5. loaded, sep3xf forbids exactly the 9 fillings with s1 = 5 or s4 = 5, which is explore's
    count. The mirror image comes from the dihedral images.
  - Without the pattern (sep3xf) and with the old binary (sep3x_new), all 25 are allowed. So the non-five letters are
    read, and nothing else changes.
- (a) Regression (`regress.py`): the same 6 queries go to the old and the new binary. They use run29b's registry, the
  j29 one-off solution's (y, x), d = 7..12, threshold d - 6 + t - 0.4, top 20 rows, and the default node limit. With
  the new section empty, the output is **byte-identical**, node counts and abort flags included (`reg_sep3x*.txt`).
  The full-LP check of 7/27 with no new patterns is the run A control. Exhaustive feascheck at eps = -0.4 was
  too slow (over 20 min at d = 9), so I stopped it.
- (c) Exactness: after convergence, feascheck with WLP_SEPF=1 (SEP_NODELIMIT=0, exhaustive) on the solution must
  print FEASIBLE. That makes t* exact (upper = lower).

## Added windows (all D on Studio dfast18, `addA_dfast18.out`, and on explore's kc, `loop/k34/fill_kc.out`)
- f7_5567576_5....5. (ring 13, both explore lines: fill.txt and full.txt), f7_5567576_5....56 and
  f7_5567576_5.5...6 (ring 13). These are all the windows the old encoding dropped.

## Run A (L2: wlp3x, xcap 3, warm = out/job28/j29b_final_rows.txt; registry = run29b's + addA)
- H30 (A): with R's 9 s1/s4 = 5 fillings forbidden, u → w2/w4 transfers relieve the 16 survivors, and the
  converged t* < 7/27.
- Kill: converged t* = 7/27 (with FEASIBLE at 7/27) → H30 dies; the certificate survives on the 16 fillings.

## Part B (Rule T)
- Parked per Long Table's final order: write no B code until A has reported, and run B only if A holds 7/27.
- The draft, written against E_rule_change section 3 and untested, is on branch `studio/job30-ruleT-wip` (97bbe5d7).
  It still has to be re-specified against loop/opus/G_ruleT_lp.
- H30B: t*(A+T) < t*(A). Kill: t*(A+T) = t*(A).

## Scope add (09:55Z): explore round 37 C window, and k3x windows loaded by glob
- **`dropped()` tightened.** `parse` keeps only fives whose four slots are all specified, plus those slots. A letter
  read only by an incomplete five was also dropped. The test now uses parse's actual coverage. Re-audit: still 0 of
  16,411 registry patterns affected (`audit_drop.py`, same rule).
- **f7_5566757_...5...** (ring 13, w2 + link 7665575 + w0; its s3 letter is on a slot no link 5 reads), loaded through
  the NF section.
  - Studio cfast: C, X = {I0-I1}, 66,430 / 8,537 / 59,788, leftover 0 (`c37_studio.cfast`). It equals explore's
    cwin.cfast and kc -C (fill_kcc.out: C-REDUCIBLE X={I0-I1}).
  - Matcher: 210 frames (all 14 dihedral images × letters 5..9 at the s slot × 3 random fillings). It newly forbids
    exactly the 35 frames with 5 at that slot and nothing else, so 0 mismatches. The w4 mirror is among the images.
- **`twoeng.py`** builds k3x_D.out / k3x_C.cfast from loop/k3*/ at run start. D needs dfast(18) D and kc D. C needs
  cfast C and kc -C C with the same X.
  - Today it loads 3 D (the k34 family) and 1 C (the window above).
  - Excluded: f7_..57556_...65.. and f7_..57556_...66.. (C on both engines, but with different X), and 1 window
    that only one engine has seen.

## 10:05Z: explore's dropped list (loop/drop/dropped.txt, 7 windows) and fixed-X agreement
- The list equals my audit plus three windows that arrived later. Nothing is missing on either side.
- f7_..57556_...65.. (11) and f7_..57556_...66.. (12): kc -C -x with Studio cfast's X {R0-I0,I0-I1,I0-I3,I3-I7}
  accepts it with leftover 0 (loop/k37/lt_cfastX.kc). twoeng.py now reads kc fixed-X lines.
- f7_5567576_.....5. (13): cfast's search finds a size-4 X, and kc finds {I0-I4}. Studio `cfast --fixed I0-I4` gives
  C-REDUCIBLE, leftover 0, on both of explore's lines (loop/k3studio/c5_fixedX.cfast). twoeng.py now reads cfast
  fixed-X lines. Rule: some single X accepted by both engines.
- twoeng now loads all 7 (3 D, 4 C).
- `matchtest.py`: sep3xf against an independent Python matcher on 140 frames per window (all dihedral images, half
  matching and half with one slot broken): 587 frames that the base allows, 0 mismatches.

## 10:15Z: explore round 38 (loop/k38, 5 w2-frame C kills), conservative X only (Long Table)
- f7_5667576_..5.... (14) and f7_5675767_.5..... (15): cfast's X is accepted by kc conservatively (kills_cfastX.kc,
  adm=yes leftover 0).
- f7_..65757_..65... (13) and f7_..65757_..55... (12): cfast's size-4 X is broad only. Studio `cfast --fixed I0-I2`
  (kc's conservative X) gives C-REDUCIBLE, leftover 0 (loop/k3studio/k38_a_fixedX.cfast).
- f7_..56757_...5... (13): cfast's X is broad only. Studio `cfast --fixed` with kc's conservative
  {I0-I4,I1-I5,R1-I0,R8-I5} gives C-REDUCIBLE, leftover 0 (k38_b_fixedX.cfast).
- So **all 5 qualify under conservative X**, and none needs the broad tag. A' (the broad-X variant) therefore equals A.
- twoeng.py now compares X as edge sets and ignores kc -C2 (broad) files (kills_cfastX_C2.kc). Loaded at run A's
  start: 3 D and 9 C.
- Matcher test on the 5: 623 frames that the base allows, 0 mismatches.

## C5 (Opus F review, 18 Oct)
122.1031's X has a ring–interior edge (R8-I3, or R6-I2 mirrored). Its admissibility rests on the registry's existing
"C cons." standard (the inherited RSST free-completion / ring-injectivity argument), as for every C window here. It is
not new to F.

## Hypothesis and kill line for F (before F runs)
- H30F: t*(A+F) < t*(A+B).
- Kill: t*(A+F) = t*(A+B), with F FEASIBLE (feascheckt in tfull + tkill mode).

## 19:45Z: explore k43, f8_...55565_...5.... (kills the 1/4 binder, d = 8 85556565/65866655)
- twoeng: C on both engines with one X, {I0-I1}: kc -C, and cfast --fixed with leftover 0 (loop/k43, f1f71335).
  The default glob is widened from loop/k3*/* to loop/k[0-9]*/*. twoeng now loads 3 D and 12 C.
- Loaded through the NF/whole-arrangement type: parse() would drop the letters on slots 3–7 and s3, so the window
  is routed to FULLP.
- sep3xf `c` on the binder row: 1 without the window, **0 with it**. networkx: the configuration's interior (degrees
  5555568) embeds into the row's arrangement model (induced, triangles onto triangles).
- Matcher test: 63 base-allowed frames, 0 mismatches.
- Long Table: Opus re-solves first, and Studio is the second engine (feascheck + lowercheck on their primal and
  certificate).

## twoeng after round 44/45 and the drop44 fix (18 Oct ~20:45Z)
- Inputs: local loop/k[0-9]* (k34..k42, k3studio), with k43/k44/k45 taken from explore's d3def56a
  (claude/project-thread-nh6pv2, extracted with git archive). kc -C2 files are ignored, including k44 rsst_C2.out,
  rsst_C2_cf.cfast and rsst_verdicts_C2.txt (the 51 broad-only configs).
- k44 alone: 196 D, 181 C (0 one-engine, 0 X mismatch). k45 alone: 7 D, 0 C.
- Full set: **378 D, 383 C** (was 187 D / 209 C).
  - Removed: exactly the 16 drop44 names (11 D, 5 C).
  - Added: 195 D from k44 (1 was already in) and 7 D from k45; 179 C from k44 (2 were already in).
  - 0 of the 16 present.
- Default-glob reruns need the local loop/k43 updated to d3def56a first; the local copy still holds the 16.
- 20:47Z: local loop/k43 was updated to d3def56a, and loop/k44 and loop/k45 were added (every file byte-identical to
  d3def56a). A default-glob twoeng then reproduces 378 D / 383 C, byte-identical to 30f86cd4, with 0 of the 16.

## twoeng after explore round 47 part A (97233611, loop/k47), 18 Oct ~21:32Z
- loop/k47 fetched by explicit path; 26 files, byte-identical to 97233611. k47 alone: 43 D, 39 C (0 one-engine, 0 X
  mismatch), as explore's scratch run.
- Default glob: **421 D / 422 C** (was 378 / 383: +43 D, +39 C; the 82 new names are exactly k47's).
- Drop44 guard (a '.' link slot w_i with both s_(i-1) and s_i fixed): the rule flags 16/16 of the drop44 names, 0 of
  the 82 new names and 0 of the existing registry. Nothing excluded.
- Matcher spot-check (matchtest.py, 11 sampled k47 names): 577 frames, 0 mismatches.
- Not taken (outside this request): explore's later k45 update (round 45 complete, +5 D kills) and the k44 broad
  diagnostics (C2 files, and rsst_x_kc.out, which is kc output only and cannot pass twoeng without cfast).
- ~21:35Z: explore's k45 update (round 45 complete, 97233611; 6 changed files copied by path, all of loop/k45 now
  byte-identical to 97233611). k45 alone: 12 D, 0 C. Default glob: **426 D / 422 C** (+5 D, 0 lost). New D:
  f7_..55855_..66666, f7_..55865_..6656., f7_..55865_.6665.., f7_.558556_.6666.., f7_.558556_.66666.
  Drop44 guard 0 flagged. Matcher on all 5: 219 frames, 0 mismatches. The k44 C2 diagnostics stay out.
- ~21:58Z: explore batch 4eefe5f5 (loop/k47 r7c/r7b1/r7b2 kills of the 1/5 receiver d=7 7765556/6575765). Only the 17
  new files were fetched by path, byte-identical; the modified A_* raw files were left at 97233611. k47 alone: 74 D /
  65 C, as explore's run. Default glob: **457 D / 448 C** (+31 D, +26 C, 0 lost, 0 one-engine, 0 X mismatch).
  Drop44 guard 0 flagged. Matcher (11 names, including the smallest kill f7_...5556_...576.): 488 frames, 0
  mismatches. Job 31 does not get this batch.
- ~22:55Z: explore round 49 (3a156a49, loop/k47/r9c_kills*: kills of the s14 d=9 binder 656566565/665656666). The 5
  r9c files were fetched by path, byte-identical; the other files of that commit (k46 grow*, A_*, win45) were not taken.
  r9c alone: 30 D / 55 C, as explore's run. Default glob: **487 D / 503 C** (+30 D, +55 C, 0 lost, 0 one-engine, 0 X
  mismatch). Drop44 guard 0 flagged. The 11 minimal names are all in, all C. Matcher (17 names: the 11 minimal plus a
  sample): 1,670 frames, 0 mismatches. dcount on argsA44_local (k3x at this commit, plus r_5..r_8): **15,527** distinct
  parsed D patterns (15,861 names), which is 15,497 + 30.
- ~23:12Z: explore 1287f92d (loop/k47/r9b_kills*: kills of the d=9 relay row 656565665/665666566). The 5 files were
  fetched by path, byte-identical; r7d is empty and skipped. r9b alone: 28 D / 45 C, as explore's run. Default glob:
  **510 D / 522 C**: +23 D, +19 C. 5 D and 26 C were already in the set from earlier batches, as were 8 of the 11
  minimal names. 0 lost, 0 one-engine, 0 X mismatch. Drop44 guard 0. Matcher (8 names: the 3 new minimal plus a
  sample): 797 frames, 0 mismatches. dcount (argsA44_local): **15,550** distinct parsed D (15,884 names), +23.
- ~01:40Z 19 Oct: explore 3b08eef3 (loop/k47/r9d_kills*: kills of the relay d=9 row 656656665/665555555). The 5
  files were fetched by path, byte-identical; r7d16 is empty and skipped. r9d alone: 295 D / 88 C, as explore's run.
  Default glob: **804 D / 604 C** (+294 D, +82 C; 1 D and 6 C were already in, as were 2 of the 29 minimal names).
  0 lost, 0 one-engine, 0 X mismatch. Drop44 guard 0. Matcher (43 names: the 27 new minimal plus a sample): 4,066
  frames, 0 mismatches. dcount (argsA44_local): **15,844** distinct parsed D (16,178 names), +294.
- ~02:00Z 19 Oct: explore d6196b7b (loop/k47/r10a_kills*: kills of the relay d=10 row 6556656556/6665656665). 5 files
  fetched by path, byte-identical. r10a alone: 11 D / 8 C, as explore's run. Default glob: **815 D / 612 C** (+11 D,
  +8 C, 0 lost, 0 one-engine, 0 X mismatch). Drop44 guard 0. Matcher (10 names: all 7 minimal plus a sample): 933
  frames, 0 mismatches. dcount (argsA44_local): **15,855** distinct parsed D (16,189 names), +11.
- ~02:45Z 19 Oct: explore 40dae1f9 (loop/k47/r7e_kills*: kills of the d=7 row 7665666/6566565). 5 files fetched by
  path, byte-identical. r7e alone: 22 D / 11 C, as explore's run. Default glob: **837 D / 623 C** (+22 D, +11 C,
  0 lost, 0 one-engine, 0 X mismatch). Drop44 guard 0. Matcher (12 names: all 4 minimal plus a sample): 783 frames,
  0 mismatches. dcount (argsA44_local): **15,877** distinct parsed D (16,211 names), +22.
- ~05:20Z 19 Oct: explore 452045da (loop/k47/r10b_kills*: kills of the relay binder d=10 6565656565/6655666666).
  5 files fetched by path, byte-identical. r10b alone: 4 D / 10 C, as explore's run. Default glob on the 8e008f86 set:
  **841 D / 633 C** (+4 D, +10 C, 0 lost, 0 one-engine, 0 X mismatch). Drop44 guard 0. Matcher on all 14 new names
  (both minimal ones included): 1,402 frames, 0 mismatches. dcount (argsA44_local): **15,881** distinct parsed D
  (16,215 names), +4. Explore reports no kills of 7655666/6756666 at ring <= 16, so there is nothing to admit for it.
- ~07:55Z 19 Oct: explore round 51, 33a69199 (loop/k47/r8b_kills*: kills of the s20c d=8 binder 76566656/65566556).
  5 files fetched by path, byte-identical. r8b alone: 28 D / 25 C, as explore's run. Default glob on 880d25c6:
  **869 D / 658 C** (+28 D, +25 C, 0 lost, 0 one-engine, 0 X mismatch). Drop44 guard 0. Matcher (17 names: all 4
  minimal plus a sample): 1,233 frames, 0 mismatches. dcount (argsA44_local): **15,909** distinct parsed D (16,243
  names), +28.
- ~09:00Z 19 Oct: explore round 51, a4b32eb2 (loop/k47/r9f_kills*: kills of the part-1f d=9 binder
  765556565/566956665). 5 files fetched by path, byte-identical. r9f alone: 93 D / 75 C, as explore's run. Default glob
  on 5fa0adb0: **962 D / 733 C** (+93 D, +75 C, 0 lost, 0 one-engine, 0 X mismatch). Drop44 guard 0. Matcher on all
  19 minimal windows: 1,435 frames, 0 mismatches. dcount (argsA44_local): **16,002** distinct parsed D (16,336
  names), +93.
  - Letter 9: none of the 168 names contains a 9. The binder's 9 is s_3 of its s-word, outside every kill window.
    Studio's parse / fullparse raise (AssertionError / KeyError) on a 9 in a non-p name rather than misreading it, so a
    future f-name with a 9 cannot slip in silently, but would need an explicit reading (9 = {>= 9}) added first.
- 19 Oct ~09:10Z: letter-9 rule (8682f8ac, Long Table confirmed) applied at admission in twoeng.py. Two-engine names
  with a 9 in the link or s word are excluded from k3x and logged to out/job30/letter9_excluded.log (letter9.lp_reading).
  f9_ names whose only 9 is the centre are admitted as normal. The frozen wlp3.py parser is unchanged. Regression on
  the default glob: 962 D / 733 C, k3x byte-identical (0 names excluded).
- ~10:10Z 19 Oct: explore round 51 r9g, c3d5cfc3 (loop/k47/r9g_kills*: kills of the part-1f binder d=9
  655665556/666559575). 5 files fetched by path, byte-identical. r9g alone: 457 D / 57 C, as explore's run. Default glob
  on 35aeebb8: **1,419 D / 790 C** (+457 D, +57 C, 0 lost, 0 one-engine, 0 X mismatch). Drop44 guard 0. Letter-9
  rule: 0 excluded. Matcher on all 17 minimal windows: 1,234 frames, 0 mismatches. dcount (argsA44_local): **16,459**
  distinct parsed D (16,793 names), +457.
- ~11:20Z 19 Oct: explore round 51 r9e, 43fdc043 (loop/k47/r9e_kills*: kills of the d=9 face row 655566556/757656565).
  5 files fetched by path, byte-identical. r9e alone: 540 D / 59 C, as explore's run. Default glob on 4b28f532:
  **1,894 D / 838 C**: +475 D, +48 C. 65 D, 11 C and 6 of the 17 minimal names were already in the set, from r9g's
  overlapping windows. 0 lost, 0 one-engine, 0 X mismatch. Drop44 guard 0. Letter-9 rule: 0 excluded. Matcher on all
  17 minimal windows: 1,248 frames, 0 mismatches. dcount (argsA44_local): **16,934** distinct parsed D (17,268 names),
  +475.
- ~11:30Z 19 Oct: explore round 51 r7h, deded528 (loop/k47/r7h_kills*: kills of the d=7 face row 7676556/7759565; the
  cfast file is empty, since there are no C names). Files fetched by path, byte-identical. r7h alone: 3 D, as explore's
  run. Default glob on 03c34729: **1,897 D / 838 C** (+3 D: f7_5567676_..5..5., f7_5567676_5.5..5.,
  f7_5567676_5.5..56; 0 lost). Drop44 guard 0. Letter-9 rule: 0 excluded. Matcher on the minimal window
  f7_5567676_..5..5.: 63 frames, 0 mismatches. dcount (argsA44_local): **16,937** distinct parsed D (17,271 names), +3.
