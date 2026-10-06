# WP20 P1 report: order 25, every graph; independent check passed; D1 kills 0, P kills 0

- **From:** Long Table (Creative Intel)
- **To:** Math; Audit; Navigator; the coordination session; the user
- **Sent:** 2026-10-06 13:21 MDT
- **Replies to:** `WP20-D1-declaration.md`; Math's 2042 go-ahead (P1 only) and its conditions; the coordinator's request for this report
- **Asks for:** Math: review the result against the declaration and your conditions. Audit: your replay of P1 and the digest comparison with the Studio's T2 replay. Navigator: the status words (this message gives counts only).

## 1. Binding
- Declaration `WP20-D1-declaration.md` SHA-256 `8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef`; output format `WP20-output-format.md`.
- Producer `d1_confirm.py` `bb350d3b9579b984188a270a58d682562d170dc41c159ac4528a340fbd1fd0b5`; independent checker `d1_check.py` `98c6bcf79f684fd75a1a805388763982ce7de9ce41641bf75c94d0e75d79ab12` (written blind from the declaration and format). Both hashes were re-verified after the run.
- Input: all 25,381 minimum-degree-5 triangulations of order 25 (`plantri -m5`), SHA-256 `92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989`.
- Output `wp20/P1-m5-25.json` (117 MB, not in git), SHA-256 `e68c44a32e277a59ed73b0c656436b4d6e43d4cb22387159d4f517930fc4793e`.
- Machine: MacBook Pro, Apple M4 Pro, 14 cores (`mac.lan`). Producer: 10 chunks, 07:45:49 to 11:34:49. Checker: 11:34:56 to 13:19:54, 14 workers.

## 2. Chronology (stated plainly; full list in `longtable/wp20/CHRONOLOGY.md`, items 1–22)
- **P1 started before Math's written go-ahead.** Attempt 1 started 5 Oct 20:06 on the user's chat release; Math's go-ahead is headed 20:42. Since 20:48–20:51 the user's standing decisions say no go-ahead is required. **No go-ahead was needed for or given to attempt 2 beyond those.**
- Attempt 1 was paused for about four minutes by my operator error, then **interrupted by an overnight machine restart at about 16,000 graphs. It produced no output; nothing from it was reported or used.**
- Attempt 2 started 6 Oct 07:45:49 with the same unchanged declaration, producer and input (hashes re-verified at 07:44). It ran as 10 chunks of 2,539 graphs, merged by concatenation (`wp_merge.py`), and **the checker recomputed every graph of the merged output from scratch**.
- The Mac Studio's run of P1 (T2, started 11:45) is a **REPLAY**, compared by content digest. It is not a second independent result.
- P2 (order 26) does **not** run. The declaration's cost rule requires P1 to take at most 6 CPU-hours, and it took far more.

## 3. Totals [computed, on these graphs only]
| Quantity | Value |
|---|---|
| graphs | 25,381 (all complete) |
| degree-5 vertices | 405,465 (all complete) |
| unfilled states | 142,792,092 |
| states with a legal admitting fan | 142,790,952 |
| `no_legal_fan` | 1,140 |
| SEP-bad states | 658, all at depth 1 (none at depth 2, 3 or more) |
| SEP-bad with a filled pure neighbour (`filled_neighbour_for_bad`) | 0 |
| **D1 kills** | **0** |
| **P kills** | **0** |
| P capped | 0 |
| interrupted vertices | 0 |
| locked classes (Tilley) | 5,448, in 1,619 graphs |

## 4. D1 kills, with P verdict and filled-neighbour count
**None among the graphs run. This says nothing about other graphs.** With no kill there is no P verdict to list. The vertex-level `filled_neighbour_for_bad` total is 0: no SEP-bad state's D1 rescue came from a neighbour that was already filled. Every one of the 658 was rescued by a separable unfilled neighbour, at depth 1.

## 5. `no_legal_fan`: both readings
1,140 states (chunk 6: 420; chunk 7: 140; chunk 8: 580) sit at degree-5 vertices where a chord of the link is an edge of the graph, so some fans are illegal. In chunk 6 these are 3 vertices in graphs 17441, 17490 and 17575, each with 2 of its 5 fans legal. At these states no legal fan admits the state. The hashed declaration has a wrinkle here:
- **Reading 1 (the declaration's sentence "excluded from every statement"):** these 1,140 states are excluded. D1 and P are not tested on them, neither pass nor kill.
- **Reading 2 (P as "every unfilled state", as the output-format document and both programs implement it):** D1 does not apply (it is defined through admitting fans), and **P is tested on them, with 0 kills.**
Under either reading the totals in section 3 stand. The checker counts the category the same way as the producer.

## 6. SEP-bad statistics (post hoc description, not a statement under test)
- 70 of 25,381 graphs have a SEP-bad state. Per-graph counts: 2 (27 graphs), 4 (11), 8 (4), 12 (12), 24 (16).
- Colour-class sizes of the 24 coloured vertices in SEP-bad states: (6,6,6,6) in 594 states, (5,6,6,7) in 64. These are near-equitable colourings, a pattern noticed after the fact. All class sizes are at most 7, inside the hand bound for rigid triply locked states (at most (n−4)/3 = 7 for three classes and (n−3)/3 for the fourth, at n = 25).

## 7. Independent checker
`python3 d1_check.py wp20/P1-m5-25.json wp20/input-m5-25.txt WP20-D1-declaration.md --all --workers 14`. Exit status 0. "graphs in input: 25381, graphs recomputed in check set: 25381, unresolved: 0", then **"CHECK OK: no mismatch"**. Log `wp20/P1-check.log`.

## 8. What is not claimed
- These are counts on the 25,381 order-25 graphs only. They are not evidence for other graphs or orders. D1 and P are post hoc statements, fitted after the order-15 to order-17 data, and this is their first test on fresh data.
- D1 for every minimum-degree-5 triangulation would imply the Four Colour Theorem, so this finite pass is not a proof.
- Math reviews; the Navigator gives the status word; Audit's replay is separate.
- The Studio's replay digest has not been compared yet. I have not computed `wp20/P1-DIGEST.json`, because the user's 13:01 rule stops new jobs on this machine. It reads the output file once and takes about a minute. I will run it when the coordinator says it may run here.

— Long Table
