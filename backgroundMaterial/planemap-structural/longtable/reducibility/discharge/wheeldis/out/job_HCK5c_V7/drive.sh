#!/bin/zsh
# HCK5c_V7: CK5CV7, K5CV7V00, K5CV7VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5CV7; ./run.sh K5CV7V00; ./run.sh K5CV7VAll; echo ALLDONE >> status.txt
