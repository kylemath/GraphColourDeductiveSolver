#!/bin/zsh
# HDST111 (ST-111 audit): Lean hD for the 32 of the 39 2026-set configs (nl2837_r11, nl3352_r13 + d9_greedy 37) with no hD yet.
# Queued behind HCK5P17-19 (waits for HCK5P19 GLUEDONE); then HDST111, the 32 V modules largest ring first at NPAR (default 3), then HDST111All.
J=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
until grep -q GLUEDONE $J/job_HCK5P19/lean/status.txt 2>/dev/null; do sleep 120; done
cd $J/job_HDST111/lean; echo "start $(date -u +%H:%MZ)" >> status.txt; ./run.sh HDST111
cat order.txt | xargs -P ${NPAR:-3} -n 1 ./run.sh
./run.sh HDST111All; echo ALLDONE >> status.txt
