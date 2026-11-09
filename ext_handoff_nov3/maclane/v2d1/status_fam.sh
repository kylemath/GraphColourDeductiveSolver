#!/bin/bash
# maclane k5g add-on status: the newest upper lane k86MS<n> (or the one named), its family, its processes, last iterations, ladder /
# tighten / in-point lines, and the outbox points by family; the families in fam/FAMILIES.txt.   usage: bash status_fam.sh [tag] [lines]
R=/tmp/maclane-k86
N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
SD=$R/fs/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sD
. $N/maclib.sh
read LT LS MX LIP LLA <<< "$(python3 $N/fam_lib.py lane)"
TM=${1:-$LT}; K=${2:-6}; O=$R/outbox/upper
SX=$(grep "\[s86K-$TM\] start " $N/run.log 2>/dev/null | tail -1 | sed -n 's/.* ARGS=args_A97_F_W13K3gB5\([A-Za-z0-9]*\)\.txt .*/\1/p')
up() { if pgrep -f "$1" > /dev/null 2>&1; then echo "running"; else echo "-"; fi; }
echo "== maclane fam $(date -u +%Y-%m-%dT%H:%M:%SZ)  load:$(uptime | sed 's/.*load average[s]*://')  available memory $(memavail_mb) MB"
echo "== families (fam/FAMILIES.txt): $(python3 $N/fam_lib.py families)"
echo "== UPPER $TM (family ${SX:-?}: LP K3gB5${SX}, checks K3l5${SX})   K run: $(up "tag=$TM ")  repladder: $(up "repladder_k5e.py $TM")  watch: $(up "watch86_k5e.sh $TM")  tightwatch: $(up "tightwatch_k5e.sh $TM")  outbox: $(up "outbox86_(k5e|fam).py $TM")  upperR2 checks now: $(pgrep -f "work=$SD/wr86r_" 2>/dev/null | wc -l | tr -d ' ')"
for t in $(grep -o '\[s86K-k86M[SK][0-9]*\] start' $N/run.log 2>/dev/null | sed 's/\[s86K-\(k86M[SK][0-9]*\)\].*/\1/' | awk '!s[$0]++'); do
  [ "$t" = "$TM" ] && continue; pgrep -f "tag=$t " > /dev/null && echo "   NOTE: $t is running too"; done
if [ -f $N/runK_$TM/K.log ]; then grep -E '^iter |in-point: t_in|warm rows admitted|^hshim: run|Traceback|Error' $N/runK_$TM/K.log | tail -n $K | cut -c1-220
else echo "  (no K.log yet)"; fi
echo "-- ladder / tighten / in-points (run.log, last $K):"
grep -E "\[s86REP-$TM\]|\[s86T\] tighten|\[watch86-$TM\]|\[maclane-outbox-$TM\]|\[maclane-outbox-fam|\[maclane\] fam: " $N/run.log 2>/dev/null | tail -n $K | cut -c1-240
if [ -f $O/POINTS.txt ]; then
  echo "-- outbox/upper/POINTS.txt by family: $(awk 'NF >= 5 {c[$4]++} END {for (f in c) printf "%s %d  ", f, c[f]}' $O/POINTS.txt); last $K:"
  tail -n $K $O/POINTS.txt
fi
echo "-- outbox/fam/RECHECK.txt (last $K):"
[ -f $R/outbox/fam/RECHECK.txt ] && tail -n $K $R/outbox/fam/RECHECK.txt
exit 0
