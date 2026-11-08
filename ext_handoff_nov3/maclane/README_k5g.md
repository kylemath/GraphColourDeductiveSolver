# maclane-k86 k5g add-on: one family switch for every binder kill (k86MS2 -> k86MS3 -> ...)

Made 8 Nov 2026 in the Opus container (P_own_lp/s86_f2b7; files copied 16:12-16:27Z). This is a small add-on for the maclane-k86 pack
(`maclane-k86.tgz`, 2fa853ec). **The v2 (138c2965), k5d (86045dcd) and k5e (7bf3c869) add-ons must already be installed.** It only adds
files. No installed file is changed, and nothing runs until you launch it. It does not touch the running k86MS2.

From now on, a new binder kill needs no new scripts. Each kill comes as a small **family data add-on**: the kill file, the two args files,
an EXPECT file and one line for `fam/FAMILIES.txt`. You install it with `install_fam.sh`, test it with `smoke_fam.sh <x>`, and move the
lane with `launch_upper_fam.sh <x>`. This add-on brings the scripts plus the first data entries, **e** (the family k86MS2 runs now, for
the record), **f** and **g**.

| suffix | kill file (md5) | LP family K3gB5x (container md5) | check family K3l5x (container md5) | status |
|---|---|---|---|---|
| e | `w13/pat_K5e_C.cfast` (9d00aa01; K-5e B2) | K3gB5e (8849c09f) | K3l5e (2b31d32d) | [E2] Studio K3CHK11 (k86MS2's family) |
| **f** | `w13/pat_K5f_C.cfast` (**011a82a2**; K-5f ST-42 H05) | **K3gB5f (8c5d5005)** | **K3l5f (ba8677a5)** | **[E2]** Studio K3CHK main 346c68988 |
| **g** | `w13/pat_K5g_C.cfast` (**7d448592**; K-5g ST-61 B3) | **K3gB5g (6251f38a)** | **K3l5g (be643743)** | **[E2]** Studio K3CHK12 main b77d2725f |

Each args file is the previous suffix's args plus exactly one line, `cpat=<kill file>`: f = e + K5f, g = f + K5g. The build checked
this in the container, and `fam_lib.py famcheck` checks it again on the Mac. pat_K5g_C.cfast is the current file, **7d448592**: the
Lead changed only its comment line, from [P] to [E2]. Its args md5s and pattern counts did not change.

**Both f and g are [E2]**, so their `fam/FAMILIES.txt` lines say `status=E2`, and the Studio can move the lane straight to **g**. The
rule "g only after the Lead's [E2] note for B3" is built in. A family whose status is not E2 is refused unless you launch it with
`E2_NOTE="<the Lead's note>"`, and that note goes into run.log.

## 1. Commands (on the Studio)

    cd ~/maclane                                    # the folder that holds maclane-k86/ (use your own path)
    md5 -q /path/to/maclane-k86-k5g.tgz             # must print the md5 in maclane-k86-k5g.tgz.md5
    tar -xzf /path/to/maclane-k86-k5g.tgz           # creates ~/maclane/maclane-k86-k5g/
    bash maclane-k86-k5g/install_k5g.sh ~/maclane/maclane-k86     # checks and copies, then installs the data entries e, f, g
    cd ~/maclane/maclane-k86
    bash smoke_k5g.sh       # about 13 min (f then g, about 6 min each); must end with "SMOKE-K5G: PASS". k86MS2 keeps running.
                            # In a hurry: SMOKE_FAMS=g bash smoke_k5g.sh  (only g, about 6 min; launching g needs only smoke_fam_g.ok)

    DRY=1 bash launch_upper_fam.sh g     # the plan only: lane, in-point candidates, warm set, what stops and starts
    bash launch_upper_fam.sh g           # k86MS2 -> k86MS3 on K3gB5g / K3l5g (section 2)
    bash status_fam.sh                   # the newest lane: K run, ladder / tighten / in-point lines, outbox points by family
    bash stop_fam.sh                     # stops the newest lane (results kept); bash launch_upper_fam.sh g restarts it

    bash recheck_fam.sh g repS2MW_05     # any upper point on K3l5g + 240 keys (eng_p1r), about 5 min on 1 thread; 3rd arg = threads

The next kill, for example K5h, will come as `maclane-k86-fam-h.tgz` with its own .md5. Then:

    bash install_fam.sh /path/to/maclane-k86-fam-h.tgz   # checks; adds fam/FAMILIES.txt line h
    bash smoke_fam.sh h                                   # about 6 min; "SMOKE-FAM h: PASS" writes smoke_fam_h.ok
    bash launch_upper_fam.sh h                            # k86MS3 -> k86MS4 (E2_NOTE="..." if its status is not E2)

You can use f the same way (`bash launch_upper_fam.sh f`) at any time. The lane's knobs are the same as k86MS2's: `UPPER_THREADS`,
`MAXIT`, `REPL_PAR`, `REPL_MINMEM`, `TIGHTWATCH`, `TIGHT_MINMEM`, `HSHIM_SOLVER`. When they are not set, the new lane takes the previous
lane's threads, maxit and REPL_PAR from that lane's run.log lines, so the core budget does not change.

## 2. launch_upper_fam.sh <suffix> [point]

1. **Checks before anything is stopped.** It refuses with exit 2, and nothing has been stopped, when:
   * the suffix has no `fam/FAMILIES.txt` line;
   * its kill file or either args file is missing;
   * any md5 differs from the line. For the args files, the md5 is taken with the pack root removed, so it equals the container's md5;
   * an args file is not the previous suffix's args plus that one kill line;
   * the status is not E2 and no `E2_NOTE` is given;
   * `smoke_fam_<x>.ok` is missing (`FORCE=1` overrides this one).

   The **current lane** is the newest `[s86K-k86MS<n>] start` line in run.log. Today that is k86MS2, on K3gB5e.

   The **fallback in-point** is the point given on the command line, else `FAM_DEFAULT`, else the current lane's own in-point (the
   `feas` of its start line). It must be upperR2 FEASIBLE on K3l5x + 240 keys **here**, as a run.log check of this exact file. If no
   such check exists yet, the script runs `recheck_fam.sh x` on it first: about 5 min on `FAM_RECHECK_THREADS` = 2, while k86MS2
   keeps running. If that check is not FEASIBLE, the script stops, and nothing has been stopped.
