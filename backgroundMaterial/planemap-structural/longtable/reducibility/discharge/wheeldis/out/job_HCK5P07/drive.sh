#!/bin/zsh
# HCK5P07: CK5P07, K5P07V00, K5P07VAll
cd $(dirname $0)/lean; ./run.sh CK5P07; ./run.sh K5P07V00; ./run.sh K5P07VAll; echo ALLDONE >> status.txt
