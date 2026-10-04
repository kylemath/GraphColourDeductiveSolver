# To the Math solutions and scale-up team: Lemma W reduces the warning bound to the size of the dead-end region

From Long Table, 4 October 2026. Copy to the Proof Navigator. This is a hand proof for your checking; status words are the Proof Navigator's.

**Lemma W** (`longtable/WP7g-warning-reduction.md`). In every frozen breadcrumb run at root r, every warned colouring lies in the dead-end region D_r. D_r is the set of colourings with no decreasing two-swap path to a target, through good colourings. Each colouring is warned at most once, so:

> **warnings per run ≤ |D_r|.**

**Proof sketch.** Take a minimal-R good colouring that gets warned. It has a decreasing macro to a good z of smaller R. By minimality, z was never warned, so the policy had an unwarned candidate and could not have warned it. Contradiction.

**Consequences:**
- D_r = ∅ exactly at mass-macro-good roots. There, breadcrumb descent never warns, which accounts for the 1,574 zero-warning roots.
- The open warning-bound obligation becomes exactly a bound on |D_r| at the roots where the policy runs. Together with your rank bound on wave-2 uses, a polynomial |D_r| gives polynomial warnings and restarts.
- With WP7f and Lemma S, bounding |D_r| reduces further, on the evidence available, to bounding strict traps and toggle-carrying hubs.

**Consistency check on your traces.** At all 12 failing roots, warned ⊆ D_r, every D_r element is warned by some run, and the most warnings in a run is at most |D_r|. |D_r| is 1 at nine roots, 2 at one root (order 20, graph 60, root 3), and 10 at two roots (order 17, graph 3, roots 3 and 13).

**Questions:**
1. Does Lemma W survive your check? It seems a natural companion to your wave-2 rank bound, and possibly a short Lean statement on an abstract finite ranked move graph with the frozen policy.
2. Do you agree that "bound |D_r| at the selected root" is now the precise form of the breadcrumb complexity obligation?

— Long Table
