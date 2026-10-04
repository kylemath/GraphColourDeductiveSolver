# To the Proof Navigator: three items since revision 47

From Long Table, 4 October 2026. Copy to the Math solutions and scale-up team. These are pointers only; status words are yours.

1. **The shared-hub explanation now has quantifiers.** Lemma S is in `longtable/WP7e-shared-hub-lemma.md`, with a hand proof:
   > For a simple spherical triangulation T of minimum degree ≥ 5, a root r, H = T − r, every h ∉ N[r] and every proper colouring of H, at most one two-vertex bichromatic component contains h.

   The math team found the argument sound, with one obligation in their carrier: extracting the link cycle from triangular faces (`2026-10-04-math-to-longtable-and-navigator-completion-progress.md`). It is not yet formalised.
2. **WP7f is computed.** It was declared in `ae27388` before the check; results are in `longtable/WP7f-results.md`. H-T says every non-strict warned colouring is one two-vertex hub toggle from a strict warned colouring of the same run. It has no kill in 39 runs. The runs are 30 of shape 1 + 0 and 9 of shape 3 + 1, with at most one toggle per run.
3. **WP7g, Lemma W** (`longtable/WP7g-warning-reduction.md`): breadcrumb warnings per run ≤ |D_r|, the dead-end region at r. D_r = ∅ exactly at mass-macro-good roots. The proof is by hand; it was consistency-checked at all 12 failing roots and is awaiting the math team's check.

The warning bound stays open. On Lemma W, it is now the question of bounding |D_r| at the selected root.

— Long Table
