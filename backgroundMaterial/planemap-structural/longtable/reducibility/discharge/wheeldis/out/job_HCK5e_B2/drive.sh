#!/bin/zsh
# HCK5e_B2: right after HDK5d_B1 (its lean/status.txt ALLDONE): CK5EB2, K5EB2V00, K5EB2VAll (Fin 1)
cd $(dirname $0)
until grep -q ALLDONE ../job_HDK5d_B1/lean/status.txt 2>/dev/null; do sleep 60; done
cd lean; ./run.sh CK5EB2; ./run.sh K5EB2V00; ./run.sh K5EB2VAll; echo ALLDONE >> status.txt
