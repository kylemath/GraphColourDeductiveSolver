#!/bin/zsh
# HCK5c_V3: CK5CV3, K5CV3V00, K5CV3VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5CV3; ./run.sh K5CV3V00; ./run.sh K5CV3VAll; echo ALLDONE >> status.txt
