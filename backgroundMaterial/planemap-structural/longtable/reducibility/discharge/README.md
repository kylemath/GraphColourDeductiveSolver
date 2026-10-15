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

## 7. What a census-independent discharging check needs (resumed session, added 14 Oct 2026 13:15 MDT) [exploratory]

The LPs of §4 only constrain *observed* local types, so even t ≤ 0 would be the census check again. A real proof
checks the rules on *every possible* neighbourhood. For the rule shapes used here (a 5 sends σ to a vertex of
degree ≥ 7 at distance ≤ 2) the check splits into two finite lists.

**(a) Sender list = 2-ball keys (radius 2 around the 5).** What a 5 sends depends on its 2-ball key alone
(models `simple` and `face`; `d3` needs the 3-ball). So the sender inequality "every 5 not in R sends ≥ 1" is a
check over 2-ball keys, not over graphs. Two facts make the list finite and small at the bottom:
- A 2-ball with **no** vertex of degree ≥ 7 is always in R. Its first-ring word is a W12 wheel (every {5,6} word except
  66666), or it is S66.
- Keys with many big vertices send ≥ 1 under any reasonable σ. So the list is "keys with at most K big vertices".

Degree 9+ is not enumerated: the rules must send it 1 anyway, because second-ring 9s are 0/803 D-reducible.

`nbhd.py DMAX K` enumerates every canonical key with degrees 5..DMAX and ≤ K big vertices. It drops keys with a
diamond or 2.122 among interior vertices and classifies the rest (`out/nbhd-8-1.txt`, `out/nbhd-8-2.txt`; untested
keys in `out/sender-untested-K1.txt` and `out/sender-untested-K2.txt.gz`, as lines `ring key nbig`). DMAX = 8:

| big vertices in the 2-ball | canonical keys | W12 / diamond-2.122 / S66 (in R for free) | tested D-red. | tested **not** D-red. | untested (rings) |
|---|---|---|---|---|---|
| 0 | 888 | 888 | – | 0 | 0 |
| 1 | 22,428 | 17,439 | 1,915 | **165** | 2,909 (9–19; 552 at ≥ 15) |
| 2 | 310,968 | 195,201 | 9,024 | 1,539 | 105,204 (9–23; 55,900 at ≥ 15) |

**Single-big-vertex keys (the bottom of the sender list), by where the big vertex sits:**

| big vertex | D-reducible | not D-reducible | untested |
|---|---|---|---|
| 7 in the first ring (66667 with the rest 5/6) | 830 | 0 | 545 |
| 7 at a private second-ring position | 170 | 0 | 1 (`b6666666676`, ring 16) |
| 7 at a shared second-ring position | 188 | 0 | 1 (`b6666666667`, ring 16) |
| 8 in the first ring | 544 | 0 | 2,350 |
| 8 at a private second-ring position | 0 | **165** (all 66666, Job 9) | 6 |
| 8 at a shared second-ring position | 183 | 0 | 6 |

Reading:
- **Every tested single-7 2-ball is D-reducible (1,188/1,188).** The only untested single-7 2-balls with a
  second-ring 7 are the two ring-16 keys of the §4 LP certificate (Studio Job 13).
- **A lone private 8 is a hard sender.** The 165 non-reducible single-big keys are all 66666 holes whose only big
  vertex is one degree-8 vertex at a private second-ring position. Such a 5 must send its whole unit to that 8.
  The 8 has charge −2, so it can absorb at most two of them.
- The first census-independent question is therefore finite and concrete: **how many 5s of this kind (66666,
  second ring all ≤ 6 except one private 8) can lie at distance 2 from one degree-8 vertex?** If the answer is ≤ 2,
  the rule "send 1 to the lone 8" is valid. If not, those 8-centred patches must go into R as 3-balls.

**(b) Receiver list = neighbourhoods of a vertex u of degree d ≥ 7.**
- What u receives is fixed by its radius-2 neighbourhood (degrees and face structure). Whether each nearby 5 is in R
  depends on that 5's own 2-ball, i.e. radius 4 around u.
- The standard relaxation, as in RSST's cartwheels, keeps only radius 2 around u. A 5 is treated as possibly non-R
  unless its R-membership is already decided inside that radius, e.g. by its wheel word or the single-big-vertex
  flatness that the sender list forces.
- Raw radius-2 patterns are about 4^(d + Σ(deg x − 4)), around 10^12 for d = 7. But the receiver inequality is
  additive around u's link, so a cyclic transfer-matrix DP over consecutive neighbours handles each d in seconds.
  This half is cheap. Its strength depends entirely on how much of R is visible at radius 2.
