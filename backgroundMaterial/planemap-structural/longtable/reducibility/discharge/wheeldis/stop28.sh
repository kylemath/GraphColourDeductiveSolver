#!/bin/zsh
# PAUSE (k, 16 Oct 17:40Z): stop loop28b right after round 13's LP solve, before its batch starts.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
until [ -f $W/out/wlp3_j28_13.txt ]; do sleep 20; done
pkill -f loop28b.py
sleep 5; pkill -f "in_13"; pkill -f "cin_13"
echo "$(date '+%m-%d %H:%M') stopped loop28b after round 13 solve (pause)" >> $W/out/job28/loop.log
