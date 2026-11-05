#!/bin/zsh
cd $(dirname $0); ./run.sh CK108
seq -f "K108V%02g" 0 18 | xargs -P 4 -n 1 ./run.sh
./run.sh K108All; echo ALLDONE >> status.txt
