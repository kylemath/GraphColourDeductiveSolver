#!/bin/sh
# Track A phase 2: beyond-census frame-class seeds (grown, n = 32, 36) + IPR dual n = 32; searches M and W. Waits for phase 1.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
# (phase 1 already done; restarted 13:53 without p24#2550, which is rigid: no frame-preserving growth found in 10 min)
for N in 32 36; do
  nice -n 10 python3 grow_seeds.py out/grow-$N-a.json $N p26#6120 > out/grow-$N-a.log 2>&1 &
  nice -n 10 python3 grow_seeds.py out/grow-$N-b.json $N p27#47915 > out/grow-$N-b.log 2>&1 &
  nice -n 10 python3 grow_seeds.py out/grow-$N-c.json $N p27#8475 > out/grow-$N-c.log 2>&1 &
  nice -n 10 python3 grow_seeds.py out/grow-$N-d.json $N p28#546102 > out/grow-$N-d.log 2>&1 &
  wait
done
nice -n 10 python3 -c "
import json, glob
from tracka_lib import parse_line, faces_from_rot
S = [s for fn in sorted(glob.glob('out/grow-*.json')) for s in json.load(open(fn))]
for l in open('out/ipr32.txt'):
    n, rot = parse_line(l); S.append(dict(name=n, faces=faces_from_rot(rot)))
json.dump(S, open('out/seeds-phase2.json', 'w')); print(len(S), 'phase-2 seeds')
" > out/phase2-seeds.log 2>&1
nice -n 10 python3 tracka_search.py out/seeds-phase2.json 200 1 out/search-phase2.jsonl M,W > out/search-phase2.log 2>&1
echo ALLDONE >> out/search-phase2.log
