#!/bin/zsh
# HCK3k glue (Opus): after K3KVAll builds, compile HK3K_00, COccHK3K_00, then HK3KOcc (same order as HCK3j).
cd $(dirname $0)/../lean
until grep -q "^K3KVAll exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK3K_00; ./run.sh COccHK3K_00; ./run.sh HK3KOcc; echo GLUEDONE >> status.txt
