# maclane-k86: two s86 LP lanes for the Mac Studio

Made 8 Nov 2026 in the Opus container (P_own_lp/s86_f2b7) because the container's 16 GB / 4 cores are full.
The pack is a black box: unpack, relocate, build, smoke-test, launch, and send back the outbox. Nothing is installed or pip-installed;
it runs on the Mac's own `/usr/bin/python3` (3.9.6, numpy 2.0.2, scipy 1.13.1), Apple clang and bash 3.2.

| lane | tag | what it is | what comes back |
|---|---|---|---|
| **UPPER** (priority) | **k86MS1** | the container's k86GS4 in-out upper solve (same flags as `launch_k86GS4.sh`) on family **K3l** (`args_A97_F_W13K3l.txt`, container md5 2727d445), from the in-point `cand/sol_k86GS4_in01.json` (UPPER-R2 FEASIBLE on K3l at t = 0.030980300342), with its repair ladder (OP-23, family K3l), the in-point checker and the tighten step | every point whose own upperR2 says FEASIBLE: `outbox/upper/` (point + log + one line in POINTS.txt) |
| **LOWER** (control) | **k86ML1** | the container's k86GL6 lext run **without kill B**: family **K3g** (`args_A97_F_W13K3g.txt`, md5 bef43766) instead of K3gB, keys `p1r/cg_keys_r13w16_16fik.txt` (240 keys), flags `lext lextcert q7pen=1e-3 consk=20 consfrac=0.25`, XF with `p1r` and the offc rpatN file, engine `eng_p1r` | the phase-1 values (`lext it N: phase 1 ... t1 = ...`) and each phase-1 cert: `outbox/lower/` (cert files + P1.txt + K.log) |

## 1. Commands

    # unpack: any folder WITHOUT spaces in its path, on a local disk
    mkdir -p ~/maclane && cd ~/maclane
    md5 -q /path/to/maclane-k86.tgz             # must print the md5 in maclane-k86.tgz.md5
    tar -xzf /path/to/maclane-k86.tgz           # creates ~/maclane/maclane-k86
    cd maclane-k86

    bash relocate.sh        # 1. checks every file against MANIFEST.md5, then points every script at this folder (prints BAD lines if a file is damaged)
    bash build.sh           # 2. compiles the separators with clang++ (about 1 min): eng/bin/{jsepf_gk,jsep3}, eng_p1r/bin/{jsepf_gk_k192,jsepf_gk,jsep3}
    bash smoke.sh           # 3. 5-15 min; must end with "SMOKE: PASS" (section 3)
    bash launch_upper.sh    # 4. the UPPER lane k86MS1 (needs smoke step 6)
    bash launch_lower.sh    # 5. the LOWER lane k86ML1
    bash status.sh          # any time: what runs, last iterations, outbox
    bash collect.sh         # any time: ../maclane-k86-out-<time>.tgz with everything worth sending back
    bash stop.sh upper      # or: lower | all

Every lane process is started with `nohup` and `nice` (K runs nice 15, checks nice 12), so the terminal can be closed after the
launch. If the Mac sleeps, the runs pause (`caffeinate -i &` keeps it awake while that terminal lives). If the folder is moved, stop
the lanes and run `bash relocate.sh` again. Apart from temporary files in $TMPDIR, nothing is written outside the pack folder except `../maclane-k86-out-*.tgz` (collect.sh).

## 2. Knobs (environment variables, set on the launch command line)

Core budget: another job uses about 6 of the 16 cores, k19 one more, plus a Lean build. At the defaults the two lanes together use
**about 6 cores**: the upper K run 2 (its separation threads; the LP solve between separations is single-threaded), the upper repair
ladder 2 (two 1-thread upperR2 checks at a time), the lower K run 2. On top of that, when a new in-point or ladder point appears,
watch86 and tightwatch each run one 1-thread upperR2 for a few minutes (`TIGHTWATCH=0` skips tightening).

| variable | default | effect |
|---|---|---|
| `UPPER_THREADS` | 2 | separator threads of the upper K run (launch_upper.sh) |
| `REPL_PAR` | 2 | concurrent repair-ladder checks (1 thread each) |
| `TIGHTWATCH` | 1 | 0 = do not tighten new FEASIBLE points |
| `LOWER_THREADS` | 2 | separator threads of the lower K run (launch_lower.sh) |
| `MAXIT` | 200 | K-run iterations |
| `HSHIM_SOLVER` | ipm | LP method of the highspy shim: `ipm` (HiGHS IPX + crossover via scipy) or `simplex` (HiGHS dual simplex) |
| `REPL_MINMEM`, `TIGHT_MINMEM` | 0 | MB of free memory (vm_stat) a ladder / tighten check waits for; 0 = no gate (128 GB) |
| `OUTBOX_POLL` | 120 / 60 | seconds between outbox scans (upper / lower) |
| `SMOKE_THREADS`, `SMOKE_LOWER` | 1, 1 | smoke.sh: threads of its two upperR2 runs; SMOKE_LOWER=0 skips step 7 |

