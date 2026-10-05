# Ranked contact and structural obstruction report

4 October 2026. Fresh source rebuild: **79/79 passed**. All previous 75 source hashes remain unchanged. The four added sources contain fourteen exact guarded axiom reports, using only the standard axioms. No general Four Colour result is claimed.

## Checked Lean contributions

`SphericalRankedContact.lean` accepts a fixed natural-number rank family before the graph/root/colouring quantifiers. Universal endpoint descent at one graph-chosen degree-five root implies four-colourability through the existing support induction and triangulation completion. The universal premise remains explicit and unproved. An actual target path uses at most the initial rank many macros. Scalarization `(B+1)p+s`, with both secondary coordinates bounded by B, exactly matches lexicographic comparison; if p≤1 the rank is at most `2B+1`. These count macros, not solver operations.

`SingletonExterior.lean` proves a carrier-independent structural fact: a unique boundary colour connected to another boundary colour, with no boundary exit in that pair, forces two distinct exterior vertices in the component. The proof takes the first two edges of a simple bichromatic path. A four-vertex path checks sharpness.

For an induced five-cycle coloured A,B,A,C,D at a full singleton lock, this forces exterior vertices in both B–C and B–D chains. The two pairs need not have disjoint exterior sets. This explains why zero minimum singleton-link mass does not mean every singleton link has zero mass. It does not distinguish good roots from bad roots.

## Independent discovery review

The unchanged WP11 discovery output passed independent replay: 279 root tables, 22,802 proper colouring orbits, all 479 registered vectors, complete indexed macro evidence, and provenance. There are 259 existential survivors and zero all-roots survivors. The fixed validation phase was released under the user's existing approval. Its output still requires independent replay.

Two prose errata were posted separately: q+lin has four bad roots rather than two; WP7's zero statistic is a minimum rather than a claim about every singleton link. Neither affects the accepted certificates or revives Conjecture 7.3.

## Next mathematical boundary

The companion `RootQuantifierAudit.md` separates graph-level rank/root selection from statewise switching. A lower-envelope rank needs descent of an active minimum, not merely some decreasing feature. The degree-five/six order-17 graph already kills charging every bad root to degree-seven curvature. A reversible vacancy slide preserves properness, but its singleton destinations can all have degree six. A constructive selector, universal descent, warning bound and polynomial solver remain open.
