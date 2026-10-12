# Track E: can a Barnette-type signed sum work on Kempe classes? (7 Oct 2026)

Question: OpenAIStructuralAnalogies.md §0.8 asks whether a Barnette-type argument can work for us. The bad (unfilled) states would cancel under a phase-flipping involution, and the class sum would factorise over Kempe cubes and be nonzero. The tests are C0, C2, C4 and C3′ from §0.9.

Engines: the project's `kempe_py.Space` (canonical states, chains, `filled`) and `escape.pi_of` (π, λ, winding). Everything else is own code in this directory. No OpenAI code was used. All runs used `nice -n 10`, at most 4 processes, single-threaded. Labels follow Track C: **data** = exhaustive computation as stated; **hand** = a short argument written here, not reviewed.

## Verdict

**The signed-sum route is dead as formulated. Its only surviving phase is a local function of the ring word.**

- **C0 (Barnette replication): passes.** It confirms the reading of the mechanism in §0.
- **C2 (per-chain phase): one natural phase passes on lock chains, and it is local.**
  - i^H (H = Heawood sum) flips on 100% of lock swaps, but on 0% of chain swaps that avoid the link.
  - Its parity is a fixed function of the ring colouring, so it is a local-type phase.
  - No phase of any kind can flip on both the lock involution and the swaps of any fixed-pair Kempe cube: there are odd cycles in 3640/3640 locked classes.
- **C4 (lock-chain involution): fails.**
  - About a third of unfilled states have no lock.
  - At about 44% of holes, even the locked states admit no involution built from lock swaps.
  - The rule "swap lock1 if it holds, else lock2" is not an involution on 19,505 states.
  - On canonical states the involution has fixed points.
- **C3′ (class sums, for i^H only): vacuous.** Every labelled class is closed under an odd colour renaming, so Σ_K i^H = 0 identically. This holds in the census, at all 66666 holes, and at the one AW hole and one BV hole tested.

## C0: Barnette's sum on Eulerian triangulations (data; `c0_barnette.py`, `c0_more.py`, `agg_c0.py`, `out/c0-summary.txt`)

**Graphs.** Eulerian triangulations with n = 6–16, found by random edge-flip walks.
- That is a sampler, so "all" is not certified.
- 103 distinct graphs: n = 6, 8, 9 (one each), 10 and 11 (two each), 12: 7, 13: 18, 14: 31, 15: 23, 16: 17. A few graphs at n = 13, 14 and 16 appear twice in the two files.
- Every black face was tried as t₀: 1,228 (T, t₀) records.

**Results.**
- J is an integer for all 3,608 pairs.
- Every directed cycle of D has δ-sum ±3 (0 exceptions).
- For every s with Q_s cyclic, Σ_r i^J = 0: 72 such pairs, 0 failures.
- Every forest s has at most one partner, so Z collapses to 3,536 tree terms.
- Each undirected-D group has exactly 2^c members, and its moments of order j < c vanish (0 failures).
- The moments of order j < c_min of the full Z vanish in every record. The moment of order j = c_min is nonzero in 741/759 records that have pairs.
  - The weights are random integers, not the spoke-circulation weights.
  - The zero cases I re-ran (n = 11, 14) with six other seeds were all nonzero, which fits an accidental degeneracy of the random weights.
- 469 records have no pair at all. Every one has a separating triangle (0 with none), which fits Barnette's 3-cut reduction.

The cancellation step was exercised on only 72 pairs, because small Eulerian triangulations rarely have cyclic Q_s with partners.

## C2: does a phase flip by a constant factor on single chain swaps? (data; `phase_lib.py`, `c2c4.py`, `agg_c2c4.py`, `out/c2c4-summary.txt`)

### Setup

**Census.** gentri, every degree-5 hole, one orientation.
- Orders 12, 14, 16–20: all graphs.
- Orders 21 and 22: the first 60 graphs in each file.
- Total: 237 graphs, 3,499 holes, 3,799 labelled Kempe classes.

**Labelled colourings.** States are canonical colourings × 24 renamings. Swaps are whole-component swaps with no renaming afterwards, so φ(c′)/φ(c) is well defined. The census contains 148.5M non-renaming swaps and 49.6M renaming swaps.

**Hand lemma 1 (only factor −1 can work).**
- Each swap type tested is closed under inversion: swapping the same chain again undoes it.
- So a constant factor ζ on a type must satisfy ζ² = 1.
- Therefore ω^H, ζ₅^rep, and "i^H by a factor i" cannot have a constant non-trivial factor. Only sign flips (−1)^f can.
- In the data, rep (the repeat or unique index) never changes on lock swaps. Its ζ₅ phase has factor 1 there.

### Candidates

Each candidate is a statistic f, tested as the sign (−1)^f:
- P = number of (+) Heawood faces of T − v. Since H = 2P − m, i^H is a constant times (−1)^P.
- Pr = the same count on the 5 ring faces.
- The colour counts n_a, and the link colour counts.
- Alon–Tarsi descents along a fixed orientation (AT1) and along a Kasteleyn orientation (KS), each for 12 colour orders.
  - The parity of the change is the same for every orientation: reversing an edge complements its indicator. So AT1 and KS give identical data.
