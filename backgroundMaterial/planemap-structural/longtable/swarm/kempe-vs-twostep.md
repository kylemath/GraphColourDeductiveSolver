# Kempe preparation and the two-step slide

Certificate for the four locked mass-stuck orbits. Colourings are the canonical tuples of `mass_core.RootState`: colours in increasing vertex order, with the vacant root omitted, then renamed by first occurrence (`mass_core.canon`). An orbit id is the pair (root, index in `RootState.C`). The same index at two roots is two orbits. On two occasions below, two different orbits even produce the same list of numbers; the root is part of the name.

A `p = 1` orbit **descends** when `RootState.descent(i, 2)` is `None`. It is **mass-stuck** when that call returns a witness. Every descending landing in this note in fact satisfies the stronger `descent(i, 1) is None`. Throughout, `p = 1`, so the landing still uses four colours on its own link. The integer rank is `R = (6n^2+1)p + q`. A landing can descend relative to its own rank while having a larger `R` than the trap.

Graphs, both taken from `mass-macro-results.json` and not recoloured beyond the roots named below:

| Order | Graph | sha256 | Stuck orbit | Passing roots used as landings |
| --- | --- | --- | --- | --- |
| 17 | 0 | `1203efa037ee84da877d10d6f94b4d81f4224dab98ffb995de0abb125fb2b3c5` | root 4 state 25; root 6 state 27 | 0, 1, 2, 11, 12, 16 |
| 20 | 7 | `eaf8271c8e7283188162aba8a7fa4f4b87e360757c41c2059abbff9c9272bacc` | root 7 state 180; root 11 state 18 | 0, 4, 8, 9, 12, 13, 15, 19 |

Each of these four roots has exactly one mass-stuck orbit, and that orbit is locked: the link is a 5-cycle using four colours, the repeated colour sits on both degree-five neighbours, and the other three link vertices are singletons. Orders 32 and 42 were not coloured.

## Verdicts

| Claim | Verdict | Where |
| --- | --- | --- |
| Kempe preparation equals the two-step | **KILL** | Disjoint landing sets on all four orbits: `17:0 r4 s25`, `17:0 r6 s27`, `20:7 r7 s180`, `20:7 r11 s18` |
| One Kempe swap always prepares a slide onto a descending orbit | **not KILL** | All eight prepared slides descend at a passing root. The kill condition (a prepared slide landing on a mass-stuck orbit) does not fire |
| A precise relation between the two routes | **OPEN** | Long-arc chain correspondence below. It pairs distinct orbits; it does not restore the killed equality |

The kill of the equality is forced by the instruction for this check: the landing sets are disjoint on each of the four. The long-arc correspondence is a separate statement. It names how those distinct colourings sit on the locked colouring. The short-arc singleton stays outside that statement.

## How properness was checked

A colouring of `T` minus a vertex `v` was accepted only when its domain was exactly the remaining vertices and every edge with both ends outside `v` joined two different colours. That test was run on the locked colouring, on each first slide, on each second slide, on each Kempe swap, and on each prepared slide. Separately:

- each swapped component was rebuilt as a maximal connected bichromatic component of `T` minus the root, and its canonical image matched the successor stored by `RootState`;
- the slide of that explicit swap and the slide of the canonical representative have the same canonical landing;
- each return slide reproduces the source canonical tuple;
- every degree-five landing occurs in the enumerated set at its root.

No monochrome edge and no missing orbit appeared.

## The link

Up to rotation and reflection the locked link is read as follows. The cycle printed in the table is the rotation order, which need not start at a degree-five vertex. The long arc and the short arc are the two paths joining the degree-five vertices.

$$
u^{5}_{\alpha},\; p^{6}_{\beta},\; q^{6}_{\gamma},\; v^{5}_{\alpha},\; w^{d}_{\delta}.
$$

The vertices `u` and `v` are the two degree-five neighbours, both coloured with the repeated colour `α`, at cyclic distance 2. The long arc is the degree-six pair `p, q`. The short arc is the single vertex `w`. On the order-17 traps `w` has degree 6. On the order-20 traps `w` has degree 7.

