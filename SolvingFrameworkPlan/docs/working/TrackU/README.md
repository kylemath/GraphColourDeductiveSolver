# Track U: a test of T1 (abstract R-cycle exclusion)

Studio, 8 Oct 2026, 11:45–13:15 local time. Nothing outside `TrackU/` was changed and nothing was committed.

Compute: at most 4 worker processes, all under `nice -n 10`. One brief overlap of 5 happened: a 30-second Python check ran during a 4-worker wave. Load from other users was 40–60 on 16 cores.

Labels:
- **[data]**: computation.
- **[data, 2 engines]**: confirmed by both the TrackT engine and an independent checker.

## 0. Verdict

**T1 is FALSE.** [data, 2 engines]

Counterexample: a simple, 3-connected, non-planar graph G with n = 22. It has one degree-5 vertex v with edges f₀ … f₄ in the given cyclic order; every other vertex is cubic. G carries a closed orbit of length 10 in matching form whose k(H) word is **1 2 1 2 1 2 1 2 1 2**:
- every state satisfies T1 (i) and (ii);
- k(M_{t−1} ∪ M_t) = 1 at even t and 2 at odd t, which is T1 (iii);
- the law holds at 10 of 10 steps.

File: `out/t1_n22_first.txt` (verification in `out/t1_n22_first_eval.jsonl`). Edges:

```
n=22  edges (id order): 0-7 0-2 0-1 0-19 0-14 1-3 2-4 2-10 3-17 3-13 4-6 4-5 21-16 16-19 5-17 5-14 6-13 6-9
      7-18 7-9 14-12 15-12 12-1 8-11 8-15 8-17 9-21 10-20 10-11 11-18 13-15 16-18 19-20 20-21
fv = (f0..f4) = edge ids 0,1,2,3,4   (i.e. v's neighbours 7,2,1,19,14 in this cyclic order)
M_0..M_9 (edge ids): [0,5,7,10,14,20,23,26,30,31,32] [3,6,8,12,15,16,19,22,24,27,29]
  [1,5,11,13,17,18,20,25,28,30,33] [4,7,9,10,12,14,19,22,24,29,32] [2,6,8,13,15,16,18,21,23,26,27]
  [0,5,7,11,12,17,20,25,29,30,32] [3,6,8,15,16,19,22,24,28,31,33] [1,5,10,13,14,18,20,23,26,27,30]
  [4,7,8,11,12,16,19,22,24,29,32] [2,6,9,13,15,17,18,21,25,28,33]
frames (index of M_t's v-edge): 0 3 1 4 2 0 3 1 4 2  (advances −2 per step)
```

### Verification

Two engines confirm the orbit:
1. **TrackT's `tt_lib`** (G5 + `run_from`, imported read-only). Starting from (M₉, M₀), the orbit closes after exactly 10 steps through the same matchings, with the same k(H) word.
2. **An independent networkx checker** (`tu_verify.py` `eng2`), written from the T1 statement alone. It checks:
   - each M_t is perfect;
   - E − M_t is connected;
   - E − M_t has v-loop pairing (f_{k−1}f_{k+1})(f_{k+2}f_{k−2});
   - M_{t+1} ⊆ E − M_t;
   - f_{k−2} ∈ M_{t+1};
   - the k(H) word, computed with networkx components.

### Other properties

- G has 48 perfect matchings, 14 of them DL-good, and this orbit is its only closed orbit.
- The counterexample survives exactly the 10 dihedral relabellings of the given order at v, and none of the other 110 orderings.
- G − v is non-planar, and no single edge deletion makes G planar.

### The family of violators

- The first violator found has n = 28 (`out/t1_first.txt`).
- A law-preserving random walk from it (mode W) kept a T1-violating orbit at every accepted step: 158,160 accepted graphs. A sample has 280 distinct WL classes out of 1,054, all non-planar.
- 52 sampled graphs (45 WL classes) were verified with both engines: all are T1 violations, L = 10 (`out/coll_t1_*`).
- Greedy n → n−2 reductions keep violations at n = 26 (146 found), 24 (85) and **22 (31, all one isomorphism class)**.
- 261,093 reductions to n = 20 give no violator. So **n = 22 is the smallest violator found**; it is not proved minimal.

