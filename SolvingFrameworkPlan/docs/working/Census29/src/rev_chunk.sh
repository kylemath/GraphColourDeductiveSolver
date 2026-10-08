#!/bin/bash
# helper: evaluate one chunk of order N if neither finished nor in progress (used to add workers from the end of the list)
N=$1; c=$2; D=out/eval/$N
if [ ! -s $D/$c.jsonl ] && [ ! -e $D/$c.jsonl.tmp ] && [ ! -e $D/$c.jsonl.tmp2 ]; then
  nice -n 10 python3 src/eval_shard.py $D/in/$c $D/$c.jsonl.tmp2 && mv $D/$c.jsonl.tmp2 $D/$c.jsonl && echo "$(date +%T) $c rev" >> $D/progress
fi