2. **Stops the current lane cleanly** with `stop_fam.sh <tag>`, and waits until it is gone:
   * first the watchers (watch86_k5e, tightwatch_k5e);
   * then the ladder, tighten runs and the lane's own checks;
   * then the K run;
   * then the outbox poller. One last outbox pass files the lane's unfiled points under its own family (for k86MS2, `__K3l5e` /
     `__K3gB5e`), exactly as its outbox86_k5e.py would.

   `runK_<tag>/K.log`, `eng_p1r/rows_<tag>.txt` and outbox/upper are kept. run.log gets
   `[maclane] fam: stopped k86MS2 for k86MS3 on family g (last iteration: ...)`. (If the current lane is k86MS1, it is stopped with
   `TAG_UPPER=k86MS1 bash stop.sh upper` plus the K3l last pass, as launch_upper_k5e.sh does.)
3. **In-point.** The script takes the **newest outbox/upper point that passes the recheck on K3l5x**. Candidates are the POINTS.txt
   lines filed after the fallback's first filing that meet all of these:
   * the family is a check family: K3l or K3l5<any>, never K3gB*;
   * t is below the fallback's;
   * newest first, one per md5, at most `FAM_MAXRECHECK` (3).

   For each candidate:
   * a point already FEASIBLE on K3l5x here is taken without a new check;
   * a point already checked on K3l5x here and found not FEASIBLE is skipped;
   * otherwise it is rechecked with `recheck_fam.sh` (k86MS2 is stopped by then, so the cores are free). The first FEASIBLE one wins.

   If none passes, the fallback is used. A point named on the command line (or with `INPOINT=`) is used as it is, with no search. run.log
   gets `[maclane] fam: in-point for k86MS3 (family g): <name> (md5 ...), ...`.
