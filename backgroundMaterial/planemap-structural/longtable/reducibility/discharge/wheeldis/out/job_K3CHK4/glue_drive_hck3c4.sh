#!/bin/zsh
cd $(dirname $0)/lean
until grep -q "^K3C4VAll exit=0" status.txt 2>/dev/null; do sleep 60; done
./run.sh HK3C4_00; ./run.sh COccHK3C4_00; ./run.sh HK3C4Occ; echo GLUEDONE >> status.txt
