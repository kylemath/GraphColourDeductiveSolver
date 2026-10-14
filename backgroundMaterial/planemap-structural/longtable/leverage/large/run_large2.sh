#!/bin/sh
# lane c, second pass (odd-degree-chain flag present): tubes + Goldberg, then padding (sample and exact)
cd "$(dirname "$0")"
C=/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working; T=$C/TrackF/graphs; M=/Users/fulkanjou/4square/maps
S="--nsamp 15000 --thin 4 --htime 45"
GM=$M/r178.json,$M/r210.json,$M/trap17.json,$M/p34r189.json,$M/p33r115.json,$M/p34r28.json,$M/p32r111.json,$M/c60.json
( nice -n 10 python3 large.py rot $T/tubes.txt,$T/goldberg.txt out/a_tubes_sample.jsonl --family tube --minn 40 --holes 1 --mode sample --nsamp 12000 --thin 4 --htime 30 --tlimit 840
  nice -n 10 python3 large.py pad $GM,out/in_frame22_4.txt out/c_pad_sample.jsonl --family pad --holes 3 --kmax 4 --mode sample $S --tlimit 840
  nice -n 10 python3 large.py pad $GM,out/in_frame22_4.txt out/c_pad_exact.jsonl --family pad --holes 3 --kmax 4 --exactn 60 --tlimit 840
) > out/log_c2.txt 2>&1 &
( nice -n 10 python3 large.py rot $T/tubes.txt,$T/goldberg.txt out/a_tubes_exact.jsonl --family tube --maxn 44 --holes 4 --exactn 44 --tlimit 600 ) > out/log_b2.txt 2>&1 &
# third pass: more Goldberg samples, more exact glued holes
( nice -n 10 python3 large.py rot $T/goldberg.txt out/a_goldberg2_sample.jsonl --family goldberg --minn 80 --holes 4 --mode sample --nsamp 30000 --thin 4 --htime 50 --tlimit 800 ) > out/log_g.txt 2>&1 &
( nice -n 10 python3 large.py glued ../../gluing/run-tight.jsonl out/b_glued_exact2.jsonl --family glued --graphs 30 --holes 1 --seed 5 --exactn 44 --tlimit 660 ) > out/log_b3.txt 2>&1 &
( nice -n 10 python3 large.py rot $T/tubes.txt,$T/goldberg.txt out/val_tubes_sample.jsonl --family val --maxn 44 --holes 4 --mode sample --nsamp 15000 --thin 4 --htime 45 --tlimit 600 ) > out/log_v.txt 2>&1 &  # sampler validation: same holes as a_tubes_exact
