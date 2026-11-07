# s86 p1r: KEYSPEC v2 single-row receiver key coefficients (flag `p1r`)

Spec: W6b `KEYSPEC2_RECEIVER.md` (md5 d5a6734b) sections 1, 2, 3.3, 4, 5, and `P1R_NOTE.md` (f0312e8e).
Engine: `s86_f2b7/eng_p1r`, a copy of `s86_f2b7/eng` (the live engine was not edited; its md5s at copy time are in `eng_md5_at_copy.txt`).

## What changed

On a receiver row of degree d = 7 or 8, every generic key K (`gkeys=`) now gets

    coef_K = max over realisations rho of IN(K; rho) - OUT(K)

This replaces the "possibly" IN count at d = 7 and the gkwin window bound at d = 8. OUT is the existing exact sure count.

### Realisations

A realisation picks one group G_j = (x_j, y_j) per link, independently, from dom_j:

* x_j = w_j's private next to s_j (W6b a_j, edge56 pin(j, 1));
* y_j = w_j's private next to s_{j-1} (W6b b_{j-1}, pin(j, 0)).

The domains are exactly the ranges of the row's own masked base terms:

| link | domain |
|---|---|
| 5 | its rotation, (s_{j-1}, s_j) |
| 6 | {(p, p)}, p in pallow(sig2 + amask & ~extra6), not R6 |
| 7 | {(p1, p2)}, the q7m / f2b7 masks (L3T at d = 7, the l3qV = 8 table at d = 8, & ~extra7, 31 & ~extra7 on a side with c or apex >= 7), pair not RBIG |
| >= 8 | all 25 pairs |

The IN slot readings are spec section 2:

* (i, +1): S.L+3 = y_i, S.L-3 = x_i, S.A+1 = x_{i-1}, S.A-1 = y_{i+1};
* (i, -1) is the mirror.

The max is an exact max-plus product round the d-cycle of sites Q_j = (x_j, y_{j+1}). Keys whose live slots match on every letter of the domain skip it.

### Files

| file | change |
|---|---|
| `eng_p1r/p1r.py` (new) | Exec'd by `pcheck.py` after `edge56.py`. Without the flag it only defines functions. With `p1r` it overrides `gk_recv_terms` and `recv_coef_R2` at d = 7 / 8; d >= 9 rows go to the unchanged code. |
| `eng_p1r/pcheck.py` | One added exec line. |
| `eng_p1r/edge56.py` | **(1)** If gkleaf is on and there are more than 64 payer-7 keys, the d = 7 leaf binary becomes `bin/jsepf_gk_k192`; the merged 200-key file has 77. With <= 64 keys nothing changes. **(2)** dualexport: d = 7 / 8 receiver rows under p1r get `mode = 'p1r'` and `ks_current`, the coefficients without p1r; `meta['p1r']` says so. |
| `eng_p1r/jsepf_gk_k192.cpp` | `jsepf_gk.cpp` with only the 7802 header limit raised from 64 to 192 keys. Mode-2 ids 1800000100 + k stay below the 7804 ids 1800000300 + k. |
| `bin/jsepf_gk_k192` | Built with `cd eng_p1r && c++ -O3 -march=native -std=c++17 -pthread -o bin/jsepf_gk_k192 jsepf_gk_k192.cpp`. bin/ is gitignored, so rebuild after a fresh checkout; the launcher checks for it. |
| `p1r/runK86p.sh`, `watchL86p.sh`, `wtest86p.sh`, `dualwatch86p.sh` | Copies of the live scripts. The only differences: `E86` is set to `eng_p1r` after sourcing `env86.sh` (env86.sh is not edited), the watcher reads the cert from `eng_p1r`, and run.log lines name the engine. |
| `../launch_k86GL4.sh` | k86GL3's family plus `p1r` on eng_p1r. Keys come from `$KEYS4`, default `p1r/cg_keys_r13w16_16f.txt`. Not started. |
| `p1r/cg_keys_r13w16_16f.txt` | md5 **ea5d79a75a4e99bfe6be99e6efca805a**: r13w16 (171) + `cg_keys_w6b16f_cur.txt` (19) + `cg_keys_w6b16f_v2.txt` (10) = 200 keys. Names are unique; none is K1. A1/C1/E1 coincide with edgekeys_r4 names, but `edgekeys=` is not in the family. |

Git holds only the eng_p1r files that differ from eng: `p1r.py`, `pcheck.py`, `edge56.py` and `jsepf_gk_k192.cpp`. To rebuild eng_p1r elsewhere:

1. `cp -a eng eng_p1r`, taken from the eng state recorded in `eng_md5_at_copy.txt`.
2. Put those four files on top.
3. Build k192.

The test key files are:

* `keys_test_p67.txt`: r13w16 + P67a;
* `keys_test_r13w16_16fcur.txt`;
* `keys_test_r13w16_16fv2.txt`.

