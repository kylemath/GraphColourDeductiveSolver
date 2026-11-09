#!/bin/bash
# usage: ctl.sh NP : (re)start the bind86 screen with NP procs (resumable); NP=0 just stops it
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; cd $W/out/job_ST87
pkill -f runb86.sh; pkill -f job_ST87/drive.sh; pkill -f "bash drive.sh"; pkill -f "mscreen.py famK5_r1516_b86"; pkill -f "mscreen.py parts/famK5_r"; sleep 2
for p in $(ps -Ao pid,ppid,command | awk '$2==1' | grep -E "loop/kc/kc|out/job52/dfast18|studio15/cfast" | grep -v "/chk/" | awk '{print $1}'); do kill $p; done
[ "$1" = 0 ] && exit 0
echo $1 > np.txt; [ -f run.log ] && cat run.log >> run_all.log
nohup bash drive.sh $1 > run.log 2>&1 &
