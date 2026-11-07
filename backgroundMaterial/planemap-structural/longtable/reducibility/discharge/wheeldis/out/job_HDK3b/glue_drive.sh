#!/bin/zsh
cd $(dirname $0)/lean
until grep -q ALLDONE status.txt 2>/dev/null; do sleep 60; done
./run.sh HK3BD_00; ./run.sh COccHK3BD_00; ./run.sh HDK3BOcc; echo GLUEDONE >> status.txt
