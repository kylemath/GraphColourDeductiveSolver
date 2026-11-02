# Two-engine reducibility audit of the Tier A forbidden set (31 Oct 2026)

## Verdict
- [M] Tier A as rebuilt from origin/main = 13,256 configurations (RSST 582 + k3x 4,464 + k3p 10 + nl51 8,200), 0 duplicate names. The outside team's 13,199 is 57 fewer because their k3x count is 4,407.
- [M] Record check: 13,246 of 13,256 have a verdict in the repo on BOTH engines (kc and dfast/cfast), and for C names the same X on both. The 10 k3p configurations are the exception: only a one-line "(two engines; from ...)" claim, no per-engine output.
- [M] Re-run on this container (kc and cfast from the repo sources, g++ -O2): the A100-only extras (421 D + 125 C) and k3p (10) all pass on BOTH engines. Zero failures anywhere. [P] Nothing else was re-run on both engines, because of the budget.
- No failing configuration was found, so no kill-table cell depends on a non-reducible configuration. The KT-table recomputation was not needed.

## Counts by source and status (records_table.csv, rerun_table.csv)
| source | kind | n | repo records, both engines | re-run kc | re-run cfast |
|---|---|---|---|---|---|
| rsst D2 | D | 249 | 249 (M: loop/k44) | 249 D | 0 |
| rsst C2cons | C | 333 | 333, same X | 333 C0 | 0 |
| k3x A83 | D | 2704 | 2704 | 2470 D | 0 |
| k3x A83 | C | 1214 | 1214, same X | 1072 C0 | 0 |
| k3x extra (A100 only) | D | 421 | 421 | 421 D | 421 D |
| k3x extra (A100 only) | C | 125 | 125, same X | 125 C0 | 125 C0 |
| k3p | D 4 / C 6 | 10 | 0 (claim only) | 10 pass | 10 pass |
| nl51 | D | 8200 | 8200 (6055 explore kc+dfast in k53 N54_* on the nh6pv2 branch only; 494 both; 1651 Studio in out/job54d, out/job54e on main) | 4294 D | 0 |

C0 = C-REDUCIBLE with leftover 0 under the recorded conservative X (kc -C -x X, adm=yes; cfast --fixed X). For rsst C the X is the verdict X of rsst_verdicts.txt, not RSST's own X.

## Extras (the main doubt)
- All 421 D extras: kc D and cfast D, classes/ext identical on both engines. All 125 C extras: kc -C -x accepts the job30 X (adm=yes, leftover 0) and cfast --fixed X gives leftover 0.
- They are in k3x_D.out/k3x_C.cfast by construction of out/job30/twoeng.py (dfast/cfast and kc must both agree; same X for C). Each has records from both engines in loop/k4x/k5x files on main. They are only missing from the A83 registry because they came in after 240b5a08. Rings: D 12-15 (4/36/163/218), C 11-15 (1/3/20/42/59).
- Engine agreement on all 556 kc/cfast pairs re-run (extras and k3p): classes and ext counts equal, 0 mismatches.

## Gaps and caveats
1. k3p (10): "two engines" is asserted in k3p_D.out/k3p_C.cfast only. Now confirmed by this re-run on both engines.
2. nl51 explore half (6055): its kc and dfast outputs (loop/k53/N54_*.out) exist on origin/claude/project-thread-nh6pv2, not on main. main has only nl54d_verdicts-style summaries, plus the Studio parts (out/job54d, out/job54e). [P] Whether the outside team has them is unknown.
3. Rings 15-18 nl51 (2,305 configs) and the other nl51 ring-14 tail were not re-run here.
4. The engines are only as independent as their two codebases: kc was written without reading dfast/cfast (loop/kc/FINDINGS.md). cfast's X admissibility is local plus Gonthier valid_contract; the global minimal-counterexample conditions are the registry's "C cons." standard, not re-checked. [C]
5. The rsst C re-run initially failed for 12 names because I used RSST's own X (adm=no on kc). With the recorded C2cons X they pass. This was my input error, not a failing configuration.

## Not re-run here: Mac Studio list
mac/remaining_jobs.txt (16,982 jobs over 12,700 configs: cfD 11,153, kcD 4,140, cfC 1,547, kcC 142), mac/configs.in, mac/X.txt, mac_run_queue.py (shardable: args ... k n). Build kc from loop/kc/kc.cpp and cfast from studio15/cfast.cpp with c++ -O2 -std=c++17. Run: `python3 mac_run_queue.py ./kc ./cfast mac/remaining_jobs.txt mac/configs.in mac/X.txt out.tsv K N` for shards K of N. Then run evaluate.py logic on the tsv (D=true, or C-REDUCIBLE with leftover 0). Cost: cfast about 7 s at ring 14, 38 s at ring 15, kc 1 s and 4.5 s. Priority is kc for nl51 rings 15-18 and cfast for rsst/A83.

## Files (all under /tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ext_reduc/)
targets.json (13,256 names, source, kc line), records_table.csv (name, source, tag, kind, ring, engine-1 kc verdict + file, engine-2 verdict + file, conflict, main_both), rerun_table.csv, res/*.tsv (raw re-run outputs), bin/kc, bin/cfast, catalog.py, table.py, evaluate.py, run_queue.py, gen_mac.py, mac/.
