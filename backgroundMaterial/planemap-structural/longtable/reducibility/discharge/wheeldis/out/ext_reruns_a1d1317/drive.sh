#!/bin/zsh
# shard k of 12: P1 then P2 then P3, our binaries (kc 07e79fae, cfast de59e72f), nice 10
cd "$(dirname $0)"; k=$1; W=../..
for p in 1 2 3; do
  nice -n 10 python3 run_queue_t600.py $W/loop/kc/kc $W/../studio15/cfast jobs_p$p.txt in/configs.in in/X.txt p${p}_s$k.tsv $k 12
  echo done > p${p}_s$k.done
done
