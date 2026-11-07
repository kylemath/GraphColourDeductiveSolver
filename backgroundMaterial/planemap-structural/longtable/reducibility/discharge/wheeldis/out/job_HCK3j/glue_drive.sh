#!/bin/zsh
cd $(dirname $0)/lean
until grep -q "^K3JVAll exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK3J_00; ./run.sh COccHK3J_00; ./run.sh HK3JOcc; echo GLUEDONE >> status.txt
