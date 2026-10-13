# flips/ — two-triangulation (Whitney / Eliahou / Kauffman) form of 4CT: exhaustive small-n tests

Status: **exploratory**, Long Table, 2026-10-13. About 50 minutes of work. Nothing here is a proof. Every number
below comes from the exact programs in this folder, and the output files are committed beside them.

## Setting

Whitney: a triangulation with no separating triangle is Hamiltonian. Cutting along the Hamilton cycle gives two
triangulations T1, T2 of a convex n-gon. So 4CT is equivalent to this: for every pair (T1, T2), the graph
H = C_n + diag(T1) + diag(T2) is 4-colourable. Colourings are normalised with c0=0, c1=1. Then

* G = proper colourings of C_n, with |G| = (3^n + 3(-1)^n)/12.
* L(T) = colourings in G that are proper on T's diagonals (T's "boundary language"; every vertex is on the boundary).
* S(T1,T2) = L(T1) ∩ L(T2). 4CT ⇔ S ≠ ∅. Here |S| = P(H,4)/12.

Literature equivalences, from memory and not re-checked against the papers:
* Eliahou, *Signed diagonal flips and the four colour theorem*, Eur. J. Combin. 20 (1999). Gravier–Payan,
  Eur. J. Combin. 23 (2002), proved that his signed-flip conjecture is equivalent to 4CT. **I do not reliably
  remember the exact sign rule.** So below I test the colour-preserving flip-path version instead (see (c)), and I
  believe that version is the same phenomenon.
* Kauffman, *Map coloring and the vector cross product* (JCTB 1990): two bracketings of x1 × ... × x_{n-1} in R^3
  have an assignment from {i,j,k} that makes them equal and non-zero. **Checked here:** "equal" and "equal up to
  sign" coincide. When no intermediate product is zero, the cross product of distinct units is the quaternion
  product, and that product is associative. So every common colouring gives the *same signed* value
  (computed: n ≤ 8 for all common colourings, n ≤ 10 for existence; `kauffman-out.txt`).
* Kryuchkov's conjecture: I recall only that it is another polygon/diagonal reformulation. I did not test it and
  will not state it from memory.

## Files

| file | what |
|---|---|
| `baseline.c` | exact bitset check of S ≠ ∅ for all pairs (T1 over dihedral orbit representatives, T2 over all); min/histogram of \|S\| |
| `dissect.c` | exact check of the dissection bound (A′) below |
| `analysis.py` | Python tests: `density`, `window`, `flips`, `kauffman`, `kempe`, `halving`, `dissect` (`python3 analysis.py TEST n`) |
| `*-out.txt` | raw outputs (JSON lines / text) |

No SAT solver was needed (pysat is not installed). All vertices are on the cycle, so a bitset over L(T1) with one
mask per chord decides every pair exactly.

## 1. Baseline (sanity, not news)

`baseline-out.txt`, `baseline-out-14.txt`: **for n = 5..14 every pair (T1,T2) is 4-colourable** (n=13: 2282 T1 representatives × 58786 T2 =
1.34·10^8 pairs, 15 s; n=14: 7528 × 208012 = 1.57·10^9 pairs, 372 s).
For every n, the minimum of |S| is 2, i.e. P(H,4) = 24: uniquely 4-colourable (stacked) unions occur at every n.

## 2. Strengthened / inductive statements

### (a) Precoloured boundary windows (Thomassen style) — dies at n=5

* One boundary edge (2 consecutive vertices) extends. This is trivial by colour symmetry.
* 3 consecutive vertices, colours proper on the induced union graph: **fails at n=5**. Example: T1={14,24},
  T2={03,13}. Here 0 and 2 are non-adjacent but receive equal colours in every 4-colouring, so the window 0,1,2 with
  three distinct colours cannot be extended. The share of pairs with a non-extendable 3-window is 16.2% at n=7 and
  17.0% at n=9. Windows of 4–6 vertices fail more often (as low as 2.4% of window colourings extendable).
* "Any two non-adjacent vertices can be coloured equal, and can be coloured different" fails at n=5 for the same
  reason (forced equalities).
Verdict: boundary precolouring is useless for 4 colours. This is expected: stacked triangulations force equalities.

### (b) Languages L(T): sizes, density, Kempe structure

* **|L(T)| = 2^(n-2) for every T** (a triangulated polygon is a 2-tree). So all languages have exactly the same size.
* The union ∪_T L(T) = G, except for the alternating 2-colouring when n is even. So no smaller common ground set
  helps, and ∩_T L(T) = ∅ for n ≥ 5.
