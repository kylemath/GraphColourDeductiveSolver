#!/bin/bash
while [ ! -f /tmp/swarm-W17/st25.done ]; do sleep 20; done
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json; A=/tmp/swarm-W17
run() { RPATN=$R F2BRULES=$F ARGSF=$A/$2 EXPECT_PAT=$3 TAG=$4 nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/$1.json 8 > /tmp/swarm-W17/$4.out 2>&1; }
run sol_rep2e_082 args_A97F_W13K3e_x_studio.txt 18136,688,158 sol_rep2e_082_zK3e_A5F
run sol_rep2e_082 args_A97F_W13K3d_x_studio.txt 18135,688,158 sol_rep2e_082_zK3d_neg
echo DONE > /tmp/swarm-W17/st24.done
run sol_repFSD_03 args_A97F_W13K3d_x_studio.txt 18135,688,158 sol_repFSD_03_zK3d_A5F
run sol_repFSD_03 args_A97F_W13K3c_x_studio.txt 18134,688,158 sol_repFSD_03_zK3c_neg
echo DONE > /tmp/swarm-W17/st27.done
