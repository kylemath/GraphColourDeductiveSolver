#!/bin/bash
# coordinator 01:48Z: switch MS4 to K3l5j at the first iteration boundary after ST-72. LP_ON_CHECK=1 as MS4 (LP on the check family)
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
K=$N/runK_k86MS4/K.log; n0=$(grep -c '^iter ' $K); echo "iters at start $n0 $(date -u +%H:%M)"
until [ "$(grep -c '^iter ' $K)" -gt "$n0" ]; do sleep 20; done
grep '^iter ' $K | tail -1 | cut -c1-120; echo "boundary $(date -u +%H:%M)"
cd $R; LP_ON_CHECK=1 bash launch_upper_fam.sh j 2>&1 | cut -c1-240
echo "launch exit ${PIPESTATUS[0]} $(date -u +%H:%M)"
