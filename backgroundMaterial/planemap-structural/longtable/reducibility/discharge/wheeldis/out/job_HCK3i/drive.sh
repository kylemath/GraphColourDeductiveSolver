#!/bin/zsh
# HCK3i: after HDK3c (GLUEDONE), build K3IV00/01 (cReducible18 hC) and K3IVAll
cd $(dirname $0)
until grep -q GLUEDONE ../job_HDK3c/lean/status.txt 2>/dev/null; do sleep 60; done
cd lean; ./run.sh K3IV00; ./run.sh K3IV01; ./run.sh K3IVAll; echo ALLDONE >> status.txt
