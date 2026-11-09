#!/bin/zsh
# HDK5m: HDK5M, HDK5MV00, HDK5MAll
cd $(dirname $0)/lean; ./run.sh HDK5M; ./run.sh HDK5MV00; ./run.sh HDK5MAll; echo ALLDONE >> status.txt
