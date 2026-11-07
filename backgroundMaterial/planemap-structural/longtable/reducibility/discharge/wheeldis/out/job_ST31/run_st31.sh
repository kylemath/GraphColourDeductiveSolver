#!/bin/bash
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json; A=/tmp/swarm-W17/args_A97F_W13K3j_x_studio.txt
GK=/tmp/swarm-W17/tab/cg_keys_r13w16.txt RPATN=$R F2BRULES=$F ARGSF=$A EXPECT_PAT=18136,692,158 TAG=sol_repS2W_04_zK3j_w16 nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS2W_04.json 8 > /tmp/swarm-W17/st31_main.out 2>&1
GK=/tmp/swarm-W17/tab/cg_keys_r13.txt RPATN=$R F2BRULES=$F ARGSF=$A EXPECT_PAT=18136,692,158 TAG=sol_repS2W_04_zK3j_r13neg nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_repS2W_04.json 8 > /tmp/swarm-W17/st31_neg.out 2>&1
echo DONE > /tmp/swarm-W17/st31.done
