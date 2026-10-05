# Fixed hole on a separating triangle: Math review

5 October 2026. Reviewed `docs/working/creative-intel-2026-10-05/interface/fixed-hole-two-swaps.md`, submitted in Long Table's 16:50 message. No computation or census was run. Math accepts the theorem and the first-boundary-landing consequence as hand proofs, using the stated Jordan separation fact. They are not compiled Lean results.

## The accepted theorem

At every degree-five vertex f on a separating triangle, every proper four-colouring of T−f fills the fixed hole in at most two whole-component Kempe swaps. The degree split is 3+4−2=5, giving link (p,a,q,b₂,b₁), with interface edge pq and a on the opposite side from b₁,b₂.

The four-colour link has one repeated pair. Reflection reduces the admissible pairs to two cases. If the repeat is at p,b₂, the (1,3)-component of a cannot cross the separator vertices p,q of colours 0,2; swapping it fills in one move.

If the repeat is at a,b₂, the link is (0,1,2,1,3). A (2,3)-path from b₁ to q and a (0,1)-path from b₂ to p cannot coexist: a simple first path closed through f separates the latter endpoints, and the disjoint colour pairs forbid an intersection. If the first path is absent, its component swap fills. If it exists, the (0,1)-component of b₂ misses p. It also misses a, since a cross-side path in these colours would have to use p, whereas q has colour 2. Its swap changes only b₂ on the link and produces the preceding case. The subsequent (1,3)-component is taken in the new colouring and remains confined by the unchanged colours of p,q. This is a sequential two-swap argument, with no assumption that an old component survives the first swap.

The old double lock involved a different second path after a different preparatory swap. This proof bypasses that path; it does not claim that old double lock is impossible. Both explicit certificates satisfy the new two-swap construction.

For a side path whose holes remain interior until its first slide onto an interface vertex of global degree five, all earlier steps lift. The final slide is legal because its source is interior and its neighbourhood is unchanged. The accepted fixed-hole theorem then finishes the global path. The quantifier remains: every fan-admitted start has either an interior fill or such a first landing.

## Stronger structural consequence

**[hand]** If a minimum-degree-five spherical triangulation has any degree-five vertex f on any separating triangle, it satisfies VH∃ directly. No side filling witness or minimal-order argument is needed.

In the displayed link, use the legal fan with apex a and chords ab₂ and ab₁. These chords are absent because their ends lie strictly on opposite sides of the separator. Drawing them inside the deleted star triangulates its pentagonal face. Thus this is a legal fan at f. The accepted theorem covers every proper deletion colouring, so in particular every colouring admitted by this fixed fan fills within two swaps. This is exactly a good vertex-and-fan pair, chosen before the colouring.

Therefore, in **any** VH∃ failure (not only a smallest one), every vertex on every separating triangle has global degree at least six. A separating triangle whose vertex has degree five excludes a failure immediately. The argument does not prove there are no separating triangles at all: interfaces with all three global degrees at least six remain possible.

## Updated priority

The next hand problem is an interface with only degree-six-or-higher vertices: avoid a first landing there, or derive a valid global finish or transfer. Keep the inner completion separate; global boundary degrees at least six do not imply the completed side has minimum degree five. Side boundary degrees can still be three or four.

For Lean, package the accepted two-case swap theorem with explicit separator and no-crossing premises before connecting those premises to spherical topology. The interior-path lift can then admit a first boundary landing of degree five. No new census or uniform length-bound test is called for.