* **Density |L(T)| / |G|**, which is exact and the same for every T:

| n | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|
| \|G\| | 20 | 61 | 182 | 547 | 1640 | 4921 | 14762 | 44287 | 132860 | 398581 |
| \|L\| | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 |
| density | 0.400 | 0.262 | 0.176 | 0.117 | 0.078 | 0.052 | 0.035 | 0.023 | 0.015 | 0.010 |

  Density = 12·2^(n-2)/(3^n+3(-1)^n) ~ 3·(2/3)^n → 0. It is **already below 1/2 at n=5**. A pure pigeonhole or
  counting proof is dead on arrival.
* Common colourings: min |S| = 2 for all n. The mean |S| is 4.0, 5.3, 7.0, 9.5, 12.7, 17.2 for n=5..10. That is
  about 1.25–1.3 × the random-subset prediction |L|²/|G|: positively correlated, but tiny.
* **Kempe connectivity of the colourings of H fails at n=8** (`kempe-out.txt`). In 23 of 1584 pairs (T1 over
  orbit representatives), the 4-colourings of H form 2 Kempe classes. Example: T1={17,27,36,37,46},
  T2={05,06,15,24,25}. H is a genuine 8-vertex triangulation (18 edges) with 72 colourings = 3 classes mod
  permutation, in 2 Kempe classes. I cross-checked this with an independent brute force. There is one class for
  all pairs at n ≤ 7.

### (c) Flips

* For a flip T→T′ in the quadrilateral abcd (ac → bd): L(T) ∩ L(T′) = {c ∈ L(T) : c(b) ≠ c(d)}. This is **exactly
  half** of L(T) for every flip (verified for every flip, n ≤ 10). L(T′) \ L(T) is the set of colourings with
  c(a) = c(c).
* **Fixed-colouring flip graphs are not connected.** For a colouring c, the flips among the triangulations T with
  c ∈ L(T) form a disconnected graph for 8/60 colourings at n=6, 28/182 at n=7, 68/546 at n=8, 152/1640 at n=9
  and 320/4920 at n=10. First example at n=6: c = (0,1,0,2,1,2) has 2 proper triangulations that are not flip-adjacent.
* **Colour-preserving flip path (Eliahou-type form): survives n ≤ 9.** For every pair there is some c ∈ S and a
  flip path T1 → T2 through c-proper triangulations. This is formally stronger than 4CT, because of the
  disconnection above. The path is never much longer than a geodesic. Excess histogram at n=9: 0 for 10449
  pairs, +1 for 1129, +3 for 5 (`flips-out.txt`).
* **"Some flip geodesic keeps one colouring proper" fails at n=7**: 4/168 pairs, e.g. T1={16,26,35,36},
  T2={04,05,14,24}, with d=5 and |S|=10. At n=10 it fails for 16770/117260 pairs.

### (d) Counting bounds — the one family that survives everything tested

* (B) Per-step: "adding one outside chord e to T1+D keeps at least half the colourings". **Fails at n=5**
  (T1={14,24}, D={03}, e=02: 6 → 2).
* (C) "Some order of adding T2's diagonals keeps at least half at every step". **Fails at n=8** (1 pair:
  T1={17,26,27,35,36}, T2={05,06,14,15,24}) and for 34 pairs at n=9.
* (A) **Aggregated: |S(T1,T2)| ≥ 2^(n-2-m), with m = |T2 \ T1|.** No failures for n ≤ 9 (`halving-out.txt`). This
  implies |S| ≥ 2^(n-2-d) with d = the flip distance (no failures for n ≤ 10, `flips-out.txt`).
* (A′) **Dissection bound**: for every triangulation T1 and every dissection D (non-crossing chords drawn outside),
  #col(T1+D) ≥ 2^(n-2-|D\T1|). Normalised as above, this says P(H,4) ≥ 24·2^{ex}, where ex = Σ over the outer
  faces of (|F|-3) is the number of edges missing from a triangulation. **No failures for n ≤ 13**:
  3.8·10^8 (T1 rep, D) checks at n=12 and 6.0·10^9 at n=13. The bound is sharp: equality occurs at every k
  (`dissect-c-out.txt`, `dissect-out.txt`). With k = n-3 and D ∩ T1 = ∅, this is exactly 4CT (P ≥ 24).

  A′ for a single quadrilateral outer face follows from 4CT: P(H) = P(H+uv) + P(H/uv) ≥ 24 + 24. The same
  deletion–contraction fails to give the bound for a pentagonal face. Contracting a distance-2 pair there drops the
  excess by 2, which only gives P ≥ 72 against the needed 96. So **A′ appears to be a genuine strengthening of 4CT,
  not a corollary**. I do not know whether it is in the literature; it resembles a Birkhoff–Lewis-type lower bound
  at λ=4.
  An induction on n removing an ear v of T1 works when deg_D(v) ≤ 1. A minimal counterexample therefore has every
  ear of T1 carrying ≥ 2 chords of D. That is the usual degree ≥ 5 territory, and it was not explored further.

