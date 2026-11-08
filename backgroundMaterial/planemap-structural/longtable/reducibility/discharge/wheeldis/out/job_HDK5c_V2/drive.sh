#!/bin/zsh
# HDK5c_V2: HDK5CV2, HDK5CV2V00, HDK5CV2All
cd $(dirname $0)/lean; ./run.sh HDK5CV2; ./run.sh HDK5CV2V00; ./run.sh HDK5CV2All; echo ALLDONE >> status.txt
