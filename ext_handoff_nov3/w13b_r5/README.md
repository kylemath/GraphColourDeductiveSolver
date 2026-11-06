# K-2: window lists for the Mac (W13b, round 5, 6 Nov 2026)

There are 10 batches with 14,396 two-ball windows in all. None of them has been screened before. The Mac screens them; nothing here has been run on these windows yet.

- **r15_01 to r15_08 (5,702 windows):** ring 15 on the 42 receivers that resist through ring 14. These come from `round4/receivers_resist.tsv`: the 44 rows swept to ring 14 and not killed, minus 5566766/5676767 and 5557557/5776777, which K-1 runs in the container. The third K-1 row, 5677757/7656555, was killed in round 4, so it is not among the 44.
- **k85r14 (1,162 windows):** ring 14 on the 25 heaviest live d = 7 receivers of the k85CL certificate (`s85_k85CL/cert_p1_00_a7999c22_exb.json`) that W13 had not swept to ring 14. Here "live" means not already killed by W13's 115 patterns.
- **k85r13 (7,532 windows):** ring <= 13 on every live k85CL d = 7 receiver that W13 had never swept.

## Engines the Mac needs

| name | built from (sources in `round6/W13-open-row-kills/bin_src/`) | how it is called | output it must print |
|---|---|---|---|
| `kc` | kc.cpp (sha256 e6f7a6d8…) | `kc -C FILE` | `D=true` / `D=false`, and if not D: `C-REDUCIBLE X={..}` or `C=false … best X={..} leftover N` |
| `dfast18` | dfast18.cpp (sha256 23e14b64…) | `dfast18 FILE` | `D=true` / `D=false` |
| `cfast` | cfast.cpp (sha256 6c842fe4…) | `cfast FILE --fixed X` (X exactly as kc printed it, e.g. `I0-I1`) | `C-REDUCIBLE` or `fails` |
| `dfast` (optional) | dfast.cpp | `dfast FILE` (used only when ring <= 16) | `D=true` / `D=false` |
| `python3` | standard library only | runs `mscreen.py` | if it is missing, `mscreen.sh` (bash 3.2) does the same, but with no per-call timeout |

FILE holds one kc line: `name r m ringadj intadj`. Paths are not fixed; pass them in the environment as `KC`, `DF18`, `CF` and (optionally) `DF`.

## Engine sequence (identical for every batch; as in round 4, Checks)

For each window, in file order:

1. Run `kc -C`. It computes the D closure first. If the window is not D, it searches for a contraction X with |X| <= 4.
2. **D windows.** If kc says D, run `dfast18` on the same line, and `dfast` too when it is present. A D hit counts only with `dfast18:D`. [P-D] needs kc D plus dfast18 D.
3. **C windows.** If kc says C-REDUCIBLE, run `cfast FILE --fixed X` with kc's X. A C hit counts only with `cfast:C-REDUCIBLE`. [P-C] needs kc -C plus cfast --fixed with the same X.
4. **Everything else** is N.

The per-call timeout is `TO=1500` seconds. A window that times out is written as TIMEOUT and is not retried.

## Batches

The time estimate is the mean seconds per window by (ring, m) over W13's 19k screened windows. Those were measured on the swarm container: one core at nice 19, under load, with the confirmations included. A Mac core is probably as fast or faster. The weights are |w| with S+R+C = 1 in each certificate; x7 = W16 round-7 x7_SF_108 / x7_AF_108.

| batch file | md5 | windows | ring | receivers | weight x7_SF / x7_AF | weight k85CL | est. core-h | outputs (in `results/`) |
|---|---|---:|---|---|---|---|---:|---|
| famR5_r15_01.tsv | 8b9d102617eb580162225a40e7b9b503 | 742 | 15 | 5: union ranks 4-8 | .0695 / .0703 | .0060 | 1.79 | res_W13b_r15_01.tsv, log_r15_01.txt |
| famR5_r15_02.tsv | 106713cfab5318f4121ace5cf5993ccb | 712 | 15 | 5: ranks 9-13 | .0556 / .0542 | .0068 | 2.07 | res_W13b_r15_02.tsv, log_r15_02.txt |
| famR5_r15_03.tsv | ad28206253e75667fa32398b8c30fb43 | 836 | 15 | 5: ranks 14-19 | .0370 / .0378 | .0079 | 2.27 | res_W13b_r15_03.tsv, log_r15_03.txt |
| famR5_r15_04.tsv | 72d866da48cecf0cf74f58c155e22dd2 | 586 | 15 | 4: ranks 20-23 | .0177 / .0177 | 0 | 1.70 | res_W13b_r15_04.tsv, log_r15_04.txt |
| famR5_r15_05.tsv | 9e094420a14ac5a4ed01c890495e6e04 | 793 | 15 | 5: ranks 24-28 | .0185 / .0177 | .0062 | 2.17 | res_W13b_r15_05.tsv, log_r15_05.txt |
| famR5_r15_06.tsv | e1c850dab3d183b96dc3b50c2b357a05 | 577 | 15 | 7: ranks 29-36 | .0167 / .0174 | .0017 | 1.76 | res_W13b_r15_06.tsv, log_r15_06.txt |
| famR5_r15_07.tsv | 61873b6950b2a7fb5bcbb1cd5adfaa13 | 738 | 15 | 4: ranks 37-40 | .0073 / .0072 | .0011 | 2.17 | res_W13b_r15_07.tsv, log_r15_07.txt |
| famR5_r15_08.tsv | cc38971b05b8e07febb8884e805e3b83 | 718 | 15 | 7: ranks 41, 47, 63, 86, 110, 116, 124 | .0049 / .0043 | .0080 | 2.30 | res_W13b_r15_08.tsv, log_r15_08.txt |
| famR5_k85r14.tsv | 305cf28c86011a5d8df65a2d89fc94eb | 1,162 | 14 | 21 k85CL rows | – | .0496 | 0.97 | res_W13b_k85r14.tsv, log_k85r14.txt |
| famR5_k85r13.tsv | 4e97a8f2c6218b6185285a46d9124ba0 | 7,532 | 9-13 | 260 k85CL rows | – | .0717 | 1.85 | res_W13b_k85r13.tsv, log_k85r13.txt |
| **total** | | **14,396** | | | .227 / .227 | .121 | **19.1** | |

