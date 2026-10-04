# WP7c results: injective charging to locked patterns is refuted

> **Erratum (after the math team's WP7d reply).** "One of them always vertex 13" holds only at root 3. Vertex 13 is the deleted root at root 13. At root 3 the five colliding pairs differ at {13, 16}, {12, 13}, {6, 13}, {7, 13} and {13, 14}. At root 13 they differ at {3, 10}, {3, 9}, {3, 4}, {0, 3} and {2, 3}. In both cases the pair differs at the **opposite hub** (13 or 3) and one of its neighbours. These two-vertex differences are **after the best colour renaming**. In the raw stored colourings, two root-13 pairs differ at six vertices: the complementary component of the same colour pair, which is the same toggle written the other way (see WP7d-results.md). Also, the ten warned colourings per root are the five strict two-swap traps plus five states that have a decreasing two-swap macro, but only into a trap. They are not ten traps. The mechanism is the subject of WP7d.

Long Table, 4 October 2026. This follows [WP7c-declaration.md](WP7c-declaration.md), committed before the test (`0430026`). The run is `wp7c_test.py`, which writes `wp7c-results.json`. Its input is the math team's warning traces, hash-checked, with no colourings regenerated. These are facts, not status claims.

## Result

- **C7c is refuted.** In 10 of the 39 runs with warnings, two distinct warned colourings share the same pattern Pat. All 10 are at order 17, graph 3: five runs at root 3 and five at root 13.
- **Every other root charges injectively.** Order 17, graph 0 roots 4, 6, 9 and 14; order 20, graph 7 roots 7 and 11; order 20, graph 60 root 3; order 20, graph 62 root 15; and order 20, graph 63 roots 3 and 15 each have as many patterns as warned colourings.

| Root | Distinct warned colourings | Distinct patterns | Most colourings sharing one pattern |
|---|---:|---:|---:|
| Order 17, graph 3, root 3 | 10 | 5 | 2 |
| Order 17, graph 3, root 13 | 10 | 5 | 2 |
| Each of the other 10 roots | 1 or 2 | equal | 1 |

## What the collisions are

In each colliding pair, the two warned colourings:
- differ at exactly **two vertices**, one of them always vertex 13;
- have R values of 1842 and 1850;
- are *not* related by any of the 10 automorphisms fixing root 3.

They are one small interior swap apart. Both are dead ends of the same basin, with the same boundary chain connectivity, the same within-boundary connectivity, and the same exterior flags.

So at a short-circuit trap, the dead-end basin contains *interior variants* that no boundary-chain pattern can distinguish. Whatever a warning charges must see some interior structure, or else carry an explicit multiplicity bound.

## What this does and does not settle

- **Settled:** injective charging to Pat, as declared, fails on the corpus.
- **Not settled:** a bounded-multiplicity charging, for example "at most k warnings per pattern". The observed multiplicity here is 2. Following the math team's caution, we do not infer a bound from that number; it would need its own statement and a structural reason. For example, interior variants of a locked pattern might be limited to the swaps of components that miss B and are adjacent to the hub. That is a hypothesis, not a finding.
- **Not settled:** the warning bound itself. It remains the open complexity obligation for breadcrumb descent.

## Where WP7 now stands

| Item | Outcome |
|---|---|
| 7.1, 7.2, 7.4 (exact lemmas) | The math team has accepted them for Lean; they are not yet compiled proofs. The Proof Navigator records them as exploring. |
| 7.3 (mass dominance) | Killed by the short-circuit traps |
| H-A and H-B (dynamic signs) | Refuted |
| H-C | Survives but is not distinctive |
| C7c (injective pattern charging) | Refuted by short-circuit interior variants |

Every negative result so far traces back to order 17, graph 3. That graph has 20 automorphisms. Root 3 is a degree-five hub whose neighbours all have degree five, ringed by degree-six vertices, with 5 traps per root. It is the natural next object for a structural description, and the obvious fixture against which to state any bounded-multiplicity charging.
