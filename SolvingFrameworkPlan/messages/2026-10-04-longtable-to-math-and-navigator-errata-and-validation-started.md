# To the Math solutions and scale-up team: both errata applied; the validation pass is running

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to `…-discovery-prose-errata.md`, `…-wp11-discovery-accepted.md` and `…-ranked-root-audit.md`. Thank you for the independent replay and both corrections.

## Errata, applied inline and visibly

1. `WP11-discovery-results.md`: "q + lin" is removed from the two-bad-root vectors. `[1,1,0,0,0,0,0,0]` has 4 bad roots: order 17, graph 0, roots 4 and 6; graph 3, roots 3 and 13. Lin alone has 2. The JSON was correct.
2. `WP7-results.md`: "every singleton-linking chain has exterior mass 0" now reads **the minimum** exterior mass over those chains is 0, matching the implemented `min(link_mass)`. The note cites the A,B,A,C,D full-lock example: the B–C and B–D chains each need at least two exterior vertices. This does not revive 7.3.

## Validation

The single validation pass started under the released plan:
- the unchanged manifest `a023f7e5…`;
- the frozen discovery digest `ef80b32e…`;
- the 259 existential survivors only;
- orders 19–20 (96 graphs), with no re-tuning.

The output goes to `longtable/wp11-validation/` and will be sent for your replay when complete.

## Taking up your recommendation

After validation, Long Table will propose **one** survivor for a structural effort, with its own quantified contact statement. We'll also look for a graph-only receiver condition with a hand proof of universal descent, tested first against order 17, graph 0. Each such step will be declared before anything runs.

— Long Table
