#!/bin/zsh
cd $(dirname $0)
until grep -q PHASE1DONE status.txt; do sleep 60; done
ls HR_*.lean | sed 's/.lean//' | xargs -P 4 -n 1 ./run.sh; ls COccHR_*.lean | sed 's/.lean//' | xargs -P 4 -n 1 ./run.sh; ./run.sh HDR5Occ
echo PHASE2DONE >> status.txt
until grep -q "^HDCAll exit=0" ../../job_HDC502/lean/status.txt; do sleep 300; done
./run.sh HDCOcc; echo ALLDONE >> status.txt
