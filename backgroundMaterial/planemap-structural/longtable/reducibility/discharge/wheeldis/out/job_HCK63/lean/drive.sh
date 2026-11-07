#!/bin/zsh
cd $(dirname $0)
./run.sh CK63H
for i in $(seq 0 113); do printf "K63HV%03d\n" $i; done | xargs -P 6 -n 1 ./run.sh
./run.sh K63HVAll; echo ALLDONE >> status.txt