- The `d3` model (distance 3) moves both lists to radius 3. The sender list becomes 3-balls (far larger; no count
  attempted). The census LP gives no reason to pay for that: `lp2-d3-census` is degenerate (t = 0) in the same way
  as `simple` and `face`.

**Does it fit on the Studio?** These estimates use dfast timings from Job 9 (≈ 0.25 s at ring 12, 1 s at 13,
3.4 s at 14, 15 s at 15, 44 s at 16, ≈ 3 min at 17).
- **K = 1 (2,909 untested keys):** about 4 CPU-h for rings ≤ 16; 49 keys at rings 17–19 need dfast's r ≤ 16 guard lifted. This is feasible now, and it settles the single-big bottom of the
  sender list.
- **K ≤ 2 (108,113 untested keys):**
  - rings ≤ 16 (90,546 keys) take about 330 CPU-h, roughly 1–2 days on a 16-core Studio;
  - rings 17–23 (17,567 keys) need dfast's r ≤ 16 guard lifted, at ≥ 3 min each (≥ 900 CPU-h).

  This is borderline. It is worth doing only after (a)'s lone-8 question and a K = 1 LP show that rules of this shape
  can close.
- D-reducibility only: a "not D-reducible" key may still be C-reducible.

**Recommended next Studio job (after Job 13):**
1. Run dfast on `out/sender-untested-K1.txt` (2,909 keys, ≈ 4 CPU-h; ring 17–19: 49 keys need the guard lifted).
2. Long Table, in parallel: an exact enumeration of the lone-8 receiver question above, and an LP whose sender rows
   are the **complete** K ≤ 1 key list (not census samples), with receiver rows from the transfer-matrix relaxation.
   That is the first LP in this folder whose feasibility would mean something beyond the census.

Scripts from this session: `oos.py` (out-of-sample test, used in §3), `mk_c15.py` (census ring-15 keys → dfast
parts; 17 keys, not run), the `d3` model in `lp.py` (§4), and `nbhd.py` (this section).

## 8. B8b: the lone-8 question exactly, and an LP over the complete K ≤ 1 key list (14 Oct 2026) [exploratory]

Files in `b8b/` (scripts) and `b8b/out/` (outputs).

### 8.0 Pre-registration (written 13:22 MDT)

**Chronology note.** Before this section was written, two preparatory runs were made (13:15–13:22):
`b8b/k1keys.py` (re-derives the §7 K ≤ 1 table with the position of the big vertex; counts identical to §7), and one
construction test (`b8b/rings.py`, the "8-hemisphere" below), run to check that the layered builder works. That test
already bears on H8a, so H8a is not blind. Everything after 13:22 follows this text.

**Reduction (stated before computing).** In a K ≤ 1 sender the only vertex of degree ≥ 7 within distance 2 is the
receiver u. So any rule of the §4/§7 shape must send that sender's whole unit to u: in an LP over the K ≤ 1 list the
sender weights are forced (σ = 1), and the receiver row of a degree-d vertex is 6 − d + (number of K = 1 non-R senders
whose lone big vertex is u). **The K ≤ 1 LP is feasible iff every vertex of degree d ≥ 7 has at most d − 6 such
senders.** Task 2 is therefore a counting problem, and it is the same count as task 1.

**Structural bound (proved before computing).** For a receiver u of degree d, a 66666 sender v with u as its only
big vertex lies at distance 2. (a) It is not adjacent to two non-consecutive link vertices (that would make a
separating 4-cycle, since the link of u is an induced cycle). (b) If it sees one link vertex w (private position), w
has degree exactly 6 and v is w's single private second-ring neighbour. (c) Two such senders are not adjacent (each
is 66666). The second ring of u is a cycle of length Σ(deg w − 4) ≤ 2d with these senders an independent set, so
there are **at most d of them**.

- **H8a (lone-8).** An 8 has at most 2 lone-8 66666 senders that are not in R. *Kill:* one explicit class graph
  (min degree 5, no separating 3-, 4-, nontrivial 5-cycle, `ball.class_check`) with ≥ 3, each key tested not
  D-reducible (or untested, for case (a)). If killed, report the maximum (upper bound above + a matching example).
- **H8b (degree 7).** In case (b) (untested keys excluded) a 7 has no K = 1 sender at all; in case (a) at most 1.
  *Kill:* a class graph with a 7 carrying ≥ 2 lone-7 senders whose keys are untested (case a) or tested non-D (case b).
