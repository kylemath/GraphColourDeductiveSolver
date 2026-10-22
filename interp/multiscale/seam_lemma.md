# The Seam Lemma: refuted. Three counterexample families and what could survive

Scripts: `/mnt/project-files/multiscale/tilt.py`, `vortex.py`, `rigid.py` (python-sat/Minisat22 + networkx). All the numbers below are reproducible from these.

## 0. Verdict

**The Seam Lemma is false, and its balanced version is false too.** There are three independent families.

| family | planar? | balanced split? | max degree | what blocks the repair | needed R |
|---|---|---|---|---|---|
| (T) tilt mismatch, triangular lattice, straight seam | yes | yes (two congruent parallelograms) | 6 | a height function: an additive invariant along the seam | grows linearly, about 0.45*L (L = seam length) |
| (V) vortex, triangular lattice disc minus a vertex | yes | no (B = {v}) | 6 | a height monodromy around v | R >= r-1 (r = disc radius) |
| (S) stacked (uniquely 4-colourable) triangulation | yes | roughly (A, B both long) | 9 | global rigidity carried through B | unbounded (no fix for R <= 11 at depth 13) |

The obstruction in (T) and (V) is principled. 4-colourings of Eulerian (all degrees even) regions have a 2-dimensional Lipschitz **height function**. A bounded-radius repair cannot reconcile two colourings whose heights drift apart along the seam (tilt mismatch), or whose height winds around a hole (vortex). Experiments missed this for two reasons. Random triangulations are full of odd-degree "defects". Colourings from solvers or hill-climbing on 200-vertex regions have small tilt, and the adversary never searched over tilts.

## 1. The height function (proved, elementary)

Identify the 4 colours with Z2^2 = {0, g, h, g+h}. For an edge uv, label(uv) = c(u)+c(v), which is nonzero. Each proper triangle carries the three distinct nonzero labels. Fix three unit vectors e_g, e_h, e_{g+h} in R^2 at 120 degrees, so their sum is 0.

Suppose the triangles of a simply connected near-triangulation can be properly 2-coloured "up/down". This holds exactly when every interior vertex has even degree, for example in any patch of the triangular lattice. Then set

  h(w) - h(u) = +e_{label(uw)} if the up-triangle at uw lies to the left of u->w, and -e_{label(uw)} otherwise.

The increments around an up triangle traversed counterclockwise sum to e_g+e_h+e_{g+h} = 0, and around a down triangle to minus that. So h is well defined up to a constant. Every edge changes h by a unit vector, so h is 1-Lipschitz in graph distance. (`tilt.py` checks closure on every triangle.)

A colour renaming is an affine map of Z2^2. All 24 permutations of 4 colours are affine, since |AGL(2,2)| = 24. It permutes the labels linearly, so h transforms by an orthogonal map P (an element of D3) plus a constant. **Norms of height increments therefore do not depend on the renaming.**

(This is the honeycomb 3-edge-colouring height of Baxter / Kondev-Henley, written in vertex language. Earlier I checked two Z2 invariants and both are vacuous. The "pairing" parity n_{12}+n_{34} ≡ F mod 2 on a disc is implied by n ≡ L ≡ F. The Z2^2 cocycle is exact, i.e. trivial.)

## 2. Family (T): tilt mismatch, balanced, planar, degree 6. Lemma fails for every R

Take the triangular lattice with vertices (i,j), neighbours ±(1,0), ±(0,1), ±(1,-1). Let U = {0<=i<=L, -D<=j<D}, with A = rows j<0 and B = rows j>=0. Both parts are parallelograms of the same size and the seam is a straight line.
- c_A = c22: c(i,j) = (i mod 2, j mod 2) in Z2^2. Every horizontal edge has label g, so h rises by exactly e_g at each step along a row. This is a tilt of slope 1, the maximum possible.
- c_B = c3: c(i,j) = (i+2j) mod 3, a proper 3-colouring. Along a row the labels cycle g, g+h, h, so the row increment over 3 steps is 0. This colouring is flat.

**Theorem (proved).** If L ≡ 0 mod 3 and L > 4R+6 (and D >= R+2), no renaming of B plus recolouring within distance R of the conflicts gives a proper colouring of U.

*Proof.* Conflicts lie in rows -1 and 0. Rows -(R+2) and R+1 are at distance > R from them, so they are fixed: they keep c_A and π c_B. Let f be any repaired proper colouring and h_f its height on U. Let x_t = (t, -(R+2)) and y_t = (t, R+1); then dist(x_t, y_t) = 2R+3. Along the fixed row, h_f(x_L) - h_f(x_0) = L e_g. Along the other fixed row, h_f(y_L) - h_f(y_0) = P·0 = 0. By the Lipschitz property,

  L = |h_f(x_L)-h_f(x_0)| <= |h_f(x_L)-h_f(y_L)| + 0 + |h_f(y_0)-h_f(x_0)| <= 2(2R+3).

