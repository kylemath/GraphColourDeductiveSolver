# W1 (cut along chords, keep each pocket level): full bottom-up recursions

22 Oct 2026, a ~75-minute probe. Code: `wk.py` (pockets, multi-walk SAT, merge), `run_w1.py` (hierarchies from `../hier.py`), `run_vor.py` (chord-adversarial Voronoi hierarchies), `summarize.py`, which writes `summary_merges.txt`. Per-merge logs are in `logs/`, and run summaries in `summary.jsonl` and `summary_vor.jsonl`. Labels: [P] proved, [M] measured (SAT is ground truth), [C] conjecture.

## Numbers first [M]

In the tables, **R** is the min repair radius for properness around the seam conflicts. **w** is the min collar width along ∂U that, together with the repair zone, makes every pocket 1-level. "Chorded" means U has internal chords.

| hierarchy | merges | chorded merges (max chords) | R at chorded merges | w at chorded merges | R at chordless merges | w at chordless merges | final closing R |
|---|---|---|---|---|---|---|---|
| top-down `hier.split`, L = 12 and 40, 12 completed runs + 2 ico20 runs (merges complete, closing unresolved) | 1,544 | 191 (12) | {0: 182, 1: 9} | {0: 124, 1: 67} | {0: 978, 1: 324, 2: 51} | ≤ 3 | **2** in 11 runs, 1 in 1; ico20 unresolved (see below) |
| same, all 24 renamings (flip10 ×2, flip20, defect_ico17 ×2) | 574 | 66 (6) | {0: 65, 1: 1} | ≤ 1 | {0: 353, 1: 151, **2: 4**} | ≤ 3 | 2 in all 5 |
| Voronoi cells, merging the neighbour that **maximises** chords (ico10, flip10, defect_ico17, rand22) + one "any" run | 1,018 | 996 (**91**) | {0: 897, 1: 92, 2: 7} | {0: 618, 1: 320, 2: 54, 3: 4} | {0: 22} | ≤ 1 | **2, 2, 2, 2**; any: 1 |

- Maps: ico10 and ico20 domes; flip10 and flip20 (defect maps, degrees 5–9, n = 1,002 / 4,002); BASE_defect_ico17 (2,892); BASE_rand22 (random, 4,842; Voronoi only, because the top-down splitter did not finish on it, as in `../RESULTS.md`); drum30_10; glue5_5_5.
- **Re-levelling never failed.** In 3,136 merges, w ≤ 3 always and there were 0 fallbacks: no full recolour was needed, and no union was found that cannot be weakly levelled.
- All 2,129 leaves have a weakly 1-level colouring. Of these, 1,259 have chords; leaves have up to 375 vertices.
- Every final colouring is proper.
- **Closing merge:** in the adversarial runs both final halves carry many chords: 32/18 (ico10), 27/30 (flip10), 64/72 (defect_ico17), 73/56 (rand22, n = 4,842; 349 conflict vertices). R_final = 2 in all four. The top-down roots were chordless, with R_final ≤ 2.
- R = 2 at chordless merges occurs only at large balanced top-down merges (median nU 528, against 56 overall). It is mostly an artefact of my search: by default I tried only the 6 renamings with the fewest conflicts. With all 24 renamings, the count drops from 2 to 0 on flip10 and from 5 to 1 on defect_ico17. Treat the R histograms as upper bounds.
- **The strict invariant is genuinely lost, and this is harmless.** τ of the whole chorded boundary reaches 8.2 (Voronoi) and 3.0 (top-down), yet R stays ≤ 2. Before re-levelling, the max pocket τ was ≤ 5.6.
- Seam-pocket counts s_A + s_B (pockets of A and B whose boundary meets the seam arc) reach 84, and R stays ≤ 2 throughout. In the Voronoi runs R depends on s, though s is confounded with merge size:

  | s | merges | share with R ≥ 1 | median nU |
  |---|---|---|---|
  | 2–3 | 645 | 0.6% | 24 |
  | 4–9 | 333 | 17% | 47 |
  | ≥ 10 | 40 | 92% | 328 |

  The 7 merges with R = 2 have s = 5–84. So s matters, but far more weakly than the linear bound below predicts.
- **Open point, ico20 (n = 4,002, both L).** All merges completed (234 and 137, with R ≤ 2 and w ≤ 3). The closing sphere repair, however, was still inside one unbudgeted CaDiCaL call after more than 40 minutes (py-spy: `proper_repair` called from the root step of `run`). R_final is therefore **undetermined, not ≤ 2**. `levelling` saw the same stall in one ico20 run. A final repair that is slow to settle may be a hard instance; it should be rerun with budgets and a logged R ladder. ico30 (9k vertices) was not run. BASE_rand22 top-down: the splitter did not finish, so it was killed.

