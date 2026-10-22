# Multiscale recursion with seam repair on binder-rich triangulations

22 Oct 2026. All code, maps (`*.pkl`, adjacency lists), logs and saved cases are in this folder. The originals in `/tmp/claude-0/ms/` were not edited. The code that changed was copied here: `runms.py` is `run()` with logging added, and `hunt_binder.py` / `hunt_strong.py` are `hunt.py` with a seam forced through the centre.

## 1. Maps

Construction (`build.py`): start from an icosphere (frequency f), or for M4 from an icosphere that was first randomised with flips. Then run simulated annealing over edge flips. Every flip must satisfy all of these:
- degrees stay in [5,8];
- no separating triangle (the new edge's endpoints have exactly the 2 common neighbours a, b);
- no chordless 4-cycle. In a triangulation every chordless 4-cycle separates, so the maps have no separating 3- or 4-cycles. Separating 5-cycles were not checked.

Score per degree-7/8 vertex, under the dihedral canonical key, which reproduces every `canon_key` in both TSVs: partial credit for a link word at Hamming distance ≤ 2 from a binder link, +1 for an exact link match plus credit for how close the second ring is, and +12 for an exact (link, second ring) row match.

Targets: all 96 binder rows of degree ≤ 8 (from the 113 distinct rows in opus_binder_rows ∪ binder_rows_swept). M3 instead used only rows whose link is one of the three highlighted canonical links 5566776 (=7766556), 5566767 (=7676655), 5566766 (=7665566).

Column key:
- **full row match**: a vertex whose degree, link word and second-ring word equal a binder row.
- **hard-4 full/link**: full matches / link-only matches for the highlighted links.
- **near**: vertices within distance 1 of a full match.

| map | n | degree histogram | full row match | distinct rows realised | link-only match | hard-4 full / link | near | sep. triangles / chordless 4-cycles |
|---|---|---|---|---|---|---|---|---|
| M1_ico16 | 2562 | 5:837 6:924 7:777 8:24 | 82 | 41 | 416 | 24/81 | 615 | 0/0 |
| M2_ico22 | 4842 | 5:1585 6:1719 7:1503 8:35 | 140 | 53 | 853 | 41/151 | 1021 | 0/0 |
| M3_ico22_hard | 4842 | 5:1518 6:1867 7:1408 8:49 | **193** | 19 | 519 | **192/535** | 1378 | 0/0 |
| M4_ico22_rand | 4842 | 5:1590 6:1716 7:1494 8:42 | 134 | 57 | 829 | 35/145 | 1015 | 0/0 |
| M5_ico31 | 9612 | 5:3082 6:3536 7:2918 8:76 | 284 | 67 | 1674 | 69/288 | 2101 | 0/0 |
| control BASE_rand22 | 4842 | 5:1611 6:1632 7:1599 | 0 | 0 | 260 | 0/24 | 0 | 0/0 |
| control BASE_defect_ico17 | 2892 | 5:1081 6:969 7:615 8:227 | 0 | 0 | 39 | 0/5 | 0 | 0/0 |

The most common rows in M3 are 5566776/5675667 ×26, 5566766/5676767 ×21, 5566776/5765666 ×21, 5566776/5665667 ×17 and 5566767/6676656 ×16 (`census.txt` lists them for every map).

BASE_rand22 is the matched control. It has the same constraints and almost the same degree histogram, but its flips were random and not steered (`base_rand.py`). BASE_defect_ico17 is the earlier `defect.py` map. BASE_ico22 (the plain dome) was dropped: `run()` on it ran for more than 11 CPU-minutes on seed 0 without finishing.

## 2. `run(adj,seed)`: 6 seeds per map (`runms.py`, `summ.txt`)

"conflicted" means merges that had at least one monochromatic seam edge after the greedy renaming. R is the repair radius `run()` needed.

| map | merges | conflicted | R=0 | R=1 | R=2 | R=3 | R≥4 | share of conflicted with R=3 |
|---|---|---|---|---|---|---|---|---|
| M1_ico16 | 4984 | 421 | 91 | 218 | 111 | 1 | 0 | 0.24% |
| M2_ico22 | 9520 | 776 | 198 | 413 | 159 | 6 | 0 | 0.77% |
| M3_ico22_hard | 9680 | 776 | 198 | 390 | 181 | 7 | 0 | 0.90% |
| M4_ico22_rand | 9551 | 761 | 187 | 397 | 170 | 7 | 0 | 0.92% |
| M5_ico31 | 19140 | 1549 | 418 | 800 | 324 | 7 | 0 | 0.45% |
| BASE_rand22 (control) | 9802 | 783 | 192 | 406 | 180 | 5 | 0 | 0.64% |
| BASE_defect_ico17 (control) | 5816 | 486 | 119 | 271 | 91 | 5 | 0 | 1.03% |

Per level, R=3 appears only at L3 and above. Typical rows:
- M3: L2 {0:156, 1:219, 2:16}, L3 {0:29, 1:139, 2:64}, L4 {0:11, 1:21, 2:48}, L5–L9 have one or two R=3 each.
- BASE_rand22: L2 {0:147, 1:208, 2:28}, L3 {…, 2:60, 3:2}, L4 {…, 2:45}.

`summ.txt` has the full per-level tables.

**Near binder vs not.** Without stratifying, merges whose conflicts touch a binder neighbourhood look worse (M3: R≥2 in 69/241 vs 16/113 in the unstratified L2–L4 counts). That is mostly a size confound: big, many-conflict merges are the ones likely to touch the roughly 28% of vertices that are binder-near. Stratified by level and conflict count (L2–L4; conflict counts 1, 2–3 and 4+), the R≥2 rates for near and far are similar in most cells. Some L4 cells show near > far, but those cells hold 1–16 merges.

## 3. Strong adversary (hill-climb over Kempe moves on halves A, B; best of 24 renamings)

Regions are the ball of radius 7 (radius 9 in one run) around a binder full-match vertex. The A/B split is a Voronoi split between two vertices at distance r from the centre on roughly opposite sides, and it is accepted only when the centre's closed neighbourhood meets both A and B, so the seam runs through the binder 1-ball. The `_strong` variant adds two things: a lexicographic objective (R, then the size of the smallest sufficient free set over all renamings), which gives the hill-climb a gradient on R plateaus, and 3 restarts per centre.

| run | centres | trials × iters | mean region size | R=1 | R=2 | R≥3 |
|---|---|---|---|---|---|---|
| M1_ico16 | binder | 40 × 1000 | 212 | 22 | 18 | 0 |
| M2_ico22 | binder | 40 × 1000 | 207 | 24 | 16 | 0 |
| M3_ico22_hard | binder (hard-4) | 40 × 1000 | 208 | 31 | 9 | 0 |
| M3_ico22_hard, radius 9 | binder | 15 × 1500 | ~340 | 2 | 13 | 0 |
| M3_ico22_hard strong | binder | 20 × 800 × 3 restarts | ~205 | 0 | 20 | 0 |
| M4_ico22_rand | binder | 40 × 1000 | 209 | 27 | 13 | 0 |
| M5_ico31 | binder | 40 × 1000 | 211 | 27 | 13 | 0 |
| M1 control | degree-6 | 40 × 1000 | ~210 | 28 | 12 | 0 |
| BASE_rand22 control | non-binder degree-7 | 40 × 1000 | ~200 | 21 | 19 | 0 |
| BASE_rand22 control strong | non-binder degree-7 | 20 × 800 × 3 | ~195 | 0 | 20 | 0 |

**Max R from the adversary is 2 everywhere.** In the strong runs the mean free set at R=2 is 95 vertices for M3 binder centres and 99 for the control: no difference.

## 4. R=3 cases (all from `run()`; none from the adversary)

All R=3 cases are saved as `case_run_<map>_s<seed>_L<level>_<k>_R3.pkl`. Each pickle holds the cluster P, the kids, the colouring before repair, the conflict edges, the freed set and the colouring after repair. `cases_run.md` describes every case:
- the degrees of the first conflict edge and the links of its two endpoints;
- the distance to the nearest binder full match;
- the distance to the cluster boundary;
- the best R over all 24 renamings of the kid that holds the conflict endpoint.

What they look like:
- Most R=3 cases are big merges (|P| from hundreds to the whole map) with many conflicts (5–295). `run()` picks renamings greedily by conflict count, not by R. For multi-conflict cases the best-renaming R was not computed (shown as None).
- Single-conflict 2-kid merges where **every** renaming gives R=3 (that is, R=3 under the hunt semantics):
  - **M2 s1 L7**: edge degree 7–5, links 7555566 | 77775. One binder vertex (7675665/5566766) at distance 2. 13 seam edges in the radius-2 disc. The ring at distance 3 (20 vertices: 3×5, 11×6, 6×7) is coloured so that the radius-2 disc (24 vertices) cannot be recoloured.
  - **M3 s0 L8**: edge 7–5, links 5775666 | 77666. One hard binder vertex (6556676/7567766 = 5566766/5677667) at distance 2. The disc is almost entirely in one kid: only v and the seam touch the other side.
  - **The control BASE_defect_ico17 s5 L6 has the same kind of case** (edge 5–8, every renaming gives R=3, no binder vertex anywhere). So this pattern is not binder-specific.
- R=3 was always enough. R≥4 never occurred, so `run()` never needed a free ball larger than radius 3.

## Honest assessment and caveats

- **No sign of a binder-specific obstruction.** Several measures match the matched random control within noise:
  - the R distribution from `run()`;
  - the R=3 rate (0.2–0.9% vs 0.6–1.0% for the controls);
  - the adversarial max R (2 vs 2);
  - the adversarial free-set size.
  Densely packing the hard rows 7766556 / 7676655 / 7665566 (M3: 192 exact rows) did not make seam repair harder.
- R=3 does occur, about once per 100–200 conflicted merges, in binder and control maps alike. It is the ordinary event that a 20–26-vertex ring colouring does not extend inside. It is not an obstruction, since R=3 always repaired it.
- These maps are 4-colourable triangulations with many binder 1.5-balls. **They are not counterexample-like** in the global sense. A minimal counterexample also forbids every reducible configuration. These maps were not checked against the registry and probably contain many reducible configurations, so they test only "binder neighbourhoods are present", not "everything reducible is absent".
- Binder matches overlap heavily: about 28% of vertices are within distance 1 of a match. "Distinct rows realised" is 19–67 of the 96 targeted rows. Rows of degree 9–11 were not targeted (degree cap 8).
- The adversary is a local hill-climb over Kempe moves on regions of about 200–340 vertices with Voronoi seams. Larger regions, other seam shapes, or exhaustive search could find R≥3. Region boundaries are unconstrained, which favours repair near the boundary, although all centres are 7–9 steps from it.
- `run()` itself is greedy: its renaming minimises conflict count, so its R is an upper bound on best-renaming R. The nearBinder flag means "some conflict endpoint is in N[binder vertex]" and is confounded with merge size (see §2).
- Separating 5-cycles (internal 6-connectivity) were not controlled.
