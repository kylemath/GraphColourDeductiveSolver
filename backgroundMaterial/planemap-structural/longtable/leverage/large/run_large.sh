#!/bin/sh
# first pass (c_pad_* outputs were later replaced by run_large2.sh). three lanes, nice 10, each python run capped at <= 14 min by --tlimit (per-hole sampler cap --htime)
cd "$(dirname "$0")"
C=/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working; T=$C/TrackF/graphs; M=/Users/fulkanjou/4square/maps
G=../../gluing
S="--nsamp 15000 --thin 4 --htime 45"
head -4 $C/Census29/out/frame-22.txt > out/in_frame22_4.txt     # pad bases (rebuilt, not committed)
GM=$M/r178.json,$M/r210.json,$M/trap17.json,$M/p34r189.json,$M/p33r115.json,$M/p34r28.json,$M/p32r111.json,$M/c60.json
( nice -n 10 python3 large.py rot $T/ipr32_52.txt out/a_ipr_exact.jsonl --family ipr --maxn 43 --holes 3 --tlimit 420
  nice -n 10 python3 large.py sw  $T/ipr32_52.txt out/a_sw_exact.jsonl --family nonipr --maxn 43 --holes 3 --tlimit 420
  nice -n 10 python3 large.py rot $T/ipr32_52.txt,$T/ipr62_part0.txt out/a_ipr_sample.jsonl --family ipr --minn 47 --graphs 20 --holes 2 --mode sample $S --tlimit 800
  nice -n 10 python3 large.py sw  $T/ipr32_52.txt,$T/ipr62_part0.txt out/a_sw_sample.jsonl --family nonipr --minn 47 --graphs 20 --holes 2 --mode sample $S --tlimit 800
) > out/log_a.txt 2>&1 &
( # (this tube run was stopped after 4 min and its output discarded; re-run in run_large2.sh with the odd-degree flag)
  # nice -n 10 python3 large.py rot $T/tubes.txt,$T/goldberg.txt out/a_tubes_sample.jsonl --family tube --minn 40 --graphs 70 --holes 1 --mode sample $S --tlimit 840
  nice -n 10 python3 large.py glued $G/run-tight.jsonl out/b_glued_exact.jsonl --family glued --graphs 8 --holes 2 --exactn 44 --tlimit 600
  nice -n 10 python3 large.py glued $G/round2.jsonl,$G/run-tight.jsonl out/b_glued_sample.jsonl --family glued --graphs 30 --holes 1 --mode sample $S --tlimit 840
) > out/log_b.txt 2>&1 &
( nice -n 10 python3 large.py pad $GM,out/in_frame22_4.txt out/c_pad_sample.jsonl --family pad --holes 2 --kmax 4 --mode sample $S --tlimit 840
  nice -n 10 python3 large.py pad $GM,out/in_frame22_4.txt out/c_pad_exact.jsonl --family pad --holes 2 --kmax 4 --exactn 60 --tlimit 840
) > out/log_c.txt 2>&1 &
