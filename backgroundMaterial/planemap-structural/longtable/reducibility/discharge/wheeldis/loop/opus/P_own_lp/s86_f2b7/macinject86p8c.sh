#!/bin/bash
# 9 Nov 23:00Z copy (8c): a check with no verdict (OOM-killed) is not marked done and is retried next cycle.
# 9 Nov 20:40Z copy for GS16: also picks the Mac lane points named sol_k86MK*__K3l5j* (ST-89 in08 was missed by sol_rep* only).
# eng_p8 copy (9 Nov 17:40Z) of macinject86.sh: every eng_p1r replaced by eng_p8 (payer-8/9 keys, PAYER8SPEC W5).
# s86 (9 Nov 13:35Z): feed the Mac lanes' Studio-checked points to a container upper run.  Every 5 min: each new
# from_studio/sol_rep*__K3l5j*/in/<name>.json (not _tneg) whose t is below the run's current in-point is checked here on the run's
# family + keys (U86, FIFO slot); FEASIBLE -> eng_p8/inject_<tag>.json (the K run takes it as its in-point when its t is lower).
# A K3l5j point with 240 or 260 keys should pass on K3gB5k/l + 260/280 (more kills, zero new keys); the check makes it certain.
# usage: ARGS=<run args> KEYS=<run keys> bash macinject86.sh <tag>      (stops when the run is gone)
N=$(cd $(dirname $0) && pwd); TAG=$1; S=/mnt/project-files/swarm/round6/W17-studio-kstar/from_studio; ST=$N/logs/macinject_$TAG.done; touch $ST
tin() { grep -o "t_in [0-9.]* -> [0-9.]*\|in-point: t_in = [0-9.]*" $N/runK_$TAG/K.log 2>/dev/null | tail -1 | grep -o "[0-9.]*$"; }   # empty until the run logs its in-point
while pgrep -f "tag=$TAG " > /dev/null; do
  for f in $(ls -d $S/sol_rep*__K3l5j* $S/sol_k86MK*__K3l5j* 2>/dev/null); do
    b=$(basename $f); j=$f/in/$b.json; [ -s $j ] || continue; grep -qx "$b" $ST && continue
    t=$(python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['t'])" $j 2>/dev/null) || continue
    ti=$(tin); [ -n "$ti" ] || continue
    python3 -I -c "import sys; sys.exit(0 if float(sys.argv[1]) < float(sys.argv[2]) - 1e-9 else 1)" $t $ti || { echo "$b" >> $ST; continue; }
    if true; then
      cp $j $N/cand/$b.json; tg=MI_${b#sol_}_$TAG
      E86OVR=$N/eng_p8 STACK=s77 ARGS=$ARGS KEYS=$KEYS bash $N/U86.sh $tg $N/cand/$b.json 2 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt > /dev/null 2>&1
      v=$(grep "\[s86U-$tg\] STACK" $N/run.log | tail -1 | grep -o "UPPER-R2: [A-Z]*"); [ -n "$v" ] || { echo "$(date -u +%H:%M:%SZ) [s86MI-$TAG] $b check gave no verdict (killed?); retry next cycle" >> $N/run.log; continue; }
      if [ "$v" = "UPPER-R2: FEASIBLE" ]; then
        cp $N/cand/$b.json $N/eng_p8/inject_$TAG.json.tmp && mv $N/eng_p8/inject_$TAG.json.tmp $N/eng_p8/inject_$TAG.json
        echo "$b" >> $ST; echo "$(date -u +%H:%M:%SZ) [s86MI-$TAG] $b (t $t < t_in $ti) FEASIBLE on $(basename $ARGS) + $(basename $KEYS) -> inject_$TAG.json" >> $N/run.log
      else echo "$b" >> $ST; echo "$(date -u +%H:%M:%SZ) [s86MI-$TAG] $b (t $t) $v on $(basename $ARGS) + $(basename $KEYS); not injected" >> $N/run.log; fi
    fi
  done; sleep 300
done
