#!/bin/bash
# round 34 part A check: dfast18 on the two ring-17 windows (2 cores), then part B ring 10-14 and 15 (3 streams)
cd "$(dirname "$0")"
until [ -f A.DONE ]; do sleep 5; done
../../bin/dfast18 a0.in > a0.df 2>&1 &
../../bin/dfast18 a1.in > a1.df 2>&1 &
wait
cat a0.df a1.df a2.df > binA_dfast.out
./runB.sh 10 14 b14
./runB.sh 15 15 b15
