# Track B: unavoidable hole types in the frame class [exploratory]

Track B agent, 7 Oct 2026, on the Mac Studio. Nothing in this directory is committed. Each claim is labelled **hand**, **data**, **computer-certified** (an exact rational certificate rechecked by a second script), or **conjecture**.

## Question
Frame class: connected spherical triangulations with min degree 5, NoSep, and no `Occ` of the diamond or of 2.122 in either orientation. The definitions are in FrameF3.lean, `DiamondP/MOcc`, `C2122P/MOcc`.

A **hole type** is the cyclic link-degree word of a degree-5 vertex, taken up to rotation and reflection, with every degree ≥ 8 written as `8+`. We want a small set S of hole types such that every frame-class triangulation has a degree-5 vertex whose type is in S.

The universe has 136 words. 19 of them contain `555` or `565`, which leaves **117 allowed words** (see §2.1). So the trivial S already has about 117 types, which is above the kill threshold of about 100.

## Headline
| | value | label |
|---|---|---|
| Frame-class graphs per order (plantri `-m5 -c4`, every graph) | 12–21: 0; 22: 1; 23: 1; 24: 4; 25: 2; 26: 11; 27: 24; 28: 104 (28 from the existing picyc list, cross-checked) | data |
| Words forced by monotype graphs (all degree-5 vertices have the same word) | 66666, 55666, 56666, 56657, 56658+ | data, exact graphs |
| Rigorous lower bound on any unavoidable S | **9**: nine verified frame-class graphs whose word sets are pairwise disjoint | data |
| Minimum hitting set of all known frame-class graphs (census + 1,267 IPR + 9 bigsample + adversarial witnesses) | 7 on census+IPR; grows to 13 after 325 adversarial witnesses, and is still growing (every round found a witness) | data |
| Best **proved** S (one-step discharging, computer-certified) | **59 allowed words + 19 `555`/`565` words = 78** (59 if an F2-type argument removes the 19) | computer-certified |
| Best proved S, most general one-step word-local rule (5-key, MILP optimum) | **also 59 + 19**, so one-step rules cannot do better | computer-certified |

**Kill-rule verdict: amber, leaning kill.** No S of size ≤ 20 is in sight. The best S we can prove has 59–78 types: not above 100, but far above 20. The data says the true minimum is at least 9, and the adversarial loop keeps raising the empirical minimum (7 → 13), so 20 is not clearly reachable even empirically. Also, PureClean is proved for **none** of these types: every existing local result (F5, weak F6, `pureClean_of_hole4`) needs `555`, which is absent from the frame class.

## 1. Data
### 1.1 Frame-class filter (faithful to the Lean `Occ`)
- `gen_schedule.py` parses the four generated Lean structures (`DiamondPOcc.lean`, `DiamondMOcc.lean`, `C2122POcc.lean`, `C2122MOcc.lean`) and emits `occ_sched.h`: the `Nx` facts, the interior degrees, and a propagation schedule from the seed (int 0, int 1).
- `frame.c` checks every `Occ` field: the `Nx` facts, the interior degrees, and injectivity of the ring and interior together, which also gives disjointness. It runs in both orientations, so the input's rotation direction does not matter.
- It also independently computes, from the graph alone:
  - `AppearFree`: every appearance (`Appears` ![5,5,5,5] / ![6,5,5,5] with induced K4 − e) has unclean tips, as in FrameAppears.lean;
  - `rsstfree`: no appearance at all;
  - NoSep: #triangles = 2n − 4;
  - minimum degree.
