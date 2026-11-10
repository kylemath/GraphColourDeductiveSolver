#!/bin/zsh
# HDK5P01: HDK5P01, HDK5P01V00, HDK5P01All
cd $(dirname $0)/lean; ./run.sh HDK5P01; ./run.sh HDK5P01V00; ./run.sh HDK5P01All; echo ALLDONE >> status.txt
