#!/bin/zsh
# HCK5P19: CK5P19, K5P19V00, K5P19VAll
cd $(dirname $0)/lean; ./run.sh CK5P19; ./run.sh K5P19V00; ./run.sh K5P19VAll; echo ALLDONE >> status.txt
