#!/bin/zsh
# HCK5P22: CK5P22, K5P22V00, K5P22VAll
cd $(dirname $0)/lean; ./run.sh CK5P22; ./run.sh K5P22V00; ./run.sh K5P22VAll; echo ALLDONE >> status.txt
