#!/bin/zsh
cd $(dirname $0)
until grep -q "^HDK3All exit=0" status.txt 2>/dev/null; do sleep 30; done
for i in $(seq 0 5); do printf "HK3D_%02d\n" $i; done | xargs -P 3 -n 1 ./run.sh; for i in $(seq 0 5); do printf "COccHK3D_%02d\n" $i; done | xargs -P 3 -n 1 ./run.sh
./run.sh HDK3Occ; echo GLUEDONE >> status.txt
