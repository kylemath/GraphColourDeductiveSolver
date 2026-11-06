#!/bin/zsh
cd $(dirname $0)
for i in $(seq 0 3); do printf "HWR4_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 3); do printf "COccHWR4_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh
until grep -q "^W4VAll exit=0" status.txt; do sleep 120; done; ./run.sh HWR4Occ; echo GLUEDONE >> status.txt
