#!/bin/zsh
# HCK5c_V6: CK5CV6, K5CV6V00, K5CV6VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5CV6; ./run.sh K5CV6V00; ./run.sh K5CV6VAll; echo ALLDONE >> status.txt
