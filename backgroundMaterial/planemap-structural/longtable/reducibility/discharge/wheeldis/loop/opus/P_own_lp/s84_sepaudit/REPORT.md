# s84_sepaudit: does our jsepf have the Studio pre-check bug? No.

(Audit agent report, 6 Nov 2026 ~00:55Z; saved by the Opus team thread because the harness refuses subagent report files.)

B = `/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp`.

Labels: **[read]** is from code reading; **[run]** is from a command run here, single-threaded at nice 15.

Line numbers refer to `s78_kstar/eng/jsepf.cpp` (b1256af5); s77 lines refer to `s77_k6patch/eng/jsepf.cpp` (bd45945d).

## Verdict
- **(a) PASS.** Every leaf term is either folded into WIN or <= 0, except the f2b/q7m deltas, which the nc slack covers. The bound counts every window once, and the window resolved at a step is added before that step's test.
- **(b) PASS.** The nc slack covers every positive delta still to come, and nothing is clamped.
- **(c) PASS, with one gap.** All sign invariants hold, but bonus >= 0 is not checked in C++, and upperR2 does not refuse q < 0.
- **(d) PASS.** Loosened and normal violator sets are identical, and an exhaustive run with no bound pruning gives the same set.
- **(e) PASS.**
- **Nothing found can make a FEASIBLE verdict wrong through pruning.**

## 0. Code identity and setup [run]

**Rebuilds.**
- `c++ -O2 -std=c++17 -pthread -o bin/jsepf jsepf.cpp` on s78 b1256af5 gives **fe70bfc0**, and on s77 bd45945d gives **fbe2ad73** (`src/rebuild/`, `src/rebuild77/`).
- `s78_kstar/eng/jsepf_nc_base.cpp` has the same md5 as s77's jsepf.cpp.
- The diff from nc base to s78 contains only added lines: the K* block L268-305, the EDGE block L306-323, and their loaders. So `rec()` and every other leaf block are identical in s77 and s78.

**Engine copy (`eng/`).**
- The `.py` files and `bin/jsep2..7` are md5-identical to s78's (`logs/src_md5_s78.txt`).
- `bin/jsepf` is the audit build of `src/jsepf_audit.cpp` (bin d9ce7c99); the full patch is `src/audit_vs_s78.diff`.

**Audit knobs** (environment variables):
- `SEPA_LOOSEN=L`: adds +L to the bound in rec and to every early exit in the leaf. Rows are still reported only above the TRUE cut, through an extra final test.
- `SEPA_BREAK=1`: control only. The bound at slot 2k omits window k-2, which is the Studio pattern.
- Counters: `shadowBr` / `shadowNodes` (branches and nodes visited only because of L); `rowsShadow` / `rowsLeafShadow` (reported rows the unloosened search would have cut); `bndViol` (leaves whose window sum exceeds the smallest bound on their path by more than 1e-9, checked at every leaf before any early exit).
- Later builds: v2 adds `SEPA_LEAFLOOSEN`; v3 flushes rows and prints counters as it goes; v4 adds `SEPA_TASKFROM` to resume after a kill. Diffs are `src/audit_v*_vs_*.diff`.

**The query.**
- `upper84.sh` runs upperR2 with `dmax=7 dtail=7` on `s78_kstar/cand/sol_k79K_in03.json` (b988f6cf, t = 0.025387578325). Settings: STACK=s77, FAM=full, KS=1, EGK=`s78_kstar/eng/edgekeys_r4.txt`, ARGS=`s79_routeF/args_A97_F.txt`. It keeps the work directory `work/in03/`.
- The log matches the certifying `s78_kstar/logs/upper_sol_k79K_in03.log` through d = 7: the same patterns and amounts; `d=7: 0 violated`; q7m hits 7327; K* 2487 / 0 / 1028; f2b hits 1,596,749, of which 183 are positive.
- Its final "INFEASIBLE (1)" line is an artefact of dtail=7 (the Karp d0 test) and is not a verdict.
- The driver argv is in `logs/argv_in03.txt`. `runq.sh` replays it on any binary or header.

## 1. (a) Leaf terms [read, run]

| line | term | sign / where it lives | next test |
|---|---|---|---|
| L165 | sum win(i), all d windows | WIN: x, rr/zh/zr, Q, l3q upper bound, K* +aK*KUB (`kstar.py`), EDGE payee bound (`edgefam.py`) | L167 c-SLACK |
| L168 | RBIG | row excluded | - |
| L170 | -bonus | <= 0 only because `prelay2.py:250` writes `v > 0`. [run] min 1.62e-4 over 136 links | c-SLACK |
| L171-186 | QX - PQ | <= 0. L459 / L460 refuse values above 1e-15 or below -1e-15 (exit 5 / 6) | c-SLACK |
| L187-209 | -PQ8 / QX8 | <= 0 (L472 / L473, exit 12 / 13) | c-SLACK |
| L210-244 | f2b V6M and QMT deltas | signed: see (b) | L243 c-SLACKT |
| L245-267 | q7m QTM delta | <= 0 in practice: QT is a max over sub-masks (`f2bglue.py q7m_write`) | L266 c |
| L268-305 | K*: -aK per payer; aK*(exact - KUB) | <= 0. aK >= 0 (L514, exit 87); KUB in {0,1} (L515, exit 88); exact <= KUB (L299, exit 81) | L304 c |
| L306-323 | EDGE: -amount per payer | <= 0. amount >= 0 (L525, exit 94); payee credit is in WIN | L322 c |
| L325-339 | FY2 | off here; any correction above 1e-12 exits 9 | L338 c |

