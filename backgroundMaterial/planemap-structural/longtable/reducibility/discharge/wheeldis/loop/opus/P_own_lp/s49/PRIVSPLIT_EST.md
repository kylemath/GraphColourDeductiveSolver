# PRIVSPLIT_EST: what a link-private split row key would buy on the top A83 binder rows (Opus s49, pricing only)

No solve was run. Everything here ran at nice 10, one thread. RSST 2.126 and 8406.123 were not used: they are excluded by name,
and they are absent from every input.

## Inputs

- **Binder rows: final.** L1.done appeared while this ran. The rows are the top 5 receiverR2 rows by |w| of the nosep cert
  `s44/run_A83/cert_q44fbA83L.json` (36 receiver rows, Σ|w| 0.397347). The canonical keys are in `s44/run_A83/binders_canon.txt`.
  - The provisional keeppen top 5 (`s44/run_A83/K.log`) is a different set of rows; see the appendix.
  - Top-5 Σ|w| = **0.202469**.
- **Loads.** The A83 keeppen solution `s44/run_A83/sol_q44fbA83.json` (t = 0.105883918), with cap 1 + t = 1.105883918 for d = 7.
  The valuation is the receiver row's own (y, x, M, r, lq, fb, lQ at Qeff), as `recv_coef_R2` computes it.
  - Control: rows 1 and 4 load at exactly the cap (slack 0, −2e−16).
  - Rows 2, 3 and 5 bind in the nosep LP but carry slack 0.0096, 0.0095 and 0.0396 under the keeppen solution.
- **Kills.** Three sources. A cell counts as dead if any one of them kills it.
  1. **This round's 2-ball containment test** (`privsplit_est.py`). It reuses s39o `offc_phys.py`'s matcher: node-induced subgraph
     isomorphism onto exact vertices with equal degrees, every triangle on a face. The window graph is the plane 2-ball of the
     row with the chosen link vertex's privates made exact. The configurations tested:
     - every A83 registry entry, with K re-derived by the OFFC_SPEC §2 rule;
     - explore's whole 2026 set `loop/k51/nl51_kc.txt`, 8,200 two-engine D configurations (md5 b9bc6e8b, rpatN3's source);
     - the 14 kpriv **v3** engine-kill windows (explore 5f4d62d1 `loop/k60/kpriv_v3.txt`, md5 2b824170).
     That gives 22,268 distinct configurations.
  2. **Explore's pair60 grid v3** (5f4d62d1 `loop/k60/pair60_grid.txt`). It covers only the kpriv rows, none of which is in the final top 5.
     The mount `/mnt/project-files/explore/pair60` gave I/O errors every time I tried it.
  3. **The A83 l3q kill table** (`reg_A83/tab_±1.json`, RELAY_SPEC_s21 §21.4). When a2 = a link 7's private is outside the table's mask,
     that letter is dead.
- **Cells.** A cell is written `p1p2`. p1 = p_{k,1} is the private next to s_{k−1}, and p2 = p_{k,2} is the private next to s_k. Letters
  run 5..9, where 9 means ≥ 9 and is never exact. Explore's `priv<a><b>` is our `ba`.

## Correction to the brief: private letters do enter the receiver row

The receiver row's coefficients depend on the privates of its link 7s through **l3q** (RELAY_SPEC_s21 §21.2). At each link 7
w_j, on each side σ with c = w_{j+σ} ≤ 6 and a ≤ 6, the centre credits +Q[(c, a, m)]. Here a2 is **w_j's private adjacent to a**:

- σ = +1 gives a = s_j and a2 = p_{j,2};
- σ = −1 gives a = s_{j−1} and a2 = p_{j,1}.

Today the credit is Qeff = max over a2 ∈ mask. At A83, only a2 = 5 carries any q:

| key | q |
|---|---|
| q(6,6,5) | 0.054770 |
| q(6,5,5) | 0.094390 |
| q(5,6,5) | 0.004719 |

So a cell where that private is not 5 has a true l3q inflow of 0. A split key, or a per-row mask, can credit q(c, a, a2_cell) exactly.
This is sound: it is §21.3 with a singleton mask. No other column family in `recv_coef_R2` reads a private.

That gives two first-order gain channels, both relieving the binder row.

- **(A) Direct.** Drop the lQ credit on the surviving cells. The relief is Σ_j min over w_j's surviving cells of (Qeff − q(c, a, a2_cell)).
  - In every row below, (A) is reached already when **every** a2 = 5 cell of that side is dead.
  - So (A) needs no split key. A receiver-row-level l3q mask is enough: the 2-ball containment kills a2 = 5 with the whole row
    known, where today the table uses only (σ, c, w2, w3, w4, a, o).
