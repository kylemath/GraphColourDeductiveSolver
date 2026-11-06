#!/bin/zsh
cd $(dirname $0)
for i in $(seq 0 26); do printf "HWD_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 26); do printf "COccHWD_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh
until grep -q "^HDW13All exit=0" status.txt; do sleep 60; done; ./run.sh HDW13Occ; echo GLUEDONE >> status.txt
