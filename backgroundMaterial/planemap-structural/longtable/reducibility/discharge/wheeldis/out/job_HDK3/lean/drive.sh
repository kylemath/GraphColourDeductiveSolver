#!/bin/zsh
cd $(dirname $0)
./run.sh HDK3
for i in $(seq 0 5); do printf "HDK3V%02d\n" $i; done | xargs -P 3 -n 1 ./run.sh
./run.sh HDK3All; echo ALLDONE >> status.txt
