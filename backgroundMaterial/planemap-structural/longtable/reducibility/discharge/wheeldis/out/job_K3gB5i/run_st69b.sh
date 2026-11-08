#!/bin/bash
# ST-69b: after my rows run: W17 K3gB5i main + tneg on in11, then report+commit
cd /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
until [ -f /tmp/swarm-W17/xrows.done ]; do sleep 60; done
SRC=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/maclane/MS3_K3gB/sol_k86MS3_in11.json bash out/maclane/autost_gb5i.sh 69b sol_k86MS3_in11 > out/maclane/autost_69b.log 2>&1
until [ -f /tmp/swarm-W17/st69b.done ]; do sleep 30; done
bash out/maclane/autost_gb5i_report.sh 69b sol_k86MS3_in11
