# Track J: near-rigid LPC [hand, unreviewed] + [data]

Studio, 8 Oct 2026. Nothing outside `TrackJ/` was changed and nothing is committed. TrackF (`surfaces.py`), TrackH (`th_engine.py`) and TrackI (`ti_chains.py`) code was imported read-only; the main engine `tj_eng.c` is new and independent.

Labels:
- **[hand, unreviewed]**: hand proof, not yet independently reviewed.
- **[data]**: computation.

Compute: at most 4 worker processes, all under `nice -n 10` (one short overlap of 5 for about 2 minutes). Load from other users was 11–18. About 2 h 20 min wall time.

**Target** (TrackI §4). *Near-rigid LPC (sphere):* no Kempe class at a degree-5 hole of a triangulated sphere consists only of DL states on all-DL π-cycles with N ≤ 9 at every state. Here N is the total number of Kempe chains.

## 0. Bottom line

1. **Structure [hand, any graph unless stated].** Suppose a near-rigid closed class 𝒦 exists and the chain-parity law holds along it, as it does on the sphere. Then 𝒦 has exactly the following shape (Theorem J5):
   - It is a disjoint union of π-cycles. Each cycle alternates rigid (N = 8) and N = 9 states, and its length is ≡ 0 (mod 10).
   - Every N = 9 state c is **in-shape**: π(c) and π⁻¹(c) are rigid. Its single extra chain Z is a link-free component of the **P1 pair graphs {α,μ} or {A,B}**. This holds because π carries the P2 components of c identically onto the P3 components of π(c) (Lemma J2).
   - Swapping Z, a move written Z(c), is a fixed-point-free involution on the N = 9 states of 𝒦.
   - The Kempe graph of 𝒦 is therefore "π-cycles plus a perfect matching Z on the 9-states", with degree 2 at rigid states and 3 at 9-states. Hence |𝒦| ≥ 20.
   - On the sphere, Z is always an {α,μ}-component [data], so Z(c) = σ(c) up to renaming.
2. **The ladder in general graphs [data]: examples exist at every rung asked for.** Near-rigid closed classes were found with each of the following added in turn. Each rung's examples were checked by an independent engine (TrackH engine + TrackI chain count):

   | rung | condition added | result |
   |---|---|---|
   | (a) | none | exists |
   | (b) | chain-parity law at every step | exists |
   | (c) | G is 4-colourable | exists |
   | (d1) | every edge of G − h in a triangle | exists |
   | (d2) | Track H's H3 edge balance E1 = E2 + 1 = E3 + 1 at every class state | exists |
   | (d) | d1 and d2 together | exists |

   - For (d) there are 43 distinct graphs (n = 34–38, 123–138 edges; `out/examples_rung_d.jsonl`). All 43 were re-verified: law at 20/20 steps, H3 at 20/20 states, 0 edges outside triangles, and 4–6 filled colourings of G − h, so G is 4-colourable.
   - Every law-respecting example has the J5 shape: one 20-cycle, N = 8, 9, 8, 9, …, with the {α,μ} extra chain and Z = π¹⁰ on the 9-states.
   - So **near-rigid LPC is not a consequence of the chain-parity law, local triangles, or the per-partition edge balance.** Like RI, it is a genuinely spherical statement (the "sphere-specific" branch of TrackI §4).
   - The examples are dense: pair-graph cycle ranks of about 10–20, against 0/1 on a sphere.
   - I added one further rung, (e) "sphere edge count |E(G − h)| = 3n − 11". With H3, this forces forests at rigid states. Nothing was found in 9.9M evaluations, but the search barely moved from its seeds (still about 24 edges too many), so this null is uninformative.