- On NoSep triangulations, Lean shows occfree ⇔ appfree (`appearFree_of_free`, and an `Occ` gives a clean appearance). The two computations agree on every graph checked: **0 mismatches** over the full census at orders 12–27 (444,820 graphs), the order-28 list, the IPR and bigsample lists, and all 325 witnesses.
- **TipsClean caveat.** No frame-class graph in any data set has an unclean appearance (`rsstfree = appfree` everywhere). So in the data the frame class equals the RSST class. In theory they can differ: an unclean appearance needs a separating 4-cycle, and F2 is not formalised.
- **Second, independent check.** The repo's own `StudioMathReview-scripts/occ_search.py`, run through `crosscheck_occ_search.py`, gives 0 disagreements on:
  - 196 frame graphs (all 147 census graphs at orders 22–28, 40 witnesses, 9 bigsample), all `Occ`-free;
  - 200 non-frame order-24 graphs, all with an `Occ`.
- The order-27 frame list is identical (same plantri indices) to `local-runs/27-studio-positive-config/in-cfree-27.txt` (picyc `cfree`).
- Orders 28 and up: I did **not** run a new plantri census. A 4-shard background census of orders 28–32 was refused by the permission system because the machine load was about 110–136. The 104 order-28 graphs come from the existing `in-cfree-28.txt` (the picyc census of all 1,160,752 graphs) and were re-verified with `frame.c`. Completeness at order 28 therefore rests on picyc's census.

Outputs: `out/count-small.log` (per-order counts), `out/frame-NN.txt` (frame graphs as rotation lists), `out/frame-ext-*.txt`.

### 1.2 Words at degree-5 vertices (cap 8+)
Full table: `out/words-cap8-base.txt`. Census (147 graphs, orders 22–28), by number of graphs containing each word:

55666 104, 56757 71, 56657 70, 55757 70, 56667 64, 56666 63, 55667 56, 55676 49, 66666 27, 55767 20, 55758+ 19, 56676 17, 56658+ 14, 56758+ 13, 57667 13, 57577 12, 55677 5, 558+58+ 4, 57758+ 3, 66667 2, 568+57 1, 56767 1.

That is 22 distinct words in the census and 83 once the witnesses are included.

