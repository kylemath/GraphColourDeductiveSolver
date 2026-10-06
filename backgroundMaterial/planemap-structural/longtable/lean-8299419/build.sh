#!/bin/bash
# Studio re-audit build of PlaneMap backup commit 8299419 over Mathlib 300d0e5.
cd "$HOME/mathlib4-planemap-build" || exit 1
export PATH="$HOME/.elan/bin:$PATH"
OUT="$HOME/studio-scratch/lean-build"
FILES="$HOME/studio-scratch/planemap-hash/snap2.txt"
mods() { awk '{print $2}' "$FILES" | grep "^$1/" | sed 's/\.lean$//; s|/|.|g'; }
step() {
  local name=$1; shift
  local t0=$(date +%s)
  echo "== $name start $(date '+%T')" >> "$OUT/summary.txt"
  nice -n 10 lake build "$@" > "$OUT/$name.log" 2>&1
  local rc=$?
  echo "== $name exit $rc, $(( $(date +%s) - t0 )) s, warnings $(grep -c '^warning' "$OUT/$name.log"), errors $(grep -c '^error' "$OUT/$name.log")" >> "$OUT/summary.txt"
}
: > "$OUT/summary.txt"
step 1-FiveColorTheorem Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem
step 2-FiveColorDemo MathlibTest.PlaneMapFiveColorDemo
step 3-Mathlib-rest $(mods Mathlib)
step 4-MathlibTest-rest $(mods MathlibTest)
echo "BUILD DONE $(date '+%T')" >> "$OUT/summary.txt"
