#!/bin/bash
# J9: rerun of the audit's §2 check (message 2026-10-06_1520_audit_...) of Studio Math's Lean files, run on the Studio.
B=$HOME/mathlib4-planemap-build
cd "$HOME/studio-scratch/main-wt2/SolvingFrameworkPlan/docs/working/StudioMathLean" || exit 1
OUT=$HOME/studio-scratch/j9/out
mkdir -p "$OUT"
W=$HOME/studio-scratch/j9/w; mkdir -p "$W"
zsh ./check.sh "$B" "$W" > "$OUT/check-sh.txt" 2>&1; echo "exit $?" >> "$OUT/check-sh.txt"
LP=$W:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
LEAN=~/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean

shasum -a 256 -c SHA256SUMS > "$OUT/shasum-c.txt" 2>&1; echo "exit $?" >> "$OUT/shasum-c.txt"
grep -nE '\b(sorry|admit|native_decide|axiom|unsafe|implemented_by|extern|opaque|ofReduceBool|trustCompiler)\b' Mathlib/Combinatorics/SimpleGraph/PlaneMap/*.lean > "$OUT/grep.txt" 2>&1; echo "grep exit $? (1 = no match)" >> "$OUT/grep.txt"

SWEEP='
open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if (env.getModuleIdxFor? c).isNone && !c.isInternal then
      n := n + 1
      for a in (← liftCoreM (Lean.collectAxioms c)) do
        if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)
  logInfo m!"file constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"'

PRINTS_ICO='
#check @SimpleGraph.SphericalMap.theorem_H
#check @SimpleGraph.SphericalMap.icoBall_of_triangulated
#check @SimpleGraph.Icosahedron.theorem_H_icosahedron
#print SimpleGraph.SphericalMap.NoSeparatingTriangleAt
#check @SimpleGraph.SphericalMap.ico_fill
#print SimpleGraph.VacancyIcosahedral.IcoBall
#check @SimpleGraph.SphericalMap.theorem_HP
#check @SimpleGraph.Icosahedron.theorem_HP_icosahedron
#check @SimpleGraph.VacancyIcosahedral.hp_cases
#print axioms SimpleGraph.SphericalMap.theorem_HP
#print axioms SimpleGraph.Icosahedron.theorem_HP_icosahedron
#print axioms SimpleGraph.VacancyIcosahedral.hp_cases'
PRINTS_RSTAR='
#print SimpleGraph.SphericalMap.PureClean
#check @SimpleGraph.SphericalMap.four_color_of_global_Rstar
#check @SimpleGraph.SphericalMap.pureClean_of_theorem_H
#check @SimpleGraph.SphericalMap.pureClean_of_theorem_HP
#print axioms SimpleGraph.SphericalMap.four_color_of_global_Rstar
#print axioms SimpleGraph.SphericalMap.pureClean_of_theorem_H
#print axioms SimpleGraph.SphericalMap.pureClean_of_theorem_HP'
PRINTS_EULER='
#check @SimpleGraph.SphericalMap.twelve_light_fives
#check @SimpleGraph.SphericalMap.edge_card_bound_sharp
#check @SimpleGraph.Icosahedron.twelve_light_fives_icosahedron
#check @SimpleGraph.SphericalMap.relative_light_fives
#check @SimpleGraph.Icosahedron.relative_light_fives_icosahedron
#print StudioMath.goodSet
#print StudioMath.highSet'

run() {  # $1 = source path without .lean, $2 = copy name, $3 = text inserted before the sweep
  local cp=/tmp/audit_$2.lean
  cp "$1.lean" "$cp"
  printf '%s\n' "$3" >> "$cp"
  printf '%s\n' "$SWEEP" >> "$cp"
  (cd "$OUT" && nice -n 10 env LEAN_PATH="$LP" $LEAN "$cp" > "/tmp/audit_$2.out" 2>&1; echo "exit $?" >> "/tmp/audit_$2.out")
  cp "$cp" "/tmp/audit_$2.out" "$OUT/"
}
date '+start %F %T %Z' > "$OUT/times.txt"
run Mathlib/Combinatorics/SimpleGraph/PlaneMap/EulerSharp EulerSharp "$PRINTS_EULER"
run Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyIcosahedral VacancyIcosahedral "$PRINTS_ICO"
run Mathlib/Combinatorics/SimpleGraph/PlaneMap/RStar RStar "$PRINTS_RSTAR"
run Mathlib/Combinatorics/SimpleGraph/PlaneMap/EulerSharp EulerSharp_negcontrol "
theorem auditPlanted : (1:ℕ) = 2 := sorry"
date '+end %F %T %Z' >> "$OUT/times.txt"
