# REBUILD of /tmp/swarm-W17 at ~/swarm-W17 (10 Nov 2026)

Reason: reboot ~20:28Z 10 Nov wiped /tmp. Rebuilt at ~/swarm-W17 (persistent); /tmp/swarm-W17 -> /Users/kylemathewson/swarm-W17 symlink.
Started 20:50Z. Rules: spec-only (no Opus engine / W6b / W6r code read); no installs; nice 15; no commits.

## Step 1 (20:50Z): base macpack + rpatN add-ons
- ext_handoff_nov3/w17macpack/ is not in this worktree's HEAD; it is on branch origin/claude/project-thread-phexa1.
  Extracted with `git show 94e6525bb:ext_handoff_nov3/w17macpack/<f>` into ~/swarm-W17/_src/macpack/:
  w17_macpack.tar.gz 8acb1a22 (OK), macpack_addon_rpatN.tar.gz 2b2f18cc, macpack_addon_rpatN_v2.tar.gz f6dc32d3, 3 READMEs.
- Unpacked base, then addon v1, then addon v2, in a scratch dir; moved contents to ~/swarm-W17.
- MANIFEST.md5: all OK except code_gk7/run17.sh and w17_upper.sh (replaced by the add-on, as intended).
  MANIFEST_addon_rpatN.md5: all OK except README_addon_rpatN.md (v2 README, intended); w17_upper.sh = affae80f (v2).
- ln -s /Users/kylemathewson/swarm-W17 /tmp/swarm-W17.
- Python: /usr/bin/python3 3.9.6, numpy 2.0.2, scipy 1.13.1 (already present).

## Step 2 (20:55Z): code_gk8, code_gk9, check8.sh, check9.sh
- Consistency check first: reverse-applied W/out/job_ST88/code_gk8.diff to the committed code_gk8 (and to check8.sh) in _src/rev:
  all 17 code_gk7 files and check.sh come out byte-identical to the macpack + v2 add-on tree. So code_gk7/check.sh as unpacked = the pre-reboot code_gk7.
- cp -Rp W/out/job_ST88/code_gk8 + check8.sh; cp -Rp W/out/job_ST108/code_gk9 (19 files) + check9.sh. All md5 = the jobs' MD5SUMS.

## Step 3 (20:57Z): data files
- tab/rules_A5final_2db75746.json: `git show 338ac11c0:ext_handoff_nov3/w18/a5final/rules_c67fa1d1_plus_A5_twins.json` = 2db75746cbf4... (also = the copy in ~/maclane/maclane-k86 .../rules/A5final/). Also copied as tab/rules_c67fa1d1_plus_A5_twins.json (2 old scripts use that name).
- tab/cg_keys_r13w16_16fik.txt (240) from W/out/job_ST48/in/ = 3d996dbb.
- tab/cg_keys_r13w16_16fikp.txt (260) from W/out/maclane/setup_260/ = 0470c459.
- tab/cg_keys_r13w16_16fikp_p8bb.txt (268) from ~/maclane/dl_v2e/ = b5875bfe (same bytes in maclane-k86 .../p1r/).
- tab/cg_keys_w6b16x_hatbb.txt from W/out/job_ST108/in/ = b9ff66bd.
- tab/rpatN3_rotation_justified.txt from the add-on = 8b90a842.
- older key/rule files (for old scripts, md5 = the md5 printed in their committed run logs): cg_keys_r13w16.txt 15c361a1 (maclane-k86 .../s85_edge56/keys/),
  cg_keys_r13w16_16fikpq.txt 7ad4bf1f (~/maclane/dl_gs14), cg_keys_GS20_nonzero.txt c8349589 (job_ST95/in), cg_keys_GS20in03_nonzero.txt 38ba0140 (job_ST99/in),
  cg_keys_GS21_nonzero.txt e948c682 (job_ST108/point), rules_studio_keep95p131f_W18strict.json c67fa1d1 (loop/studio/opus_check/f2b041/keep95p131f/w18_428/in).
- kill/patched298 from the base pack: U7 b493a0ce, U8 = U9 618eb300 (MD5 file OK).
- pat/K3/ (37 files): K3..K3l (12) from the staged ext_handoff_nov3/k86{KS,MS,CS,FS}/ commits (git show of the last commit of each path); each = the same-name file in
  maclane-k86 .../s86_f2b7/w13/. K3l5, K3l5e/g/h/i, K3gB5i from W/out/job_K3l5*/ and job_K3gB5i/; K3l5j..v from W/out/maclane/setup_k5{j..v}/.
- args_A97F_W13K3{,b,c,c_noC,d,e,f,i,j,k,l}_x_studio.txt from the same staged commits (K3l = f90ed3dc, as job_K3l5/NOTE.md records);
  args K3l5, K3l5e/g/h/i, K3gB5i from the job dirs; K3gB5k from setup_260; K3l5{j..v} and K3gB5{l..v} from setup_k5*. (44 args files)
- MD5SUMS check: 39 files OK against their dirs' MD5SUMS, 0 bad. Dirs without MD5SUMS: job_K3l5h, job_K3l5i, setup_k5s/t/u/v (bytes as committed;
  K3l5v 21f30585 / K3gB5v fe41165a match commit 7458959d1's message). Every pat=/cpat=/rpat= path in every args file exists (script in _src/install_fam.sh, log _src/install_fam.log).

