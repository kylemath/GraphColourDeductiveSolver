#!/bin/bash
cd /tmp/swarm-W17
for p in "sol_repGSG_06 sol_repGSG_06_zK3f_A5F" "sol_repGSG_06_tneg sol_repGSG_06_tneg_zK3f_A5F"; do set -- $p
RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt F2BRULES=/tmp/swarm-W17/tab/rules_A5final_2db75746.json ARGSF=/tmp/swarm-W17/args_A97F_W13K3f_x_studio.txt EXPECT_PAT=18136,689,158 TAG=$2 nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/$1.json 8 > /tmp/swarm-W17/st28_$1.out 2>&1
done
echo DONE > /tmp/swarm-W17/st28.done
