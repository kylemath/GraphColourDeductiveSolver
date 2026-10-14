#!/bin/zsh
# Job 7 step 2 worker: fullerene / IPR / Goldberg / glued inputs in out/extra/in_*; skip holes with more than 1M states
cd "$(dirname $0)"
mkdir -p out/extra/res out/extra/lock
for s in out/extra/in_*(N); do
  b=${s:t}
  mkdir out/extra/lock/$b 2>/dev/null || continue
  nice -n 10 ./bnd --dump-fail --distscan --maxS 1000000 < $s > out/extra/res/$b.tmp && mv out/extra/res/$b.tmp out/extra/res/$b.jsonl
done
