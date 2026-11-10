#!/bin/bash
# coordinator 09:30Z: ST-105 after ST-101, then ST-103 after ST-105 (4 screen procs in total). Detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
until grep -q ALLDONE $W/out/job_ST101/run.log 2>/dev/null; do sleep 60; done
cd /tmp; bash $W/out/job_ST105/ctl.sh 4; echo "ST-105 started $(date -u +%H:%M)"
sleep 60; until grep -q ALLDONE $W/out/job_ST105/run.log 2>/dev/null; do sleep 60; done
cd /tmp; bash $W/out/job_ST103/ctl.sh 4; echo "ST-103 started $(date -u +%H:%M)"