- **Forced (monotype) words, data:**
  - 55666 (p22#196, the order-22 graph; also p24#2550, p26#20634, ...);
  - 56657 (p23#598);
  - 56658+ (p26#5298);
  - 56666 (p27#129338, ...);
  - 66666 (all 1,267 IPR duals, n = 32–52).
  
  Each of these words must be in every unavoidable S.
- **Common but not forced:** 56757, 55757, 56667, 55667, 55676. They are frequent, but no graph has them alone.
- **Packing bound (rigorous lower bound, data, `packing.py`): 9.** Nine verified frame-class graphs have pairwise disjoint word sets:
  - the five monotype graphs above;
  - p28#213130 {55758+, 55767, 558+58+};
  - p28#228371 {55757, 57577};
  - two adversarial witnesses.
  
  So |S| ≥ 9.
- **Hitting sets:**
  - census + IPR + bigsample: exact minimum 7, {55666, 55757, 55767, 56657, 56658+, 56666, 66666}; greedy also finds 7.
  - With cap 7+, the minimum is 8 and the packing bound is 7.

### 1.3 Adversarial loop (is the data's hitting set really unavoidable?)
**Method** (`avoid.py`, `iterate.py`; single process, nice 10):
- Simulated annealing over edge flips at fixed order. It keeps min degree ≥ 5 and NoSep as hard constraints, and penalises clean appearances and degree-5 vertices whose word is in S.
- Every witness is re-verified with `frame.c` (the Lean `Occ` matcher).
- Each round recomputes the exact minimum hitting set over all known graphs, then searches for a frame-class graph that avoids it.

**Result (data):**
- The 7-word census set is **avoidable**: witnesses at n = 51, 52, 60 were found within seconds.
- Over 325 rounds (two runs, 25 + 300) the minimum hitting set grew 7 → 8 → 9 → 10 → 11 → 12 → 13 (rounds per size: 2, 6, 25, 26, 70, 111, 85+). **Every round found a witness**, so the loop had not converged when it stopped. Final round's set: {55666, 55668+, 55677, 55757, 55758+, 55767, 56657, 56658+, 56666, 56667, 56757, 56758+, 66666}.
- Witnesses have orders 42–60 (mostly perturbed IPR duals). They are in `out/witness-cap8.txt`, with the log in `out/iterate-cap8.log`.
- Interpretation (conjecture): the true minimum S is clearly above 9, plausibly in the teens to 20s, and the search only explores n ≤ 60. With higher-degree vertices at larger n, more words become avoidable.

## 2. Theory
### 2.1 Hand facts
- **(hand)** Euler: Σ(6 − deg) = 12, so degree-5 vertices exist.
- **(hand)** Suppose a degree-5 vertex v has three consecutive link degrees 5,5,5 (or 5,6,5). Then v and its middle neighbour are the centres of an appearance of the diamond (or of 2.122, with the degree-6 vertex as int 0). The tips are non-adjacent by NoSep: adjacent tips would form a non-facial triangle through v. With clean tips, Lean's bridge (`occ_of_appears`) gives an `Occ`. So in the frame class a `555` or `565` word forces unclean tips, which means a separating 4-cycle tip–v–tip–x. Without F2 these 19 words cannot be dropped; with F2 they never occur.
- **(hand / literature)** IPR fullerene duals give infinitely many frame-class triangulations whose only word is 66666: there are no adjacent 5s, so no diamond or 2.122, and fullerene duals have no separating triangles. Hence 66666 ∈ S for any S. Data: all 1,267 IPR duals 32–52 pass `frame.c`.

### 2.2 One-step discharging (computer-certified)
Rule family (`discharge_lp.py`): a degree-5 vertex v sends to each neighbour u of degree ≥ 7 an amount σ(p, D, q), where:
- D = min(deg u, 8);
- p and q are the capped degrees of the two common neighbours of v and u, that is, the two letters next to u in v's word.

So what v sends depends only on its capped word. Receiver side:
- a degree-7 vertex receives at most 1: all 4^7 link sequences are enumerated;
- a vertex of degree ≥ 8 receives at most d/4 ≤ d − 6, by a potential certificate showing that the order-2 de Bruijn cycle mean is ≤ 1/4.

So if every degree-5 vertex sends at least 1, the total charge is ≤ 0 < 12. Hence **S_σ = {w : sent(w) < 1} is unavoidable in every min-degree-5 triangulation**. This uses neither NoSep nor `Occ`-freeness.

The MILP minimises |S_σ|. Optimal σ, all values in {1/8, 1/6, 1/4, 1/3, 3/8, 11/24, 1/2}; full table in `out/discharge-frameonly.json`:
- D = 7: (5,7,6) 1/8; (5,7,7), (5,7,8) 1/6; (6,7,6), (6,7,7), (6,7,8), (7,7,7), (7,7,8) 1/3; (8,7,8) 1/4; (5,7,5) 0.
- D = 8+: (5,8,5) 1/4; (5,8,6) 1/3; (5,8,7), (5,8,8) 3/8; (6,8,6), (6,8,7), (6,8,8), (7,8,7) 1/2; (7,8,8) 11/24; (8,8,8) 1/4.

**Result: |S| = 59 allowed words + 19 `555`/`565` words = 78.**
- Exactly re-verified in rational arithmetic by `check_cert.py`: d = 7 maximum receipt exactly 1, the potential inequalities hold, and S is recomputed exactly.
- Validated on graphs by `verify_discharge.py`: 0 violations on 1,624 frame-class graphs and on all 10,221 min-degree-5 4-connected triangulations of orders 12–24. Every vertex of degree ≥ 7 ends ≤ 0, and every degree-5 vertex outside S ends ≤ 0.
- S (allowed part): every word with no letter ≥ 7, and most words with one or two letters ≥ 7 (list in the JSON).
- Why this family cannot do better: a degree-7 vertex can have up to seven degree-5 neighbours, and a 7-vertex with three isolated 5-neighbours caps σ(6,7,6) at 1/3. So a degree-5 vertex with at most two neighbours of degree ≥ 7 rarely reaches 1.

### 2.3 General one-step word-local rule (5-key)
`discharge_lp2.py` lets the amount depend on v's whole capped word, read from u: σ[D; a, b, c, e]. The receiver condition at d = 7 is then over the link together with the outer apexes, handled by cutting planes with exact max-plus DP separation; d ≥ 8 uses a potential on a 256-state graph. **Result:**
- The MILP optimum is again **59 allowed + 19 = 78**, the same set as §2.2. It needed 56 cutting-plane rounds and 2,200 cuts (`out/discharge2.log`).
- Exact rational re-check: d = 7 maximum receipt = 1, potentials OK, |S| = 78 (`out/check_cert2.log`).
- Graph check: 0 violations on 1,748 frame graphs and on 10,221 min-degree-5 graphs.
- **So 59 (78 without F2) is the limit of any rule in which a 5-vertex's gifts depend only on its own capped word**, given our sufficient receiver condition for degree ≥ 8 (receipt ≤ d/4).

### 2.4 What a real proof would need (conjecture)
Getting from about 59 down to about 15 needs rules that look past the first neighbourhood. Examples:
- relaying through degree-6 vertices;
- charging 7-vertices according to how their 5-neighbours cluster;
- reducible exclusions beyond the two configurations.

The ten most used candidate words are all "5-heavy, ≤ 1 high neighbour" types: 55666, 55757, 56657, 56666, 66666, 56667, 55667, 56757, 55758+, 56658+. Any useful extra reducible configuration would have to kill one of the monotype families, and those families are infinite (IPR → 66666). So a 66666 PureClean argument is unavoidable on any route.

## 3. Kill-rule assessment
- Promising needs |S| ≤ about 20 **with PureClean proved per type**. We have:
  - a lower bound of 9 (data);
  - an empirical minimum of ≥ 13 that is still rising;
  - a proved bound of 59 (78 without F2);
  - PureClean for 0 types.
- Kill needs > about 100 types, or a type with no local handle. The proved S is under 100. But **66666 is in every S**: a degree-5 vertex surrounded by degree-6 vertices, as in an IPR fullerene dual. It has no candidate exclusion, because IPR duals are genuinely in the frame class. Unless someone has a local handle for PureClean at a 66666 hole, the second kill clause is met for that type.
- Verdict: **amber, leaning kill.** The set-size side is borderline. The 66666 type, together with the absence of `555` structure in every S word, makes "PureClean per type" the binding problem.

## 4. Next steps (if continued)
1. Give 66666 holes (and 56666 / 55666) to Track A/C: a PureClean test on IPR duals, as a go/no-go for the whole track.
2. Run the plantri census at orders 29–31 once the load allows. It was refused at load 136; about 4 single-threaded workers for about 1 hour would do it.
3. Run `iterate.py` longer, with seeds at n = 60–120 and degree ≥ 9 moves, to see where the empirical minimum S saturates.
4. Two-step discharging (5 → 6 → 7+ relays) with the same LP and exact-certificate pipeline, to test whether the proved S can fall below about 30.

## Files
| file | purpose |
|---|---|
| `gen_schedule.py` → `occ_sched.h` | Lean Occ structures → C schedule |
| `frame.c` (`frame`) | frame-class filter (Occ, AppearFree, RSST, NoSep) |
| `words.py` | words, frequencies, forced words, greedy/exact hitting sets |
| `packing.py` | disjoint-word-set lower bound, monotype words |
| `avoid.py`, `iterate.py` | adversarial S-avoidance search loop |
| `discharge_lp.py`, `discharge_lp2.py` | discharging MILPs (3-key, 5-key) |
| `check_cert.py` | exact rational certificate check |
| `verify_discharge.py` | rule check on actual graphs |
| `crosscheck_occ_search.py` | independent Occ check with the repo's `occ_search.py` |
| `out/` | all outputs and logs |
