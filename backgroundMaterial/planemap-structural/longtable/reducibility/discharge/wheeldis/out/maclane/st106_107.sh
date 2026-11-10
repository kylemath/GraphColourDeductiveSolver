#!/bin/bash
# coordinator 09:47Z: ST-106 (MK5 in-point, gk8, nonzero k268 keys) then ST-107 (MK4 in-point, gk7, nonzero 260 keys), sequential, on K3l5q
M=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/maclane
echo "=== ST-106"; bash $M/autost_mk5.sh 106 sol_repK3MW_01__K3l5q_k268
echo "=== ST-107"; bash $M/autost_mk4nz.sh 107 sol_k86MK2_in08_tight__K3l5q_k260
echo ST106107DONE
