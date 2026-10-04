# K6 — Kempe classes at a degree-\(5\) vertex (KC5)

**Group:** K6 (M-Kempe, Track 1). **Date:** 2 October 2026.
**Status:** finite check. KC5 on all planar triangulations is not proved. It would inductively prove the Four Colour Theorem, and it is stronger than that theorem.

## 1. Definitions

Implemented in `compute/kempe/a1720_k6_kc5.py`. Let \(G\) be a planar triangulation, \(\deg v=5\), and \(H=G-v\). Colourings of \(H\) are proper \(4\)-colourings, modulo \(S_4\). The quotient is exact: a global transposition is the product of all Kempe swaps of that pair, Kempe adjacency descends to the quotient, and \(|c(N(v))|\) is \(S_4\)-invariant (`a1720_k6_kc5.py` docstring).

**KC5 at \((G,v)\).** Every Kempe class of proper \(4\)-colourings of \(H\) that contains a colouring with \(|c(N(v))|=4\) also contains one with \(|c(N(v))|\le 3\).

A class that contains a \(4\)-colouring of the link and no colouring of the link with at most three colours is a **bad class**.

Named graphs are accepted only after `check_named` in `compute/kempe/a1720_k6_named.py` (order, size, planarity, \(m=3n-6\)).

## 2. Statement

For every triangulation on \(n\le 11\) vertices and every vertex of degree \(5\), KC5 holds. The same sentence was checked on the icosahedron and on the degree-\(5\) vertices of the Errera graph.

If KC5 holds for every planar triangulation and every degree-\(5\) vertex, then with the degree-\(\le 4\) inductive steps it yields the Four Colour Theorem: delete \(v\), \(4\)-colour \(H\), and Kempe-change inside the class until \(N(v)\) misses a colour. The universal sentence is stronger than the Four Colour Theorem, because \(4\)-colourability of \(G\) does not assert this property of Kempe classes of \(H\).

## 3. Evidence

```
.venv/bin/python compute/kempe/a1720_k6_kc5.py 4 5 6 7 8 9 10 11
.venv/bin/python compute/kempe/a1720_k6_named.py
```

The cache script’s default range is \(4,\ldots,11\), and it writes `K6_cache_n4_11.json`. The named script writes `K6_named.json`.

Cache, \(n=11\): \(1249\) triangulations, \(2747\) pairs \((G,v)\), \(2785\) classes, `n_bad_classes` \(=0\), \(0.69\,\mathrm{s}\). Every order \(n\le 11\) has `n_bad_classes` \(=0\). (Orders \(4\) and \(5\) have no degree-\(5\) vertex.) Some classes need more than one swap: at \(n=11\), `n_pairs_needing_ge2_swaps` \(=1793\) and `max_kempe_distance_to_fix` \(=2\).

Icosahedron: \(n=12\), \(m=30\), all degrees \(5\), structural check passed. All \(12\) vertices: \(1\) class, \(0\) bad classes, distance to a \(3\)-coloured link at most \(1\). Elapsed \(0.03\,\mathrm{s}\).

Errera: \(n=17\), \(m=45\), twelve degree-\(5\) vertices and five degree-\(6\) vertices, structural check passed. All \(12\) degree-\(5\) vertices: \(0\) bad classes. Maximum Kempe distance to a fix is \(3\) (vertices \(0\) and \(4\)). Elapsed \(0.14\,\mathrm{s}\).

Kittell: the stored adjacency has \(n=23\), \(m=65\), and `networkx` reports it non-planar. A triangulation on \(23\) vertices has \(63\) edges. `ok` is false, so KC5 was not run. The construction failed.

Cross-check of the quotient against `kempe_ops.py` on every degree-\(5\) vertex of every triangulation \(n=7,8,9\): \(139\) pairs, bad-class count \(0\) on both sides, assertions passed.

**Tilley.** James A. Tilley, arXiv:1809.02807 (2018; the arXiv comment says the article was retitled “Kempe-locking configurations”), reports that every Kempe-locked triangulation in his search contains a Birkhoff diamond and conjectures that a Birkhoff diamond is necessary for Kempe-locking (https://arxiv.org/abs/1809.02807).

Errera (1921) is a counterexample to Kempe’s two-swap procedure at a degree-\(5\) vertex. Heawood (1890) had already shown that procedure is not a proof. On this Errera graph the procedure’s conclusion, KC5, still holds at every degree-\(5\) vertex, including vertices whose shortest fixing sequence has length \(3\).

## 4. Result

Computed. KC5 holds with \(0\) bad classes on every degree-\(5\) vertex of every triangulation \(n\le 11\), on every vertex of the icosahedron, and on every degree-\(5\) vertex of the Errera graph. Kittell was not verified.

## 5. Kill criterion

One written bad class. **Not met** on the graphs that were checked. The failed Kittell encoding is not a counterexample.

## 6. Not proved

A finite check is not a theorem. KC5 for all planar triangulations is open. If it were proved, the degree-\(\le 4\) steps would give an inductive proof of the Four Colour Theorem, and the Kempe-class claim is stronger than \(4\)-colourability. Errera kills Kempe’s two-swap procedure, not KC5.

## 7. Feasibility

A proof of universal KC5: **Low**. Re-running KC5 on a correct \(23\)-vertex Kittell triangulation, once the edge list matches \(m=63\) and planarity: **Medium-High**.

## 8. Next steps

1. Replace the Kittell adjacency with a list that passes `check_named` (\(n=23\), \(m=63\), planar, triangulation) and run `run_named`. Until that check passes, Kittell is untouched.
2. Keep Errera as a witness against the two-swap procedure and as a non-witness against KC5.
3. Do not promote the \(n\le 11\) count, the icosahedron, or Errera to a theorem.
