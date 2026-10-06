# wp21/ (WP21 working directory)

Declaration: `../WP21-declaration.md` (draft until announced). Nothing here is declared data.

- `seeds17.txt`, `reg17-run1*`, `reg17-run2*`: driver regression on order-17 seeds (4 chains x 6 steps). **Deterministic**: the two evaluated files are byte-identical (SHA-256 `06503b91…`). `d1_check21.py --all` accepts run 1.
- Planted faults, all detected by `d1_check21.py` on real driver output (script in the commit message of the package commit): corrupted count, corrupted witness depth, wrong input hash, wrong declaration hash, and an **invalid triangulation** (two neighbours swapped in one rotation; reported as "graph 5 is not a valid minimum-degree-5 spherical triangulation").
- `sample-A-m5-26.txt`: the phase-A selection, 4,578 of the 91,441 graphs of `plantri -m5 -a 26`, rule `sha256("WP21-A-"+i)[:8] mod 20 == 0`. SHA-256 of this file: `24e381cbc4a0a65092fb2689f57bbb8163fad2d17573bf552a2ffcc42964ba31`.
- `full-m5-26.txt` (not committed, ~15 MB): the full list; regenerate with `plantri -m5 -a 26`; its SHA-256 `88acad11…76a8` is pre-registered.
