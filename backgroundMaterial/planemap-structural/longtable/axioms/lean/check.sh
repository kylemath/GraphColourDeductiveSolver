#!/bin/zsh
# Long Table A5v drafts: compile against the PlaneMap build at ~/mathlib4-planemap (read-only).
# The built Mathlib .olean tree is cloned copy-on-write (APFS `cp -c`) into a scratch directory;
# the needed Studio Math modules (read-only sources: TutteSides and the 22-module closure of
# QuarterLockParity + QuarterTait) and the Long Table A5v modules are compiled into it.
# Usage: zsh check.sh [path-to-built-checkout] [scratch-dir]
B=${1:-$HOME/mathlib4-planemap}
W=${2:-$(mktemp -d)}
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
cd "$(dirname "$0")"
L=$PWD
S=$(cd "$L/../../../../../SolvingFrameworkPlan/docs/working/StudioMathLean" && pwd)
P=Mathlib/Combinatorics/SimpleGraph/PlaneMap
[ -d "$W/Mathlib" ] || cp -c -R "$B/.lake/build/lib/lean/Mathlib" "$W/Mathlib"
LP=$W:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
for f in TutteSides QuarterFloor QuarterRotation QuarterRotationPlanar QuarterPi QuarterWinding \
    QuarterFloorH QuarterSigmaExit QuarterSigmaGroups QuarterGammaPeriod QuarterSigmaK34 \
    QuarterJordanDual QuarterPeriodJ QuarterLockJ QuarterWindow QuarterEvenCut QuarterTait NoFrozen \
    EulerSharp QuarterEuler QuarterSigmaFix QuarterPairDuality QuarterLockParity; do
  echo "== $f (Studio Math, read-only source)"
  (cd "$S" && nice -n 10 env LEAN_PATH="$LP" $TC/bin/lean -R "$S" -o "$W/$P/$f.olean" \
    -i "$W/$P/$f.ilean" "$P/$f.lean" > /dev/null) || exit 1
done
for f in A5vJordan A5vWitnessMap A5vWitness A5vNeedsFills A5vBridge A5vPrimMap A5vBridgeWitness; do
  echo "== $f"
  nice -n 10 env LEAN_PATH="$LP" $TC/bin/lean -R "$L" -o "$W/$f.olean" -i "$W/$f.ilean" "$f.lean" || exit 1
done
echo "== all modules compiled"
