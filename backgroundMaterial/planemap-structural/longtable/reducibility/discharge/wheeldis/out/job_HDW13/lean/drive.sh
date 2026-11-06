#!/bin/zsh
cd $(dirname $0)
./run.sh HDW13
for i in $(seq 0 26); do printf "HDW13V%02d\n" $i; done | xargs -P 8 -n 1 ./run.sh
./run.sh HDW13All; echo ALLDONE >> status.txt