- On 10 cores this is one wave, about 2.3 h by the container estimate.
- On fewer cores, run them in this order: r15_01, r15_02, k85r14, r15_03, k85r13, r15_05, r15_08, r15_06, r15_07, r15_04.
- Each ring-15 batch holds whole receivers, heaviest first. A finished batch therefore closes ring 15 for every receiver in it.
- `receivers_r5.tsv` lists each receiver with its batch, window count and weights.

## Commands

Check the files first. On the Mac, run `shasum -a 256 -c SHA256SUMS`. On Linux, run `md5sum -c MD5SUMS`.

To run all 10 batches at nice 20, 10 at a time:

```
cd round5/mac
KC=/path/to/kc DF18=/path/to/dfast18 CF=/path/to/cfast [DF=/path/to/dfast] bash runall.sh 10
```

To run one batch (same for every tag; here r15_01):

```
mkdir -p results
KC=/path/to/kc DF18=/path/to/dfast18 CF=/path/to/cfast nice -n 20 python3 mscreen.py famR5_r15_01.tsv results/res_W13b_r15_01.tsv > results/log_r15_01.txt 2>&1
```

If python3 is missing, use `bash mscreen.sh` in its place with the same two arguments.

- **Resume.** To resume a batch after a stop, run the same command again. Windows already in the res file are skipped.
- **Time limit.** An optional third argument MAXSEC makes mscreen.py stop cleanly after that many seconds.
- **Done.** A batch is finished when the last line of its log is `COMPLETE n` and its res file has as many lines as the batch has windows.

**Send back** all of `results/`, the res files and the logs, into `round6/W13-open-row-kills/round5/mac/results/`. Each res line has W13's 12 columns: code, ring, m, name, verdict (N/D/C/TIMEOUT/ERROR), leftover, X, reached/classes, secs, family, confirm, kc line. Hits are also printed in the log as `HIT D|C ...`.

## What was skipped, and how

- **Window-level skip (W13's own skip logic).** A window is left out when its canonical code (`kcanon.code`, all rotations and reflections) is already in any W13 result file. That covers 19,342 codes from 25 res files: work/res_*.tsv plus the B1 results. Every one of the 2,291 windows of K-1's `famR4_R15top3.tsv` is also left out, because K-1 screens those. Batch files share no code.
- **Sweep registry.** W13's rounds 2-4 swept 336 canonical receivers: 65 to ring 14 and 271 to ring 13. All ring <= 14 windows of the 42 ring-15 receivers were already screened, which checks the registry.
- **k85CL letters.** Letters 5-8 are exact; 9 means 9+ and is never exact. 9-vertices are kept out of every window. With them left out, the window set is the same for degree 9, 10 and 11 (checked on 4 rows), so each window is valid for 9+. Exact-8 vertices are allowed; 3,847 of the k85 windows contain one.
- **k85CL receivers already dead.** 61 of the 504 d = 7 receivers, |w| 0.0613, are killed by W13's existing 115 patterns. That is mapping only [M], with letters over the 14 images. So the k85CL stack evidently does not load them (inferred from the row list; worth confirming with Opus). These rows get no windows. Among them are k85CL ranks 1-4: 5556677/7577757, 5757677/5557755, 7577575/7755755 and 5677757/7656555.
- **Live k85CL receivers.** There are 443, |w| 0.2144: 368 never swept (0.1079), 52 at ring 13 (0.0579) and 23 at ring 14 (0.0486).
  - The ring-14 set is the 25 heaviest live rows not at ring 14 (|w| 0.0579, k85CL ranks 8-50). Four of them (ranks 22, 30, 36, 47) add no window of their own. Each of their ring-14 windows is either already screened or listed under a heavier receiver of the set. That is why `receivers_r5.tsv` shows 21 families.
  - The same holds for 108 of the 368 never-swept rows (|w| 0.0362): each of their ring <= 13 windows is already screened or listed under a heavier receiver.
  - So when both k85 batches finish, every one of the 368 + 25 rows is covered to its ring. The family column names only the first receiver that brought a window in.

## Mapping, once results come back

`../scripts/map_r5.py` is W13's method:

- f-name, using Opus parse_name spec 4.5;
- all 14 dihedral images, against the Studio-full and A97 worlds, the x7_SF/AF certificates and k85CL;
- then the independent pure-Python cross-check, as in xval3.

Run it as `python3 map_r5.py round5/mac/results round5/map/`. It needs the container files `/tmp/swarm-W13/r2/world567_recv.tsv` and numpy.

Test: replaying W13's round-4 res files with the round-3 list as "old" reproduces round 4 exactly:

- 7 new patterns (3 D, 4 C);
- +6 receivers in each x7 certificate, 0.039774;
- worlds +203 / +211;
- xval equal on all 5 sets.

Built by `../scripts/build_r5.py` and `../scripts/batch_r5.py` (build log `../scripts/log_build.txt`).