### What this means for NRC (TrackT §5)

- On the sphere with the planar labelling, T1 is exactly NRC′. Off the plane it fails.
- So **the chain-parity law plus the matching dynamics does not exclude R-cycles**. NRC-M needs a second planar input beyond the law (Lemma 5): Hamiltonicity at alternate states, the law, and figure-eight connectivity are all realisable together in non-planar graphs.
- The natural candidate for that input is still the bipartite interlace graph, i.e. planarity of the chord diagram at the rigid states, as TrackT §5 anticipated.
- **Caveat: no violator was found to be the Tait dual of a simplicial surface triangulation.** An embedding search (orientable, then non-orientable, by simulated annealing) on the n = 28 violator got its defect count no lower than 18 (`tu_embed*.py`). So there is no surface-level R-cycle here, and it was not possible to check a violator with the TrackS/TrackJ colouring engines, because those need a primal triangulation.

## 1. Engine

`tu_eng.c` is new. It works on the abstract graph in matching form (TrackS S2–S4) and differs from TrackT's `tt_abstract.py` in one important way: it enumerates **all** perfect matchings, not only the Hamiltonian states.

- A matching M is **DL-good** if E − M is a connected figure-eight whose loops are X (through f_{k−1}, f_{k+1}, an even number of inner vertices) and Y (through f_{k+2}, f_{k−2}, odd).
- The orbit map is M ↦ succ(M), the perfect matching of E − M that contains f_{k−2}. It is injective: 𝔇 has degree ≤ 2.
- The state is (pred(M), M) and k(H) = k(pred ∪ M).
- **Law:** k(H) changes parity at each step between states whose F12 is also connected.
- **T1 violation:** a closed orbit with word 1,2,1,2,….

Each graph takes about 0.05–1 ms (n = 16–40), compared with roughly 10 ms per graph for TrackT's Python engine.

### Cross-checks

- **C30#0 holes 0 and 16:** one 20-cycle with word 3 2 3 2 … and the law at 20/20 steps. It matches TrackS §2.1. Of the 125 perfect matchings, 40 are DL-good.
- **RP²/Klein Q-cycle holes:** TrackS's Tait words are reproduced:
  - `rp2_s203_w664_t327` h13: 3 2 3 2 3 2 2 1 …;
  - `klein_s204_w374_t916` h0: 2 2 1 3 1 2 2 3 2 3 ×2;
  - the other three RP² holes.

  All violate the law (4 or 8 violations).
- **Discrepancy, not resolved.** At `rp2_s203_w501_t418` h2 the matching-form engine finds **two** closed orbits. One is **law-respecting**, with word 4 5 4 5 2 3 2 3 2 3 2 5 4 5 4 3 2 3 2 3, confirmed by both engines in matching form. TrackS's colouring engine (`ts_tait_holes.py`) lists only one all-DL π-cycle at this hole, with word 3 3 4 3 4 2 3 2 3 2 3 2 4 3 4 3 3 2 3 2. Its first half matches my second orbit; its second half is shifted by one state.

  Off the sphere the chain-count DL condition is not the same as the Tait figure-eight condition, so the converse of Corollary S4 (an 𝔇-cycle gives a π-cycle) apparently fails there. Treat the RP² law orbit as a matching-form object only.

## 2. Results

### (1) Law-respecting closed orbits off the plane: yes, at every level found

| source | law closed orbits | k(H) levels |
|---|---|---|
| T1 violators (n = 22–28, abstract, non-planar) | many (above) | {1, 2} |
| RP² hole `rp2_s203_w501_t418` h2 (matching form) | 1 | {2, 3, 4, 5} |
| law-preserving walks/anneals from RP²/Klein seeds (n = 50, 54, abstract, non-planar) | 90 sampled, 2 engines (`out/coll_seeded_*`) | {2, 3} (81), {2, 3, 4, 5} (9) |
| C30#0 neighbourhood (n = 26) | only C30#0 itself | {2, 3} |

