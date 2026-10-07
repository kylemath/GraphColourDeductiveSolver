#!/bin/bash
# J13: the audit's independent check of Studio Math (local) cd0fcfc: new module Conf2122Witness, docstring-only
# edits to FrameF3 and RStarSanity. Run on the MacBook under the coordinator's relay (17:2x, 6 Oct) of the user's
# decision: capped local compute, at most 6 cores and 45 minutes per job. Every lean process: ulimit -t 1800,
# nice 10, LEAN_NUM_THREADS=6. Usage: run_j13.sh COMMIT SCRATCH OUTDIR
set -u
C=${1:?commit}; S=${2:?scratch}; OUT=${3:?outdir}
R=/Users/fulkanjou/GraphColour; B=$HOME/mathlib4-planemap
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3; LEAN=$TC/bin/lean
P=Mathlib/Combinatorics/SimpleGraph/PlaneMap
mkdir -p "$OUT" "$S/src" "$S/w"
date '+start %F %T %Z' > "$OUT/times.txt"
# 1. clean tree of the Lean folder at the commit (git archive: no working-tree files, no index)
git -C "$R" rev-parse "$C" > "$OUT/commit.txt"
git -C "$R" archive "$C" SolvingFrameworkPlan/docs/working/StudioMathLean | tar -x -C "$S/src"
L=$S/src/SolvingFrameworkPlan/docs/working/StudioMathLean
# 2. base: the 8299419 olean tree from ~/mathlib4-planemap (bcff6cd), cloned copy-on-write; one missing library
#    olean (SphericalFourContact, source hash = lean-8299419/SHA256SUMS-copied) compiled into the clone
W=$S/w
[ -d "$W/Mathlib" ] || cp -c -R "$B/.lake/build/lib/lean/Mathlib" "$W/Mathlib"
LP=$W:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
shasum -a 256 "$B/$P/SphericalFourContact.lean" > "$OUT/base.txt"
git -C "$B" rev-parse HEAD >> "$OUT/base.txt"
( ulimit -t 1800; cd "$B" && nice -n 10 env LEAN_NUM_THREADS=6 LEAN_PATH="$LP" $LEAN -o "$W/$P/SphericalFourContact.olean" -i "$W/$P/SphericalFourContact.ilean" "$P/SphericalFourContact.lean" ) >> "$OUT/base.txt" 2>&1
echo "SphericalFourContact exit $?" >> "$OUT/base.txt"
# 3. the authors' check.sh, all 24 modules, into the clone
cd "$L"
s=$(date +%s); ( ulimit -t 1800; LEAN_NUM_THREADS=6 zsh ./check.sh "$B" "$W" ) > "$OUT/check-sh.txt" 2>&1; echo "exit $?" >> "$OUT/check-sh.txt"
echo "check.sh wall $(( $(date +%s) - s ))s" >> "$OUT/times.txt"
shasum -a 256 -c SHA256SUMS > "$OUT/shasum-c.txt" 2>&1; echo "exit $?" >> "$OUT/shasum-c.txt"
find . -name '*.lean' -print0 | xargs -0 grep -nE '\b(sorry|admit|native_decide|axiom|unsafe|implemented_by|extern|opaque|ofReduceBool|trustCompiler)\b' > "$OUT/grep.txt" 2>&1; echo "grep exit $? (1 = no match)" >> "$OUT/grep.txt"
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
pr() { case $1 in
Conf2122Witness) echo '
#check @SimpleGraph.Witness2122.occ_C2122M
#check @SimpleGraph.Witness2122.occ_C2122P
#check @SimpleGraph.Witness2122.not_conf2122Free
#check @SimpleGraph.Witness2122.mem_class
#print SimpleGraph.SphericalMap.C2122M.Occ
#print SimpleGraph.SphericalMap.Conf2122Free
#print SimpleGraph.SphericalMap.RStarNoSepTri
#print axioms SimpleGraph.Witness2122.not_conf2122Free
#print axioms SimpleGraph.Witness2122.mem_class
#print axioms SimpleGraph.Witness2122.occ_C2122P
example : ¬ SimpleGraph.Witness2122.sphericalMap.Conf2122Free ∧ (0 < 22 ∧ SimpleGraph.Witness2122.sphericalMap.graph.Connected ∧ SimpleGraph.Witness2122.sphericalMap.Triangulated ∧ (∀ x, 5 ≤ SimpleGraph.Witness2122.sphericalMap.graph.degree x) ∧ SimpleGraph.SphericalMap.NoSep SimpleGraph.Witness2122.sphericalMap) := ⟨SimpleGraph.Witness2122.not_conf2122Free, SimpleGraph.Witness2122.mem_class⟩' ;;
FrameF3) echo '
#print SimpleGraph.SphericalMap.RStarFrame
#print SimpleGraph.SphericalMap.DiamondFree
#print SimpleGraph.SphericalMap.Conf2122Free
#check @SimpleGraph.SphericalMap.four_color_of_RStarFrame
#print axioms SimpleGraph.SphericalMap.four_color_of_RStarFrame' ;;
RStarSanity) echo '
#check @SimpleGraph.Icosahedron.not_diamondFree
#check @SimpleGraph.Icosahedron.conf2122Free' ;;
esac; }
run() {
  local cp=$S/audit_$2.lean
  cp "$P/$1.lean" "$cp"; printf '%s\n' "$3" >> "$cp"; printf '%s\n' "$SWEEP" >> "$cp"
  local s=$(date +%s)
  ( ulimit -t 1800; nice -n 10 env LEAN_NUM_THREADS=6 LEAN_PATH="$LP" $LEAN "$cp" ) > "$S/audit_$2.out" 2>&1; echo "exit $?" >> "$S/audit_$2.out"
  echo "$2 wall $(( $(date +%s) - s ))s" >> "$OUT/times.txt"
  cp "$cp" "$S/audit_$2.out" "$OUT/"
}
for m in Conf2122Witness FrameF3 RStarSanity; do run $m $m "$(pr $m)"; done
run Conf2122Witness Conf2122Witness_negcontrol "
theorem auditPlanted : SimpleGraph.Witness2122.sphericalMap.Conf2122Free := sorry"
date '+end %F %T %Z' >> "$OUT/times.txt"
