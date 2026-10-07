#!/bin/bash
# all degree-5 holes of the six C6 adversarial graphs, 40 random colourings each (seed 1), single core
D=../../../studiointel/path3-local/run_dd
rm -f big.jsonl
for g in A5_exc A6_chain A7_exc K3_exc hog1152_chain r5_80b930d1_exc; do
 for h in $(python3 -c "
import json
from collections import Counter
f=json.load(open('$D/best-$g.json'))['faces']
c=Counter(v for t in f for v in t); print(' '.join(str(v) for v in sorted(c) if c[v]==5))"); do
  nice -n 10 python3 adv.py $D/best-$g.json $h 1 40 big.jsonl
 done
done
