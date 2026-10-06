# J3: the audit's WP20 P1 replay, route A, on the Mac Studio

The audit writes the verdict; this README only records what was run.

- Route: A (the audit's compare_p1.py on the transferred first-Mac P1 output).
- Machine: Kyles-Mac-Studio.local, Apple M4 Max, Python 3.9.6.
- Code: detached worktree ~/studio-scratch/main-wt at origin/main 46c843e (contains the audit commit b8bea9b), with LT=backgroundMaterial/planemap-structural/longtable. The coordinator approved this in place of fast-forwarding the studio-wp21 checkout.
- Input: origin/transfer-p1 wp20/P1-m5-25.json.gz, gunzipped to ~/studio-scratch/p1audit/P1-m5-25.json.
- sha256 checks before the run (`shasums.txt`): P1-m5-25.json e68c44a3..., input-m5-25.txt 92e482ed...d989, wp20_audit.py d0fc8759..., compare_p1.py 511cf77e..., WP20-D1-declaration.md 8758a9f8..., d1_confirm.py bb350d3b..., d1_check.py 98c6bcf7.... All are as announced.
- Command, run from the worktree root, detached via wp_launch.py (`run_j3.sh`):
  `( ulimit -t 7200; LONGTABLE_DIR="$LT" nice -n 10 python3 $LT/audit/wp20-replay/compare_p1.py ~/studio-scratch/p1audit/P1-m5-25.json $LT/wp20/input-m5-25.txt --workers 2 --out "$OUT" ) 2>&1 | tee "$OUT/run.log"`
- Times (`times.txt`): start 2026-10-06 14:14:44 MDT, end 14:53:25 MDT, exit 0.
- Outputs, verbatim: `compare-result.json`, `run.log`.
