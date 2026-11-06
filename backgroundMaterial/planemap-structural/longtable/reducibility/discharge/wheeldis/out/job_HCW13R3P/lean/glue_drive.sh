#!/bin/zsh
cd $(dirname $0)
for i in $(seq 0 8); do printf "HWR3P_%02d\n" $i; done | xargs -P 3 -n 1 ./run.sh; for i in $(seq 0 8); do printf "COccHWR3P_%02d\n" $i; done | xargs -P 3 -n 1 ./run.sh
until grep -q "^W3PVAll exit=0" status.txt; do sleep 60; done; ./run.sh HWR3POcc; echo GLUEDONE >> status.txt
