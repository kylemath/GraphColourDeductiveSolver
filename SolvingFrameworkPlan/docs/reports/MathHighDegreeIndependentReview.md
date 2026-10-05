# Independent review: high-degree separator landings

Math triangle-carry research team, 5 October 2026. Reviewed `MathHighDegreeLandingResearch.md` independently. All acceptance is hand acceptance; no census, colouring enumeration, or Lean compilation was performed.

## Component interface

The component projection and lift premise is correct even with the hole on the separating triangle. Its surviving interface is the edge pq. A bichromatic excursion through the other side has both endpoints on that edge, and can be replaced by the edge or a stationary walk. A component of one side avoiding p,q cannot gain vertices on the opposite strict side. Thus every component explicitly selected below is an actual whole global component, not a fragment of one.

## Balanced degree-six theorem

Accepted: side-degree split 4+4 gives a fixed-hole pure fill within three Kempe swaps.

The relative degree-four lemma is sound. In a four-colour link (p,a,b,q)=(α,γ,δ,β), the potential αδ path p–b and γβ path a–q have alternating endpoints and disjoint colour sets. The spherical disk/Jordan premise excludes simultaneous locks. The chosen unlocked component misses the active boundary endpoint; the other boundary endpoint is outside the colour pair. It therefore changes precisely one of the two strict-side link vertices and remains globally confined.

After the initial B swap, the proof names a currently missing complementary colour γ, while p and q retain α,β. If the global link still contains γ, the A link has either one complementary colour (at precisely one neighbour, because a,b are adjacent), or both complementary colours.

In the first case the γδ component of that neighbour is confined to A, changes the only γ link occurrence, and introduces no γ elsewhere on either side link.

In the second case, the proof first attempts the component that removes γ directly. If that lock exists, the opposite disjoint-colour lock is absent. Its swap removes δ from A and leaves B unchanged. When B still contains δ, it contains δ at exactly one of its two adjacent strict-side neighbours. In the new colouring the γδ component of that neighbour is globally confined to B because p,q are outside the colour pair. It changes the unique δ on the B link to γ. Any other vertices it changes were not γ-coloured B-link vertices before this swap; γ was absent from that link. Thus no δ is introduced back onto the link. A remains unchanged and both links now omit δ.

This verifies the crucial sequential step: the final component is defined after the preceding swap, and no persistence of an earlier component is asserted. The reflected ordering of a,b exchanges the two locks and is valid. Every selected component avoids p,q, so the boundary colours used to define the complementary pair stay fixed throughout. The total cost is at most one initial swap plus two finishing swaps.

The path consequence is also correct: a first slide to this separator vertex can be lifted from an interior source because singleton legality depends on the source neighbourhood; the balanced fixed-hole theorem then finishes. The theorem does not imply an admissible degree-five root or fan exists by itself.

## Thin-side transfer

Accepted for each fixed proper deletion start: κ_B≤κ_T≤κ_B+1 when κ_B is finite, and finiteness is equivalent.

Projection of each global swap is zero or one genuine B swap, so a global fill projects to a B fill. Conversely each chosen B component lifts to its unique global component. The lift may recolour p,q and strict A vertices; the proof correctly uses their current colours after the lifted B path. Once B fills, a missing colour η differs from both current boundary colours. If the sole strict-A link neighbour a has colour η, swapping its component in the two complementary colours is confined to A and changes the only A-link occurrence of η. Otherwise no extra swap is needed. No prescribed boundary colours or arbitrary extension of a B colouring is assumed.

The statement is about the restriction of a given global start. It must not be promoted to a universal assertion about every B colouring unless its extension to A is separately justified. The report does not make that promotion.

## Nested triangle and source rerouting

Accepted: when the thin-side unique interior neighbour a has global degree at least five, the triangle paq has vertices on both sides. The degree-three star of f accounts for one side; a's additional neighbours, confined to A, lie on the other. Therefore a degree-five source at a is already on a separating triangle and fills by the accepted two-swap theorem before taking any proposed slide onto f. This works even when f has larger degree.

The structural failure corollary follows because that degree-five vertex provides a good pair directly. It does not assert that all unbalanced degree-six targets or higher-degree targets are fillable.

## Outcome

All four sections accepted as hand arguments with the report's stated spherical no-crossing premise and scope. No correction was needed. The balanced theorem narrows the ordinary boundary-landing problem; it does not discharge the protected-face condition in VH_C.

## Addendum: degree-four side with arbitrary other degree

The later §3a is accepted as a hand theorem. For d_A(f)=4 and d_B(f)=d, the same A-side repair either removes the B-missing complementary colour γ, or removes the other complementary colour δ from A. In the latter case swap every B γδ component meeting a δ-coloured B-link vertex. The pair-induced graph and its component partition are unchanged by γδ swaps, so these are sequential actual whole components; there is no hidden assumption that arbitrary Kempe components persist after a different-pair swap. Boundary p,q are outside the pair and every selected component stays in B.

Since no B-link vertex initially has γ, the swaps introduce no δ on that link. The δ vertices form an independent set on the d−2 strict-B-neighbour path, giving at most ceil((d−2)/2) components. Therefore κ_B≤κ_T≤κ_B+1+ceil((d−2)/2), and pure-fill existence is equivalent for the fixed global start and its B restriction. The scope restrictions in the initial review remain: no universal boundary-colouring extension and no mixed path landing theorem are implied.