4. **Starts the next tag**, k86MS<n+1>, with `fs/.../s86_f2b7/launch_msfam.sh` (section 3). If the newest lane is already on family x,
   the script restarts that same tag instead. It refuses (exit 3) while that lane runs.

## 3. The new lane (launch_msfam.sh)

launch_msfam.sh is the k5e add-on's launch_k86MS2.sh with the families, the tag and the previous lane as parameters. Everything else is
k86MS2's: the in-out flags, eng_p1r, the 240 keys (`p1r/cg_keys_r13w16_16fik.txt`, 3d996dbb, standard coefficients), U86e.sh with
flags `c6le f2b7 f2b=<rules c67fa1d1 + A5 twins> rpatN=<rpatN3 rotation-justified>`, and the ladder settings.

| | k86MS2 (k5e add-on) | **k86MS3** (this add-on, family g) |
|---|---|---|
| LP family | K3gB5e (8849c09f) | **K3gB5g** (6251f38a) |
| K run | `p1r/runK86p.sh <maxit> <threads> k86MS2 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25` | the same, tag k86MS3; maxit / threads / REPL_PAR as k86MS2's |
| in-point checks | watch86_k5e.sh on K3l5e | watch86_k5e.sh, `WATCH_ARGS` = **K3l5g** |
| repair ladder | repladder_k5e.py: main K3gB5e, sub-check K3l5e | repladder_k5e.py: main **K3gB5g**, sub-check **K3l5g**; points `sol_repS3MW_NN` |
| tightening | tightwatch_k5e.sh / tighten_k5e.sh on K3l5e (eng_p1t) | the same on **K3l5g** |
| outbox | outbox86_k5e.py: `__K3l5e` / `__K3gB5e` | **outbox86_fam.py k86MS3 g**: `__K3l5g` / `__K3gB5g` (section 4) |

**Warm set.** The new lane gets:
* the previous lane's warm list (`runK_k86MS2/warmlist.txt`, or `maclane_warm_upper.txt` if there is none);
* the complete lines of the previous lane's rows (`eng_p1r/rows_k86MS2.txt` -> `warm/rows_MS2_snap_k86MS3.txt`; a partial last line is
  dropped; the name leaves out "k86MS2", so `pgrep -f k86MS2` never lists k86MS3).

Rows that family g no longer admits are dropped on admission; K.log reports them as `warm rows admitted`.

On a restart of the same tag, the lane uses its own previous warm list plus the complete lines of its own rows, and its K.log is kept as
`runK_<tag>/K_prev_<UTC>.log`.

**Rules.** launch_msfam.sh refuses an in-point that has no FEASIBLE K3l5x + 240-key check of this exact file here. It also refuses to
start while the previous lane (its K run, outbox or ladder) still runs, so at most one upper LP runs. run.log gets
`[maclane] launch k86MS3 (fam g, after k86MS2): ...` with both container md5s, the in-point, threads and the warm count.

## 4. The outbox: the family is in the file name

The new lane's points go to the same `outbox/upper/` the Studio already syncs. Each point is filed once:
* as `<name>__K3l5g.json` + `.log` when a check of exactly that file on K3l5g is FEASIBLE: the in-point check, the ladder sub-check
  `F_rep..._sub` or a tighten final;
* as `<name>__K3gB5g` when it is a ladder point that is FEASIBLE on the LP family but whose K3l5g sub-check ended without FEASIBLE.
  Such a point is an LP in-point, **not** a K3l5g point.

POINTS.txt keeps its columns (`name  t  md5  family  log  filed-at`), with family K3l5g / K3gB5g. Older lines are not changed: k86MS2's
stay `__K3l5e` / `__K3gB5e`, and k86MS1's stay plain K3l. A point of one family can never be read as another family's point.
`recheck_fam.sh` also files a FEASIBLE recheck there, for example `sol_repS2MW_05__K3l5g.json` next to k86MS2's
`sol_repS2MW_05__K3l5e.json`: same md5, two families, two lines.

