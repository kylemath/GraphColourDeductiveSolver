# Hole-filling glue

**DOES NOT PLUG IN.**

This is not a four-colour proof. `TriangulatedFiveExtension`, `EmptyMassRegionHypothesis`, `MassMacroDescentHypothesis`, `EmptyRankedRegionHypothesis`, and `RankedMacroDescentHypothesis` are unproved. The theorems below are conditional assemblies.

**Missing lemma.** If every proper 4-colouring of one deletion of a minimum-degree-5 spherical triangulation can be carried by singleton slides and Kempe swaps to a proper 4-colouring of some, possibly different, deletion whose link uses at most three colours, then some degree-5 vertex \(r\) has the property that 4-colourability of the fixed graph \(T-r\) implies 4-colourability of \(T\).

## The implication that was asked for

Let \(T\) be a spherical triangulation of minimum degree at least 5. Suppose every proper 4-colouring of \(T\) with one vertex deleted can be carried, by singleton vacancy slides and Kempe swaps, to a vertex whose link uses at most three colours. The proposed conclusion is that every spherical map is 4-colourable.

The steps that are already theorems reduce every spherical map to one gate, and discharge that gate only while the deleted vertex stays fixed. The vacancy sentence does not enter the gate.

## What the induction already does

`four_color_of_triangulated_five_extension` says that `TriangulatedFiveExtension` implies 4-colourability of every spherical map. The proof inducts on the cardinality of the support.

`TriangulatedFiveExtension` is the statement: for every nonempty connected spherical triangulation of minimum degree at least 5, there exists a vertex \(r\) of degree exactly 5 such that 4-colourability of the induced subgraph \(T-r\) implies 4-colourability of \(T\). The root is chosen before any colouring. The gate asks for colourability of that one deletion, not for an extension of every colouring, and not for a hole that has moved.

On a supported vertex of degree at most 4, `isolate_closed` and `isolate_support_card_lt` pass to a smaller spherical map, the inductive hypothesis colours it, and `four_color_extension` extends across that same vertex. That branch is the degree-at-most-4 fill. It does not accept a degree-5 root, and it recolours the deletion it was given.

On minimum degree at least 5, `supportTransport` with `support_min_degree` carries the support onto a spherical map whose support is the whole carrier, and `exists_triangulated_completion_min_five` embeds that map in a connected triangulation \(T\) of minimum degree at least 5 on the same labels. The gate is applied to this \(T\). The isolate of the chosen degree-5 root is coloured by the inductive hypothesis. A 4-colouring of \(T\) returns along the embedding by `Colorable.mono_left` and `extendSupportColoring`. The header of `SphericalFourContact` records that no Kempe component is transported across the completion. The pullback starts only after \(T\) itself is coloured.

Filling whichever hole a slide has reached, and then inducting on the number of vertices, is a different leaf. The support induction is already closed once the gate is assumed. Its degree-5 leaf never fills a moved hole.

## What the contact theorem demands

`four_color_of_empty_ranked_region` and `four_color_of_ranked_macro_descent` discharge the gate from `EmptyRankedRegionHypothesis` and `RankedMacroDescentHypothesis`. The mass forms `four_color_of_empty_mass_region`, `four_color_of_mass_macro_descent`, and `four_color_of_mass_rank_specialization` are the same theorems at `massRankFamily`, which is `deletionMassRank`. `four_color_of_portfolio_descent` chooses one root and one portfolio index before the colouring quantifier.

In every one of these hypotheses the quantifiers are the same. For the triangulation \(T\) one first chooses a vertex \(r\) with \(\deg(r)=5\). Only then does one quantify over colourings of the single induced graph \(T-r\). A state is a `DeletionColouring` of that fixed deletion. A move is a `TwoSwapMacro`: equality, or one `ComponentStep`, or two `ComponentStep`s. A `ComponentStep` is one whole-component swap on \(T-r\). The target `boundaryTarget` says that the link of this same \(r\) receives at most three colours. `RankedGood` is `Breadcrumb.Good` for a `DeletionRankFamily` evaluated at this same \(r\): each macro's endpoint has strictly smaller rank. `RankedMacroPath` counts those macros. `colorable_of_ranked_good` and `colorable_of_mass_good` reach a boundary target and call `colorable_of_boundary_target`, which calls `four_color_extend_missing` at the same \(r\).

