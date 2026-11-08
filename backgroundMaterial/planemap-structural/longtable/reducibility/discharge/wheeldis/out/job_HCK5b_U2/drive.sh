#!/bin/zsh
# HCK5b_U2: CK5BU2, K5BU2V00, K5BU2VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5BU2; ./run.sh K5BU2V00; ./run.sh K5BU2VAll; echo ALLDONE >> status.txt
