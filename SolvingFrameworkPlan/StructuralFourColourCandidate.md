# Gate D: root-selecting Kempe escape, with exterior-aware progress

Date: 4 October 2026. Status: **research candidate, neither theorem nor algorithm**. This is one precise attack after the compiled degree-four and small-order gates. It must not be inserted as an assumption into the advertised general result.

## Exact candidate and its strength

Let T be a finite simple spherical triangulation with at least twelve vertices and minimum degree at least five. Let D(T) be its degree-five vertices. For r in D(T), let H = T − r, and list r's five neighbours B in its embedded cyclic order. A state c is a proper map V(H) → {0,1,2,3}. A legal move chooses two distinct colours and **one connected component** of the induced bichromatic subgraph, and exchanges those two colours throughout that component. A target state uses at most three colours on B; adding r in the missing colour extends the colouring.

The first candidate is the following quantified assertion:

> There are fixed constants C,k and executable procedures Select and Step such that, for every T in this class, Select(T) returns r ∈ D(T); for **every** proper four-colouring c of T − r, Step reaches a target by legal moves within C·|V(T)|^k steps. Select, each Step, and all maintained data have polynomial total cost.

This is deliberately a **root-selection strengthening** of four-colourability. It does not require every degree-five root to work, but it requires every colouring at the selected root to work. That universal colouring quantifier is a Kempe-class obligation. Failure of the candidate would not refute the Four Colour Theorem or the overall structural objective. The fallback is to constrain the input to a constructively specified reachable family of recursively produced colourings; the invariant describing that family must itself be proved and preserved. Merely calling the family “extendible” is circular.

The triangulation restriction requires the separately stated [support-carrier and triangulation-completion obligations](TriangulationCompletionObligation.md). They include proved filling preservation under edge addition and a support-size induction measure, since completion can increase the edge count. Finite enumeration may falsify this research candidate or validate examples; it does not establish universal coverage.

## Invariant, information, and measure obligations

Invariant: H stays fixed; the state is a proper four-colouring; all moves are genuine connected-component exchanges. The data available to Step include the **entire exterior graph, rotation, and current colouring**, not only the five boundary colours and six bichromatic connectivity partitions.

A proposed proof interface is an executable certificate P(T,r,c) with a lexicographic measure (p,q) in the natural numbers. For every non-target reachable state, a certified legal move must strictly decrease (p,q), preserving P. p may be a coarse structural potential; q is a root- and exterior-dependent plateau rank. Both coordinates and the number of steps must have proved polynomial bounds. Once a target is obtained, delete the root in the outer recursion and reconstruct its colour; the outer vertex-count measure decreases. Finding a certificate and finding the move are part of the cost bound.

**No concrete P,p,q is currently established.** “Distance to a target” would provide a rank only after reachability is proved, and computing it by enumerating all colourings is exponential. It therefore cannot discharge this interface. Proving universal coverage and polynomial bounds remains the gate-D research problem.

The first kill witness for the quantified candidate is one triangulation T for which every degree-five root has a Kempe component of T − r containing no target colouring. The smallest such T in an explicitly searched size range would be a minimal witness **within that range**, not an unqualified globally smallest counterexample. A growing required distance can kill a proposed particular polynomial bound without killing all bounds.

## Independently replayed Kittell experiment

