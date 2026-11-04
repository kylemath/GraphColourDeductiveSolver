# job A3W (Opus / swarm Team A, the 7-5-5-5 diamond rows): Studio window sweep, rings 15–17 (4 Nov)

**Result: 0 D and 0 C in all 8,486 windows**, on both of Studio's engines where checked. Every one of the 14 dual rows is
"neither" at rings 15, 16 (plain windows) and 15–17 (apex windows, t = 7 and 8). **The best C leftover is 192 (|X| ≤ 4).** No near
miss. This agrees with the swarm (0 disagreements on their 286 records).

## Independence statement
- **Engines:** Studio's own binaries, nothing rebuilt: kc loop/kc/kc (07e79fae), dfast18 out/job52/dfast18 (07cb1e0b), cfast
  ../studio15/cfast (de59e72f).
- **Plain windows:** generated with the repo's loop/k45/win45.py, copied to win45.py. It is the same construction as the swarm's
  win45p.py; the only differences are the two path lines.
- **Apex windows:** generated with the swarm's gen.py + binder.py, as Opus asked. They were run on a local copy whose only change is
  binder.py's W path (apex/binder.diff).
- **Driver:** drive_A3W.py, Studio's.
- **Not opened:** Opus engine code and Team B material.
- **Inputs** (in/, all md5 = MD5SUMS.txt):
  - f413aa1a ext_handoff_nov3/a3diamond/;
  - the R3A2 generator from 1ccb5da4;
  - the swarm verdicts res.jsonl, 19368003 (e50761a1), used only for the comparison.

## Windows
**Plain:** the 14 rows of a3_rows.json, at RMAX 16, rings 15–16. That is 6,604 row-windows, or **4,724 unique**: 2,294 at ring 15
and 2,430 at ring 16 (windows_r15r16.txt; window_rows.json maps each window to its rows).

**Apex:** windows containing the face apex t, at t = 7 and t = 8, at rings 15–17 (apex_windows_r15_17.txt).
| | ring 15 | ring 16 | ring 17 | total |
|---|---|---|---|---|
| t = 7 | 558 | 682 | 934 | 2,174 |
| t = 8 | 348 | 558 | 682 | 1,588 |
| all | | | | **3,762** |

## Protocol
- **Window run:** `kc -C -s 60 -t 600` on every window. A D would go to dfast18 and a C to `cfast --fixed {kc X}`; neither was ever
  triggered.
- **Order:** the apex windows ran before the last 719 plain ring-16 windows, as asked.
- **kc INCOMPLETE at t600:** 0.
- **Second engine (cfast D check):** run on a random sample of **300 windows** (seed 2026): 75 plain ring 15, 75 plain ring 16, and
  150 apex (29 at ring 15, 54 at 16, 67 at 17). **All 300 are D=false.**
  - The swarm's 285 were excluded from the sample.
  - cfast was not run on all 8,486, because of time (rings 16–17).
- **kcf for |X| ≥ 5:** not run. The best |X| ≤ 4 leftover is 192, far from 0. The swarm reports that |X| ≤ 6 on their 20 best changed
  nothing.

## Results by row (summary.txt has every per-ring count). All windows are "neither".
| row | d | LK | SV | dual mass | plain r15 / r16 | apex t7 r15 / 16 / 17 | apex t8 r15 / 16 / 17 |
|---|---|---|---|---|---|---|---|
| 0 | 8 | 77655556 | 65758586 | 0.0193 | 437 / 454 | 51 / 73 / 133 | 23 / 51 / 73 |
| 1 | 7 | 6667655 | 7776756 | 0.0383 | 238 / 210 | 35 / 43 / 70 | 33 / 35 / 43 |
| 2 | 7 | 6667655 | 7876756 | 0.0084 | 197 / 199 | 33 / 35 / 63 | 33 / 33 / 35 |
| 3 | 7 | 7666556 | 7676586 | 0.0055 | 255 / 196 | 40 / 46 / 65 | 21 / 40 / 46 |
| 4 | 7 | 7666556 | 8876576 | 0.0019 | 159 / 204 | 33 / 31 / 33 | 33 / 33 / 31 |
| 5 | 7 | 7655666 | 7657686 | 0.0017 | 221 / 201 | 28 / 52 / 65 | 36 / 28 / 52 |
| 6 | 7 | 7665566 | 6765776 | 0.1388 | 196 / 231 | 60 / 52 / 64 | 13 / 60 / 52 |
| 7 | 7 | 7665566 | 7765766 | 0.0557 | 224 / 234 | 48 / 55 / 53 | 24 / 48 / 55 |
| 8 | 7 | 7665566 | 6765766 | 0.0170 | 246 / 227 | 52 / 66 / 72 | 25 / 52 / 66 |
| 9 | 7 | 7665566 | 7765767 | 0.0131 | 245 / 188 | 39 / 39 / 57 | 24 / 39 / 39 |
| 10 | 7 | 7665566 | 7795676 | 0.0012 | 171 / 229 | 31 / 29 / 61 | 16 / 31 / 29 |
| 11 | 7 | 7665566 | 6785687 | 0.0005 | 194 / 181 | 33 / 46 / 44 | 12 / 33 / 46 |
| 12 | 7 | 7655667 | 7657656 | 0.0134 | 295 / 263 | 48 / 50 / 84 | 29 / 48 / 50 |
| 13 | 7 | 7665567 | 7765756 | 0.0019 | 255 / 254 | 27 / 65 / 70 | 26 / 27 / 65 |

**Best C leftovers (kc, |X| ≤ 4):**
- 192: a8_u.7655556_.57585.. (plain, ring 15) and t7_8_77655556_65758586_s1s2s3s4s5tuw2w3w4w5w6w7 (apex, ring 15);
- then 216, 224 and 240.

All of these are in row 0 (d = 8).

## Comparison with the swarm
- **res.jsonl (19368003):** 286 records, all matched to ours by name. **0 verdict disagreements** (all neither in both).
  - The leftover number differs in 267 of the 286. kc's best-X search is heuristic and time-sliced, so the best leftover found is not
    a fixed quantity. The swarm's smallest is 298; ours is 192.
- **r15.kc:** all 157 of the swarm's ring-15 windows are in ours, and all are neither in our run.
- **Apex windows, t = 7 logs:** the swarm's two files hold 43 and 98 names. All of them are among ours (202 and 304), with 0 of
  theirs missing.

## Files
| file | contents |
|---|---|
| kc.tsv | plain window kc results |
| apex_kc.tsv | apex window kc results |
| cfd.tsv | cfast sample results |
| summary.txt | summary and per-ring counts |
| windows_r15r16.txt, apex_windows_r15_17.txt, cfd_sample.txt | window lists |
| win45.py, apex/ | generators and the binder.diff |
| drive_A3W.py | driver |
