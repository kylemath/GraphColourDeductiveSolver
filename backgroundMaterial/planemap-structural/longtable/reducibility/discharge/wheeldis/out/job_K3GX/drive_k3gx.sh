#!/bin/zsh
# ST-69 Lean: after P01-P04 (their GLUEDONE): HDK3GX and CK3GX, then all V modules at most 6 at a time (nice 20), then the All modules
cd /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
for j in HDK5P01 HCK5P02 HCK5P03 HCK5P04; do until grep -q GLUEDONE out/job_$j/lean/status.txt 2>/dev/null; do sleep 120; done; done
(cd out/job_HDK3GX/lean; ./run.sh HDK3GX); (cd out/job_HCK3GX/lean; ./run.sh CK3GX)
(for i in $(seq -f %02g 0 89); do echo "out/job_HDK3GX/lean HDK3GXV$i"; done; for i in $(seq -f %02g 0 68); do echo "out/job_HCK3GX/lean K3GXV$i"; done) | xargs -P 6 -L 1 zsh -c 'cd $0 && ./run.sh $1'
(cd out/job_HDK3GX/lean; ./run.sh HDK3GXAll; echo ALLDONE >> status.txt); (cd out/job_HCK3GX/lean; ./run.sh K3GXVAll; echo ALLDONE >> status.txt)