3. **Sphere data [data]: nothing comes close.**
   - Exhaustive census 22–32 (frame class, all 357,582 degree-5 holes), plus all of plantri24 and fullerene duals C20–C46 (473,178 holes in total): **0** near-rigid closed classes and **0** π-cycles inside R = {DL states with N ≤ 9}.
   - The longest π-run inside R is **7** (8 holes), against ≥ 10 needed for a cycle. The sphere flip search (0.86M graphs) also reaches 7 and no more.
   - Every sphere all-DL cycle class has at least 10 of its 20 cycle states at N ≥ 10, and at least 80 states off the cycles. Best case: C30#0, with 10 N = 9 states and 10 N = 10 states on one 20-cycle, in a 100-state class with 40 filled states.
   - Contrast: on RP², where neither the law nor RI holds, flip walks (0.93M graphs) reach π-runs of length 11 inside R. They still produced no cycle in R and no near-rigid class.
4. **Proof status: no proof.**
   - **Smallest open claim** (§4): the *near-rigid cycle exclusion* NRC — on a triangulated sphere no π-cycle consists of DL states with N ≤ 9. Equivalently, by Theorem 6, no all-DL π-cycle alternates Tait-rigid and in-shape states.
     - NRC implies near-rigid LPC; closure under Z is not needed.
     - NRC is false in general graphs that satisfy the law, 4-colourability, triangles and H3. So its proof must use planarity itself (Jordan / band surgery), as RI does.
   - A first planar lemma towards it, the **σ-type lemma**: on the sphere the extra chain of an in-shape state is an {α,μ}-component; in Tait form, the free {2,3}-cycle C′ lies on the e₃ side of H₀.
     - Data: **26,481 / 26,481** sphere in-shape states (all 25,800 census ones, plus 681 from the plantri24 / fullerene samples).
     - False in general graphs: 80 of 3,475 in-shape states.

## 1. Task 1: structure of N = 9 states and of a near-rigid class [hand, unreviewed]

### 1.1 Notation

- Link (α, μ, α, A, B) at x_j … x_{j+4}.
- Pair graphs in role order: αμ, AB, αA, μB, αB, μA.
- Partitions: P1 = {αμ | AB}, P2 = {αA | μB}, P3 = {αB | μA}.
- D means ¬inA ∧ ¬inB at a DL state. It holds at every state of an all-DL π-cycle, on any graph (TrackH Lemma H0, with the "s DL" hypothesis added by the TrackH review).
- π = swap of K_{αA}(x_{j+2}). π⁻¹ = π̃ = swap of K_{αB}(x_j), the mirror move, with π̃∘π = id.

### 1.2 Lemmas

**Lemma J1 (link components; any graph).** Let c be DL with D. In each pair graph, the components that meet the link are exactly:
- αμ: one, {x_j, x_{j+1}, x_{j+2}} via the link path;
- AB: one, via the edge x_{j+3}x_{j+4};
- αA: two, K(x_{j+2}) ∋ x_{j+3} and K(x_j), which are distinct by ¬inA;
- μB: one (Lock2);
- αB: two, K(x_j) ∋ x_{j+4} and K(x_{j+2}), which are distinct by ¬inB;
- μA: one (Lock1).

Hence **N(c) = 8 + ℓ(c)**, where ℓ is the number of link-free components (sharpening TrackH H4). Rigid ⇔ ℓ = 0. **N = 9 ⇔ there is exactly one link-free component Z** (the extra chain), lying in exactly one pair graph.

*Proof.* Every link vertex of colour p ∈ {q, r} lies in the listed component of G[{q, r}], and the listed components are distinct by D and the locks. ∎

*Data:* at all N = 9 DL states of the sphere sets (frame 22–29 all, frame-30 1/4, frame-31 1/16, plantri24 1/20, fullerene duals 1/4; 22,328 holes) the excess vector is a unit vector and the extra component is link-free: 336,093 / 336,093 (`X1`). D held at all 4,700,801 DL states.

**Lemma J2 (π-transport; any graph).** Let c be unfilled, π defined, u = π(c). By H0, the roles of u are (α, B, μ, A). Then:
- G[{α, A}] has the same vertex set and the same components in c and in u, and {α, A} = {α_u, B_u};
- G[{μ, B}] is untouched by π, and {μ, B} = {A_u, μ_u}.

