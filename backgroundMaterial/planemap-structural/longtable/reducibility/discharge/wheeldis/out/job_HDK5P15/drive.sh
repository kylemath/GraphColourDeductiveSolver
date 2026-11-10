#!/bin/zsh
# HDK5P15: HDK5P15, HDK5P15V00, HDK5P15All
cd $(dirname $0)/lean; ./run.sh HDK5P15; ./run.sh HDK5P15V00; ./run.sh HDK5P15All; echo ALLDONE >> status.txt
