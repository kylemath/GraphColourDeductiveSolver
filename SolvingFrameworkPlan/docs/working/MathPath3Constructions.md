# Path 3: constructed multi-class instances (design, hand only)

Math worker for the two-week plan, path 3. Written 6 October 2026 on the MacBook. **Nothing was run** (battery rule). The scripts in `MathPath3-scripts/` are **untested**. Exact Studio commands are in §6.

Labels:
- **[read]**: I read the text myself, and say how much.
- **[cited]**: taken from a repo page, not re-derived.
- **[hand]**: my own argument, not reviewed.
- **[heuristic]**: a reason to try something, not an argument.
- **[from memory]**: not checked.

Nothing here changes a status word.

**The question (TwoWeekPlan, reframing).** Given 4CT, R\* at v fails iff T − v has a Kempe class that contains no restriction of a colouring of T: a NEW class. Equivalently, the class contains no filled state. "Contains a restriction" and "contains a filled state" are the same thing for each single class: a filled state extends by giving v the missing colour, and a restriction is filled. So kmap's `hit_by_T` flag is exactly "contains a filled state". Only instances with κ(T − v) ≥ 2 are evidence.

---

## 1. Priority seeds for Studio intel's kc_search

### 1.1 Mohar's akempic triangulations

**What I could read.**
- **Mohar 1985 itself (Discrete Math. 54, 23–29): not read.** No open copy was found.
- **[read, full text]** Florek, arXiv:2504.13316v2, read via text extraction. It restates Mohar's definition and results:
  - *Nonsingular colouring:* a 4-colouring in which the two vertices opposite each edge have different colours.
  - *Akempic:* T has a nonsingular colouring that is Kempe-equivalent to no other colouring.
  - *Fisk (Prop. 1.1 there):* a plane triangulation has a nonsingular colouring iff every degree is divisible by 3.
  - Mohar characterised and counted the akempic triangulations with all degrees 3 or 6.
  - These have exactly four vertices of degree 3. Florek describes them by index-vectors (K, M, S⁺) with |P| = 2KM + 2.
  - Florek's Theorem 1.3: a P with index-vector (1, n, s) is akempic iff gcd(s, n) = gcd(s+1, n) = 1.
  - Theorem 1.2 (Mohar's count) is stated for odd n.
- **[read, full text]** Mohar 2006 (§4) says these give κ ≥ 2 on plane triangulations, and that 3-sums give arbitrarily many classes. The 3-sums have separating triangles, so they are not in the core class.

**Generator: a reconstruction [from memory], checked by the builder on each instance.**
- A (3,6)-triangulation of the sphere is a triangular-lattice torus modulo z ↦ −z. The four 2-torsion points become the degree-3 vertices, with cone angle π.
- Take L = Z² with neighbours ±(1,0), ±(0,1), ±(1,−1). Let Λ' = ⟨(a,0), (s,b)⟩, of index n = ab, and Λ = 2Λ'.
- Then **AK(a,b,s) = (L/Λ)/±**. It has 2n + 2 vertices and 4n faces.
- The colouring c₀(x,y) = (x mod 2, y mod 2) is well defined because Λ ⊂ 2Z² and −p ≡ p mod 2. It is proper and nonsingular.
- I do not rely on matching Florek's index convention. The builder tests directly whether c₀ is **frozen**, meaning all six bichromatic subgraphs are connected. Frozen c₀ is the akempic property.
- The builder keeps only frozen instances. For b = 1 it also prints gcd(s,n) and gcd(s+1,n), so Florek's criterion can be compared.
- Builder: `akempic(a,b,s)` in `path3_build.py`. It rejects degenerate or non-simple quotients.
- Mohar's AK has degree-3 vertices, so it is **not** a core instance. It needs the repair in §1.3.

### 1.2 Florek's two-pole belts G_n

**[cited, belt-joined.md §1]** G_n has:
- poles a and b, not adjacent;
- belt vertices u_i, v_i (i mod n), with edges a u_i, b v_i, u_i u_{i+1}, v_i v_{i+1}, u_i v_i and u_i v_{i−1};
- belt degree 5 and pole degree n.

**[read, abstract only]** Florek, arXiv:2511.00485: G_n has at least ⌊n/6⌋ Kempe classes, and G_n minus a pole has one class. His separating invariant is not in the abstract.

Builder: `florek(n)` gives the faces (a,u_i,u_{i+1}), (b,v_i,v_{i+1}) and the antiprism band. G_5 is the icosahedron, which is a sanity gate.

**Lean scope [cited, audit/team-b-lean-belt-report.md].** The compiled Lean covers only belt local moves with *slides* (the doubled-0 II opening, and the I short branch at u_0). Nothing about Kempe classes of G_n is compiled. The belt theorem itself uses slides, so it does not prove pure-Kempe R\* at belt holes.

**Diamonds.** G_n contains Birkhoff diamonds for every n: the faces u_i u_{i+1} v_i and u_i v_{i−1} v_i share the edge u_i v_i, and all four vertices have degree 5. At n = 6 the belt link (5,6,5,5,5) also contains the 2.122 proxy pattern.

### 1.3 Repair rules: getting to min degree 5 and 4-connected while keeping the mechanism

**Lemma K3: deleting a degree-3 vertex is Kempe-neutral [hand].**
- Let x have degree 3 with link triangle y_a y_b y_c, coloured a, b, c. Then c(x) = d is forced.
- So colourings of T and T − x correspond one to one.
- For a pair that does not contain d, the two link vertices with those colours are adjacent, so they lie in one component, and x is not in it.
- For a pair (a, d), the (a,d)-component of y_a in T is K ∪ {x}, where K is its component in T − x. x has only one a-neighbour.
- So swaps correspond one to one, and **the Kempe graphs are isomorphic**. The class count and the hit/filled status at any hole v not adjacent to x are preserved exactly.
- Deleting x makes its link triangle a face, so that separating triangle is destroyed.

**Lemma F: frozen colourings survive leaf moves only [hand].**
- If c is frozen on a triangulation, every bichromatic subgraph is a **tree**: E = 3n − 6 = Σ over the six pairs of (n_i + n_j − 1).
- A degree-3 vertex is a leaf in its three trees, so deleting it keeps c frozen. This also follows from K3.
- An edge flip either makes the colouring improper (when the two opposite vertices have the same colour) or removes an edge from one tree, which disconnects it. **So flips destroy frozenness.**

**Lemma N: no frozen colouring of T − v [hand].**
- T − v (deg v = 5) has 3n − 11 edges. Frozen would need Σ(n_i + n_j − 1) = 3n − 9 edges.
- **So a frozen class can never be a NEW class.** A new class needs a non-frozen mechanism. This agrees with Studio intel's lemma that no doubly locked state is frozen, and with Long Table's 15:04 item 4.

**The rule for each family.**

| family | repair | min degree / 4-connectivity | why the mechanism survives |
|---|---|---|---|
| AK(a,b,s) → **RAK** | Delete the four degree-3 vertices; each link triangle becomes a face. | Twelve degree-5 vertices in four triangles, all other vertices degree 6. Needs the degree-3 vertices pairwise ≥ 3 apart, otherwise a vertex drops to 4; the builder reports min degree. The four link triangles are no longer separating. Any other separating triangle is reported and the instance is flagged, never flipped (Lemma F). | Lemma K3: **κ(RAK) = κ(AK) ≥ 2 exactly**, with a frozen singleton class [hand]. RAK is a fullerene dual with four pentagon triples (C₂₈-like [from memory]). |
| FL(n) = G_n | None needed: min degree 5, and 4-connected (builder checks). It contains diamonds. Diamond-free repair: insert degree-6 rings to get TU(n, L ≥ 3), with n ≠ 6 to avoid the 2.122 proxy. | TU(n, L ≥ 3): degree-5 vertices only in rings 1 and L; no diamond (two adjacent ring-1 vertices have common neighbours a and a ring-2 vertex of degree 6). | **Not argued.** The poles are untouched, but whatever Florek's invariant is, it must pass through a longer floppy tube. This is a measurement (P-A2). |
| SL (slipped stacks) | Place dislocations in different bands, or shift them, so that no vertex has a single neighbour on both sides (degree 4). | Builder checks; the ring sizes in the presets are chosen for this. | By design (§4B). |
| CF, CC | None: min degree 5 by construction. | Builder checks 4-connectivity. | By design (§4C, §4D). |
| any host with a degree-4 vertex | **open.** Deleting a degree-4 vertex is not Kempe-neutral: its 4-cycle link can be 2-coloured, and the two (a,b)-components through x merge. | – | – |

**Prediction for RAK holes [hand].** By Lemma N, the frozen class of RAK does not survive in T − v. c₀|T − v is a restriction, so its class is HIT. **The akempic mechanism therefore gives multi-class T, never a new class.** It is a seed for kc_search (min degree 5, κ(T) ≥ 2 proved), not a counterexample candidate. If 2n − 2 ≤ 26 the census already contains these graphs, so the census's κ(T) must be ≥ 2 on them. That is a free cross-check of kmap.

---

## 2. Two hand facts that steer the design

**(P1) Tutte's parity [read in Mohar 2006 §5; Fisk not read].**
- Mohar defines the degree d(c) of a 4-colouring of a triangulation of an orientable surface (faces 234 counted against 432). He says it does not depend on the colour triple, and that Tutte observed its parity is a Kempe invariant.
- **[hand]** The faces missing colour i number F − Σ_{c(x)=i} deg x. So with O_i = #(odd-degree vertices of colour i) mod 2, all O_i are equal: write p(c) for the common value. A swap (a,b) on K changes O_a by #odd(K).
- **Corollary [hand]:** in a 4-coloured sphere triangulation, every Kempe component contains an even number of odd-degree vertices.
- **In T − v** (T-degrees, v removed) we have Σ O_i ≡ 1. A filled state's "odd one out" colour equals the colour missing on the link of v.
- O can change only through a component that contains an odd number of T-odd vertices. On the closed sphere this never happens. Whether in T − v it happens only for components that meet the link of v is **[open]**.
- `path3_kclasses.py` records the set of O-vectors in each class, so this can be tested.

**(P2) The torus invariant does not transfer directly [hand; Mohar–Salas abstract read].**
- Mohar–Salas: on 3-colourable triangulations of closed orientable surfaces, the degree mod 12 is a Kempe invariant. T(3L,3M) has ≥ 2 classes.
- Around one degree-5 vertex, a 3-colouring of the flat triangular lattice has holonomy equal to a **transposition** (a 60° rotation about an A-site swaps the B and C sublattices). So a flat annulus around a single degree-5 vertex is not 3-colourable, and there is no locally Eulerian annulus around v.
- An annulus is 3-colourable only around a set of degree-5 vertices whose holonomies multiply to the identity: an even number of them, with matching sublattice data.
- So "a Mohar–Salas invariant on an annulus around v" is not available as such. The flat-region test (CF, CC) is purely empirical.
- **Practical bound:** every Studio engine needs n ≤ 64 and enumerates every colouring. So the flat radius around v can be at most 2 (CF(3,1), n = 47). Math's check (c), "κ growing with flat radius", cannot go further with these tools.

---

## 3. Literature: what was read

| source | read | used for |
|---|---|---|
| Mohar, "Kempe equivalence of colorings", Graph Theory in Paris (2006) 287–297 | **full text** (author's reprint, text extracted) | Fisk Thm 4.1 (3-colourable plane triangulation: κ = 1); Cor 4.5 (χ(G) < k: one class); §4 akempic gives ≥ 2, 3-sums give arbitrarily many; Problem 3.4 remark (one vertex K-change = one or more edge K-changes in the dual cubic graph); Problem 4.6 (4-critical planar); §5 degree and Tutte's parity |
| Mohar–Salas, J. Phys. A 42 (2009) 225204, arXiv:0901.1010 | abstract | degree mod 12 invariant; T(3L,3M) non-ergodic (P2) |
| Belcastro–Haas, Discrete Math. 325 (2014) 77–84, arXiv:1209.1730 | abstract | 2-connected planar bipartite cubic graphs: one edge-Kempe class; multi-class families are **non-planar** |
| Florek, arXiv:2504.13316v2 (2025) | full text | akempic definition, Fisk Prop 1.1, Thm 1.3, index-vectors (§1.1) |
| Florek, arXiv:2511.00485 (2025) | abstract | G_n: ≥ ⌊n/6⌋ classes; minus a pole, one class |
| Fisk, "Geometric coloring theory", Adv. Math. 24 (1977) | **not read** | only through Mohar 2006 and Florek |
| Mohar, Discrete Math. 54 (1985) 23–29 | **not read** | through Florek 2504.13316 |

**Consequence for the plan's first step ("smallest Belcastro–Haas, dualised").** It yields **no sphere instance**:
- The dual of a planar bipartite cubic graph is an Eulerian triangulation, which has one class (Fisk).
- Belcastro–Haas's multi-class examples are non-planar.
- By Mohar's Problem 3.4 remark, edge-Kempe classes are coarser than vertex-Kempe classes. So a single edge class says nothing about vertex classes.

I recommend dropping that item from path 3.

---

## 4. Families (builder: `path3_build.py`; n = number of vertices)

Common to all families:
- **Configuration flags** are proxies: a diamond is two faces on an edge with all four vertices of degree 5; the 2.122 proxy is a consecutive link pattern (5,6,5) at a degree-5 vertex (Math 16:15). Studio intel's `rsst_contain.py` decides (`rsst_flags.py`).
- **"Every degree-5 vertex"**: the builder prints the orbits of the degree-5 vertices under the automorphism group of the embedding. A new class at a vertex v refutes R\* at that orbit. It refutes "some degree-5 vertex has R\*" on that graph only if every orbit fails.

### A. Two-pole tubes TU(n, L) and FL(n) = TU(n, 2) (Florek-type)

**Construction.**
- Pole a, rings R_1…R_L of n vertices each, pole b.
- Fans a–R_1 and b–R_L; antiprism bands with R_k,i ~ R_{k+1},i and R_{k+1},i−1.
- Degrees: poles n, rings 1 and L have degree 5, inner rings degree 6.
- n = nL + 2. The degree-5 vertices form one orbit [hand: rotation, reflection, end swap]; the builder confirms.

**Mechanism [heuristic].**
- The ring around a pole of colour α is a closed walk on the triangle of the other three colours, with winding w ∈ Z, w ≡ deg (mod 2), |w| ≤ deg/3.
- A swap not involving α changes w by an even amount, through ring segments whose ends have different colours.
- A tight belt blocks those changes. The number of attainable |w| levels is about n/6, which matches Florek's ⌊n/6⌋. This is consistency, not derivation; his invariant was not read.
- The tube between the poles is 3-colourable as an annulus iff 3 | n. Then it is locally Eulerian (the flat-annulus case of §2).

**Predictions.**
- P-A1: κ(FL(n)) ≥ ⌊n/6⌋ (gate: FL(12) must give ≥ 2).
- P-A2: κ(TU(n,L)) does not increase with L [heuristic: 4-colourings of the tube are floppy].
- P-A3: at ring-1 holes, the a-winding is destroyed (v sits on a's ring), so no new class.

**What a new class would mean.** It would lie at every degree-5 vertex, refuting R\* outright on that graph.

**Configurations.** L = 2 has diamonds. For L ≥ 3: no diamond, and the 2.122 proxy iff n = 6.

**Presets.**

| instance | n |
|---|---|
| FL(5..12) | 12–26 (all in the census, so κ data may already exist) |
| TU(6,3..5) | 20, 26, 32 |
| TU(7,3) | 23 |
| TU(8,3), TU(8,4) | 26, 34 |
| TU(9,3), TU(9,4) | 29, 38 |
| TU(12,3) | 38 |
| heavy: TU(9,5), TU(12,4) | 47, 50 |

### B. Slipped two-pole stacks SL(sizes): the hole sits between two pole-carriers (**top priority**)

**Construction.**
- Like A, but one band joins rings of sizes m and m + 1 (a "slip" band).
- The lower vertex X_0 gets 3 neighbours above, and the upper vertex Y_0 gets 1 neighbour below. So Y_0 has degree 5 and X_0 has degree 7: an adjacent 5–7 dislocation. In the variant where X_0 is in ring 1, X_0 has degree 6 instead of 7.
- Euler check for [n, n+1, n+1]: (6 − n) + (n − 1 + 1 + n + 1) + (5 − n) = 12. ✓
- Hole v = Y_0, with link (6,6,5,5,6), or (7,6,6,6,6) when there are inner rings on both sides.

**Mechanism [heuristic].**
- v is far from both poles, so both pole windings survive deletion of v. In T they are coupled through the tube and through the dislocation core, which is v itself.
- Deleting the core may relax the coupling. A class of T − v whose pair (w_a, w_b) is not realisable with a coloured core would be **new**.
- **This is the only family where the design aims directly at "deletion creates a class".** In all other families the mechanism lives in T and at best survives in T − v.

**What a new class would mean.** At v only (a per-vertex R\* failure). The other degree-5 vertices (rings 1 and L) are different orbits.

**Configurations.** No diamond. The 2.122 proxy should not occur for n ≥ 8; the builder checks.

**Presets.**

| sizes | n | note |
|---|---|---|
| [8,9,9], [9,10,10], [10,11,11], [11,12,12] | 28, 31, 34, 37 | |
| [8,8,9,9], [9,9,10,10] | 36, 40 | |
| [9,10,10,9] | 40 | two opposite slips |
| [9,10,9,9] with a shift | 39 | adjacent slips |
| heavy: [9,9,10,10,10] | 50 | v has an all-6 link |

### C. Cone + Florek cap CF(R, E): the flat-annulus test (Math's check (c))

**Construction.**
- Apex v of degree 5, a flat 5-fold cone of radius R (ring i has 5i vertices; corners on ring R), then E rings of 5R vertices (antiprism), then a pole of degree 5R.
- Degrees: v 5; cone corners 5; the last ring 5; everything else 6; the pole 5R.
- n = 2 + 5R(R+1)/2 + 5RE.
- The ball of radius R − 1 around v is flat: every vertex in it other than v has degree 6.

**Mechanism.**
- None at v rigorously (P2: the annulus around a single degree-5 vertex is not 3-colourable).
- The pole of degree 5R = 10 or 15 is a Florek-type carrier far from v [heuristic]. So **κ(T − v) ≥ 2 is likely, and these are exactly the multi-class holes the plan wants counted**: high-value evidence rows.

**What a new class would mean.** At v only; v is the only apex.

**Presets.**

| instance | n | flat radius around v |
|---|---|---|
| CF(2,1), CF(2,2), CF(2,3) | 27, 37, 47 | 1 |
| CF(3,1) | 47 | 2 |
| heavy: CF(3,2) | 62 | 2 (expect state caps) |

CF(1,1) would be the icosahedron.

### D. Double cone CC(R, twist)

**Construction.**
- Two flat cones of radius R joined by one antiprism band. Any gluing of two discs gives a sphere.
- Degrees: apices 5, the 5 + 5 corners 5, all other vertices 6. n = 2 + 5R(R+1).
- CC(1) is the icosahedron (gate). CC(2,·) has n = 32 (twist 0, 1, 2; one twist is presumably the C₆₀ dual [from memory]). Heavy: CC(3,0), n = 62.

**What it tests.** Symmetric flat-annulus instances with no high-degree pole. Prediction: κ(T − v) = 1 [heuristic: no carrier]. If κ(T − v) ≥ 2 here, the flat region itself is the cause, which is Math's worry 2(iii).

**What a new class would mean.** At both apices (one orbit).

### E. RAK (repaired akempic), §1.3

- n = 2ab − 2.
- κ(T) ≥ 2 is **proved** [hand: K3 + Mohar], conditional on two things: the builder's frozen flag, and AK having a second colouring (Mohar's definition; kmap shows it).
- Holes: the twelve degree-5 vertices, in at most four orbits.
- Prediction: there is no new class by this mechanism (Lemma N), and κ(T − v) is small.
- Value: min-degree-5 multi-class seeds, and the cross-check against the census.

---

## 5. What each outcome means

- **κ(T − v) = 1:** non-evidential (plan reframing).
- **κ(T − v) ≥ 2 and every class hit:** one evidence row for path 3's "~10⁴ multi-class holes". Record the class sizes and diagnostics.
- **new_classes > 0, or targetless > 0, or ρ = null:** a **candidate only**. It counts after:
  - (i) `path3_kclasses.py` (independent pure-Python code) reproduces it, including `consistency_hit_iff_filled`;
  - (ii) kreach and kempe agree (both are already in the runner);
  - (iii) the audit sees the instance file and the hashes.
- Then report it with the orbit information: one vertex, or every degree-5 vertex.
- **Diagnostics to report even without a kill:**
  - for each class of T − v: the size, the link colour counts, the pole windings and the O-parity vectors (rep-level in the runner, whole-class in the checker);
  - κ(TU(n,L)) as a function of L (P-A2);
  - for SL: whether the classes of T − v are separated by the pair (|w_a|, |w_b|).

---

## 6. Studio commands (untested; run in this order)

```sh
REPO=~/GraphColour                                  # the repo checkout on the Studio (adjust)
S=$REPO/SolvingFrameworkPlan/docs/working/MathPath3-scripts
B=~/studio-scratch/census                           # where kmap/kreach/kempe live (traps.py uses this)
W=~/studio-scratch/path3; mkdir -p $W
# 0. engines (only if missing)
clang++ -O3 -march=native -o $B/kmap   $REPO/backgroundMaterial/planemap-structural/longtable/studio-explore/kempe-census/kmap.cpp
clang++ -O3 -march=native -o $B/kreach $REPO/backgroundMaterial/planemap-structural/longtable/studio-explore/sage-qa-runs/kreach.cpp
clang++ -O3 -march=native -o $B/kempe  $REPO/backgroundMaterial/planemap-structural/studiointel/fast/kempe.cpp
# 1. build (prints one JSON summary line per instance; SKIP lines go to stderr)
python3 $S/path3_build.py --out $W/core --preset core > $W/core.build.jsonl 2> $W/core.build.err
# 2. authoritative diamond / 2.122 flags
(cd $REPO/backgroundMaterial/planemap-structural/studiointel && python3 $S/rsst_flags.py $W/core > $W/core/rsst.jsonl)
# 3. kappa(T), kappa(T-v), per-class hit (= filled), kreach, kempe rho; one record per (instance, orbit rep)
nice -n 10 python3 $S/run_path3.py $W/core --bin $B --workers 8 --cap 50000000 --timeout 7200 \
    > $W/core/results.jsonl 2> $W/core/kill.log
# 4. independent whole-class check: the gates, every KILL-CANDIDATE, and the diagnostics on small multi-class holes
python3 $S/path3_kclasses.py $W/core/FL_n12.json --hole reps --max-states 2000000
python3 $S/path3_kclasses.py $W/core/SL_rings8-9-9.json --hole all
# 5. later: complete akempic list and heavy instances
python3 $S/path3_build.py --out $W/ak --preset ak > $W/ak.build.jsonl 2> $W/ak.build.err
python3 $S/path3_build.py --out $W/heavy --preset heavy > $W/heavy.build.jsonl 2> $W/heavy.build.err
nice -n 10 python3 $S/run_path3.py $W/heavy --bin $B --workers 4 --cap 50000000 > $W/heavy/results.jsonl 2> $W/heavy/kill.log
```

**Gates (all must hold before any result is used):**
- G1: `FL_n5` and `CC_R1_tw0` are the icosahedron: n = 12, all degrees 5, n_automorphisms = 120, one orbit.
- G2: `FL_n12` gives kT ≥ 2 (Florek).
- G3: every `RAK_*` with frozen = true gives kT ≥ 2 with a class of size 1.
- G4: on every instance where `path3_kclasses.py` finishes, it agrees with kmap on kT, kH and new_classes.

**Files for kc_search.**
- `NAME.tri`: oriented faces (the kempe.cpp format).
- `NAME.edges`.
- `NAME.json`: rotation system; plantri ascii for n ≤ 26.
- `all.g`: census.cpp lines.

kc_search's own input format is not in this checkout, so the adapter is Studio intel's.

**Cost [estimate, unverified].** The number of colourings grows roughly like 1.4–1.5ⁿ, so n ≤ 40 should be minutes. n = 47–50 may approach the 50M state cap: a capped record is inconclusive, never a pass. n = 62 will probably cap.

---

## 7. Open, and what I did not do

- I did not read Mohar 1985, Fisk 1977, or Florek 2511.00485 beyond its abstract. The AK generator is a reconstruction checked by property, not by matching Florek's index convention.
- The SL mechanism and the winding explanation of Florek's count are [heuristic].
- No repair rule is given for degree-4 vertices.
- Mirror and isomorphic duplicates in the AK list are not removed. Use the census canonical form if counts matter, for example to compare with Mohar's a(n).
- No code was run. Every script is untested, including the orientation and orbit routines.
