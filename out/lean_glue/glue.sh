#!/bin/zsh
# Lean claim-glue build (Long Table 19 Oct 19:00Z): ClaimGlue.lean at 93797745, in a separate detached worktree
# (/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/glue_wt), against ~/mathlib4-planemap-build oleans read-only (copy-on-write). No lake. nice 19.
# Waits for the rows 1-2 C re-run streams to finish (free slot).
S=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job30/s52r12; WT=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/glue_wt; H=$WT/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck
W=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/glue_build; L=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/out/lean_glue
until [ -f $S/DONE_p0 ] && [ -f $S/DONE_p1 ]; do sleep 30; done
date -u; echo "toolchain: $(cat $H/lean-toolchain); mathlib: $(git -C ~/mathlib4-planemap-build rev-parse HEAD)"
mkdir -p $W; cd $H   # lean -o needs the input under the root (cwd)
echo "### build_r2.sh"; nice -n 19 $H/build_r2.sh $W > $L/build_r2.log 2>&1; echo "build_r2 exit $?"
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
for f in DCheckPinch DCheckPinchGeom DCheckOccWalk ClaimGlue; do
  echo "### $f"; nice -n 19 env LEAN_PATH="$LP" $TC/bin/lean -o $W/dc/$f.olean -i $W/dc/$f.ilean $H/$f.lean > $L/$f.log 2>&1; echo "$f exit $?"
done
date -u; echo ALLDONE
