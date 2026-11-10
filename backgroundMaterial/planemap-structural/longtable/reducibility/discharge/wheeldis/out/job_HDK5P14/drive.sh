#!/bin/zsh
# HDK5P14: HDK5P14, HDK5P14V00, HDK5P14All
cd $(dirname $0)/lean; ./run.sh HDK5P14; ./run.sh HDK5P14V00; ./run.sh HDK5P14All; echo ALLDONE >> status.txt
