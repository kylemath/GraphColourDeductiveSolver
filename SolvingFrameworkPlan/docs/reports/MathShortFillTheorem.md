# Two mixed moves can be replaced by Kempe swaps

Math, 5 October 2026. Accepted hand theorem, derived by the Math root and independently reviewed by both parallel teams. This settles M3, with stronger scope than its WP19 formulation. The frozen experiment continues unchanged; its M3 observations are reported separately from this proof.

## Statement

Let G be a finite simple graph and C a finite colour palette. Start with a proper colouring c of G-h. A **target** has a current hole whose neighbour colours omit at least one member of C. A **slide** h→u transfers c(u) to h and makes u the hole; it is legal when c(u) occurs exactly once among the neighbours of h. A **Kempe move** exchanges two colours on one whole connected component of their induced graph in the current deletion. Singleton components are allowed.

Let ℓ be the minimum number of mixed moves to a target, allowing the hole to move. Let κ be the minimum number of Kempe moves to a target at the original hole h. Then

**If ℓ≤2, then κ=ℓ.**

No planarity, fan, triangulation, degree restriction or four-colour assumption is used. In particular, the WP19 assertion ℓ=2⇒κ=2 is a theorem.

## Terminal-slide lemma

Suppose a slide z→w carries colour α and reaches a target at w. Choose a colour x missing from the new link. The newly coloured neighbour z has colour α, so x≠α. In the original deletion G-z, no coloured neighbour of w has α, by properness, or x, by the missing-colour condition. Thus {w} is a whole {α,x} component. Swap it: w changes from α to x, removing the unique α from the original link of z. One Kempe move therefore gives a target at z.

## Paths of length two

If the start or an intermediate state is already a target, the claim follows from zero moves or the terminal-slide lemma. Otherwise consider a two-move target path. KK already consists of two Kempe moves. KS becomes KK by terminal-slide elimination. SS becomes SK by eliminating its second slide at the intermediate hole. It remains to treat SK.

Write the first slide as h→u, carrying the unique link colour σ=c(u). In the intermediate deletion G-u, h has colour σ. Let the second move swap pair P on whole component K, and let x be a colour omitted from the final link of u.

**P avoids σ.** The P-induced graphs before and after the slide are identical: u and h have colour σ and are excluded in their respective deletions. Commute the swap before the slide. The slide remains legal because σ occurrences are unchanged. Eliminate this now-terminal slide to obtain two Kempe moves at h.

**P={σ,ρ}, and x lies outside P.** The swap changes no x occurrence, so x was already absent from the originally coloured neighbours of u. Properness excludes σ there too. Recolour the singleton {u} from σ to x: the original h-link loses its unique σ and fills in one Kempe move.

The remaining cases have x∈P.

**h∉K.** The final h-colour is σ, so x=ρ. Every original ρ-neighbour of u belongs to K, since otherwise it retains ρ on the final u-link. If u has none, its original {σ,ρ} component is the singleton {u}, whose swap already fills at h. Otherwise K∪{u} is a whole original {σ,ρ} component: removing h leaves K unchanged and adding u joins it through the nonempty set of ρ-neighbours, all in K. No original ρ-neighbour of h is in K, because it would connect K to intermediate σ-coloured h. Swap K∪{u}; u changes to ρ, no other h-neighbour becomes σ, and h fills in one move.

**h∈K.** The final h-colour is ρ, so x=σ. No original ρ-neighbour of u lies in K, since it would become σ on the final u-link. Properness excludes original σ-neighbours of u. Consequently K−{h} is a union of whole {σ,ρ} components in G-h: deleting h can split K, but restoring u cannot attach any resulting piece. Every original ρ-neighbour of h lies in K−{h}, being directly adjacent to intermediate σ-coloured h. The original {σ,ρ} component J containing u is therefore disjoint from all those ρ-neighbours. Swap J. The unique σ on the original h-link, at u, becomes ρ; no ρ-neighbour of h becomes σ. Again h fills in one Kempe move.

Thus every SK target path either converts to two Kempe moves or collapses to one. This completes all four move types. Since mixed moves include Kempe moves, ℓ≤κ; the constructed replacements give κ≤ℓ for ℓ=0,1,2, proving equality.

## Review and computational consistency

Team A independently verified the initial degree-five proof and its component premises. Team B independently verified the stronger one-component escape that removes the degree bound. The Math root reviewed both and supplied the final branch correction when u has no ρ-neighbour. Reviews are `longtable/audit/team-a-m3-review.md` and `team-b-m3-review.md`.

The separate constructive check `longtable/audit/math_m3_review.py` uses only independently implemented moves and four existing fixtures (12:0, 14:0, 17:0, 17:1). It checks 1,378 four-colour starts and 8,284 SK target paths: 5,744 containing the slide colour collapse to one original Kempe move; 2,540 others commute and convert to two. All 396 SK paths from starts without a one-move fill fall in the commuting case. These checks corroborate the hand argument; they are not its proof and introduce no new census.

This result does not bound ℓ globally, settle M1/M2, prove VH∃, or extend equality to distance three. Canonical colour renaming in computational paths must be lifted to consistent actual labels before applying the argument.
