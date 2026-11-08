#!/bin/zsh
# HCK5b_L2: CK5BL2, K5BL2V00, K5BL2VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5BL2; ./run.sh K5BL2V00; ./run.sh K5BL2VAll; echo ALLDONE >> status.txt