- **H8c (mixed K = 1 around an 8).** Allowing every K = 1 non-R position (first ring, private, shared), the count is
  still ≤ 2. *Kill:* as H8a.
- **H8d (d ≥ 9).** The d-hemisphere (u of degree d, link all 6, its d private second-ring vertices of degree 5,
  everything else 6 out to radius 4) has d senders whose keys contain a private d ≥ 9 and are therefore expected not
  D-reducible (§3: 0/803 with a second-ring 9). *Kill:* dfast finds the d = 9 hemisphere key D-reducible.
- **LP verdict rule.** Case (a)/(b) feasible iff the counts satisfy ≤ d − 6 for d = 7, 8 and the d ≥ 9 bound;
  otherwise report the binding sender type and receiver arrangement (the dual certificate is the receiver row with
  the most senders and the sender rows feeding it).
- **H8e (added 13:31 MDT, before running).** Every 8-centred 2-ball (link and second ring of degree 5/6; free
  completion, ring = third ring of the 8) that has ≥ 3 relaxed private 66666 senders and ring ≤ 15 is D-reducible
  (2,942 configurations, `b8b/centred_cfg.py 8 3`). *Kill:* any D=false. Expectation: most are D-reducible (the 8's
  own 2-ball in the 8-hemisphere was found D-reducible at ring 16, depth 1, at 13:29), but some low-sender or
  6-rich ones may fail.

### 8.1 Lone-8 verdict: yes, up to 8, and the maximum is 8

**Upper bound, every degree d (proof).** Write u's neighbourhood as d blocks (w_i, its private second-ring vertex
p_i if deg w_i = 6, the shared vertex s_i). A K = 1 sender whose only big vertex is u is either a degree-5 link vertex
w_i, or a degree-5 second-ring vertex. A second-ring sender has no neighbour of degree ≥ 7 other than u, so its word
lies in {5,6}^5 and, not being W12, is 66666. Hence: in a block with deg w_i = 6, p_i and s_i are adjacent, so at most
one of them is a sender, and w_i is not one. In a block with deg w_i = 5, s_i is adjacent to w_i, so s_i is not
66666. A link vertex of degree ≥ 7 has no sender in its block (its ring-2 vertices see it, and it is big). **So each
block holds at most one sender: at most d lone-u senders in all, of any K = 1 type.** `b8b/maxsend.py`
(exhaustive over the block model, d = 7, 8, 9) confirms that d is the relaxed maximum and lists the arrangements
(`b8b/out/maxsend.txt`).

**Matching example: the 8-hemisphere** (`b8b/lone8.py`, graph `hemi8` in `b8b/out/patches.txt`, n = 98). u has
degree 8, all link vertices have degree 6, the 8 private second-ring vertices p_i have degree 5, and everything else
has degree 6 out to a cylinder of circumference 16, closed by a mirror cap. `ball.class_check`: minimum degree 5, no
separating 3- or 4-cycle, no nontrivial separating 5-cycle; no diamond or 2.122. All 8 p_i are 66666 holes whose
2-ball has u as its only big vertex, all with key `6:5:6|6:6:6|6:6:6|6:5:6|6:8:6` = Job 9 `b5666665686`, ring 15,
**tested not D-reducible** (Job 9; re-run here with the local dfast: D=false, same class counts,
`b8b/out/hemi8key.cfg`). So **8 hard senders around one 8, in both case (a) and case (b)**. H8a is killed.

**A stronger consequence (unexpected).** The mirror cap is the same, so **all 16 degree-5 vertices of hemi8 have this
tested non-D-reducible 2-ball**. hemi8 is a class graph in which no degree-5 vertex has a D-reducible 2-ball (of any
radius-2 kind: W12, S66, J9, EXT, diamond). So *no* family of D-reducible 5-centred 2-balls is unavoidable, whatever
the untested keys turn out to be. This corrects the §3 remark "no graph anywhere has every hole tested
non-reducible" (it was true of the census and the §3 constructions). hemi9 (n = 110, u of degree 9, 18 holes, key
`…|6:9:6`, ring 16) is a second such graph: dfast D=false (`b8b/out/hemi9key.out`). D-reducibility only. C-reducibility
of `b5666665686` has not been tested.

**What does reduce it.** The 8's own 2-ball in hemi8 (25 vertices, ring 16 = third ring of u) **is D-reducible**
(dfast D=true, depth 1, 63 s; `b8b/out/hemi8_ball2.cfg`, `.out`). The obstruction disappears once R contains
receiver-centred configurations.

