# C_kc_ring17: kc on the binders' and HARD28 rows' untested B-fixed windows at ring 17-20 [exploratory, single engine kc, E]

Q (08:55Z): with kc, do the 7/27 binders' and the HARD28/HARD28-like rows' untested exact B-fixed windows at ring 17-20 turn D?
Guess: a minority (10-20%) of windows turn D, at most 1-2 rows die; ring 17 was 0/6 on HARD28; the 7/27 binder 5675765/6577575 stays free.
Plan-changer: if the 7/27 binder (and the next binders) die, the ring <= 16 supply limit no longer binds and a ring 17-20 kc loop + LP rerun is a route; if ~0 D, the ring >= 17 supply at u is not the route (consistent with GATE-K2 §5: kills sit at neighbouring 7s).

Run 18 Oct 08:40Z-09:57Z, at most 2 cores, peak RSS 253 MB. kc's maximum ring is 20 (`n > 20` means SKIP). Every verdict below comes from kc alone [E], except where dfast is named.

## Part 1 (08:40-09:00Z): u-centred B-fixed windows at ring 16-18 (stopped by the course change)

Builder: `mk.py buildall OUT RMIN RMAX FAMILY` (w2.py with every |S|, and a per-row report in `w*.txt.rows`). Families: `fam1` = the 7/27
certificate row 5675765/6577575, `fam2` = binders_self plus the free d=7 binders from rounds 28-30, `fam3` = HARD28 (15), `fam4` = HARD28-like (48).
Untested windows at ring 17-20: 2 / 14 / 35 / 127 (`w1..w4_*.txt`), queued as `queue.txt`.

| window | ring | verdict | ext | reached | wall s |
|---|---|---|---|---|---|
| f7_.556757_.56.77. (R) | 16 | not D | 98,480 | 352,695 | 77 |
| f7_.556757_.57.77. (R) | 17 | not D | 206,754 | 629,529 | 308 |
| f7_5567576_56.77.7 (R) | 17 | not D | 305,410 | 1,907,986 | 261 |
| f7_.557557_.57777. (5765575/7565777) | 17 | not D | 248,471 | 909,169 | 338 |
| f7_.557557_.76.77. (7557755/7775776) | 17 | not D | 223,797 | 783,115 | 339 |
| f7_.557657_.57.77. (5576576/5757756) | 17 | not D | 211,680 | 707,273 | 304 |
| f7_5567557_56.7777 (5765575/7565777) | 17 | not D | 357,720 | 1,986,515 | 241 |

- 0 D of 7. Ring 17 not-D takes about 5 min (8-10 Gauss-Seidel passes), not 2.
- R's three windows match explore's round 34 `k34/binA_kc.out` exactly. That is the same engine run twice, so it shows reproducibility, not a second engine.
- Two binders cannot be reached by u-centred B-fixed windows at all:
  - R has only 4 B-fixed windows (ring 11, 16, 17, 17), all not D.
  - 5567576/5756756 has no window above ring 16.
- The run was stopped at the course change. w007 and w008 were killed and have no verdict.

## Part 2 (09:00-09:57Z): windows of R not centred on u (course change)

Windows are connected induced subsets X of the 15 vertices whose degrees R fixes (u, w0..w6, s0..s6). X is taken at exact degrees, the rest of the
map is free ring, and windows equal to round 34's (u + all link) are excluded. Files: `nonu.py` (s1 = s4 = 5, `x_all.txt`, 1,407 lines at ring <= 20) and `fill.py`
(s1, s4 in {6,7,8,9+}, `f_all.txt`, 2,780 lines at ring <= 18). Names are `x7_<u|-><w letters>_<s letters>`. Results are in `results2.txt` and `results3.txt`.
`cover.py` writes `../fillings_opus.txt`.

- **s1 = 5 or s4 = 5:** 9 D windows at ring 11-12, and dfast (Studio's, rebuilt here) gives the same D on all 9 (`xD.txt`, `xD_dfast.out`).
  - Examples: x7_u5..5765_....5.5 (s4 = 5, ring 11) and x7_u5675..5_.5....5 (s1 = 5, ring 11).
  - Each one uses a five at s1 or s4. These fillings are the 9 that explore had already killed.
- **The 16 fillings with s1, s4 >= 6: 0 D.** 1,350 windows were run with neither s1 nor s4 at 5 (ring 6-16), all not D.

| ring | 6-12 | 13 | 14 | 15 | 16 | 17-20 |
|---|---|---|---|---|---|---|
| windows run, s1/s4 not 5 | 393 | 243 | 327 | 156 | 12 | 0 |
| D | 0 | 0 | 0 | 0 | 0 | - |

- Coverage by class:
  - 77777-five wheel (u, w2, w3, w4, s2, s3 plus more): ring 15-16, 26 of 28 run.
  - w2/w4-centred (the 7 with all its fixed neighbours): ring 14-15, 21 of 27 run.
  - All other subsets: complete at ring <= 14; ring 15, 143 of 520.
- Untested: 1,644 windows at ring 15-20 (`untested_r15_20.txt`, dfast format, smallest ring first).
- `fillings_opus.txt` lists all 16 fillings with s1, s4 in {6..9} as **open**.
- The triangle-frame windows (u + w2 + e, e', x3) were cancelled by the lead and not built.

## Reading [I]

- At rings 13-15, D in sub-configurations of R appears only when s1 or s4 is a five.
- With s1, s4 >= 6, every subset at ring <= 14 is not D. The large (ring 16-20) wheel and w2/w4 windows are untested, but the ring-17 D rate here was 0 of 7.
- So windows inside R's fixed patch, at u or away from it, are unlikely to close the 16 open fillings.
- Killing them probably needs vertices outside R's patch: case splits over the privates (p) and the third ring, which is GATE-K2 §5's "kills at neighbouring 7s" read one ring further out.
- Ring >= 17 supply at u is not a route to t* <= 0 on this evidence.
