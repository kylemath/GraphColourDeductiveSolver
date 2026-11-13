# Can the rules be a few operations in a richer space? (FAM-1, 12 Nov 2026)

Light analysis, one tool, nothing here is a proof claim. Code: `code/ops.py`, `code/tworound.py`, `code/build_atlas.py` (family tree). Earlier evidence: `FABLE_IDEAS.md`, `REPORT.md`.

## What the family tree says

Nearest-relative tree over mirror pairs (Atlas, "Family tree" tab). Branch = number of nodes that differ.

| proof | rules | branches of 0-1 node | 2 nodes | 3-4 | 5 or more |
|---|---|---|---|---|---|
| RSST / Coq | 38 | 3 | 8 | 19 | 7 |
| Inoue 2026 | 43 | 2 | 14 | 19 | 7 |
| Outside 588 | 308 | 21 | 30 | 116 | 140 |
| Outside 854 | 42 | 3 | 9 | 21 | 8 |

So single swaps exist but are the minority: in the 588 proof 51 of 307 branches are 1 or 2 nodes, and 140 are 5 or more. The rules are closer to isolated points than to one connected family.

## Which swaps recur (pairs of rules 1 or 2 nodes apart)

588 proof: 77 pairs, 138 node changes, 30 distinct swap types. The top five cover 55%:

| swap | count |
|---|---|
| fan vertex: 6 vs 7 or more | 31 |
| fan vertex: 5 vs 6 or more | 14 |
| fan vertex: 5 vs 7 or more | 12 |
| hat vertex: 5 vs 6 | 10 |
| hat vertex: 6 vs 7 or more | 9 |

These are complement pairs: the two rules are the two answers to one yes/no question about one outer vertex ("is it at least 6?", "is it at least 7?"). Near relatives are case splits, not variations. In RSST the dominant swap is different: "spoke: any vs 5" (5 of 22), i.e. adding one condition.

## Footprint test (two nearest-neighbour steps)

Does a part read only the hub's neighbours plus the neighbours of ONE spoke? That is the footprint of two nearest-neighbour steps.

| | RSST 71 parts | 533 added parts |
|---|---|---|
| real | 65 of 71 (92%) | 0%; needs 4.4 spokes on average |
| slot-scrambled nulls (3) | 73%, 86%, 92% | 0%; 4.3 to 4.4 |

RSST fits the two-step footprint, but no better than chance: RSST parts simply have few outer conditions. The added parts are full neighbourhood descriptions.

## Ideas, with status

1. **Add a time axis (rounds).** Rule = first-ring operation that reads the charge so far, not a second-ring picture. Candidate operations: PUSH (a 5 pays a big neighbour), FORWARD (a 7 or 8 left over-full passes the surplus on), RELAY (tunnel: in one door, out another). Evidence: FORWARD explains 89% of the 493 added push parts (null 7 to 9%); tunnels are literally two steps. Gap: who receives the forwarded unit is not explained (most-slack neighbour only 40%).
2. **Rules are the shadow of the configuration list.** A smooth law ("charge flows from sharp to flat") fits the rules, but fits scrambled rules equally well. The information is in the exceptions: the thin set of over-full neighbourhoods that contain no reducible configuration. So rule complexity is forced by holes in the configuration set. Three data points on that trade-off: 43 rules with 8,200 configurations, 32 with 633, 604 parts with 588.
3. **The rule set is not canonical.** Three very different rule sets prove the same theorem, so simplicity should come from choosing a different feasible point, not from compressing a given one. Concretely: fix a small round 1, offer the solver only FORWARD-type columns for round 2 ("hub left at +6 sends to neighbour class X", a handful of classes), and ask whether the world still closes.
4. **Threshold alphabet.** The recurring swaps are threshold questions, so outer vertices might need only two bits (at least 6? at least 7?) instead of a degree range. Decision diagrams over the full parts were larger than the part list (FABLE), so this helps notation, not count.

## Did not work

Low-rank behaviour (305 classes need 100 factors), decision diagrams, averaged transfer laws, mirror symmetry as the reason for 3 + 3 splits.

## Cheapest decisive test

Idea 3 as an engine run: round 1 = RSST's 71 parts, round 2 = FORWARD columns only, world = the 588 proof's. If it closes with a handful of receiver classes, the 533 added parts become one operation plus a receiver rule. Needs the swarm's engine and k's go.
