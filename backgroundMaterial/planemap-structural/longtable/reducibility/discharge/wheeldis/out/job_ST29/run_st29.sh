#!/bin/bash
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json
RPATN=$R F2BRULES=$F ARGSF=/tmp/swarm-W17/args_A97F_W13K3i_x_studio.txt EXPECT_PAT=18136,691,158 TAG=sol_k86GS_in01_zK3i_A5F nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_k86GS_in01.json 8 > /tmp/swarm-W17/st29_main.out 2>&1
RPATN=$R F2BRULES=$F ARGSF=/tmp/swarm-W17/args_A97F_W13K3f_x_studio.txt EXPECT_PAT=18136,689,158 TAG=sol_k86GS_in01_zK3f_neg nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_k86GS_in01.json 8 > /tmp/swarm-W17/st29_neg.out 2>&1
echo DONE > /tmp/swarm-W17/st29.done