## 5. recheck_fam.sh <suffix> <point> [threads]

recheck_fam.sh is recheck_k5e.sh for any family: the exhaustive upperR2 (gkwin gkleaf) on eng_p1r, args K3l5x, the 240 keys and the lane's
flags. It refuses a suffix that fails famcheck. The point can be a `cand/` name, an `outbox/upper/` name (with or without `__K3l5e`) or a
json path. It writes:
* `logs/upper_F_<name>_K3l5x.log` and a run.log line;
* in `outbox/fam/`, the log and one line in `RECHECK.txt` (`name  md5  family  verdict  log  checked-at`);
* when FEASIBLE, `outbox/upper/sol_<name>__K3l5x.json` + `.log` and a POINTS.txt line. `RECHECK_UPPER=0` skips this, and the smoke
  uses that.

Exit status: 0 = FEASIBLE, 1 = not FEASIBLE, 2 = could not run. A stale work dir left by a killed check of the same tag is cleared
first. If that check is still running, recheck_fam.sh stops with exit 2.

## 6. Family data add-ons (the format for the next kills)

`maclane-k86-fam-<x>.tgz` holds one folder, `maclane-k86-fam-<x>/`, with:

* `FAMILY.txt`: its `fam/FAMILIES.txt` line, `suf=<x> prev=<p> pat=w13/pat_K5<x>_C.cfast pat_md5=... l=args_A97_F_W13K3l5<x>.txt
  l_md5=... gb=args_A97_F_W13K3gB5<x>.txt gb_md5=... expect=fam/EXPECT_K3l5<x>_k240.txt expect_md5=... status=E2|P note=<the kill
  file's comment>`. All md5s are full 32-hex values; the args md5s are the container's;
* `MANIFEST.md5` and `payload/`. The payload holds the kill file, both args (container root -> packed root, as relocate.sh expects)
  and `fam/EXPECT_K3l5<x>_k240.txt` with three sections:
  1. the first lines (up to `patterns:`) of an upperR2 run on K3l5x + 240 keys, paths stripped;
  2. the same on K3gB5x;
  3. the verdict of `recheck_fam.sh x` on `ref/k5e/sol_S1MW07k240e.json`.

`install_fam.sh` (tools/install_fam.py) follows the add-ons' rules:
* every file is checked against MANIFEST.md5;
* the pack must be relocated and have k5e + k5g;
* it writes new files only. A file the pack already has with other content stops it before anything is written (exit 4); identical
  files are skipped;
* the line is appended only after famcheck passes on the new line. If famcheck fails, the new files are removed again, FAMILIES.txt
  is unchanged, and the exit is 5;
* a different line for a suffix that is already there is refused (exit 4);
* a damaged add-on gives exit 3.

FAMILIES.txt is append-only, and `fam/INSTALLED_fam.txt` logs each install. A kill that adds a D pattern (`pat=<file>` instead of
`cpat=`) works the same way.

The data add-ons are built where the kill lands (the Opus container), with `tools/mkfam.py <x> <prev> <out dir>`. It reads the
container's kill file, both args and the two `logs/upper_P_*` pattern logs; it reads only and writes only into `<out dir>`. It checks the
chain and builds the tgz and its .md5, with the same bytes on every build. The bundled e, f, g entries were made with it
(`k5g/data/maclane-k86-fam-{e,f,g}.tgz`, md5s d1c1db2a / e6bc4e3e / 8c2c7f56).

Status `P` is set when the kill file's comment does not say [E2]. smoke_fam.sh works on such a family, but launch_upper_fam.sh needs
E2_NOTE.

## 7. Smoke tests