Example: `UPPER_THREADS=3 REPL_PAR=1 bash launch_upper.sh`.

## 3. Smoke test (smoke.sh)

1. the pack is relocated to the folder smoke.sh is in;
2. python / numpy / scipy versions; reports whether highspy exists (expected: no, so the shim is used);
3. **the highspy shim against highspy**: `tools/hshim_check.py` solves 40 LPs whose highspy 1.15.1 solutions were stored in the container
   (`tools/hshim_ref.json`), twice each on one model object (the second time after cost, bound and row edits), with both shim methods;
   status, objective (1e-7) and, where the vertex is unique, x, row duals and column duals (1e-6, signs included) must match;
4. every engine module parses under this python;
5. the five separator binaries exist;
6. **upper lane**: upperR2 of `cand/sol_k86GS4_in01.json` on K3l with the lane's engine, keys and flags, compared line by line
   (paths and timings normalised) with the container's log `ref/upper_F_k86GS4_in01_K3l.log`; must be FEASIBLE at t = 0.030980300342.
   This writes `logs/upper_F_k86GS4_in01.log`, which launch_upper.sh requires.
7. **lower lane engine**: the same point with eng_p1r, K3g, the 240 keys and `p1r` (d = 7 runs bin/jsepf_gk_k192). This pack has no
   container reference for it (the container had no memory to spare for that run), so it must run to the end with no traceback and
   print an `UPPER-R2:` verdict; the verdict itself (FEASIBLE or not on K3g) is reported, not judged. `SMOKE_LOWER=0` skips it.

Logs: `smoke.log`, `smoke_hshim.log`, `smoke_upper_cmp.log`, `logs/smoke_lower_in01_K3g.log`. Steps 6 and 7 take about 3 min each at
1 thread in the container (load ~60 s, d = 7 ~65 s, d = 8 ~30 s, the rest ~25 s).

Step 6 tolerates one unit in the 6th printed digit of a diagnostic number (such lines are listed as "close" in smoke_upper_cmp.log):
the container's separators were built by GCC with `-march=native`, which fuses 3 multiply-adds, this build does not
(`-ffp-contract=off`). Integers (pattern / key / leaf / violated counts) and the verdict line must match exactly. If step 6 fails:
do not launch the upper lane; run `bash collect.sh` and send the tarball back.
(launch_upper.sh itself only checks that logs/upper_F_k86GS4_in01.log says `UPPER-R2: FEASIBLE at t = 0.030980300342`.)

## 4. What comes back (outbox/)

