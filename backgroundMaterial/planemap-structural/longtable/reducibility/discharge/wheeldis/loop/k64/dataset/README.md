# Explore's judged windows and binder-row history (21 Oct 2026, 21:15Z)

Explore built these three files for the "Interpretable route to four colours" thread when the discharging sweeps were paused at 21:08Z. They are copies, and the sources are on branch `claude/project-thread-nh6pv2` under `backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/`.

## windows_judged.tsv (97,174 rows)

There is one row per configuration ("window") that explore's kc engine judged. These are positives and negatives together. They come from the kc cache `loop/k47/A_kcc.out`, joined to the dfast cache (`A_df.out`), the cfast cache (`A_cf.out`) and the two-engine kill list (`KILL`).

A window is a connected set of vertices around a degree-7+ receiver u: u itself, its link w_i and its second-ring apexes s_i. It is cut from one binder row (a link word and a second-ring word) at its exact degrees, out to ring size 15 (a few at 16-17). Vertices of letter 9 (degree >= 9) are never inside a window.

Columns:
- `name`: window name `a<d>_<u or -><link letters>_<s letters>`. A `.` means not in the window. F/N means w_i is outside while both s_(i-1) and s_i are inside; F is used when w_i has degree 5, N otherwise.
- `ring`, `m`: the ring (boundary cycle) length and the number of interior vertices.
- `n5..n8`, `int_degrees`: interior vertex degrees, which are exact.
- `ring_adj`, `int_adj`: kc's configuration line. For each interior vertex it lists the ring indices it touches, then the interior vertices it touches. Ring vertices have free degree.
- `kc_D`: kc's D-reducibility verdict (true/false). false is definite for D.
- `kc_C`: `true` means kc found a contraction X with leftover 0. `false_Xle4` means no admissible X of size <= 4 worked. That is NOT a proof of non-reducibility.
- `kc_X`: kc's X when kc_C is true.
- `dfast_D`, `cfast_fixedX`: the second engine's verdicts, where it was run. `-` means it was not run.
- `two_engine`: `D` or `C` when both engines agree (the registry-grade label), `-` otherwise.
- `first_window_file`: the window list it first came from. Its name carries the row as `win45_<d>_<link>_<s>_A<maxring>.txt`.

Label counts:

| label | count |
|---|---|
| two-engine D | 2,912 |
| two-engine C | 1,017 |
| kc D, dfast not confirmed or not run | 23 |
| kc C, cfast rejected | 7 |
| neither | 93,215 |

Caveats:
- Windows overlap heavily, because many come from the same row and are nested subsets. Split train and test by row (`first_window_file`) or by family, not at random.
- "Neither" at ring <= 15 says nothing about the same row at ring 16+.
- Windows at ring 16-21 that ran at Studio or on the farm are not here.

## binder_rows_swept.tsv (50 rows)

These are the rows explore's ring <= 15 queue ran in rounds 54-64, from the logs `k47/q54.log` and `k5x/q5x.log` through `k64/q64.log`. Each row has the minimal two-engine kills (ring, D/C : count). If it had no kill, the row lists the ring 16-18 to-do handed to Studio or the farm. Rounds before 54 used other drivers and are not parsed here. EXPLORE-LOG.md (SolvingFrameworkPlan/docs/working/) has every round.

## opus_binder_rows.tsv (113 rows)

This is every binder row in Opus's seven `binders_canon.txt` lists (s39o A74, s42a A78, s44 A78/A83/A83nf, s47 A84/A84nf), merged by dihedral canonical key. Each row keeps its most negative LP weight and the certs it appears in. It also gives the registry containment at explore's head adm64g (A109 plus r64g): 69 rows are dead (a registry configuration lies inside the row's 1.5-ball) and 44 are alive.

The admitted registry itself (two-engine D and C, canonical f-names) is `out/job30/k3x_D.out` and `k3x_C.cfast` on main.