## Step 4 (20:58Z): build (nice 15)
- `nice -n 15 bash build.sh` (sep3, sep3f, sep3r, sep3r_ak, sep3r_gk7) + `nice -n 15 clang++ -std=c++17 -O3` code_gk8 -> wd/bin/sep3r_gk8, code_gk9 -> wd/bin/sep3r_gk9. 0 warnings. Apple clang 17.0.0.
- sep3r_gk8 849b8884e3480030f8e052e26320c2b9 = job_ST88/sep3r_gk8.md5 (MATCH); sep3r_gk9 23ef75a52ff835078b5f2cad8add30a1 = job_ST108/sep3r_gk9.md5 (MATCH). Build is deterministic.
- sep3r_gk7 73d3f825694badc9cd35f6461c6712da (no recorded md5 found to compare), sep3 = sep3f e68d0dbd, sep3r 169b2216, sep3r_ak 85bb30a3.

## Step 5 (20:59Z): gate 1 launched (ST-115 point, throwaway NN 9115)
- Scratch script gate/autost_mk6nz_nocommit.sh = W/out/maclane/autost_mk6nz.sh with: J -> ~/swarm-W17/gate/job_ST9115 (nothing written in the repo),
  the run_autost cp / MD5SUMS / git add+commit+push lines deleted, NPROC 6 -> 4 (load; NPROC does not change the parts). Run with nohup; output gate/gate1_9115.out.
- Note: the code resolves /tmp/swarm-W17 to /Users/kylemathewson/swarm-W17 in its header lines (was /private/tmp/swarm-W17); cosmetic.
- Key filter: "keys loaded 112 dropped 148 payer-8/9 0 missing-from-file 0 refused 0" (recorded run: 112 keys).
- 21:00:45Z gate 1 main Python step done (1 min): p0.log already equals the recorded main.out on kill md5s, GK 112 keys cbedc9d9, senderR2 22496 violated 0 min slack 1.39e-08,
  D 18154 / C 712 / RPAT 158 (same by-d counts), F2B rules 2db75746, self-tests 0 mismatches (same compared counts 5430 / 8785), DP margin -1.02167, Karp lambda 0.749720579. Separator running.
- 21:20:01Z gate 1 main done (20 min wall at NPROC 4): RESULT FEASIBLE. diff of main.out vs W/out/job_ST115/main.out, after normalising paths
  (/Users/kylemathewson/swarm-W17 and /private/tmp/swarm-W17 -> /tmp/swarm-W17, ST9115 -> ST115), clock times, CPU seconds and the runtime-estimate wording:
  the only differing line is the header's "6 processes" vs "4 processes". Everything else is identical, line for line. tneg running.
- Watcher note: `pgrep -f autost_mk6nz_nocommit` also matched the watcher shells themselves; those watchers were stopped and replaced with a file-based wait.
- 21:41:07Z gate 1 tneg done: RESULT INFEASIBLE, d7 98 / d8 323 / d9 12, senderR2 violated 181. tneg.out identical to W/out/job_ST115/tneg.out after the same normalisation
  (incl. process count); tneg_receiver_violators.txt byte-identical (cmp); in/keys_nonzero.txt = cbedc9d9 = the recorded one. GATE 1 PASS.

## Step 6 (21:42Z): gate 2 launched (gk9: ST-108 GS21 point)
- sol/sol_k86GS21_in02.json from W/out/job_ST108/point/ (2d6c1779). Scratch gate/run_gs21_scratch.sh = job_ST108/point/run_gs21.sh with J -> ~/swarm-W17/gate/gs21 (nothing else changed; NPROC 4 as recorded).
- 22:33Z gate 2 done (51 min wall, NPROC 4): main RESULT FEASIBLE at t 0.013963963437 (DP margin -1.61945, Karp 0.728008717); tneg RESULT INFEASIBLE d7 24 / d8 52 / d9 0.
  main_K3gB5n.out and tneg_K3gB5n.out are IDENTICAL to W/out/job_ST108/point/ after normalising paths, clock times and CPU seconds (same NPROC, so no other difference);
  tneg_K3gB5n_receiver_violators.txt byte-identical. This exercises gk9 + sep3r_gk9 with payer-8 and HATBB keys. GATE 2 PASS.

## Step 7 (22:35Z): manifest
- MANIFEST_rebuild.md5 (md5 -r of every file except logs/, st16/, q/, gate/, _src/): 543 files.
- Left in place from the gates: tab/keys_ST9115.txt, sol/sol_k86MK6_in04_tight__K3l5r_k260{,_tneg}.json, sol/sol_k86GS21_in02{,_tneg}.json,
  logs/ and st16/ for the four gate TAGs (same TAGs as the original ST-115 / ST-108 runs; the old ones were lost with /tmp). Delete if unwanted.
- Not restored (referenced only by old, finished scripts; not found anywhere in the repo or ~): tab/A97F_111keys.txt, args_k95f.txt.
  Also not restored: per-job artefacts in the old /tmp tree (st*.done markers, st*_main.out, old logs/ and st16/ caches, old sol/ points other than the gate ones).
Finished 22:36Z. Total about 1 h 46 min (20:50Z-22:36Z), of which about 1 h 30 min was the gate runs.
