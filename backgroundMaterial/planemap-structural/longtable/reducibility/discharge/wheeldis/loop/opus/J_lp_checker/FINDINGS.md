# J: independent checker for the discharging LP bound (18 Oct 2026, 11:35Z-13:05Z) [E]

Question: can the LP's t* (7/27 today; Job 30 A/B next) be verified from the row definitions, independent of
sep3x/feascheck, on both sides? Guess: yes, d = 7 the slow part. Plan-changer: a failure on either side of 7/27.

1. **Lower bound reproduced, exact.** The j28_13 dual certificate is valid: t >= 7/27 with weights 10/27 55667 +
   5/27 55767 + 2/27 77777 + 10/27 receiver d = 7 5675765/6577575 (`cert_j28_13.json`). The receiver row is admissible
   against our own loading of 15,897 patterns (14,860 D + 1,037 C; 9,314 at d = 7), 104 RBIG wheels, the R5/R6 wheels,
   7 D fans and 2.122. No y <= 1 bound used. Own LP (x = 0, own separator) held t = 7/27 for iterations 0-6 (48,820
   rows), still adding ~3.5k rows per iteration when stopped: lower-side evidence only (`solve_j28_13.log`).
2. **Upper bound not finished.** No full-precision round-13 y exists on the branches read; the 4-decimal y in
   out/wlp3_j28_13.txt was tested at t = 7/27 + 1e-3. All 342 sender rows pass; the exhaustive d = 7 receiver run did
   not finish in 30 min (`upper_4dp_plus1e3.log`); d = 8..17 and the Karp tail not run. **No upper verdict.**
3. Timing per d (one core): d = 7 minutes to tens of minutes (130k pattern instances); d = 8 ~14 s; d = 9 ~2 s;
   d = 10..17 < 1 s. Speedups not done: break the 2d symmetry; tighter bound than max over unread letters.
4. B_rsst_rows' `wlp3r_w0_sol.json` is infeasible (d = 8, e.g. 55657567/56565557 load 2.74 > 2.26; d >= 9), as
   expected from a warm-row-only LP. It was never claimed as a bound.
5. Semantics: load = sum over positions of a 5^9 window table over (w_{i-2..i+2}, s_{i-2..i+1}), carrying y outflow,
   x transfers, rule-T outflow flags and T inflow; -inf marks an R5 word or a 6 with no non-R6 private. RBIG links
   (d = 7, 8) and pattern instances excluded under all 2d symmetries with every specified slot kept. d > dmax:
   relaxed max-plus DP without patterns (conservative), then exact pattern-free search, then Karp on the letter-9 matrix.
6. Read: README §0/1/6/7.3, JOB28, COORDINATOR-STATE Job 29/30, G/B FINDINGS; code for input formats only (wlp.py,
   wlp3.py, wlp3x taus() and docstring, wlp3xt ykey/tkey and JSON keys, feascheck.py). Not read: sep3*.cpp.
7. Run on Job 30's dump (M = a wheeldis extract, e.g. `git archive origin/main`):
   - `python3 jcheck.py lower cert=C.json root=$M args=ARGS [nf=KILLS]`
   - `python3 jcheck.py upper sol=S.json root=$M args=ARGS [nf=KILLS] [dmax=17 dtail=30 excl=out/def_,hr1_or1]`
   - `args=` takes Studio's .args files (pat=/cpat=), or `argsjson=`. Part A kills: any `f<d>_<link>_<s>` name with
     s-letters at non-five slots honoured, in a pat file or `nf=FILE` (a name, or `d LINK SWORD`, per line).
   - Solution JSON: `t`, `y{"7|5566":v}`, `x{"<tau int>":v}`; part B: `yT{"75566|01":v}`, `tau{"75566|10a":v}`
     (Studio's keys, re-derived with own ykey/tkey carrying the side). Rule-T sender rows checked over every
     z-bigness assignment with the 6-wheel coupling; T inflow takes the conservative maximum.
   - Certificate JSON: list of `{"w":"p/q","row":["sender",W] | ["receiver",d,LINK,S]}`; rule-T certificates not yet.
8. Untested: the x and T paths (no converged x or T solution exists; the T = 0 test via to_tzero.py not run).
   Next: `upper` on a full-precision 7/27 y (Studio's feascheck solution JSON), d = 7 detached (an hour or more).
