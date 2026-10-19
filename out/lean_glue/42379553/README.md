# CGlue draft build (42379553), Mac Studio, 19 Oct 22:01-22:08Z

Fresh detached worktree at 42379553e0777b12d65b102194191657ef30b65e, no local patches (git status and git diff vs
42379553 empty before and after). Toolchain v4.35.0-rc3; Mathlib 300d0e53, oleans read-only. No lake, no download,
nice 19, k19 untouched. Driver glue_4237.sh = glue.sh steps + C66666 + CGlue.

Exit codes: build_r2 0, DCheckPinch 0, DCheckPinchGeom 0, DCheckOccWalk 0, ClaimGlue 0, C66666 0, CGlue 0; 0 errors.
One `declaration uses sorry` warning, at CGlue.lean:420 (`contract_subgraph`).

sorry path (AxPath.lean, a Studio diagnostic file importing CGlue, not part of the commit; AxPath.log):
- sorryAx: contract_subgraph (its own sorry) -> ConfigOccW.contract_reducer -> CGlue.CEntry.colorable -> cGlueX,
  four_color_of_unavoidableC.
- sorry-free: ConfigOccW.xGraph_labels, colorable_of_cReducible18, colorable_of_goodT, occursCX_of_configOcc,
  runGoodRefT_sound, extCAux_complete, cf66666_hC, cf66666_not_I0I1, and the e66666 entry itself (data + decide).
Single-edge path: CEntry.colorable uses contract_reducer for every X, single-edge X included, and the file has no
separate single-edge reducer; so no C path, single-edge or not, closes without contract_subgraph. e66666 is a sorry-free
CEntry, but its colourability goes through CEntry.colorable and so through the sorry.
