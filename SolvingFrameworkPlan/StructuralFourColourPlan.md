# Structural Four Colour execution plan

Date: 4 October 2026. This replaces the seven-track exploration as the active route in the navigator. Earlier work and failed proposals remain in its historical branch. The companion [Gate-D candidate](StructuralFourColourCandidate.md) is the first quantified research target.

## Finish line

Construct a new structural proof, without a large configuration census, that supplies an executable four-colouring for every finite simple spherical map. Prove correctness, termination, and a polynomial bound for the implementation; then benchmark it against DSATUR, SAT, genetic, and randomized solvers. A geometric planarity bridge extends the statement to ordinary planar graphs. A colouring existence theorem alone does not complete this objective, and a polynomial primitive does not establish a polynomial solver.

The authoritative Lean checkout is `../mathlib4-planemap`, using Lean `v4.35.0-rc3`. GraphColour's older Lean 4.15 Kempe project is a separate package. Navigator statuses refer to named declarations and checked artifacts, not optimistic feasibility judgments.

## Checked foundation

`SphericalMap` consists of a finite simple graph, a cyclic rotation at each nonisolated vertex, and a filling property for mod-two even edge combinations. `SphericalMap.ofPlaneMap` proves the filling property from the generated PlaneMap construction; it is not an assumed planar oracle. Spanning-subgraph closure and `isolate_closed` retain vertex labels and accommodate disconnected deletions. Strict decrease of edge count supplies the existing induction carrier.

The general Five Colour Theorem compiles for spherical maps and generated PlaneMaps. Its axiom audit reports only `propext`, `Classical.choice`, and `Quot.sound`. The original audited sources were already committed at `5efe00e4f4908480d8c25e1c9f12d83d301ea41e`; `PlaneMapBaseline.sha256` records the 28-source baseline separately from the new four-colour modules. The repaired compatibility module `JordanGrow` is included in that baseline.

Generated construction history, a spherical rotation/filling certificate, a geometric drawing, and a forbidden-minor definition are distinct representations. No implication between them is advertised without its own theorem. In particular, the checked foundation does not yet represent every ordinarily planar graph.

## Gates and present status

| Gate | Deliverable | Status |
| --- | --- | --- |
| A | Extend a four-colouring after deleting a vertex of degree at most four in a spherical map | Compiled |
| B | Spherical elimination certificate and four-colourability through eleven vertices | Compiled |
| C | Sound boundary semantics for one concrete candidate, with explicit exterior information | Research in progress |
| D | Uniform structural reduction with coverage and a proved progress measure | Open; this is the mathematical four-colour gap |
| E | General spherical four-colour theorem, executable reconstruction, termination, and polynomial cost | Open; depends on D |
| F | Representation of ordinary planar graphs and transport of the constructive result | Open; can proceed beside D |

### A: the valid degree-four Kempe argument

`PlaneMap/FourColorExtension.lean` proves `SphericalMap.four_color_extension`. If fewer than four colours occur on the neighbours, the missing colour extends directly. With four distinct neighbour colours, alternating separation prevents the two crossing bichromatic connections from both occurring; one component exchange opens a colour. `alternating_walks_intersect` needs four neighbours and successive rotation steps, not a fifth neighbour or triangulation.

This is a spherical extension theorem. An abstract 4-degenerate graph need not be four-colourable: K5 is a counterexample. No graph-only four-colouring claim is inferred from the degree bound.

### B: elimination and the twelve-vertex obstruction

`SphericalSmallOrder.lean` proves the incidence coordinates sum to zero, so the incidence range has codimension at least one. Together with filling and the constant face function in the boundary kernel, this sharpens the rank bound to `e + 2 ≤ s + f` for an edge-containing map, where `s` counts nonisolated vertices. The short-face argument forces a low-degree vertex when necessary; no connectedness or minimum face-length premise is added.

If every positive degree is at least five, the degree and face counts give `5s ≤ 2e` and `3f ≤ 2e`. With the sharpened rank bound, `12 ≤ s`. Consequently every edge-containing spherical map on at most eleven labels has a positive-degree vertex of degree at most four.

`FourColorSmallOrder.lean` defines `HasFourElimination` on the graph, quantifying over its spanning subgraphs. It proves spherical four-colourability under this condition, proves the condition through eleven vertices, and supplies the PlaneMap wrappers. `FourEliminationOrder.lean` packages a finite certificate whose steps contain the removed vertex, exact isolated carrier, degree bound, strict edge decrease, and tail. Certificate soundness gives a four-colouring, and certificate length is at most the initial edge count. Witness existence uses classical choices; this is not yet an executable certificate search or colouring reconstruction algorithm.

Regression checks include K4, symbolic small paths, and a five-vertex path deletion retaining two edges with formally disconnected endpoints. The classical icosahedron has twelve vertices, thirty edges, twenty faces, and degree five everywhere: it explains sharpness and lies outside the eleven-vertex corollary. A spherical Lean encoding of that example is a remaining example task, not evidence already provided by the tests. Enumerating graphs through eleven vertices cannot test the minimum-degree-five obstruction.

