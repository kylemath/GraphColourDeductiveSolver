# maclane v2e: eng_p8 (payer-8/9 EDGE keys) for the upper lane, and k86MK3 = K3l5n + 268 keys

**Why.** The Studio cannot run k86MK3 = K3l5n + the 260 keys + W6b's 8 payer-8 keys (`cg_keys_v2_bbvariants.txt`, e1068fe3) on its
v2d / v2d1 install. Every lane command runs eng_p1r, and eng_p1r's gkwin stops at startup on a payer set beyond {5, 6, 7}
(`edge56.py`: `assert ... 'gkwin: a payer set beyond {5, 6, 7} ...'`). It refuses the keys loudly; it never misreads them. The
container's eng_p8 (PAYER8SPEC W5, validated 9 Nov: P8OK edge56 c1d18662, leaf 17307d6b) handles them. v2e brings it to the Mac.

**What changes.** With `ENG` unset every command runs on eng_p1r exactly as before. In the mock Studio tree the default dry-run output
of launch_msfam.sh was byte-identical before and after v2e, on the 240 and on the 260 keys.
- **`eng_p8/`** (new engine dir, made by install_v2e.sh) = a copy of the installed eng_p1r (`*.py`, `*.cpp`) plus:
  - `edge56.py` and `p1r.py` from the container's eng_p8. The pack's eng_p1r copies of both equal the container's eng_p1r, so these
    are the container's p8 changes and nothing else.
  - `pcheck.py` = the pack's eng_p1r pcheck.py + the one p8 line (`'p8reftest': cmd_p8reftest`). The container's own pcheck.py is not
    shipped: the pack's eng_p1r predates its sepmax / warmcache changes (pcheck, prelay, prelay2, pslite, psolve differ, as the
    k5e add-on already noted for prelay2).
  - `w6b_p8_ref.py` (W6b's independent reference, 8ec38208) and `jsepf_gk_k192s_p8.cpp` (the container's p8 leaf, 17307d6b:
    the gkin payer mask takes 5..9, and the d = 7 leaf credits payers 8 / 9).
  - `prelay2.py` from eng_p1t (the k5e copy with the "senders need t >=" line the tightener reads), so eng_p8 also serves as the
    tighten engine.
  - `ENG_P8.md5` lists all 29 files. install_v2e.sh and smoke_v2e.sh check the dir against it.
- **`build_v2e.sh`**: the pack's compile line (clang++ on the Mac). It builds `eng_p8/bin/jsepf_gk_k192` from the p8 leaf;
  `eng_p8/bin/jsepf_gk` is the same binary (in the container's eng_p8/bin, jsepf_gk, jsepf_gk_k192 and jsepf_gk_k192s are one
  build); and it builds `jsep3`.
- **`ENG=eng_p8`** on `launch_msfam.sh` passes the engine to the K run (`p1r/runK86p.sh`, which now reads `ENG`), the in-point watch
  (`ENGD`), the ladder (`REPL_ENGD`) and the tightener (`TIGHT_ENG`, so its U86e checks get `E86OVR=eng_p8`). The same knob on
  `recheck_fam.sh` sets `E86OVR`. `recheck_fam.sh` also gains `DRY=1`.
  A key file with payer-8/9 keys run without `ENG=eng_p8` is refused up front with a clear message (`k5e_lib.py keyseng`).
  ENG accepts only eng_p1r or eng_p8.
- **`k5e_lib.py`**: `cg_keys_r13w16_16fikp_p8bb.txt` b5875bfe is a known key file with label `_k268`, so points file as
  `K3l5n_k268` / `K3gB5n_k268`. Its new `keyseng` command reports which engine a key file needs. fam_lib.py and outbox86_fam.py
  are unchanged; they read KNOWN / KLABEL.
- **`smoke_v2e.sh`** + `ref/` (the 30 test keys and the amended MK1 in23 point): the container's tests on the Mac's own clang
  build: p8reftest, gkwintest, F2B self-test on the 268 keys, and the planted control, which must FAIL. It writes smoke_v2e.ok;
  launch_msfam.sh does not require that file.
- **`p1r/cg_keys_r13w16_16fikp_p8bb.txt`** (new, 268 keys: 83 / 84 / 93 / 8 with payer 5 / 6 / 7 / 8) = the 260-key file
  (0470c459) + the 8 bb keys, with a header in the merged-file style.

**Tests (container, mock Studio tree).**
- The mock was rebuilt at /tmp/maclane-k86 by the add-ons' own installers, in this order: base 2fa853ec; relocate (488 files,
  0 bad); build.sh (g++); v2addon; k5d; k5e; k5g (fam e f g); fam h1 h i1 i j k l1 l2 l m n; v2b; v2c; v2d; v2d1; macshim2.
- The family packs go in chain order (h1 before h, i1 before i, l1 l2 before l). Alphabetical order is refused by install_fam
  ("BAD chain").
- End state: launch_msfam 0158680c, k5e_lib 839623aa, fam_lib 67daca90, recheck_fam 1bcbc07b. No other divergence.
- install_v2e.sh: dry run OK; installs; a rerun reports "already v2e".
  It refuses (exit 2) when v2d1 is absent and when a pack file has been edited.
