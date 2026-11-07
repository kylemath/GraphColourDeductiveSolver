#!/bin/zsh
cd $(dirname $0)
for i in $(seq 0 14); do printf "HWN_%02d\n" $i; done | xargs -P 3 -n 1 ./run.sh; for i in $(seq 0 14); do printf "COccHWN_%02d\n" $i; done | xargs -P 3 -n 1 ./run.sh
until grep -q "^HDW18NAll exit=0" status.txt; do sleep 30; done; ./run.sh HDW18NOcc; echo GLUEDONE >> status.txt
