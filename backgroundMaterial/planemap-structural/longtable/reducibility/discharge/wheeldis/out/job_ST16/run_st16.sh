#!/bin/bash
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; A5=/tmp/swarm-W17/tab/rules_c67fa1d1_plus_A5_twins.json; C67=/tmp/swarm-W17/tab/rules_studio_keep95p131f_W18strict.json
RPATN=$R F2BRULES=$A5 ARGSF=/tmp/swarm-W17/args_A97F_W13K3b_x_studio.txt EXPECT_PAT=18133,687,158 TAG=sol_crep_qA_zW13K3b_A5 nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qA.json 8 > /tmp/swarm-W17/st16_main.out 2>&1
RPATN=$R F2BRULES=$C67 ARGSF=/tmp/swarm-W17/args_A97F_W13K3b_x_studio.txt EXPECT_PAT=18133,687,158 TAG=sol_crep_qA_zW13K3b_c67neg nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qA.json 8 > /tmp/swarm-W17/st16_negA.out 2>&1
RPATN=$R F2BRULES=$A5 ARGSF=/tmp/swarm-W17/args_A97F_W13K3_x_studio.txt EXPECT_PAT=18130,686,158 TAG=sol_crep_qA_zW13K3_A5neg nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qA.json 8 > /tmp/swarm-W17/st16_negB.out 2>&1
echo DONE > /tmp/swarm-W17/st16.done
