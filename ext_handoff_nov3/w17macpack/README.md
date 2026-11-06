# W17 macpack: the code_gk7 second-engine upper check, for the Mac Studio

Swarm W17 (team U, claim U-1), 6 Nov 2026, round 6.

**What it is.** This is the Studio-side second engine that checks Opus's in-out upper points: GK generic keys plus f2b7.

- It is code_gk7 exactly as it runs in the swarm container, packed with every data file a run reads. The file list comes from an strace of a complete run.
- **The family it checks (the default):**
  - the W13 stack, with W13's 27 D and 88 C kill patterns;
  - full q7 + c6le + gkwin gkleaf;
  - F2B7, with the proof stack's rule file **rules_zcons_minus_W18rejects** (`tab/rules_zcons_minus_W18rejects.json`, 2b362955, 6,016 rules, from round6/W18-rule-audit/rules/).
    - It is the Studio's DERIVE Z-consistency fix rules_zcons (e6c496a1, 6,290 rules, Studio main a7fbd198) minus 274 rules.
    - W18's strict audit rejected those 274 because they only embed under a face-set reading at cut or pendant vertices.
  - 151 keys (cg_keys_r13.txt, fe8a97a7, Opus's bytes).
- **Rule files.** In every group and side: default ⊂ zcons ⊂ f7s (704c371f) ⊂ 45a4c6d1. This was checked here.
  - zcons drops 3,036 of 45a4c6d1's 9,326 rules, 1,716 of them w6 rules.
  - The default drops 274 more.
  - The three older files are in the pack for comparison only. `F2BRULES=` overrides the rule file in every script.
- **The target point is a parameter:** `bash check.sh /path/to/point.json 8`. Run the point Opus names FEASIBLE on the corrected rules + W13 + 151 keys.
- **First job:** `sol/sol_q53A97q.json` (06767b0b, t = 0.098789365409), from from_opus/s86_k86RS. Opus: UPPER-R2 FEASIBLE on exactly this family (`ref/s86_k86RS/upper_R_q53A97q.log`). It is the f2b-free s53 A97 point with the q7 / q7m flags set and q empty.
- **Later points.** New k86RS points (`sol_k86RS_inNN.json`) land in from_opus/s86_k86RS/ with a POINTS.txt line. Copy each into `sol/` and run it the same way.
  - k86B in11 (2db802ad) and in10 (65418d1e) are in `sol/` for the smoke test and for timing. They were made and checked on the unsound f7s family, so they are not targets.

**Testing.** The bundle was tested here before shipping. It was unpacked into a scratch directory, compiled with clang++, and the smoke test was run under Python 3.9.25 with numpy 2.0.2 and scipy 1.13.1, the Mac's versions. See section 9.

## 1. Unpack (keep /tmp/swarm-W17)

    cd /tmp && tar xzf w17_macpack.tar.gz          # creates /tmp/swarm-W17/...
    cd /tmp/swarm-W17 && while read h f; do [ "$(md5 -q "$f")" = "$h" ] || echo "BAD $f"; done < MANIFEST.md5   # optional: no output = every file intact

- **Path.** Every path is the literal `/tmp/swarm-W17`. To unpack anywhere else, run `bash relocate.sh /new/root/swarm-W17` first; it rewrites the path in every text file.
- **Older pack.** If you already have a /tmp/swarm-W17 from an older pack, move it aside first.
- **Layout:**
  - `code_gk7/`: the checker. Python rows plus the separator source `sep3r_gk.cpp`.
  - `wd/`: the Studio builder (`wlp.py`, `wlp3.py`, `wlp3r6.py`), the Studio separator sources (`sep3.cpp`, `sep3r.cpp`, `sep3r_ak.cpp`) and `bin/`, which stays empty until build.sh runs. It also holds the files the check needs from the Studio repo's `out/` and `loop/`. Here those two are real folders; in the container they are links into the repo.
  - `pat/`: the A97 + F pattern files (`A97`, and the exname-filtered `A97x`). `pat/W13/` holds Opus's W13 files, md5-checked against Opus's MD5SUMS.
  - `args_A97F_W13_x_studio.txt`: the pattern args for the W13 family. md5 bfca4bc4, from W17b (U-3), giving EXPECT_PAT 18128,686,158. It is `args_A97F_x_studio.txt` (exname-filtered, 18101,598,158) plus the 4 W13 files. The exname filter drops 0 W13 blocks.
  - `kill/patched298/`: the kill stack.
  - `tab/`:
    - key files: `cg_keys_r13.txt` (151 keys, fe8a97a7, the default) and `cg_keys_r12.txt` (140 keys, bb547900);
    - `exname_keep95p131f.txt`;
    - `rules_zcons_minus_W18rejects.json` (2b362955), the default rule file;
    - `rules_zcons.json` (e6c496a1), the Studio's zcons file, for comparison. `zcons/` holds the Studio's MD5SUMS, compare.txt, cmd.txt, run log and provenance summary for it.
    - `rules_studio_keep95p131f_f7s.json` (704c371f): Opus's f7s filter of 45a4c6d1. It holds unsound rules and is kept for comparison only.
    - `f2b7/`: Opus's SPEC, REVIEW and MD5SUMS.
  - `ext/k95f/tab/`: the unfiltered rule file 45a4c6d1. It holds unsound rules, is kept for comparison only, and is never used by default.
  - `sol/`:
    - `sol_q53A97q.json` (06767b0b), the first target;
    - k86B in11 (2db802ad) and in10 (65418d1e), from from_opus/s86_k86S. They are smoke and timing points, not targets.

    Copy each new target point here.
  - `ref/s86_k86RS/`: Opus's README, MD5SUMS, the upper log of q53A97q on this family, and its f2b self-test on 2b362955.
  - `ref/s86_k86S/`: the same for in10 and in11 (f7s family), for comparison.
  - `macshim/`: `md5sum` and `timeout` stand-ins for macOS. The scripts put this folder on PATH themselves.

## 2. Compile (about 30 s)

    bash /tmp/swarm-W17/build.sh

This runs `clang++ -std=c++17 -O3` on four sources:

- `wd/sep3.cpp`, also copied as `sep3f`;
- `wd/sep3r.cpp`;
- `wd/sep3r_ak.cpp`;
- `code_gk7/sep3r_gk.cpp`, built as `wd/bin/sep3r_gk7`.

Notes:

- Only the standard library is needed: no OpenMP, no Boost, no `bits/stdc++.h`.
- Set `CXX=...` to use another compiler, or `CXXFLAGS=...` for other flags.
- The parallelism is multiprocess: one separator process per part, NPROC at a time.

## 3. Python

The scripts use `python3`, which is /usr/bin/python3 3.9.6 on the Mac.

**Modules needed:**

- **numpy:** used throughout.
- **scipy:** only imported, as `scipy.optimize.linprog` and `scipy.sparse`, by the Studio builder `wd/wlp3r6.py`, part of which is executed.
- Everything else is the standard library.

Nothing comes from outside the bundle: no `wd/` modules beyond those listed, and no site-packages other than numpy and scipy.

The code has no Python 3.10+ syntax. It was parsed with `feature_version=(3, 9)`, and the smoke test ran under CPython 3.9.25.

## 4. Smoke test (about 3-4 min)

    bash /tmp/swarm-W17/smoke.sh

Both runs use in11 on the default family (W13 args, rules_zcons_minus_W18rejects, 151 keys). The smoke test checks the pipeline and its controls, and makes no claim about in11 itself.

1. **PASS run.** The point goes through the whole pipeline on d = 24..26 only:
   - the Python step: senders, cons2, mrowL, the C++ vs Python self-tests (W10, GK, f2b) on random and planted rows, and the DP and Karp tail;
   - three separator parts;
   - the summary.

   It must print `RESULT: PARTIAL PASS ...`.
2. **Planted control that must FAIL.**
   - Setup: the same point, with q[7665657] raised by 1. That key is kept by the f2b7 7-side mask of the admissible d = 7 row 5776667 / 9567857.
   - The separator search is restricted to that one row.
   - It must report the row above the bound (`F2B7ROWS FAIL ... reported above the bound`).

The script ends with `SMOKE: PASS` when (1) passes and (2) fails as it should. The logs are in `/tmp/swarm-W17/logs/smoke_pass*` and `smoke_ctl.log`. It can be rerun at any time, since each run starts fresh.

## 5. The check, at 8 processes

    bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_q53A97q.json 8      # first job (TAG sol_q53A97q_zW13)
    cp /path/to/sol_k86RS_inNN.json /tmp/swarm-W17/sol/ && bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_k86RS_inNN.json 8   # each later point

The target point is the first argument, either a path to its sol.json or the shorthand `in10` / `in11` for the two points in `sol/`. check.sh runs `code_gk7/w17_upper.sh`, the same command the swarm runs, with two changes: the process cap is lifted from 2 to 16, and the work is split into finer parts. For a point `sol/sol_X.json` (the TAG is `sol_X_zW13`), the command is:

    cd /tmp/swarm-W17 && PATH=/tmp/swarm-W17/macshim:$PATH W17NICE=20 env RESUME=1 C6LE=1 NOCLAMP=1 F2B7=1 \
      F2BRULES=/tmp/swarm-W17/tab/rules_zcons_minus_W18rejects.json GK=/tmp/swarm-W17/tab/cg_keys_r13.txt \
      ARGSF=/tmp/swarm-W17/args_A97F_W13_x_studio.txt EXPECT_PAT=18128,686,158 EXNAME=/tmp/swarm-W17/tab/exname_keep95p131f.txt \
      NPROC=8 NPROCMAX=16 DMAXP=26 DLIST=7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26 PARTS=7:4,8:12,9:24,10:9,11:6,12:3,13:2 \
      bash /tmp/swarm-W17/code_gk7/w17_upper.sh /tmp/swarm-W17/sol/sol_X.json /tmp/swarm-W17/kill/patched298 sol_X_zW13

**Checks that the right family loaded.** These lines in `logs/<TAG>/p0.log` confirm it:

- the header line `rules /tmp/swarm-W17/tab/rules_zcons_minus_W18rejects.json`;
- `F2B rules /tmp/swarm-W17/tab/rules_zcons_minus_W18rejects.json ...: {('w6', 7): 1531, ('w6', 8): 1114, ('w6', 9): 87, ('w7', 7, 1): 928, ('w7', 7, -1): 928, ('w7', 8, 1): 714, ('w7', 8, -1): 714}`. For comparison, zcons gives 1577 / 1248 / 97 / 947 / 737, and f7s gives 2437 / 1738 / 463 / 1356 / 877.
- `W17 GK keys: 151 from .../cg_keys_r13.txt (md5 fe8a97a7)`;
- `patterns distinct by kind: D 18128 ..., C 686 ..., RPAT 158`. The pattern count check refuses any other stack, which is a hard FAIL.

Opus's upper log of the same point should show the same D, C and RPAT counts and the same rule counts. Opus's by-degree pattern counts at d = 7, 8, 9 run 3, 4 and 7 higher than this code's; every stack shows those same offsets.

**Steps of a run.**

1. The Python step, about 1.7 min on one core.
2. The separator jobs: 73 parts over d = 7..26, NPROC at a time, at `nice W17NICE`. check.sh sets 20, so the jobs yield to other work on the Mac.
3. An exact Python re-check of any reported arrangement.
4. `summarize17.py`.

**Result.** The verdict is the `RESULT:` line of `logs/<TAG>/summary.txt`:

- `FEASIBLE`: every sender row, cons2, mrowL, d = 7..26 exhaustive, DP 27..30 and Karp pass;
- `INFEASIBLE`: the exact violators are listed;
- `NOT ESTABLISHED`: something did not finish, or a Python check failed.

**Options:**

- `TAG=...`: another log folder (the default is `<point>_zW13`).
- `DLIST=7,8 TAG=<point>_zW13_d78`: only the f2b7 degrees, first. Give each DLIST its own TAG.
- `STACK=A97F`: the older stack without W13, with 140 keys. For comparison only.
- `GK=`, `ARGSF=`, `EXPECT_PAT=`, `F2BRULES=`: override single files. `F2BRULES=/tmp/swarm-W17/tab/rules_zcons.json` (or `.../rules_studio_keep95p131f_f7s.json`) reproduces an older family, for comparison only.

## 5b. Sending results back

The verdict is the `RESULT:` line of `/tmp/swarm-W17/logs/<TAG>/summary.txt`. TAG is the point's file name plus `_zW13`, for example `sol_q53A97q_zW13`. Send back the whole log folder and the run log:

    cd /tmp/swarm-W17/logs && tar czf /tmp/<TAG>_result.tgz <TAG> <TAG>_run.out && md5 /tmp/<TAG>_result.tgz

The folder holds:

- `p0.log`: the Python step;
- `sep.log`: one line per separator part;
- `summary.txt`: the verdict;
- `viol_*.txt`: any reported arrangements;
- `stamp.txt`.

Put the tgz in the swarm mount, at `round6/W17-studio-kstar/from_studio/<TAG>/`. The `RESULT:` line alone is enough for a first relay; the tgz is the record.

## 6. Restarts and memory

**Restartable.** check.sh always runs with `RESUME=1`, so after a crash, reboot or kill you rerun the same line.

- It keeps the Python step when the solution md5, code, args and env are unchanged and the query dump is complete.
- It keeps every separator part that finished: its `sep.log` line has rc=0 and an END, and its viol file exists.
- It reruns only the parts that were running or not yet started. A killed run therefore loses at most NPROC running parts, each at most about 4 min of CPU.
- `smoke.sh` is rerunnable too.

**Memory**, measured here on in11 with the W13 stack and 151 keys (peak RSS):

| process | peak RSS | count |
|---|---|---|
| Python step (`st21_w17.py`) | 0.65 GB (0.83 GB virtual) | one, during step 1 only |
| separator (`sep3r_gk7`) | 0.16 GB | one per running part |
| `drive17.py` driver | 15 MB | one per running part |

At NPROC 8 the total is about 1.4 GB (8 x 0.17 GB) once the Python step has ended. Every process is well under 3 GB. In the container each job also runs under `ulimit -v 4 GiB`. On macOS no limit is set, because macOS does not enforce `ulimit -v`.

## 7. Expected wall time

**PARTS.** `PARTS=d:n` splits degree d into n slices of its 25 start states, so n can be at most 25.

- The default split gives 73 parts, with the longest single part about 3-5 min on one container core.
- 8 processes stay busy until the last few minutes.
- At 10 or more processes, use `PARTS=7:6,8:16,9:25,10:12,11:8,12:4,13:2`.

**CPU.** The total separator CPU at t = 0.0185..0.0215 was 128-150 core-min on one swarm-container core:

| run | separator CPU | longest part (8 or fewer parts per d) |
|---|---|---|
| k85B in06 | 143 min | 755 s |
| k85C in01 | 128 min | 675 s |
| k86B in09 | d = 9 alone 45 min, about the same as in06 | |

For in11 at t = 0.01818 with W13 and 151 keys (f7s rules), the container's d = 7 CPU is in section 9. The corrected rule files have fewer rules, so their masks kill less. Expect the d = 7, 8, 9 separator to search somewhat more.

**Estimate at NPROC 8:**

- 150 / 8, about 19 core-min of wall time per process;
- about 1-2 min of table loading per part;
- the 1.7 min Python step.

**About 25-45 min wall for a point near t = 0.018, if a Mac core is as fast as a container core**, and less on an M-series performance core.

**q53A97q (t = 0.0988).** The bound is much looser there, and q is empty. Opus's own engine needed 12.6 s, 11.5 s and 6.0 s for d = 7, 8, 9. The estimator's t scale is 0.50 there, against 2.28 at t = 0.018. Expect **about 10-20 min wall at NPROC 8**, most of it the 2-min Python step, table loading and the d = 7..9 parts. Section 9 has the container's measured time.

## 8. What the check covers (for the record)

`upperR2` at the point's t on the k86S family, as a second engine:

- every sender row;
- cons2 in c6le form;
- mrowL;
- every receiver arrangement at d = 7..26, by an exhaustive separator with the f2b7 7-side masks and the GK windows plus an exact leaf;
- the d >= 27 DP and Karp tail.

The f2b leaf and the f2b7 7-side masks use only the rules in the chosen rule file: by default rules_zcons_minus_W18rejects (Studio zcons minus W18's strict-audit rejects).

## 9. Tested here (swarm container, 6 Nov 2026; this version 22:17-22:23Z container time)

**Setup.**

- **Tools:** Ubuntu clang 18.1.3 (`-std=c++17 -O3`) and CPython 3.9.25 with numpy 2.0.2 and scipy 1.13.1, in a uv venv.
- **Isolation.** The tarball was unpacked into a scratch folder. It was run at the literal `/tmp/swarm-W17` path inside a private mount namespace, in which the swarm's own `/tmp/swarm-W17`, `/mnt` and the Studio repo were hidden.
- **Slot.** The runs went through the swarm's cpuslot wrapper.

**Results.**

- **Manifest and build.** `MANIFEST.md5` all OK. `build.sh` took 16 s, with no errors and no warnings.
- **`smoke.sh`:** `SMOKE: PASS`, in 3 min 36 s under strace.
  - (1) `RESULT: PARTIAL PASS ... receivers d = 24,25,26 exhaustive 0 violated`. The run loaded `F2B rules /tmp/swarm-W17/tab/rules_zcons_minus_W18rejects.json ... {('w6', 7): 1531, ('w6', 8): 1114, ('w6', 9): 87, ('w7', 7, 1): 928, ('w7', 7, -1): 928, ('w7', 8, 1): 714, ('w7', 8, -1): 714}`, GK 151 keys (fe8a97a7), and D 18128 / C 686 / RPAT 158.
  - The Python-step self-tests PASS: W10 C++ vs Python; GK windows 0 mismatches; f2b self-test 6,000 arrangements with 0 Python vs C++ mismatches.
  - (2) `VERDICT: F2B7ROWS FAIL ... receiver d=7 5776667 9567857 reported above the bound (load 1.591377316)`, against a bound of 1.018178464, with 2b362955 loaded.
- **strace of the smoke**, with every file and exec call recorded:
  - Nothing outside the bundle, the system folders and the Python install was opened.
  - The only lookups outside were the two `[ -f ]` tests in `code_gk7/run17.sh` for the container's own copies. Both were absent, so the bundle copies were used, as designed.
  - Every bundle path the code looked up exists in the bundle.
- **`check.sh` and resume.** `DLIST=25,26 TAG=chk_mini bash check.sh in11 2` loaded 2b362955 and gave `RESULT: PARTIAL PASS`. Rerunning the same line gave `step 1: RESUME: kept ...` and `RESUME: 2 separator parts kept, 0 to run`, with the same RESULT.
- **Added after the test.** `sol/sol_q53A97q.json` and `ref/s86_k86RS/` were added after this test. They are data only; the code is byte-identical to the tested copy. The container is running q53A97q on the same code (see the swarm's round5/checks/R_q53A97q/VERDICT.md).
- **Timing reference** (container, f7s rules, so not a verdict). k86B in11, W13, 151 keys, one process, d = 7 with PARTS 7:4: separator CPU 611 s (parts of 159, 190, 112 and 150 s). Peak RSS was 649 MB in the Python step and 156 MB per separator.

**Input md5s:**

| file | md5 |
|---|---|
| `tab/rules_zcons_minus_W18rejects.json` | 2b362955 |
| `sol/sol_q53A97q.json` | 06767b0b |
| `args_A97F_W13_x_studio.txt` | bfca4bc4 |
| `pat/W13`, the 4 files | as Opus's MD5SUMS |
| `tab/cg_keys_r13.txt` | fe8a97a7 |
| `code_gk7/sep3r_gk.cpp` | f44f8668 |

Comparison only: `tab/rules_zcons.json` e6c496a1, `tab/rules_studio_keep95p131f_f7s.json` 704c371f, in11 2db802ad, in10 65418d1e.
