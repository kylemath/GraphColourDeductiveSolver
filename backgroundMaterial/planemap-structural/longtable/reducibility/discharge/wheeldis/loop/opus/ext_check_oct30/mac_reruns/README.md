Two-engine re-runs for the Mac Studio. 16,982 jobs over 12,700 configs (cfD 11,153, kcD 4,140, cfC 1,547, kcC 142).
Run: python3 mac_run_queue.py ./kc ./cfast remaining_jobs.txt configs.in X.txt out.tsv K N   (shard K of N)
Build kc from loop/kc/kc.cpp and cfast from studio15/cfast.cpp with c++ -O2 -std=c++17.
Priority: kc on nl51 rings 15-18, then cfast on rsst/A83. A row passes if D=true, or C-REDUCIBLE with leftover 0 under the listed X.
See REDUC_REPORT.md. Verdict rule: only rows with a fresh two-engine pass count for the "own rules only" claim.
