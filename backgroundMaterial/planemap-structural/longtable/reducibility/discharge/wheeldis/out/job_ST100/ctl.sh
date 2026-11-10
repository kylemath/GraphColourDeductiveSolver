#!/bin/bash
# usage: ctl.sh NP : (re)start this job's K-5 screen with NP procs (resumable); NP=0 just stops it.
# Scoped (9 Nov): the drive runs in its own process group (set -m), recorded in drive.pgid; stopping kills only that group,
# so two screens can run side by side (the old pkill patterns matched every job's drive / mscreen).
J=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_ST100; cd $J
if [ -f drive.pgid ]; then g=$(cat drive.pgid); [ -n "$g" ] && [ "$g" -gt 1 ] && kill -TERM -$g 2>/dev/null; sleep 3; fi
[ "$1" = 0 ] && exit 0
echo $1 > np.txt; [ -f run.log ] && cat run.log >> run_all.log
set -m
nohup bash drive.sh $1 > run.log 2>&1 &
echo $! > drive.pgid
