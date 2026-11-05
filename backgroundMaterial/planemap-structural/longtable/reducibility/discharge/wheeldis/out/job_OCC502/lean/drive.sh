#!/bin/zsh
cd $(dirname $0)
[ -f $HOME/studio_lean_builds/rsst118_fb35d2d1/dc/COccBridge.olean ] || ./run.sh COccBridge
ls HK_*.lean H30_*.lean HC_*.lean | sort | sed 's/.lean//' | xargs -P 4 -n 1 ./run.sh
ls COccHK_*.lean COccH30_*.lean COccHC_*.lean | sort | sed 's/.lean//' | xargs -P 4 -n 1 ./run.sh
./run.sh HDCtrlOcc; ./run.sh HD30Occ; echo PHASE1DONE >> status.txt
