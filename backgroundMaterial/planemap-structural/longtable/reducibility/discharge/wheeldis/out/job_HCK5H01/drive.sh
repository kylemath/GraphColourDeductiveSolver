#!/bin/zsh
# HCK5H01: CK5H01, K5H01V00, K5H01VAll (Fin 1), ahead of the Lean queue
cd $(dirname $0)/lean; ./run.sh CK5H01; ./run.sh K5H01V00; ./run.sh K5H01VAll; echo ALLDONE >> status.txt
