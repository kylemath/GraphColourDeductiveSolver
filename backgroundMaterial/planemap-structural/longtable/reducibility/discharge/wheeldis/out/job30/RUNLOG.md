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
