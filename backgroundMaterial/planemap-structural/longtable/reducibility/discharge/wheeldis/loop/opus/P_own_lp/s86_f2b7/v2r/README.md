# s86 v2r: KEYSPEC v2 receiver rows on d = 7 / 8 as realisation rows (flag `v2r`)

Spec: W6b `KEYSPEC2_RECEIVER.md` (md5 d5a6734b) section 3.1 (the exact max-row), sections 1, 2, 4, 5. Row format for replays:
`V2ROW_SPEC.md` (this folder). Running log with all test numbers: `NOTES.md`.
Engine: `s86_f2b7/eng_v2`, a copy of `s86_f2b7/eng_p1r` (md5s at copy time: `eng_md5_at_copy.txt`; eng_p1r was not edited).

## What changes under `v2r`

* A d = 7 / 8 receiver (link w, apex s) is the max-row  max over rho of value(rho; x) <= d - 6 + t.  The LP holds it as linear
  realisation rows `('receiverV2', d, link, apex, rho)`: value(rho; x) - t <= d - 6, one per realisation met so far.
  rho = x_0 y_0 ... x_{d-1} y_{d-1}, x_j = w_j's private next to s_j, y_j = next to s_{j-1}; domains = p1r_domains (the masked row's
  own envelope ranges).  value = fixed (masked row minus its M / Q / lQ entries) + each group's copy (h / q + lq) + per key
  IN(K; rho) - OUT(K) (exact picture).  Integer coefficients; `v2r_row(d, link, apex, rho)` rebuilds a row from its id alone.
* No masked d = 7 / 8 receiver row is ever built (it is stronger than the v2 row); lowerR2 rejects one in a v2r cert.
  d >= 9 receivers (gkwin window), senders, cons2, mrows and all separators are unchanged.
* Separation: the masked separators (jsepf leaf, window tables) list a superset of the v2-violated d = 7 / 8 receivers (their values
  are >= the v2 value pointwise), up to their top-K cap.  Each listed receiver gets an exact max-plus DP at the LP point
  (`v2r_dp`, 25-state sites round the d-cycle); its argmax row is added when it exceeds d - 6 + t by more than `v2tol` (1e-9).
  `v2rescan=k` (default 1): every k-th round, and always before the loop would stop, the DP re-checks every known d = 7 / 8 receiver
  not listed this round (phantoms, i.e. masked-violated but v2-satisfied receivers, can crowd the separators' top-K lists; the log
  says `CROWDED` when the cap was reached with phantoms).  Missing a violated receiver only lowers the lower bound (still valid).
* Seeding: every warm `R 7|8 ...` line gets its DP argmax row at the point `v2seed=` (a sol json, e.g. the k86GL5 phase-1 sol),
  x = 0 without it.  Warm `V2 d link apex rho` lines (written by a v2r run's rows file) add that exact realisation row.
* The rows file of a v2r run logs, per added row, `R d link apex` and `V2 d link apex rho`.

## Options / flags

| option | meaning |
|---|---|
| `v2r` | the model above (asserts the s86 family: gkeys gkwin gkleaf, f2b f2b7 q7 q7m l3q l3qV=7,8 filt16 apexcls) |
| `v2seed=<sol.json>` | seed point for the warm d = 7 / 8 receivers |
| `v2rescan=k` | DP re-scan of all known d = 7 / 8 receivers every k-th round (0 = only the separators' lists) |
| `v2inner=k` | (lext) after each phase-1 solve, up to k rounds of: DP on every known d = 7 / 8 receiver at the phase-1 point, add the violated argmax rows, warm phase-1 re-solve (new columns cost 0 in phase 1). Default 0. The restricted LP needed 17 cutting-plane rounds from the seed rows, so without it the lane needs ~17 lext iterations before the realisation rows settle. |
| `v2tol=` | violation tolerance of the DP (default 1e-9) |
| `v2bug=p1p2` | CONTROL ONLY: the row builder swaps every 7's two privates (a rebuild must fail) |

Commands (no LP family run): `v2rtest` (unit tests: W6b test vectors, DP vs p1r_core vs brute force on a cert's rows),
`v2restricted cert= v2mode=mask|p1r|v2|v2p1rkeys|v2curkeys [v2seed= v2out= v2json=]` (restricted LP on a cert's rows, realisation
rows added iteratively), `v2rshow v2rows=<file> v2show=<json>` (full decomposition of given rows; V2ROW_SPEC test vectors).

## Files

| file | change |
|---|---|
| `eng_v2/v2r.py` (new) | exec'd by `pcheck.py` after `p1r.py`. Without the flag it only defines functions and the three commands. |
| `eng_v2/prelay2.py` | solveR2: `recv` routes d = 7 / 8 to the DP (`v2recv`), warm `V2` lines, seed point, sepround DP on the separators' d = 7 / 8 lists + rescan, rows-file `V2` lines; lowerR2: `receiverV2` rows rebuilt by `v2r_row`, masked d = 7 / 8 receiver rows rejected under v2r. |
| `eng_v2/edge56.py` | dualexport: `receiverV2` rows (type, d, link, apex, rho, privates, ks = IN - OUT at rho); `meta['v2r']`. |
| `eng_v2/pcheck.py` | exec line for v2r.py; commands v2restricted, v2rtest, v2rshow. |
| `v2r/runK86v.sh`, `watchL86v.sh`, `wtest86v.sh`, `dualwatch86v.sh`, `bindwatch86v.sh`, `binding86v.py` | copies of the p1r scripts with eng_p1r -> eng_v2 (binding86v also counts receiverV2 rows). |
| `v2r/v2r_run.sh` | one memory-gated (MemAvailable >= 5 GB), nice 19 pcheck command on eng_v2 with the K3g / k86GL5 family flags; logs in `v2r/logs/`. |
| `v2r/rlp_queue.sh` | validation step 2: the restricted LPs one after another. |
| `../launch_k86GV1.sh` | the first v2 lext lane (K5a args, 16fik keys, GL6 flags + v2r). Not started. |
| `v2r/seed_sol_k86GL5_p1.json` | snapshot of eng_p1r/sol_k86GL5_p1.json (md5 e537d18d), the seed point of k86GV1. |
| `v2r/rlp/` | restricted-LP results (json) and dual certs (cert_rlp_<mode>.json, _exb.json from lowerR2). |
| `v2r/smoke/` | the two smoke runs' sols, rows files and certs (logs in `v2r/logs/smoke_GV1.log`, `smoke2_GV1.log`). |
| `v2r/spec_check.py` | re-derives the V2ROW_SPEC test vectors from the spec text alone (no engine): `python3 -I spec_check.py V2ROW_vectors.json <gkeys>`. |
| `v2r/V2ROW_vectors.json`, `V2ROW_vectors_rows.txt` | the 5 worked rows of V2ROW_SPEC.md (v2rshow output, md5 b4b3eed4) and their ids. |
| `v2r/lx_queue.sh`, `rest_queue.sh`, `smoke_queue.sh`, `smoke2_queue.sh` | the validation step 3 and smoke queues (memory-gated, one at a time). |
| `v2r/eng_md5_at_copy.txt` | md5s of eng_p1r at copy time. |
