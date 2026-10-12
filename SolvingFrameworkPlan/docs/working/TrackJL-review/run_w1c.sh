#!/bin/sh
# worker 1, third job (the queued tail of run_w2.sh, moved here so worker 2 only runs sphere5)
cd "$(dirname "$0")"
nice -n 10 ./rv_eng -E 1 -s 11 -M 4000000 < out/fresh_rp2_3.txt > out/w2_rp2_3.log 2> out/w2_rp2_3.err
nice -n 10 ./rv_eng -E 1 -s 11 -M 4000000 < out/fresh_rp2_5.txt > out/w2_rp2_5.log 2> out/w2_rp2_5.err
nice -n 10 ./rv_eng -E 2 -s 11 -M 4000000 < out/fresh_sphere3.txt > out/w2_sphere3.log 2> out/w2_sphere3.err
