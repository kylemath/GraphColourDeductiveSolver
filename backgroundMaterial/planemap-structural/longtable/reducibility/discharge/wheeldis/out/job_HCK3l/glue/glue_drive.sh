#!/bin/zsh
# HCK3l glue (Opus): after K3LVAll builds, compile HK3L_00, COccHK3L_00, then HK3LOcc (same order as HCK3j).
cd $(dirname $0)/../lean
until grep -q "^K3LVAll exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK3L_00; ./run.sh COccHK3L_00; ./run.sh HK3LOcc; echo GLUEDONE >> status.txt
