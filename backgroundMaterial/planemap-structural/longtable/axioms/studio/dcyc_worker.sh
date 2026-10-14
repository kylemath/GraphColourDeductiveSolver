#!/bin/zsh
# Studio Job 5 worker: claims shards of out/dcyc/shards (mkdir lock), runs dcyc rot, writes out/dcyc/res/<shard>.jsonl.
# Start any number of these (each is one process, nice 10).
cd "$(dirname $0)"
mkdir -p out/dcyc/res out/dcyc/lock
for s in out/dcyc/shards/*(N); do
  b=${s:t}
  mkdir out/dcyc/lock/$b 2>/dev/null || continue
  nice -n 10 ./dcyc rot < $s > out/dcyc/res/$b.tmp && mv out/dcyc/res/$b.tmp out/dcyc/res/$b.jsonl
  grep -h '"R0c_violation": true' out/dcyc/res/$b.jsonl >> out/dcyc/ALERT.jsonl
done
