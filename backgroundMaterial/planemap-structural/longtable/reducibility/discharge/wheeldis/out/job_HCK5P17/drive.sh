#!/bin/zsh
# HCK5P17: CK5P17, K5P17V00, K5P17VAll
cd $(dirname $0)/lean; ./run.sh CK5P17; ./run.sh K5P17V00; ./run.sh K5P17VAll; echo ALLDONE >> status.txt
