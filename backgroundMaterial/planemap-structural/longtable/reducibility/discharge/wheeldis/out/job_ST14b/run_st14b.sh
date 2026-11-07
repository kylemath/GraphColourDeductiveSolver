#!/bin/bash
# wait for ST-14 (main + control) to finish, then ST-14b main, then its control
while [ ! -f /tmp/swarm-W17/st14.done ]; do sleep 20; done
cd /tmp/swarm-W17
RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt F2BRULES=/tmp/swarm-W17/tab/rules_studio_keep95p131f_W18strict.json ARGSF=/tmp/swarm-W17/args_A97F_W13K3b_x_studio.txt EXPECT_PAT=18133,687,158 TAG=sol_crep_qM_zW13K3b nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qM.json 8 > /tmp/swarm-W17/st14b_main.out 2>&1
RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt F2BRULES=/tmp/swarm-W17/tab/rules_studio_keep95p131f_W18strict.json ARGSF=/tmp/swarm-W17/args_A97F_W13K3_x_studio.txt EXPECT_PAT=18130,686,158 TAG=sol_crep_qM_zW13K3_neg nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qM.json 8 > /tmp/swarm-W17/st14b_neg.out 2>&1
echo DONE > /tmp/swarm-W17/st14b.done