### C: one candidate's boundary interface

Specify the patch, cyclic boundary, proper colourings, legal component exchanges, target extension, and the information available to each move. Prove restriction and gluing for that patch. Distinguish reducibility of one patch from coverage of all maps. A whole port of the Rocq development would not by itself discharge coverage and is not the active route.

The independently replayed Kittell experiment shows why boundary connectivity alone is insufficient for a particular memoryless policy: identical boundary signatures can have different successors, and five of forty pooled signatures lose the robust boundary-action game. This is computational evidence against that precise information restriction. It does not disprove full-state Kempe search or the Four Colour Theorem. The candidate therefore permits exterior information and root selection.

### D: attack the quantified lemma first

The companion candidate specifies finite simple spherical triangulations of minimum degree five, a selected degree-five root, legal four-colour component exchanges, a target with at most three boundary colours, and fixed polynomial bounds. Its universal quantifier over deletion colourings makes it stronger than four-colourability. It is a research conjecture, never a premise silently added to the advertised theorem.

The first experiment is to find an efficiently computed exterior invariant and a well-founded progress rank, or produce a witness defeating the candidate. Root-specific replay succeeds at eleven of fifteen tested Kittell roots and fails in the restricted boundary-action model at four. This gives a test fixture, not a general root-selection rule. Any proposed invariant must survive that fixture before receiving further interface work.

Require every proposal to name the graph class, move relation, invariant, measure, input colouring family, coverage statement, and a falsifying witness. A rank equal to distance to an extendible state is circular until reachability is proved, and exhaustive colouring-state search does not meet the polynomial objective. If the universal colouring obligation fails, a recursively generated family is admissible only with an independent invariant proved to be preserved and sufficient for extension.

Triangulations are a restricted research class. General spherical maps require a proved completion/restriction interface or direct coverage; minimum-degree-five cores are not automatically triangulations. Neither Meyniel's theorem starting from an existing four-colouring, nor a successful five-to-four Kempe search, nor chromatic-polynomial, flow, or sheaf reformulations supplies this missing structural theorem. The local degree-five hub's failure of D-reducibility and the computed Birkhoff diamond result remain useful historical evidence, with their original scope.

### E: executable construction and complexity

`Coloring/FiniteReachability.lean` already provides executable finite component extraction and a bichromatic component swap, with proofs of equality to reachability and preservation of proper colouring. Kernel `decide` checks and actual evaluation on two disjoint edges verify the swap changes only the selected component. Its instrumented full-scan model charges exactly `n³` adjacency slots for `n` expansion rounds. This is an abstract accounting theorem, not a bound on arbitrary adjacency deciders, data structures, the compiler, or the complete solver.

Next extract a finite representation of rotation and deletion carriers, a computable low-degree choice, and an executable degree-four reconstruction rule; prove these agree with the mathematical interfaces. Then integrate a successful D rule into recursive deletion. The outer edge/vertex measure and inner progress measure must compose into a termination proof. Bound construction, component work, rank computation, root selection, and total number of steps explicitly. Finite certificates with bounded length are useful intermediate deliverables but do not discharge these implementation obligations.

Only after correctness and the complexity theorem, benchmark the executable solver against the named baselines on declared datasets and matched hardware/time budgets. Include correctness checks, adverse instances, preprocessing cost, and failures. Competitive performance is a separate empirical claim.

### F: ordinary planar graph bridge

Choose and document the input planarity representation. Construct a spherical rotation/filling certificate from that representation and prove its graph agrees with the original graph, including disconnected components and isolated vertices. This bridge may advance beside D. A forbidden-minor definition without a proved embedding construction is insufficient.

## Execution and evidence rules

1. Preserve the audited Five Colour baseline; keep new A/B sources separate until built and audited. Commit only explicit owned files, following `PlaneMapGitWorkflow.md`; the nested `mathlib4/` checkout is excluded.
2. Build the new modules and permanent regression tests. Audit theorem axioms and rebuild the custom stack from source with old custom build artifacts excluded. Record a hash manifest for the checked revision.
3. Publish the consolidated route to navigator revision 34, preserving old node IDs, notes, results, and failed routes in an inactive historical branch. Active statistics describe the new route. Proof gates and computations are labelled separately.
4. Attack the first Gate-D statement and its existing counterexample fixtures before extracting more speculative interfaces. Keep C proportional to that candidate.
5. Maintain an executable A/B implementation track and a representation track beside D. No global theorem, executable solver, or polynomial bound is marked proved until its corresponding artifact is checked.

The verified advance reaches Heawood's boundary: degree four extends, while a core with minimum positive degree five has at least twelve vertices. Crossing that boundary remains new mathematics. It is the active objective, not a consequence of completing the infrastructure.
