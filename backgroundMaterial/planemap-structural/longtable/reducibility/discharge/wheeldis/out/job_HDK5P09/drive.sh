#!/bin/zsh
# HDK5P09: HDK5P09, HDK5P09V00, HDK5P09All
cd $(dirname $0)/lean; ./run.sh HDK5P09; ./run.sh HDK5P09V00; ./run.sh HDK5P09All; echo ALLDONE >> status.txt
