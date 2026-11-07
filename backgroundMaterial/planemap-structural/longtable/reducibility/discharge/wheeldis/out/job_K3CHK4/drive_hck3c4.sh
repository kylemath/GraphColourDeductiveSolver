#!/bin/zsh
# HCK3C4: after HDK3b (ALLDONE), build K3C4V00 (cReducible18 hC) and K3C4VAll
cd $(dirname $0)
until grep -q ALLDONE ../job_HDK3b/lean/status.txt 2>/dev/null; do sleep 60; done
cd lean; ./run.sh K3C4V00; ./run.sh K3C4VAll; echo ALLDONE >> status.txt
