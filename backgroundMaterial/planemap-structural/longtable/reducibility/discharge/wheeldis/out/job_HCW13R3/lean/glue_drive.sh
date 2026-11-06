#!/bin/zsh
cd $(dirname $0)
for i in $(seq 0 26); do printf "HWR3_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 26); do printf "COccHWR3_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh
until grep -q "^W3VAll exit=0" status.txt; do sleep 120; done; ./run.sh HWR3Occ; echo GLUEDONE >> status.txt