- TrackT's statement that no law-respecting closed orbit of any kind exists off the plane was an artefact of its search, which only followed orbits through Hamiltonian states.
- Even so, law cycles are **very rare** in unbiased searches:
  - **random graphs** (`out/rand_n*.jsonl`): 3.76M graphs at n = 22, 26, 30, 34 gave 11,193 closed 5-cycles and 118 closed 10-cycles, and **0 law-respecting** ones. Almost all of these orbits (all but 3) pass through a Hamiltonian state;
  - **SA from random starts:** 68.5M evaluations (modes A and B, n = 16–40, plus 49 × 30 s short runs) gave **0 law cycles**. The one exception is the 30 s n = 28 run that produced the first violator after 51,674 evaluations; its log was overwritten during a rerun.
  - So the landscape is needle-like. SA climbs to 10-cycles with exactly 2 violations (word 2121212112 and similar) and stalls there.

### (2) Pushing toward k(H) = 1

- **Seeds C30#0, Klein, RP² w664/w501 (mode B, 20 min each):**
  - every law cycle reached stays at levels {2, 3} or {2, 3, 4, 5}, and **none contains a Hamiltonian state**;
  - the best mode-B scores came from abandoning the law: 10-cycles with v = 2, e.g. 2112121212.
- **Law-preserving walk from C30#0 (mode W, 12 min):**
  - 247,897 accepted moves, but all of them are stub relabellings: 1 WL class in a sample of 1,240;
  - **C30#0 is an isolated point**: every structural 1–3-swap destroys its law cycle.
- **The same walk from a T1 violator** moves freely: 280 classes in its sample, every one still a T1 violation.

So the T1 violators sit in their own family. The search did not connect them to the sphere/C30 law cycles (level {2, 3}) or to the RP²/Klein ones.

### (3) Best T1 violation

A full violation: n = 22, L = 10, word 1212121212, law 10/10. All checked violators have L = 10, all are non-planar, and none is in a known polyhedral embedding.

## 3. Files

| file | content |
|---|---|
| `tu_eng.c` (`tu_eng`, `tu_eng2`, `tu_eng3` binaries) | C engine. `eval FILE` lists all closed orbits; `anneal SEED N SECS MODE SIMPLE [SEEDFILE idx]` with MODE A (law cycles), B (toward 1212), R (random census), W (law-preserving walk). Binaries 2 and 3 are the same source with modes R and W added |
| `tu_seeds.py` | exports Tait duals of surface holes (TrackT `tait_dual`) to engine graph lines; `out/seed_c30.txt`, `out/seed_surf.txt` |
| `tu_verify.py` | two-engine check: TrackT `tt_lib` + independent networkx checker of T1 (i)–(iii) and the law |
| `tu_collect.py` | dedupe and verify law cycles from logs; `out/coll_*_{graphs,eval,verify,summary}` |
| `tu_planarcheck.py` | planarity, connectivity, rotation-at-v agreement, WL class |
| `tu_shrink.py` | n → n−2 reductions preserving a T1 violation; `out/t1_shrunk.txt` (n = 22), `out/t1_shrunk2.txt` (n = 20: none) |
| `tu_embed.py`, `tu_embed_sa.py` | search for a polyhedral (simplicial-dual) embedding: not found |
| `out/t1_first*.txt/jsonl`, `out/t1_n22_*` | the n = 28 and n = 22 counterexamples with their evaluations |
| `out/ann*`, `out/seed*`, `out/shortA*`, `out/rand*`, `out/walk*` | search logs (the walk log from the n = 28 violator is subsampled 1/150) |
| `run_u.sh`, `run_u2.sh` | launch scripts |
