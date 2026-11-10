#!/bin/zsh
# HDK5P11: HDK5P11, HDK5P11V00, HDK5P11All
cd $(dirname $0)/lean; ./run.sh HDK5P11; ./run.sh HDK5P11V00; ./run.sh HDK5P11All; echo ALLDONE >> status.txt
