#!/bin/zsh
# HDK5b_L3: HDK5BL3, HDK5BL3V00, HDK5BL3All
cd $(dirname $0)/lean; ./run.sh HDK5BL3; ./run.sh HDK5BL3V00; ./run.sh HDK5BL3All; echo ALLDONE >> status.txt