- Cube coordinates io_pq.
- Component counts kc_pq.
- Theorem-W winding of the π-orbit, λ, the lock bits, and the Heawood vertex sums at the link vertices.

### Flip fractions (each count is "swaps where the sign flips / swaps of that type")

| swap type | swaps | i^H (P) | Pr | n_a | W | best AT/KS |
|---|---|---|---|---|---|---|
| chain avoids link | 46,338,384 | **0** | 0.39 | 0.13 | 0.17 | 0.80 |
| meets link in 1 vertex | 65,874,336 | 0.55 | 0.28 | 0.28 | 0.03 | 0.37 |
| meets link in 2 vertices | 25,753,056 | 0.68 | 0.83 | 0.19 | 0.10 | 0.57 |
| meets link in 3 / 4 vertices | 7,956,768 / 2,589,360 | **1 / 1** | 0.66 / 1 | <0.3 | <0.2 | ~0.4–0.6 |
| lock chains (both locks) | 8,290,656 | **1** | 0.73 | 0.17 | 0.09 | 0.53 |
| R1 involution swaps | 6,471,264 | **1** | 0.73 | 0.17 | 0.09 | 0.53 |
| whole-pair renamings | 49,624,560 | **1** | 1 | 0.24 | 0 | 0.49 |

The remaining candidates (io, kc, λ, lock bits, Heawood vertex sums) are 100% on no type except as shown in `out/c2c4-summary.txt`. λ and the Heawood vertex sums never change parity.

**Exhaustive linear test (F₂ affine hull).** Over all 55 statistics at once, is there an F₂-combination that flips on every swap of a type? Zero in the hull means no such combination exists. Zero is in the hull, so none exists:
- on chains that avoid the link, at 3,443 of 3,499 holes;
- on all chains, at 3,499 of 3,499 holes.

### i^H is local (data, with an explanation by hand)

- `probe_P.py`: the parity of the change in P under a swap is fixed by the link data of the chain. It is 0 for chains that avoid the link.
- `c2_local.py`, run on 573 holes at orders 12–19:
  - P mod 2 is a function of the labelled ring word (0 exceptions).
  - Explicitly, P(c) + P_fill(w) ≡ const(T, v) (mod 2), where P_fill counts the (+) faces of any proper chord-triangulation of the pentagonal hole. Any such fan gives the same parity (0 ambiguities, 0 holes where the sum is not constant).
- The same holds at all 66 census 66666 holes (orders 21–23) and at the AW/BV holes listed below.
- This is the Scheim/Heawood invariance of the sphere: filling the hole with chords gives a closed triangulation, on which the Heawood parity is constant.
- So i^H flips on lock swaps only because a lock swap changes the ring word from (α, μ, α, A, B) to (α, A, α, μ, B). This is exactly the "local type" phase that §0.8 and NightG66 rule out as carrying information.

### Most general test: any phase at all (data, with a lemma by hand)

**Hand lemma 2.** If an edge set E of swaps has an odd cycle inside a class, then no function φ at all satisfies φ(c′) = −φ(c) on every E-edge. By hand lemma 1, no constant factor other than −1 is possible either.

Labelled classes whose swap graph has an odd cycle:

| edge set | classes with an odd cycle |
|---|---|
| R1 only | 0 (it is a matching) |
| all lock swaps | 0 |
| one fixed-pair cube {a,b} | 0 (a hypercube) |
| all non-renaming chains | 3,786 / 3,799 |
| chains that avoid the link | 2,451 / 3,799 |
| **R1 ∪ cube{a,b}, for each of the 6 labelled pairs** | **3,640 / 3,640 locked classes** |
| lock ∪ cube{a,b} | 3,640 / 3,640 |
| R1 ∪ edge-cube(e₀) | 3,499 to 3,593 of 3,640, depending on the edge |

- **Fixed-pair cubes.** No phase flips on the lock involution and on every chain of a fixed-pair cube. This holds in every locked class of the census.
- **Edge-cubes.** For the ten sampled edges e₀ per hole, R1 ∪ edge-cube(e₀) is bipartite in 408 locked classes. `probe_e0.py` checked every edge e₀ at orders 12–18 and found 490 bipartite class–edge pairs out of 9,928. Those cases are not informative:
  - the cube chains are so few that the class splits into about 3.4 states per component of R1 ∪ cube, leaving a free sign on each component;
  - 57% of the unfilled states in those classes lie outside the involution's domain.

## C4: is "swap the lock chain" a fixed-point-free involution on unfilled states? (data; `c2c4.py`, `c4_lockgraph.py`, `out/c4_lockgraph-12-20.txt`)

Canonical unfilled states in the same 3,499 census holes: 405,405. By lock type:

| lock type | states |
|---|---|
| no lock | 135,769 (33%) |
| lock1 only | 96,914 |
| lock2 only | 96,914 |
| both locks (DL) | 75,808 |

