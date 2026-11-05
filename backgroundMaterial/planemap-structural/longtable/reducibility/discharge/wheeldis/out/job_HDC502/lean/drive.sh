#!/bin/zsh
cd $(dirname $0); ./run.sh HDC
ls HDCV*.lean | sort | sed 's/.lean//' | xargs -P ${NPAR:-11} -n 1 ./run.sh
./run.sh HDCAll; echo ALLDONE >> status.txt
