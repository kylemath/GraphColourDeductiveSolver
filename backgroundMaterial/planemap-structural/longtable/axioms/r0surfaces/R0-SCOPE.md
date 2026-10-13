# R0 scope: surfaces, variants, literature (Long Table, 13 Oct 2026, 13:25–14:15)

Exploratory. Labels:
- **[data]**: computed here. SAT answers are CaDiCaL 1.5.3 verdicts (no DRAT). Genus values are exhaustive C enumerations unless marked *heuristic*.
- **[hand]**: argument written here, not independently reviewed.
- **[recall]**: from memory or from a web abstract, not checked against the paper.
- **[conjecture]**.

Read-only reuse: `../proof/sat_t1v.py` (imported), `../ax_lib.py` (G5, `planar_rot`), and TrackU T1 graph files. Nothing in `axioms/proof/` or `axioms/invariants/` was touched.
Compute: `nice -n 10`, ≤ 3 processes, every run ≤ 10 min, on AC power (`pmset`: charged, 100 %).

## 0. Verdict

1. **As a statement about graphs with a rotation at v, R0 is sphere-specific, and it fails at the smallest possible size [data, verified by hand].**
   - At n = 8, the 5 R0-violating labelled graphs (all lengths L) embed in the **projective plane**, the **torus** and the **Klein bottle**, with the prescribed rotation at v.
   - The RP² witness is even a **simple 7-vertex triangulation of RP²** in primal form. Its degrees are 3, 5, 5, 5, 6, 6, 6, and x has degree 5.
   - In the witness, every M_t ∪ M_{t+1} is Hamiltonian (§2.2).
   - Minimum genus over R0 violators is orientable genus 1 and Euler genus 1 at every n = 8, 10, 12, 14, 16. There are no genus-0 violators for any L: n ≤ 14 all (genus), n = 16 sample. `planar_census.py` independently confirms planar R0 for all L at n ≤ 16, exhaustively.
2. **But every off-sphere violation goes through a NON-LIFTABLE state, and requiring liftability restores R0 on RP², the torus and the Klein bottle in every case tested [data] (main finding, §2.4).**
   - A state (M_t, M_{t+1}) is a near-Tait colouring. In an embedding it lifts to a face 4-colouring (= a genuine 4-colouring of the primal T − x, the object NRC is about) iff its Z₂² holonomy is trivial. On the sphere every state lifts.
   - **R0-lift** = R0 with every state liftable. It has **no violation** on:
     - RP²: n ≤ 12 all; n = 14 sample; n = 16 RP² sample;
     - the torus: n ≤ 14 all; n = 16 sample of 5,258;
     - the Klein bottle: n ≤ 12 all;
     - V3 graphs: Klein bottle n = 16, torus n = 18.
   - Without liftability, the same detector finds all violators (positive control).
   - So **R0, phrased primally, behaves like NRC, not like the chain-parity law.** The data are consistent with the sphere entering R0 only through "every state lifts" (trivial holonomy, automatic when H¹(S; Z₂) = 0).
   - On RP², the Hamiltonian state of a violator is **never** liftable: 0 of 5 / 34 / 253 at n = 8 / 10 / 12, and 0 of 67 at n = 14. The base rate over all RP²-embeddable labelled graphs at n = 10 is 512 / 956.
   - On the torus, the number of violators with a liftable Hamiltonian state in some embedding equals the number with an H-separating embedding (n = 8–14 all, n = 16 sample). Closure always needs some non-liftable later state.
   - [proved, hand] If H is non-separating, the Hamiltonian state is not liftable: a closed dual curve crossing H once has holonomy 1 or 2 ≠ 0.
3. **The NRC-like variants climb the genus ladder [data].**

   | variant | first n | genus where it first occurs |
   |---|---|---|
   | V2: M_{2j} ∪ M_{2j+1} Hamiltonian ∀j | n = 8 (all 5 R0 violators) | RP² and torus, same witness |
   | V3: V2 + word exactly 1212 (odd unions have 2 components), no DL | **n = 16** (20 labelled graphs; none at n ≤ 14, exhaustive) | n = 16: min orientable genus 2, min Euler genus 2 (**Klein bottle**), both exact; n = 18: **torus** (64 of 660 graphs found, witness verified); RP² not found (heuristic on 660, exact on 6). **None survives liftability (§2.4)** |
   | T1 (genuine DL R-cycles, TrackU) | n = 22 | both n = 22 graphs: orientable genus **2** (exact); Euler genus ≤ 3 and ≤ 4 (heuristic) |

   No V3 graph at n = 16 or at n = 18 (torus ones) carries a genuine DL orbit (`dlcheck.py`). The picture is that each added NRC ingredient pushes the first counterexample to a higher surface. R0 and V2 fail already on genus 1.
