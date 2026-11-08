# maclane k5g add-on: start an upper lane k86MS<n> on the family of suffix x: launch_k86MS2.sh (k5e add-on) with the families, the tag and
# the previous lane as parameters, so every later binder kill needs only a data add-on (fam/FAMILIES.txt line + kill file + 2 args).
#   LP      K3gB5x = args_A97_F_W13K3gB5x.txt + keys p1r/cg_keys_r13w16_16fik.txt (240, 3d996dbb, standard coefficients) on eng_p1r:
#           p1r/runK86p.sh <maxit> <threads> <tag> inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols
#           feasall consk=20 consfrac=0.25   (the flags of k86MS2 and of the container's k86GS9)
#   checks  K3l5x = args_A97_F_W13K3l5x.txt + the 240 keys on eng_p1r: in-points (watch86_k5e.sh, WATCH_ARGS), ladder sub-checks
#           (repladder_k5e.py: main check on K3gB5x decides the new in-point; REPL_ARGS2 = K3l5x), tightening (tightwatch_k5e.sh /
#           tighten_k5e.sh, ARGS = K3l5x, engine eng_p1t)
#   outbox  outbox86_fam.py <tag> x: <name>__K3l5x (ladder points FEASIBLE only on the LP family: <name>__K3gB5x), family in POINTS.txt
# Warm: the previous lane's warm list (runK_<prev>/warmlist.txt, else maclane_warm_upper.txt) + the complete lines of its rows
#   (eng_p1r/rows_<prev>.txt, k86MS1: eng/rows_k86MS1.txt -> warm/rows_<prev without k86>_snap_<tag>.txt); rows the family does not
#   admit are dropped on admission (K.log 'warm rows admitted').  A restart of the same tag: its previous warm list + the complete lines of
#   its own rows (warm/rows_<tag>_snap_<UTC>.txt); its K.log is kept as runK_<tag>/K_prev_<UTC>.log.
# usage: TAG=k86MS<n> PREV_TAG=<lane before it, or the same tag on a restart> FAM_SUFFIX=<x> bash launch_msfam.sh <in-point json>
#   (launch_upper_fam.sh sets these, stops the previous lane and picks the in-point).  The in-point must be upperR2 FEASIBLE on K3l5x +
#   the 240 keys on this machine (a run.log check of this exact file: fam_lib.py verified x <json>).
# Knobs (env): UPPER_THREADS / MAXIT / REPL_PAR (default: the previous lane's, from run.log; else 2 / 200 / 2), REPL_MINMEM (0),
#   TIGHTWATCH (1), TIGHT_MINMEM (0), HSHIM_SOLVER, DRY=1 (print what would start, start nothing).
R=/tmp/maclane-k86
N=/tmp/maclane-k86/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; B=$(dirname $N)
PATH=$R/macshim:$PATH; export PATH
TAG=$TAG; TP=$PREV_TAG; X=$FAM_SUFFIX; DRY=${DRY:-0}; FEAS=$1; S=$(date -u +%Y%m%dT%H%MZ)
die() { echo "launch_msfam: $1" >&2; exit $2; }
[ -n "$TAG" ] && [ -n "$TP" ] && [ -n "$X" ] || die "TAG, PREV_TAG and FAM_SUFFIX must be set (bash $R/launch_upper_fam.sh <suffix> sets them)" 2
case "$TAG" in k86MS[0-9]*) ;; *) die "TAG must be k86MS<n>, not $TAG" 2;; esac
[ -n "$FEAS" ] && [ -f "$FEAS" ] || die "usage: TAG=.. PREV_TAG=.. FAM_SUFFIX=.. bash launch_msfam.sh <in-point json>  (or bash $R/launch_upper_fam.sh <suffix>)" 2
[ "${FEAS#/}" != "$FEAS" ] || FEAS=$(cd "$(dirname "$FEAS")" && pwd -P)/$(basename "$FEAS")
for b in jsepf_gk_k192 jsepf_gk jsep3; do [ -x $N/eng_p1r/bin/$b ] || die "eng_p1r/bin/$b missing: run build.sh first" 2; done
for f in $N/U86e.sh $N/p1r/runK86p.sh $N/p1r/cg_keys_r13w16_16fik.txt $N/repladder_k5e.py $N/outbox86_fam.py $N/fam_lib.py $N/k5e_lib.py \
         $N/watch86_k5e.sh $N/tightwatch_k5e.sh $N/tighten_k5e.sh $N/mkeng_p1t.sh $N/maclane_warm_upper.txt; do
  [ -f $f ] || die "$f missing: install the v2, k5d, k5e and k5g add-ons" 2; done
