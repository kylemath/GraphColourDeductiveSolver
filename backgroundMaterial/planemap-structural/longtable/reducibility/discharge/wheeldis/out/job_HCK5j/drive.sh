#!/bin/zsh
# HCK5j: CK5J, K5JV00, K5JVAll
cd $(dirname $0)/lean; ./run.sh CK5J; ./run.sh K5JV00; ./run.sh K5JVAll; echo ALLDONE >> status.txt
