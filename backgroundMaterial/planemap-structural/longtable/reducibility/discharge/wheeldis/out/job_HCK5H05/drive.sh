#!/bin/zsh
# HCK5H05: CK5H05, K5H05V00, K5H05VAll (Fin 1)
cd $(dirname $0)/lean; ./run.sh CK5H05; ./run.sh K5H05V00; ./run.sh K5H05VAll; echo ALLDONE >> status.txt
