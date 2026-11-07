# e7kc: kc lines for the 13 d7 offc kills recorded only as e7_ names

The 13 names Studio listed (12 in out/eq_D7_dfast.out, 1 in out/lp_dfast.out) are in `e7names.txt`.

## What an e7 name means
`e<d>_<L>_<S>_<mask>` comes from `gen.py` (`make`, line 118); all three files are on main.
- `<d>` is the degree of the centre u.
- `<L>` is the link word w_0..w_{d-1}:
  - `5`/`6` is a configuration vertex of that exact degree.
  - `B` is a big neighbour (7, 8 or 9). It is a **ring** vertex, not part of the configuration (built as degree 9 and kept out of I).
  - `.` is a position outside the window.
- `<S>` is the second-ring word s_0..s_{d-1}, where s_i is the common neighbour of w_i and w_{i+1} (the vertex opposite u on edge w_i w_{i+1}). It uses the same letters.
- `<mask>` (the third block) is 1 where L is not `.`. That is the set of link positions in the window, B included. It is redundant with L and is kept to tell sender sets apart in names.
- The configuration is u (degree d), plus every w_i and s_i lettered 5 or 6, with those exact degrees. Its ring is what pairs.py's builder gives.
- Names are canonical over the dihedral group. The eq_D7 generation used a different rotation representative, so a name rebuilt by today's `canon_key` can be a rotation of the stored one: same L/S pair, same configuration.

## Files
- `e7kc_stored.tsv`: verbatim kc lines for the 12 eq_D7 kills, from `eq_D7_k3.txt.gz` (on main, md5 2732ad76).
  - Columns: source, then the dfast input line (`name r m ringadj intadj`).
  - `e7kc_stored_kc.txt` is the same lines without the source column.
- `e7kc_rebuilt.txt`: all 13 rebuilt from the name alone by `e7kc.py`, which execs gen.py and calls its `make`. The names printed are today's canonical form.
- `compare.txt`: for each of the 12, the rebuilt and stored lines are interior-isomorphic (interior graph + degrees) with equal r/m. For all 13, r/m equal the dfast record.
- `stored_dfast18.out` / `rebuilt_dfast18.out`: our dfast18 (loop/opus/K_frame_kill/dfast18) on both sets. Result: 12/12 and 13/13 D=true.
  - The stored lines reproduce `eq_D7_dfast.out`'s classes/ext/reached exactly.
  - The lp kill's rebuilt line reproduces `lp_dfast.out` exactly: r=10 m=7 classes=2461 ext=623 reached=2461 D=true depth=7.
- For the lp kill, use the rebuilt line (no stored input survives):
  `e7_...6556_...5B5._0001111 10 7 0,1,2;2,3,4;6;6;0,8,9;4,5,6;6,7,8 1,2,3,4;0,2,5;0,1,3,5;0,2,4,6;0,3,6;1,2;3,4`