FC=$(python3 $N/fam_lib.py famcheck $X quiet) || die "family $X: $FC" 2
LPA=$(echo "$FC" | sed -n 's/.* gb=\([^ ]*\) .*/\1/p'); QA=$(echo "$FC" | sed -n 's/.* l=\([^ ]*\) .*/\1/p')
[ "${LP_ON_CHECK:-0}" = 1 ] && LPA=$QA   # v2c (Opus 8 Nov 22:00Z): LP on the check family K3l5x, so every ladder / in-point is a checkable upper (K3gB5x carries the 159 K3g-only kills, [E2] but not in Lean)
cmd5() { python3 -c "import sys, hashlib; print(hashlib.md5(open(sys.argv[1], 'rb').read().replace(sys.argv[2].encode() + b'/fs/', b'/')).hexdigest()[:8])" "$1" "$R"; }
pgrep -f "tag=$TAG " > /dev/null && die "a run with tag=$TAG is already going (bash $R/stop_fam.sh $TAG first)" 3
if [ "$TP" != "$TAG" ]; then
  if pgrep -f "tag=$TP " > /dev/null || pgrep -f "outbox86(_k5e|_fam)?(\.sh|\.py) $TP" > /dev/null || pgrep -f "repladder(_k5e)?\.py $TP" > /dev/null; then
    if [ "$DRY" = 1 ]; then echo "launch_msfam: (dry) $TP is still running; launch_upper_fam.sh stops it first"
    else die "$TP (or its outbox / repladder) is still running: stop it first (bash $R/launch_upper_fam.sh does)" 3; fi
  fi
