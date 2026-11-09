#!/bin/bash
# ST-88 T6: no-payer-8/9 regression of code_gk8 (check8.sh) on the ST-86 point, K3l5j + 260 keys, 4 processes, nice 20.
cd /tmp/swarm-W17 && GK=/tmp/swarm-W17/tab/cg_keys_r13w16_16fikp.txt RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
  F2BRULES=/tmp/swarm-W17/tab/rules_A5final_2db75746.json ARGSF=/tmp/swarm-W17/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 \
  TAG=sol_repK1MW_04__K3l5j_k260_gk8_regr W17NICE=20 nice -n 20 bash /tmp/swarm-W17/check8.sh /tmp/swarm-W17/sol/sol_repK1MW_04__K3l5j_k260.json 4
