#!/bin/sh
# Track F slot 2: icosahedral (Goldberg-Coxeter) fullerene duals, one hole each (all 12 equivalent), sampling
cd "$(dirname "$0")/.."
for g in GC30_C180 GC22_C240 GC40_C320; do
  grep "^$g " graphs/goldberg.txt > out/gold/$g.in
  h=$(python3 -c "import sys; p=open('out/gold/$g.in').read().split(); rot=[r.split(',') for r in p[2].split(';')]; print([i for i,r in enumerate(rot) if len(r)==5][0])")
  for s in 1 2 3 4; do nice -n 10 ./src/f66_w4_new out/gold/$g.in --holes $h --sample 2000000 --seed $s --budget 200000 --dump 12 --dumpfile out/gold/$g.s$s.runs.jsonl >> out/gold/$g.holes.jsonl 2>> out/gold/$g.err; done
done
grep "^GC33_C540 " graphs/goldberg.txt > out/gold/GC33_C540.in
h=$(python3 -c "import sys; p=open('out/gold/GC33_C540.in').read().split(); rot=[r.split(',') for r in p[2].split(';')]; print([i for i,r in enumerate(rot) if len(r)==5][0])")
nice -n 10 ./src/f66_w5_new out/gold/GC33_C540.in --holes $h --sample 1000000 --seed 1 --budget 400000 --dump 12 --dumpfile out/gold/GC33_C540.runs.jsonl >> out/gold/GC33_C540.holes.jsonl 2>> out/gold/GC33_C540.err
echo done > out/gold/DONE
