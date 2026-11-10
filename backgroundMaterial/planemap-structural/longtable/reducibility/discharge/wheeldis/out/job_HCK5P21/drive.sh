#!/bin/zsh
# HCK5P21: CK5P21, K5P21V00, K5P21VAll
cd $(dirname $0)/lean; ./run.sh CK5P21; ./run.sh K5P21V00; ./run.sh K5P21VAll; echo ALLDONE >> status.txt
