#!/bin/zsh
# HDK5c_V4: HDK5CV4, HDK5CV4V00, HDK5CV4All
cd $(dirname $0)/lean; ./run.sh HDK5CV4; ./run.sh HDK5CV4V00; ./run.sh HDK5CV4All; echo ALLDONE >> status.txt
