#!/bin/zsh
# Studio Job 6 walks: 12 workers, nice 10, about 3 h (killed by the caller's cap).
cd "$(dirname $0)"
i=0
for spec in "torus 11" "torus 12" "torus 13" "klein 21" "klein 22" "klein 23" "rp2 31" "rp2 32" "genus2 41" "genus2 42" "rp2x3 51" "rp2x3 52"; do
  set -- ${=spec}
  nice -n 10 python3 walk.py $1 $2 100000000 out/walks/$1_$2 > out/walks/$1_$2.out 2>&1 &
done
wait
