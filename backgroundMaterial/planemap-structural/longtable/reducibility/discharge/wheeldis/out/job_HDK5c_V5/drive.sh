#!/bin/zsh
# HDK5c_V5: HDK5CV5, HDK5CV5V00, HDK5CV5All
cd $(dirname $0)/lean; ./run.sh HDK5CV5; ./run.sh HDK5CV5V00; ./run.sh HDK5CV5All; echo ALLDONE >> status.txt
