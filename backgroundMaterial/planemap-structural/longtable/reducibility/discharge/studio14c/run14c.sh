#!/bin/zsh
# 43 deferred K=1 keys (36 r17 + 7 r18), wheelcheck18, 12 workers, nice 10, longest first
cd "$(dirname $0)"
mkdir -p out
ls in | xargs -P 12 -I{} zsh -c 'nice -n 10 /usr/bin/time -l ../../dcheck/.lake/build/bin/wheelcheck18 in/{} > out/{}.out 2> out/{}.time'
echo DONE > DONE