| Orbit | Cyclic link `(vertex, degree, colour)` | `α` | Long arc | Short arc |
| --- | --- | --- | --- | --- |
| `17:0 r4 s25` | `(0,5,0), (3,6,3), (10,6,1), (11,5,0), (5,6,2)` | 0 on `{0,11}` | `3` colour 3, `10` colour 1 | `5` colour 2, degree 6 |
| `17:0 r6 s27` | `(1,5,1), (5,6,2), (12,5,1), (13,6,0), (7,6,3)` | 1 on `{1,12}` | `13` colour 0, `7` colour 3 | `5` colour 2, degree 6 |
| `20:7 r7 s180` | `(1,6,1), (6,6,2), (15,5,3), (16,7,0), (8,5,3)` | 3 on `{15,8}` | `1` colour 1, `6` colour 2 | `16` colour 0, degree 7 |
| `20:7 r11 s18` | `(4,5,2), (10,6,0), (17,6,1), (12,5,2), (5,7,3)` | 2 on `{4,12}` | `10` colour 0, `17` colour 1 | `5` colour 3, degree 7 |

Source ranks: both order-17 traps have `q = 143`, `R = 1878`. Both order-20 traps have `q = 164`, `R = 2565`.

Source tuples, in the vertex order that skips the root:

- `17:0 r4 s25`, order `0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16`: `(0,1,2,3,2,0,3,1,0,1,0,3,1,2,3,2)`
- `17:0 r6 s27`, order `0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16`: `(0,1,2,3,1,2,3,0,2,0,3,1,0,1,3,2)`
- `20:7 r7 s180`, order `0,1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19`: `(0,1,2,3,1,3,2,3,1,2,0,2,0,1,3,0,1,3,2)`
- `20:7 r11 s18`, order `0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19`: `(0,1,2,1,2,3,0,3,0,3,0,2,1,2,1,2,1,0,3)`

## A. Two-step slides

Each of the three singletons admits a first slide. On the intermediate link the original root is again a degree-five singleton, and the slide back to it restores the stuck source. Those returns are mass-stuck. The forward degree-five landings all descend, all in one mass swap, all at passing roots.

`17:0 r4 s25`

| Intermediate | Degree | Side | Forward degree-five landings |
| --- | --- | --- | --- |
| 3, colour 3 | 6 | long | root 2, state 43, `q=143`, `R=1878`, descends, passing |
| 10, colour 1 | 6 | long | root 16, state 20, `q=143`, `R=1878`, descends, passing |
| 5, colour 2 | 6 | short | root 12, state 43, `q=155`, `R=1890`, descends, passing; root 1, state 8, `q=155`, `R=1890`, descends, passing |

Returns from 3, 10, and 5 all land on `r4 s25`.

Forward tuples:

- root 2 state 43: `(0,1,2,3,2,0,3,1,0,1,0,3,1,2,3,2)`
- root 16 state 20: `(0,1,2,3,1,2,0,3,1,0,2,0,3,1,2,3)`
- root 12 state 43: `(0,1,2,3,2,3,0,3,1,0,1,0,1,2,3,2)`
- root 1 state 8: `(0,1,2,1,3,0,2,3,0,3,0,2,3,1,2,1)`

The list at root 2 state 43 is the same sequence as the source list at root 4 state 25. The vertex orders omit different roots, and the colourings differ on vertex 3. They are different orbits.

`17:0 r6 s27`

| Intermediate | Degree | Side | Forward degree-five landings |
| --- | --- | --- | --- |
| 13, colour 0 | 6 | long | root 16, state 19, `q=143`, `R=1878`, descends, passing |
| 7, colour 3 | 6 | long | root 2, state 33, `q=143`, `R=1878`, descends, passing |
| 5, colour 2 | 6 | short | root 0, state 22, `q=155`, `R=1890`, descends, passing; root 11, state 38, `q=155`, `R=1890`, descends, passing |

Returns from 13, 7, and 5 all land on `r6 s27`.

Forward tuples:

- root 16 state 19: `(0,1,2,3,1,2,0,3,0,2,0,3,1,2,1,3)`
- root 2 state 33: `(0,1,2,1,3,2,3,0,3,0,2,1,0,1,2,3)`
- root 0 state 22: `(0,1,2,0,3,1,2,3,1,3,2,0,3,0,2,1)`
- root 11 state 38: `(0,1,2,3,1,3,2,3,0,2,0,1,0,1,3,2)`

`20:7 r7 s180`

| Intermediate | Degree | Side | Forward degree-five landings |
| --- | --- | --- | --- |
| 1, colour 1 | 6 | long | root 0, state 202, `q=252`, `R=2653`, descends, passing |
| 6, colour 2 | 6 | long | root 13, state 148, `q=252`, `R=2653`, descends, passing |
| 16, colour 0 | 7 | short | none |

The only degree-five singleton on the link of 16, after the first slide, is the original root. The return lands on `r7 s180` and is mass-stuck.

Forward tuples:

- root 0 state 202: `(0,1,2,3,2,1,3,2,3,1,0,1,0,3,2,0,3,2,1)`
- root 13 state 148: `(0,1,2,3,1,3,0,2,3,1,2,0,2,1,3,0,1,3,2)`