## 3. Kempe chains on the polygon

A flip of ac → bd keeps exactly the colourings with c(b) ≠ c(d). If c ∈ L(T) has c(b) = c(d), the fix is a
Kempe switch at b or d in the union graph. This is the degree-4/5 Kempe argument under another name. The Kempe
failure at n=8 shows that the colourings of H need not be Kempe-connected, so "walk inside S by Kempe moves" is not
available either. The flip calculus repackages the Kempe obstruction; it does not remove it.

## Honest assessment

* Survivors: the colour-preserving flip-path form (n ≤ 9) and, most interesting, the **counting bound A′ /
  A (|S| ≥ 2^(n-2-m))**, which is sharp and has no failures for n ≤ 13 / n ≤ 9.
* Dead: precoloured windows (n=5), per-step halving (n=5), ordered halving (n=8), geodesic colour-preservation
  (n=7), Kempe-connectivity of the union's colourings (n=8), connectivity of fixed-colour flip graphs (n=6), and any
  density/pigeonhole argument (density 0.4 at n=5, decaying like (2/3)^n).
* Inductive handle: **weak**. Every per-step or locally inductive form tested fails at small n. Only aggregated
  statements survive, and their base case (k = n-3) is 4CT itself. An induction on n for A′ runs into the
  same high-degree reducibility problem as the classical proof. A′ is the one candidate worth a second look,
  as a quantitative strengthening that might suit a different induction (e.g. on faces of size ≥ 5). I would not
  call this route promising for a short proof.

---

# Run 2 — Bound A′: literature, general form, induction lemmas (2026-10-13, about 60 min, exploratory)

Recap of A′: for H = C_n + T1 + D (T1 a triangulation of the polygon, D non-crossing chords drawn outside),
P(H,4) ≥ 24·2^m, where m = 3n−6−|E(H)| is the number of missing edges. Nothing below is a proof. Every claim
marked "verified" comes from the exact programs listed here. The literature notes come from web search summaries
(abstracts only) plus my recall, and are marked as such.

## New files

| file | what |
|---|---|
| `gentri.py` | all sphere triangulations on n vertices (flip-BFS from the double wheel, networkx iso); counts 1,1,2,5,14,50,233 for n=4..10 match the known sequence |
| `planecount.c` | exact P(G,4) for **every embedded spanning subgraph of every triangulation** (that is, every connected simple plane graph), n ≤ 10, via a monochromatic-edge histogram plus a subset-sum transform. Classes: 1 connected, 2 2-connected, 3 2-connected with every 2-cut an edge, 4 3-connected. Also runs the general one-chord lemma tests (n ≤ 9) |
| `faceconst.py` | sharp per-face constants from the `SIG` lines |
| `lemmaA.c` | dissect.c plus one-chord induction lemmas *inside the A′ class* (n ≤ 12) |
| `lemmaC.py` | structural reduction lemma inside the A′ class (n ≤ 10) |
| `verify_n10.py`, `edgesum13.py`, `ico_minus_vertex.py` | independent brute-force checks of the counterexamples below |
| `run2/` | all outputs (`planecount-out-n.txt`, `lemmaA-out.txt`, `lemmaC-out.txt`, `faceconst-out.txt`, `tri-n.txt`, …) |

There is no plantri in the repo. I did not download it; gentri.py stands in for it.

## 1. Literature verdict

* **Birkhoff–Lewis** (1946): P(G,λ) ≥ λ(λ−1)(λ−2)(λ−3)^{n−3} for planar G, proved for λ ≥ 5 and conjectured for
  λ ≥ 4. At λ = 4 this gives only 24 (= 4CT), and it **ignores missing edges entirely**. At λ = 5 it is the
  known sharp bound 60·2^{n−3}, attained by stacked triangulations. A′ is *not* a Birkhoff–Lewis consequence.
