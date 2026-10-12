#!/bin/bash
# usage: eval_all.sh N PAR -- split out/frame-N.txt into chunks of 50 lines, run eval_shard.py on each (PAR at a time, nice 10);
# chunks with an existing .jsonl are skipped (restartable); out/eval/N/progress logs finished chunks; DONE marker at the end.
N=$1; PAR=${2:-4}; cd "$(dirname "$0")/.."; D=out/eval/$N; mkdir -p $D/in
[ -n "$(ls $D/in 2>/dev/null)" ] || split -l 50 -a 4 out/frame-$N.txt $D/in/c
ls $D/in | xargs -P $PAR -I{} bash -c "if [ ! -s $D/{}.jsonl ]; then nice -n 10 python3 src/eval_shard.py $D/in/{} $D/{}.jsonl.tmp && mv $D/{}.jsonl.tmp $D/{}.jsonl && echo \$(date +%T) {} >> $D/progress; fi"
cat $D/c*.jsonl > out/eval-$N.jsonl; touch $D/DONE
