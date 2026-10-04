# Interior escape and a one-bit observation, 4 October 2026

These are finite computational results, not Lean theorems, a uniform reduction rule, or a complexity bound. Run `python escape.py` with NetworkX installed. The input SHA256 is recorded in `results.json`; the input is the corrected 23-vertex, 63-edge Kittell graph. The second fixture is `networkx.icosahedral_graph()` (12 vertices, 30 edges, degree five everywhere).

## Observation and action semantics

At each deleted degree-five root, orient the boundary using NetworkX's planar embedding, starting at its smallest labelled neighbour. Canonicalise colour names by their first appearance on the boundary, then in increasing full vertex order. The old observation `sigma` contains the boundary colouring and all six bichromatic partitions of boundary positions.

An old boundary action `(a,b,I)` swaps the unique `(a,b)` component whose intersection with the boundary is exactly the nonempty index set `I`. The action is common when it exists for **every** concrete colouring with the same observation. Its resulting observation may differ across those colourings. A robust winning action must take all of them to an already winning observation.

An interior action `(a,b,v)` selects the component containing the fixed labelled vertex `v`, requiring this component to miss the boundary. This is also required to be common over every representative of the observation. We test every vertex seed and colour pair. 'Some escape in each concrete state' is a different, strictly weaker statement than one common action.

A repeated-colour action is an old boundary action whose pair contains the boundary's unique repeated colour. The JSON separates common actions from counts of states admitting some action.

## One move does not repair the old observation

For each of the five losing signatures at each of roots 3, 13, 17, and 21, there is **no** common interior action, and **no** common repeated-colour boundary action, taking every representative directly to the old robust winning set. This checks 20 root/signature cells. Concrete state escape counts vary; root 3 has a repeated-colour one-step escape in every losing concrete state, but the action cannot be chosen from the old observation alone.

Adding all labelled interior actions while retaining the old observation also leaves five losing signatures at each of the four roots. Thus simply adding interior moves does not repair that particular memoryless game.

## A directly computable bit does repair each root-specific fixture

Define the observation bit

`beta(c) := the component of the smallest remaining vertex in canonical colours {1,3} meets the deleted-root boundary`.

If the seed is not in either colour, the bit is false. At all four failing Kittell roots the smallest remaining vertex is 0. This is an ordinary bichromatic connectivity predicate. It is evaluable by a graph traversal, with no enumeration of colourings and no target-distance query.

Using observation `(sigma,beta)`, **only the original boundary actions**, and knowledge of the root, the robust games have no losing observation:

| Root | Concrete colouring orbits | Refined observations | Largest certified lookup rank |
|---|---:|---:|---:|
| 3 | 508 | 54 | 4 |
| 13 | 418 | 55 | 5 |
| 17 | 418 | 64 | 4 |
| 21 | 398 | 60 | 4 |

`results.json` records a complete lookup strategy: every nonterminal observation has one common action, and every concrete successor has strictly smaller recorded rank. The script checks that condition against all representatives. It also records full colourings witnessing where the two bit values lead to different selected actions for the same old signature.

The bit is a **computable observation**, not a preserved invariant. The ranks and policies above are finite tables obtained by exhaustive attractor analysis; they are not the required uniform rank formula. The seed and pair are empirical choices for this fixture. No graph-independent selection theorem follows. Pooling all Kittell roots while hiding the root still leaves 10 of 80 refined observations losing. Root-specific success must not be presented as a single root-blind policy.

This gives a concrete correction to the team's inference: failure of one common interior or repeated-colour action does **not** imply that a boundary refinement cannot fix the roots. A refinement can distinguish states requiring different boundary actions. The bit above demonstrates that phenomenon.

## Icosahedron and the quantified kill witness

Each of the 12 roots has 20 proper deletion-colouring orbits modulo global colour permutations, and 10 old boundary signatures. Its full Kempe state graph is connected. Every orbit reaches a three-colour boundary in at most one swap; the old restricted robust game already wins at every root. The pooled refined game has 20 observations and no losing observation. The icosahedron therefore is a sharp minimum-degree-five fixture, but does not stress this candidate as strongly as might have been hoped. This computation does not by itself construct its `SphericalMap` carrier.

The reachability kill witness remains precisely: one finite simple spherical triangulation with minimum degree at least five, such that **for every degree-five vertex r**, there is a proper four-colouring of `T-r` whose Kempe-connected class contains **no** colouring using at most three colours on the boundary of r. Neither Kittell nor the icosahedron supplies that witness. This would kill the universal deletion-colouring quantifier in the root-selecting candidate; it would not refute four-colourability. Even absence of such a witness would not establish the polynomial bound.

The script asserts properness of every enumerated colouring, closure of every component swap within the enumeration, involutivity of the resulting state transitions modulo global colour permutation, and strict rank decrease of each lookup action on every representative. Enumeration completeness follows from branching over all four colours, introducing new colour names in canonical order. Results remain computational evidence, not kernel-checked proofs.