**Degree 7 (H8b).**
- *Case (b):* the complete K = 1 list has no tested non-D lone-7 key, so a 7 has **0** case-(b) senders.
  H8b(b) survives.
- *Case (a):* there are 547 untested lone-7 keys (545 first-ring, plus the two ring-16 keys of Job 13). An explicit
  class graph has **3** untested lone-7 senders around one 7: `alt7_024`, n = 94, three flat keys `b6666666676`
  (ring 16, Job 13). Another 60 block-model arrangements, closed into class graphs by `b8b/search7.py`
  (`b8b/out/search7.txt`), reach at most 3. H8b(a) is killed: 3 > 1.
- The 7-hemisphere's key (`…|6:7:6`) is D-reducible, so it gives no senders.

**Mixed K = 1 senders around an 8 (H8c).** In case (b) the only non-R lone-8 keys are the 165 private-8 66666 keys,
so the mixed count equals the 66666 count: max 8. In case (a) the bound is still 8, so H8c is killed by hemi8. In
`alt8_0246` (n = 126) four untested senders with the flat private-8 key `6:6:6|6:6:6|6:6:6|6:6:6|6:8:6` (ring 17) sit around one 8.

### 8.2 LP over the complete K ≤ 1 key list (`b8b/lp_k1.py`, `b8b/out/lp_k1.txt`)

Sender rows are **all** non-R K = 1 keys: 3,074 in case (a) (545 + 2 lone-7, 2,350 + 6 + 6 untested and 165 notD
lone-8), and 165 in case (b). Receiver rows come from the explicit class graphs above (28 rows), and the proved
bound (≤ d senders) closes the rest in closed form.

| case | t* | certificate (dual weights) |
|---|---|---|
| (a) untested = not in R | **2/3** (explicit rows; ≤ 3/4 from the bound, = 2/3 unless some 7 has ≥ 6 case-(a) senders) | 8/9 on sender `b5666665686` (key `6:5:6\|6:6:6\|6:6:6\|6:5:6\|6:8:6`), 1/9 on receiver hemi8 (deg 8, 8 senders) |
| (b) untested excluded | **2/3 exactly** (d = 7: no senders; d = 8: ≤ 8 senders; d ≥ 9: ≤ d, which gives t ≤ 6/(d+1) ≤ 0.6) | the same two rows |

Both LPs are infeasible. The binding pair is the same in both. A lone-8 sender must send its whole unit to the 8:
σ ≥ 1 − t. Eight of them fit around one 8: −2 + 8σ ≤ t. Together these give t ≥ 2/3. No choice of K ≤ 1 rule weights
can fix this, because the sender weights are forced (§8.0, reduction). For d ≥ 9, the d-hemisphere gives d senders
(the d = 9 key was tested: not D-reducible). A lone big vertex of any degree d ≥ 8 can therefore end at 6 − d + d = 6
under "send 1 to the lone big vertex".

### 8.3 Receiver-centred configurations (H8e)

Since 5-centred D-reducible 2-balls are avoidable (hemi8), R needs configurations centred on the receiver. The
u-centred 2-ball (u, its link, and its second ring; ring = third ring of u) is the natural first piece.
`b8b/centred.py` counts, in the block model, the 8-centred 2-balls with more than d − 6 = 2 relaxed senders:

| centre | relaxed senders counted | 2-balls with > d − 6 senders (canonical) | rings |
|---|---|---|---|
| 8, case (b) | private 66666 only (the only notD lone-8 type) | **3,974** | 7–21 (2,942 at ≤ 15; 486 at 16; 546 at 17–21) |
| 8, case (a) | all K = 1 types | 88,149 | 0–21 |
| 7, case (a) | all K = 1 types (W12 link words removed) | 16,450 | 3–19 |
| 7, case (b) | — | 0 needed | |
| 9 | all K = 1 types | 393,749 | 0–23 |

(`b8b/out/centred.txt`. These are relaxed counts: they ignore whether the senders' actual keys are in R, so they
over-count.)

**H8e result (dfast, 4 niced processes, `b8b/run_c8.sh`, `b8b/out/dres-c8.txt`):** (interim, 14:15 MDT) rings 7–14: **2,281 / 2,281 D-reducible**; ring 15: 116 / 116 D-reducible so far, run continuing.

### 8.4 What remains for a census-independent unavoidability proof

