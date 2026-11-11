#!/bin/zsh
# ST-132b: after the K783 census (st132/DONE), if d7 has 0 failing leaves, replay d7, d8, d9..14, then the assembly
# (one module at a time via lean1.sh; stops at the first degree with failing leaves)
cd $(dirname $0)/..
until [ -f st132/DONE ]; do sleep 60; done
fails() { [ -f st132/cert$1_census.txt.summary.json ] || { echo MISSING; return; }; grep -o '"census_leaves": [0-9]*' st132/cert$1_census.txt.summary.json | awk '{print $2}'; }
for d in 7 8; do [ -n "$(fails $d)" ] && { echo "STOP d$d failing $(fails $d)" >> st132/replay.log; exit 0; }; done
./lean1.sh RSSTDeg7R783 >> st132/replay.log 2>&1
./lean1.sh RSSTDeg8R783 >> st132/replay.log 2>&1
for d in 9 10 11 12 13 14; do [ -n "$(fails $d)" ] && { echo "STOP d$d failing $(fails $d)" >> st132/replay.log; exit 0; }; done
./lean1.sh RSSTDegHiR783 >> st132/replay.log 2>&1
./lean1.sh RSSTB5AllR >> st132/replay.log 2>&1
echo REPLAYDONE >> st132/replay.log
