#!/bin/zsh
# HCK5P20: CK5P20, K5P20V00, K5P20VAll
cd $(dirname $0)/lean; ./run.sh CK5P20; ./run.sh K5P20V00; ./run.sh K5P20VAll; echo ALLDONE >> status.txt
