#!/bin/zsh
cd /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
nice -n 15 python3 out/job30/ringmerge_cpat_sweep.py loop/studio/opus_check/s51/A87/argsA87_local.txt > loop/studio/opus_check/s51/A87/ringmerge_sweep_A87.out 2>/dev/null
K3X=loop/studio/opus_check/s51/A87/k3x_D_b253a4ad.out,loop/studio/opus_check/s51/A87/k3x_C_b253a4ad.cfast nice -n 15 python3 out/job31/st16_filter.py out/job31/s51A87/kill > out/job31/s51A87/kill/st16_filter_A87.log 2>&1
nice -n 15 python3 out/job31/l3q_masks.py loop/studio/opus_check/s51/A87/k3x_D_b253a4ad.out loop/studio/opus_check/s51/A87/k3x_C_b253a4ad.cfast out/job31/s51A87 > out/job31/s51A87/l3q_masks_A87.log 2>&1
L3QV=8 nice -n 15 python3 out/job31/l3q_masks.py loop/studio/opus_check/s51/A87/k3x_D_b253a4ad.out loop/studio/opus_check/s51/A87/k3x_C_b253a4ad.cfast out/job31/s51A87/V8 > out/job31/s51A87/V8/l3q_masks_V8_A87.log 2>&1
echo done > out/job31/s51A87/BUILD.DONE
