#!/bin/zsh
cd $(dirname $0)/lean
until grep -q "^K3IVAll exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK3I_00; ./run.sh HK3I_01; ./run.sh COccHK3I_00; ./run.sh COccHK3I_01; ./run.sh HK3IOcc; echo GLUEDONE >> status.txt
