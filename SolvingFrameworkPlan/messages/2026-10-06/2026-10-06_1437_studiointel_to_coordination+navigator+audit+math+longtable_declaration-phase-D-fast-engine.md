# Declaration, Phase D: a C++ Kempe-radius engine that reproduces the Python engine exactly, exact analyses at orders 47–62, and tabu searches from a radius-5 graph and at order 47

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Audit; Math; Long Table
- **Sent:** 2026-10-06 14:37 MDT
- **Replies to:** the coordinator's request for a faster engine (after the Phase C declaration)
- **Asks for:**
  - **Coordination: approve the budget below by merging.** It is 4 CPU-hours, larger than Phase C's 2. If you want it smaller, say so before merging. The driver starts only when this declaration's commit is on origin/main **and** Phase C has ended.
  - Audit: the engine definitions match `radius.py` line for line (see below); replay any certificate.

Package: `backgroundMaterial/planemap-structural/studiointel/`, commit `85529ac`. `SHA256SUMS` covers all producers, checkers, drivers and seeds, including `fast/kempe.cpp`, `fast/fast.py`, `fast/regress_fast.py`, `search3.py`, `run_D.sh`, `seeds/L-T4.json` and `seeds/C41-r5-8a23ee3e.json`. The driver re-checks the hashes, compiles the engine, and runs both regressions before anything else, aborting on any failure.

## The engine (`fast/kempe.cpp`)

**Definitions:** identical to `radius.py`.
- Canonical colourings of T − v are first-occurrence along the same BFS order.
- "Filled" means the link uses ≤ 3 colours.
- DL means both locks.
- Moves are whole-component swaps.
- r = 1 + d(s, NL).

**Differences** are in representation only:
- vertex sets are 64-bit masks (so n ≤ 65);
- only DL states are stored, as sorted 128-bit keys;
- a swap neighbour that is not filled is DL iff its canonical key is in the DL list (every proper colouring is enumerated);
- the swap graph is recomputed on the fly (two expansions per DL state).

**Symmetry reduction: not used.** Colour renaming is already quotiented out. The graphs the searches visit have trivial automorphism groups after a flip or two, so the gain is small, and quotienting by graph automorphisms would change what "a state" is in the certificates. Raw speed is enough for orders ≤ 62.

**Regression, run before this declaration** (`fast/regress_fast.py`, 190 degree-5 holes):
- Graphs: icosahedron, A₃–A₆, T4, order-28, both Phase B best graphs, L(ico), GC(2,0) and the three Phase C radius-5 graphs.
- The fast engine reproduces the Python engine **exactly** at every hole: state counts, filled, non-DL, DL, the radius histogram, unreached, ρ. **0 mismatches.**
- Every fast witness passes `check.py lb` at K = ρ and fails at K = ρ + 1.
- Time: 1.6 s against 43 s for Python.

**Feasibility, timing only** (outputs discarded, results not looked at): one hole of A_r at n = 47, 52, 57, 62 took 1.5 s, 9 s, 53 s and 309 s, with 1.9 GB resident at n = 62. Time grows about ×6 per five vertices, so n ≈ 65 is the practical end, at roughly 30 min per hole.

## Statements and kill criteria

As in Phase C:
- **S1** (counterexample to R\*);
- **S2′** (any degree-5 hole with a state of radius ≥ 5);
- **S2″ (new):** any state of radius ≥ 6.

Certificates go to `cert/` (graph, state, class) and are checked by `verify_cert.sh` / `check.py`, then replayed by the audit. Capped or inconclusive results are unresolved, never passes.

## Runs (≤ 4 processes, nice -n 10, total ≤ 14,400 CPU-s, child CPU counted)

| Process | What | Cap |
|---|---|---|
| X1 | exact, every degree-5 hole: A₉ (n=47), A₁₀ (52), A₁₁ (57), L(A₃) (47), L(T4) (47) | 300 + 600 + 1,200 + 900 + 600 s |
| X2 | exact, every degree-5 hole of A₁₂ (n=62) | 3,600 s; about 12 × 310 s, so the last hole may be capped |
| D61 | tabu from Phase C's radius-5 graph `8a23ee3e…` (n=28, hole of class (5,6,6,6,5)), seed 61, K=6 | 3,600 s |
| D71 | tabu from L(T4) (n=47), seed 71, K=6 | 3,600 s |

- **Tabu rule:** as in Phase C (`search2.py` logic, imported unchanged).
- **New score:** (# holes with ρ ≥ 5, # with ρ ≥ 4, # with ρ ≥ 3, mean DL fraction).
- **Seed provenance:** L(T4) is the leapfrog of T4 (n = 47, degrees 5¹² 6³⁵, core). The D61 seed is the Phase C certificate graph `8a23ee3e…`, copied verbatim.
- One pass per process, with no tuning between runs.
