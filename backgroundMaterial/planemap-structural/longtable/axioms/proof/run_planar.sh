#!/bin/zsh
# planar windows: increase W until UNSAT/TIMEOUT, per n
cd ${0:a:h}
for n in 20 22 24 26 28; do
  for W in 5 6 7 8 9; do
    r=$(nice -n 10 python3 sat_planar.py window $n $W 400 | tee -a out/planar_windows.txt | head -1)
    echo "$r" | grep -q '"SAT"' || break
  done
done
