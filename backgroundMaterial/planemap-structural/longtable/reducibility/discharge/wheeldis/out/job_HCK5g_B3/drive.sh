#!/bin/zsh
# HCK5g_B3: CK5GB3, K5GB3V00, K5GB3VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5GB3; ./run.sh K5GB3V00; ./run.sh K5GB3VAll; echo ALLDONE >> status.txt
