#!/bin/bash
# J12: the audit's extended check (message 2026-10-06_1618_audit_..._RStarFrame-statement-PASS-and-J12-extended.md, section 3),
# J11 procedure. Every lean process is capped at 1800 CPU-s (ulimit -t is per process; a capped module is INCONCLUSIVE).
B=$HOME/mathlib4-planemap-build
cd "$HOME/studio-scratch/main-wt2/SolvingFrameworkPlan/docs/working/StudioMathLean" || exit 1
OUT=$HOME/studio-scratch/j12/out; mkdir -p "$OUT"
W=$HOME/studio-scratch/j12/w; mkdir -p "$W"
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3; LEAN=$TC/bin/lean
P=Mathlib/Combinatorics/SimpleGraph/PlaneMap
date '+start %F %T %Z' > "$OUT/times.txt"
git rev-parse HEAD > "$OUT/commit.txt"
( ulimit -t 1800; zsh ./check.sh "$B" "$W" ) > "$OUT/check-sh.txt" 2>&1; echo "exit $?" >> "$OUT/check-sh.txt"
LP=$W:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
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
FrameF3) echo '
#print SimpleGraph.SphericalMap.RStarFrame
#print SimpleGraph.SphericalMap.DiamondFree
#print SimpleGraph.SphericalMap.Conf2122Free
#check @SimpleGraph.SphericalMap.four_color_of_RStarFrame
#check @SimpleGraph.SphericalMap.rStarFrame_of_noSepTri
#print axioms SimpleGraph.SphericalMap.four_color_of_RStarFrame
#print axioms SimpleGraph.SphericalMap.rStarFrame_of_noSepTri' ;;
DiamondMOcc) echo '
#print SimpleGraph.SphericalMap.DiamondM.Occ
#check @SimpleGraph.SphericalMap.DiamondM.colorable_of_occ
#print axioms SimpleGraph.SphericalMap.DiamondM.colorable_of_occ' ;;
C2122MOcc) echo '
#print SimpleGraph.SphericalMap.C2122M.Occ
#check @SimpleGraph.SphericalMap.C2122M.colorable_of_occ
#print axioms SimpleGraph.SphericalMap.C2122M.colorable_of_occ' ;;
RStarSanity) echo '
#check @SimpleGraph.Icosahedron.occ_DiamondM
#check @SimpleGraph.Icosahedron.occ_DiamondP
#check @SimpleGraph.Icosahedron.not_diamondFree
#check @SimpleGraph.Icosahedron.conf2122Free' ;;
RadiusFive) echo '
#check @SimpleGraph.RadiusFive.R80.pureFill
#check @SimpleGraph.RadiusFive.R91.pureFill' ;;
esac; }

run() {  # $1 module, $2 copy name, $3 extra text before the sweep
  local cp=/tmp/audit_$2.lean
  cp "$P/$1.lean" "$cp"; printf '%s\n' "$3" >> "$cp"; printf '%s\n' "$SWEEP" >> "$cp"
  local s=$(date +%s)
  (cd "$OUT" && ( ulimit -t 1800; nice -n 10 env LEAN_PATH="$LP" $LEAN "$cp" ) > "/tmp/audit_$2.out" 2>&1; echo "exit $?" >> "/tmp/audit_$2.out")
  echo "$2 wall $(( $(date +%s) - s ))s" >> "$OUT/times.txt"
  cp "$cp" "/tmp/audit_$2.out" "$OUT/"
}
for m in RingJordan RingChains RingReduce DiamondCert Conf2122Cert OccToRing DiamondMCert DiamondMOcc DiamondPCert DiamondPOcc C2122MCert C2122MOcc C2122PCert C2122POcc FrameF3 RStarSanity RadiusFive; do
  run $m $m "$(pr $m)"
done
run FrameF3 FrameF3_negcontrol "
theorem auditPlanted : (1:ℕ) = 2 := sorry"
date '+end %F %T %Z' >> "$OUT/times.txt"
