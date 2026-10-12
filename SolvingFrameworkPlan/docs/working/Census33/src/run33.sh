#!/bin/bash
# Census33 pipeline: (1) plantri -m5 -c4 33 res/256 | frame (256 shards), (2) frame-33.txt, (3) eval33.py in chunks of 100.
# Load-aware parallelism via runq.py (12 workers, 6 when load > 30 for > 10 min). Restartable.
cd "$(dirname "$0")/.."; B=$PWD
python3 src/runq.py out/gen_jobs.txt out/gen_progress.log --max 12 --low 6
nd=$(ls out/shards/33/*.txt 2>/dev/null | wc -l | tr -d ' '); echo "$(date +%T) shards with output: $nd" >> out/pipeline.log
[ "$nd" = 256 ] || { echo "incomplete generation" >> out/pipeline.log; exit 1; }
for r in $(seq 0 255); do cat out/shards/33/$r.txt; done > out/frame-33.txt
echo "$(date +%T) frame-33: $(wc -l < out/frame-33.txt) graphs" >> out/pipeline.log
mkdir -p out/eval/in; [ -n "$(ls out/eval/in)" ] || split -l 100 -a 4 out/frame-33.txt out/eval/in/c
for c in $(ls out/eval/in); do printf "%s\tcd $B && nice -n 10 python3 src/eval33.py out/eval/in/%s out/eval/%s.jsonl.tmp && mv out/eval/%s.jsonl.tmp out/eval/%s.jsonl && mv out/eval/%s.jsonl.tmp.runs out/eval/%s.runs\n" $c $c $c $c $c $c $c; done > out/eval_jobs.txt
python3 src/runq.py out/eval_jobs.txt out/eval_progress.log --max 12 --low 6
cat out/eval/c*.jsonl > out/eval-33.jsonl; cat out/eval/c*.runs > out/runs-33.jsonl
echo "$(date +%T) eval done: $(wc -l < out/eval-33.jsonl) records" >> out/pipeline.log
