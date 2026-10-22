# LT-XU: admissibleXU, the C glue without the |X| ≤ 4 cap (Studio, 22 Oct 2026)
- **New file:** dcheck/CGlueU.lean (imports CGlue; nothing in CGlue is changed).
  - **Contents:** `admissibleXU` (admissibleX minus `decide (eqR.length + eqI.length ≤ 4)`), `admissibleXU_of_admissibleX`, and the U
    copies of `ConfigOccW.xGraph_labels`, `contract_reducer_of` and `xGraph_labels_fold`. Each is generated verbatim from CGlue.lean
    with `hadm : admissibleXU` and one fewer discarded conjunct in the obtain pattern.
  - **Entry structures:** `CEntryU`, `OccursCXU`, `CEntryU.colorable(_of_contract)`, `CGlueXU` / `cGlueXU`, `CEntryFU`,
    `OccursCXFU`, `CEntryFU.colorable`, `CGlueXFU` / `cGlueXFU`.
- **CGlueU.lean build** (the 2a4bc4cf Lean build; the dcheck sources are unchanged to HEAD): exit 0, sorry 0.
  - **#print axioms:** equal to the originals' (cGlueXU = cGlueX, 9 axioms; cGlueXFU = cGlueXF, 13; xGraph_labelsU / foldU = the
    originals, 3 each); log CGlueU.log.
- **Clean rebuild into a fresh directory:**
  - CGlue: exit 0, sorry 0, #print axioms identical to the 2a4bc4cf log on all 22 theorems. The olean differs only in embedded paths.
  - CXRing: exit 0, olean byte-identical.
  - CC2All: exit 0, axioms identical to f2acc3e7's.
- **Smoke** (CGlueUSmoke.lean, exit 0):
  - **The entry:** f7_...5565_....... (r 9, m 5) with interior-only X = {I0-I1, I0-I3, I0-I4, I1-I4, I3-I4}, |X| = 5. The triangles
    (0,1,4) and (0,3,4) lie inside one merged group {0,1,3,4}.
  - **Proved by native_decide:** `xuSmoke_admU` (admissibleXU = true), `xuSmoke_not_adm` (admissibleX = false),
    `xuSmoke_len` (|X| = 5) and `xuSmoke_interior` (eqR = []).
  - **cfast on this X:** INADMISSIBLE with gonthier (sparse), admissible with --nogonthier, not C-reducible (leftover > 0).
  - **No hC:** so no CEntryU instance (hC) is built for it.
  - **The search for a real C case:** among the CXInt configurations (r ≤ 11, every triangle plus 2 edges, cfast --nogonthier
    --fixed), no |X| = 5 triangle-group X with leftover 0 was found yet. A wider search runs in the background.