`Breadcrumb.good_of_forall_descent` turns a rank decrease at every non-target state into `Breadcrumb.Good`. The mass file records that this matches an empty dead-end region, and that bare Kempe reachability does not have those quantifiers. A path that merely arrives, with no rank falling on a fixed deletion, is not `MassGood` and not `RankedGood`.

So the existing contact theorem requires the hole to stay at one degree-5 root while a rank falls. A singleton slide is not a step of that descent.

## What a slide actually produces

`VacancySlide.lean` imports `SphericalDelete` only. It does not import the contact files, and the contact files do not import it.

`properOff_slide` preserves properness off the vacant vertex when the neighbour's colour is unique on the old link. `slideIsolateColouring` returns a colouring of `isolateGraph` at the new vertex. Its docstring states that it makes no assertion about the degree of the new vacancy. `uniqueAt_reverse` and `slide_reverse_away` show that the slide has an inverse on the relevant colours, and the first of those is explicitly not a progress conclusion. There is no rank on pairs \((\text{vacant vertex},\text{colouring})\).

After the slide, the state is not a `DeletionColouring` of the original root, so it is not a successor for `TwoSwapMacro`, `deletionMassRank`, or a `DeletionRankFamily` at that root. `DeletionRankFamily` is a rank of colourings of one already chosen deletion. Changing the deleted vertex leaves its domain.

## Gaps that are not theorems

1. No theorem interleaves `VacancySlide.slide` with `ComponentStep`. One slide under `UniqueAt` is proved. A Kempe swap on one fixed deletion is proved. A finite path that uses both, and that may change the vacant vertex more than once, is not a relation in the checkout.

2. No theorem turns the landing colouring into a `DeletionColouring` of the landing vertex. `inducedColouring` converts `ProperOff` into a colouring of the induced deletion, and `isolate_colouring_properOff` converts an isolate colouring into `ProperOff`. Neither is applied to a slide that began as a `DeletionColouring`, and neither is applied after a Kempe swap on a graph whose hole has moved.

3. No theorem concludes that the landing link uses at most three colours. `boundaryTarget` is a predicate on a `DeletionColouring` of a named vertex. The vacancy file never mentions it.

4. No theorem fills the landing vertex from such a path. `colorable_of_boundary_target` and `four_color_extend_missing` colour the whole graph from a proper colouring of one induced deletion whose neighbour-colours omit a colour. They take that deletion colouring as input. They do not take a slide. `four_color_extension` stops at degree 4 and recolours the deletion it started with. The degree of a slid vacancy is not known to be at most 4.

5. No theorem derives `TriangulatedFiveExtension`, `EmptyMassRegionHypothesis`, or `EmptyRankedRegionHypothesis` from the vacancy sentence. `PortfolioDescentHypothesis` still uses `TwoSwapMacro` and `boundaryTarget` at one root chosen first. `exists_pos_degree_le_five`, together with minimum degree 5, yields some vertex of degree 5 on a nonempty spherical map, but that combination is not a named theorem and is not the obstruction. The gate and the contact hypotheses already ask for a degree-5 root. They also ask for a descent that never moves it.

The missing lemma stated at the top is gap 5, packed as the single implication the assembly would need. Gaps 1–4 are why that lemma is not an instance of `colorable_of_boundary_target`.

## Feasibility

Feasibility that the vacancy sentence instantiates the mass or ranked contact: **Low**. The deleted vertex is part of the state type of those hypotheses, and a slide changes it.

Feasibility that proving the missing lemma would be absorbed by the existing induction, completion, degree-4 extension, and support transport: **High**. `four_color_of_triangulated_five_extension` is exactly that absorption, and its proof already contains those three constructions.

Feasibility that the missing lemma is `colorable_of_boundary_target` applied at the landing vertex: **Low**. The landing state is not a `DeletionColouring` with `boundaryTarget` in this checkout, and the contact theorems that call `colorable_of_boundary_target` call it at the original degree-5 root.

## Next steps

1. Keep singleton slides out of `MassGood`, `RankedGood`, and `PortfolioDescentHypothesis`.
2. A moving hole can meet the assembly only by a proof of the missing lemma, aimed at `TriangulatedFiveExtension`. Routing it through `RankedMacroDescentHypothesis` requires a rank on pairs \((\text{vacant vertex},\text{colouring})\) that falls while the vacant vertex changes. No such rank is defined here.
3. Leave completion, support transport, and the degree-4 extension where they already sit, inside `four_color_of_triangulated_five_extension`. They do not move a hole.
