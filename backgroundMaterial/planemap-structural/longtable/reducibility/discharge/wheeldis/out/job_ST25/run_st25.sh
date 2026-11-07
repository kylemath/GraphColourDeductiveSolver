#!/bin/bash
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json
RPATN=$R F2BRULES=$F ARGSF=/tmp/swarm-W17/args_A97F_W13K3f_x_studio.txt EXPECT_PAT=18136,689,158 TAG=sol_rep2f_082_zK3f_A5F nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_rep2f_082.json 8 > /tmp/swarm-W17/st25_main.out 2>&1
RPATN=$R F2BRULES=$F ARGSF=/tmp/swarm-W17/args_A97F_W13K3e_x_studio.txt EXPECT_PAT=18136,688,158 TAG=sol_rep2f_082_zK3e_neg nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_rep2f_082.json 8 > /tmp/swarm-W17/st25_neg.out 2>&1
echo DONE > /tmp/swarm-W17/st25.done
