#!/bin/bash
p=$1; cd "$(dirname "$0")"
s=$(date +%s.%N); timeout 60 ./jsep_ref pert7_all.txt work_pert/win_d7.bin $p > pref/$p.out 2>&1; rc=$?; e=$(date +%s.%N)
echo "$p rc=$rc $(grep END pref/$p.out) $(echo "$e-$s"|bc)" >> pref/summary.txt