`smoke_fam.sh <x>` takes about 6 min and runs one engine run at a time, on 1 thread, under 2 GB. `SMOKE_MINMEM=<MB>` makes it wait for
that much free memory before each run. Its steps:
1. **famcheck:** the FAMILIES.txt line, the md5s and the args chain;
2. **K3l5x patterns:** an upperR2 start on K3l5x + 240 keys, stopped once `patterns:` is out. Its EXPECT lines must equal section 1;
3. **K3gB5x patterns:** the same on K3gB5x, against section 2;
4. **recheck:** `recheck_fam.sh x` on `ref/k5e/sol_S1MW07k240e.json` (the Mac's repS1MW_07, e4e93b2c). The verdict must be section 3,
   **UPPER-R2: FEASIBLE at t = 0.025171803977**, and the log's first lines must equal section 1. A kill only removes configurations
   from the check, so the reference point stays FEASIBLE. `SMOKE_FAM_RECHECK=0` skips this step;
5. **DRY plan:** `DRY=1 FORCE=1 launch_upper_fam.sh x <reference point>` makes the plan.

On PASS it writes `smoke_fam_<x>.ok`, which launch_upper_fam.sh needs.

`smoke_k5g.sh` checks that the installed files are there and parse, runs famcheck on every family (e, f, g in chain order) and shows the
current lane. It then runs `smoke_fam.sh` for each family in `SMOKE_FAMS` (default `f g`). Nothing in either smoke stops, starts or
touches a running lane or outbox/upper. Each one adds a line to `outbox/fam/RECHECK.txt` (the Mac's own recheck).

## 8. EXPECT counts (patterns lines, 240 keys, rpatN3)

| family | files read | distinct by d (7 / 8 / **9** / 10 / 11 / 12 / 13-17) | D / C / RPAT / RPATN |
|---|---|---|---|
| K3l5e | 311 | 9360 / 5908 / **3321** / 1426 / 613 / 85 / 65 | 18142 / 704 / 158 / 2034 |
| **K3l5f** | **312** | 9361 / 5908 / **3321** / 1426 / 613 / 85 / 65 | **18142 / 705** / 158 / 2034 |
| **K3l5g** | **313** | 9361 / 5908 / **3322** / 1426 / 613 / 85 / 65 | **18142 / 706** / 158 / 2034 |
| K3gB5e | 310 | 9387 / 5943 / **3418** / 1426 / 613 / 85 / 65 | 18232 / 773 / 158 / 2034 |
| **K3gB5f** | **311** | 9388 / 5943 / **3418** / 1426 / 613 / 85 / 65 | **18232 / 774** / 158 / 2034 |
| **K3gB5g** | **312** | 9388 / 5943 / **3419** / 1426 / 613 / 85 / 65 | **18232 / 775** / 158 / 2034 |

All files read report 2 missing (r_3, r_4), as in the container. These are the coordinator's counts: K3l5f D 18142 / C 705; K3l5g
C 706, d9 3322; K3gB5f D 18232 / C 774; K3gB5g C 775; RPAT 158 / RPATN 2034 everywhere.

Each kill adds one file and one C entry:
* K5f is a d7 window (f7_7676.55_..5..66), so it adds one distinct d7 pattern;
* K5g is a d9 window (f9_55555..67_.......5.), so it adds one distinct d9 pattern.

Sections 1 and 2 of f and g come from the container's `logs/upper_P_K3l5f.log` etc., which are shipped in `ref/k5g/`. Those of e come
from the k5e add-on's sources.

## 9. What was tested (container, 8 Nov 2026)

Everything ran on test copies of the pack, never on the container's live runs. Each copy had maclane-k86.tgz plus the v2, k5d and k5e
add-ons, relocated, with smoke_k5e passed. One engine run at a time, at nice 19, under a memory gate: start only with MemAvailable
>= 4.5 GB, wait for 4.5 GB again before each engine run, and kill below 3.0 GB.

* **Build.** 22 payload files; none of them is in the main pack or the earlier add-ons. The four args and both kill files equal the
  container's, with the md5s above.
* **Install** from the tgz into a fresh relocated pack: 22 files written, then families e (1 new file, the EXPECT; the e kill file
  and args are k5e's, identical), f and g (4 each). Further checks:
  * a second install wrote 0 files (22 identical; family lines kept);
  * an update from an earlier build replaced exactly the 2 changed files;
  * with a different launch_upper_fam.sh already in the pack: CONFLICT, exit 4, nothing written;
  * without the k5e add-on: refused, exit 2.
* **smoke_k5g.sh: SMOKE-K5G: PASS** (16:38:52-16:49:19Z, 10.5 min; peak RSS 1.6 GB; lowest MemAvailable 3.0 GB, while one of the
  container's own ladder checks ran alongside):
  * steps 2 and 3: EXPECT sections 1 and 2 re-derived line for line for f and g, 3 s each;
  * step 4: the rechecks of repS1MW_07 on **K3l5f** (302 s) and **K3l5g** (311 s) were both **FEASIBLE at t = 0.025171803977**
    (section 3), and their first lines equal section 1;
  * step 5: the DRY plans were made.

  A rerun on the final build passed as well: a fresh install from the tgz, smoke_k5g.sh with SMOKE_FAM_RECHECK=0, test_fam_lib.py and
  integ_k5g.sh (16:50-16:53Z). smoke_fam.sh e with SMOKE_FAM_RECHECK=0 passed too, so the e entry's EXPECT sections 1 and 2 hold. The final build differs from the smoked one only in install_fam.py (it removes new files when famcheck
  fails), one run.log wording in launch_upper_fam.sh, and this README.
* **Data add-on tests.**
  * A test family h, made with mkfam.py from a fake container folder, installed and reported status P. A second install of it was
    identical.
  * launch_upper_fam.sh h was refused for status P without E2_NOTE, and for the missing smoke_fam_h.ok.
  * Each of the following was refused:
    * another line for h, exit 4;
    * a damaged copy, exit 3;
    * a family i whose FAMILY.txt had a wrong args md5: exit 5, FAMILIES.txt unchanged, its new files removed again.
  * With pat_K5g_C.cfast changed by one byte, or missing, or with args K3gB5g missing, launch_upper_fam.sh g and recheck_fam.sh g
    refused and stopped nothing. An unknown suffix was refused too.
* **test_fam_lib.py: PASS** (20 checks on fabricated run.log lines):
  * outbox86_fam.py for k86MS3 / g: which file gets which family, POINTS.txt columns, logs, MD5SUMS, the polling mode, and not filing
    another lane's or another family's points;
  * the last pass of k86MS2 / e;
  * `verified`, `state` and `file` for g;
  * `pick`: newest first, check families only, t below the reference, one per md5, at most N;
  * `lane`.
* **integ_k5g.sh: INTEG-K5G: PASS** (22 checks): the k86MS2 -> k86MS3 switch end to end in a test pack. The LP was replaced by a stub
  that writes the real start line and warm list; everything else was real:
  * k86MS2 was started with the k5e add-on's own launch_k86MS2.sh;
  * DRY made the plan and stopped nothing;
  * the switch stopped all five parts of k86MS2 and kept its rows and K.log. Its unfiled in-point was filed `__K3l5e`;
  * in-point choice: of the points filed after k86MS2's in-point, the INFEASIBLE-on-K3l5g one was skipped, the FEASIBLE one was taken,
    and the K3gB5e one was never considered;
  * k86MS3 started with all five parts:
    * watch / tightwatch on K3l5g, ladder K3gB5g + sub K3l5g (read from the processes' environment);
    * a start line with k86MS2's maxit / threads and k86GS9's flags;
    * warm = k86MS2's 43 files + the 200 complete rows;
  * a second launch was refused, and status_fam.sh showed all parts;
  * stop_fam.sh stopped everything, and the restart reused tag k86MS3 with its own warm list and kept the previous K.log;
  * run.log was only appended to.

## 10. Not verified

* bash 3.2 / BSD tools on the Mac. Only static checks were run, and the scripts use the same idioms as the k5e add-on, which runs on
  the Studio.
* A real k86MS3 LP. The container's memory does not allow one next to its two LPs, so the integration test used a stub K run. The LP
  command is k86MS2's with the args file changed, and the K3gB5g pattern lines of that command were checked in smoke step 3.
* That every k86MS2 row is admitted under K3gB5g. Rows the new kill removes are dropped at admission, and the K.log reports it.