**The bound** is at L382-394 (s77 L310-322). At even slot 2k, 2 <= k <= d-1: bnd = V[d-k+2][A_{k-1}] + h1 + exactsum, where V covers windows k-1..d-1 and 0 by a max-plus DP over H = max over (w_{i-2}, s_{i-2}) of WIN (L443-449, computeV L144-162), h1 covers window 1 (L385), and exactsum covers windows 2..k-2 (window k-2 is added at L384, before the test at L392). Each window is counted exactly once. Branches are pruned iff `bnd + SLACK <= cut - 1e-12`. There is no "remaining x max" term, so the Studio `(d - NRES[i+1])*XINMAX` pattern has no analogue. jsep3 (d >= 10, `$B/jsep3.cpp` L156-170) has the same structure with no leaf terms.

**[run] `bndViol`:**

| run | leaves | bndViol | largest gap |
|---|---|---|---|
| in03, L = 0 | 8,282,062 | 0 | 4.4e-16 |
| in03, L = 0.05 | 12,444,923 | 0 | 4.4e-16 |
| pc010, L = 0.05 | 13,476,638 | 0 | 4.4e-16 |
| pc010, exhaustive | 281,520,978 + 613,679,062 | 0 | 4.4e-16 |
| control, `SEPA_BREAK=1` | - | **552,530** | 0.467 |

## 2. (b) nc slack [read, run]

**Definition (L497-505).** dV, dQ, dT are the largest positive deltas over all table entries and all sub-masks (the form `m & ~ex` the leaf uses). SLACKT = d*dT (+1e-12); SLACK = d*dV + 2d*dQ + SLACKT (+1e-12). Each position gives at most one V6M term or at most two QMT terms (branches at L214 / L225), and q7m at most one term per link 7.

| test | slack used | positive terms still to come |
|---|---|---|
| rec L392 and leaf L167, L170, L185, L208 | SLACK | f2b + q7m |
| L243 | SLACKT | q7m |
| from L266 on | plain cut | only <= 0 terms |

**Nothing is clamped.** Each v is always added (L222-224, L237-239, L262-264); the "clamped N" counter counts deltas that were kept.

**[run]** `check_c.py` recomputes from `work/in03/f2b_d7.bin` and `q7m_d7.bin` (`logs/check_c_in03.txt`): dV = 0, dQ = 0.000857923571 (one QMT entry: c = 6, apex = 5, mask 30 -> 28), dT = 0, so SLACK = 0.01201093 and SLACKT = 0, as in the C++. Positive terms observed: 183 (in03), 350 (in03, L = 0.05), 394 (pc010, L = 0.05), 210 (exhaustive, tasks 301 on); each 0.000857923571, never more than one per leaf. q7m positives 0; `posOver` = `posOverT` = 0. Certifying logs `s78_kstar/logs/upper_sol_k79K_in01/02/03.log`: positives only at d = 7, from QM (in01 dQ 1.06e-3, 131 kept; in02 9.53e-4, 161; in03 8.58e-4, 183); at d = 8, 9 slack 0 and 0 positives.

## 3. (c) Sign invariants [read, run]

- Enforced in C++: at load L459, L460, L472, L473, L514, L515, L525; at the leaf L299 and L337.
- **Not checked in C++:** bonus >= 0 (L475). A one-line refusal is recommended.
- **Not refused by upperR2:** q < 0. A negative q would make some link's true bonus negative; `write_bonus` would drop it and the leaf would under-count. In in03, q min = 1.42e-5.
- [run] in03 files: l3q / l3q8 QX max 0, PQ min 0; bonus min 1.62e-4; kstar_d7.bin aK = 0.0174951, KUB in {0,1} (13800 + 13800 ones); edge amounts (0, 0.0009996, 0); WIN no NaN or +inf.

## 4. (d) Loosened pruning and positive control [run]

Query `work/in03`, d = 7, thr = 1.025387579325154, mode 0. Positive control `hdr/in03_pc010.txt`: same query with line 1 changed to thr - 0.01 and K = 1e9. Outputs in `runs/`, `run.log`; comparisons in `logs/cmp_pc010.txt`, `logs/cmp_norec_full.txt`, `logs/cmp_pc010_sym_nosym.txt`.

