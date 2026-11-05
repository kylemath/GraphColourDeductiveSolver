# Team D (round 6): K* and the generic EDGE family as engine families (s78_kstar)

Folder: `$B/s78_kstar/`, with B = `/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp`. README.md there gives the full spec and the code map. Every number below is from this engine at nice 15, 1 thread.

## Verdict

- **K\*** = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B] (cap 3) is a working engine family and passes all six tests.
  - The payer side is exact; the payee side uses exact masks plus a window bound; the leaf corrections are ≤ 0.
  - It adds nothing to the nc slack. Nothing is clamped.
  - A positive term outside WIN is impossible by construction and is also refused at run time (exit 81).
- **Generic EDGE family** (the coordinator's round 4 request): `EDGE(7->P)[slot conditions]`, where each key is a line in a data file.
  - **A1, C1 and E1** (W6 round 4's order) are in `eng/edgekeys_r4.txt` and pass all six tests plus the controls.
  - The payer side is exact: only positions inside the payer's 2-ball are allowed, others are refused. It is applied at the d = 7 leaf, where it is ≤ 0.
  - The payee credit is a window bound held in WIN at every degree, including d ≥ 10 and the Karp tail, and the LP rows use that same bound.
  - No slack, no clamps.
  - BC and BE are not included, as instructed.
- **Pointers** (nosep LPs, test 6):
  - **W6 pool, rrz model:** t 0.006468 → 0 with K\* at W6's amount 0.125. W6 had 0.005768 → 0.
  - **Binding set of the s77 L b77U6, base model, t 0.026384**, all amounts capped at 0.125:

    | keys on | t |
    |---|---|
    | K\* | 0.016626 |
    | A1 + C1 + E1 | 0.013354 |
    | all four | **0.002053** |

    With caps of 3, any of these sets reaches 0.
  - With the engine's full q7 key set, both small sets are already at the t = 0 floor without the new keys.
- **K solve: prepared, not launched**, on both stacks with K\* + A1 + C1 + E1 on (section 4). Both start points were re-checked with every new family on at amount 0, and each came back FEASIBLE at its reference t.

## 1. The families as implemented

Letters: B = {7, 8, 9+}, S = {5, 6}. Positions follow gext.py `EPOS`:
- S.L±k: the payer's link, counted from the payee.
- S.A+1: the vertex across the face (S.L+1, S.L+2) from u.
- S.A-1: the same across (S.L-1, S.L-2).
- R.L±2: the payee's next neighbour after S.L±1.

Each rule fires once per oriented match.

**K\* (`eng/kstar.py`, jsepf argv[13]).**
- Payer row (d = 7 centre, for each link 7 at i, e1 = ±1):
  - conditions: w_{i-e1} ∈ B, w_{i+e1} ∈ S, w_{i+2e1} = w_{i+3e1} = 5, apex(i+e1, i+2e1) ∈ B;
  - coefficient −1;
  - exact, so no second-ring family is needed.
- Payee row (d = 7 centre, payer at link 7 j, k = j+e1):
  - exact conditions: w_{j-e1} ∈ B, w_k ∈ S, apex(j,k) = 5;
  - possible-credit conditions:
    - S.L-3: letter 5 is in `L3T & ~extra7`;
    - S.A-1 ∈ B: the exact apex(k, k+e1) when c- = 5, or `amask & ~extra6` when c- = 6;
  - coefficient +1.
- WIN gets `+K1·KUB`. KUB is the slot in the window centred at c-, with L3T OR-ed over w_{j+4e1} and no extras; 13800 + 13800 of the 5^9 windows are set.
- jsepf leaf terms:
  - the exact payer term, −K1 per firing;
  - `K1·(exact − KUB) ≤ 0`;
  - a negative amount is refused (exit 87);
  - exact > KUB is refused (exit 81).
- Mode-2 leaf ids 1800000001 and 1800000002.

**Generic EDGE (`eng/edgefam.py`, jsepf argv[14], `edgekeys=<file>`).**
- File format: one line per key, `NAME EDGE(7->P)[POS=SYM ...]`.
- Payer degree is exactly 7. P ⊆ B selects the payee row degrees.
- Allowed positions: S.L±1..3, S.A±1 and R.L±2, which are exactly the exact letters of the payer's 2-ball.
- Payer row: an exact count with coefficient −1.
- Payee row: credit +1 if every condition is possible. The positions resolve as:
  - S.L±1 and R.L±2: link letters;
  - S.L±2: apexes;
  - S.L±3: u's private, via L3T & m at U = 7 when it applies, otherwise free;
  - S.A±1: when w_k = 5, the exact far apex; when w_k = 6, `amask_U & m`; when w_k ≥ 7, free.
- The payee credit is evaluated as the window bound centred at the payer: letters outside the window are OR-ed out per condition and the extras are dropped. The Python coefficient is this bound.
- The mode-2 class table gets a fold of the bound signature (14 signatures).
- The amount column is `('ks', NAME)`, sharing K\*'s hooks and cap. upperR2 refuses unknown names, negative values and values out of range.
- C++ leaf id 1800000100 + key.

**Sources (md5).**

| file | md5 |
|---|---|
| kstar.py | a28b00b8 |
| edgefam.py | f1b3afea |
| jsepf.cpp (K\* + EDGE) | b1256af5 |
| bin/jsepf | fe70bfc0 |
| K\*-only source / binary | jsepf_kstar_only.cpp cc28e242 / bin/jsepf_kstar_only 670ee08e |

The nc base is s75 jsepf.cpp bd45945d (bin fbe2ad73). The diff is `eng/kstar_jsepf_vs_nc.patch`, which covers K\* only; the EDGE block is described in the jsepf.cpp header.

## 2. Reading of the grammar, and why

The orientation comes from W6's code (tests/w6/grammar.py 9f0783eb and gext.py f2618fb8, both copied unchanged), not from the prose. Test 0 builds W6's own `certpics.recv_pic`-style picture of each arrangement:
- link and apexes exact;
- 6-privates `amask & ~extra6`;
- 7-privates `L3T & ~extra7` at d = 7, and free at d = 8.

It then compares the engine with grammar.py's columns.

| test | stack | arrangements (half planted) | result |
|---|---|---|---|
| K\*: engine K1 vs grammar K\* | s75 | 20000 | **0** mismatches; mirror 0; mis-oriented S.A+1 control 2525 (must be > 0). PASS |
| K\*: same | s77 | 6000 | 0 / 0 / 774. PASS |
| EDGE: payer = grammar SURE count | s75 | 6000 (d = 7 and d = 8) | equal on every row for A1, C1, E1 and KG (= K\* as a generic key) |
| EDGE: payee bound ≥ grammar POSSIBLE count | s75 | 6000 | ≥ on every row; equal on 5965 (A1), 5964 (C1), 5888 (E1), 5694 (KG) of 6000 at d = 7; equal on 5936 (A1) and 6000 (E1) at d = 8 |
| EDGE: mirror key and mis-oriented control | s75 | 6000 | mirror identical; control differs wherever the key has slots. PASS |
| EDGE: same checks | s77 | 3000 | PASS |
| KG vs the K\* family | s75 | 6000 | payer identical; generic payee ≥ exact K\* payee, equal on 5694/6000 |

My only free choice is that a 9+ letter counts as B.

## 3. Acceptance tests

Logs: `logs/upper_<tag>.log`, one line per run in `run.log`, and `logs/seq*.out`.

| # | test | result |
|---|---|---|
| 1 | K\* off, in09 (s75) | **FEASIBLE 0.033528013422**, the nc reference |
| 1 | K\* off, in10 (s75) | **FEASIBLE 0.033088194780**, the s75 log value |
| 1 | K\* off, eval self-test, in09 | PASS: max \|py − C++\| 5e-13 / 4.99e-13 / 5e-13 at d = 7 / 8 / 9 |
| 1 | EDGE binary, families off, b77F_in02 (s77 patched) | **FEASIBLE 0.029906108105**, the coordinator's reference |
| 2 | K\* on at 0: in09 / in10 | FEASIBLE 0.033528013422 / 0.033088194780 |
| 2 | K\* + EDGE on at 0, b77F_in02 (s77) | **FEASIBLE 0.029906108105** |
| 2 | K start points, K\* on at 0: s75 in14 / in15 / b77F_in01 (s77) | FEASIBLE 0.031634694934 / 0.031374540966 / 0.031541705178, all equal to their references |
| 2 | K start point s75 in16, K\* + EDGE on at 0 | **FEASIBLE 0.031151161091** (reference 0.031151161091) |
| 3 | K\* exactness: in10, K1 0.125, `ksforce` (1144 of 3000 d = 7 rows have a nonzero K1, range −2..2) | PASS: 4.99e-13 / 5e-13 / 5e-13 at d = 7 / 8 / 9 |
| 3 | EDGE exactness: in02 with A1 0.1, C1 0.07, E1 0.05, `egforce`, 3000 arrangements per d (nonzero coefficients at d = 7: A1 570, C1 373, E1 855; at d = 8 and 9: A1 450, E1 714–726) | PASS: 5e-13 at d = 7, 8, 9 |
| 3b | K\* window bound (`kub_gap.py`, 20000 arrangements) | exact ≤ KUB on every slot; 89.7 % of bound slots are tight |
| 3c | Controls `ksplant` and `egplant` (Python and C++ deliberately disagree) | self-test FAIL as required: diff 0.25 = 2·K1, and 0.2 = 2·A1 |
| 3d | Control `ksnowin` (no window bound) | jsepf refuses, exit 81, as required |
| 4 | K\* symmetry, d = 7, sym on/off, threshold −0.0005, on the K\*-firing tables of test 5 | **PASS**: 78855 rotation classes identical (sym 87262 rows, nosym 551985 rows, complete), totals equal per class |
| 4 | EDGE symmetry, same method, on the A1-firing tables of test 5 (edge payer leaf firing: 3499 sym, 22750 nosym) | **PASS**: 142429 rotation classes identical (sym 157670 rows, nosym 997003 rows, complete), totals equal per class |
| 5 | K\* planted: in09 + K1 0.125 | **INFEASIBLE** (≥ 200 rows, all at d = 7) |
| 5 | EDGE planted: in02 + A1 0.125 | **INFEASIBLE** (801 rows: 200 each at d = 7, 8, 9, 10, plus 1 at d = 11) |
| 6 | Pointer LPs | see below |

**Test 5 details.**
- K\*: every named row is a **payee** row, with K1 coefficient +1 (26 rows) or +2 (174 rows), and every one is ≤ 1 + t at K1 = 0. Example: `R 7 9567776 5555555`, value 1.083881 (excess 0.050353), credited by the payers at link positions 3 and 5, value 0.833881 at K1 = 0. File: `logs/t5_named.txt`.
- EDGE: every named row is an A1 payee row (A1 coefficient > 0), and every one is ≤ d − 6 + t at A1 = 0. File: `logs/e5_named.txt`. Examples:
  - `R 7 9565767 5556755`: +1 from the payer at j = 6, value 1.066719, which is 0.941719 at 0;
  - `R 10 8575757575 5555555555`: +8, credited twice each by the 7s at 2, 4, 6 and 8, value 4.050957, which is 3.050957 at 0. This shows the d ≥ 10 separators and W9 carry the bound.
- A payer's outflow can never violate its own row, so an overpayment always shows up at the payees.

**Test 6: pointer LPs.** These are nosep LPs (runL style) over a fixed receiver set, with every sender row, the conservation basis and the mrows. "Floor" means the 3 floor-cert d = 8 receivers, which give t ≥ 0. Amounts at cap 3 are degenerate (rc 0) once the floor is reached.

| row set | stack / families | off | K\* | A1 + C1 + E1 | K\* + A1 + C1 + E1 |
|---|---|---|---|---|---|
| W6 pool: 297 W6 dual-support receivers + floor | s77 / rrz (no q7) | **0.006468** | cap 0.125: 0; cap 0.0625: 0.000796 | cap 0.125: 0 (A1 0.125) | cap 3: 0 |
| same | s77 / full (engine q7) | 0 (floor) | 0 | | |
| q75B K-run rows (3832) + W6 pool | s75 / full | 0 | 0 | | |
| s77 L b77U6 dual support: 293 receivers + floor (b77U6 t* 0.026384) | s75 / base | **0.026384** | cap 0.0625: 0.021469; cap 0.125: **0.016626**; cap 3: 0 | cap 0.125: **0.013354** (A1 0.125 rc −0.061, E1 0.120, C1 0 rc +0.005); cap 3: 0 | cap 0.125: **0.002053** (A1, E1, K1 at cap; rc −0.071 / −0.026 / −0.085; C1 0) |
| same | s75 / full | 0 | 0 | | |

**Reading.**
- Direction and size match W6.
- C1 stays at 0 in every LP here. C1's target row C (5757575/7755777) is not tight in these sets.
- Whether the new keys help on top of the full q7 key set can only show in the K solve.

## 4. K solve: prepared, NOT launched (the coordinator decides)

The command is one line per stack. Settings: 1 thread, nice 15; FAM=full (q7 q7m q7rc q7cap=3, the full q7 key set); K\* on and EDGE keys A1, C1 and E1 on, every amount in [0, 3]; keeppen with xpen 1e-3 and q7pen 1e-3; in-out exactly as q75B/b77F. Each line includes its in-point watcher, which runs upperR2 with the same STACK/FAM/KS/EGK. To drop a key, point EGK at a file without it; to run K\* alone, drop `EGK=…`.

**k78A, unpatched** (s75 tab, kill6 U7 c0527d29). Start: s75 `cand/sol_q75B_in16_full.json` (md5 3d86009c), nc FEASIBLE 0.031151161091; with K\* + EDGE on at 0: FEASIBLE 0.031151161091.

```
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; cd $N && . ./env78.sh && STACK=s75 FAM=full KS=1 EGK=$N/eng/edgekeys_r4.txt WARM=$W7POOL,$WX75,$WK75,$N/warm/rows_q75B_snap78.txt,$N/warm/rows_b77F_snap78.txt,$N/tests/t6/pool_W6support_floor.txt,$N/tests/t6/pool_b77U6dual_floor.txt FEAS=$N75/cand/sol_q75B_in16_full.json nohup bash runK78.sh 200 1 k78A inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > logs/runK_k78A.out 2>&1 & (sleep 20; cd $N; STACK=s75 FAM=full KS=1 EGK=$N/eng/edgekeys_r4.txt nohup bash watch78.sh k78A > logs/watch_k78A.out 2>&1 &)
```

**k78B, B1-patched** (s77 tab, kill6 U7 b493a0ce). Start: s77 `cand/sol_b77F_in02.json` (md5 6839528d), nc FEASIBLE 0.029906108105; with K\* + EDGE on at 0: FEASIBLE 0.029906108105 (test 2).

```
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; cd $N && . ./env78.sh && STACK=s77 FAM=full KS=1 EGK=$N/eng/edgekeys_r4.txt WARM=$W7POOL,$WX75,$WK75,$N/warm/rows_q75B_snap78.txt,$N/warm/rows_b77F_snap78.txt,$N/tests/t6/pool_W6support_floor.txt,$N/tests/t6/pool_b77U6dual_floor.txt FEAS=$N77/cand/sol_b77F_in02.json nohup bash runK78.sh 200 1 k78B inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > logs/runK_k78B.out 2>&1 & (sleep 20; cd $N; STACK=s77 FAM=full KS=1 EGK=$N/eng/edgekeys_r4.txt nohup bash watch78.sh k78B > logs/watch_k78B.out 2>&1 &)
```

**Warm rows.**
- W7POOL, WX75 and WK75: the same set b77F used.
- `warm/rows_q75B_snap78.txt`: 3832 rows, a superset of b77F's snap3.
- `warm/rows_b77F_snap78.txt`: 96 rows.
- The two test-6 pools.

**Expected cost:** about 273k rows, so roughly 30 to 50 min per LP at 1 thread, as with b77F.

**Where to look:**
- per-iteration amounts and reduced costs: `grep 'kstar it' runK_k78X/K.log`;
- checkpoints: `eng/rows_k78X.txt` and `eng/sol_k78X_{lp,inNN}.json`, which the watcher copies to cand/ and checks.

## 5. Things that looked wrong (grammar or engine)

1. **s75 `run_sep` throws away jsepf's stderr**, so the clamp, nc-slack and K\* counters were never visible. My copy logs the summary lines, and on a failure it logs the exit code and message.
2. **The nc binary still labels its counters "clamped N"** (header comment and the "f2b/q7m leaf hits …, clamped N" lines). In nc, N is the number of positive corrections that were **kept**, the same number as on the "kept (not clamped)" line. This is cosmetic but easy to misread.
3. **The mode-2 class lacks p and s** for c = 0 windows (a, b, e, f, q, r) and for c ≥ 2 windows. Any WIN term that reads them makes rows within one class differ. K\* handles this with leaf ids; EDGE folds its bound signature into the class table. Every new family needs one of the two.
4. **The s75 engine changed after my copy.** `prelay2.py` changed at 18:09Z: Team C's lowerR2 `capof` now prices q at q7cap. I ported it; the note is in `eng/SOURCE_MD5_s75teamA.txt`.
5. **My own slip:** I removed jsep2..jsep7 (the d ≥ 10 separators) from `eng/bin` while cleaning. The first in09 run crashed at d = 10, loudly. I restored md5-identical copies and the rerun was FEASIBLE 0.033528013422.
6. **Grammar.** There is no disagreement with grammar.py on K\*, A1, C1, E1 or KG. Two points for the record:
   - "Overpaying" is only detectable at the payees.
   - W6's pool gains are real in the rrz and base models, but the full-q7 engine already sits at the floor on those small sets.
   - The generic payee is a window bound. It is slightly looser than exact; for A1, C1 and E1 the grammar's exact credit is equal on 98–99.6 % of rows.
   - Keys that need positions outside the payer's 2-ball are refused, because they would need separated payer rows: R.L±3, R.A±1 and S.A±2.
7. **Possible speed-up, not done.** The K\* payer term and the window-local EDGE payer terms (A1 and C1; E1 spans 6 links) could go into WIN as exact negative terms. That would tighten pruning when the amounts are positive.
