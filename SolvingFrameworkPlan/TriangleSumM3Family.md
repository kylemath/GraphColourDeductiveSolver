# An infinite family with exact fan-selection length three

Math, 5 October 2026. Hand theorem with an independently checked finite seed. Both parallel teams reviewed the clique-interface argument. No graph of a new order was generated, coloured or searched. This takes Task C's requested infinite-family direction; it does not settle whether m is bounded on all triangulations.

## The family and result

Let Q be the existing order-17 graph 1, with its saved embedding and vertex labels. Its disjoint facial triangles are F₋={1,2,7} and F₊={3,4,11}; both avoid vertex 0. Form Hₖ from k copies of Q arranged in a chain: identify F₊ of each copy with F₋ of the next, reversing boundary orientation, and retain a single copy of each interface edge. Each step replaces a facial triangular disc by the triangulated disc from the next copy.

For every k≥1, Hₖ is a simple minimum-degree-five spherical triangulation with

**|V(Hₖ)|=14k+3 and m(Hₖ)=3.**

Thus the family has orders 17,31,45,… and supplies infinitely many exact-m=3 graphs. For k≥2 it also has vertices of degree at least eight. These statements follow from the hand argument below; they are not computational results on those new orders.

## The component restriction lemma

Suppose G=A∪B, their vertex intersection F is a clique, and there is no edge from A∖F to B∖F. Consider a proper deletion colouring with its hole r in A∖F. For any colour pair, a whole bichromatic component of G-r restricts to either the empty set or exactly one whole bichromatic component of A-r.

To see connectedness of a nonempty restriction, take a path in the global component between two of its A vertices. Replace each excursion through B∖F by a path of length zero or one in the interface. Its endpoints lie in F and carry the selected colours. If they are distinct, they are adjacent in the clique; properness makes their colours distinct, so that interface edge is an edge of the same bichromatic graph. The resulting path stays in A-r. Completeness follows because every pair-edge path already in A-r is also a global path. These two facts establish the claim.

Conversely, any whole pair component K in A-r has a unique containing global component, whose restriction is exactly K. Swapping that global component therefore performs precisely the selected swap on A, while also recolouring any attached B vertices. Properness is preserved by the whole-component move.

For our triangular interfaces the clique hypothesis holds at every stage. The hole is fixed outside the interface when this lemma is used.

## Lower bound preserved by triangular connected sums

Assume A and B are minimum-degree-five spherical triangulations, both have full proper four-colourings, and every legal vertex/fan pair in each has an admitted start with no mixed fill in at most two moves. Glue them along facial triangles as above.

Each interface vertex has degree deg_A(v)+deg_B(v)−2≥8. Consequently a degree-five vertex of the glued graph belongs to exactly one side and is outside F. Its neighbour set, cyclic link and induced graph on those neighbours are unchanged; its legal fans are precisely its old legal fans. No new edge between old A vertices is introduced, because every interface edge was already present.

Take such a root r in A and any legal fan there. Choose A's certified hard start. Its fully coloured interface triangle uses three distinct colours. Permute a full four-colouring of B to agree on those three colours and extend the start to the glued graph. It remains proper and fan-admitted. The same construction works with A/B interchanged.

Suppose this extended start admitted a global mixed filling path of length at most two. The general short-fill theorem in `MathShortFillTheorem.md` converts it to at most two Kempe swaps at the original root r. Restrict those swaps to A using the component restriction lemma, deleting any move with empty restriction. Every resulting move is one whole original A component. Since r has no neighbours outside A, a global target at r is also an A target. This contradicts the chosen hard start. Thus every global legal pair has a start requiring more than two moves.

This argument specifically uses the proved short-fill theorem; it does not assume that every longer slide path can be projected, or that moving holes stay on one side.

## The seed certificates

The independent script `longtable/audit/triangle_sum_seed_check.py` checked only the existing Q record. Its complete evidence is `triangle-sum-seed-results.json`.

- All 60 legal vertex/fan pairs have proper admitted lower witnesses with no mixed target in layers 0,1,2.
- At vertex 0, fan 1, the two chords are 2–4 and 2–5. All 34 admitted starts have Kempe-only distances 0,1,2,3 in counts 5,17,10,2. Each has a saved pure path of length at most three, recomputed and replayed independently.
- F₋ and F₊ are actual facial triangles, are disjoint and avoid root 0.
- An explicit full proper colouring of Q is

```
[3,0,1,0,1,2,1,2,0,3,1,3,0,2,3,2,0]
```

Therefore Q has the lower property needed for connected sums and a matching three-swap upper bound at one fixed fan. Its full colouring is explicit, so neither the construction nor the extension step invokes the Four Colour Theorem.

## Induction and upper bound

Triangular connected sum preserves a simple spherical triangulation: replacing a triangular face by a triangulated disc preserves the embedding and triangular faces. Every noninterface vertex retains its degree; interface degrees add and lose exactly the two duplicated interface neighbours. The minimum degree remains at least five. Each new copy contributes 17−3=14 vertices, giving 14k+3. Full colourings extend along the interface by a permutation of colours, so the lower-bound gluing lemma applies inductively to every Hₖ.

For the upper bound use root 0, fan 1 in the last copy. Its incoming face avoids root 0, so the root still has its original five neighbours and the same legal fan. Any admitted colouring of Hₖ-0 restricts to one of the seed's 34 starts, after a consistent global permutation of colour names. Apply its recorded sequence of at most three pure swaps. At each step lift the chosen seed component to its unique global component by the restriction lemma. The local colouring follows the seed path exactly, and the global colouring remains proper. Root 0 has no exterior neighbours, so the seed target is a global target. Hence this one fan works within three moves for every start, proving m≤3.

The all-pair lower bound gives m≥3. Together these prove exact m=3 for every k.

## Scope

This is a hand construction with finite verified base certificates, not a Lean compilation or a new-order census. It supplies an explicit natural class on which C2's m≤3 bound holds sharply. It proves no universal bound and produces no m≥4 graph. The graphs have separating triangles; no corresponding claim about four-connected triangulations is made. Claims of smallest possible new order or novelty in the literature are not part of this result.