**outbox/upper/** (filled by `outbox86.sh`, every 2 min): for every `cand/sol_X.json` whose own upperR2 log says `UPPER-R2: FEASIBLE`
(watch86 in-points `sol_k86MS1_inNN`, repair-ladder points `sol_repS1MW_NN`, tightened points `sol_X_tight`, and the start point from the smoke test):

* `sol_X.json` and its log `upper_sol_X.log` / `upper_F_X.log`;
* one line in `POINTS.txt`: `name  t  md5  family  log  filed-at`;
* `MD5SUMS`.

**outbox/lower/** (filled by `outbox86L.sh`, every 60 s): each time `eng_p1r/cert_k86ML1_p1.json` changes (a new lext phase-1 cert), once
its size is stable and it parses as JSON:

* `cert_k86ML1_p1_NN_<md5 8>.json` and `sol_k86ML1_p1_NN.json`;
* one line in `P1.txt`: `NN  md5  t1 <value>  it <iteration>  filed-at`;
* `K_k86ML1.log` (the whole K.log, refreshed) and `P1_lines_k86ML1.txt` (all `lext it N: phase 1 ... t1 = ...` lines);
* `MD5SUMS`.

`bash collect.sh` puts outbox/ plus both K.logs, run.log, the rows files and the smoke logs into one tarball next to the pack folder.
These t1 values and certs are [M] until the container's lowerR2 checks a cert; lowerR2 / exactbasis / the dual watchers do not run here.

## 5. How it differs from the container (and why the results are the same objects)

* **highspy → hshim.** highspy is not installed and must not be. Every `import highspy` in the engine copies is
  `try: import highspy` / `except ImportError: import hshim as highspy` (HSHIM_FORCE=1 forces the shim even where highspy exists).
  `eng/hshim.py` (same file in eng_p1r) keeps the model (column bounds / costs, sparse rows lo <= a.x <= hi) and solves it from
  scratch at every `run()` with `scipy.optimize.linprog(method='highs-ipm')` (HiGHS's IPX + crossover, i.e. a vertex; `simplex` =
  HiGHS dual simplex). Ranged rows are passed as two one-sided rows and their duals recombined into HiGHS's sign convention
  (row dual >= 0 when the lower side binds, <= 0 when the upper side binds), which is what the lext phase-1 cert and the in-out code read.
  Supported: Highs(), setOptionValue (output_flag, threads, solver, time_limit, primal/dual_feasibility_tolerance, presolve), addVar(s),
  addRow(s), changeColCost, changeColsCost, changeColBounds, changeColsBounds, changeRowBounds, getCols, getNumCol/Row/Nz, run,
  getModelStatus, modelStatusToString, getSolution (col_value, col_dual, row_value, row_dual), getInfo().objective_function_value,
  getRunTime, getBasis (+HighsBasisStatus, reconstructed from the solution; only lowerR2 exactbasis uses it, which does not run here),
  kHighsInf, HighsModelStatus.
  **Differences:** no warm start (each LP is solved from scratch; in the container each iteration's LP already fell back from 45 s
  of simplex to IPM + simplex, ~1700 s at 353k rows x 97k columns for k86GS4); `time_limit` is ignored, so the engine's `lpmax`
  fallback is never taken (the shim already uses IPM); `threads` is ignored. A shim run prints one `hshim: run N: ...` line to
  the K.log (set HSHIM_QUIET=1 to silence). Every point is still checked by the exhaustive upperR2, every cert by the container's lowerR2.
* **Python 3.9.** All 42 Python files of the pack (both engines, hshim, the tools, repladder, tighten_floor) were scanned for 3.10+
  syntax and APIs (ast feature_version 3.9, PEP 701 f-strings, 3.10-3.13 stdlib calls, numpy >= 2.1 names): 0 findings, nothing patched.
* **macOS tools.** `macshim/md5sum`, `macshim/timeout` stand in for the GNU tools (the scripts put macshim/ on PATH). Mac copies of
  four scripts: `tighten.sh` (a here-document inside `$( )`, which bash 3.2 mis-parses, moved to `tighten_floor.py`), `tightwatch.sh`
  and `repladder.py` (memory gate via `vm_stat` instead of `/proc/meminfo` / `free`, off by default; repladder's swarm copy removed —
  outbox86.sh files its points; REPL_PAR default 2), `env86.sh` (puts macshim/ on PATH). New: `launch_k86MS1.sh`, `launch_k86ML1.sh`,
  `outbox86.sh`, `outbox86L.sh`, `smokeU.sh`, `maclib.sh`, `tighten_floor.py`, `maclane_warm_upper.txt`, `maclane_warm_lower.txt`.
* **Paths.** Every file sits at `fs/<its container path>`. Scripts, args files and warm lists had the three container prefixes
  (`/home/claude/GraphColourDeductiveSolver/`, `/tmp/claude-0/`, `/mnt/project-files/`) rewritten to `<pack>/fs/...`; data files are
  byte-identical (`ORIGMD5.tsv`: relpath, container path, container md5, packed md5, kind). Logs therefore name `<pack>/fs/...` paths.
* **Separators.** Built on the Mac by build.sh: `clang++ -std=c++17 -O3 -pthread -ffp-contract=off -include cstdint` (+ `-mcpu=native`
  when the compiler accepts it). The sources use only standard headers (no x86 intrinsics, no long double); `-include cstdint` because
  they use uint64_t etc. without including it (GCC's headers happen to pull it in, libc++'s need not).
* **Warm rows.** Upper: k86GS4's launch list (`runK_k86GS4/warmlist.txt`, 41 files) + `warm/rows_k86GS4_snap_MS1.txt` (k86GS4's own
  rows at pack time; rows the K3l family does not admit are dropped by the engine on admission). Lower: k86GL6's launch list
  (`runK_k86GL6/warmlist.txt`), unchanged.

## 6. Expectations

* Memory: in the container a K run is 4.5-5 GB with highspy; the shim adds scipy's copies of the constraint matrix, so expect
  roughly 6-10 GB per K run, ~1.1 GB per upperR2 check. Disk: a few hundred MB of logs / rows per day.
* Time: one K iteration = one LP (from scratch) + separation rounds; in the container k86GS4 takes ~2100-4300 s per iteration, of
  which the LP is ~1700-2000 s (its warm simplex already hit the 45 s limit every iteration and fell back to IPM). The shim's LP
  time on the Mac is not known in advance: the first `hshim: run 1: ...` line in K.log reports it.

## 7. Files

    README.md  MANIFEST.md5  ORIGMD5.tsv  .root
    relocate.sh build.sh smoke.sh launch_upper.sh launch_lower.sh status.sh stop.sh collect.sh
    tools/  relocate.py hshim_check.py hshim_ref.json cmp_upper.py
    macshim/  md5sum timeout
    ref/    upper_F_k86GS4_in01_K3l.log (smoke step 6 reference), K_k86GS4_container.log / K_k86GL6_container.log (the container
            runs these lanes follow), container_scripts/ (their launch scripts and warm lists; not run here)
    outbox/ upper/ lower/
    fs/home/claude/GraphColourDeductiveSolver/.../P_own_lp/s86_f2b7/   (N: engines eng/ eng_p1r/, scripts, args, cand/, logs/, runK_<tag>/)
    fs/...  every other file the lanes read, at its container path

## 8. What was tested before packing (container, 8 Nov 2026)

* **Shim vs highspy 1.15.1** (container Python 3.13, numpy 2.5.3, scipy 1.18.1):
  * 400 small random LPs (<= / >= / ranged / equality rows, free / capped / boxed columns), each solved 3 times on one model
    object with cost, bound and row edits in between, as the engine edits its model: 600 solves per method, 0 status and 0 objective
    mismatches, max relative objective difference 1.6e-12 (ipm) / 3.9e-13 (simplex); at the 482 / 456 nondegenerate vertices
    max |dx| 1.1e-11, |d row dual| 7.9e-11, |d col dual| 5.4e-11; 18,789 nonzero row duals compared, 0 sign mismatches; the shim's
    own certificates: primal infeasibility <= 4.8e-13, |c - A'y - col_dual| <= 1.6e-12, duality gap <= 1.3e-13, 0 duals on the wrong side.
  * an engine-shaped LP (free t, sender rows >= 1, receiver rows, lext phase 1 / phase 2 cost and bound switching): phase-1
    t1 = 0.011534239321 and phase-2 t = 0.011534240321 with both.
  * 12 medium LPs (463-1335 columns, 517-2234 rows) x 3 solves, ipm: max relative objective difference 6.3e-14 over the 16 solves
    optimal in both, nondegenerate |dx| <= 1.2e-10, |dy| <= 1.4e-10, 0 sign mismatches in 8,188 nonzero row duals; 9 edited models
    were infeasible, where highspy's warm-started simplex stopped at Unknown after 57-87 s and the shim reported Infeasible.
  * `tools/hshim_check.py` (smoke step 3) on its reference file: 40 LPs x 2 solves x 2 methods, 0 failures, max relative objective
    difference 1.4e-14, x / duals within 1.4e-13, 0 sign errors.
* **Python 3.9 scan**: 42 files, 0 findings (section 5).
* **C++**: the 8 separator sources of the engine copies compile with g++ 13.3 and clang++ 18.1 (x86-64) under
  `-std=c++17 -O3 -pthread -ffp-contract=off -include cstdint -Wall -Wextra`: clang 0 warnings; g++ only `-Wmisleading-indentation`
  on `if (fread(...) != n) return 73; fclose(qf); QM = true;` (the fclose is meant unconditionally; the code is right).
* **The pack**: tarred, unpacked in another folder, `relocate.sh` (manifest 0 bad, every path rewritten), `build.sh` with clang++
  (5 binaries in 13 s), smoke steps 1-5, status.sh, collect.sh and stop.sh run there.
* **Completeness**: every path in both args files exists in the pack (304 / 306 pattern files; the 2 others, out/job28/r_3.cfast and
  r_4.cfast, are missing in the container too and both logs say so), as does every path the lane environment expands to, every file
  the launch / runner / check scripts name, and every warm file (42 upper, 43 lower). No container path is left in a rewritten file.
  The start of smoke step 6 was run from the unpacked pack under strace (shim forced): its first 6 log lines (rules, 171 keys,
  jcheck, exname, `patterns: 304 files read, 2 missing`, counts by d) are identical to the container's, 394 files were opened inside
  the pack, none outside it and none missing.
* **Not run in the container**: smoke steps 6-7 to the end, any K run, the shim on a full-size LP (353k rows x 97k columns). Each
  needs >= 1.1 GB for minutes and the container's free memory stayed at 4.3-4.8 GB under its 4.5 GB floor while the live runs went
  on (the traced run above was stopped by the memory gate after 6 s). Not run anywhere: bash 3.2, the BSD tools and vm_stat (the
  scripts were reviewed for them and syntax-checked with bash 5). The Mac's smoke.sh is the first full run of steps 6 and 7.