This contradicts L > 4R+6. ∎

SAT check (`tilt.py`): the minimum R over all 24 renamings, with exact radius-R recolouring.

| L | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 24 | 30 | 36 |
|---|---|---|---|---|---|---|---|---|---|---|
| min R | 0 | 1 | 3 | 4 | 6 | 7 | 9 | 10 | 13 | 16 |
| proved lower bound ceil((L-6)/4) | 0 | 0 | 1 | 2 | 3 | 3 | 4 | 5 | 6 | 8 |

The truth is about 0.45*L: the repair must reach a fixed fraction of the seam length. More generally, if the two sides' tilts along the seam direction d differ in norm by δ, the theorem gives R >= δL/4 - O(1).

Answers to specific questions in the brief:
- **Does renaming plus radius freedom avoid blocked vertices?** Not in this example. The failure is not a single blocked vertex. It is a conserved, additive quantity, the height current, and that defeats any bounded window.
- **Heuristic (not proved).** Uniform random 4-colourings of flat regions are believed to be critical, with GFF-like heights (Kondev-Henley, approximate). Two independent random colourings would then mismatch along a seam by about log L, so even typical inputs would need R growing like log L. That slow growth is consistent with "R <= 4 up to 12k vertices". Geodesic domes have only 12 defects and are mostly flat, so they are the right place to test this: grow the frequency and measure R against tilt mismatch.

## 3. Family (V): single vertex, the colleague's item (1)

A = G - v, B = {v}, with G a hexagonal disc of radius r in the triangular lattice. Around the link 6-cycle of v, sum the height increments; the result is the monodromy. Of the 732 proper colourings of a 6-cycle, 360 have nonzero monodromy, of norm 2√3. Examples are (0,1,0,1,2,3) and (0,1,0,2,1,3), and all of these use 4 colours. SAT extends such a link to a colouring of G - v. That colouring has nonzero monodromy around every loop enclosing v, and every loop at distance > R+1 is fixed. Any proper colouring of the disc G has a single-valued height, so its monodromy is zero. Therefore **no repair works for any R < r-1.** The SAT result for r = 9 is: fails for R = 0..7, succeeds at R = 8 = r-1, where the repair reaches the outer boundary.

