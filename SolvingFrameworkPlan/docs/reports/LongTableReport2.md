# Long Table report 2: mass table consumed, predeclared sets evaluated

4 October 2026. To the Math solutions and scale-up team and the Proof Navigator group. This reports facts only; the navigator assigns statuses. Files are in `backgroundMaterial/planemap-structural/longtable/`, with hashes in its own `SHA256SUMS`.

## 1. Consumption and independent replay

- **Input.** `mass-macro-results.json` matches `mass-macro-SHA256SUMS`, which verifies in full. The adversary checks that:
  - the whole-file hash matches the manifest;
  - each graph's ASCII matches the corpus and its newline-free `ascii_sha256`;
  - no root has an empty colouring family;
  - each graph's roots equal D(T).
- **Replay.** `verify_corpus_witnesses.py` recomputes, with our separate implementation, all 12 roots of the new fixture (order 17, graph 0) and every published failing root. All 20 rows match exactly: orbits, non-target count, one-swap stuck, two-swap stuck, outcome and vertex order.
  - The first witness reproduces: order 17, graph 0, root 4, rank (1,143), R = 1878, with the identical colouring.
  - There are 21 stuck orbits in total, as reported.
  - This is a third implementation agreeing with the sweep and its independent checker. It is still not an independent enumeration of the passing roots outside order 17, graph 0.

## 2. Predeclared sets against the mass table

S0 and S1± were declared before the table existed, so they are evaluated on the whole corpus. The tie-break is the smallest label.

| Rule | Graphs where the set contains a failing root | Graphs where the tie-break picks a failing root | All of D(T) fail | First tie-break failure |
|---|---:|---:|---:|---|
| S0 = D(T) | 6 | 0 | 0 | none |
| S1+ (most degree-five neighbours) | 4 | 3 | 0 | order 17, graph 3, root 3 |
| S1− (fewest degree-five neighbours) | 2 | 2 | 0 | order 17, graph 0, root 4 |
| anchor rule (label-based regression) | 5 | 2 | 0 | order 17, graph 0, root 6 |

- **Every-member guarantee.** It fails for S0, S1+ and S1−. Each set contains a failing root in at least one tested graph.
- **The existential claim** survives the corpus: no graph has all of its degree-five roots failing.
- **S0's tie-break never picking a failing root is a fact about the Plantri labelling, not the graphs.** Failing roots form whole automorphism orbits (§3). In each of the six failing graphs, relabelling one failing root as 0 would make the same tie-break pick it. This result should not be read as a selector.

## 3. Automorphism diagnostic (optional, from rotations only)

`automorphisms.py` computes each graph's map automorphisms, orientation-reversing ones included, by extending from a single dart. It never enumerates colourings.

**In all 118 graphs, the failing-root set is a union of automorphism orbits,** as `InvarianceNote.md` predicts. 26 graphs have a trivial automorphism group.

| Graph | Automorphisms | Failing orbits |
|---|---:|---|
| order 17, graph 0 | 4 | {4, 6}, {9, 14} |
| order 17, graph 3 | 20 | {3, 13}, the whole minority orbit; the other ten roots form one orbit |
| order 20, graph 7 | 4 | {7, 11} |
| order 20, graph 60 | 2 | {3} |
| order 20, graph 62 | 2 | {15} |
| order 20, graph 63 | 2 | {3, 15} |

## 4. Discovery on orders 12–18: no rule frozen, holdout untouched

There are 279 roots in this range, of which 6 fail, in 3 orbit types: order 17, graph 0 {4, 6} and {9, 14}, and order 17, graph 3 {3, 13}.
- **The first ring does not separate them.** Every failing pattern of neighbour degrees also occurs at passing roots. The uniform ring (5,5,5,5,5) passes 14 times and fails twice.
- **No simple rule survives discovery.** We screened twelve equivariant arg-max/arg-min rules over local degree statistics:
  - degree-five neighbours;
  - degree-five vertices at distance 2;
  - their sum;
  - second-ring size;
  - ring degree sum;
  - charge in the 2-ball.

  Every one contains a failing root in at least one of the two failing discovery graphs. Nothing qualified to be frozen, so **orders 19–20 remain unspent as a holdout.**
- **A descriptive observation, not a rule.** All three failing orbit types have an unusually uniform second ring:
  - {4, 6}: all eight vertices at distance 2 have degree five;
  - {3, 13}: a degree-five hub whose neighbours are all degree five, ringed by five degree-six vertices;
  - {9, 14}: five of seven vertices at distance 2 have degree five.

  We will not turn this into a rule fitted to two graphs.

**Our suggestion for next steps.** Local degree statistics look like the wrong vocabulary for MMD-select. The math team's planned structural reading of the first failure is the better next input. We'd like to contribute a paired comparison inside order 17, graph 0: the stuck colouring at root 4 against the passing behaviour at root 8, which has the same orbit count (54) and the same non-target count (38). That would show which component interaction the two-swap macro cannot reach. We will start only if the math team wants it, since the structural reading is theirs.

## 5. Edge-insertion statement review

See [EdgeInsertionReview.md](EdgeInsertionReview.md). In brief:
- **Q1.** The update is a successor transposition of a.symm and b.symm in the face permutation, so chord insertion splits one orbit and bridge insertion merges two, with repeated vertices harmless. Non-adjacency also rules out digon faces.
- **Q2.** Bridge availability is immediate after support transport. Chord availability is the real lemma. We suggest checking whether the proved combinatorial Jordan separation, or Gate A's `alternating_walks_intersect`, already rules out both diagonals.
- **Q3.** Coefficient normalisation is sound. An optional alternative characterises Fills as s − e + f = 2c, after which both cases are counting. That needs the face-boundary kernel to be exactly the per-component constants.

## Files

| File | Contents |
|---|---|
| `adversary.py` | Adversary tool, adapted to the published layout |
| `adversary-mass.json` | Mass-table results, whole corpus |
| `adversary-mass-max18.json` | Mass-table results, discovery orders only |
| `adversary-sigma-beta.json` | (σ, β) results (unchanged) |
| `verify_corpus_witnesses.py`, `verify-corpus-witnesses.json` | Independent replay of the failing roots and the order-17 graph-0 fixture |
| `automorphisms.py`, `automorphisms.json` | Automorphism diagnostic |

— The Long Table authors
