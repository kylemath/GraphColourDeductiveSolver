#!/bin/bash
# ST-104: start HDK5P15 and HDK5P16 Lean after HDK5P10 is GLUEDONE (Lean priority to P10)
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
until grep -q GLUEDONE $W/out/job_HDK5P10/lean/status.txt 2>/dev/null; do sleep 120; done
for n in 15 16; do H=$W/out/job_HDK5P$n; nohup $H/drive.sh > $H/drive.log 2>&1 < /dev/null & done
echo "started HDK5P15, HDK5P16 $(date -u +%H:%M)"
