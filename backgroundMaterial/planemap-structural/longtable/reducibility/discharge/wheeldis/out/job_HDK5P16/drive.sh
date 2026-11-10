#!/bin/zsh
# HDK5P16: HDK5P16, HDK5P16V00, HDK5P16All
cd $(dirname $0)/lean; ./run.sh HDK5P16; ./run.sh HDK5P16V00; ./run.sh HDK5P16All; echo ALLDONE >> status.txt
