#!/bin/zsh
# HCK5P03: CK5P03, K5P03V00, K5P03VAll
cd $(dirname $0)/lean; ./run.sh CK5P03; ./run.sh K5P03V00; ./run.sh K5P03VAll; echo ALLDONE >> status.txt
