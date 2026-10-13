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
