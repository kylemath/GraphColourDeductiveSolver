#!/bin/zsh
# Re-elaborate one draft (BeltGraph or BeltWalk) after ./build.sh has populated _build.
set -eu
HERE=${0:A:h}; OUT=${OUT:-$HERE/_build}; BASE=/tmp/planemap-audit-20261005-short-fill
export LEAN_PATH=$(python3 -c "import json;m=json.load(open('$BASE/manifest.json'));print(':'.join('$OUT/lib' if x=='$BASE/lib' else x for x in m['lean_path']))")
cd $HERE && /Users/fulkanjou/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean -R $HERE -o $OUT/lib/$1.olean $1.lean
