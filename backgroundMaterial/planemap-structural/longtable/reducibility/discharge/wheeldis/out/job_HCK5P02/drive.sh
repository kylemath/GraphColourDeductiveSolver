#!/bin/zsh
# HCK5P02: CK5P02, K5P02V00, K5P02VAll
cd $(dirname $0)/lean; ./run.sh CK5P02; ./run.sh K5P02V00; ./run.sh K5P02VAll; echo ALLDONE >> status.txt