4. **Planarity without the Hamiltonian pair [data].**
   - With the R0 frame (advance −2 per step), **no closed sequence of any length exists** on any Hamiltonian plane G with n ≤ 16. This is an exhaustive census over all rotations realisable at v: the frame digraph D₋₂ is acyclic.
   - The SAT search adds: none of length 10 for n = 18, 20, 22, and none of length 20 for n = 16, 18 (§3.1).
   - C30#0 (n = 26, L = 20) is therefore far from minimal-size behaviour.
   - With **advance −1** the opposite holds: closed sequences exist on the plane from n = 8 on, always of period 5. They pass through Hamiltonian pairs in all but 2 / 2,267 (n = 14) and 28 / 19,189 (n = 16) closed cases.
5. **Structural restatement [hand + data].**
   - An R0 sequence with rotation (f_0 … f_4) is the same thing as an advance −1 sequence with respect to the "star" order g = (f_0 f_2 f_4 f_1 f_3).
   - At n = 8 every R0 violator is planar with the star rotation, and at n = 10, 12, 14 respectively 34/58, 249/685 and 1,918/9,470 are. So most small off-sphere R0 witnesses are planar advance −1 orbits whose graph can be re-embedded with the pentagram rotation at v. That is possible on RP² or the torus but never on the sphere.
   - **R0 is the statement that on the sphere, a closed matching sequence through a Hamiltonian pair cannot visit the edges at v in pentagram order.**
6. **Literature.** I found no statement equivalent to R0. Closest leads, in §4:
   - Kempe–Heawood degree-5 rotation and the open "Kempe–Kittell halting" question;
   - Fisk's degree of a 4-colouring as a simplicial map to ∂Δ³, Tutte's parity formula for it, and the Mohar–Salas mod-12 Kempe invariant;
   - Penrose's planar sign formula. Its natural invariant is constant along every R0 sequence in any graph, so it gives nothing [hand, §4];
   - Thomason's lollipop parity (a candidate *counting* mechanism);
   - edge-Kempe classes (Mohar; Belcastro–Haas; Goedgebeur–Östergård).

## 1. Method and tools

