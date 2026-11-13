#!/bin/bash
# sequential world enumerations (one core, nice 19); each saves its own pickle
cd /tmp/swarm-W16
for spec in "567 7" "578 7,8" "568 8" "5678 7"; do
  set -- $spec; tag=$(echo "$1_$2" | tr ',' '-')
  for v in std noA111; do
    out=data/world_${tag}_${v}.pkl; [ -s $out ] && continue
    if [ $v = noA111 ]; then E="NOA111=1"; else E="NOA111=0"; fi
    env $E timeout 1700 nice -n 19 python3 -I code/world.py $1 $2 $out > logs/world_${tag}_${v}.log 2>&1
    env $E timeout 1700 nice -n 19 python3 -I code/world_lp.py $out data/world_${tag}_${v}_lp.json >> logs/world_${tag}_${v}.log 2>&1
  done
done
echo ALLDONE
