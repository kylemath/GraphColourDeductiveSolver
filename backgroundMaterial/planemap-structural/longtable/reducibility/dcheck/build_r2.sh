#!/bin/zsh
# Job 19: build the R2 glue (DCheckR2A..D) against the PlaneMap Mathlib build and the StudioMathLean
# PlaneMap modules up to RingReduce. Read-only on ~/mathlib4-planemap-build (oleans cloned copy-on-write).
# Usage: ./build_r2.sh [scratch-dir]   (Lean v4.35.0-rc3, nice 10)
set -e
H=${0:a:h}; W=${1:-$(mktemp -d)}
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
SRC=$H/../../../../../SolvingFrameworkPlan/docs/working/StudioMathLean; SRC=${SRC:a}
P=Mathlib/Combinatorics/SimpleGraph/PlaneMap
mkdir -p $W/dc
[ -d "$W/Mathlib" ] || cp -c -R "$B/.lake/build/lib/lean/Mathlib" "$W/Mathlib"
LP=$W:$W/dc:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
for f in EulerSharp VacancyIcosahedral RStar SideTriangle RStarCore MinimalFrame RingJordan RingChains RingReduce OccToRing DiamondMCert DiamondMOcc; do
  echo "== $f"; (cd $SRC && nice -n 10 env LEAN_PATH="$LP" $TC/bin/lean -R "$SRC" -o "$W/$P/$f.olean" -i "$W/$P/$f.ilean" "$P/$f.lean" > /dev/null)
done
for f in DCheck DCheckSound DCheckRef DCheckS1 DCheckS3 DCheck16 DCheck18 DCheckR1 DCheckT DCheckTEq DCheckSoundT DCheckRefT DCheckS1T DCheckR1T DCheckR2A DCheckR2B DCheckR2C DCheckR2D DCheckR2Diamond; do
  echo "== $f"; nice -n 10 env LEAN_PATH="$LP" $TC/bin/lean -o $W/dc/$f.olean -i $W/dc/$f.ilean $H/$f.lean 2>&1 | grep -v 'warning\|Hint\|Note\|linter\|^  \[\|̵\|^$' || true
done
