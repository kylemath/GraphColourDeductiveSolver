#!/bin/zsh
# HCK5P04: CK5P04, K5P04V00, K5P04VAll
cd $(dirname $0)/lean; ./run.sh CK5P04; ./run.sh K5P04V00; ./run.sh K5P04VAll; echo ALLDONE >> status.txt