### Unchanged

The following keep their current coefficients:

* d >= 9 receivers, senders, cons2 and mrows;
* every separator: the jsepf leaf 7802 / 7804, the gkwin tables and the class fold;
* upperR2, which is C++ only.

## Tests

The runners are `p1r_test.sh` (driver for `p1r_test.py`), `p1r_run.sh` (one pcheck command on eng_p1r with the GL2 / K3g family flags) and `p1r_gk67.py`. Logs and JSON are in `p1r/logs/`.

### (a) Test vectors

`test_vectors.json` (892f1e1f): **24 / 24** reproduced (OUT, IN max, IN min, p1_r, and current incl. the d = 8 window).

### (b) Coefficient changes on the GL2 cert

Cert `cert_k86GL2_p1` f8893e87: 816 d = 7 / 8 receiver rows x 171 r13w16 keys = 139,536 pairs.

* **64 changes**, IDENTICAL to `p1r_changes.json` (2c0c1333): same pairs, same values.
  * By key: E1 52, A1 5, gk00_50 2, and one each for gk02_25, gk01_67, gk02_85, gk01_100, gk01_108.
  * **0 increases.**
* At d = 8, p1_r <= the KEYSPEC picture <= the window on all 45,657 pairs.
* 0 rows with an empty domain; 595 rows needed the DP.
* An independent brute force (gk_slots on exact-letter pictures, every realisation of the links a live slot reads) agrees on 4,191 pairs, with 0 mismatches. 520 pairs were skipped as having more than 4,000 realisations.

Merged 200-key file (`p1rtest_merged16f`): 163,200 pairs, 263 changed, 0 increases. The r13w16 part is still identical to W6b's 64.

**The 29 16f keys:** 816 x 29 = 23,664 pairs, **199 changed, 0 increases**.

| key | changes |
|---|---|
| v03 | 31 |
| v01 | 29 |
| v04 | 27 |
| v02 | 23 |
| v05 | 20 |
| v06 | 20 |
| v08 | 20 |
| c04 | 9 |
| c07 | 8 |
| v00 | 5 |
| c15 | 3 |
| v07 | 2 |
| c08 | 1 |
| v09 | 1 |

The brute force agrees on 4,906 pairs (0 mismatches; 699 skipped).

With the 29 keys as extra columns (5,528 columns), the restricted LP on the cert's 3,529 rows reaches t = 0 under both current and p1r coefficients. That is the conservation floor. It says only that the cert's rows no longer bind once the new keys are priced; new rows are needed.

W6b's `check.json` reports 773 "v2max > current" for the 16f keys. That is an artifact of their current values coming from a dual export with no ks for those keys (cur = 0). Recomputed in the engine, no pair increases.

### (c) Restricted primal LP

The LP is min t over the cert's 3,529 rows (5,499 columns), solved with scipy HiGHS.

| coefficients | t |
|---|---|
| current | **0.00188205161548**, the same under the default solve, dual simplex and IPM |
| p1r, default solve | 8.34064865e-5 |
| p1r, dual simplex and IPM at 1e-10 tolerances | **8.33748473e-5** |

W6b report 8.33866e-5, and 8.3375e-5 as p1_rc.

The default-solve point is feasible (max row violation 8e-12) but slightly suboptimal: it stops within HiGHS's 1e-7 dual tolerance.

* The two tight solves (dual simplex 8.33748473188e-5, IPM 8.33748473203e-5, row violation <= 8.5e-12) agree to 2e-15 absolute and match W6b's p1_rc.
* The p1r LP's optimum is therefore sensitive to solver tolerance at about 4e-4 relative; the current LP is not.

### gkselftest and gkwintest

**gkselftest PASS** (worked examples, KS vs K* on 20,000 rows, mirror on 6,000 pictures) on:

* `keys_test_p67.txt` (r13w16 + `P67a EDGE({67}->7)[S.L+1=S S.L-1=S S.L-3=5 S.A-1=B]`);
* r13w16 + `cg_keys_w6b16f_cur.txt` (b167547d);
* r13w16 + `cg_keys_w6b16f_v2.txt` (9925c5bb);
* the merged file.

**gkwintest PASS** on p67 and on the merged file.

### Multi-letter payer {67} and set payees (`p1r_gk67.py`)

The check runs on every key with a multi-letter payer or payee set:

* p67 file: A1, E1, P67a;
* merged file: A1, E1, c00-c04, c07, c14, c15, v01, v03, v06, v07, v08.

For each such key, the counts must equal the sum over its single-letter split keys on:

* receiver pictures at d = 7 / 8 / 9 (3,000 each);
* all R2 sender pictures;
* all cons2 pictures (all6 x {5,7}^6);
* gk_tables at U = 7 / 8 / 9.

