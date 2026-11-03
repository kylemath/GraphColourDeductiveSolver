#!/bin/zsh
cd $(dirname $0); ./run.sh CR118
seq -f "R118V%02g" 0 19 | xargs -P 4 -n 1 ./run.sh
./run.sh R118All; echo ALLDONE >> status.txt
