# Round 33 (H-KC): an independent Kempe D-closure engine, and k19

Engine level, 18 Oct 2026, 02:54Z-04:15Z. `kc.cpp` (sha256 4b7c62f2...), a C++ port of `../kempe_w7_5666567.py`,
written from textbook definitions. **No dfast, cfast or Lean source was read**; dfast's output lines were used only
to compare.

**Method.** Canonical ring colourings ranked directly. Extension by backtracking over the interior. Closure: a bad
class becomes good if, for some pairing, every coarsest admissible chain partition (a non-crossing partition of the
ab-runs with its Kreweras complement on the cd-runs) has a swap of whole chains landing on a good class. Witness
partitions are cached per class and pairing. Gauss-Seidel order by default, Jacobi with `-j`; checkpoints with `-c`.

**Validation** (all with the final build):
| Set | Keys | Result |
|---|---|---|
| c7_5666567, ring 13, not D | 1 | ext 7,372, reached 53,690, depth 18: equal to dfast and to the Python, pass by pass |
| Windows, rings 10-16 (`val.txt`, every k-th line of loop/n9 win9/25/27/31) | 98 (80 not D) | classes, ext, reached, D and Jacobi depth equal to dfast on all 98 (`cmp_val.txt`) |
| Ring 17 not D, 6:6:6\|6:6:6\|6:6:6\|6:6:6\|6:8:6 | 1 | ext 550,968, reached 3,387,935, depth 4: equal to dfast18 |
| Ring 17 D, 6:5:6\|6:6:6\|6:6:5\|6:6:6\|8:666:6 | 1 | ext 884,946, D, depth 3: equal to dfast18 |
| Ring 18 D, 6:6:6\|6:6:6\|6:6:6\|6:6:6\|8:566:6 (GS) | 1 | ext 1,939,190, D: equal to dfast18; 275 s, 253 MB |

An earlier build (plain ranker) also matched dfast on the first 61 windows.

**k19** (`k19.txt` = studio14b/part00.txt, `6:6:6|6:6:6|6:6:6|6:6:6|8:666:6`, ring 19, m = 18), one core, Gauss-Seidel:
**D = true**, classes 48,427,561, ext 3,909,279, reached 48,427,561, in 3 passes (36,531,067 + 7,987,132 + 83 new),
1,511 s, 683 MB peak (`k19_kc.out`, `k19_kc_log.txt`). dfast18: classes 48,427,561, ext 3,909,279, D = true, depth 4,
19,736 s. Classes, ext and the verdict agree.
