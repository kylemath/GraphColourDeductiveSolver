#!/bin/zsh
# Single-file check of the Studio Math modules against a built PlaneMap snapshot 8299419
# (Mathlib 300d0e5 + PlaneMap files), read-only. Usage: ./check.sh [path-to-built-checkout]
B=${1:-$HOME/mathlib4-planemap-build}
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$(ls -d $B/.lake/build/lib/lean $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
cd "$(dirname "$0")"
for f in Mathlib/Combinatorics/SimpleGraph/PlaneMap/EulerSharp.lean \
         Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyIcosahedral.lean; do
  echo "== $f"; nice -n 10 env LEAN_PATH="$LP" $TC/bin/lean "$f" || exit 1
done