So the single-vertex reduction (the colleague's point that the stated lemma implies 4CT plus locality) is not just "stronger than 4CT". It is false, with a concrete planar witness.

**Balanced version (colleague's item 1).** Restricting to balanced splits does remove the single-vertex reduction formally. Family (T) is already balanced, though: two congruent parallelograms with a straight seam. So the balanced version is false as well. It is not "plausibly easier" in any sense that helps, because the obstruction is a 1-D drift along the seam and has nothing to do with the sizes of the parts.

## 4. Family (S): rigidity, and a check of the colleague's item (2)

The colleague's U-shaped P_N^3 example is non-planar. Fowler's theorem (approximate: uniquely 4-colourable planar graphs are exactly the stacked triangulations) does **not** block a planar version. The trick is not to bend the strip, but to interleave A and B along it.
- Core: x1..xm with x_i adjacent to x_{i-1}, x_{i-2}, x_{i-3}. This is P_m^3, stacked and uniquely colourable as c(x_i) = i mod 4.
- Pendant stacked chains: y1..yk inserted into the face (x1,x2,x4), and z1..zk into the face (x_{m-3},x_{m-2},x_m). Each new vertex goes into the face formed by its predecessor triple.
- A = odd x's (a path) ∪ y-chain ∪ z-chain. B = even x's (a path). Both are connected, and the graph is planar.
- c_B is the unique colouring. c_A is the unique colouring on the y's, a transposition of it on the z's, and the odd path recoloured to fit. A is flexible because the odd path carries no rigidity.

*Proof that it fails.* U is uniquely colourable, so any repair equals τ·c_U. The deep y's (distance > R from the seam) force τ = id. The deep z's force τ = σ. Contradiction.

SAT (`rigid.py`, m=24, k=40, n=104, max degree 9): uniqueness confirmed; repair fails for every R in 0..11.

This family is degenerate: the seam is interleaved and there are many separating triangles. It is worth recording only because it shows that planarity does not rescue the lemma. Family (T) is the decisive one.

**Colleague's item (3), Errera/Kittell single-vertex tests:** not run. Family (V) already settles the single-vertex case negatively, with R forced to grow linearly in the radius. Kempe-chain-length families would at best give another lower bound of the same kind.

## 5. What could survive (weakest natural repairs, all conjectural)

1. **Bounded-mismatch seam lemma.** Restrict to input pairs whose height discrepancy along the seam (after the best renaming) varies by at most M, with no vortices near the seam. Conjecture: R = O(M) + O(1) in flat regions. To use this, the hierarchy must maintain an invariant, e.g. "every cluster colouring is flat (bounded tilt) along its boundary". It is not known that such colourings always exist with the other constraints, so this is open, and it is the central difficulty.
2. **Defect-dependent R.** At odd-degree vertices the up/down 2-colouring breaks: h becomes multivalued with D3-type monodromy, and tilt may be dumpable there. Conjecture: R bounded in terms of Δ and the longest seam stretch with no odd vertex within a fixed distance. This fits the experiments (dense defects). It cannot handle all triangulations, because large Eulerian (3-colourable) patches exist. Those would need separate treatment, e.g. canonical 3-colourings, which are flat.
3. **Unbounded Kempe changes inside A or B.** In family (T), U is 3-colourable, so all its 4-colourings are Kempe equivalent (Mohar, approximate) and the merge succeeds. But this gives up locality. For general planar triangulations, Kempe-equivalence of all 4-colourings is, I believe, open, and it is at least as hard as the original programme.
4. **R proportional to cluster radius.** By (T), R must be about 0.45 × seam length. That is comparable to the cluster size, so each merge is essentially global and the recursion gains nothing.

## 6. Proof-route analysis (transfer matrix / compactness)

Suppose degrees near the seam are at most Δ and the seam has bounded local geometry. A cross-section of the band of width w then has at most 4^{O(wΔ)} colour states, and finitely many local environment types exist. The seam becomes a 1-D word over a finite alphabet. "Constant R works" means that for every word and every pair of boundary colourings, a domain wall of width 2R exists. By compactness (König), it is enough to check every finite word. **The constant-word "all degree 6, flat" is one of those words, and (T) shows the check fails.** In transfer-matrix language, the transfer graph carries an additive cocycle, the height increment. A wall exists only between states of equal accumulated height, and the height difference is unbounded along the seam.

So a finite-check proof is possible only for a statement that includes the invariant. Concretely, one would need: (a) to classify the transfer graph's cocycles, i.e. show the height is the only obstruction; (b) a finite check that any bounded height mismatch can be resolved within width O(M), for every local environment of degree at most Δ; (c) a separate argument that the recursion keeps mismatch bounded. Unbounded degree breaks finiteness in (b). Item (c) is not a finite check at all, and that is where a global argument would have to come in. Proved here: sections 1–4. Everything in sections 5–6 is conjecture.

Relation to the distributed lower bound: this is the same mechanism. Lower bounds for LOCAL colouring of grids and planar graphs (Brandt et al. on 3-colouring grids; Aboulker–Bonamy–Bousquet–Esperet 2019 for planar 4-colouring; approximate) rest on winding/height-type invariants that local rules cannot change. Here the seam window is what is local. The cluster-level freedom does not help, because the input colourings may carry arbitrary tilt.

## 7. Literature (from memory, approximate)

- Kempe 1879; Heawood 1898: a triangulation is 3-colourable iff it is Eulerian.
- Fisk 1977, Geometric coloring theory: 4-colourings viewed as maps to the tetrahedron boundary; parity and degree results; Kempe equivalence for Eulerian triangulations.
- Meyniel 1978: 5-colourings of planar graphs are Kempe equivalent. Las Vergnas–Meyniel 1981. Mohar 2006: 4-colourings of 3-colourable planar graphs are Kempe equivalent. Bonamy–Bousquet–Feghali–Johnson 2019: Mohar's conjecture.
- Reconfiguration: Cereceda–van den Heuvel–Johnson on 3-colourings use winding/height and frozen colourings, the 1-D analogue of this obstruction.
- Baxter 1970 (honeycomb 3-edge-colourings); Kondev–Henley 1996 (2-component height, critical).
- Precolouring extension and locality: Thomassen's 5-list-colouring. Dvořák–Lidický–Mohar–Postle (5-list-colouring with distant precoloured vertices) and Postle–Thomas hyperbolicity are a locality theory that does hold for 5 colours. Dvořák–Král'–Thomas use winding numbers for triangle-free 3-colouring. At 4 colours on triangulations the height obstruction appears, much as winding does for 3-colourings of grids.
- Fowler 1998: uniquely 4-colourable planar graphs are stacked.
- Aboulker–Bonamy–Bousquet–Esperet 2019: Ω(n) LOCAL rounds for planar 4-colouring.
