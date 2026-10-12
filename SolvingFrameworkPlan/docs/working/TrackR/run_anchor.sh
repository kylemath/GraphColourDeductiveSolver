#!/bin/sh
# shared anchored rule (part tags at t-1..t+1 plus offset from an anchor) for pairs of cycles: 230 (anchor 0) vs B (anchor b)
cd "$(dirname "$0")"
A=data/n1_7121_17_230_K_L_L_data.json
for B in n1_7121_138_352 n1_7511_15_2656 n1_7511_15_3104 n1_7221_43_1416 n1_7511_14_2004 n1_7121_119_1473; do
  for b in 0 1 2 3 4 5 6 7 8 9; do echo "$B $b"; done
done | xargs -P 4 -L 1 sh -c 'nice -n 10 ../TrackQ/.venv/bin/python tr_rule.py 1 partA '$A'@0 data/$0_data.json@$1 2>&1 | grep RESULT | sed "s/^/$0 b=$1 /"' > out/anchor_pairs.log
