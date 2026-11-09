#!/bin/bash
# maclane k5g add-on stop: stops an upper lane k86MS<n> (n >= 2: k86MS2 of the k5e add-on or a lane of launch_upper_fam.sh).  Watchers
# first (watch86_k5e, tightwatch_k5e: no new checks start), then the ladder, the tighten runs and the lane's upperR2 checks, then the K run;
# then the outbox poller, followed by one last outbox pass under the lane's own family (outbox86_fam.py <tag> <suffix> once).
# usage: bash stop_fam.sh [tag]   (default: the newest k86MS<n> lane in run.log; k86MS1: bash stop.sh upper; v2d1: a side lane k86MK<n> by name)
# Results already written stay: cand/, outbox/upper/, runK_<tag>/K.log, eng_p1r/rows_<tag>.txt.  Hand-started rechecks and the other
# lanes are not touched.
R=/tmp/maclane-k86
N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
SD=$R/fs/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sD
PATH=$R/macshim:$PATH; export PATH
read LT LS MX LIP LLA <<< "$(python3 $N/fam_lib.py lane)"
TM=${1:-$LT}; RF=${REPL_FAM:-MW}
case "$TM" in k86MS1) echo "stop_fam: k86MS1 is stopped with: TAG_UPPER=k86MS1 bash $R/stop.sh upper" >&2; exit 2;; k86MS[0-9]*|k86MK[0-9]*) ;; *) echo "stop_fam: no k86MS<n> / k86MK<n> lane to stop (run.log: $LT)" >&2; exit 2;; esac
T2=$(echo $TM | sed 's/.*\(..\)$/\1/')
# the lane's family: from its newest start line
SX=$(grep "\[s86K-$TM\] start " $N/run.log 2>/dev/null | tail -1 | sed -n 's/.* ARGS=args_A97_F_W13K3gB5\([A-Za-z0-9]*\)\.txt .*/\1/p')
kill_tree() {   # children first (BSD / GNU pgrep -P)
  local c
  for c in $(pgrep -P $1 2>/dev/null); do kill_tree $c; done
  kill $1 2>/dev/null
}
stop_pat() {
  local p n=0
  for p in $(pgrep -f "$1" 2>/dev/null); do [ "$p" = "$$" ] && continue; kill_tree $p; n=$((n + 1)); done
  [ $n -gt 0 ] && echo "  stopped $n: $1"
  return 0
}
echo "upper lane $TM (family ${SX:-?}):"
stop_pat "watch86_k5e.sh $TM( |$)"; stop_pat "tightwatch_k5e.sh $TM( |$)"; stop_pat "repladder_k5e.py $TM "
stop_pat "tighten_k5e.sh $N/cand/sol_(${TM}_in|rep${T2}${RF}_)"
stop_pat "U86e.sh (sol_${TM}_in|F_rep${T2}${RF}_|F_${TM}_in)"; stop_pat "work=$SD/wr86r_(sol_${TM}_in|F_rep${T2}${RF}_|F_${TM}_in)"
stop_pat "runK86p.sh [0-9]+ [0-9]+ $TM "; stop_pat "tag=$TM "
stop_pat "outbox86_k5e.py $TM( |$)"; stop_pat "outbox86_fam.py $TM "
sleep 2
if [ -n "$SX" ]; then (cd $N && python3 $N/outbox86_fam.py $TM $SX once | sed 's/^/  last outbox pass: /')
else echo "  no start line of $TM in run.log: no last outbox pass"; fi
left=$(pgrep -f "tag=$TM " 2>/dev/null | wc -l | tr -d ' ')
echo "processes of $TM still running: $left"
exit 0
