#!/bin/bash
# pool chain: nosep LP over a fixed row pool, forbid the binders of the previous pool cert, repeat (lower bounds only)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s27o/env.sh
cd $S; POOL=$1; prev=r1pre
for k in 2 3 4 5 6; do
  python3 addforbid.py forbid_p$((k-1)).txt cert_$prev.json forbid_p$k.txt pool$k > addforbid_p$k.log
  python3 pcheck.py solveR2 $F0 nosep tag=p$k $A $CB forbid=$S/forbid_p$k.txt warm=$POOL K=300 xcap=3 dcap=3 threads=1 work=$WK/p$k > p$k.log 2>&1
  python3 pcheck.py lowerR2 $F0 forbid=$S/forbid_p$k.txt cert=cert_p$k.json xcap=3 dcap=3 $A work=$WK/p$k > lower_p$k.log 2>&1
  date -u +%H:%M:%SZ > p${k}_done.txt
  python3 -c "import json,sys; t=json.load(open('sol_p$k.json'))['t']; sys.exit(0 if t>1e-9 else 1)" || break
  prev=p$k
done
