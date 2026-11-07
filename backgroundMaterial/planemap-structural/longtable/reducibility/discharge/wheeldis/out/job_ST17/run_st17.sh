#!/bin/bash
while [ ! -f /tmp/swarm-W17/st16.done ]; do sleep 20; done
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; A5=/tmp/swarm-W17/tab/rules_c67fa1d1_plus_A5_twins.json
RPATN=$R F2BRULES=$A5 ARGSF=/tmp/swarm-W17/args_A97F_W13K3c_x_studio.txt EXPECT_PAT=18134,688,158 TAG=sol_crep_qC_zW13K3c_A5 nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qC.json 8 > /tmp/swarm-W17/st17_main.out 2>&1
RPATN=$R F2BRULES=$A5 ARGSF=/tmp/swarm-W17/args_A97F_W13K3c_noC_x_studio.txt EXPECT_PAT=18134,687,158 TAG=sol_crep_qC_noK3cC_neg nice -n 20 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qC.json 8 > /tmp/swarm-W17/st17_neg.out 2>&1
echo DONE > /tmp/swarm-W17/st17.done
