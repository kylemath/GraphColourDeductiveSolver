# B8: is a reducible degree-5 2-ball unavoidable? (Long Table, 14 Oct 2026) [exploratory]

Status: **exploratory**. Data and heuristics only; nothing here is a proof.

## 0. Pre-registration (written 12:15 MDT, before any graph was scanned)

**Class.** Triangulations of the sphere with minimum degree 5, no separating triangle, no separating 4-cycle, and
no nontrivial separating 5-cycle (internally 6-connected). The census lists (`Census29`, `Census33`, orders 22–33)
are additionally diamond-free and 2.122-free (frame filter) and were checked earlier to have no separating 4-cycle
and no nontrivial separating 5-cycle (`../../gluing/GLUING.md`).

**Family R0.**
- the 12 D-reducible first-ring wheels of Studio Job 8 (55555, 55556, 55557, 55566, 55567, 55656, 55657, 56566,
  56567, 55666, 56657, 56666; up to rotation/reflection), and
- the 66666 2-balls whose second ring has all degrees ≤ 6 (78/78 D-reducible, Studio Job 9).

**H0.** Every graph of the class contains a member of R0 at some degree-5 vertex.

**Kill criterion.** One explicit graph of the class (min degree 5, no separating 3-, 4-, nontrivial 5-cycle;
checked by script) in which every degree-5 vertex has a non-reducible wheel word and is not a 66666 hole with
second ring ≤ 6. Expected: H0 is false (the census is diamond/2.122-free and all-5/6 66666 2-balls need a large
flat patch).

**Reporting rule.** Report the fraction of census graphs where H0 fails per order, and the smallest witness
(graph name + order), whether or not H0 survives.

**H1 (secondary, also pre-registered).** R1 = R0 + every D-reducible 66666 2-ball of Job 9 (4,223 patterns, any
second-ring degrees, ring ≤ 15). Same kill criterion with R1 in place of R0.

## 1. Method

- **2-ball key** (`ball.py`). At a degree-5 vertex v with link x_0..x_4: block_k = (deg x_k, degrees of the
  deg x_k − 5 private second-ring neighbours of x_k, degree of s_k shared by x_k and x_{k+1}), canonical under the
  dihedral group. `ball.build(key)` gives the free completion in WheelMain/dfast format (same fan construction as
  Studio `gen_2ball.py`; checked identical to `gen_2ball` on 5,000 66666 configurations, configuration string and
  ring size). Ring r = Σ_private(d − 4) + Σ_shared(d − 5).
- In a graph, `ball_at` also checks that the 2-ball is regular: simple second ring, no chord, every second-ring
  vertex adjacent to exactly the expected first-ring vertices. **All 1,337,323 census holes are regular**, and in
  all 59,660 holes of the H1-failing census graphs the free-completion ring is injective in the graph
  (|N(B₂) \ B₂| = r; `inj.py`).
- D-reducibility: Studio's `dfast` (C++ port of Lean `DCheck.run`), compiled locally, rings ≤ 14 only on the MacBook.
- Census: Census29 orders 22–32 (21,931 graphs) and Census33 order 33 (58,194), all frame-class and internally
  6-connected (GLUING.md). Scan: `scan.py` → `out/scan-*.jsonl.gz`; family test: `h0.py`.
- Constructions (`construct.py`): fullerene duals (IPR 32–60, Goldberg GC up to n = 170), then greedy-random edge
  flips between two degree-6 vertices (5-7 dislocation pairs) next to holes that are still in R, until no hole is
  in R and the graph has no Birkhoff diamond and no 2.122; then `ball.class_check` (min degree 5, no separating
  3-cycle, 4-cycle, nontrivial 5-cycle). Untested 2-balls count as **not** in R (conservative).

## 2. H0 and H1: killed (as expected)

| family | census graphs with no member | smallest |
|---|---|---|
| R0 = W12 + S66 (H0) | **3,065 / 80,125 = 3.83%** (25: 1/2, 26: 4/11, 27: 3/24, 28: 10/104, 29: 8/296, 30: 47, 31: 153, 32: 585, 33: 2,254) | **p25#2111** |
| R1 = R0 + all Job 9 D-reducible 66666 2-balls (H1) | 2,937 / 80,125 = 3.67% | p25#2111 |

**Witness p25#2111** (`Census29/out/frame-25.txt`): class_check: min degree 5, 0 separating triangles, 0 separating
4-cycles, 0 nontrivial separating 5-cycles; diamond- and 2.122-free. Its 18 degree-5 vertices have words 55757
(×12), 56757 (×4) and 57577 (×2); none is a W12 wheel and none is 66666. (It is also the A2 counterexample.)
W12 alone already hits 96% of census graphs (341,027 holes).

