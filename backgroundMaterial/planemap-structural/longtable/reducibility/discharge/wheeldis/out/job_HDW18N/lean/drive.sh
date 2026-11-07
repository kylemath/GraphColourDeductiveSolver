#!/bin/zsh
cd $(dirname $0)
./run.sh HDW18N
for i in $(seq 0 14); do printf "HDW18NV%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh
./run.sh HDW18NAll; echo ALLDONE >> status.txt
