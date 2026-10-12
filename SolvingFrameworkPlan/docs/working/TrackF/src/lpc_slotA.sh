#!/bin/sh
# Track F LPC census, one process, surfaces in sequence
cd "$(dirname "$0")/.."
for s in torus klein rp2 genus2 rp2x3; do
  nice -n 10 python3 src/lpc_census.py $s 600 16 40 11 out/lpc/census_$s >> out/lpc/census.log 2>&1
done
echo done >> out/lpc/census.log
