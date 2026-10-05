# Math: degree-six landings on a separating triangle

5 October 2026. Author: Math / high_degree_landings. These are hand proofs for review, not compiled results. No census, graph generation, or colouring enumeration was run. The accepted degree-five theorem is in `MathFixedHoleReview.md`; the new face-avoiding hypothesis bypasses boundary landings and is a separate route. The results here support the original VH∃ route.

## Setting and component facts

Let T be a finite simple spherical triangulation, F={f,p,q} a separating triangle, and A,B its closed triangulated sides. They meet exactly in F, with no edges between their strict interiors. Keep the hole at f. A proper four-colouring of T−f assigns distinct colours α,β to p,q. Name the other two colours γ,δ.

Every side-to-side path in T−f meets p or q. Consequently a bichromatic component that lies on one side and avoids both p,q is a whole component of T−f. Its swap is legal globally and changes nothing on the other side. This applies even if its colour pair contains one boundary colour: the component must then be shown to miss that boundary vertex.

The restriction to B of a global bichromatic component is empty or one whole bichromatic component of B−f. To see uniqueness, any excursion outside B has its endpoints in {p,q}. If both are active, the edge pq connects them inside B; if only one is active, an excursion returns to that same vertex. Replace every excursion by that edge or by a stationary segment. Thus any two B vertices in the global component are joined inside B. Conversely a component of B−f seeded at a B vertex is the restriction of its global component. These are fixed-hole projection and lift facts; they do not move a hole onto F.

## 1. Relative four-neighbour fill

**[hand] Lemma.** Suppose f has side-degree four in A, so its A-link is the cycle (p,a,b,q). From any proper colouring of A−f, at most one Kempe swap whose component avoids p,q fills that side's link.

If at most three colours occur, do nothing. Otherwise name the colours at (p,a,b,q) as (α,γ,δ,β). The two potential locks are an {α,δ}-path from p to b and a {γ,β}-path from a to q in A−f. They cannot coexist: their endpoints alternate around the deleted star, and their colour sets are disjoint. More explicitly, close a simple first path through f using fb and fp. The Jordan curve separates a and q, and the second path cannot intersect the first or f. This is a contradiction.

If the p-to-b lock is absent, swap the {α,δ}-component of b. It avoids p; q has colour β and is outside the pair. Only b among the four link vertices changes, from δ to α, eliminating δ. If the a-to-q lock is absent, swap the {γ,β}-component of a, similarly eliminating γ. The selected component avoids p,q and therefore the same swap is confined to A's strict interior in T−f.

The no-crossing premise is the usual embedded-cycle argument, applied in the spherical completed side A. No assertion about old components surviving later swaps is used.

## 2. Balanced degree-six separator: three swaps suffice

**[hand] Theorem.** If f has global degree six and side degrees d_A(f)=d_B(f)=4, every proper four-colouring of T−f fills the fixed global hole in at most three Kempe swaps. All selected components avoid p,q, so their colours are preserved throughout.

Write the A-link as (p,a,b,q) and the B-link as (p,c,d,q). Apply Lemma 1 to B, using zero or one globally legal swap. The B-link now omits one complementary colour, call it γ. It still contains the boundary colours α,β. If the global link already omits γ, stop.

Otherwise an A-interior neighbour has colour γ. There are two possibilities.

**Only one complementary colour occurs among a,b.** The other neighbour has a boundary colour α or β. Swap the {γ,δ}-component of the γ-coloured neighbour in A−f. It avoids p,q; the other neighbour is outside the colour pair. It changes the only γ on the A-link to δ. Since B has no γ on its link and remains unchanged, the global link now omits γ. This costs one additional swap.

**Both complementary colours occur among a,b.** Suppose first (a,b)=(γ,δ). Consider the a-to-q {γ,β} lock. If it is absent, its component swap changes a from γ to β without changing any other A-link vertex or anything on B. This fills the global hole by omitting γ.

If that lock exists, the disjoint-colour crossing argument shows the b-to-p {δ,α} lock is absent. Swap the {δ,α}-component of b. It avoids both boundary vertices and changes b to α, so the A-link now omits δ. If B also omits δ, stop. Otherwise δ appears at exactly one of c,d: they are adjacent, so cannot both have colour δ, and p,q have the other two colours. In B−f swap the {γ,δ}-component containing that δ-coloured neighbour. It avoids p,q. There was no γ on the B-link, so this swap sends the only δ on that link to γ and introduces no δ there. A is unchanged. Now both side links omit δ, and the global hole is filled.

If (a,b)=(δ,γ), exchange the roles of the two opposite locks: first try the b-to-p {γ,α} component; when it is locked, the a-to-q {δ,β} component is unlocked. The same two-step finish applies, with its actual components recomputed in the colouring on which each swap acts.

There are at most one initial B swap and two subsequent swaps, hence at most three. Internal γ-vertices in B cause no problem: the final swap can exchange them with δ, but none was a B-link vertex before that swap. Only the link trace matters for the claimed elimination.

**[hand] Path consequence.** An interior path that first reaches F by a slide onto such an f can be lifted up to that slide and then finished by at most three Kempe swaps. Its source is interior, so the slide's singleton condition has the same neighbourhood in the side and in T. This extends the accepted degree-five landing consequence to the balanced degree-six case. It does not by itself provide a good degree-five root.

## 3. A thin side gives exact pure-fill transfer

**[hand] Theorem.** Suppose d_A(f)=3, with A-link (p,a,q). For a fixed proper deletion start c, let κ_T be the minimum number of pure Kempe swaps filling f in T, and κ_B the corresponding minimum for its restriction to B. Finite distances satisfy

    κ_B ≤ κ_T ≤ κ_B + 1.

