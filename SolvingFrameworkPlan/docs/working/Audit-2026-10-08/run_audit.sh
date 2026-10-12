#!/bin/zsh
# Audit 2026-10-08: per-module audit copies (statement prints + axiom sweep), J12 procedure.
SP=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver/78bd1589-fda1-4d14-8502-268e6b6d2668/scratchpad
W=$SP/build; OUT=$SP/audit/out; mkdir -p $OUT
B=$HOME/mathlib4-planemap-build
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3; LEAN=$TC/bin/lean
R=/Users/kylemathewson/GraphColourDeductiveSolver/SolvingFrameworkPlan/docs/working
P=$R/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap
LP=$W:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
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
FrameNoFrozen) echo '
#print SimpleGraph.QuarterFloor.NoFrozenFrame
#print SimpleGraph.QuarterFloor.DLState
#print SimpleGraph.QuarterFloor.DoublyLocked
#check @SimpleGraph.QuarterFloor.rStarFrame_of_no_allDL_orbit
#check @SimpleGraph.QuarterFloor.four_color_of_no_allDL_orbit_frame
#check @SimpleGraph.QuarterFloor.pureClean_of_no_allDL_orbit' ;;
FrameScope) echo '
#print SimpleGraph.SphericalMap.FrameScope.LinkTipsClean
#check @SimpleGraph.SphericalMap.FrameScope.no_555_run
#check @SimpleGraph.SphericalMap.FrameScope.no_565_run' ;;
FrameWit22) echo '
#check @SimpleGraph.FrameWit22.frameClass_nonempty
#print SimpleGraph.SphericalMap.RStarFrame
example : SimpleGraph.SphericalMap.RStarFrame ↔ SimpleGraph.SphericalMap.RStarFrame := Iff.rfl' ;;
QuarterLockParity) echo '
#print SimpleGraph.QuarterFloor.Pent
#print SimpleGraph.QuarterFloor.RepeatAt
#print SimpleGraph.QuarterFloor.Lock1
#print SimpleGraph.QuarterFloor.Lock2
#print SimpleGraph.QuarterFloor.kcomp
#print SimpleGraph.QuarterFloor.boundaryCard
#print SimpleGraph.QuarterFloor.oddCount
#print SimpleGraph.VacancyShortFill.pairGraph
#print SimpleGraph.VacancyShortFill.Active
#print SimpleGraph.VacancySlide.ProperOff
#print SimpleGraph.SphericalMap.Triangulated
#check @SimpleGraph.QuarterFloor.lock2_iff_odd_boundary
#check @SimpleGraph.QuarterFloor.lock2_iff_odd_oddCount
#check @SimpleGraph.QuarterFloor.lock1_iff_odd_boundary
#check @SimpleGraph.QuarterFloor.lock1_iff_odd_oddCount
#check @SimpleGraph.QuarterFloor.alphaMu_odd_boundary
#check @SimpleGraph.QuarterFloor.alphaMu_odd_oddCount
#check @SimpleGraph.QuarterFloor.parity_alphaA' ;;
ChainCount) echo '
#print SimpleGraph.QuarterFloor.chainCount
#print SimpleGraph.QuarterFloor.nChains
#print SimpleGraph.QuarterFloor.RigidAt
#print SimpleGraph.QuarterFloor.ChainParityLaw
#check @SimpleGraph.QuarterFloor.eight_le_nChains
#check @SimpleGraph.QuarterFloor.rigidAt_iff' ;;
ChainMod4) echo '
#print SimpleGraph.QuarterFloor.fxor
#print SimpleGraph.QuarterFloor.isCW
#print SimpleGraph.QuarterFloor.FaceAvoids
#print SimpleGraph.QuarterFloor.cwAt
#print SimpleGraph.QuarterFloor.cwDarts
#print SimpleGraph.QuarterFloor.cwCount
#print SimpleGraph.QuarterFloor.linkInner
#print SimpleGraph.QuarterFloor.LinkBalanced
#print SimpleGraph.QuarterFloor.handB
#print SimpleGraph.QuarterFloor.handS
#print SimpleGraph.QuarterFloor.ChainFormulaF
#print SimpleGraph.QuarterFloor.ConjectureF
#print SimpleGraph.VacancyShortFill.Whole
#print SimpleGraph.QuarterFloor.StarHyp
#check @SimpleGraph.QuarterFloor.lemmaW
#check @SimpleGraph.QuarterFloor.lemmaW_linkFree
#check @SimpleGraph.QuarterFloor.cw_piMove' ;;
TutteSides) echo '
#print SimpleGraph.TutteSides.chainSpace
#print SimpleGraph.TutteSides.gammaM
#check @SimpleGraph.TutteSides.tutte_sides
#check @SimpleGraph.TutteSides.euler_tri' ;;
ChainF) echo '
#check @SimpleGraph.QuarterFloor.chainFormulaF
#check @SimpleGraph.QuarterFloor.conjectureF
#check @SimpleGraph.QuarterFloor.chainParityLaw_sphere
#check @SimpleGraph.QuarterFloor.rigid_isolation
#check @SimpleGraph.QuarterFloor.remark7
#print axioms SimpleGraph.QuarterFloor.lemmaW
#print axioms SimpleGraph.QuarterFloor.cw_piMove
#print axioms SimpleGraph.QuarterFloor.eight_le_nChains
#print axioms SimpleGraph.QuarterFloor.rigidAt_iff
#print axioms SimpleGraph.TutteSides.euler_tri
#print axioms SimpleGraph.TutteSides.tutte_sides' ;;
FrameWit22Map) echo '
#check @SimpleGraph.FrameWit22.sphericalMap_triangulated
#check @SimpleGraph.FrameWit22.fills' ;;
esac; }
run() { # $1 module, $2 copy name, $3 extra
  local cp=$OUT/audit_$2.lean
  cp "$P/$1.lean" "$cp"; printf '%s\n' "$3" >> "$cp"; printf '%s\n' "$SWEEP" >> "$cp"
  local s=$(date +%s)
  ( ulimit -t 1800; nice -n 10 env LEAN_PATH="$LP" $LEAN "$cp" ) > "$OUT/audit_$2.out" 2>&1; echo "exit $?" >> "$OUT/audit_$2.out"
  echo "$2 wall $(( $(date +%s) - s ))s" >> "$OUT/times.txt"
}
date '+start %F %T %Z' > $OUT/times.txt
for m in FrameNoFrozen FrameScope FrameWit22Map FrameWit22 QuarterLockParity ChainCount ChainMod4 TutteSides ChainF; do
  run $m $m "$(pr $m)"
done
run ChainF ChainF_negcontrol "
theorem auditPlanted : (1:ℕ) = 2 := sorry"
# challenges: copies with sweep
for c in RStarFrameChallenge RStarFrameBridge FourColorSphericalMapChallenge FourColorBridge; do
  cp $R/Challenges/$c.lean $OUT/audit_$c.lean; printf '%s\n' "$SWEEP" >> $OUT/audit_$c.lean
  ( ulimit -t 1800; nice -n 10 env LEAN_PATH="$LP" $LEAN $OUT/audit_$c.lean ) > $OUT/audit_$c.out 2>&1; echo "exit $?" >> $OUT/audit_$c.out
done
# non-vacuity
( ulimit -t 1800; nice -n 10 env LEAN_PATH="$LP" $LEAN $SP/audit/NonVacuity.lean ) > $OUT/NonVacuity.out 2>&1; echo "exit $?" >> $OUT/NonVacuity.out
date '+end %F %T %Z' >> $OUT/times.txt