## 3. Enlarging R (three rounds; ring ≤ 14 on the MacBook)

| round | source of new keys | keys tested | D-reducible |
|---|---|---|---|
| r1 | every hole of the 2,937 H1-failing census graphs | 10,725 | 9,386 (87.5%) |
| r2 | constructed graphs round 1 (57 graphs, n = 32–170) | 721 | 713 |
| r3 | constructed graphs round 2 (50 graphs) | 556 | 543 |
| cen (LP input) | every remaining census key, ring ≤ 14, not W12 / not Job 9 | 26,066 | 23,761 |
| **all** | | **38,068 distinct keys** | **34,403** |

Results (`out/dres-*.txt`, `out/dstats.txt`):
- **R2 = W12 + S66 + J9 + EXT(r1) is unavoidable on the whole census: 0 / 80,125 graphs miss it** (`out/h2.txt`).
  A greedy cover needs **259 extra keys** (rings 7–13, `out/cover.txt`), a long tail: in-sample only.
- **Out of sample** (`oos.py`, written by a parallel resumed B8 session in this folder): R built from the
  D-reducible keys of orders ≤ 32 (16,428 keys) misses **1 / 58,194** order-33 graphs; from orders ≤ 30 (3,168 keys)
  it misses 31 / 78,504 orders 31–33. The 133-key greedy cover of orders ≤ 32 misses 701 (1.2%) at order 33:
  minimal covers overfit; the family must be described, not listed.
- **No graph anywhere (census or constructed) has every hole tested non-D-reducible.** Every failure so far is
  "untested", never "tested and reducibility fails at every hole".
- **D-rate by maximum second-ring degree, all hole words, ring ≤ 14:** 5 → 12/12, **6 → 6,642/6,642**, 7 → 23,746/23,854
  (99.5%), 8 → 4,003/6,757 (59%), 9 → **0/803**. The Job 9 finding generalises: *every tested 2-ball (any first-ring
  word) whose second ring has no vertex of degree ≥ 7 is D-reducible.* Degree-9 second-ring vertices kill it
  completely (not cross-checked in Lean; worth one spot check).
- D-rate by ring: 8: 245/246, 10: 5,502/5,648, 12: 11,364/12,847, 13: 3,055/4,098, 14: 700/946.

Structural families (census, `out/flat.txt`; constructed, `out/flat-wit.txt`):