Moreover κ_T is finite exactly when κ_B is finite.

For the lower bound, restrict a global filling path to B. The component restriction fact turns each global step into zero or one genuine B step. A global fill is also a B fill.

For the upper bound, lift a shortest B filling path to T by swapping each global component containing the selected B seed. Component restriction ensures that the B trace follows the prescribed path, even if vertices in A also change. Once B fills, it omits a colour η. Since p,q are adjacent, η is one of the two colours complementary to their *current* colours. If a does not have colour η, T already fills. If a does have colour η, swap its component in the two complementary colours. This component misses p,q and stays in A's strict interior. It changes the only A-link occurrence of η, namely a, to the other complementary colour. B's link remains unchanged and the global link omits η. This costs at most one additional swap.

For a degree-six f with split 3+5, this reduces fixed-hole pure fill to the ordinary degree-five fixed-hole problem on B. It does not solve that problem, supply a uniform bound, or justify extending the balanced theorem to every degree-six interface vertex. B need not have minimum degree five at its other boundary vertices.

## 3a. Pure-fill transfer also holds for a side of degree four

**[hand] Theorem.** Suppose d_A(f)=4, with A-link (p,a,b,q), and let d=d_B(f). For any proper deletion start, fixed-hole pure-fill existence in T is equivalent to fixed-hole pure-fill existence in B. When κ_B is finite,

    κ_B ≤ κ_T ≤ κ_B + 1 + ceil((d−2)/2).

The lower bound is the same component-projection argument. For the upper bound, lift a shortest B filling path to T. Rename the current colours at p,q as α,β and their two complements as γ,δ; the lifted path was allowed to change the boundary colours. Choose γ to be a colour now omitted by B's link. If the global hole does not fill, A has a γ-coloured interior neighbour.

Apply exactly the A-side argument of Theorem 2. Either one confined swap eliminates γ from A, completing the global fill; or one confined swap eliminates the other complementary colour δ from A. In the latter branch, B still omits γ but may have more than one δ-coloured link vertex. Swap each B-component in the pair {γ,δ} that contains such a δ-coloured link vertex. Every component avoids p,q and remains entirely on B's strict side. Before these swaps there is no γ on B's link, so each selected component eliminates all of its δ-link occurrences and introduces no δ there. The {γ,δ} active vertex set, induced graph, and component partition remain unchanged under these swaps, so components may be selected sequentially without altering the others.

The d−2 strict-B neighbours form a path. Its δ-coloured vertices form an independent set, of size at most ceil((d−2)/2). There are at most that many selected components. Thus the repair costs at most one A swap plus ceil((d−2)/2) B swaps. Both links then omit δ.

This covers arbitrarily large global degrees without relying on a singleton at the global hole. Its premise is still a genuine pure fill on B, not merely a mixed side path. A mixed side path that moves onto the interface is not covered by this theorem.

For d=4, Lemma 1 gives κ_B≤1 and the bound is three, as in Theorem 2. For d=3 it gives at most two, reproducing the accepted degree-five separator bound. For d=5 it gives κ_T≤κ_B+3, but finiteness of κ_B at an arbitrary degree-five deletion remains unresolved here.

## 4. A degree-five source cannot get trapped through a thin side

**[hand] Lemma.** Assume T has minimum degree five and d_A(f)=3, with unique strict-A neighbour a. Then {p,a,q} is itself a separating triangle. In particular, if a has global degree five, it already satisfies the accepted two-swap fixed-hole theorem.

The triangles fpa and faq fill the portion of the A-disc between the boundary fpq and the cycle paq. All other A vertices and every additional neighbour of a lie on the opposite side of paq from f. Such additional neighbours exist: a has degree at least five, while only f,p,q are among the named vertices. The other side contains f and the strict B interior. Thus both sides of paq contain a vertex, and paq is separating.

If a side path with its current hole at a of degree five proposes the slide a→f through this degree-three side, replace that slide and the rest of the path by the accepted two-swap fill at a. The hole stays fixed. This works for any global degree of f, and requires no classification of the colouring produced by the proposed slide.

**[hand] Structural corollary.** In a VH∃ failure, the sole interior neighbour on a degree-three side of any separator vertex has degree at least six. Otherwise that neighbour is a degree-five vertex on the nested separating triangle and gives a good pair directly, by `MathFixedHoleReview.md`.

## Remaining obstruction and relevance to VH∃

These results narrow the original boundary-landing gap:

- Degree-five separator targets: already handled in two swaps.
- Degree-six targets with split 4+4: now handled in three swaps.
- Degree-six targets with split 3+5: fixed-hole existence reduces exactly to the degree-five problem on the larger side. A degree-five source entering through the thin side is already fillable before landing.
- Higher degrees and other entries through an unbalanced side remain open.

More generally, a completed side of boundary degree three or four is not an additional obstruction to pure-fill existence: that existence is equivalent to the other side's, with the explicit additive repairs in §§3–3a. This equivalence concerns the boundary hole f; it does not assert that an interior good pair remains good after a mixed path reaches f.

None of the arguments changes the quantifiers in VH∃, assumes a slide is available after reaching a large hole, or proves that every degree-six vertex on a separator is good. In the new face-avoiding route, holes are forbidden on the designated face, so Theorem 2 is not a substitute for the face-avoiding hypothesis. It is an independent fallback for unconstrained side paths and a concrete local theorem suitable for the same separator/no-crossing Lean interface as the accepted degree-five theorem.

The thin-side transfer also identifies a dead end: proving a universal degree-six theorem by treating the degree-three side as a harmless buffer would still require solving the degree-five fixed-hole problem on the other side. No new census is suggested here.
