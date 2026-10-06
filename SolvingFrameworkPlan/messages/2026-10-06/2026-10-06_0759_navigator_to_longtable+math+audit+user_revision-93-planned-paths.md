# Revision 93: the eight dead Lean paths are flagged "planned, not yet written"

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit; the user
- **Sent:** 2026-10-06 07:59 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_0756_navigator_to_longtable+math+audit_revision-92.md`
- **Asks for:** the user, a decision on six further broken paths (below); others, information only

## User decision recorded

The user chose, in chat on 6 October, to keep the nodes and mark each of these paths "planned, not yet written": `lean4/FourColor/Foundation/F2_Planarity.lean`, `F3_EulerFormula.lean`, `F5_FiveColorTheorem.lean`, and the directories `Track1_KempeSwap/`, `Track2_ChromaticPoly/`, `Track3_Flows/`, `Track5_Spectral/`, `Track6_Sheaf/`.

## What changed

- `data.js`: nodes `f2`, `f3`, `f5`, `t1-4`, `t2-1`, `t3-1`, `t5-2`, `t6-2` carry `plannedFiles` next to `files`. `app.js` and `styles.css` show "(planned, not yet written)" beside those paths in the detail panel.
- New `docs/navigator/check-paths.cjs`: checks every node's file paths on disk, skips `plannedFiles`, prints a note if a planned file now exists, and exits 1 on any other missing path.
- `planning.test.cjs`: asserts the eight flags, that the check ignores exactly those eight, that a bogus path and an unflagged copy of a planned path still fail, and that the set of broken paths equals the known list below, so any new broken path fails the test.
- `planning.json` revision 93: a note on each of the eight nodes and a journal entry. No status changed.

## Found while writing the check, not covered by the decision

My revision 85 check only looked at paths starting with `SolvingFrameworkPlan`, `backgroundMaterial`, `docs` or `lean4`. The full check finds **six more broken paths** in the original plan nodes, all under `compute/`: `chromatic/root_finder.py` (nodes t2-2 and t7-2), `spectral/colin_de_verdiere.py` (t5-1), `topology/sheaf_cohomology.py` (t6-1), `discovery/tensor_network.py` (t7-1), `discovery/gnn_coloring.py` (t7-3). The directories exist and hold differently named files (for example `a1720_cdv.py`, `a1720_sheaf.py`), but nothing maps the old names, so I did not guess. They are not flagged and are not in PATHMAP.md. **User: flag them as planned, repoint them, or leave them failing?**

`planning.test.cjs` passes. No finite check is upgraded.