1. **Coverage fails.** One third of unfilled states have no lock chain, so no lock swap can pair them. These unlocked states occur in every labelled class (581/581 at orders 12–19).
2. **The rule R1 fails.** R1 = "swap lock1 if it holds, else lock2" is not an involution at 19,505 states; R2 (lock2 first) fails at 19,443. The mechanism: swapping lock2 can create lock1 in the image.
3. **No lock-swap involution exists at many holes.**
   - The lock graph (edges = lock swaps) has degree ≤ 2, so its components are paths and cycles.
   - All cycles are even. But odd paths exist, for example a single-locked state, a DL state and a single-locked state in a row.
   - A perfect matching of lock swaps therefore fails at 692 of 1,574 holes at orders 12–20, and at 23 of 66 holes with link 66666.
4. **Fixed points on canonical states.** On canonical states, 161,547 of 269,636 R1 swaps swap the whole {μ,A}-subgraph, i.e. they are renamings and fix the canonical state. A phase on canonical states would have to vanish there. On labelled states this is avoided only by phases that are anti-invariant under renaming, which leads to C3′ below.

## C3′: class sums (data, with a lemma by hand; `c3_ih.py`, `adversarial.py`)

The only partial survivor of C2/C4 is φ = i^H. It flips on lock swaps but not on cubes, and it is local.

**Hand lemma 3.**
- m (the number of faces of T − v) is odd, so H is odd, and i^H ∘ τ = i^{−H} = −i^H for every odd renaming τ.
- If a labelled class K contains c and τc for some c, then τK = K, because renaming commutes with Kempe swaps. Hence Σ_K φ = −Σ_K φ = 0.

Data:
- Orders 12–19: all 581 labelled classes are closed under an odd renaming. Σ_K i^H = 0 and Σ_unfilled i^H = 0 in all of them, which is the trivial vanishing, not cancellation by the involution.
- The 66 census 66666 holes (orders 21–23): 80/80 classes closed under an odd renaming, 80/80 sums zero, and 0 lock classes with R1 ∪ cube{a,b} bipartite.
- AW/BV: see the next section.

So (a) "unfilled states cancel" holds only for the trivial reason, and (b) "Σ_K ≠ 0" fails everywhere.

## Adversarial graphs (data; `adversarial.py`, `out/adv-BV.jsonl`, `out/adv-AW.jsonl`, `out/adv-66666.jsonl`)

Each graph was checked at the hole given in its file; both holes have link (6,5,5,5,5).

| graph | canonical states | labelled classes | i^H parity a ring-word function? | odd-renaming-closed classes, Σ i^H = 0 | unfilled: none / L1 / L2 / DL | R1 not an involution | odd lock-paths | R1 ∪ cube{a,b} bipartite |
|---|---|---|---|---|---|---|---|---|
| BV `best-c-A7f3-w2-it412` | 18,560 | 3 | yes (0 exceptions) | 3/3 | 2,372 / 2,012 / 2,012 / 4,044 | 308 | 2,208 | 0 of 3 locked classes, all 6 pairs |
| AW `walk-best-A7f1-3-A34-w4-it575` | 23,306 | 1 | yes (0 exceptions) | 1/1 | 3,398 / 3,062 / 3,062 / 3,010 | 688 | 4,008 | 0 of 1, all 6 pairs |
| 66 census 66666 holes (orders 21–23) | | 80 | yes | 80/80 | 3,260 / 2,670 / 2,670 / 2,406 | 192 | 912 (at 23 holes) | 0 of 69 locked classes |

Not run: the other two AW hits (`A7f2-A34-w5-it918`, `A7f4-A34-w3-it967`) and the other 11 BV graphs. Each graph takes about 40–70 minutes in Python, and the outcome is fixed by hand lemmas 1–3 together with the census.

## Why the route is dead, in one paragraph

Barnette needs a single exact planar identity (the ±3 disk identity) that gives every relevant cycle the same phase jump. That one identity yields both the sign-reversing involution and the common leading phase of the cube factors.

Our only exact planar phase identity of this kind is Heawood/Scheim parity. On T − v it is constant up to a function of the ring word. So it flips on lock swaps for a purely local reason, and never on interior chains.

Without any candidate list, the swap graph rules out the cube half of the argument: lock involution ∪ fixed-pair cube has an odd cycle in every locked class of the census, so no phase exists at all. The involution half also fails on its own, because a third of unfilled states are unlocked and lock swaps often cannot be matched. Rescuing the route would need a different bad set, a different involution and a non-cube factorisation. None of these is suggested by the data.

## Files

- `c0_barnette.py`, `c0_more.py`, `agg_c0.py`: C0.
- `phase_lib.py`: the labelled space and statistics. `c2c4.py`, `agg_c2c4.py`: C2/C4 on the census.
- `probe_P.py`, `c2_local.py`: locality of i^H. `probe_e0.py`: edge-cubes. `c4_lockgraph.py`: lock-graph matchings.
- `c3_ih.py`: C3′ for i^H. `adversarial.py`: 66666 holes and AW/BV.
- Outputs are in `out/`.
