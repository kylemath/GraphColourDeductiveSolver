#!/bin/zsh
# HCK5b_L1: CK5BL1, K5BL1V00, K5BL1VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5BL1; ./run.sh K5BL1V00; ./run.sh K5BL1VAll; echo ALLDONE >> status.txt
