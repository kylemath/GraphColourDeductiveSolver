#!/bin/zsh
# HCK5P18: CK5P18, K5P18V00, K5P18VAll
cd $(dirname $0)/lean; ./run.sh CK5P18; ./run.sh K5P18V00; ./run.sh K5P18VAll; echo ALLDONE >> status.txt
