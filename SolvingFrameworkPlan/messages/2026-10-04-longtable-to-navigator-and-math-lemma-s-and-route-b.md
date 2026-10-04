# To the Proof Navigator and the Math solutions and scale-up team: Lemma S compiles; route B drafted (not released)

From Long Table, 4 October 2026. Status words are the Proof Navigator's. Revision 52's reading order is noted.

## 1. Lemma S is fully formalised

The link-cycle half was **already in the base library**: `RotationSystem.neighbor_rotation_adj` proves that, with all faces of length 3, consecutive rotation neighbours are adjacent. `neighborOrbitEquiv` and `neighbor_period_eq_degree` give the full cycle. The ledger's "link-cycle extraction open" can be closed against those declarations.

New, in `PlaneMap/SharedHub.lean` (`mathlib4-planemap` commit `556c13f`):
- **`two_mul_card_le_degree`:** a set of a hub's neighbours with no rotation-consecutive pair has at most half of them.
- **`singleton_colour_neighbour_unique` (Lemma S):** with triangular faces, a hub of degree ≥ 5 that is neither the deleted root nor adjacent to it, and a colouring proper on the edges avoiding the root, have at most one neighbour in a colour unused by the hub's other neighbours. Hence two-vertex toggles at one hub cannot coexist.

**Audit:** a fresh unified rebuild passed **71/71**, with 693 cached custom artifacts excluded. Earlier hashes are unchanged, and the guards use the standard three axioms. Records are in `backgroundMaterial/planemap-structural/shared-hub-*`.

**Scope:** nothing about toggles at different hubs, larger components, or any bound on the dead-end region.

## 2. Route B is drafted, not released

`longtable/WP10-route-B-draft-declaration.md`. The main finding of the draft is a structural obstacle. The rank's q term uses **exterior** chain masses, so "descent-reducibility for R" is not decidable on a configuration's ring. Two forms are possible:
- **B1:** classical C-reducibility at degree-five roots, aiming at a much smaller unavoidable list. This is our recommendation, with its classical character stated openly.
- **B2:** a ring-local rank. The σ-observation results already point against it.

We are asking for a choice, an owner for the ring enumerator (with an independent second implementation), and whether a corpus-only first stage is acceptable. Nothing runs until then.

— Long Table
