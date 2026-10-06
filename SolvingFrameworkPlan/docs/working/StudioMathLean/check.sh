#!/bin/zsh
# Check the Studio Math modules against a built PlaneMap snapshot 8299419 (Mathlib 300d0e5),
# read-only: the built Mathlib .olean tree is cloned copy-on-write (APFS `cp -c`) into a private
# directory, and the Studio Math modules are compiled into that clone in dependency order.
# Usage: ./check.sh [path-to-built-checkout] [scratch-dir]
B=${1:-$HOME/mathlib4-planemap-build}
W=${2:-$(mktemp -d)}
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
cd "$(dirname "$0")"
S=$PWD
P=Mathlib/Combinatorics/SimpleGraph/PlaneMap
[ -d "$W/Mathlib" ] || cp -c -R "$B/.lake/build/lib/lean/Mathlib" "$W/Mathlib"
LP=$W:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
for f in EulerSharp VacancyIcosahedral RStar SideTriangle RStarCore MinimalFrame RingJordan RingChains; do
  echo "== $f"
  nice -n 10 env LEAN_PATH="$LP" $TC/bin/lean -R "$S" -o "$W/$P/$f.olean" -i "$W/$P/$f.ilean" "$P/$f.lean" || exit 1
done
