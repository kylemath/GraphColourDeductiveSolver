#!/bin/zsh
# Job 29 L2 with win9 + win25 included (round-13 pattern set + loop/n9), many=200; nice 19.
cd "$(dirname $0)"
A=($(cat out/job28/j28_13.args) pat=loop/n9/win9.out pat=loop/n9/win25.out)
nice -n 19 python3 wlp3x.py tag=j29_13n9 many=200 warm=out/job28/all_13.txt $A > out/job28/j29_xn9.log 2>&1
echo done > out/job28/j29b.DONE
