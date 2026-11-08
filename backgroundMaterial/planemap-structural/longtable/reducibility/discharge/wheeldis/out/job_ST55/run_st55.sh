#!/bin/bash
# ST-52; afterwards restart ST-42 at 2 procs
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json
AL=/tmp/swarm-W17/args_A97F_W13K3l_x_studio.txt; A5=/tmp/swarm-W17/args_A97F_W13K3l5_x_studio.txt
G=/tmp/swarm-W17/tab/cg_keys_r13w16.txt; G240=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AL EXPECT_PAT=18136,694,158 TAG=sol_repS1MW_11_zK3l_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS1MW_11.json 8 > /tmp/swarm-W17/st55_main.out 2>&1
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AL EXPECT_PAT=18136,694,158 TAG=sol_repS1MW_11_tneg_zK3l_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS1MW_11_tneg.json 8 > /tmp/swarm-W17/st55_tneg.out 2>&1
GK=$G240 RPATN=$R F2BRULES=$F ARGSF=$A5 EXPECT_PAT=18137,699,158 TAG=sol_repS1MW_11_zK3l5_k240 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS1MW_11.json 8 > /tmp/swarm-W17/st55_K3l5.out 2>&1
echo DONE > /tmp/swarm-W17/st55.done
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd $W/out/job_K5; mv run.log run11.log; SKIP=$PWD/skip_K5.txt KC=$W/loop/kc/kc DF18=$W/out/job52/dfast18 CF=$W/../studio15/cfast nohup bash runk5.sh 2 > run.log 2>&1 &