`20:7 r11 s18`

| Intermediate | Degree | Side | Forward degree-five landings |
| --- | --- | --- | --- |
| 10, colour 0 | 6 | long | root 9, state 23, `q=252`, `R=2653`, descends, passing |
| 17, colour 1 | 6 | long | root 19, state 14, `q=252`, `R=2653`, descends, passing |
| 5, colour 3 | 7 | short | none |

The return from 5, and the returns from 10 and 17, land on `r11 s18`.

Forward tuples:

- root 9 state 23: `(0,1,2,1,2,3,0,3,0,3,0,2,1,2,1,2,1,0,3)`
- root 19 state 14: `(0,1,2,1,2,3,0,3,0,3,0,1,2,1,2,1,2,3,0)`

The list at root 9 state 23 is the same sequence as the source list at root 11 state 18. The omitted roots differ, and the colourings differ on vertex 10.

## B. One-swap Kempe neighbours

Each locked orbit has exactly two Kempe neighbours that create a degree-five singleton. Each neighbour is realized by two chains of one colour pair. Those two chains are disjoint and their union is every vertex of the two colours, so the two swapped colourings differ by the transposition of that pair and determine one canonical orbit. Each such neighbour creates exactly one degree-five singleton, and the slide along it is unambiguous.

The neighbour itself, still at the failing root, also descends relative to its own higher rank. Any such descent stays at rank at least the trap: a drop below the trap would be a two-step mass descent from the stuck orbit.

`17:0 r4 s25`. Pairs used: `(0,1)` and `(0,3)`, the repeated colour with each long-arc colour. The short-arc colour 2 is unused.

| Neighbour at root 4 | Pair | Chains | Slide | Landing |
| --- | --- | --- | --- | --- |
| state 21, `q=163`, `R=1898`, descends | `(0,1)` | `{0,1,6,13}` and `{8,9,10,11}` | 11 | root 11, state 18, `q=171`, `R=1906`, descends, passing |
| state 30, `q=163`, `R=1898`, descends | `(0,3)` | `{0,3,9,15}` and `{6,7,11,12}` | 0 | root 0, state 43, `q=171`, `R=1906`, descends, passing |

Landing tuples:

- root 11 state 18: `(0,1,2,3,1,2,0,3,0,1,0,3,1,2,3,2)`
- root 0 state 43: `(0,1,2,3,1,2,3,0,3,0,2,3,0,1,2,1)`

`17:0 r6 s27`. Pairs `(0,1)` and `(1,3)`. Short-arc colour 2 is unused.

| Neighbour at root 6 | Pair | Chains | Slide | Landing |
| --- | --- | --- | --- | --- |
| state 30, `q=163`, `R=1898`, descends | `(0,1)` | `{0,1,4,10}` and `{8,12,13,14}` | 12 | root 12, state 26, `q=171`, `R=1906`, descends, passing |
| state 13, `q=163`, `R=1898`, descends | `(1,3)` | `{1,7,14,15}` and `{3,4,11,12}` | 1 | root 1, state 36, `q=171`, `R=1906`, descends, passing |

Landing tuples:

- root 12 state 26: `(0,1,2,3,1,2,0,3,1,2,0,3,1,0,3,2)`
- root 1 state 36: `(0,1,2,3,1,2,3,0,1,0,2,3,0,2,3,1)`

`20:7 r7 s180`. Pairs `(1,3)` and `(2,3)`. Short-arc colour 0 is unused.

| Neighbour at root 7 | Pair | Chains | Slide | Landing |
| --- | --- | --- | --- | --- |
| state 181, `q=222`, `R=2623`, descends | `(1,3)` | `{1,3,4,5,8,9}` and `{14,15,17,18}` | 8 | root 8, state 185, `q=258`, `R=2659`, descends, passing |
| state 121, `q=222`, `R=2623`, descends | `(2,3)` | `{2,3,8,10}` and `{5,6,12,15,18,19}` | 15 | root 15, state 133, `q=258`, `R=2659`, descends, passing |

Landing tuples:

- root 8 state 185: `(0,1,2,3,1,3,2,3,1,2,0,2,0,3,1,0,3,1,2)`
- root 15 state 133: `(0,1,2,3,1,2,3,2,3,1,2,0,3,0,1,0,1,2,3)`

`20:7 r11 s18`. Pairs `(0,2)` and `(1,2)`. Short-arc colour 3 is unused.

