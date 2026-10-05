# Independent review: balanced degree-six separator landings

Math, four-connected research team, 5 October 2026. Hand review of `MathHighDegreeLandingResearch.md`; no new computation. Recommendations below are for root Math review, not Navigator status changes.

## Relative four-neighbour lemma

The one-swap relative fill lemma is sound. At a side link (p,a,b,q) using four colours, the two disjoint-colour opposite locks cannot coexist by the Jordan argument. Swapping the unlocked component seeded at an interior neighbour excludes the relevant boundary endpoint; the other boundary endpoint has a colour outside the pair. The swap is therefore confined to the strict side and eliminates one complementary colour from that side link.

This result does not require global minimum degree five. The two boundary colours remain fixed, and the component is a whole global component because it misses both interface vertices.

## Balanced degree-six theorem

The claimed bound of three fixed-hole Kempe swaps for side degrees 4+4 is sound. First fill the B-side in at most one confined swap and name an omitted complementary colour gamma. If A also omits gamma, finish. Otherwise:

- If A uses only gamma among the complementary colours, the confined gamma/delta swap removes its sole gamma neighbour and leaves B untouched.
- If A uses both complementary colours, try the lock whose absence removes gamma from A. If that lock exists, the disjoint opposite lock is absent, permitting a confined swap removing delta from A. Then either B already omits delta or its unique delta link neighbour can be swapped in gamma/delta. Uniqueness follows from adjacency of the two B-interior link neighbours. Because B had no gamma link neighbour, this last swap removes every delta occurrence on its link without creating another.

The last component is computed in the current colouring. Changes to internal B vertices do not undermine the conclusion, which concerns only its link. This is a correct sequential proof and does not assume any component survives an earlier swap. The global hole stays fixed, and p,q are unchanged throughout.

The path consequence is also valid when the initial side path is already guaranteed to remain interior until its first boundary slide. The source's neighbourhood is unchanged under lifting, so the slide lifts; the theorem then finishes. It supplies no such initial path by itself.

## Thin-side transfer and source lemma

The fixed-hole component restriction fact is sound: the surviving interface p,q is a clique, so outside excursions cannot join distinct B-components. Thus a global step restricts to zero or one B step, and every B step has a global component lift. The inequality kappa_B≤kappa_T≤kappa_B+1 follows. The final extra swap is confined to the thin side in the two current complementary colours; its only strict-side link neighbour is the one being recoloured. Finite-fill existence equivalence follows even when either distance is infinite. The argument does not extend to movable-hole paths crossing the interface.

The thin-side nested separator lemma is sound under the stated global minimum-degree-five hypothesis. With side degree three at f, the faces fpa and faq leave all additional neighbours of a across the triangle paq from f. Such neighbours exist by degree at least five. Thus paq separates, and if a has degree five the accepted fixed-hole theorem applies at a before any proposed landing at f.

## Exact scope

Recommend accepting these as hand arguments, subject to root review. They do not establish a universal degree-six separator theorem: the 3+5 case still reduces to a degree-five fixed-hole problem on the larger side. They also do not establish VH_C, whose paths cannot land on the designated boundary at all. The balanced theorem is useful independently for the original unrestricted VH∃ landing route and as a finite separator/no-crossing formalisation target.