* **Thomassen** (2^{n/9} 5-list-colourings) and follow-ups (correspondence colourings, Postle–Smith-Roberge) are all
  about 5 colours. There is nothing exponential for 4 colours in general, because uniquely 4-colourable
  triangulations exist.
* **Closest match: Albertson–Wilf, "Boundary values in the four color problem", Trans. AMS 181 (1973) 471–482**
  (abstract only; I could not fetch the paper). Let G be planar with outer boundary a k-cycle, and let ψ = the number
  of boundary colourings that extend. They show that 4CC ⇒ ψ ≥ 3·2^k for k = 3..6, they **conjecture ψ ≥ 3·2^k
  for all k**, and they prove ψ ≥ c·φ^k unconditionally (φ the golden ratio). Annuli satisfy the conjecture.
  Note that 3·2^k = 24·2^{k−3}, and k−3 is exactly the number of edges missing from G. Since P(G,4) ≥ ψ, **the
  Albertson–Wilf conjecture implies the one-hole case of A′**: one non-triangular face, inner side an arbitrary
  near-triangulation. In normalised form it reads |boundary language| ≥ 2^{k−2} = |L(T)|. I did not find out
  whether the AW conjecture is now settled. *To check against the paper.*
* Dvořák–Lidický, "Coloring count cones of planar graphs" (arXiv 1907.04066) studies the vector of extension
  counts on a 5-cycle and makes a cone conjecture that strengthens 4CT. It is the same family of ideas, but it
  does not state A′.
* **Verdict: (ii) for one hole, (iii) in general.** The single-hole case of A′ is a consequence of the open
  Albertson–Wilf conjecture, which itself rests on 4CT for k ≤ 6. The multi-hole statement A′ (many
  non-triangular faces on the far side of a Hamilton cycle) was not found in the literature as far as I searched,
  so it is *apparently new*. Since its natural generalisation is false (§2), the structure of A′ is load-bearing.

## 2. Generalising beyond the polygon setting (n ≤ 10, all connected simple plane graphs)

"miss" = 3n−6−|E| = Σ_faces (|f|−3). Test: P(G,4) ≥ 24·2^miss. Graphs are counted as embedded edge subsets, so
there are repeats.

| n | class 1 conn. fails/total | class 2 2-conn | class 3 2-conn + all 2-cuts edges | class 4 3-conn |
|---|---|---|---|---|
| 8 | 1906521/2135114 | 161784/322112 | **0**/32652 | 0/6067 |
| 9 | 52658633/58401302 | 3695188/7160719 | **0**/530458 | 0/83785 |
| 10 | 1.89e9/2.08e9 | 1.09e8/2.08e8 | **3160**/11307343 | **3160**/1489953 |

* **Cut vertices:** for blocks B_i, P = ∏P(B_i)/4^{b−1} and miss = Σmiss_i + 3(b−1). The ratio therefore picks up
  an exact factor **(3/4)^{b−1}**. This is sharp: trees, with K2 blocks, attain it with equality.
* **Non-adjacent 2-cuts:** C_4 gives 84 < 96 (factor 7/8). For C_n, P/(24·2^miss) ≈ (8/3)(3/4)^n → 0, so there
  is no constant-factor bound for 2-connected graphs.
* **Class 3 holds for n ≤ 9 and fails at n = 10, even for 3-connected graphs.** Smallest counterexample, checked by
  independent brute force (`verify_n10.py`): a cubic 3-connected plane graph with n=10, |E|=15, faces
  3,3,3,5,5,5,6, edges 01 07 09 12 17 23 28 34 38 45 49 56 59 67 68. **P = 9480 < 24·2^9 = 12288** (ratio 0.77).
  Two more: faces (5,5,5,5) with P=5976 < 6144, and (4,4,5,5,6) with P=11784 < 12288. The mechanism is that sparse
  (cubic) graphs have only about 2.6^n colourings (Bethe-type heuristic), while 2^miss ≈ 2^{1.5n} ≈ 2.83^n.
* **Density does not rescue it:** "class 3 and |E| ≥ 2n−3" has no failures for n ≤ 10, but an edge 2-sum
  multiplies ratios (P = P1·P2/12). Gluing a stacked K5 onto edge 01 of the counterexample gives n=13, |E|=23 =
  2n−3, P = 18960 < 24576 (`edgesum13.py`).
