#!/bin/zsh
cd $(dirname $0)
./run.sh HK3P_00; ./run.sh HK3P_01; ./run.sh COccHK3P_00; ./run.sh COccHK3P_01; ./run.sh HDK3POcc; echo GLUEDONE >> status.txt
