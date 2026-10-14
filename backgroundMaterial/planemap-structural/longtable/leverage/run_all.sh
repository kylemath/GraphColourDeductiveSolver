#!/bin/sh
# three lanes, nice 10; each python run is capped at <= 14 min by --tlimit
cd "$(dirname "$0")"
C=/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working; T=$C/TrackF; M=/Users/fulkanjou/4square/maps
cat $C/Census29/out/frame-2[2-8].txt > out/in_frame22_28.txt   # inputs are rebuilt, not committed
cat $C/Census29/out/frame-3[0-2].txt $C/Census33/out/frame-33.txt > out/in_frame30_33.txt
( nice -n 10 python3 leverage.py out/in_frame22_28.txt out/sphere_frame22_28.jsonl
  nice -n 10 python3 leverage.py $M/r178.json,$M/r210.json,$M/trap17.json,$M/p34r189.json,$M/p33r115.json,$M/p34r28.json,$M/p32r111.json,$M/c60.json out/gamemaps.jsonl --json --maxstates 3000000 ) > out/log_a.txt 2>&1 &
( nice -n 10 python3 leverage.py $T/graphs/torus.txt out/torus.jsonl --surface torus --sample 1500
  for s in rp2 klein genus2 rp2x3; do nice -n 10 python3 leverage.py $T/out/lpc/census_$s.graphs.txt out/$s.jsonl --surface $s --sample 1200 --tlimit 300; done ) > out/log_b.txt 2>&1 &
( nice -n 10 python3 leverage.py out/in_frame30_33.txt out/sphere_frame30_33.jsonl --sample 2500 --seed 7
  nice -n 10 python3 leverage.py $T/graphs/plantri24.txt out/sphere_plantri24.jsonl --sample 1500 --seed 3 ) > out/log_d.txt 2>&1 &
