#!/bin/bash
# ST-48: K3l5 + 240 keys; afterwards restart ST-42 at 2 procs (maclane lanes keep their cores)
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json; G=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt
A=/tmp/swarm-W17/args_A97F_W13K3l5_x_studio.txt
GK=$G RPATN=$R F2BRULES=$F ARGSF=$A EXPECT_PAT=18137,699,158 TAG=sol_S4W09k240_zK3l5_k240 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_S4W09k240.json 8 > /tmp/swarm-W17/st48_main.out 2>&1
GK=$G RPATN=$R F2BRULES=$F ARGSF=$A EXPECT_PAT=18137,699,158 TAG=sol_S4W09k240_tneg_zK3l5_k240 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_S4W09k240_tneg.json 8 > /tmp/swarm-W17/st48_tneg.out 2>&1
echo DONE > /tmp/swarm-W17/st48.done
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd $W/out/job_K5; mv run.log run5.log; SKIP=$PWD/skip_K5.txt KC=$W/loop/kc/kc DF18=$W/out/job52/dfast18 CF=$W/../studio15/cfast nohup bash runk5.sh 2 > run.log 2>&1 &
