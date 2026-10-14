# Studio report: Job 10, arena hard set v1

- **From:** Studio session
- **To:** Long Table (coordinator)
- **Sent:** 2026-10-14 12:30 MDT
- **Replies to:** `2026-10-14_1214_longtable_to_studio_arena-hardset.md`
- **Label:** exploratory
- **Repo:** GraphColourRLArena `main` at `883467b` (pushed): `docs/arena/hardset/hardset-v1.json` and its README

## What was built

There are 302 maps, all sphere triangulations with a degree-5 hole that pass the arena's `checkTriangulation`. Each
is in the arena map format (`key, name, n, hole, link, edges, rot`), with source, a one-line why, meta, split and
exact distances.

| family | maps (train/eval) | n | states N | max distance to a fill |
|---|---|---|---|---|
| census floor-tight (Census29, one hole per graph, smallest orders first) | 150 (120/30) | 27–31 | 1,227–5,809 | 2: 67, 3: 83 |
| glued floor-tight (Studio Job 2, smallest n first) | 50 (40/10) | 42–45 | 84,018–418,298 | 2: 5, 3: 45 |
| R0 counterexample maps (p27#4710 h14, C40#14 h0) | 2 (2/0) | 27, 22 | 1,203; 321 | 3 |
| 66666 holes with a non-D-reducible 2-ball (Job 9 results, located in Census29 orders 30–32) | 100 (80/20) | 30–32 | 2,452–8,450 | 2: 30, 3: 70 |

**Distances.**
- Exact for all 302 maps (`stateSpace`, no cap reached; 2 min in total).
- The state count, unfilled count and max distance equal Job 7's `bnd.cpp` on all 251 census maps (a second engine).
- The maps are proof-hard but shallow: max distance ≤ 3. This is noted in the README.

**Checks.** `node tools/arena_check.js --quick`: all good. No retraining. The held-out census test maps are untouched.

**Tools in the arena repo.**
- `tools/hardset_select.py` reads a GraphColour checkout. For a 2-ball pattern it extracts (p_i, s_i) degrees around
  the hole, canonicalises with Job 9's `gen_2ball.canon`, and looks up `run9_results`.
- `tools/arena_hardset.js` computes the distances.

## Failures and notes

- None failed.
- Census33 was not needed: Census29 orders 27–31 supplied 150 floor-tight holes. Census29 uses `minfrac`, Census33
  uses `mf`; both are read.
- The 2-ball holes appear from order 30. Census orders 22–29 have no 66666 hole whose tested (ring ≤ 15) 2-ball is
  non-D-reducible.
- B7 (ring-16 / 3-ball runs) is held, as instructed. The Studio is idle.
