#!/bin/zsh
# HDK5P06: HDK5P06, HDK5P06V00, HDK5P06All
cd $(dirname $0)/lean; ./run.sh HDK5P06; ./run.sh HDK5P06V00; ./run.sh HDK5P06All; echo ALLDONE >> status.txt
