#!/bin/zsh
# Lean claim-glue build of 42379553 as committed (Long Table 19:56Z): fresh detached worktree, no local patches, fresh
# build dir, ~/mathlib4-planemap-build oleans read-only (copy-on-write). No lake. nice 19. Same steps as out/lean_glue/glue.sh.
WT=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/glue_4237; H=$WT/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck; W=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/glue_4237_build; L=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/out/lean_glue/42379553
date -u; echo "commit: $(git -C $WT rev-parse HEAD); status lines: $(git -C $WT status --short | wc -l); diff vs 42379553 lines: $(git -C $WT diff 42379553 | wc -l)"
echo "toolchain: $(cat $H/lean-toolchain); mathlib: $(git -C ~/mathlib4-planemap-build rev-parse HEAD)"
mkdir -p $W; cd $H
echo "### build_r2.sh"; nice -n 19 $H/build_r2.sh $W > $L/build_r2.log 2>&1; echo "build_r2 exit $?"
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
for f in DCheckPinch DCheckPinchGeom DCheckOccWalk ClaimGlue C66666 CGlue; do
  echo "### $f"; nice -n 19 env LEAN_PATH="$LP" $TC/bin/lean -o $W/dc/$f.olean -i $W/dc/$f.ilean $H/$f.lean > $L/$f.log 2>&1; echo "$f exit $?"
done
echo "after build: status lines: $(git -C $WT status --short | wc -l); diff vs 42379553 lines: $(git -C $WT diff 42379553 | wc -l)"
date -u; echo ALLDONE
