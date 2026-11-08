#!/bin/zsh
# HCK3l: CK3L, K3LV00, K3LVAll (Fin 1), alongside the Lean queue
cd $(dirname $0)/lean; ./run.sh CK3L; ./run.sh K3LV00; ./run.sh K3LVAll; echo ALLDONE >> status.txt
