#!/bin/zsh
# HDK5P10: HDK5P10, HDK5P10V00, HDK5P10All
cd $(dirname $0)/lean; ./run.sh HDK5P10; ./run.sh HDK5P10V00; ./run.sh HDK5P10All; echo ALLDONE >> status.txt