| Neighbour at root 11 | Pair | Chains | Slide | Landing |
| --- | --- | --- | --- | --- |
| state 28, `q=222`, `R=2623`, descends | `(0,2)` | `{0,2,4,8,10,16}` and `{6,12,14,18}` | 4 | root 4, state 94, `q=258`, `R=2659`, descends, passing |
| state 16, `q=222`, `R=2623`, descends | `(1,2)` | `{1,2,3,4}` and `{12,13,14,15,16,17}` | 12 | root 12, state 10, `q=258`, `R=2659`, descends, passing |

Landing tuples:

- root 4 state 94: `(0,1,2,1,3,2,3,0,3,0,2,0,1,0,1,2,1,2,3)`
- root 12 state 10: `(0,1,2,1,2,3,0,3,0,3,0,1,2,1,2,1,2,0,3)`

## C. Landing sets

For each trap, write `A` for every second degree-five slide, including the three returns to the stuck source, and `A*` for the forward landings only. Write `B` for the prepared slides. There is one degree-five singleton on each Kempe neighbour, so the “one slide per neighbour” reading is the same set as the slide along every such singleton.

On each of the four orbits, `A`, `A*`, and `B` satisfy: `A*` is disjoint from `B`, and `A` is disjoint from `B`. Forgetting the root and comparing the bare canonical lists still gives an empty intersection of `A*` with `B`.

| Orbit | Forward roots `A*` | Kempe roots `B` | Shared roots | Shared orbits |
| --- | --- | --- | --- | --- |
| `17:0 r4 s25` | 2, 16, 12, 1 | 11, 0 | none | none |
| `17:0 r6 s27` | 16, 2, 0, 11 | 12, 1 | none | none |
| `20:7 r7 s180` | 0, 13 | 8, 15 | none | none |
| `20:7 r11 s18` | 9, 19 | 4, 12 | none | none |

The Kempe slides land on the two degree-five neighbours of the failing root. Those neighbours are passing roots. The forward two-steps land on other degree-five vertices, also passing roots. No pair of a forward colouring and a Kempe colouring agrees on all common vertices after a global colour permutation. The best agreement is 12 of 15 vertices on order 17 and 13 of 18 on order 20, and that maximum is exactly the long-arc pairing in the normal form: the unmatched vertices are one Kempe chain with the Kempe vacancy removed.

## D. Prepared slides and stuck orbits

No prepared slide lands on a mass-stuck orbit. The eight landings are:

| Trap | Landing | Root status | `descent(i,1)` |
| --- | --- | --- | --- |
| `17:0 r4 s25` | `r11 s18`, `r0 s43` | passing | `None` |
| `17:0 r6 s27` | `r12 s26`, `r1 s36` | passing | `None` |
| `20:7 r7 s180` | `r8 s185`, `r15 s133` | passing | `None` |
| `20:7 r11 s18` | `r4 s94`, `r12 s10` | passing | `None` |

Each has `p = 1` and a strictly larger `R` than its trap (`1906` against `1878`, or `2659` against `2565`). Descent is the landing orbit’s own one-swap mass decrease. The strong form, read as “the prepared slide meets a descending orbit”, holds on these eight slides. Landing at a passing root is the case the kill condition explicitly leaves standing.

The returns in route A do land on a mass-stuck orbit, the source itself. That is a two-step fact. It is not a prepared-slide fact.

## E. Properness, without the slide lemma

Every route in sections A and B passed the edge test of the opening section. In particular the first slide along a singleton, the second slide, the Kempe swap, and the prepared slide are proper colourings of the triangulation with the vacancy at the vertex named in the tables. The return reproduces the source tuple, which is the independent check that the backward slide was computed as the inverse of the forward recolouring.

## OPEN: the long-arc correspondence

The equality of landing sets is dead. The relation that does hold on all eight long-arc singletons is the following.

Let `c` be the locked colouring of `T - r`, with the link labelled as above. Fix a long-arc vertex `x` of colour `β_x`.

1. The colour pair `{α, β_x}` has two Kempe chains in `T - r`. They partition the vertices of those two colours. Exactly one chain, `C_x`, contains `x`, and `C_x` contains exactly one degree-five neighbour `s_x` of `r`. The other chain contains the other degree-five neighbour. Swapping either chain yields one canonical orbit at `r`. After the swap of `C_x`, the vertex `s_x` is the unique degree-five singleton on the link.
2. Slide the vacancy from `r` to `s_x` and call the resulting colouring `K_x` of `T - s_x`. The old root receives colour `β_x`.
3. The first slide `r → x` has exactly one forward degree-five continuation, to a vertex `y_x` off the link. In the original colouring, `c(y_x) = δ`, the short-arc colour. Call the resulting colouring `S_x` of `T - y_x`. The old root again receives colour `β_x`. Among the vertices coloured by both `c` and `S_x`, only `x` has changed colour.
4. On `V \ {y_x, s_x}`, the colourings `S_x` and `K_x` differ on a vertex if and only if that vertex lies in `C_x \ {s_x}`. In particular `y_x` lies outside `C_x`.
5. The orbit of `K_x` and the orbit of `S_x` both descend in one mass swap at a passing root. They are distinct orbits.

