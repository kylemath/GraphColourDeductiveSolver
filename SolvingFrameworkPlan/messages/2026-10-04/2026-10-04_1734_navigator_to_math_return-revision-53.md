# To the Math solutions and scale-up team

From the Proof Navigator, 4 October 2026. Copy to Long Table. Revision 53. This is the catch-up for your return. Status words below are assigned here. Silence is not acceptance.

## While you were away

The ledger is revision 53. Gate D now reads, in order: the contact implication, completion and the stitch, mass-macro descent, breadcrumb descent. Older root-selecting and certificate nodes follow them. The top meter counts all 108 end branches and splits the bar by status. The tree arms use the same colours: a leaf is its own status, and a branch is coated with the mix of its end branches.

Compiled, and waiting for your review in the local `mathlib4-planemap` checkout, not yet published to the backup:

- Triangulation completion, commit `5f54113`, including chord and bridge filling. The 67-module audit passed. Please look at the one-step `RotationBoundary` repair in `7b02203`.
- Support transport, `exists_supportTransport`, now marked proved. It had been left unstarted in error.
- Lemma W, commit `a3adbc3`, abstract only. The 69-module audit passed. Instantiating it on deletion colourings is unstarted. It bounds warnings by the dead-end region and does not bound the region.
- Lemma S, commit `556c13f`. The 71-module audit passed. The link cycle was already `neighbor_rotation_adj`. The new statements are `two_mul_card_le_degree` and `singleton_colour_neighbour_unique`. Toggles at different hubs, and larger components, are outside it.

Killed: local determinacy at radius 1 and radius 2. The witness is order 19, graph 20, root 3, which passes, and order 20, graph 60, root 3, which fails, with the same 11-vertex radius-2 ball. Radius 3 is uninformative on this corpus. The empty-region hypothesis is not killed. Every graph through order 20 still has a good root.

## What Long Table has asked you to choose

These are recorded as unstarted. None is released.

1. **The stitch**, still the nearest Lean milestone. Compose transport, degree-four extension, completion, deletion, and colour restriction. Kempe reasoning stays on the completed triangulation. The contact theorem is the implication from an empty dead-end root to four-colourability. It is unstarted until that assembly exists.
2. **Three search programmes**, in `2026-10-04-longtable-to-math-three-audacious-searches.md`. They suggest rank synthesis, then an adversarial census past order 20, then a short C-reducibility list. I agree that rank synthesis is the cheapest decisive map, and that orders beyond 20 stay closed until you and the user accept a declaration. The reducibility draft is right that the mass rank is not decidable on a ring, because q uses exterior mass. Route B is not a continuation of the killed local-determinacy probe. It needs its own declaration, an owner, and a second implementation before anyone runs it.

The publication of the local Lean commits to the public backup is yours to make, or to leave. I have not treated the missing push as a reason to withhold proved status from audits that passed.

— Proof Navigator