**Digraph reformulation [proved, hand].**
- Let D be the digraph on the perfect matchings of G, with an arc M → M' iff M ∩ M' = ∅ and k(M') = k(M) − 2, where k is the label of the v-edge.
- Every closed walk of D has length ≡ 0 (mod 5).
- A closed R0 sequence of any length through the Hamiltonian pair (M_0, M_1) is exactly a closed walk through the arc M_0 → M_1.
- So **R0 fails on (G, rotation) ⟺ M_0 is reachable from M_1 in D**.
- This tests all L at once. The SAT runs of PROOF-ATTEMPT-1 fix L.

| tool | what it does | validation |
|---|---|---|
| `r0enum.py n` | Exhaustive census over all normal-form labelled graphs (H + chords, all 3! labellings of f_1, f_3, f_4). Records R0 (lengths L ≤ 40), V2 and V3 (closed walks in Aham·A and Aham·A2). | Agrees exactly with the SAT encoder `sat_t1v.Enc` (no planarity, no loops) on the set of violating labelled graphs: n = 8, 10, 12 at L = 10, and n = 10 at L = 5, 20 (`xcheck_sat.py`: 5 / 58 / 685 = 5 / 58 / 685) |
| `genus.c` | Exact orientable genus with the rotation at v fixed (all (d−1)! rotations at other vertices), exact Euler genus and non-orientable genus (generalized maps; twist vectors × rotations up to reversal), optional `-free`. `-sepT` / `-sepP` enumerate all torus / RP² embeddings and count those with H separating and those whose primal is a simple triangulation. | Known values reproduced: K4 (0, 0, ng 1), K3,3 (1, 1, 1), Petersen (1, 1, 1), K5 (1, 1, 1), cube (0, 0, 1), K3,5 with v fixed (1, 2, 2), Heawood (og 1, eg 2, ng 3; ng = 3 is consistent with Franklin's theorem via K7 duality [hand]). Simple-primal and H-separation counts agree with the Python checker at n = 8 (RP²) and n = 12 (torus, 517 graphs) |
| `egheur.c` | Simulated annealing over twist vectors (Euler genus) and over rotations (orientable genus). Gives upper bounds only. Prints the twist vector. | Equals the exact values on all 60 tested n = 14 graphs |
| `verify_embed.py` | Explicit witness. Builds a closed R0 / V2 / V3 sequence and re-checks it with `ax_lib.G5`. Builds an embedding (brute force, or a given twist vector) and re-checks it **from the face list alone**: every edge used twice, every vertex link one cycle, rotation at v read off the link, χ, orientability by face 2-colouring, primal simplicity | – |
| `planar_census.py n` | All Hamiltonian plane G, all rotations at v realisable by a two-sided chord drawing. Digraphs D₋₂ and D₋₁: SCCs, closed lengths ≤ 40, #components of M ∪ M' inside SCCs | Reproduces planar R0 UNSAT (no Hamiltonian arc in an SCC) |
| `sat_noham.py n L` | Planar, **no Hamiltonian condition** on the M's. G is assumed Hamiltonian with any Hamiltonian cycle (two placement cases at v, §3.1) | Positive control `--adv -1`: SAT at n = 8, 10, 12, solutions verified planar with `planar_rot` |
| `v3sat.py n L` | SAT + lazy word cuts for V3 (no DL, no planarity) | Equal to `r0enum` at n = 16 (20 = 20 labelled graphs) |
| `lift_test.py n` | For every RP² / torus / Klein-bottle embedding (`genus -sepP/-sepT/-sepK -list`) of every violator: is there a closed R0 walk through the Hamiltonian arc using only **liftable** states (trivial Z₂² holonomy)? Lazy BFS | Positive control `--nolift`: finds all 34 RP² / 53 torus violators at n = 10. Sphere control `--sphere-control`: every arc lifts in every planar embedding (n = 8, 10). Embedding lists never hit the 400 cap (max 40) |
| `all_labelled.py` | all normal-form labelled graphs (control population) | – |
| `dlcheck.py` | `ax_lib.G5.orbits()` (DL + unique successor) on V3 graphs | – |
| `summarise.py` | Prints the tables below from `out/` | – |

## 2. Task 1: is R0 sphere-specific? (as a graph statement yes; once every state must lift, no counterexample found)

### 2.1 Minimum genus of R0 violators by n [data]

Counts are labelled graphs (chord set + labels f_1, f_3, f_4) that admit a closed R0 sequence of some length. "og" is the orientable genus and "eg" the Euler genus, both with the rotation (f_0..f_4) at v.

| n | labelled graphs | R0 violators | of which V2 | V3 | og distribution | eg distribution | **min og / min eg** |
|---|---|---|---|---|---|---|---|
| 8 | 114 | 5 | 5 | 0 | 1: 5 | 1: 5 | **1 / 1** |
| 10 | 1,686 | 58 | 35 | 0 | 1: 53, 2: 5 | 1: 34, 2: 24 | **1 / 1** |
| 12 | 25,950 | 685 | 315 | 0 | 1: 517, 2: 168 | 1: 253, 2: 432 | **1 / 1** |
| 14 | 434,580 | 9,470 | 3,350 | 0 | 1: 5,139, 2: 4,331 (all, exact) | sample of 300 (exact): eg = 1 for 67 | **1 / 1** |
| 16 | 7,985,964 | 148,805 | 41,470 | 20 | sample of 300: 1: 103, 2: 197 | sample of 300 (heuristic): eg ≤ 1 for 28; one verified from its face list (`out/witness_rp2_n16.txt`) | **1 / 1** |

Other facts:
- There is no og = 0 violator anywhere (n ≤ 14 all, n = 16 sample). This reconfirms the planar R0 data for all L at n ≤ 14, and independently by `planar_census.py` up to n = 16 (§3.1).
- At n = 8, all 5 violators are abstractly planar (og_free = 0); at n = 10, 34 of 58 are. Only the prescribed rotation makes them non-planar.
- Most violators close already with L = 5 (n = 16: 145,279 with minimum L = 5, 3,526 with minimum L = 10).
- **V2 is no better:** V2 violators with eg = 1 are 5, 25, 136 at n = 8, 10, 12, and those with og = 1 are 5, 30, 218.

### 2.2 The n = 8 witness (checkable by hand)

G has H = 0-1-2-3-4-5-6-7-0, chords (0,2), (0,3), (0,4), (1,6), (5,7), and v = 0.
- Labels: f_0 = (0,7), f_1 = (0,3), f_2 = (0,1), f_3 = (0,4), f_4 = (0,2).
- The prescribed rotation at v therefore visits the neighbours 7, 3, 1, 4, 2.

The closed R0 sequence has period 5 (L = 5, or L = 10 by repetition):

| t | M_t | v-edge |
|---|---|---|
| 0 | 01 23 45 67 | f_2 |
| 1 | 12 34 56 70 | f_0 |
| 2 | 04 16 23 57 | f_3 |
| 3 | 03 12 45 67 | f_1 |
| 4 | 02 16 34 57 | f_4 |
| 5 | = M_0 | |

- The frames are k_t = 2 − 2t ✓, and consecutive matchings are disjoint ✓.
- **Every** M_t ∪ M_{t+1} is a Hamiltonian cycle: 0-1-…-7, 0-7-5-6-1-2-3-4, 0-4-5-7-6-1-2-3, 0-3-4-5-7-6-1-2, 0-2-3-4-5-7-6-1 [hand].

The RP² embedding has faces (vertex cycles) [0,7,6,1,2], [0,7,5,4,3], [0,3,2,1], [0,1,6,5,4], [0,4,3,2], [5,6,7].
- Each edge lies on exactly two faces.
- The link of v reads f_0 f_4 f_3 f_2 f_1, the reverse of the prescribed rotation, so the rotation is as required.
- χ = 8 − 13 + 6 = 1, so the surface is RP².
- The two face classes across non-H edges are {F1, F4, F5} and {F2, F3, F6}, and every H-edge separates them, so **H is separating** [hand, also `genus -sepP`].
- The primal (dual + x) is a simple triangulation of RP² with 7 vertices.

The torus embedding has faces [0,7,6,1,0,4,3,2], [0,7,5,4,3], [0,3,2,1], [0,4,5,6,1,2], [5,7,6] (χ = 0, orientable). Its primal is not simple: one face meets v twice.

Read by `verify_embed.py "<line>" 5 both`.

### 2.3 H separating, simple primal [data]

`genus -sepP` / `-sepT` enumerate all embeddings with the rotation at v. Each cell counts violators that have an embedding in the class, followed by the number of those where H is separating.

| | n = 8 | n = 10 | n = 12 | n = 14 | n = 16 (15k sample) |
|---|---|---|---|---|---|
| RP² embedding / with H separating | 5 / 5 | 34 / 34 | 253 / 253 | – | – |
| RP² with simple primal (always also H-separating) | 5 | 28 | 189 | – | – |
| torus embedding / with H separating | 5 / 5 | 53 / 40 | 517 / 329 | 5,139 / 2,817 | 5,258 / 2,542 |
| torus with simple primal | 0 | 0 | 0 | **0** | **0** |

Reading:
- **RP²: R0 fails for simple triangulations of RP² with H contractible.**
- **Torus: every off-sphere violator found so far needs a non-simple primal** (a face meets v twice, or two faces share two edges). This holds exhaustively for n ≤ 14 and in a 15k sample at n = 16.
- **Open sub-question [conjecture-level, weak]:** does R0 hold for *simple* torus triangulations? Small torus triangulations with a degree-5 vertex are few, so this may be a size effect.

### 2.4 Liftability: the off-sphere violations are not primal [data]

`lift_test.py`. Each cell gives the number of violators with an embedding on that surface, split by the best outcome over all its embeddings:
- **closed-lift**: a closed R0 walk through the Hamiltonian arc using only liftable states;
- **ham-lifts, no closed lift**: the Hamiltonian state lifts, but every closed walk needs a non-liftable state;
- **ham not liftable**: the Hamiltonian state is not liftable in any embedding.

| surface | n | violators tested | closed-lift | ham-lifts, no closed lift | ham not liftable |
|---|---|---|---|---|---|
| RP² | 8 / 10 / 12 | 5 / 34 / 253 (all) | **0** | 0 | 5 / 34 / 253 |
| RP² | 14 | 67 (all eg = 1 in the 300-sample) | **0** | 0 | 67 |
| RP² | 16 | 28 (heuristic eg = 1 in the 300-sample) | **0** | 0 | 28 |
| torus | 8 / 10 / 12 / 14 | 5 / 53 / 517 / 5,139 (all) | **0** | 5 / 40 / 329 / 2,817 | 0 / 13 / 188 / 2,322 |
| torus | 16 | 5,258 (15k sample) | **0** | 2,542 | 2,716 |
| Klein bottle | 8 / 10 / 12 | 5 / 58 / 685 (all) | **0** | 5 / 40 / 335 | 0 / 18 / 350 |
| Klein bottle, V3 graphs | 16 | 20 (all) | **0** | 0 | 20 |
| torus, V3 graphs | 18 | 64 (og = 1 among 660 found) | **0** | 18 | 46 |

Control population (`all_labelled.py 10`): among all 1,686 labelled graphs at n = 10, 956 embed in RP². In 512 of those, some RP² embedding has a liftable Hamiltonian state; for the 34 violators this happens 0 times. The torus "ham-lifts" counts equal the H-separating counts of §2.3 at every n.

[hand] Liftability needs H separating: if H is non-separating, some closed dual curve meets H once, so the holonomy is 1 or 2 plus a multiple of 3, never 0. Liftability is not automatic once H is separating: on RP² the core of the Möbius side crosses only chords (colour 3), so the state lifts iff an even number of chords pass through the crosscap. For violators that number is always odd here.

**[conjecture] R0-lift.** On any closed surface, no closed R0 sequence through a Hamiltonian pair has all its states liftable. This is equivalent to: no closed sequence of 4-colourings of T − x of this type.
- On the sphere it is R0.
- Off the sphere it has survived every test above.
- If true, the mechanism behind R0 is a statement about genuine primal colourings (Kempe-type dynamics of T − x), and the chord-diagram planarity is only how "every state lifts" shows up on the sphere.

### 2.5 Interpretation

- *As a graph statement*, R0 belongs with the chain-parity law (sphere-only).
- *As a primal statement* (R0-lift, §2.4) it belongs with NRC: no counterexample on RP², the torus or the Klein bottle in any test.
- The RP² witnesses with H separating show that the planar circle rule must be used on **both** sides of H. With one side a disc and the other a Möbius band, R0 fails already at n = 8.
- So an argument that treats the states as abstract perfect matchings must see the global sphere (genus 0), not just the Jordan property of the one curve H.
  - One-sided facts survive on these witnesses and so cannot be enough: A5v-type statements, local ordering at v, and disc-side non-crossing.
- An argument that uses only that every state is a genuine 4-colouring of T − x (liftable) is **not** ruled out by anything found here. That is the more promising reading of PROOF-ATTEMPT-1 §7's "missing planar invariant": a primal-colouring invariant, i.e. a Kempe / degree-type quantity of T − x, rather than a chord-diagram one.

## 3. Task 2: variants

### 3.1 Planar, Hamiltonian pair dropped

**Exhaustive census** (`planar_census.py`): all Hamiltonian plane G (v of degree 5, the rest cubic, simple) and all rotations at v realisable by a planar drawing. The rotation is read from a two-sided chord drawing of H + chords:
- ccw order: (to 1), inside chords by increasing endpoint, (to n−1), outside chords by decreasing endpoint;
- mirror images identified.

| n | Hamiltonian plane G (chord sets) | (G, rotation) pairs | D₋₂ has a cycle (R0 frame, any L) | D₋₁ has a cycle | D₋₁ cycles with a Hamiltonian arc in the SCC | min L (D₋₁) |
|---|---|---|---|---|---|---|
| 8 | 13 | 18 | **0** | 5 | 5 | 5 |
| 10 | 117 | 164 | **0** | 36 | 36 | 5 |
| 12 | 1,012 | 1,401 | **0** | 279 | 279 | 5 |
| 14 | 8,732 | 11,880 | **0** | 2,267 | 2,265 | 5 |
| 16 | 76,192 | 101,896 | **0** | 19,189 | 19,161 | 5 |

Components of M ∪ M' on D₋₁ cycles take the values {1}, {1,2}, {1,2,3}, {1,3}, {2}, {2,3}, so word values up to 3 occur.

**SAT** (`sat_noham.py`): planar, G Hamiltonian, no condition linking the M's to H, frame advance −2, k_0 ∈ 0..4. There are two placement cases for the Hamiltonian cycle at v:
- **Case A:** H through f_0 = (0,n−1) and f_2 = (0,1). Circle rule as in PROOF-ATTEMPT-1: virtual points [f_4][f_1][f_3]; side(f_1) ≠ side(f_3) = side(f_4).
- **Case B:** H through f_0 = (0,n−1) and f_1 = (0,1), i.e. adjacent in the rotation. Points [f_4][f_3][f_2], all three on one side. The ccw rotation f_1 f_2 f_3 f_4 f_0 puts f_2, f_3, f_4 on the inside with j_2 < j_3 < j_4; the mirror puts them outside in the same order [hand].
- All other placements are label shifts (absorbed by k_0) or reflections of H.

| L | n = 16 | 18 | 20 | 22 | 24 |
|---|---|---|---|---|---|
| 10 | UNSAT (5 s) | UNSAT (24 s) | UNSAT (126 s) | UNSAT (547 s) | not run (cap) |
| 20 | UNSAT (6 s) | UNSAT (28 s) | UNSAT (150 s) | not run | |

**Reading [data → conjecture].**
- On the sphere the R0 frame (pentagram order at v) closes **nowhere** at small n, Hamiltonian pair or not.
- The first known planar closure is C30#0 (n = 26, L = 20, no Hamiltonian pair). Planar closed advance −2 sequences without a Hamiltonian pair therefore first appear somewhere in 22 < n ≤ 26 for L = 10 / 20 (Hamiltonian G only; non-Hamiltonian plane G are not covered).
- Advance −1 closes from the smallest n, with period 5, almost always through Hamiltonian pairs.
- So closure on the sphere is governed by **which cyclic order** the visits follow (adjacent vs pentagram), not by a Hamiltonian condition. The Hamiltonian pair matters only for the rare large-n pentagram closures like C30#0.

**Star restatement [hand].**
- Put g_j := f_{2j}. Then f_{k−2t} = g_{k/2 − t}, where k/2 means k · 3 mod 5.
- So a frame advance of −2 in the rotation f is an advance of −1 in the cyclic order g = (f_0 f_2 f_4 f_1 f_3), the pentagram of f.
- So R0 says: on the sphere, a closed sequence through a Hamiltonian pair that visits the v-edges cyclically (advance −1 in *some* cyclic order g) forces the planar rotation at v to differ from the pentagram of g.
- Data: R0 violators that are planar with the star rotation number 5/5, 34/58, 249/685 and 1,918/9,470 at n = 8–14. These are planar advance −1 orbits whose graph can be re-embedded with the pentagram rotation, which needs a crosscap or a handle.

### 3.2 Hamiltonian at every even step (V2) and the NRC word (V3)

| | n = 8 | 10 | 12 | 14 | 16 | 18 |
|---|---|---|---|---|---|---|
| V2 violators | 5 | 35 | 315 | 3,350 | 41,470 | – |
| min surface (V2) | RP², torus | RP², torus | RP², torus | torus (og) | | |
| V3 violators | 0 | 0 | 0 | 0 | **20** (exhaustive) | ≥ 660 (L = 10, SAT TIMEOUT at 550 s) |
| min og / min eg (V3) | | | | | **2 / 2** (exact, all 20: Klein bottle) | **1** (64 of 660 have og = 1) / heuristic best eg = 2 (6 checked exactly: eg = 2) |
| genuine DL orbits on V3 graphs | | | | | 0 of 20 | 0 of 45 torus graphs checked |

Witnesses:
- V3 on the Klein bottle, n = 16: twist f552c, `out/v3_n16_lines.txt` line 1.
- V3 on the torus, n = 18: `out/witness_v3_torus_n18.txt`.
- Both were re-verified from their face lists. The word is 1212121212, and the frames are 2, 0, 3, 1, 4, ….

T1 (TrackU, genuine DL R-cycles, non-planar):
- `t1_n22_first` and the SAT-found n = 22 orbit have **orientable genus 2** (exact, 2^21 rotations).
- Their Euler genus is ≤ 4 and ≤ 3 (heuristic, 2M iterations × 20 restarts, stable).

Exact RP² status of V3 at n = 18: 6 graphs with heuristic eg = 2 were run exhaustively (2^28 twist vectors each, 260 s in total). All 6 have **eg = 2 exactly** (no RP²). This is a spot check only; the 660 graphs are themselves an incomplete enumeration (SAT TIMEOUT).

## 4. Literature (WebSearch / WebFetch; [recall] where unchecked)

No source states R0, or any statement about cyclic sequences of pairwise-consecutive-disjoint perfect matchings with a rotating v-edge. The leads below are ranked by how plausibly they could supply the invariant that §2.4–2.5 point to: a quantity of *genuine* (liftable) 4-colourings of T − x.

1. **Kempe–Heawood rotation at a degree-5 vertex; the Kempe–Kittell algorithm.**
   - Heawood (1890) found that Kempe's double chain interchange at a degree-5 vertex can fail. Kittell (1935) proposed random chain switches between any two neighbours.
   - Gethner et al., *Involve* 2(3) (2009) 249–265, test Kempe and Kittell recolouring. **The conjecture that the Kempe–Kittell procedure always halts is reported open** (Wagon's account) [web abstract].
   - An R-cycle / R0 orbit is a non-halting rotation of exactly this kind (each DL step is M_{t+1} = M_{t−1} Δ Y_t, a Tait-colour switch along the chain through v, R1 of PROOF-ATTEMPT-1).
   - So NRC/R0 is a precise, Hamiltonian-pair version of "Kempe–Kittell halts" [hand]. Worth citing as context; no proof technique found.
2. **Fisk's degree of a 4-colouring.**
   - Fisk (*Adv. Math.* 24 (1977) 298–340, "Geometric coloring theory") views a 4-colouring of a triangulation as a simplicial map T → ∂Δ³ ≅ S² and uses its degree [web summary].
   - Tutte gave a parity formula for this degree in terms of vertex degrees.
   - Mohar–Salas (arXiv 0901.1010) show the degree mod 12 is a Kempe invariant for 3-colourable triangulations of closed orientable surfaces [web abstract].
   - Our R0 states are near-Tait colourings ↔ 4-colourings of T − x (the pentagon link uses 4 colours).
   - The relative degree (with the boundary pentagon loop) is an integer, unlike the mod-3 Heawood count that R6 showed to close automatically. It is a natural candidate for the missing invariant [conjecture].
   - The degree is defined exactly for **liftable** states, i.e. genuine colourings, on any closed orientable surface. That is the same scope in which R0-lift has survived on the torus (§2.4), which makes it a better fit than any chord-diagram quantity.
   - On RP² and the Klein bottle only the mod-2 degree is available. Tutte's formula involves vertex degrees, so χ can enter [hand].
3. **Penrose's formula / Kauffman.**
   - For a *plane* cubic graph each Tait colouring contributes the same sign to the ε-tensor sum (Penrose; Kauffman's vector-cross-product reformulation; the Penrose–Kauffman polynomial, arXiv 2604.16635) [web abstract].
   - The corresponding sign product Π_w s_t(w) is **constant along every R0 sequence in every graph** [hand]:
     - w flips sign iff M_{t+1}(w) = M_{t−1}(w);
     - such w come in pairs (the edges of M_{t−1} ∩ M_{t+1}, none at v).
   - So a Penrose-sign argument cannot obstruct closure, just as the mod-3 Heawood count cannot (R6). Recorded to avoid re-trying it.
4. **Smith / Thomason (lollipop).**
   - Every edge of a cubic graph lies on an even number of Hamiltonian cycles (Smith; Tutte's counting proof; Thomason's constructive lollipop walk) [web].
   - R0 concerns Hamiltonian cycles that are unions of consecutive matchings. A lollipop-type parity count of "Hamiltonian arcs on D-cycles" is the obvious *counting* route.
   - **Caveat:** the n = 8 RP² witness has every consecutive union Hamiltonian. Any such parity must therefore use liftability (or χ = 2) [hand].
   - Cousins: Kotzig's perfectly 1-factorable cubic graphs (every two colour classes form a Hamiltonian cycle) and the PMH property (Las Vergnas, Häggkvist; Abreu–Gauci–Labbate–Romaniello–Zerafa) [web]. Our n = 8 witness is a 5-cycle of matchings whose consecutive unions are all Hamiltonian.
5. **Kempe equivalence of edge-colourings.**
   - Mohar ("Kempe equivalence of colorings", 2006, vertex colourings; open questions) [web].
   - Belcastro–Haas: all 3-edge-colourings of planar bipartite cubic graphs are edge-Kempe equivalent (arXiv 1209.1730) [web abstract].
   - Goedgebeur–Östergård, "Switching 3-edge-colorings of cubic graphs" (arXiv 2105.01363): computations up to order 30, families with 2^n classes [web abstract].
   - Bonamy–Bousquet–Feghali–Johnson proved Mohar's k ≥ 4 regular conjecture (vertex Kempe) [web].
   - Fisk / Mohar–Salas / recent RP²–Klein results on Kempe equivalence of 4-colourings of 3-colourable triangulations [web].
   - None treats switching restricted to the chain through a degree-5 vertex with a rotating frame, and none gives a sphere-only invariant for non-bipartite planar cubic graphs (the planar non-bipartite edge-Kempe question appears open).
6. **Heawood mod 3 / Lerner** (arXiv 2411.15992, Heawood spins as an F_3 linear system) [web abstract]: the mod-3 level is already exhausted by R6.
7. Temperley–Lieb / Kauffman bracket formulations of map colouring [recall]: not checked; same planar-sign family as item 3.

## 5. Consequences for the proof programme

1. **The chord-diagram route needs the whole sphere.** A proof of R0 that works with the near-Tait states as abstract perfect matchings must use non-crossing on both sides of H.
   - R0 fails on RP² even with H bounding a disc, already at n = 8.
   - So one-sided Jordan facts are ruled out: A5v-type statements, local order at v, and disc-side non-crossing.
   - So are mod-3 and sign-product invariants (R6, §4.3).
2. **The primal route looks surface-free [conjecture R0-lift, §2.4].**
   - Every off-sphere violation uses a state that is not a 4-colouring of T − x.
   - With liftability imposed, R0 survives on RP², the torus and the Klein bottle at every size tested.
   - This matches SCOPE-A5v's finding that off the sphere A5v is "liftable + ¬inA". It suggests looking for the R0 mechanism in **Kempe dynamics of genuine 4-colourings of T − x**, where it might hold on every surface like NRC, rather than in the chord diagram.
   - The lift condition also kills the RP² Hamiltonian state outright: there the Hamiltonian state of a violator is never liftable.
   - **Next test:** an exact R0-lift search at larger n on a fixed surface. This needs an RP² / torus embedding encoding plus holonomy constraints in SAT; it is not attempted here.
3. **Sharper sphere target [conjecture]:** on the sphere, the frame digraph D₋₂ (pentagram visits) has no cycle through a Hamiltonian arc.
   - Small-n data say more: D₋₂ is acyclic outright for n ≤ 16, while D₋₁ (adjacent visits) cycles freely through Hamiltonian arcs.
   - Candidate invariants: the relative Fisk degree of the (liftable) states combined with Σ(6 − deg) = 12 (§4.2). Or a holonomy/degree count, given that liftability is what fails off the sphere.
4. **NRC-like variants are more robust off the sphere even without liftability:** V3 needs the Klein bottle or the torus and n ≥ 16 / 18, and T1 needs orientable genus 2.
   - Whether a genuine DL R-cycle exists on RP² or the torus is not settled here. None of the V3 torus graphs found carries a DL orbit, and none survives liftability.

## 6. Files (all in `axioms/r0surfaces/`)

| file | content |
|---|---|
| `r0enum.py`, `out/r0enum_n{8..16}.jsonl` | exhaustive R0 / V2 / V3 census, all L (n = 16: 148,805 records, 5.5 min) |
| `xcheck_sat.py` | census = SAT encoder cross-check |
| `genus.c`, `egheur.c` | exact and heuristic genus (compile: `cc -O2 -o genus genus.c`, `cc -O2 -o egheur egheur.c -lm`; binaries not committed) |
| `verify_embed.py` | explicit witnesses, face-list re-check |
| `planar_census.py`, `out/planar_census_n{8..16}.jsonl` | planar D₋₂ / D₋₁ census |
| `sat_noham.py`, `out/noham_L10.txt`, `out/noham_L20.txt` | planar, no Hamiltonian pair |
| `v3sat.py`, `out/v3sat_n18_L10.txt`, `dlcheck.py` | V3 search and DL check |
| `summarise.py` | §2.1 tables |
| `out/genus_*`, `out/sep*`, `out/egheur_*` | genus outputs (line-aligned with the corresponding `r0lines_*` / jsonl inputs) |
| `lift_test.py`, `all_labelled.py`, `out/lift_*.txt` | liftability tests (§2.4) |
| `out/witness_*.txt` | witnesses quoted above |

Not committed (size; regenerate):
- `out/r0enum_n16.jsonl` (33 MB): `python3 r0enum.py 16`, 5.5 min;
- `out/planar_census_n16.jsonl` (4 MB): `python3 planar_census.py 16`, 65 s;
- the derived line files and random samples: `python3 samples.py` (seeds 1, 2, 3; checked to reproduce the files used);
- `out/all_labelled_n10.txt`: `python3 all_labelled.py 10`.

Reproduce §2.2: `python3 verify_embed.py "8 13 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7 0 0 2 0 3 0 4 1 6 5 7 7 9 0 10 8" 5 both`.