| family | census graphs missed | constructed graphs (154) missed |
|---|---|---|
| W12 + {2-balls with second ring ≤ 6} (all tested ones are D-reducible) | 896 / 80,125 (first p26#34638) | 86 (smallest n = 49 with *no* flat-second-ring hole at all) |
| W12 + {D-reducible 2-balls with second ring ≤ 7} | **1** / 80,125 (p30.r8#37968: 24 identical 55858 holes, key ring 9, D-reducible but has an 8) | 31 (n ≥ 60; all have untested ring 12–18 keys) |

So "flat second ring" alone is avoidable (killed), but "D-reducible with second ring ≤ 7, plus the 55858-type
holes" is close to unavoidable on everything tested.

**Constructed graphs.** 154 class-checked, diamond/2.122-free graphs were built over three rounds (`out/wit-r*.txt`,
lines `name+flips n rot #class=...`). After round 3, **146 contain a tested D-reducible 2-ball**; the 8 that do not
(n = 122, 162, Goldberg-based) have only ring ≥ 15 holes, all untested. A fourth construction pass (re-test only,
47 graphs, `wit-r3.txt`) again found graphs whose holes are new keys (417 at ring ≤ 14, prepared in
`out/parts/r4_*.txt`, **not run** — round cap). The adversary always finds new keys; when they are tested ~98% are
D-reducible.

## 4. Discharging LP (`lp.py`)

Charge 6 − deg; every degree-5 vertex sends σ[f] to each vertex of degree ≥ 7 within distance 2 (model `simple`:
f = (distance, capped degree); `face`: distance-1 also by the two face apices, distance-2 by number of common
neighbours; `d3`: distance ≤ 3, added by the parallel session). Rows = distinct observed local types: every non-R
5-vertex (1 − sent ≤ t) and every 7+ vertex whose 5s within the radius are all non-R (6 − d + received ≤ t).
Minimise t; t ≤ 0 = rules exist for all observed R-free types.

| run | t | reading |
|---|---|---|
| R0, census 22–32 (`lp-*-R0-census`) | 0.87–0.89 | infeasible; certificate: 66666 holes seeing a single 7 at distance 2, and 7s surrounded by such holes |
| R2 with complete census keys (`lp2-{simple,face,d3}-census`) | **0** | feasible, but **degenerate**: σ = 1 everywhere; in census graphs (n ≤ 32) R-free receiver neighbourhoods are tiny. Not evidence. |
| R2, census + constructed graphs (`lp2-face-census+wit`) | **0.78** | infeasible. Certificate (dual weight): 66666 holes with one degree-7 vertex at distance 2 sharing 2 (0.44) or 1 (0.33) common neighbours, 66677 holes (0.11), and a degree-7 receiver with 2 + 3 + 4 such senders (0.11). |

**The certificate is the next family.** The 66666 senders in it are exactly **two configurations**: the flat
66666 2-ball with one second-ring vertex raised to 7, at a private position (`b6666666676`, 13 holes) or a shared
one (`b6666666667`, 2 holes). Both have ring 16, just beyond Job 9 (≤ 15); with any 5 added the ring drops to ≤ 15
and Job 9 already covers it. Next come 66677/66667 2-balls (rings 15–18). On the sphere these are what remain when every 5 has its
nearest 7 at distance exactly 2 in an otherwise flat patch.

## 5. Honest reading

- H0 and H1 are false (p25#2111). The reducible wheels plus flat 66666 2-balls are not unavoidable; neither is
  "any 2-ball with a flat second ring" (smallest census miss p26#34638, constructed n = 49).
- With enough D-reducible 2-balls, every census graph and 146/154 constructed graphs contain one, and no graph
  has been found whose holes are all tested non-reducible. But the needed family is large (thousands of keys) and
  keeps growing under adversarial construction; the census alone (n ≤ 33) is too small to support a discharging
  argument (LP degenerate there).
- The real obstruction is unchanged from Job 9: second-ring vertices of degree ≥ 8 (59%, 0% for 9) and large
  rings (≥ 15) around 6/7-rich holes. A proof along this route needs either (a) C-reducibility for those, or
  (b) 3-balls, or (c) a discharging rule that moves charge from 5s to 8+/9+ at distance 2 strongly enough that
  such holes need not be reducible.
- Caveats: D-reducibility only (no C-reducibility); "appears" checked as regular 2-ball with injective ring in
  the census, not proved in general; untested = treated as not reducible; LP rows are observed types, not all
  types; nothing Lean-confirmed here (dfast agrees with Lean on Job 8/9 data).

## 6. For the Studio (`out/studio-keys.txt`, configs via `mkconf.py out/studio-keys.txt RMIN RMAX`)

2,055 untested keys seen in census/constructed graphs: ring 11–14: 417 (constructed round 4) + census; ring 15: 681;
16: 492; 17: 332; 18: 106; 19–21: 27. Most frequent words: 66677, 66667, 56677, 56667, 57677, 66767.
Estimated cost with dfast (≈12 s at ring 15, ≈44 s at 16 on one core; ring 17 ≈ 3 min, needs dfast's r ≤ 16 guard
lifted; ring 18 needs matchings of 18 transitions): about 40 CPU-hours for rings 15–18.

Full enumerations (raw patterns, second-ring degrees 5–8, before symmetry ≈ ÷|Aut word| and 2.122 pruning;
`enum_count.py`): 66666 ring 16: 63,460 (≈6.3k canonical, = B7); 66667: ≤ 14: 60,622, 15: 59,950, 16: 100,298;
66677: ≤ 14: 44,928, 15: 59,268, 16: 116,336; 56667 as 66666; 56677 as 66667.

**Recommended next Studio job:** (1) the two ring-16 configurations `b6666666676` and `b6666666667` (flat 66666 +
one 7; the LP certificate; ≈ 1 min each in dfast; they are in Job 9's `configs_2ball.txt` naming), then the 1,621
constructed-graph keys at rings 15–16; (2) a Lean spot-check of
the "degree-9 second-ring vertex ⇒ never D-reducible" pattern and of ~20 ring-13/14 EXT positives; (3) then rerun
`construct.py` + `lp.py` with the enlarged family.

## Files

`ball.py` (keys, build, class check), `scan.py`, `h0.py` (family test), `cover.py`, `inj.py`, `construct.py`,
`nextround.py`, `witcheck.py`, `run_round.sh` (4 × nice dfast), `lp.py`, `enum_count.py`, `mkconf.py`;
`oos.py`, `mk_c15.py` and the `d3` LP model were added by a parallel resumed session. Outputs in `out/`
(`out/parts/` and the `dfast` binary are git-ignored).
