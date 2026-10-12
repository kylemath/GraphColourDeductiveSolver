#!/bin/bash
# Census34 pipeline (same as Census33/src/run33.sh, order 34): (1) plantri -m5 -c4 34 res/256 | frame (256 shards),
# (2) frame-34.txt, (3) eval34.py in chunks of 100. Load-aware parallelism via runq.py (12 workers, 6 when load > 30
# for > 10 min). Restartable: runq.py skips jobs logged as done; shard/chunk outputs are written via .tmp + mv.
# usage: run34.sh pilot   (shards 0,1,2 of 256 + their evaluation in out/pilot/)
#        run34.sh full    (all 256 shards; pilot shards are reused)
cd "$(dirname "$0")/.."; B=$PWD; MODE=${1:-full}; mkdir -p out/shards/34
gj() { printf "g%s\tcd $B && /usr/bin/time -p nice -n 10 bin/plantri -m5 -c4 34 %s/256 2>out/shards/34/%s.plog | nice -n 10 bin/frame p34.r%s > out/shards/34/%s.txt.tmp 2> out/shards/34/%s.count && mv out/shards/34/%s.txt.tmp out/shards/34/%s.txt\n" $1 $1 $1 $1 $1 $1 $1 $1; }
ej() { printf "%s\tcd $B && nice -n 10 python3 src/eval34.py %s/in/%s %s/%s.jsonl.tmp && mv %s/%s.jsonl.tmp %s/%s.jsonl && mv %s/%s.jsonl.tmp.runs %s/%s.runs\n" $2 $1 $2 $1 $2 $1 $2 $1 $2 $1 $2 $1 $2; }
if [ "$MODE" = pilot ]; then
  echo "$(date +%T) pilot launch" >> out/pipeline.log
  for r in 0 1 2; do gj $r; done > out/gen_jobs_pilot.txt
  python3 src/runq.py out/gen_jobs_pilot.txt out/gen_progress.log --max 12 --low 6
  mkdir -p out/pilot/eval/in; for r in 0 1 2; do cat out/shards/34/$r.txt; done > out/pilot/frame-pilot.txt
  [ -n "$(ls out/pilot/eval/in)" ] || split -l 100 -a 4 out/pilot/frame-pilot.txt out/pilot/eval/in/c
  for c in $(ls out/pilot/eval/in); do ej out/pilot/eval $c; done > out/pilot/eval_jobs.txt
  python3 src/runq.py out/pilot/eval_jobs.txt out/pilot/eval_progress.log --max 12 --low 6
  cat out/pilot/eval/c*.jsonl > out/pilot/eval-pilot.jsonl
  echo "$(date +%T) pilot done: $(wc -l < out/pilot/frame-pilot.txt) frame graphs" >> out/pipeline.log
  exit 0
fi
echo "$(date +%T) full launch" >> out/pipeline.log
for r in $(seq 0 255); do gj $r; done > out/gen_jobs.txt
python3 src/runq.py out/gen_jobs.txt out/gen_progress.log --max 12 --low 6
nd=$(ls out/shards/34/*.txt 2>/dev/null | wc -l | tr -d ' '); echo "$(date +%T) shards with output: $nd" >> out/pipeline.log
[ "$nd" = 256 ] || { echo "incomplete generation" >> out/pipeline.log; exit 1; }
for r in $(seq 0 255); do cat out/shards/34/$r.txt; done > out/frame-34.txt
echo "$(date +%T) frame-34: $(wc -l < out/frame-34.txt) graphs" >> out/pipeline.log
mkdir -p out/eval/in; [ -n "$(ls out/eval/in)" ] || split -l 100 -a 4 out/frame-34.txt out/eval/in/c
for c in $(ls out/eval/in); do ej out/eval $c; done > out/eval_jobs.txt
python3 src/runq.py out/eval_jobs.txt out/eval_progress.log --max 12 --low 6
cat out/eval/c*.jsonl > out/eval-34.jsonl; cat out/eval/c*.runs > out/runs-34.jsonl
echo "$(date +%T) eval done: $(wc -l < out/eval-34.jsonl) records" >> out/pipeline.log
