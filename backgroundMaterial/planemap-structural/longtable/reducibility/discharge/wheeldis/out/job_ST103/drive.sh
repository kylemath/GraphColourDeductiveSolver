#!/bin/bash
# ST-103 ring-15-first driver (Studio; runt98.sh unpatched, same mscreen.py per window): usage drive.sh NP. Resumable.
cd /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_ST103; NP=$1; KC=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/kc/kc; DF18=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job52/dfast18; CF=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/../studio15/cfast; SKIP=$PWD/skip_t98.txt; export KC DF18 CF SKIP
mkdir -p results
for PH in 15 16; do
  RUN=r${PH}_$(date +%H%M%S); N=$(python3 parts.py $PH $NP $RUN); echo "phase $PH run $RUN remaining $N"
  [ "$N" = 0 ] && continue
  ls parts/famK5_${RUN}_*.tsv | xargs -P "$NP" -I{} sh -c 't=$(basename {} .tsv); t=${t#famK5_}; nice -n 20 python3 mscreen.py {} results/res_K5_$t.tsv >> results/log_$t.txt 2>&1'
  echo "phase $PH done"
done
echo ALLDONE
