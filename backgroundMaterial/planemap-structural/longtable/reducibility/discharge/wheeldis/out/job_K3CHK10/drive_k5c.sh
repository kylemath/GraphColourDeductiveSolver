#!/bin/zsh
# K3CHK10 Lean jobs: after the five K5b jobs (out/job_K3CHK9/LEANDONE), run the 8 K5c jobs side by side (nice 20), ahead of HDK3b/HCK3C4/HDK3c/HOFFC7
cd $(dirname $0)/../..
until [ -f out/job_K3CHK9/LEANDONE ]; do sleep 60; done
for j in HDK5c_V1 HDK5c_V2 HCK5c_V3 HDK5c_V4 HDK5c_V5 HCK5c_V6 HCK5c_V7 HCK5c_V8; do out/job_$j/drive.sh > out/job_$j/drive.log 2>&1 & done; wait; echo ALLDONE > out/job_K3CHK10/LEANDONE
