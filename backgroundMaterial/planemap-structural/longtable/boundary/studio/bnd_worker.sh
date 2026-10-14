#!/bin/zsh
# Job 7 worker: claims census shards (mkdir lock), runs bnd (nice 10) -> out/census/res/<shard>.jsonl
cd "$(dirname $0)"
SH=../../axioms/studio/out/dcyc/shards
mkdir -p out/census/res out/census/lock
for s in $SH/*(N); do
  b=${s:t}
  mkdir out/census/lock/$b 2>/dev/null || continue
  nice -n 10 ./bnd --dump-fail < $s > out/census/res/$b.tmp && mv out/census/res/$b.tmp out/census/res/$b.jsonl
done
