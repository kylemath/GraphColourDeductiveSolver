# Revision 94: six broken compute paths flagged "planned, not yet written"

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit; the user
- **Sent:** 2026-10-06 08:01 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_0759_navigator_to_longtable+math+audit+user_revision-93-planned-paths.md`
- **Asks for:** information only

## Coordinator decision recorded

The coordinator gave the six broken `compute/` paths the same treatment the user chose for the Lean paths. They are flagged with `plannedFiles` and shown in the app as "(planned, not yet written)": `chromatic/root_finder.py` (nodes t2-2 and t7-2), `spectral/colin_de_verdiere.py` (t5-1), `topology/sheaf_cohomology.py` (t6-1), `discovery/tensor_network.py` (t7-1), `discovery/gnn_coloring.py` (t7-3). **They were not repointed.** Each node's note says that differently named files exist in those directories (for example `a1720_cdv.py`, `a1720_sheaf.py`), that no mapping is established, and that a later pass may repoint them.

## Check and test

`docs/navigator/check-paths.cjs` now reports 14 planned paths and 0 broken (exit 0). It still exits 1 on any other missing path. `planning.test.cjs` asserts the 14 flags and replaces the known-broken list with an assertion that no other path is broken; the bogus-path fixtures still fail as required, and the test passes. No status changed, and nothing is upgraded from finite data.
