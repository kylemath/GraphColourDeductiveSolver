#!/bin/zsh
# Job 24: generate and compile one occurrence module per deferred K=1 key (sequential, nice 15)
cd ${0:a:h}
n=$(grep -c . ../../discharge/studio14b/k1_r17_19.txt)
: > results.txt
for i in $(seq 0 $((n-1))); do
  ns=$(printf 'K%02d' $i)
  if ! python3 gen_occ_key.py ../../discharge/studio14b/k1_r17_19.txt $i $ns . 2> $ns.gen.err; then echo "$ns GENFAIL" >> results.txt; continue; fi
  s=$(date +%s)
  /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/j19/lk.sh $ns.lean > $ns.out 2>&1
  e=$(grep -c 'error' $ns.out); so=$(grep -c sorryAx $ns.out)
  echo "$ns $(head -c 60 <(sed -n "$((i+1))p" ../../discharge/studio14b/k1_r17_19.txt | cut -d' ' -f1)) errors=$e sorry=$so $(($(date +%s)-s))s" >> results.txt
done
echo DONE >> results.txt
