#!/bin/zsh
cd $(dirname $0)
./run.sh COccBridge COccBridge.lean /Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1/dc
./run.sh HD13; ls HD13V*.lean | sed 's/.lean//' | xargs -P 5 -n 1 ./run.sh; ./run.sh HD13All
seq -f "H13_%02g" 0 9 | xargs -P 5 -n 1 ./run.sh
seq -f "COccH13_%02g" 0 9 | xargs -P 5 -n 1 ./run.sh
./run.sh HD13Occ; echo ALLDONE >> status.txt