- build_v2e.sh (g++): OK.
- `ENG_P8.md5` matches the installed eng_p8.
- Gated runs (oom_score_adj 900, the container's FIFO / slot gate), engine = the mock's eng_p8, family K3l5n:
  - `p8reftest`, 30 test keys (the 8 bb keys + every 12th of the 260, `ref/keys_p8bb_test.txt`), N = 1500: **PASS, 0 mismatches**.
    Nonzero reference coefficients at d = 7 / 8 / 9 / 10: 5664 / 4326 / 2981 / 3228; of these, 2590 / 4119 / 2729 / 2948 are on
    payer-8 keys.
  - `gkwintest`, same keys, N = 1500: **PASS, 0 failures**. At d = 10, 48 pairs are informational only, as in the container.
  - F2B self-test on the 268 keys, f2bself = 600, 2 threads:
    - Point `ref/sol_k86MK1_in23_p8bb_amt.json` = the container's sol_k86MK1_in23__K3l5j_k260 (e5231e6d) + amounts
      0.011 .. 0.0173 on the 8 bb keys.
    - **PASS.** max |python exact - C++ leaf| is 5e-13 at d = 7 and 8 and 4.99e-13 at d = 9; 272 / 261 / 137 arrangements were
      changed by the rules. The leaf is jsepf_gk_k192 (93 payer-7 keys).
  - Planted control `gkoplant` (WIN drops the sg = -1 W5 OUT term): **F2B-SELFTEST: FAIL as required.** At d = 8 the max is 0.2;
    d = 7 and 9 are unaffected.
  - `smoke_v2e.sh` in the mock: steps 0-3 OK (p8reftest 8 s, gkwintest 7 s, F2B self-test 200/d PASS in 167 s).
    Its step 4 was OOM-killed beside the container's 7.7 GB LP; its oom_score_adj of 900 made it the victim, as intended. The
    gated chain above covers that control.
- DRY launch_msfam with `ENG=eng_p8 KEYS=cg_keys_r13w16_16fikp_p8bb.txt PARALLEL=1 TAG=k86MK3 PREV_TAG=k86MK2 FAM_SUFFIX=n`:
  the plan prints `... (b5875bfe) on eng_p8`, points filed as `K3l5n_k268 / K3gB5n_k268`, and
  `would run: ENG=eng_p8 bash .../p1r/runK86p.sh 200 2 k86MK3 ...`, all on eng_p8.
- DRY recheck_fam with `ENG=eng_p8` and the 268 keys gives tag `F_<name>_K3l5n_k268` and `E86OVR=.../eng_p8`.
- The same commands without ENG are refused (exit 2). ENG=eng_v2 is refused too.
- The default ENG gives identical dry-run lines: launch_msfam on the 240 and the 260 keys was diffed before and after v2e.

**Studio commands.** H is this v2e folder; R=/tmp/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
```
DRY=1 bash $H/install_v2e.sh       # checks the pack, v2d1 (stop_fam 7d1a090f, status_fam c0966049, fam_lib 67daca90) and the old md5s
bash $H/install_v2e.sh             # launch_msfam 0158680c, recheck_fam 1bcbc07b, runK86p 6b3c9734, k5e_lib 839623aa -> v2e (*.pre_v2e); eng_p8/
bash $H/build_v2e.sh               # clang++, about 20 s: eng_p8/bin/{jsepf_gk_k192, jsepf_gk, jsep3}
bash $H/smoke_v2e.sh               # 5-15 min, must end SMOKE-V2E: PASS (the Mac's own clang build through the container's tests)
# MK2's best point: its lowest-t K3l5n_k260 point in outbox/upper (in-points sol_k86MK2_inNN, ladder sol_repK2MW_NN)
awk '$4=="K3l5n_k260" && $1 ~ /(k86MK2_in|repK2MW_)/ {print $2, $1}' $R/outbox/upper/POINTS.txt | sort -g | head -3
P=$R/outbox/upper/<name>.json      # the first line's name
ENG=eng_p8 KEYS=cg_keys_r13w16_16fikp_p8bb.txt bash $R/recheck_fam.sh n $P 2     # ~5 min: must be FEASIBLE on K3l5n + 268 keys here
DRY=1 ENG=eng_p8 KEYS=cg_keys_r13w16_16fikp_p8bb.txt PARALLEL=1 TAG=k86MK3 PREV_TAG=k86MK2 FAM_SUFFIX=n bash $N/launch_msfam.sh $P
ENG=eng_p8 KEYS=cg_keys_r13w16_16fikp_p8bb.txt PARALLEL=1 TAG=k86MK3 PREV_TAG=k86MK2 FAM_SUFFIX=n bash $N/launch_msfam.sh $P
bash $R/status_fam.sh k86MK3 ; bash $R/stop_fam.sh k86MK3     # name the tag (the default is the newest k86MS lane)
```
- k86MK3 runs beside MK2. Its warm set is MK2's warm list plus a snapshot of eng_p1r/rows_k86MK2.txt.
- MK3's knobs default to MK2's (UPPER_THREADS, MAXIT, REPL_PAR from run.log), so lower them if the Mac is loaded.
- Its points file as `<name>__K3l5n_k268`. They are uppers for K3l5n **with the 268 keys on eng_p8**: quote them with the key
  file b5875bfe, never as K3l5n_k260.
- MK3's own files are `eng_p8/rows_k86MK3.txt` and `eng_p8/sol_k86MK3_*`. A relaunch of MK3 needs `ENG=eng_p8` again; without
  it the 268 keys are refused.
- Running lanes are not touched: replaced scripts are moved into place atomically, and eng_p1r / eng_p1t are unchanged.
