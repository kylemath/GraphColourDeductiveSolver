# Revision 85: Math's catch-up reviews recorded; WP20 P1 in progress, no results

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-05 20:42 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_2042_math_to_longtable+navigator+audit_catch-up-reviews-and-WP20-go-ahead.md`
- **Asks for:** information only; Math to re-read trace §2b (see below)

## Recorded (planning.json revision 85)

- **Accepted by hand, not compiled** (Math 20:42): Tilley bridge, Lemma F, D1 reduction to (N) in the rigid triply locked case, Lemma L4, E1–E4, Theorem P. New nodes under `structural-tilley` (bridge, Lemma F, `structural-d1-rigid`: proved). L4/E1–E4 and Theorem P are notes on `structural-long-fill` and `structural-equal-pole`; the latter stays exploring, since Theorem P is the no-singleton pole case and compiled results cover only unequal poles.
- **Trace lift** for triangles and 4-cycles: `structural-trace-lift`, proved by hand on Math's reference proof (`MathTraceGameLiftReview.md`). The 17:30 "not accepted" note applied to the old page text. The exploratory counts (435, 4004, 2002) are `exploring`, not replayed.
- **§2b (5-cycle):** `exploring`. Math 20:42: not yet accepted. Long Table's pentagon paragraph (commit bf58cf8) is not yet re-reviewed.
- **SEP and D1:** `exploring`, conjecture from post hoc data. D1 for all minimum-degree-5 triangulations would imply the Four Colour Theorem. No upgrade from finite passes.
- **Degree-6 separator, 4+4 split:** `structural-deg6-split`, proved by hand (Math 17:29).

## WP20 chronology (facts, not acceptance of anything)

P1 (order 25, 25,381 graphs) started 20:06 on the user's chat release. Math's written go-ahead for P1 only, naming declaration SHA-256 `8758a9f8…2fef` and commit `303e291`, is headed 20:42, after the start, and does not backdate it. P2 is not covered. Math did not read the producer, the checker or the output-format file. Hashes in the declaration, producer and checker match the files on disk (checked now). Results are not in. The report must list each D1 kill with its P verdict and `filled_neighbour` count. Clock note: Math's file appeared at about 20:39 on the machine clock; the order against 20:06 is unaffected.

## Pathways confirmed

- `node docs/navigator/planning.test.cjs`: passes (190 nodes), with new assertions for the ten new nodes.
- Syntax check of `app.js`, `tree.js`, `data.js`, `tree3d.js` and JSON validity: ok. `index.html` script and style links resolve. A browser load was not run.
- 389 file paths cited in nodes (`planning.json`, `data.js`) were checked on disk: 381 resolve, including every new node's files and the WP20 package.
- **Broken (8):** `lean4/FourColor/Foundation/F2_Planarity.lean`, `F3_EulerFormula.lean`, `F5_FiveColorTheorem.lean`, and `lean4/FourColor/Track1_KempeSwap/`, `Track2_ChromaticPoly/`, `Track3_Flows/`, `Track5_Spectral/`, `Track6_Sheaf/`. They appear in the original `data.js` plan nodes (unstarted), not in `PATHMAP.md`, and were never created. They are not moves. Left as is; the owner of `data.js` should decide whether to retire them.
