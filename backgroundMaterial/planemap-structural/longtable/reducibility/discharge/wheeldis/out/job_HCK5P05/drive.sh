#!/bin/zsh
# HCK5P05: CK5P05, K5P05V00, K5P05VAll
cd $(dirname $0)/lean; ./run.sh CK5P05; ./run.sh K5P05V00; ./run.sh K5P05VAll; echo ALLDONE >> status.txt
