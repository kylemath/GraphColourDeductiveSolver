#!/bin/bash
# eng_p8 copy (9 Nov 17:40Z) of subchk86.sh: every eng_p1r replaced by eng_p8 (payer-8/9 keys, PAYER8SPEC W5).
# s86 (9 Nov 17:10Z): for each in-point a GS run files ([s86F-sol_<tag>_inNN] filed), recheck it with the run's keys on the smaller
# families in FAMS (default K3l5j = Lean-complete, then K3l5m) so we know whether it counts now; logs [s86SC-<tag>] lines.
# usage: KEYS=<run keys> [FAMS="K3l5j K3l5m"] bash subchk86.sh <tag>     (stops when the run is gone)
N=$(cd $(dirname $0) && pwd); TAG=$1; ST=$N/logs/subchk_$TAG.done; touch $ST; FAMS=${FAMS:-K3l5j K3l5m}; KL=$(basename $KEYS .txt)
while pgrep -f "tag=$TAG " > /dev/null; do
  for s in $(grep -o "\[s86F-sol_${TAG}_in[0-9]*\] filed" $N/run.log | grep -o "sol_${TAG}_in[0-9]*"); do
    grep -qx "$s" $ST && continue; echo "$s" >> $ST
    for F in $FAMS; do tg=F_${s#sol_}_${F}_${KL: -4}
      E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13$F.txt KEYS=$KEYS bash $N/U86.sh $tg $N/cand/$s.json 2 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt > /dev/null 2>&1
      v=$(grep "\[s86U-$tg\] STACK" $N/run.log | tail -1 | grep -o "UPPER-R2: [A-Z]* ([0-9]*)\|UPPER-R2: FEASIBLE"); vd=$(grep "^d=[0-9]*: [1-9]" $N/logs/upper_$tg.log | cut -d' ' -f1-3 | tr '\n' ' ')
      echo "$(date -u +%H:%M:%SZ) [s86SC-$TAG] $s on $F + $(basename $KEYS): $v $vd" >> $N/run.log
    done
  done; sleep 120
done
