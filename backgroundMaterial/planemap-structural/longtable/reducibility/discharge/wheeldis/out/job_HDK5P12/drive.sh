#!/bin/zsh
# HDK5P12: HDK5P12, HDK5P12V00, HDK5P12All
cd $(dirname $0)/lean; ./run.sh HDK5P12; ./run.sh HDK5P12V00; ./run.sh HDK5P12All; echo ALLDONE >> status.txt