## The weakened invariant, precisely

**Pockets [P].** Let U be a near-triangulated disc. Its *internal chords* are the edges of U joining non-consecutive vertices of ∂U. Cutting along all of them splits U into pockets P_1…P_k:
- each pocket is a disc with no internal chord;
- the pockets form a tree T(U) with k − 1 = |Ch(U)| edges;
- every pocket boundary lies in ∂U ∪ Ch(U), so it uses only vertices of ∂U.

Chords that are G-edges *outside* U do not affect U's colouring or walks. They matter only later, when they become edges of a parent.

**Definition.** A colouring c of U is *weakly K-level* if τ(P_i, c|P_i) ≤ K for every pocket, with each pocket taken in its own boundary gauge (`levelling` §1.2). This is still a property of the boundary word c|∂U alone, now read along the tree T(U), so a finite-state description survives.

[P] A pocket that is a single triangle is always level, because its walk uses three distinct labels. On fully chorded strips the invariant is therefore vacuous. All the work is pushed to the merge where the pockets fuse.

**Mismatch Lemma W [P].**
- Along ∂A, A's gauge and pocket P's gauge differ only at chord endpoints, where the fan parities change. So on each maximal stretch of ∂A inside one pocket, H_A = ±H_P + const, and that stretch lies in a K-ball.
- Consecutive stretches share a chord endpoint, so their centres are within 2K of each other.
- Hence, if the seam arc of A crosses j_A stretches and that of B crosses j_B, then for every renaming the mismatch is at most 2K(j_A + j_B). For j = 1 this recovers the 4K of `levelling` (i).
- So W1 keeps bounded mismatch *when seams cross O(1) pockets*. The data says R is small far beyond that regime.

**Conjecture W-LML [C].** There are constants R and w such that, for every planar triangulation G with minimum degree 5:
- **(a_W) Merge.** Let A and B be disjoint discs with U = A ∪ B a disc (chords allowed anywhere), and let c_A, c_B be weakly 1-level. Then some renaming π and some weakly 1-level c_U agree with c_A ∪ πc_B outside N_R(conflicts) ∪ N_w(∂U).
  - The collar N_w(∂U) contains every pocket boundary of U.
  - Pockets of A and B that the seam fuses are re-levelled as one pocket.
  - Measured: R ≤ 2 and w ≤ 3.
- **(b_W) Closing.** If A and B are discs partitioning V(G), each weakly 1-level, then some renaming plus a recolouring of N_R(conflicts) is proper. Measured: R ≤ 2 with up to 73 chords per half.
- **(c_W) Decomposition.** Any disc hierarchy with bounded leaves works. [C, believed easy]: greedy Voronoi merging always completed here, and the top-down splitter only needed occasional large "nodisc" leaves.
- **(d_W) Leaves.** Every bounded disc has a weakly 1-level colouring. This is a finite check: 2,129 of 2,129 passed [M].
- [P] (a_W) to (d_W) imply the 4CT, by the same recursion as LML.
- Part (c) has moved from open (`../RESULTS.md`: chordless hierarchies seem not to exist) to essentially free. The cost is that (a_W) must re-level arbitrarily many freshly fused pockets inside one collar. Empirically that costs nothing extra: w at chorded merges is ≤ 3, the same as at chordless ones.

## Calibration and caveats

- [M] The evidence is about 3,100 merges on 9 maps up to n = 4,842: no failure, R ≤ 2, w ≤ 3. That is consistent with LML's numbers, and W1 does not degrade them, even under adversarial chord maximisation.
- The top-down chorded merges are small (nU ≤ 120). The Voronoi runs supply the large chorded unions, up to 2,785 vertices and 91 chords.
- No run above 5k vertices completed: the 9k ico30 run was not attempted and ico20 is partial.
- The SAT re-level uses a conflict budget of 3·10⁶. Every call that mattered returned SAT, so the w values are exact minima, except that a budget-out at a smaller w would show up as a larger w.
- [C, about 70%] (a_W) and (b_W) hold with R ≤ 2 and w ≤ 4 on bounded-degree maps. [C, about 60%] W1 is the right replacement for chordless hierarchies. The main risk is that the pocket count along a seam is unbounded in an adversarial hierarchy, and Lemma W gives no bound there.
- Next steps:
  - redo the measurements with all 24 renamings everywhere;
  - finish ico20/ico30;
  - build seams that cross many pockets on purpose, to try to break the s-independence.
