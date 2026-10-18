#!/bin/sh
# reproduce: own LP (x = 0) on the round-13 registry, rows from jsep
M=${M:-/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/main/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis}
cd "$(dirname "$0")"
python3 jcheck.py solve tag=j28_13 root=$M args=$M/out/job28/j28_13.args warm=$M/out/job28/tight_13.txt dmax=17 > solve_j28_13.log 2>&1
