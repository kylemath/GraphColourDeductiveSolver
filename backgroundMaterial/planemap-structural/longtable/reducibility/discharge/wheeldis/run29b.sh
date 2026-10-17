#!/bin/zsh
# Job 29 L2 with win9, win25, win25b, win27 (round-13 pattern set + loop/n9), many=200, warm from the last row dump; nice 19.
cd "$(dirname $0)"
A=($(cat out/job28/j28_13.args) pat=loop/n9/win9.out pat=loop/n9/win25.out pat=loop/n9/win25b.out pat=loop/n9/win27.out)
nice -n 19 python3 wlp3x.py tag=j29_13n9 many=200 warm=out/job28/j29b_warm.txt $A > out/job28/j29_xn9.log 2>&1
echo done > out/job28/j29b.DONE