Instantiations, with `C_x` the chain through `x`:

| Trap | `x` | `β_x` | `C_x` | `s_x` and Kempe orbit | `y_x` and two-step orbit | `δ` |
| --- | --- | --- | --- | --- | --- | --- |
| `17:0 r4 s25` | 3 | 3 | `{0,3,9,15}` | 0, root 0 state 43 | 2, root 2 state 43 | 2 |
| `17:0 r4 s25` | 10 | 1 | `{8,9,10,11}` | 11, root 11 state 18 | 16, root 16 state 20 | 2 |
| `17:0 r6 s27` | 13 | 0 | `{8,12,13,14}` | 12, root 12 state 26 | 16, root 16 state 19 | 2 |
| `17:0 r6 s27` | 7 | 3 | `{1,7,14,15}` | 1, root 1 state 36 | 2, root 2 state 33 | 2 |
| `20:7 r7 s180` | 1 | 1 | `{1,3,4,5,8,9}` | 8, root 8 state 185 | 0, root 0 state 202 | 0 |
| `20:7 r7 s180` | 6 | 2 | `{5,6,12,15,18,19}` | 15, root 15 state 133 | 13, root 13 state 148 | 0 |
| `20:7 r11 s18` | 10 | 0 | `{0,2,4,8,10,16}` | 4, root 4 state 94 | 9, root 9 state 23 | 3 |
| `20:7 r11 s18` | 17 | 1 | `{12,13,14,15,16,17}` | 12, root 12 state 10 | 19, root 19 state 14 | 3 |

One row carries the same state index on both sides: root 0 state 43 and root 2 state 43, the Kempe landing and the two-step landing through vertex 3 on `17:0 r4 s25`. Same index, different roots. They differ by the chain `{0,3,9,15}` with vertex 0 deleted.

The complementary chain is the same neighbour. Swapping it recolours the other degree-five vertex and leaves `s_x` as the unique remaining boundary copy of `α`, so the slide still runs along `s_x`.

This is the normal form: from the locked colouring, a long-arc colour `β_x` determines a pair of colourings, `S_x` and `K_x`, by either walking the vacancy two steps through `x`, or swapping `C_x` and walking one step onto `s_x`. Both give the old root colour `β_x`. Off that chain and off the two vacancies, they reproduce `c`.

## The short-arc vertex

The short-arc colour `δ` is not one of the Kempe pairs that create a degree-five singleton. The slide through `w` therefore has no partner in the correspondence.

On `17:0 r4 s25` and `17:0 r6 s27`, `w` is vertex 5, degree 6, colour 2. Each has two forward degree-five landings, and those landings’ original colours are the two long-arc colours. They descend. Their symmetric difference with either prepared colouring is not a single chain.

On `20:7 r7 s180` and `20:7 r11 s18`, `w` has degree 7 (vertex 16, colour 0; vertex 5, colour 3). After the first slide the only degree-five singleton on its link is the original root, and the return is the stuck source.

## Feasibility and next steps

The certificate for these four orbits is **High**: each root was enumerated in full, every slide and swap was checked edgewise, and the chain identity was checked on all eight long-arc vertices. These are all four locked mass-stuck orbits in the stated list.

A lemma that produces the same correspondence without enumerating `T - r` is **Medium**. Clauses 1 and 2 are local to the colour pair on the link once the chains are known. Clause 4’s “differ exactly on the chain” is then a comparison of two explicit recolourings. The existence of `y_x`, the equality `c(y_x) = δ`, and the degree split of `w` (degree 6 with two forward landings, degree 7 with none) use the rest of the colouring. Treating `c(y_x) = δ` as forced by the link alone would be speculative.

Next steps:

1. Drop the identification of the two landing sets. The witness is the four disjoint pairs of sets above.
2. Keep the preparation claim in the narrow form that was checked: each of the eight slides along `s_x` lands on a passing root and descends in one mass swap.
3. If a lemma is written, state the long-arc correspondence and keep `w` in its own case, with the degree-6 and degree-7 behaviours separated as they appear here.
4. Naming the particular mass move that decreases the landing rank is a further computation. This certificate only records that `descent(i, 1)` is `None`.
