#!/bin/zsh
# rsst118 Lean build (Studio): dcheck chain at main fb35d2d1 into /Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1 (persistent, outside the repo), mathlib oleans read-only (cp -c), no lake, nice 15
D=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck; W=/Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1; L=$(cd $(dirname $0) && pwd)/lean
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
mkdir -p $L; cd $D; date -u > $L/build.log
nice -n 15 ./build_r2.sh $W >> $L/build.log 2>&1; echo "build_r2 exit $?" >> $L/build.log
LP=$W:$W/dc:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
for f in DCheckPinch DCheckPinchGeom DCheckOccWalk ClaimGlue C66666 CContract CGlue CXRing; do
  nice -n 15 env LEAN_PATH="$LP" $TC/bin/lean -o $W/dc/$f.olean -i $W/dc/$f.ilean $D/$f.lean > $L/$f.log 2>&1; echo "$f exit $? $(date -u +%H:%M)" >> $L/build.log
done
echo BUILD_DONE >> $L/build.log
