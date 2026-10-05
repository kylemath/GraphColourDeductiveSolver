# Long Table report 3: root 4 versus root 8, and a broadening search

4 October 2026. To the Math solutions and scale-up team and the Proof Navigator group. This runs in tandem with the math team's structural reading of the first failure. It reports facts and exploratory evidence only, with no status claims. Scripts and outputs are in `backgroundMaterial/planemap-structural/longtable/`: `compare_roots.py` → `compare-roots.json`, and `broaden_variants.py` → `broaden-discovery*.json`.

## 1. Paired comparison at order 17, graph 0

Roots 4 and 8 are at distance 2 in the graph. Each has 54 colouring orbits, 38 of them non-target. Root 4 fails and root 8 passes.

| | Root 4 (fails) | Root 8 (passes) |
|---|---|---|
| Neighbour degrees | 5, 6, 6, 5, 6 | 5, 6, 5, 5, 6 |
| One-swap stuck states | 5 | 3 |
| Two-swap stuck states | 1 | 0 |
| Greatest target distance (diagnostic only) | 4 | 3 |
| Escape from each one-swap stuck state (fewest swaps to a lower R / least possible climb of R on the way) | four states: 2 / +2; **the trap: 3 / +20** | 2 / +0, 2 / +0, 2 / +4 |

**Root 8's stuck states are shallow.** A two-swap escape exists, and R climbs at most 4 on the way. **Root 4's failure is a genuine basin:** leaving it takes three swaps and a climb of 20 in R, from 1878 up to 1898.

### Anatomy of the trap

The trap is root 4, state 25, the published first witness, with boundary B = [0, 3, 10, 11, 5]. Its features:

- **A fully locked boundary.** The repeated colour sits on vertices 0 and 11. Each of the three single-coloured vertices (3, 10, 5) is chained to another boundary vertex in *every* one of its three colour pairs. No single swap frees a colour. This is the configuration Kempe's 1879 argument mishandled.
- **The repeated colour is also chained.** Vertices 0 and 11 lie in one {0,2}-chain through vertex 5.
- **It is the deepest kind of state.** It is one of only 2 states at Kempe distance 4 at this root, out of 54.
- **It sits in a narrow corridor.** Only 4 distinct states are one swap away and 4 more are two swaps away. Their target distances are 3, 3, 4, 4 and 2, 2, 3, 3 respectively.
- **The escape** found by `compare_roots.py` runs as follows:
  1. swap a chain joining two boundary vertices, so the mass rises;
  2. swap a chain touching one boundary vertex;
  3. swap a second single-touch chain, landing at q = 101, against the trap's 143.

## 2. Broadening search: two predeclared rounds

Following the joint plan's discipline, the variant lists and the protocol were committed before each round ran (commits `e08e299` and `b9a3e93`):
- Every variant keeps the same class, moves, two-swap macro and stopping rule; only the rank changes.
- Each is a separately stated candidate, never a renaming of mass-macro descent.
- Screening uses orders 12–18 only. Only a variant with **zero** failing roots there would advance to orders 19–20.

The control, base, reproduced the published outcome at every discovery root (asserted in the run).

| Round | Variant | Rank | Failing roots (orders 12–18) | Graphs where every root fails |
|---|---|---|---:|---:|
| control | base | lex(p, q) | 6 | 0 |
| 1 | lock | lex(p, L, q), L = linked singleton pairs, 0–9 | **2** | 0 |
| 1 | lockq | lex(p, q + n²L) | **2** | 0 |
| 1 | lin | lex(p, Σ\|K∖B\|) | **2** | 0 |
| 1 | full | lex(p, Σ\|K\|²) | 8 | 0 |
| 1 | rep | lex(p, q over the pairs with the repeated colour) | 18 | **1** |
| 1 | Lonly | lex(p, L) | 18 | **1** |
| 2 | lockL | lex(p, L, lin) | **2** | 0 |
| 2 | linq | lex(p, lin, q) | **2** | 0 |
| 2 | Lallq | lex(p, Lall, q), with links counted at every boundary vertex | **2** | 0 |
| 2 | linksq | lex(p, number of boundary-linking chains, q) | **2** | 0 |
| 2 | linksl | lex(p, links, lin) | **2** | 0 |

- **Refuted on discovery:** rep and Lonly. Each has a graph where every root fails, so neither works as a formula even for the existential claim.
- **The rest reduce failures to one orbit.** Eight variants cut the failures from three orbits in two graphs to the single orbit {4, 6} of order 17, graph 0.
- **No variant reached zero,** so by the protocol nothing advanced. **Orders 19–20 have still not been used for any rule or formula.**

## 3. The wall, and what it means

**A rank always exists in principle.** Wherever every Kempe class contains a target, distance to a target in the two-swap move graph is a valid two-swap descent rank. That rank is the circular one. So these failures are limits on what a cheap formula can express, not facts about the colourings.

**Why every variant fails at the trap.** For all six variants checked, the trap is the *minimum* over its entire two-swap neighbourhood: base, lock, lin, Lallq, linksq and linksl. Every formula we tried rewards some form of tidiness: less exterior mass, more locking or fewer boundary links. The trap is the tidiest state in its corridor, and the only way out is to make the colouring messier first. Tweaking a monotone tidiness formula looks unlikely to get through; this is a structural barrier.

We do not propose a longer macro. The macro bound stays at two.

## 4. Suggested directions, for joint decision

1. **Selection plus a reduced-failure formula.** Under lin, lock and their relatives, the discovery failures shrink to one orbit in one graph, and that graph has 10 passing roots under lin. If the teams agree, we could write a new protocol that advances *reduced-failure* variants to the holdout and counts failing orbits rather than requiring zero. It would be declared and committed before any run, as before. We will not change the protocol on our own.
2. **Make the trap the object of study.** A fully locked boundary, a repeated colour chained through a singleton, Kempe distance 4 and a narrow corridor look like a recognisable local pattern. A lemma could say either that a selected root never admits such a trap, or that the recursion never produces one. That is the restricted-input certificate route in concrete form, and it may sit closer to the math team's structural reading than a new formula does.
3. **A non-monotone potential.** The escape's first move raises mass by joining a chain that links two boundary vertices. A rank that *credits* certain boundary-linking moves, rather than penalising all mass, would need its own stated definition and a proof. We list it only as a direction.

We will wait for the math team's structural reading of the first failure before choosing between directions 1 and 2, so that the two lines of work stay complementary.

— The Long Table authors
