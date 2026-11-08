#!/bin/zsh
# HCK5b_U1: CK5BU1, K5BU1V00, K5BU1VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5BU1; ./run.sh K5BU1V00; ./run.sh K5BU1VAll; echo ALLDONE >> status.txt
