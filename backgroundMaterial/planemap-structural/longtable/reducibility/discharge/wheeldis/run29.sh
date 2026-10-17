#!/bin/zsh
# Job 29 L2: validation (transfers off) then the full L2 solve, on round 13's exact pattern set; nice 19.
cd "$(dirname $0)"
A=($(cat out/job28/j28_13.args))
nice -n 19 python3 wlp3x.py notx tag=j29_13 warm=out/job28/all_13.txt $A > out/job28/j29_notx.log 2>&1
nice -n 19 python3 wlp3x.py tag=j29_13 warm=out/job28/all_13.txt $A > out/job28/j29_x.log 2>&1
echo done > out/job28/j29.DONE
