#!/bin/bash
# ST-108 T4: no-HATBB regression of code_gk9 (check9.sh) on sol_k86MS5_in07__K3l5j (dd2fcc97), K3l5j + the 240 keys of
# tab/cg_keys_r13w16_16fik.txt (no HAT line), 2 processes, nice 20. Reference: the code_gk7 run of the same point and family,
# job_ST79/st79_main.out (tag sol_k86MS5_in07__K3l5j_zK3l5j_k240).
cd /tmp/swarm-W17 && GK=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
  F2BRULES=/tmp/swarm-W17/tab/rules_A5final_2db75746.json ARGSF=/tmp/swarm-W17/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 \
  TAG=sol_k86MS5_in07__K3l5j_k240_gk9_regr_st108 W17NICE=20 nice -n 20 bash /tmp/swarm-W17/check9.sh /tmp/swarm-W17/sol/sol_k86MS5_in07__K3l5j.json 2