It also checks p1_r: the split maxes must satisfy max(parts) <= max <= sum(parts).

The leaf files are written and decoded, and each record is compared with its key:

* 7802 (payer-7 keys: payee mask and conditions);
* 7804 (payee-7 keys: payer mask and conditions).

**Both files PASS with 0 failures.**

* p67: P67a has 7802 payee mask 4 with 4 conditions, and 7804 payer mask 6. It is nonzero on 2,115 / 91,136 cons2 pictures and 916 / 2,000 d = 7 receivers, and zero on senders and d = 8 / 9 receivers, as it should be.
* Merged: the brace payees `6->{67}` and `7->{79}` parse and split correctly.

### Python vs C++ leaf (f2bself)

This test runs without p1r: `upperR2 ... f2bself=3000 q7force`. It compares the Python row value with the C++ jsepf leaf total on 3,000 arrangements at each of d = 7, 8 and 9. Both sols are copies of `sol_repS2W_04` with extra key amounts; they are not candidates.

| keys | extra amounts | leaf binary | result |
|---|---|---|---|
| `keys_test_p67.txt` (62 payer-7 keys) | P67a = 0.05 | `jsepf_gk` | PASS: max abs difference 5e-13 at d = 7, 8 and 9 |
| `cg_keys_r13w16_16f.txt` (77 payer-7 keys) | the 29 16f keys at 0.02 each | `jsepf_gk_k192` | PASS: max abs difference 5e-13 at d = 7, 8 and 9 |

The second row shows that the k192 build reads all 77 7802 records and agrees with Python.

### Without the flag

Command: `bash p1r/p1r_run.sh upper_noflag_repS2W_04 upperR2 nomax sol=cand/sol_repS2W_04.json`. It runs eng_p1r with the K3g family, r13w16, gkwin and gkleaf, without p1r.

* Result: **`UPPER-R2: FEASIBLE at t = 0.038043023627`**.
* The log is line-for-line identical to `logs/upper_F_repS2W_04.log` (39 lines). The only differences are the 11 timing fields.

## Interpretations and caveats

1. **Separators keep the current coefficients.** The jsepf leaf (d = 7: possibly-IN, 7802 OUT), the gkwin window tables (d = 8) and the class fold are >= p1_r. A separator may therefore report a row that is not violated once Python recomputes it under p1r (a "phantom").
   * solveR2's `recv()` dedups rows, so an iteration whose violated rows are all phantoms adds 0 rows and ends the run early.
   * That costs quality, not soundness. Every row in the LP and in the cert is a Python p1r row, and lowerR2's exactbasis check re-derives the rows in Python.
   * The real fix is a p1r-aware jsepf leaf, which is not done here.
2. **upperR2 and wtest are C++-only**, so they price keys with the current coefficients. A solution feasible only under p1r is rejected, which is conservative.
   * f2b_selftest (Python row vs C++ leaf) will report differences under p1r on rows where p1_r < current. Run it without p1r, as below.
3. **Empty domain.** A d = 7 / 8 row whose domains admit no realisation cannot occur. It keeps its current coefficients rather than getting -inf. No cert row has one.
4. **Domains = base-term ranges, asserted per row.** The M / Q / lQ entries implied by the domains must equal the row's own (`recv_coef_R2` below the gkeys wrapper). Each domain projection must lie inside `gk_recv_picture`'s private masks. Any disagreement raises, so the coefficient is never silently weaker than the spec. This is how sections 1 and 5 ("the same sets the masked model already uses") were read, including f2b7's 31 & ~extra7 on a 7's side with c or apex >= 7.
5. **d = 8:** p1_r replaces the gkwin window coefficient on Python rows only. Separators keep the window (caveat 1).
6. **Keys reading no private position** get max IN - OUT with the domains still applied (P1R_NOTE). That equals the current count unless a domain is empty.
7. **Payer-8 keys** (PAYER8SPEC) do not exist in these key files, since payers are 5 / 6 / 7. OUT at d = 8 is therefore 0.
8. **More than 64 payer-7 keys.** The merged file has 77. The live `jsepf_gk` refuses more than 64 (exit 92), and the live `gk_write` asserts it. Hence `jsepf_gk_k192`, used only when there are more than 64.
   * The original `bin/jsepf_gk` (c31466c0) could not be rebuilt byte-identically from `jsepf_gk.cpp`: same size, different .text, probably a compiler or flag difference. So k192 is validated by f2bself rather than by binary identity.
9. **dualexport** marks p1r rows `mode = 'p1r'` and adds `ks_current`. `window_rows_where_window_differs_from_picture` also counts the p1r rows whose coefficients differ from current.
10. **Cost.** The p1r setup is about 2.1-2.5 ms per d = 7 / 8 row. At ~100k warm d = 7 / 8 rows that adds a few minutes per full row pass.
