# XR: outside-check re-runs (Opus, a1d13173 loop/opus/ext_check_oct30/mac_reruns), Studio engines

- **Inputs** (in/, byte copies, md5 = MD5SUMS.txt):
  - remaining_jobs.txt e85a4d0c (16,982 jobs);
  - configs.in 918e6701 (12,700 configs);
  - X.txt 2feb6cac;
  - mac_run_queue.py c291094b.
- **Engines:** our existing binaries, not rebuilt:
  - kc = loop/kc/kc (md5 07e79fae);
  - cfast = ../studio15/cfast (md5 de59e72f).
- **Runner:** run_queue_t600.py is mac_run_queue.py with exactly one change, `-t 600` on the two kc commands (kc's own stop flag,
  which prints INCOMPLETE). The flags are therefore:
  - kcD: `kc -t 600 {cfg}`
  - kcC: `kc -t 600 -C -x {X} {cfg}`
  - cfD: `cfast {cfg}` (no timeout)
  - cfC: `cfast {cfg} --fixed {X}` (no timeout)
- **Dispatcher audit** (read in full before running):
  - It calls only the two binaries.
  - It makes no network or git calls.
  - Besides the results tsv it writes per-shard temporary inputs (`<tsv>.in<k>`, `<tsv>.in<k>.x`). They are not committed.
- **Priority split** (jobs_p*.txt, made by Studio from remaining_jobs.txt):
  - P1: nl kcD, 3,906 jobs (rings 14-18);
  - P2: f kcD + kcC, 376 jobs (the k3x A83 rows);
  - P3: all cfD + cfC, 12,700 jobs.
  - The union is exactly the 16,982 jobs.
  - 12 shards (drive.sh k = 0..11, i mod 12), each running P1, P2, P3 in order at nice 10.
- **Pass rule:** D=true for kcD/cfD; for kcC/cfC, C-REDUCIBLE with leftover 0 under the listed X, and not INCOMPLETE (summarize.py).
