#!/bin/zsh
cd $(dirname $0)/lean; ./run.sh K3JV00; ./run.sh K3JVAll; echo ALLDONE >> status.txt
