# K-3 ring-15 batches for the Mac (W13b, 7 Nov 2026)

These are the ring-15 windows of the 110 BINDING rows that still have no kill. The rows come from Opus `s86_k86PS/BINDING.md`, `viol_P_crep_q.txt` and `viol_P_q53A97q.txt`, 244 canonical rows in all.

- **Already handled elsewhere.** The other 134 rows (the d = 8 classes 56568567, 56568568 and 56568569) are killed by the container's ring-13 D hit (see `../REPORT.md`). The container screens ring <= 14 itself.
- **Order.** Windows are in value order: a window shared by more uncovered excess comes first. Batch 01 holds the most valuable windows.
- **Skipped windows.** None of these windows has been screened by W13, KS5 or the container.
- **Where the windows come from.** Every window is taken from the realised 2-ball picture of a row (centre at its exact degree d, link, apexes). It is rotation-correct by construction.
- **9 letters.** 9 means 9+, so 9-vertices are never inside a window.

## Engines (the same pipeline as KS5)

| step | what runs | what counts |
|---|---|---|
| 1 | `kc -C FILE` | D closure first; if not D, it searches for X with |X| <= 4 |
| 2, D windows | `dfast18 FILE`, plus `dfast FILE` if present | D=true |
| 2, C windows | `cfast FILE --fixed X`, with kc's X | C-REDUCIBLE |

- FILE holds one kc line. Binaries are passed as `KC`, `DF18`, `CF` (and optionally `DF`).
- `mscreen.py` needs python3 (standard library only). It is KS5's screener plus an optional `SKIP` file of codes to leave out.
- The per-call timeout is `TO`, 1500 s by default.

## Run (macOS bash 3.2 safe)

```
cd round6/W13-open-row-kills/round6/K3/mac
shasum -a 256 -c SHA256SUMS
KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runk3.sh 10
```

- runk3.sh runs every famK3_r15_*.tsv in name order, 10 at a time, at nice 20, one core each.
- If fewer cores are free, run fewer at a time (`bash runk3.sh 4`). Name order is priority order.
- To run one batch:

```
mkdir -p results
KC=/path/kc DF18=/path/dfast18 CF=/path/cfast SKIP=$PWD/skip_k3.txt nice -n 20 python3 mscreen.py famK3_r15_01.tsv results/res_K3_r15_01.tsv >> results/log_r15_01.txt 2>&1
```

- **Skip list.** `skip_k3.txt` lists codes whose BINDING rows have all been killed since packaging. W13b refreshes it as container kills land. It is read when a batch starts, so restarting a batch (same command; it resumes) picks up a newer list. runk3.sh uses it automatically.
- **KS5 timeouts (optional, low priority).** `famK3_timeouts.tsv` (md5 98d7c14093cda1ca61c8737daa2e0b01) holds the 7 KS5 windows that timed out at 1500 s. None of them is in a BINDING row. To give them up to 6 h per call: `TO=21600 nice -n 20 python3 mscreen.py famK3_timeouts.tsv results/res_K3_timeouts.tsv >> results/log_timeouts.txt 2>&1`.
- **Send back** `results/` (res_K3_*.tsv and logs) into `round6/W13-open-row-kills/round6/K3/mac/results/`. A batch is finished when its log ends with `COMPLETE n`.

## Batches

The container estimate is W13's mean seconds per window by (ring, m). The Mac ran KS5 at about 0.45 times this while it had free cores, and about 2.3 times while the 8-core Studio check ran alongside.

| file | md5 | windows | ring | est. container h | value (excess) | classes (windows) |
|---|---|---:|---|---:|---|---|
| famK3_r15_01.tsv | 60674f0378ef8208ccd0d136662f6272 | 1074 | 15 | 3.92 | 1.5096 to 0.1531 | d9 839, d7 210, d8 25 |
| famK3_r15_02.tsv | b1c266f921397fa31a924b1c02a15196 | 1340 | 15 | 3.92 | 0.1531 to 0.0964 | d9 698, d8 594, d7 48 |
| famK3_r15_03.tsv | c3b1a79445a30ffdae8d674fc2572cea | 1108 | 15 | 3.92 | 0.0964 to 0.0772 | d9 690, d8 392, d7 26 |
| famK3_r15_04.tsv | 3aeaa6be99a57adee683f242b8ecae6b | 1301 | 15 | 3.92 | 0.0772 to 0.0503 | d8 657, d9 345, d7 299 |
| famK3_r15_05.tsv | 1370fe04ab5c45901709332bd3552c53 | 978 | 15 | 3.92 | 0.0503 to 0.0413 | d8 421, d7 374, d9 183 |
| famK3_r15_06.tsv | 937cd8284b4a2240d122ae20d928d98d | 1126 | 15 | 3.92 | 0.0413 to 0.0413 | d9 1126 |
| famK3_r15_07.tsv | 2491a89c079de1a530270acff058b4db | 1163 | 15 | 3.92 | 0.0413 to 0.0350 | d9 954, d8 207, d7 2 |
| famK3_r15_08.tsv | 995cf86f7588e490581a591beb2c3094 | 1265 | 15 | 3.92 | 0.0350 to 0.0219 | d7 923, d8 272, d9 70 |
| famK3_r15_09.tsv | 350cbd408aa4a5cfbc8112dcc65592ec | 1150 | 15 | 3.92 | 0.0219 to 0.0192 | d9 936, d7 155, d8 59 |
| famK3_r15_10.tsv | f6826856f247c0f4564aa225f87d515c | 1322 | 15 | 3.92 | 0.0192 to 0.0029 | d8 616, d7 487, d9 219 |
| **total** | | **11,827** | | **39.2** | | |

That is about 18 Mac core-hours at free-core speed, so about 2 h of wall time on 10 cores.
