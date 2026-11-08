#!/bin/bash
# W17 harness (Studio K3l5g args 1bd9a34b + 240 keys) on the 7 MS3 points that fail K3l5g, to list the failing rows; ST-67 at 4 procs meanwhile
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; S=/tmp/swarm-W17/sol
[ -f $W/out/job_ST67/run.log ] && ! grep -q ALLDONE $W/out/job_ST67/run.log && bash $W/out/job_ST67/ctl.sh 4
OB=$HOME/maclane/maclane-k86/outbox/upper; for n in 03 04 05 06 07 08; do cp $OB/sol_repS3MW_${n}__K3gB5g.json $S/x_repS3MW_$n.json; done
cp $HOME/maclane/maclane-k86/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7/cand/sol_k86MS3_in10.json $S/x_k86MS3_in10.json
cd /tmp/swarm-W17; R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json; A=/tmp/swarm-W17/args_A97F_W13K3l5g_x_studio.txt; G=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt
for p in k86MS3_in10 repS3MW_08 repS3MW_07 repS3MW_06 repS3MW_05 repS3MW_04 repS3MW_03; do
  GK=$G RPATN=$R F2BRULES=$F ARGSF=$A EXPECT_PAT=18142,706,158 TAG=x_${p}_zK3l5g bash /tmp/swarm-W17/check.sh $S/x_$p.json 8 > /tmp/swarm-W17/xrows_$p.out 2>&1
  cat /tmp/swarm-W17/logs/x_${p}_zK3l5g/viol_d*.txt | grep -v "^#" | sort -u > $W/out/job_K3gB5g_extras/rows_$p.txt
  grep -E "^RESULT|exact violated [1-9]|senderR2 rows" /tmp/swarm-W17/xrows_$p.out | cut -c1-120 > $W/out/job_K3gB5g_extras/verdict_$p.txt
  cp /tmp/swarm-W17/xrows_$p.out $W/out/job_K3gB5g_extras/
done
echo DONE > /tmp/swarm-W17/xrows.done
[ -f $W/out/job_ST67/run.log ] && ! grep -q ALLDONE $W/out/job_ST67/run.log && bash $W/out/job_ST67/ctl.sh 8
