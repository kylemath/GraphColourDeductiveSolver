#!/bin/bash
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json; G=/tmp/swarm-W17/tab/cg_keys_r13w16.txt
AK=/tmp/swarm-W17/args_A97F_W13K3k_x_studio.txt; AJ=/tmp/swarm-W17/args_A97F_W13K3j_x_studio.txt
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AK EXPECT_PAT=18136,693,158 TAG=sol_repS3W_06_zK3k_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS3W_06.json 8 > /tmp/swarm-W17/st39_main.out 2>&1
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AJ EXPECT_PAT=18136,692,158 TAG=sol_repS3W_06_zK3j_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS3W_06.json 8 > /tmp/swarm-W17/st39_ctlA.out 2>&1
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AK EXPECT_PAT=18136,693,158 TAG=sol_repS3W_06_tneg_zK3k_w16 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS3W_06_tneg.json 8 > /tmp/swarm-W17/st39_ctlB.out 2>&1
echo DONE > /tmp/swarm-W17/st39.done
