#!/bin/zsh
cd ${0:a:h}
for n in 20 22 24 26; do
  nice -n 10 python3 sat_planar.py closed $n 10 560 >> out/planar_closed.txt
done
