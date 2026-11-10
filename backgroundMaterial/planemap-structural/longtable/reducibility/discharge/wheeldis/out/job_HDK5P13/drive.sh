#!/bin/zsh
# HDK5P13: HDK5P13, HDK5P13V00, HDK5P13All
cd $(dirname $0)/lean; ./run.sh HDK5P13; ./run.sh HDK5P13V00; ./run.sh HDK5P13All; echo ALLDONE >> status.txt
