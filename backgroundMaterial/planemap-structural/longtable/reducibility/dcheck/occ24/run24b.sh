#!/bin/zsh
# Job 24b: the 2,855 Studio-D K=1 keys (rings 9-16, Job 14): wheelcheck18 (DCheck18 executable) verdict
# and the occurrence module, one key at a time, nice 15. Modules are compiled in scratch and not committed.
cd ${0:a:h}
until grep -q DONE results.txt; do sleep 30; done
M=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/j19/mods24b; mkdir -p $M
: > results24b.txt
n=$(grep -c . k1_studioD.txt)
for i in $(seq 0 $((n-1))); do
  ns=$(printf 'S%04d' $i)
  sed -n "$((i+1))p" k1_studioD.txt > $M/$ns.in
  v=$(nice -n 15 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/reverent-cartwright-aa34d5/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/.lake/build/bin/wheelcheck18 $M/$ns.in 2>&1 | grep -o 'D=[a-z]*')
  if ! python3 gen_occ_key.py k1_studioD.txt $i $ns $M 2> $M/$ns.gen.err; then echo "$ns $v GENFAIL" >> results24b.txt; continue; fi
  /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/j19/lk.sh $M/$ns.lean > $M/$ns.out 2>&1
  e=$(grep -c 'error' $M/$ns.out); so=$(grep -c sorryAx $M/$ns.out)
  echo "$ns $(cut -d' ' -f1-2 $M/$ns.in) $v errors=$e sorry=$so" >> results24b.txt
  [ $e = 0 ] && rm -f $M/$ns.out
done
echo DONE >> results24b.txt
