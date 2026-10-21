# Kill hunt handoff (paused by k, 21 Oct 2026 ~21:07Z)

Result: no KILL_D, KILL_C or FZERO line from any machine. All finished windows were `D=false C=false` (valid non-kills).
The queue was far from finished; every kc/kcf job is stopped.

| Machine | Work | Done | Notes |
|---|---|---|---|
| Local (this thread) | r63d_1 1-115, others | 115+63+12+12 (kc), 20 kcf | 0 kills |
| Box A | slice_A, r63d_2 | 2 + 4 | 318 + 230 unstarted; copies in /mnt/project-files/farm63/A/ |
| Box B | slice_B (275) | 9 | 266 unstarted |
| Box C | r64c_r16 (276), earlier 9 | 161 + 9 | 115 unfinished |
| Box D | 167 | 23 | 144 never run |
| Box E | f_02+f_03 (80); c17_02+03 (235) | 80; 7 | 228 ring-17 unfinished |
| Box F | r63j ring-16 reversed (312) | 171 at 20:57Z | c17_01 never started |
| Studio (Mac) | s5 kcf over k47c (622) | 113 | 0 FZERO, 0 kills, 0 timeouts; 509 unfinished listed in out/job_F63/s5/unfinished_s5.txt (commit 9be448b5 on main); s1,s2,s3,s6,s4 never started; k47d stopped at 313/391 |

Unfinished queues, ready to resume: farm63/q/ (s1..s6, c17_00..05, c_gr; MD5SUMS) plus
/mnt/project-files/explore/todo63/ (win52_* r64e, r64f low priority).
Resume with farm63/work.sh (kc) or run_bin.py (prebuilt binary); kcf pass for k47c is q/s5. Results are keyed by window name.
Kills remain candidates only: explore and Long Table admit, two engines needed.
