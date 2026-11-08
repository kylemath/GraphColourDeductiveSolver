#!/bin/zsh
# HDK5c_V1: HDK5CV1, HDK5CV1V00, HDK5CV1All
cd $(dirname $0)/lean; ./run.sh HDK5CV1; ./run.sh HDK5CV1V00; ./run.sh HDK5CV1All; echo ALLDONE >> status.txt
