#!/bin/zsh
cd $(dirname $0)
./run.sh CW3P
for i in $(seq 0 8); do printf "W3PV%02d\n" $i; done | xargs -P 6 -n 1 ./run.sh
./run.sh W3PVAll; echo ALLDONE >> status.txt
