#!/bin/sh
# worker 1: Census29 frame classes 22-31 (all holes), sphere constants
cd "$(dirname "$0")"
cat ../Census29/out/frame-2[2-9].txt | nice -n 10 ./rv_eng -E 2 -s 7 > out/w1_frame22-29.log 2> out/w1_frame22-29.err
nice -n 10 ./rv_eng -E 2 -s 13 < ../Census29/out/frame-30.txt > out/w1_frame30.log 2> out/w1_frame30.err
nice -n 10 ./rv_eng -E 2 -s 29 < ../Census29/out/frame-31.txt > out/w1_frame31.log 2> out/w1_frame31.err