* **Sharp face constants c_k** (largest c_k with P ≥ 24·∏c_{|f|}):
  * class 3 (n ≤ 10): **c_k = 2^{k−3} exactly**. A single k-face attains equality for every k ≤ 10 (it is the
    one-hole A′ / Albertson–Wilf case), and so do 30+ mixed signatures. Pentagons do **not** allow more than 4.
    Yet the product form fails at n=10 (above), so no per-face constant law holds in class 3 beyond single-face
    or A′-structured cases.
  * 3-connected, single k-face: min P/24 = 3, 5, 11, 21, 43 for k = 4..8 (Jacobsthal, attained by wheels:
    (2^k+2(−1)^k)/6), which is about (4/3)·2^{k−3}.
  * class 2, single face: 2^{k−3} (equality). Class 1, single facial walk: c = 2, 3, 4.5, 9, 13.5, … (cut-vertex
    factors).
* **So the right general statement is not "2^missing for all plane graphs".** The safe statements are
  (a) single non-triangular face (near-triangulation with outer k-cycle): P ≥ 3·2^k. This is implied by
  Albertson–Wilf, with no failures for n ≤ 10.
  (b) A′ itself: all non-triangular faces on one side of a Hamilton cycle whose other side is triangulated
  without interior vertices. No failures for n ≤ 13 (Run 1).
  The untested joint generalisation A″ allows an arbitrary near-triangulation inside the cycle, with outside
  chords D between cycle vertices. Both the n=10 counterexample and the n=13 edge-sum lie outside A″, because
  their non-triangular faces cover vertices not on any such cycle. A″ is the natural next conjecture to test.

## 3. Induction by deletion–contraction (P(G) = P(G+e) + P(G/e), e a chord of a face)

Lemma **S** (strong): some chord e has P(G/e) ≥ P(G+e). Lemma **W** (weak): some chord e has
P(G/e) ≥ 24·2^{miss−1}. Either lemma, plus the bound for G+e (one fewer missing edge), gives the bound for G. The
induction bottoms out at triangulations, i.e. at 4CT. So **A′ ⇔ 4CT + (W within the A′ class)**. W is the exact
extra content of A′ beyond 4CT, if W is true.

| test | result |
|---|---|
| S, general 2-connected | fails at n=4 (C_4). Fails for 3-connected at n=6 (prism, P=264) |
| S, class 3, n=9 | 58751/530408 fail |
| **W, class 3** | holds for n ≤ 8; **fails at n=9**: 334 graphs, all 3-connected, e.g. faces 3,3,3,4,5,5,5 with P=3240 (edges 01 06 08 17 16 28 23 27 34 37 45 47 58 56) |
| S, A′ class (outside chords only) | fails at n=6 (T1 = fan at 0, D={15}: 10 colourings, best chord gives 4 < 5) |
| **W, A′ class** | **no failures for n ≤ 12** (3.7·10^8 (T1 rep, D) instances at n=12, 120 s). It is tight in many cases |
| C (structural): some admissible chord uw has ≥ 2 common neighbours and H/uw in class 3 | holds for n ≤ 9; **fails at n=10** (71 cases, every admissible chord has t=1), e.g. T1={02,03,04,05,57,59,79}, D={18,19,28,36,46} |

What W buys: it turns A′ into a one-step statement, "some outside chord has at least 2^{n−3−k} normalised
colourings with its ends equal". That statement is about H/uw, a graph on n−1 vertices that is no longer in the
A′ class. Lemma C, which tries to reduce W to the class-3 bound on H/uw, fails at n=10 when all chords have a
single common neighbour (pentagon-type faces: README Run 1's 72-vs-96 gap). The class-3 bound is false anyway at
n=10. So **no self-contained induction survives**. W in the A′ class is the surviving inductive statement
(n ≤ 12), but it is a statement about contracted graphs outside the class, and I have no handle on it.

## Run 2 assessment

* A′ is the multi-hole sibling of the 1973 **Albertson–Wilf conjecture** (ψ ≥ 3·2^k), whose single-hole case
  implies one-hole A′. As far as the search went, the multi-hole A′ is not in the literature.
* The "each missing edge doubles" law is **false for general plane graphs**: 3-connected cubic counterexample at
  n=10, and an |E| ≥ 2n−3 version at n=13. Its validity depends on the Hamilton-cycle/2-tree structure of A′
  (or on a single hole). Sharp constants in the valid settings are c_k = 2^{k−3}; pentagons give nothing extra.
* The one-chord induction survives only as Lemma W inside the A′ class (n ≤ 12). Its structural reduction dies at
  n=10, and the general versions die at n=4/6/9. Route status: an interesting quantitative conjecture, not a proof
  route.