Hence **(#αA, #μB)(c) = (#αB, #μA)(π c)**: P2 of c is P3 of π(c), component for component.

*Proof.* π permutes colours inside one component of G[{α, A}], and touches no μ or B vertex. ∎

*Data:* 0 failures in 4,700,801 sphere DL states with π defined (`X2`), and 0 in 27,980 general-graph states.

**Corollary J3 (where the extra chain sits).** Let c be DL with N(c) = 9, and suppose π(c) and π⁻¹(c) are rigid; call such a c *in-shape*. Then Z lies in P1, i.e. Z is a link-free {α,μ}- or {A,B}-component.

*Proof.*
- (#αA, #μB)(c) = (#αB, #μA)(πc) = (2, 1).
- (#αB, #μA)(c) = (#αA, #μB)(π⁻¹c) = (2, 1).
- So the excess is in P1. ∎

*Data:* sphere in-shape states 26,481 / 26,481: 1,907 in the `tj_struct.py` samples (`X3`), and all 25,800 census ones by the engine count `inshape_extraP23` = 0. General graphs: 3,475 / 3,475, as the proof requires. For the stronger, sphere-only statement Z ⊂ {α,μ} see §1.4.

**Lemma J4 (moves at near-rigid states; any graph).**
- *Rigid state:* the Kempe neighbours are π(c) and π⁻¹(c) (TrackH H5).
- *In-shape state with extra chain Z ⊂ G[P1 pair]:*
  - μB and μA are connected, and the other P1 pair graph is connected, so swapping any of them is a renaming;
  - αA has two components, and either swap is π(c) up to renaming;
  - αB likewise gives π⁻¹(c);
  - the P1 pair graph containing Z has two components, Z and the link component L. Swapping L is a renaming composed with swapping Z.

  So the distinct neighbours are exactly **{π(c), π⁻¹(c), Z(c)}**. If Z ⊂ {α,μ}, then L = K_{αμ}(x_{j+2}) and **Z(c) = σ(c)** up to renaming.
- *Properties of Z(c):*
  - Z is link-free, so Z(c) has the same link colours and the same j;
  - Z is still a link-free component of the same pair graph in Z(c), so N(Z c) ≥ 9;
  - Z(Z(c)) = c.

*Data:*
- Kempe degree is 2 at all 66,035 sphere rigid states.
- Every sphere N = 9 state (336,093) has Kempe degree 3 when its extra chain lies in αμ, AB, μB or μA, and 4 when it lies in αA or αB (the extra neighbour is π∘Z or π⁻¹∘Z). See `nine_deg_*` in `out/struct_*.log`.

**Theorem J5 (shape of a near-rigid closed class).** Let 𝒦 be a Kempe class all of whose states lie on all-DL π-cycles with N ≤ 9. Assume the chain-parity law N(πc) − N(c) ≡ [πc DL] (mod 2) holds at every state of 𝒦, as it does on a triangulated sphere (TrackI Theorem 6). Then:

1. **Alternation.** Along every π-cycle of 𝒦, N alternates 8, 9, 8, 9, … (every step is DL → DL, so N flips parity, and 8 ≤ N ≤ 9).
   - j advances by 3 per step, so a cycle has length ≡ 0 (mod 5); with alternation, ≡ 0 (mod 10).
   - 𝒦 cannot be all-rigid (that is RI); half of each cycle has N = 9.
2. **In-shape.** Every 9-state of 𝒦 is in-shape (its π-neighbours have N = 8), so its extra chain Z is in P1 (J3).
3. **Z-matching.** Z(c) ∈ 𝒦 has N = 9 (J4), so Z is a fixed-point-free involution on the 9-states of 𝒦.
4. **Kempe graph.** Up to renaming, the Kempe graph of 𝒦 is (disjoint π-cycles) ∪ (perfect matching Z on the 9-states), with degrees 2 and 3.
5. **Where Z(c) lies.** Z(c) has the same j as c.
   - If Z(c) is on c's own cycle, at offset d, then 3d ≡ 0 (mod 5) and d is even, so d ≡ 0 (mod 10). That needs a cycle of length ≥ 20.
   - Otherwise Z(c) is on another cycle.
   - Either way **|𝒦| ≥ 20**: one 20-cycle with Z = π¹⁰ on its 9-states, or two 10-cycles matched by Z.
6. **Converse.** Any nonempty set of rigid and in-shape DL states that is closed under π, π⁻¹ and Z is such a class.

So, on the sphere: **near-rigid LPC ⇔ there is no nonempty set of rigid / in-shape DL states closed under π^{±1} and Z.**

### 1.3 Data check of J5 (where examples exist)

- Every law-respecting general-graph example of §2 has exactly the J5 shape: rungs (c), (d1), (d2), (d); 325 + 300 checked by `tj_zoffset.py`, plus 4 (d2) and 3 (d) examples by `tj_verify.py`.
  - One 20-cycle, N = 8, 9, 8, 9, …
  - Kempe degree (8, 2) / (9, 3).
  - The extra chain is {α,μ} at all 10 nine-states.
  - **Z(c) = π¹⁰(c) at every 9-state.**
- They were verified independently with TrackH's pure-Python engine and TrackI's primal chain count (`tj_verify.py`): law 20/20, 0 filled states in the class, filled states elsewhere, 0 edges outside triangles in the (d1) and (d) examples, and H3 at 20/20 states in the (d2) and (d) examples.
- **"Local σ-isolation" (NRI) is false on spheres.** NRI would say: the Z-partner of an in-shape state is never in-shape. Counterexamples (in-shape c with Z(c) in-shape):

  | set | count |
  |---|---|
  | plantri24 | 66 |
  | fullerene duals | 28 |
  | frame-29 | 2 |
  | frame-30 (1/4 sample) | 4 |
  | frame-31 (1/16 sample) | 2 |
  | full scan (§3.2) | 1,260 states at 583 holes |

  So the obstruction is not local at one Z-edge; it has to be global around the π-cycles.

### 1.4 Sphere-only refinements [data; hand where marked]

- **Z ⊂ {α,μ} (σ-type extra chain)** at every sphere in-shape state:

  | set | in-shape states |
  |---|---|
  | census 22–32, every hole (engine count `inshape_extraAB` = 0, `inshape_extraP23` = 0; `out/scan2_census.log`) | 25,800 |
  | plantri24 (1/20 sample, `tj_struct.py`) | 408 |
  | fullerene duals (1/4 sample, `tj_struct.py`) | 273 |
  | **total** | **26,481 / 26,481** |

  The Python check `tj_struct.py` independently gives the same result on the census samples: frame 22–28, 259; frame-29, 319; frame-30 (1/4), 281; frame-31 (1/16), 367.

  In general graphs it fails: 80 of 3,475 in-shape states have Z ⊂ {A,B}. Hence on the sphere the matching Z is σ.
- **H3 form [hand].** Apply TrackH Lemma H3 with χ = 2 (c_k − β_k = 2, 3, 3):
  - rigid ⇔ all six pair graphs are forests;
  - an in-shape state has P2 and P3 forests and P1 of cycle rank exactly 1 (the P1 component that surrounds Z).
  - In Tait form, H = H₀ ∪ C′ with C′ a free {2,3}-cycle bounding the disc of Z. F12 and F13 are connected figure-eights with the DL pairings, and σ is the switch of C′.
  - Along a near-rigid cycle the cycle-rank vector is (0,0,0) at rigid states and (1,0,0) at 9-states, consistent with J2 (β₂(c) = β₃(πc)). So H3 counting alone gives no contradiction. Off the sphere (or without H3) the general-graph examples have β ≈ 10–20 in every partition.
- Remark 7 (N + L1 + L2 preserved by link-free moves) holds at all 336,093 extra-chain swaps from sphere N = 9 states (`X5`). It fails in general graphs (103 / 22,599).

## 2. Task 2: the general-graph ladder [data]

**Search** (`tj_search.py`, engine `tj_eng`):
- **Graphs.** h = 0 adjacent exactly to an induced 5-cycle 1..5. Other vertices have degree ≥ 3, and moves toggle 1–2 edges (annealing).
- **Seeds.** TrackH's general counterexamples, the RP² test beds, and the Census29 sphere cycle graphs; later runs also seed from earlier examples.
- **Score per class with an all-DL cycle.** bad = (states off cycles) + Σ max(0, N − 9) + [law failures] + [H3 imbalance Σ|E1 − E2 − 1| + |E2 − E3|] + 5·[no N = 9 state]. An example is bad = 0 together with the rung's graph conditions.

| rung | condition | evaluations | result |
|---|---|---|---|
| (a) | none (closed class, all states on all-DL cycles, N ≤ 9, some N = 9) | 0.45M | **exists**: 937 distinct graphs. All are one 20-cycle with N ≡ 9 and the law failing at all 20 steps; 287 of them are 4-colourable. (Rigid N ≡ 8 classes are TrackH's.) |
| (b) | + chain-parity law at every π-step | 1.5M (b-only runs: 0 hits; walk luck), plus the (c) run | **exists** (the (c) examples) |
| (c) | + G 4-colourable (some filled state of G − h) | 1.95M | **exists**: 325 distinct graphs (n = 30), all from one walk seeded at RP² test bed `rp2_s203_w16_t134`. One 20-cycle 8/9 alternating, Z = π¹⁰, 2–15 filled states elsewhere. Verified independently |
| (d1) | + every edge of G − h in a triangle of G | 12.7M (soft triangle penalty; the hard-constraint run, 1.2M, found none because it could not repair the seeds) | **exists**: 411,556 distinct graphs (n = 30, about 120 edges). Same shape. Verified independently: 0 edges outside triangles |
| (d2) | + H3 edge balance E1 = E2 + 1 = E3 + 1 at every class state | 12.5M + 9.5M with plain edge toggles: none (best bad 8, with H3 failing at 3 consecutive states of an otherwise perfect 20-cycle). Then 3.5M **with vertex stacking** (`TJ_GROW`: a new vertex on a random triangle of G − h, which keeps the Kempe structure and the H3 differences) | **exists**: 4 distinct graphs (n = 34, 123 edges). Verified: H3 20/20, law 20/20, 4–6 filled states. 1–3 edges are not in triangles |
| (d) | d1 + d2 | 11.4M + 1.1M + 0.6M from older seeds: none. Then seeded from the (d2) examples, with stacking | **exists**: `jd632_41_6403` and others (n = 37–38, about 135 edges). Verified: 0 edges outside triangles, H3 20/20, law 20/20, 4 filled states |
| (e) | d + sphere edge count \|E(G − h)\| = 3n − 11 (with H3, this forces all pair graphs at rigid states to be forests, as on the sphere) | 9.9M (2 runs seeded from the (d) examples) | **none**. Best bad 48, i.e. still about 24 edges above 3n − 11; the search barely moved. An uninformative null |

**Reading.**
- Everything Theorem J5 needs (alternation, in-shape 9-states, a Z-matching, Z ⊂ {α,μ}, here Z = π¹⁰) can be realised in 4-colourable graphs where:
  - every edge of G − h lies in a triangle;
  - every class state satisfies the per-partition edge balance of triangulated surfaces (H3);
  - the chain-parity law holds at every step.
- So none of these local or counting consequences of a triangulated sphere implies near-rigid LPC. TrackI §4 asked "local and uninteresting, or sphere-specific like RI?". The answer is **sphere-specific like RI**.
- The H3 rung needed vertex stacking. Pure edge toggling stalled at "H3 fails at 3 consecutive states", which is also roughly where TrackH's rigid-class balance search stopped.
- The examples are dense: pair-graph cycle ranks of about 10–20, against 0 (rigid) / 1 (9-state) on the sphere. That is what rung (e) tests.

## 3. Task 3: sphere data — how far from near-rigid closed? [data]

### 3.1 All-DL cycle classes

These are the Census29 cycle graphs (13 graphs) plus C30#0, at every hole with a cycle (`tj_nrcomp.py`, `out/nrcomp_cyclegraphs.log`).
- "good" = states on an all-DL cycle with N ≤ 9.
- In the N profile, a = 10, b = 11, …

| graph h | class size (filled) | N along the 20-cycle | good | cycle N ≥ 10 | off-cycle | moves leaving the good set |
|---|---|---|---|---|---|---|
| C30#0 h0 / h16 | 100 (40) | a9a9a9a9a9a9a9a9a9a9 | 10 | 10 | 80 | 30 (10 → non-DL, 20 → cycle N = 10) |
| p32.r11#14729 h27 / h30 | 5459 (2411) | b8baba9ababa9a9a9ab8 | 6 | 14 | 5439 | 17 |
| p32.r124#210513 h23 | 4770 (2310) | dededaba9a98b89a9aba | 6 | 14 | 4750 | 14 |
| p32.r29#12613 h25 | 4345 (2100) | ba9a9abcbcfa9ab8ba9a | 5 | 15 | 4325 | 14 |
| p32.r96#9744 h16 | 5064 (2696) | 9abcbcfcbcba9a9aba9a | 4 | 16 | 5044 | 12 |
| p32.r68#2466 h2 | 4594 (2136) | abadabcdcbabc9a9a9cb | 3 | 17 | 4574 | 9 |
| p31.r1#7302, p31.r19#11250 h15 | 3784 / 5404 | … | 2 | 18 | … | 6 |
| p31.r13#292235 h3 | 3122 (1608) | bababa9abababababcba | 1 | 19 | 3102 | 3 |
| 7 other cycle classes | 3976–8458 | all N ≥ 10 | 0 | 20 | … | – |

So each class is at least 80 states and at least 10 cycle states away from near-rigid closure. The nearest case, C30#0, has every other cycle state at N = 10, and σ exits to non-DL states exactly at its 9-states.

### 3.2 Census-wide, without needing an all-DL cycle

R = {DL states with N ≤ 9}. Measured per hole (`tj_scan.py`, `out/scan_census.log`, `out/scan_census_notable.jsonl`):
- the longest π-run inside R;
- whether a π-cycle lies in R;
- in-shape states, and in-shape states whose σ-partner is in-shape;
- near-rigid closed classes.

| set | holes | |R| | longest π-run in R | holes with run ≥ 5 | π-cycles inside R | all-DL cycles | in-shape states | in-shape with in-shape σ-partner | near-rigid closed classes |
|---|---|---|---|---|---|---|---|---|---|
| frame 22–27 | 639 | 8,498 | 4 | 0 | 0 | 0 | 119 | 0 | 0 |
| frame-28 | 1,563 | 28,305 | 5 | 5 | 0 | 0 | 140 | 0 | 0 |
| frame-29 | 4,533 | 84,504 | 5 | 8 | 0 | 0 | 319 | 2 | 0 |
| frame-30 | 18,490 | 405,406 | 6 | 60 | 0 | 1 | 985 | 6 | 0 |
| frame-31 | 69,006 | 1,812,952 | 6 | 235 | 0 | 6 | 5,473 | 96 | 0 |
| frame-32 | 263,351 | 7,904,435 | **7** | 1,038 | 0 | 10 | 18,764 | 316 | 0 |
| plantri24 (all 7,209) | 111,492 | 943,244 | 7 | 701 | 0 | 5 | 6,523 | 718 | 0 |
| fullerene duals C20–C46 (all) | 4,104 | 49,643 | 6 | 118 | 0 | 4 | 865 | 122 | 0 |
| **total** | **473,178** | 11.2M | **7** | 2,165 | **0** | 26 | 33,188 | 1,260 | **0** |

- The longest run grows slowly with order: 4 → 5 → 6 → 7 from frame-27 to frame-32. A near-rigid cycle needs ≥ 10.
- The 8 runs of length 7 (`tj_runs.py`), for example p32.r84#686339 h23, all look like 9(αμ) 8 9(αμ) 8 9(αμ) 8 9(αμ) or 8 9 8 9 8 9 8.
  - They start after a non-DL π-preimage.
  - They end when π(c) leaves DL, or when N jumps to 10–12.
  - The extra chain is αμ at every in-shape state; the run's end states sometimes carry μA / μB extras.

R-components in the Kempe graph, for the cycle graphs (`out/nrcomp_cyclegraphs.log`):
- 5,019 components; the largest has 6 states (2 rigid, 4 nine), with 4–6 exits;
- 0 components without exits.

### 3.3 Adversarial flip search on spheres and RP²

`tj_sphsearch.py` runs flip walks (min degree 3) maximising Rrun + 3·Rcyc + ½·#σ-closed in-shape states. Every logged graph was re-validated as a simplicial surface of the right χ.

| surface | seeds | evaluations (graphs; every degree-5 hole each) | longest π-run in R | π-cycles in R | near-rigid closed classes | max σ-closed in-shape at one hole |
|---|---|---|---|---|---|---|
| sphere | frame-28, frame-29, plantri24 | 864,506 | **7** (1 graph; 59 at 6) | 0 | 0 | 8 |
| RP² | 202 TrackH RP² test beds | 930,416 | **11** (16 graphs) | 0 | 0 | 12 |

- On RP² the law and RI fail, so runs in R need not alternate (8 → 8 steps occur), and they get longer. Even so, no π-cycle in R and no near-rigid closed class was found.
- On the sphere the search does not beat the exhaustive census maximum of 7.

## 4. Task 4: proof status and the smallest open claim [hand, unreviewed]

**What J5 reduces near-rigid LPC to.** On the sphere, with Z = σ (§1.4, data), a counterexample is a nonempty set 𝒮 of DL states with these properties:
- every state of 𝒮 is either Tait-rigid (H, F12, F13 all connected; DL pairings), or in-shape (H = H₀ ∪ C′ with one free {2,3}-cycle C′; F12, F13 connected; DL pairings);
- π and π⁻¹ alternate the two types;
- σ (the switch of C′) maps in-shape states to in-shape states.

**What does not work.**
1. *Parity.* Theorem 6 is already used up; it forces the alternation. Remark 7 / Lemma R give only N + L1 + L2 parity under σ, which is satisfied.
2. *Local σ-isolation.* False (§1.3: 1,260 in-shape states at 583 sphere holes have an in-shape σ-partner).
3. *H3 counting.* Consistent with the J5 shape, with cycle-rank vectors (0,0,0) / (1,0,0) (§1.4). Realised in general graphs (rung d2 / d).
4. *A run bound from one rigid step.* RI forbids 8 → 8. Sphere runs 8 9 8 9 8 9 8 of length up to 7 occur, so no "two-step RI" (9 → 8 → 9 forbidden) holds either.

**Smallest open claims** (each implies near-rigid LPC on the sphere).
- **NRC (near-rigid cycle exclusion).** On a triangulated sphere, no π-cycle at a degree-5 hole consists of DL states with N ≤ 9. Equivalently: no all-DL π-cycle alternates Tait-rigid and in-shape states.
  - It does not need the Z-closure. It is a statement about a single π-orbit, like RI, which is NRC's "all rigid" special case.
  - Data:
    - census 22–32, plantri24 and fullerenes: 0 such cycles in 473,178 holes; max run 7 (§3.2);
    - sphere flip search: max run 7;
    - RP² flip search: runs to 11, no cycle;
    - general graphs: false even with the law, 4-colourability, triangles and H3 (rung d).
  - So a proof must use planarity proper (Jordan / band surgery, as in RI), not just its counting shadows.
- **σ-type lemma (sphere).** At an in-shape state the extra chain is an {α,μ}-component. Data: 26,481 / 26,481 on spheres; false in general graphs (80 / 3,475). In Tait form [hand]: H₀ separates the sphere into the side containing e₃, which touches the faces x_{j+3}, x_{j+4} (an AB region), and the side containing e₀, e₁ (an αμ region). Z ⊂ αμ ⇔ C′ lies on the e₃ side. It is offered as the first planar lemma towards NRC, since it pins the free cycle to one side of the Hamiltonian part H₀.
- **Possible route to NRC (speculation, not attempted).** Follow the free cycle along the orbit: c₀ (in-shape, C′₀) → c₁ = π(c₀) (rigid) → c₂ (in-shape, C′₂) → …
  - By J2, P2 of c_i is P3 of c_{i+1}, component for component. So the new free {2,3}-cycle C′₂ of c₂ must be created by the switch on X(c₁), out of P1 / P2 data of c₁.
  - TrackI's band-surgery picture (Lemma R) controls how many curves such a switch creates, but not where they lie.
  - A proof would need a monotone quantity. For example: the disc of C′ shrinks, or moves away from e₃ (σ-type lemma), along the orbit, so the orbit cannot close.
  - The sphere runs of §3 look like this: …9(am) 8 9(am) 8 9(am)… ending when N jumps to 10–12 or π leaves DL. That suggests checking such a quantity on the 8 runs of length 7 (`tj_runs.py`).

## 5. Run inventory

| run | what | evaluations | log |
|---|---|---|---|
| struct | task 1 checks on spheres (frame 22–29 all, frame-30 1/4, frame-31 1/16, plantri24 1/20, fullerenes 1/4) and on 1,523 general example graphs | 22,328 + 1,523 holes | `out/struct_*.log` |
| a, b1, b2, c | rungs a–c | 0.45M, 1.5M, 1.95M | `out/search_{a,b1,b2,c}.*` |
| t, t_hard | rung d1 | 12.7M, 1.2M | `out/search_t*.log`; examples in `out/search_t_examples_first300.jsonl` |
| h, h2, h3a, h3b | rung d2 (h3b with vertex stacking) | 12.5M, 9.5M, 3.8M, 3.5M | `out/search_h*.log`; examples in `out/examples_rung_d2.jsonl` |
| d_v1, d_hard, d, d3, d4, d5 | rung d (d4, d5 seeded from the d2 examples, with stacking) | 0.6M, 1.1M, 11.4M, 3.4M, 8.4M, 7.5M | `out/search_d*.log`; examples in `out/examples_rung_d.jsonl`; verification in `out/verify_rung_d*.jsonl` |
| e1, e2 | rung e | 4.8M, 5.0M | `out/search_e*.log` |
| scan, scan2 | census 22–32 + plantri24 + fullerenes, all holes | 473,178 holes, then 357,582 again | `out/scan_census.log`, `out/scan2_census.log`, `*_notable.jsonl` |
| nrcomp | all-DL cycle classes and R-components of the 14 sphere cycle graphs | 232 holes | `out/nrcomp_cyclegraphs.log` |
| sphflip, rp2flip | flip searches | 0.86M, 0.93M graphs | `out/sphflip.*`, `out/rp2flip.*` |

## 6. Files

| file | content |
|---|---|
| `tj_eng.c` / `tj_eng` | C engine: colourings of G − h up to renaming, all Kempe moves, classes, π, locks, D, N, role component counts, H3 counts, all-DL cycles; per-class near-rigid statistics; R-runs, in-shape counts; `--dump` per-state records |
| `tj_lib.py` | pipe driver and parsers |
| `tj_struct.py` | task 1 checks X1–X5 and NRI (`out/struct_*.log`) |
| `tj_search.py` | task 2 annealing, rungs a/b/c/t (= d1)/h (= d2)/d/e; `TJ_GROW` enables vertex stacking (`out/search_*.log`, `*.jsonl`) |
| `tj_verify.py`, `tj_zoffset.py` | independent verification (TrackH engine + TrackI chain count) and Z-offset structure of examples |
| `tj_nrcomp.py`, `tj_scan.py` | task 3: all-DL cycle classes and R-components; census-wide R statistics |
| `tj_sphsearch.py` | task 3: flip searches on spheres / RP² |
| `tj_runs.py` | prints the longest π-runs inside R at given holes, with extra-chain pairs |
| `run_struct.sh`, `run_search*.sh`, `run_phase*.sh` | the launch scripts actually used |
| `out/seeds_*.txt` | search seeds (`seeds_cex` = rung-c examples, `seeds_tex` = rung-d1 examples) |
| `out/search_a.jsonl`, `out/search_c.jsonl`, `out/search_t_examples_first300.jsonl`, `out/examples_rung_d2.jsonl`, `out/examples_rung_d.jsonl` | the example graphs per rung (format 'name n adj;…', hole 0, link = 1..5). The full d1 log (411k examples, 192 MB) was truncated to its first 300 lines |