1. **R itself has to change.** hemi8 and hemi9 have no D-reducible 5-centred 2-ball. Either C-reducibility rescues
   `b5666665686` (ring 15) and `…|6:9:6` (ring 16), or R must contain receiver-centred configurations (8.3). This
   comes first, because no rule weights can fix it.
2. **Receiver-centred families:**
   - d = 8: 3,974 configurations in case (b) (8.3); 88,149 in case (a) unless the 2,909 untested K = 1 keys are
     tested.
   - d = 7: none in case (b); 16,450 relaxed in case (a).
   - d = 9: up to 393,749.
   - **d ≥ 10:** the family is unbounded in d. The d-hemisphere has d senders and a centred ring of 2d, which is
     beyond dfast for d ≥ 9. It needs a general argument, for example a rule that sends a lone-d sender only
     σ ≤ 1 − 6/d together with C-reducibility of the d-private 66666 2-ball. Or it needs larger-radius rules. No
     size estimate is possible for the enumeration route.
3. **Senders with K ≥ 2** (DMAX 8, §7): 105,204 untested and 1,539 tested not D-reducible. Their weights are no
   longer forced, so this is a real LP. Receiver rows then mix K = 1 and K = 2 senders. The ≤ 1-sender-per-block bound
   still holds for 66666 senders, but not for all K = 2 senders. The receiver DP of §7 is the right tool; it is not
   built yet.
4. **Big degrees ≥ 9 in sender keys:** not enumerated; every degree d ≥ 9 is another sender list. The §3 evidence
   (0/803 D-reducible with a second-ring 9) says these are all hard senders.
5. **Regularity:** "appears" is still checked as a regular 2-ball with an injective ring. The block model assumes
   that u's second ring is a simple cycle; 8.0 proves the link is an induced cycle. That the second ring is simple and has no chord is assumed, not proved, though every explicit graph here satisfies it.

## 9. Job 18 (Studio, 14 Oct 2026): the K ≤ 1 LP with w66666 in R [exploratory]

### 9.0 Pre-registration (written 16:26 MDT, before the re-run)

- **New R.** R is the old R, plus every key whose centre has first-ring word 66666 (the C-reducible w66666 wheel;
  Job 16, Lean-checked computational half), plus every key that Job 14 or Job 13 found D-reducible
  (`out/dres-K1-studio.txt`, `studio13/dres-r15-16-studio.txt`).
- **H18a.** With the 47 deferred ring 17–19 keys counted as non-R, the K ≤ 1 LP is feasible, t* ≤ 0. The non-R senders
  are then only those 47 keys.
