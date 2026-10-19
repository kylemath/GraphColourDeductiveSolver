# CGlue sorry-free build (60269a51, contains 1ebfc919), Mac Studio, 19 Oct 22:29-22:36Z

Fresh detached worktree at 60269a51894bc4c770fbfdf4f9638cdf399b9e82, no local patches (git status and git diff vs
60269a51 empty before and after). Toolchain v4.35.0-rc3; Mathlib 300d0e53 oleans read-only. No lake, no download,
nice 19, k19 untouched. Driver glue_6026.sh: glue.sh steps, then C66666, CContract, CGlue.

Exit codes: build_r2 0, DCheckPinch 0, DCheckPinchGeom 0, DCheckOccWalk 0, ClaimGlue 0, C66666 0, CContract 0,
CGlue 0. `grep -c sorry`: 0 on every log; `grep -c sorryAx`: 0. Kill line not met.
#print axioms (AxPath.lean: a Studio diagnostic file importing CGlue, not part of the commit; cGlueX is not printed in
the file itself): contract_subgraph_gen = propext, Classical.choice, Quot.sound; CEntry.colorable and cGlueX = those +
DCheck.R1.check4..9 native_decide aux; four_color_of_unavoidableC = those + DCheck.Meet.{check4_true, check5_true,
size4, size5} native_decide aux. No sorryAx anywhere.
