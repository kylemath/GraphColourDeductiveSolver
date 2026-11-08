#!/bin/zsh
# K3CHK9 Lean jobs: after HCK5H01 (its glue GLUEDONE), run the 5 jobs side by side (nice 20), ahead of HDK3b/HCK3C4/HDK3c/HOFFC7
cd $(dirname $0)/../..
until grep -q GLUEDONE out/job_HCK5H01/lean/status.txt 2>/dev/null; do sleep 60; done
for j in HCK5b_L1 HCK5b_L2 HDK5b_L3 HCK5b_U1 HCK5b_U2; do out/job_$j/drive.sh > out/job_$j/drive.log 2>&1 & done; wait; echo ALLDONE > out/job_K3CHK9/LEANDONE
