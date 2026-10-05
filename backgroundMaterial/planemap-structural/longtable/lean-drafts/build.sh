#!/bin/zsh
# Elaborate the Long Table belt drafts against Math's accepted 83-module overlay.
# Method follows longtable/audit/belt_preparation_audit.py: a symlinked copy of the
# accepted lib, fresh compilation of the helper modules this draft imports
# (read-only from the Math repo), then the drafts. Nothing is written to the Math
# repo or the accepted build; all .olean files go to $OUT (default: ./_build).
set -eu
HERE=${0:A:h}
REPO=/Users/fulkanjou/mathlib4-planemap
BASE=/tmp/planemap-audit-20261005-short-fill
LEAN=/Users/fulkanjou/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean
OUT=${OUT:-$HERE/_build}
PM=Mathlib/Combinatorics/SimpleGraph/PlaneMap

rm -rf $OUT; mkdir -p $OUT/lib/Mathlib/Combinatorics/SimpleGraph
# overlay: symlink everything except the PlaneMap directory, which is copied as symlinks per file
for p in $BASE/lib/*; do [[ ${p:t} == Mathlib ]] || ln -s $p $OUT/lib/${p:t}; done
for p in $BASE/lib/Mathlib/*; do [[ ${p:t} == Combinatorics ]] || ln -s $p $OUT/lib/Mathlib/${p:t}; done
for p in $BASE/lib/Mathlib/Combinatorics/*; do [[ ${p:t} == SimpleGraph ]] || ln -s $p $OUT/lib/Mathlib/Combinatorics/${p:t}; done
for p in $BASE/lib/Mathlib/Combinatorics/SimpleGraph/*; do [[ ${p:t} == PlaneMap ]] || ln -s $p $OUT/lib/Mathlib/Combinatorics/SimpleGraph/${p:t}; done
mkdir -p $OUT/lib/$PM
for p in $BASE/lib/$PM/*; do ln -s $p $OUT/lib/$PM/${p:t}; done

LP=$(python3 -c "import json;m=json.load(open('$BASE/manifest.json'));assert m['status']=='passed';print(':'.join('$OUT/lib' if x=='$BASE/lib' else x for x in m['lean_path']))")
export LEAN_PATH=$LP

# helpers not in the accepted overlay (compiled fresh, sources read-only)
for m in VacancyPotential BeltOpeningWords BeltVacancyTeamA BeltCapsMath; do
  echo "== $PM/$m.lean"
  (cd $REPO && $LEAN -o $OUT/lib/$PM/$m.olean $PM/$m.lean)
done
# drafts (module names BeltGraph, BeltWalk; root = this directory)
for m in BeltGraph BeltWalk AxiomCheck; do
  echo "== $m.lean"
  (cd $HERE && $LEAN -R $HERE -o $OUT/lib/$m.olean $m.lean)
done
echo "== done"
