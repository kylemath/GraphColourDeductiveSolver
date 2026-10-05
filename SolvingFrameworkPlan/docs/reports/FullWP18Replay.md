# Complete independent replay of the existing WP18 outputs

Independent audit, 4 October 2026. This extends the earlier witness audit to every admitted start on every legal vertex-and-fan pair in the existing P1–P4 files. No new graphs were generated.

The replay passed: 961 graphs, 68,890 pairs, 3,765,835 distinct admitted states counted separately per graph, and 7,618,165 fan memberships. A state admitted by several fans is counted several times only in the latter number. Every reported start count, distance histogram, pair maximum L, graph minimum m, and phase histogram agrees.

| Existing phase | Graphs | m=1 | m=2 | m=3 |
| --- | ---: | ---: | ---: | ---: |
| P1, orders 12–18 | 22 | 10 | 11 | 1 |
| P2, orders 19–20 | 96 | 22 | 74 | 0 |
| P3, order 21 | 192 | 46 | 146 | 0 |
| P4, order 22 | 651 | 105 | 546 | 0 |
| Total | 961 | 183 | 777 | 1 |

Order 17 graph 1 is the sole m=3 graph. Every other graph in these files has m<=2. Every admitted start on every tested pair has mixed distance at most four. These are now independently reproduced computation claims on the supplied graphs. They neither prove an unrestricted bound nor settle VH∃.

## Method and reproducibility

`backgroundMaterial/planemap-structural/longtable/audit/wp18_full_replay.py` uses the audit's standard-library graph validation, restricted-growth colour enumeration, legal fan construction, Kempe component moves, singleton slides and breadth-first distances. It imports neither the WP18 producer nor `mass_core`. It reconstructs each fan's family instead of trusting the producer's starts. Shared starts reuse the same independently computed distance within their graph. Breadth-first search stops at depth four only after searching all earlier layers; every state reaches a target within that cap.

The earlier independent review binds the supplied graph lists to the existing inputs and verifies witnesses. This extension compares the complete families. Results, graph-level summaries, four input-output digests and both source digests are in `audit/wp18-full-replay-results.json`. Runtime was about 128 seconds.

Run from the repository:

    python3 backgroundMaterial/planemap-structural/longtable/audit/wp18_full_replay.py

This supersedes only the previous limitation that the other graphs' upper bounds and full histograms had not been independently reconstructed. Math acceptance and any future release remain separate decisions. The producer's resource-limit concerns from the earlier review remain relevant to future runs.

## Belt progress

The new `swarm/doubled-one-opening-audit.md` supplies a local transition for both missing doubled-1 opening words: one slide fills, or three legal slides return to the same opening class two indices forward. It explicitly does not infer termination from a cyclic shift. Long Table still owns assembly, doubled-0 coverage and the final overlap checks.