| run | binary | rows | nodes | extra nodes (branches) | rows only because loosened | wall |
|---|---|---|---|---|---|---|
| in03, normal | original fe70bfc0 | 0 | 38,282,818 | - | - | 82 s |
| in03, normal | audit, L = 0 | 0 (stdout byte-identical) | 38,282,818 | 0 | 0 | 80 s |
| in03, loosened | audit, L = 0.05 | **0** | **48,990,552** | 10,707,734 (1,132,316) | **0 / 0** | 122 s |
| pc010, normal | original | **3706** | **40,223,904** | - | - | 90 s |
| pc010, normal | audit, L = 0 | 3706, identical | 40,223,904 | 0 | 0 | 85 s |
| pc010, loosened | audit, L = 0.05 | **3706, identical row by row and in order** | **51,465,477** | 11,241,573 (1,205,553) | **0 / 0** | 126 s |
| pc010, exhaustive | v3 tasks 1..300 + v4 tasks 301..end; rec pruning off, leaf tests at the true cut | **3706, identical row by row and in order** | 378,828,865 + 813,906,790 | - | 0 / 0 | 1213 s + 2431 s |
| pc010, control | audit, `SEPA_BREAK=1` | **1336 (2370 lost)** | 19,487,942 | - | - | 26 s |

- Node accounting is exact: 48,990,552 - 10,707,734 = 38,282,818 and 51,465,477 - 11,241,573 = 40,223,904.
- The only differences between the pc010 outputs are the node counts on the END line.
- The exhaustive run was killed by the container restart after task 300 (1430 rows, equal to the first 1430 normal rows) and resumed with `SEPA_TASKFROM=300`; the resume was validated first (normal pruning, tasks 301 on: 2276 rows = normal rows 1431..3706).
- d = 7 margin: original binary mode 1 gives MAX 1.025387516715 (link 9775566, apexes 5565676), 6.16e-8 below d - 6 + t. Every row above thr - 0.01 lies at or below this value, so in03's d = 7 FEASIBLE verdict holds with no bound pruning at all.

## 5. (e) Rotation invariance [read, run; K*/EDGE: Team D]

Symmetry break L369-373 (s77 L297-301): keeps every rotation with P_0 >= P_i; `break` valid because letters are tried in ascending order; reflection not broken. Patterns are expanded over all 2d rotations and reflections (`pcheck.py` L199-215). V does not use the symmetry break. Every leaf term is a sum over positions i of letters at fixed offsets from i (win, l3q, l3qV, q7m, K*, EDGE relative to i; f2b `f2bExtra(bk, i)` offsets 0..d-1 from i, matching `f2bglue.py f2b_buckets` `o % d`; bonus and RBIG use canonlink(); mode-2 ids sorted), so the leaf total is rotation-invariant.

[run] pc010 with the symmetry break off (argv[4] = 0, original binary): 24,367 rows, 419,677,295 nodes, the same 3481 rotation classes as sym on (3706 rows) with equal loads; 24,367 = 7 x 3481. Team D's test 4 passes for both families: `s78_kstar/logs/symchk_kstar_t5/cmp_result.txt` (78,855 classes), `s78_kstar/logs/symchk_edge_e5/cmp_result.txt` (142,429 classes).

## 6. Every prune test (s78 line / s77 line)

| s78 | s77 | test | verdict |
|---|---|---|---|
| L372-373 | 300-301 | symmetry break | exact |
| L375 | 303 | `patok` | row semantics, not a bound |
| L378 | 306 | A_1 claim | work split only (1 thread: every A_1 visited) |
| L384, 385, 389 | 312, 313, 317 | -inf feasibility | exact |
| **L392** | **320** | the bound | **sound, no off-by-one** |
| L165, 167, 170, 185, 208 | 149, 151, 154, 169, 192 | leaf early exits at c - SLACK | sound |
| L243 | 227 | leaf early exit at c - SLACKT | sound |
| L266, 304, 322, 338 | 250, -, -, 266 | leaf early exits at the cut | exact |
| L353 | 281 | mode-2 re-test | exact |

Structural note: our search keeps one representative per rotation class, where Studio searched all 125 start states, so one wrong cut here would lose the class outright. The run checks in sections 1 and 4 show no wrong cut happens on this query.

## 7. Residual risks (not pruning)
- The row definition itself (Python `recv_coef_R2` against WIN plus leaf) rests on Team D's eval self-tests (<= 5e-13), not redone here.
- The two unguarded signs from section 3 (bonus in C++, q in upperR2).
- d >= 8 was not rerun. jsep3 (md5 13b99293) could not be reproduced from `$B/jsep3.cpp` (8aa4cae6) under four flag sets. By reading, it has the same bound and no leaf terms.

## Files
`upper84.sh`, `runq.sh` (run scripts); `check_c.py` (sign and slack check); `cmp_rows.py`; `src/` (audit sources v1-v4, diffs, rebuild folders); `eng/` (engine copy); `work/in03/` (query files); `hdr/` (edited headers); `runs/` (jsepf outputs); `logs/`; `run.log`.

## Deviations
- A read-only `grep -r` over `/mnt/project-files/swarm` ran under 2 minutes before it was stopped.
- A stray scratchpad copy of jsepf.cpp was made and deleted.
- Two of the agent's own runs were stopped to restart with better logging (`runs/*aborted*`).
- The ~00:00Z container restart killed the exhaustive run; it was resumed from task 301.
- No other process was touched, and nothing outside `s84_sepaudit/` under $B was written.
