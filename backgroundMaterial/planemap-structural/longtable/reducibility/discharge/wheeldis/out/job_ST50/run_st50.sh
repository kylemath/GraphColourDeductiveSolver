#!/bin/bash
# ST-43; afterwards restart the ST-42 K5 screen (paused for this run) with 6 procs
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json; G=/tmp/swarm-W17/tab/cg_keys_r13w16.txt
AL=/tmp/swarm-W17/args_A97F_W13K3l_x_studio.txt; AK=/tmp/swarm-W17/args_A97F_W13K3k_x_studio.txt
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AL EXPECT_PAT=18136,694,158 TAG=sol_repS1MW_02_zK3l_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS1MW_02.json 8 > /tmp/swarm-W17/st50_main.out 2>&1
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AL EXPECT_PAT=18136,694,158 TAG=sol_repS1MW_02_tneg_zK3l_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS1MW_02_tneg.json 8 > /tmp/swarm-W17/st50_tneg.out 2>&1
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AK EXPECT_PAT=18136,693,158 TAG=sol_repS1MW_02_zK3k_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS1MW_02.json 8 > /tmp/swarm-W17/st50_K3k.out 2>&1
echo DONE > /tmp/swarm-W17/st50.done
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd $W/out/job_K5; mv run.log run3.log; SKIP=$PWD/skip_K5.txt KC=$W/loop/kc/kc DF18=$W/out/job52/dfast18 CF=$W/../studio15/cfast nohup bash runk5.sh 2 > run.log 2>&1 &
