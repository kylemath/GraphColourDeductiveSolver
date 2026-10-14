#!/bin/zsh
# Job 11: census 22-28 (8 shards) and hardset-v1 (6 shards), nice 10
cd "$(dirname $0)"; mkdir -p out
for i in 0 1 2 3 4 5 6 7; do nice -n 10 node a6_run.js census22_28.json out/census_$i.jsonl --shard $i/8 > out/census_$i.log 2>&1 & done
for i in 0 1 2 3 4 5; do nice -n 10 node a6_run.js /tmp/hardset_maps.json out/hardset_$i.jsonl --shard $i/6 > out/hardset_$i.log 2>&1 & done
wait; echo DONE > out/DONE