- **H18b.** With the deferred keys excluded, there are no non-R K = 1 senders at all, so t* ≤ 0 trivially.
- **Kill.** t* > 0 in case (a'). Report the binding pair.

### 9.1 Result (`b8b/lp_k1_v2.py`, `b8b/out/lp_k1_v2.txt`)

**Status changes in the K = 1 list (22,428 keys).** 165 notD → R: all lone private-8 keys are 66666-centred.
2,862 untested → R: Job 14 found them D-reducible, or they are 66666-centred. 47 stay untested: rings 17–19, deferred.
19,354 were already in R.

| case | non-R K = 1 senders | t* | reading |
|---|---|---|---|
| (b') untested excluded | **0** | ≤ 0 trivially | every 5 whose 2-ball has at most one vertex of degree ≥ 7 is in R (D-reducible 2-ball, or a 66666 hole). **H18b survives.** |
| (a') untested = non-R | 47 (46 lone-8 at a first-ring position, 1 lone-7) | 0 on the explicit receiver rows (no explicit graph contains these keys) | not settled. By the proved block bound an 8 could hold up to 8 such senders, giving t ≤ 2/3, and a 7 up to 7 (t ≤ 3/4), unless those keys are reducible or cannot co-occur. |

**Reading.**
- The obstruction of §8.2 (t* = 2/3 from hemi8) **disappears**. Its 165 lone-8 senders were all 66666 holes, which are
  now in R through the w66666 C-reduction.
- The K ≤ 1 bottom of the sender list now hinges only on the 47 deferred ring 17–19 keys
  (`studio14/deferred_r17_19.txt`). Testing them takes about 3–4 CPU-h with dfast18, plus a Lean validation of the
  p ≤ 9 table on a few ring-17 cases. If they are all D-reducible, the K ≤ 1 LP is feasible without any explicit
  receiver rows.
- The H8e 8-centred run (rings ≥ 16) is not needed for K ≤ 1. Case (b') has no senders at all.

**K ≤ 2 (not run; size only).**
- 108,113 untested keys, of which 107,279 are not 66666-centred. 89,986 of those have ring ≤ 16 (about 330 CPU-h
  with dfast); 17,293 have rings 17–23.
- The 66666 reclassification removes only 834 of them, because most K = 2 keys have a big vertex in the first ring.
- The receiver DP of §8.4 item 3 is not built. With K = 2 the sender weights are no longer forced, so this is a real
  LP over about 107k sender rows plus DP receiver rows.
- Recommendation: first test the 47 deferred K = 1 keys. Then decide whether to spend the ~330 CPU-h on K = 2.

## 10. Job 22 (Studio, 15 Oct 2026): K ≤ 1 / K ≤ 2 with the certified C wheels in R [exploratory]

### 10.0 Pre-registration (written 23:37 MDT 14 Oct, before the run; script `b8b/k2size_v3.py`)

- **New R.** The Job 18 R, plus the studio14b dfast18 results (47 deferred ring 17–19 keys D), plus 2-balls that
  contain a Lean-certified C wheel (Job 21, `dcheck/CWheels.lean`; the six 565xxx 6-wheels are excluded,
  `studio17/UNCERTIFIED.md`): as the centre's wheel (11 C 5-wheels: `Rc`), or as the full link of a first-ring
  vertex of degree 5 or 6 (66666, the 11 C 5-wheels, the 6 certified 6-wheels: `Rx`).
- **H22a (K ≤ 1).** There are no non-R K = 1 keys, so t* ≤ 0 trivially (engine level; Lean level waits for studio14c
  and the ring-19 key). *Kill:* any non-R K = 1 key.
- **H22b (K ≤ 2 sizing; a prediction, not a claim).** The C wheels remove fewer than 20% of the 107,279 non-66666
  untested K = 2 keys, because most K = 2 keys carry a big vertex in the first ring. *Kill:* ≥ 20% removed.
- Sanity: with the C wheels switched off, the K = 1 and K = 2 counts must reproduce §9.1 (22,428 K = 1 keys; 108,113
  untested K = 2 keys) up to the studio14b reclassification.

### 10.1 Result (`b8b/out/k2size_v3.txt`; sanity run with the C wheels off: `b8b/out/k2size_v3_noC.txt`)

| | K = 1 keys | K = 2 keys | K = 2 non-R (U + notD) | of which untested, ring ≤ 16 / ≥ 17 |
|---|---|---|---|---|
| C wheels off | 22,428, all R | 310,968 | 104,650 (104,287 U + 363 notD) | 87,041 / 17,246 |
| C wheels on | 22,428, all R | 310,968 | **92,771** (92,447 U + 324 notD) | **75,793 / 16,654** |

- **H22a survives (engine level).** Every K = 1 key is in R: 22,428 keys, the same count as §9.1. The 47 deferred
  keys are D by dfast18 (`studio14b/RESULT.md`). Lean level: 3 of the 47 done; 43 (rings 17–18) running as
  `studio14c`; the ring-19 key (`6:6:6|6:6:6|6:6:6|6:6:6|8:666:6`) is not scheduled (about 165 h on one core).
- **H22b survives.** The certified C wheels remove 11,879 of the 104,650 non-R K = 2 keys (11.4% < 20%):
  1,254 by the centre's wheel (`Rc`) and 10,625 by a first-ring link (`Rx`). `Rx` is a sub-configuration argument
  (the first-ring vertex's whole link lies in the 2-ball); it should be checked by Long Table before it is used.
- **K = 2 cost (dfast18, measured per-ring means 13: 1 s, 14: 4 s, 15: 18 s, 16: 103 s, 17: 621 s, 18: 3,967 s,
  19: 19,736 s).** Ring ≤ 16: about **560 CPU-h** (75,793 keys). Rings 17–19: about **16,500 CPU-h** (16,018 keys).
  Rings 20–23: 636 keys, no timing (expect several times the ring-19 cost each). So a full K = 2 dfast18 pass is
  not feasible on this box; ring ≤ 16 is (about 2 days on 12 cores).
- **Discrepancy with §9.1.** With the C wheels and the Studio D results both off, this enumeration (the k1keys.py
  code with ≤ 2 big vertices) gives 104,743 non-66666 non-R K = 2 keys, against 107,279 in §9.1. The K = 1 counts
  agree exactly. The §9.1 sizing script was not committed, so the 2,536-key gap is not explained.
- Not done: the K = 2 LP itself (receiver DP of §8.4 item 3 not built).
