#!/bin/zsh
# HCK5c_V8: CK5CV8, K5CV8V00, K5CV8VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5CV8; ./run.sh K5CV8V00; ./run.sh K5CV8VAll; echo ALLDONE >> status.txt
