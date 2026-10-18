#!/bin/zsh
# Job 26 (a): derived-dinj walk modules for the 49 deferred keys (no ring injectivity assumed), nice 19, one core;
# waits until at most 15 heavy jobs besides k19 are running (core counting).
cd ${0:a:h}
heavy() { ps -axo %cpu=,command= | awk '$1 > 40 && $0 !~ /wheelcheck18 k19/ && $0 !~ /mediaanalysisd/' | wc -l; }
until [ $(heavy) -le 14 ]; do python3 -c 'import time; time.sleep(120)'; done
n=$(grep -c . ../../discharge/studio14b/k1_r17_19.txt); : > walkD_results.txt
for i in $(seq 0 $((n-1))); do
  ns=$(printf 'D%02d' $i)
  if ! python3 gen_occ_walk.py ../../discharge/studio14b/k1_r17_19.txt $i $ns /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/w26d 2> /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/w26d/$ns.gen.err; then echo "$ns GENFAIL $(tail -1 /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/w26d/$ns.gen.err)" >> walkD_results.txt; continue; fi
  s=$(date +%s); (cd ..; /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/lk.sh /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/w26d/$ns.lean > /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/w26d/$ns.out 2>&1)
  e=$(grep -c ': error' /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/w26d/$ns.out); so=$(grep -c sorryAx /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/w26d/$ns.out)
  echo "$ns $(sed -n "$((i+1))p" ../../discharge/studio14b/k1_r17_19.txt | cut -d' ' -f1-2) errors=$e sorry=$so $(( $(date +%s)-s ))s" >> walkD_results.txt
done
echo DONE >> walkD_results.txt