Input: `backgroundMaterial/agent1720/groups/K6_kittell.json`, SHA256 `71d772e23a5b8118c19f8e26c76bfe39b290594bf7464b2d06b04af3126b7465`. The replay consumes the edges, independently checks planarity, enumerates all proper deletion colourings modulo global colour renaming, reconstructs all bichromatic component moves, checks move reversibility, and computes target distances. The graph has 23 vertices and 63 edges. The input records its provenance as Sage's `graphs.KittellGraph` in [Sage's generator source](https://github.com/sagemath/sage/blob/develop/src/sage/graphs/generators/smallgraphs.py).

The replay independently reproduces all fifteen per-root colouring counts and distances in the input: **6,350 root-colouring states**, each root's Kempe graph connected, and every state reaches a target in at most four moves. Kittell therefore supplies no kill witness for the new candidate.

It does kill a narrower proposed progress mechanism. Define sigma(c) as the boundary colours, canonicalized by first boundary occurrence, together with the partitions of boundary vertices induced by each of the six bichromatic subgraphs. This quotient has forty signatures across the fifteen deletions. Different concrete states with the same sigma have different sets of successor signatures: sigma is not a complete transition state.

For a stronger check, an abstract action is (colour pair, nonempty boundary subset), meaning swap the unique bichromatic component intersecting B in exactly that subset. Components disjoint from B are excluded from this particular action model. At each signature require **one common action** that works for every represented concrete state. Start with target signatures and repeatedly add signatures having an available common action all of whose represented successors are already winning. The robust attractor contains **35 signatures; five remain losing**. This reproduces the previous report independently.

Consequently there cannot be a policy selecting a single boundary action from sigma alone, with a strictly decreasing well-founded rank depending on sigma alone, that solves all these concrete inputs. This conclusion applies to this precisely defined memoryless boundary-action model. It says nothing against policies using the full exterior, root identity, memory, interior swaps, a bounded multi-move macro, or an enriched plateau rank. It also says nothing against four-colourability: all tested concrete states succeed.

The detailed collision witness, per-root counts, cyclic boundaries, five losing signatures, and hash are in [replay-results.json](../backgroundMaterial/planemap-structural/replay-results.json). The replay source is [replay.py](../backgroundMaterial/planemap-structural/replay.py). These are computational research evidence, not Lean theorems. The immediate experiment is to refine sigma with root-dependent exterior data or two-step component-interaction information, recompute robust attraction, and reject each proposed rank as soon as this known test defeats it. Passing this finite test still leaves the universal lemma and complexity proof open.

## First refinement experiment: retain root identity

Repeating the robust game separately at each root, rather than pooling signatures from distinct deletions, gives zero losing signatures at roots `2,4,5,8,9,12,14,16,18,20,22`. Roots `3,13,17,21` each retain five losing signatures. Thus merely selecting the root and keeping root-specific transition information repairs the tested boundary policy at eleven of fifteen roots. It does **not** repair it at every root, and nothing here gives a uniform rule for selecting a good root in general. This positive finite observation is why the quantified candidate selects one root rather than demanding every root work.

## Lower-strength alternative: recursively supplied winning certificates

Instead of demanding all Kempe classes at a selected root extend, define a computable abstraction alpha(T,r,c) and its concrete action semantics. Define W0 as target abstractions; W(j+1) adds states with a legal abstract action whose **every concretization successor** belongs to Wj. A certificate consists of the least attained layer j together with a certified action. This is an explicit robust-attractor condition, not a synonym for colouring existence.

The alternative induction interface is: the recursively executed deletion algorithm returns (c, certificate alpha(T,r,c) ∈ Wj) at the root selected by a proved structural rule, with j and all action/extraction costs polynomially bounded. We must prove the recursive algorithm can produce this stronger output and that its reconstruction preserves the next required certificate. For our finite Kittell fixture, W is genuinely computed and root selection gives a nonempty successful range. For arbitrary spherical maps, existence and preservation of certificates are **unproved**, and computing W by enumerating all global colourings supplies no polynomial algorithm. A universal lemma saying only “an extendible colouring exists” would be the original theorem's obligation in disguise; it must not be accepted as a coverage proof.


## Current attack: an exterior bit and a bounded kill-witness search

The [interior-escape report](../backgroundMaterial/planemap-structural/InteriorEscapeReport.md) tests every common labelled interior action and every repeated-colour boundary action on the twenty losing root/signature cells. None gives a common one-step escape into the old robust winning set. Nevertheless the directly computed bit beta, testing whether the smallest remaining vertex's canonical {1,3} component meets the boundary, repairs every root-specific Kittell robust game using the original boundary actions. Verified finite lookup ranks at roots 3,13,17,21 are respectively at most 4,5,4,4. Hiding the root still leaves ten of eighty refined observations losing.

This refutes the inference that failure of those one-step actions rules out observation refinement. Beta is an observation, not a preserved invariant or a universal rank. The tables are obtained by exhaustive finite analysis; they do not supply polynomial root selection or a solver complexity theorem.

The distinction between the quotient game and actual policies is essential: a losing robust attractor excludes a policy with a strictly decreasing observation-only rank and a common-action guarantee against arbitrary represented successors. A concrete memoryless policy could revisit an observation while its hidden concrete state progresses. The quotient failure alone does not disprove every such actual policy.

The icosahedron has twenty deletion-colouring orbits at each of its twelve roots, all reaching a target within one swap. Its original boundary-action game wins at every root. The [Plantri search report](../backgroundMaterial/planemap-structural/SearchReport.md) checks all 118 minimum-degree-five triangulations through order twenty, comprising 1,586 root instances, 244,051 colouring orbits, and 1,626 Kempe classes. Every checked class contains a target. This searches the stated kill witness rather than assuming class connectivity; some deletion graphs have multiple Kempe classes. No claim beyond that finite range or about polynomial growth follows.


## First root rule: available but insufficient for the refined rank

The explicit rule fixes the smallest-labelled anchor and selects the smallest degree-five root outside its closed neighbourhood. `DegreeFiveOutside.lean` proves there are at least six eligible roots in any minimum-positive-degree-five spherical core. The proof combines the degree deficit outside the anchor's star with spherical sparsity; it does not assume a triangulation or graph census.

The [anchor-rule experiment](../backgroundMaterial/planemap-structural/AnchorRuleReport.md) tests this rule with the fixed sigma-plus-beta robust observation. It succeeds on 117 of 118 fixtures but fails at order twenty, graph 36, root 8. Its 198 colouring orbits give 55 observations, five of which remain in a certified robust losing set. All 198 concrete colourings still reach a target in the full Kempe graph. Thus availability is proved, the restricted root/rank rule is falsified, and the full quantified escape candidate remains open. Twelve of the 46 failing root instances in the bit stress test are genuinely exterior, so moving the seed outside the boundary does not by itself repair the model.