- **(B) Payer spare (Long Table's added ask).**
  - The setup: the centre (7) pays the link 7 X = w_j more, keyed on X's privates being in the surviving set.
  - How much X can take is set by X's own d = 7 row, written in its own frame:
    - link (u, w_{j+1}, s_j, p_{j,2}, p_{j,1}, s_{j−1}, w_{j−1});
    - apexes (w_{j+2}, p_{j+1,1} or s_{j+1}, r3, r3, r3, p_{j−1,last} or s_{j−2}, w_{j−2}), where r3 is a ring-3 vertex;
    - free letters 5..9, and only admissible fillings count (A83 registry + rpatN3, engine `admissible()`).
  - extra spare = worst X load over all 25 cells − worst over the surviving cells.
  - At every X the worst load over all cells is exactly the cap. So today's spare is 0, and spare_surv = extra spare.
- **First-order gain** ≤ |w| × relief. This is a bound, not a prediction:
  - it assumes the basis does not change;
  - (B) needs a new payment column that has not been built;
  - two binders may lean on the same X-row spare, so the (B) terms do not add jointly;
  - the 31 other receiver rows (49% of |w|) take over once these rows go slack.

## Row 1: 7676655 / 6667656, d = 7, w = −0.047191 (rank 1)

**Big link vertices:** w0 = 7 and w2 = 7, with 25 cells each. The joint 625-cell key was not tested; see Limits.

**w0: 9/25 cells dead, which is every cell with a 5.**

| cell(s) | killed by |
|---|---|
| 55 | D `e7_B5565B._BBB55.._1111110` |
| 56 | D `f7_.566675_.....5.` |
| 57, 58, 59 | nl0425_r11 (p0,1 = 5) |
| 65 | C `f7_...5665_.....5.` |
| 75, 85, 95 | C `f7_..56675_.....5.` (p0,2 = 5) |

16 cells survive: both privates ≥ 6.

**w2: 9/25 cells dead, again every five cell.**

| cell(s) | killed by |
|---|---|
| 55 | nl0498_r13 |
| 56–59 | nl3740_r14 (p2,1 = 5) |
| 65, 75, 85, 95 | the l3q table (mask {6..9} at a2 = p2,2) |

16 cells survive.

**Row status:** the row survives, at f = 16/25 per vertex (≈ 256/625 jointly, before any joint kills).

**Proxy:** yes. The surviving cells exclude the letter that the coefficient depends on (a2 = 5) at all three lQ terms:

| vertex, side | lQ key | a2 | Qeff |
|---|---|---|---|
| w0, σ+ | (6,6,31) | p0,2 | 0.054770 |
| w0, σ− | (5,6,31) | p0,1 | 0.004719 |
| w2, σ− | (6,6,31) | p2,1 | 0.054770 |

**Gains:**
- **(A)** relief 0.114258, gain ≤ **0.005392**. The row-mask route reaches all of it.
- **(B)**
  - X = w0: worst load over all cells 1.105884 (cell 57, X-row 7667565/7666555, which is binder 4); over the surviving cells 0.988324
    (cell 66, X-row 7666665/7668555). Extra spare 0.117560.
  - X = w2: worst over all cells 1.105884 (cell 55); over the surviving cells 0.898901. Extra spare 0.206983.
  - Total gain ≤ **0.015316**.

## Row 2: 7665566 / 7765766, d = 7, w = −0.047191 (rank 2)

**Big link vertex:** w0 = 7, with 25 cells.

**w0: 6/25 cells dead.**

| cell(s) | killed by |
|---|---|
| 55 | nl0498_r13 |
| 56–59 | nl3706_r14 (p0,1 = 5) |
| 65 | nl3852_r15 |

19 cells survive. They include **75, 85 and 95**, which are open five cells with p0,2 = 5 next to s0.

**Row status:** the row survives, at f = 19/25.

**Proxy:** there is nothing to drop. The only lQ term (σ−, a2 = p0,1) already has the mask {6..9}, so Qeff = 0 today.

**Gains:**
- **(A)** 0.
- **(B)** X = w0: worst over all cells 1.105884 (cell 55); over the surviving cells 1.042145 (cell 75). Extra spare 0.063739.
  Gain ≤ **0.003008**.

## Row 3: 7766656 / 6566556, d = 7, w = −0.044045 (rank 3)

**Big link vertices:** w0 = 7 and w1 = 7.

**w0: only 2/25 cells dead.**

| cell | killed by |
|---|---|
| 55 | nl0451_r13 |
| 65 | nl3440_r13 |

23 cells survive. Seven open five cells remain: 56–59 (p0,1 = 5 next to s6), and 75, 85, 95.

**w1: 9/25 cells dead, which is every five cell.**

| cell(s) | killed by |
|---|---|
| 55, 65, 75, 85, 95 | nl0477_r13 (p1,2 = 5) |
| 56 | nl0766_r15 |
| 57, 58, 59 | nl4231_r15 |

16 cells survive.

**Row status:** the row survives.

**Proxy:** no. The lQ(6,6,31) term at w0 σ− (a2 = p0,1, Qeff 0.054770) keeps a surviving a2 = 5 cell, so the worst case over the
surviving cells is unchanged. The lQ term at w1 σ+ already has the mask {6..9}.

**Gains:**
- **(A)** 0.
- **(B)**
  - X = w0: worst over all cells 1.105884; over the surviving cells 0.968005 (cell 56). Extra spare 0.137879.
  - X = w1: worst over the surviving cells is still 1.105884 (cell 76, X-row 7656767/6555656). Extra spare 0.
  - Gain ≤ **0.006073**.

## Row 4: 7667565 / 7666555, d = 7, w = −0.042996 (rank 4)

**Big link vertices:** w0 = 7 and w3 = 7.

**w0: 6/25 cells dead.**

| cell(s) | killed by |
|---|---|
| 55 | D `e7_B5555.._B5BB..._1111100` |
| 56–59 | nl0279_r10 |
| 65 | C `f7_...5565_.......` |

19 cells survive. They include 75, 85 and 95, which are open five cells.

**w3: 9/25 cells dead, which is every five cell.**

| cell(s) | killed by |
|---|---|
| 55 | D `e7_B5565B._BBB56.._1111110` |
| 56 | C `f7_...5665_.....5.` |
| 57–59 | C `f7_..56675_.....65` |
| 65 | D `f7_.566675_.....65` |
| 75, 85, 95 | nl0311_r11 |

16 cells survive.

**Row status:** the row survives.

**Proxy:** yes at w3. The term lQ(6,6,31) at w3 σ− (a2 = p3,1, Qeff 0.054770) has a2 = 5 dead on every cell. The other two lQ terms
already have the mask {6..9}.

**Gains:**
- **(A)** relief 0.054770, gain ≤ **0.002355**. The row-mask route reaches all of it.
- **(B)**
  - X = w0: worst over the surviving cells is still the cap (cell 66, X-row 7676655/6669656, which is binder 1). Extra spare 0.
  - X = w3: worst over all cells 1.105884; over the surviving cells 0.885930. Extra spare 0.219954.
  - Gain ≤ **0.009457**.

## Row 5: 7766556 / 6576576, d = 7, w = −0.021045 (rank 5)

**Big link vertices:** w0 = 7 and w1 = 7.

**w0: 10/25 cells dead, which is every five cell except p0,1 = 5.**

| cell(s) | killed by |
|---|---|
| 55 | nl0333_r12 |
| 65, 85, 95 | kpriv `r7766556_6567566_w0_priv59` |
| 66 | kpriv `…priv66` |
| 75 | kpriv `…priv57` |
| 56–59 | the l3q table (mask {6..9} at a2 = p0,1) |

The kpriv windows transfer from 7766556/6567566 to this sword.

**w1: 9/25 cells dead, which is every five cell.**

| cell(s) | killed by |
|---|---|
| 55, 65, 75, 85, 95 | nl0333_r12 |
| 56 | nl1338_r15 |
| 57 | kpriv `…w1_priv75` |
| 58, 59 | kpriv `…w1_priv95` |

**Row status:** the row survives, at f = 15/25 for w0 and 16/25 for w1.

**Proxy:** there is nothing to drop. Both lQ terms already have the mask {6..9}.

**Gains:**
- **(A)** 0.
- **(B)**
  - X = w0: worst over all cells 1.105884; over the surviving cells 0.931060. Extra spare 0.174824.
  - X = w1: extra spare 0, because cell 76 is still at the cap.
  - Gain ≤ **0.003679**.

## Totals (final top 5, A83)

| row | \|w\| | (A) relief | (A) gain ≤ | (B) extra spare | (B) gain ≤ |
|---|---|---|---|---|---|
| 7676655/6667656 | 0.047191 | 0.114258 | 0.005392 | 0.324543 | 0.015316 |
| 7665566/7765766 | 0.047191 | 0 | 0 | 0.063739 | 0.003008 |
| 7766656/6566556 | 0.044045 | 0 | 0 | 0.137879 | 0.006073 |
| 7667565/7666555 | 0.042996 | 0.054770 | 0.002355 | 0.219954 | 0.009457 |
| 7766556/6576576 | 0.021045 | 0 | 0 | 0.174824 | 0.003679 |
| **total** | 0.202469 | | **0.007747** | | **0.037533** |

**Reading.**
- No cell kill removes a whole row. The direct l3q channel (A) is worth at most about 0.0077 in t, and it needs only a row-level
  l3q mask, not a split key.
- The payer-spare channel (B) is a first-order bound of about 0.0375, and it is not jointly achievable:
  - it needs a new centre→link-7 payment column keyed on the link 7's privates;
  - the same X rows recur. The X-row 7766766/6555755 is the worst surviving row for several X's, and 7656767/6555656 caps three of them.
- Together the two channels bound a ≤ 0.045 first-order drop from t = 0.1059. The real gain needs a solve, and other binders
  will cap it well below that bound.

Under the keeppen solution, rows 2, 3 and 5 are slack (they bind only in the nosep LP). Their (B) bounds are measured against loads
that are already below the cap.

**A84:** the `reg_A84` tables exist, but no A84 solution does yet (the s47 run_A84 K stage started at 06:49Z). So the pricing is on A83 only.

## Appendix: the provisional keeppen top 5 (K.log), and Long Table's link 7s

This is the 2-ball test only, before kpriv v2/v3 and before union with the grid. It was stopped when L1.done appeared.

| row | K w | 2-ball test | other sources |
|---|---|---|---|
| 7665566/6675676 | −0.028140; final cert rank 11, w −0.008914 | w0 9/25 (every five cell: nl0498, nl3706) | grid: 9 |
| 9656775/5556655 | −0.020977 | w4 6/25, w5 7/25 | grid v3: 9 and 10 |
| 7766655/6567659 | −0.019977 | w0 5/25, w1 10/25 | grid: 5 and 10 |
| 755676556/756556665 (d9) | −0.014260 | not reached | |
| 7655667/7657655 | −0.011824 | w0 5/25, w6 13/25 | |

Pricing (B) under keeppen at Long Table's link 7s, using the grid v3 survivors:

| row | X | extra spare |
|---|---|---|
| 7665566/6675676 | w0 | 0.180026 |
| 9656775/5556655 | w4 | 0.174824 |
| 9656775/5556655 | w5 | 0.053385 |
| 7766655/6567659 | w0 | 0.266719 |
| 7766655/6567659 | w1 | 0 |
| 7666567/5665565 | w0 | 0 |
| 7666567/5665565 | w6 | 0.109472 |
| 7766556/6567566 | w0 | 0.174824 |
| 7766556/6567566 | w1 | 0 |

(A) relief: 9656775 0.054770 (w4 σ−) and 7666567 0.054770 (w6 σ−); 0 on the others.

These rows have no weight in the final cert, apart from 7665566/6675676 at rank 11.

## Limits of the method

- **Marginal keys only.**
  - Each big link vertex is split alone, giving 25 cells. Joint kills that need both vertices' privates were not tested on the final
    rows, for cost: about 6 s per cell, and 256–400 surviving joint cells per row.
  - A full row kill would need every surviving joint cell to die. With 15–23 survivors per vertex, that is not plausible.
- **The 2-ball model** is offc_phys's plane disc. Privates are distinct, ring 2 has no chords, ring 3 is unknown, and letter 9 is never exact.
- **Configurations that need ring 3 cannot be seen.**
- **Registry entries the K rule skips are lost.** These are 1,075 D and 110 C entries with an ambiguous s–s pair, plus 10 C entries
  with r = m = 0. They might fit once the privates are known.
- **RSST configurations outside the engine's window registry are missed.**
  - Two cases show it. The l3q table kills a2 = 5 in row 1 at w2 σ+ and in row 5 at w0 σ−, and my matcher did not.
  - explore's grid cites rsst196 and rsst180 kills that my registry does not hold.
  - Those cells were added from the table and the grid. Other such kills may exist, so the dead counts are lower bounds.
- **The pricing is first order**, under one solution: keeppen loads, nosep weights. The X rows are X's own 1.5-ball, with free
  letters off the binder.
- **The kc engine-kill windows** (kpriv v3) are used as configurations on the strength of their recorded two-engine verdicts. They
  were not re-run here.

## Summary

- Rows fully killed: **0 of 5**.
- Rows partly split: **5 of 5**, over 9 link 7s. Dead cells per vertex: 9, 9 | 6 | 2, 9 | 6, 9 | 10, 9 of 25.
- Total |w| fully killed: **0 of 0.202469** (top-5 total). The non-kill channels are bounded first order at (A) 0.0077 and (B) 0.0375.

Files: `privsplit_est.py`, `price_l3q.py`, `combine.py` (+ `combine.out`, `combine.json`, `res_final.json`, `price_final.json`,
`rows_final.txt`, `spec_final.json`, `kpriv_kc.txt` = kpriv v3 kc lines, `pair60_grid3.txt`, `run_final.log`).
