#!/bin/zsh
# Job 29 one-off solves of run29b's final row dump: binders (xcap 3) and the cap test (xcap 1000); nice 15.
cd "$(dirname $0)"
A=($(cat out/job28/j28_13.args) pat=loop/n9/win9.out pat=loop/n9/win25.out pat=loop/n9/win25b.out pat=loop/n9/win27.out pat=loop/n9/win29.out pat=loop/n9/win31.out)
WLP3X_DEF=1 nice -n 15 python3 wlp3x.py tag=j29_dump maxit=0 warm=out/job28/j29b_final_rows.txt $A > out/job28/j29_dump.log 2>&1
WLP3X_DEF=1 nice -n 15 python3 wlp3x.py tag=j29_dumpcap maxit=0 xcap=1000 warm=out/job28/j29b_final_rows.txt $A > out/job28/j29_dumpcap.log 2>&1
echo done > out/job28/j29d.DONE
