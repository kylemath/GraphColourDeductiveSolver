#!/bin/zsh
cd /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
nice -n 10 python3 out/job30/ringmerge_cpat_sweep.py loop/studio/opus_check/s53/A97/argsA97_local.txt > loop/studio/opus_check/s53/A97/ringmerge_sweep_A97.out 2>/dev/null
K3X=loop/studio/opus_check/s53/A97/k3x_D_8ec00aea.out,loop/studio/opus_check/s53/A97/k3x_C_8ec00aea.cfast nice -n 10 python3 out/job31/st16_filter.py out/job31/s53A97/kill > out/job31/s53A97/kill/st16_filter_A97.log 2>&1
nice -n 10 python3 out/job31/l3q_masks.py loop/studio/opus_check/s53/A97/k3x_D_8ec00aea.out loop/studio/opus_check/s53/A97/k3x_C_8ec00aea.cfast out/job31/s53A97 > out/job31/s53A97/l3q_masks_A97.log 2>&1
L3QV=8 nice -n 10 python3 out/job31/l3q_masks.py loop/studio/opus_check/s53/A97/k3x_D_8ec00aea.out loop/studio/opus_check/s53/A97/k3x_C_8ec00aea.cfast out/job31/s53A97/V8 > out/job31/s53A97/V8/l3q_masks_V8_A97.log 2>&1
echo done > out/job31/s53A97/BUILD.DONE
