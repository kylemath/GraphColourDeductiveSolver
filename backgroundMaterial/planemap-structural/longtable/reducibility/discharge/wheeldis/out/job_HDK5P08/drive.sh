#!/bin/zsh
# HDK5P08: HDK5P08, HDK5P08V00, HDK5P08All
cd $(dirname $0)/lean; ./run.sh HDK5P08; ./run.sh HDK5P08V00; ./run.sh HDK5P08All; echo ALLDONE >> status.txt
