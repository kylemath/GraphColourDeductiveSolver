#!/bin/bash
# main oracle chain: rounds 2..6 after round 1 (round.sh 1) has written r1_Ldone.txt. Deadline 22:13Z (4 h from start).
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s27o/env.sh
cd $S; DL=$(date -u -d "2026-10-19 22:13:00" +%s)
until [ -f r1_Ldone.txt ]; do sleep 20; done
WARM=$WARM0
for k in 2 3 4 5 6; do
  p=$((k-1))
  python3 -c "import json,sys; t=json.load(open('sol_r${p}L.json'))['t']; sys.exit(0 if t>1e-9 else 1)" || { echo "t<=0 at round $p"; break; }
  WARM=$S/rows_r$p.txt,$WARM
  python3 addforbid.py forbid_r$p.txt cert_r${p}L.json forbid_r$k.txt round$k > addforbid_r$k.log
  now=$(date +%s); rem=$((DL - now))
  [ $rem -lt 2700 ] && { echo "out of time before round $k"; break; }
  TL=$((rem - 2700)); [ $TL -gt 3600 ] && TL=3600
  echo "round $k start $(date -u +%H:%M:%SZ) tlimit $TL"
  ./round.sh $k $WARM $S/forbid_r$k.txt $TL
done
echo MAINDONE $(date -u +%H:%M:%SZ)
