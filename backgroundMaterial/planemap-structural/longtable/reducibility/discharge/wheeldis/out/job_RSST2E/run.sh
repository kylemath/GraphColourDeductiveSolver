#!/bin/bash
# RSST-2E: second-engine pass of the 51 RSST "none" configs with RSST's own X: cfast --fixed X --nogonthier (admissibility ignored), kc -x (listed X only, no search). nice 20.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/job_RSST2E
CF=$W/../studio15/cfast; KC=$W/loop/kc/kc; mkdir -p $J/one
: > $J/cfast.out
while read -r line; do n=$(echo "$line" | awk '{print $1}'); X=$(grep "^$n " $J/in/none51_x.txt | sed 's/.*{//; s/}.*//'); echo "$line" > $J/one/$n.in
  echo "== $n X=$X" >> $J/cfast.out; nice -n 20 $CF $J/one/$n.in --fixed "$X" --nogonthier >> $J/cfast.out 2>&1; done < $J/in/none51.txt
nice -n 20 $KC -t 600 -x $J/in/none51_x.txt $J/in/none51.txt > $J/kc.out 2>&1
echo RSSTDONE