fi
if V=$(python3 $N/fam_lib.py verified $X $FEAS); then :
elif [ "$DRY" = 1 ]; then echo "launch_msfam: (dry) $(basename $FEAS) has no FEASIBLE K3l5$X check here yet (launch_upper_fam.sh rechecks it first)"; V="- (to-be-rechecked) -"
else die "in-point $FEAS is not upperR2 FEASIBLE on K3l5$X + 240 keys on this machine ($V): bash $R/recheck_fam.sh $X $FEAS" 2; fi
TIN=$(echo "$V" | awk '{print $3}'); MIN=$(md5sum < $FEAS | cut -c1-8)
if [ "${TIGHTWATCH:-1}" != 0 ]; then bash $N/mkeng_p1t.sh || die "eng_p1t could not be made (TIGHTWATCH=0 runs without tightening)" 2; fi
# the previous lane's settings, from its run.log lines (env overrides)
L1=$(grep "\[s86K-$TP\] start " $N/run.log 2>/dev/null | tail -1); L2=$(grep "\[maclane\] launch $TP[: ]" $N/run.log 2>/dev/null | tail -1)
MI0=$(echo "$L1" | sed -n 's/.* maxit \([0-9]*\) threads [0-9]* .*/\1/p'); TH0=$(echo "$L1" | sed -n 's/.* maxit [0-9]* threads \([0-9]*\) .*/\1/p')
RP0=$(echo "$L2" | sed -n 's/.* REPL_PAR \([0-9]*\),.*/\1/p')
TH=${UPPER_THREADS:-${TH0:-2}}; MI=${MAXIT:-${MI0:-200}}; RP=${REPL_PAR:-${RP0:-2}}
export STACK=s77 ARGS=$LPA KEYS=$N/p1r/cg_keys_r13w16_16fik.txt FEAS
export XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
# warm
mkdir -p $N/warm $N/logs $N/cand $N/runK_$TAG
if [ -s $N/runK_$TAG/warmlist.txt ]; then WARM=$(cat $N/runK_$TAG/warmlist.txt); WS="the previous $TAG run's warm list"
else
  if [ -s $N/runK_$TP/warmlist.txt ]; then WARM=$(cat $N/runK_$TP/warmlist.txt); WS="$TP's warm list (runK_$TP/warmlist.txt)"
  else WARM=$(cat $N/maclane_warm_upper.txt); WS="maclane_warm_upper.txt"; fi
  RW=""; for r in $N/eng_p1r/rows_$TP.txt $N/eng/rows_$TP.txt; do [ -s $r ] && { RW=$r; break; }; done
  if [ -n "$RW" ]; then
    WP=$N/warm/rows_${TP#k86}_snap_$TAG.txt   # (no 'k86<prev>' in this lane's command line: pgrep -f <prev tag> never lists it)
    [ "$DRY" = 1 ] || python3 $N/k5e_lib.py snaprows $RW $WP > /dev/null
    WARM=$WARM,$WP; WS="$WS + $TP's rows ($(basename $(dirname $RW))/$(basename $RW))"
  fi
fi
if [ -s $N/eng_p1r/rows_$TAG.txt ]; then
  [ "$DRY" = 1 ] || python3 $N/k5e_lib.py snaprows $N/eng_p1r/rows_$TAG.txt $N/warm/rows_${TAG}_snap_$S.txt > /dev/null
  WARM=$WARM,$N/warm/rows_${TAG}_snap_$S.txt; WS="$WS + the previous $TAG run's rows"
fi
WARM=$(echo "$WARM" | tr ',' '\n' | awk 'NF && !s[$0]++' | paste -s -d, -); export WARM
NW=$(echo "$WARM" | tr ',' '\n' | grep -c .); MISS=""
for w in $(echo "$WARM" | tr ',' ' '); do
  [ -e $w ] && continue
  [ "$DRY" = 1 ] && [ "${w%_snap_*}" != "$w" ] && continue   # (dry: snapshots are not made)
  MISS="$MISS $w"
done
[ -z "$MISS" ] || die "warm files missing:$MISS" 2
echo "launch_msfam: $TAG: LP $(basename $LPA) ($(cmd5 $LPA)) + $(basename $KEYS) ($(md5sum < $KEYS | cut -c1-8)) on eng_p1r; checks on $(basename $QA) ($(cmd5 $QA)); in-point $(basename $FEAS) (md5 $MIN, t $TIN; $(echo $V | awk '{print $2}')); maxit $MI, threads $TH, REPL_PAR $RP, tightwatch ${TIGHTWATCH:-1}; $NW warm files: $WS"
if [ "$DRY" = 1 ]; then
  echo "launch_msfam: (dry) would run: bash $N/p1r/runK86p.sh $MI $TH $TAG inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25"
  echo "launch_msfam: (dry) + watch86_k5e.sh $TAG (WATCH_ARGS $(basename $QA)), outbox86_fam.py $TAG $X, $( [ "${TIGHTWATCH:-1}" != 0 ] && echo "tightwatch_k5e.sh $TAG (ARGS $(basename $QA)), ")repladder_k5e.py $TAG (REPL_ARGS $(basename $LPA), REPL_ARGS2 $(basename $QA), REPL_PAR $RP)"
  exit 0
fi
if [ -s $N/runK_$TAG/K.log ]; then mv $N/runK_$TAG/K.log $N/runK_$TAG/K_prev_$S.log; fi
echo "$(date -u +%H:%M:%SZ) [maclane] launch $TAG (fam $X, after $TP): LP ARGS $(basename $LPA) (container md5 $(cmd5 $LPA)), keys $(basename $KEYS) ($(md5sum < $KEYS | cut -c1-8)), engine eng_p1r; in-points / ladder sub-checks / tightening on $(basename $QA) ($(cmd5 $QA)); in-point $(basename $FEAS) (md5 $MIN, t = $TIN, FEASIBLE on K3l5$X: $(echo $V | awk '{print $2}')), threads $TH, maxit $MI, REPL_PAR $RP, $NW warm files ($WS)" >> $N/run.log
nohup bash $N/p1r/runK86p.sh $MI $TH $TAG inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 > $N/logs/runK_$TAG.out 2>&1 &
sleep 5
cd $N && ENGD=eng_p1r WATCH_ARGS=$QA nohup bash $N/watch86_k5e.sh $TAG > $N/logs/watch86_$TAG.out 2>&1 &
cd $N && REPL_FAM=MW nohup python3 $N/outbox86_fam.py $TAG $X >> $N/logs/outbox86_$TAG.out 2>&1 &
if [ "${TIGHTWATCH:-1}" != 0 ]; then cd $N && ARGS=$QA REPL_FAM=MW nohup bash $N/tightwatch_k5e.sh $TAG >> $N/logs/tightwatch_$TAG.out 2>&1 & fi
cd $N && REPL_ENGD=eng_p1r REPL_FAM=MW REPL_ARGS=$LPA REPL_ARGS2=$QA REPL_KEYS=$KEYS REPL_PAR=$RP REPL_MINMEM=${REPL_MINMEM:-0} nohup python3 $N/repladder_k5e.py $TAG $FEAS 60 >> $N/logs/repladder_$TAG.out 2>&1 &
sleep 2; echo "launched $TAG (fam $X): K run log $N/runK_$TAG/K.log, outbox $R/outbox/upper/POINTS.txt (family column K3l5$X / K3gB5$X), status: bash $R/status_fam.sh, stop: bash $R/stop_fam.sh"
