#!/bin/zsh
cd $(dirname $0); ./run.sh HDCtrl; ./run.sh HD30
ls HDCtrlV*.lean | sed 's/.lean//' | xargs -P 3 -n 1 ./run.sh; ./run.sh HDCtrlAll
ls HD30V*.lean | sed 's/.lean//' | xargs -P 4 -n 1 ./run.sh; ./run.sh HD30All; echo ALLDONE >> status.txt
