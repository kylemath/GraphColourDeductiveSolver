#!/bin/zsh
# Compile the frozen challenges and their anti-drift bridges against the PlaneMap build.
# Needs a scratch dir in which StudioMathLean/check.sh has already compiled the Studio modules
# (the bridges import FrameF3).  Usage: ./check.sh <scratch-dir> [path-to-built-checkout]
W=${1:?scratch dir from StudioMathLean/check.sh}
B=${2:-$HOME/mathlib4-planemap-build}
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
cd "$(dirname "$0")/.."
S=$PWD
mkdir -p "$W/Challenges"
LP=$W:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
for f in RStarFrameChallenge RStarFrameBridge FourColorSphericalMapChallenge FourColorBridge; do
  echo "== $f"
  nice -n 10 env LEAN_PATH="$LP" $TC/bin/lean -R "$S" -o "$W/Challenges/$f.olean" -i "$W/Challenges/$f.ilean" "Challenges/$f.lean" || exit 1
done
