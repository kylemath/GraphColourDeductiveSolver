#!/bin/zsh
# Job 24b remainder worker K (of 4; Long Table 18 Oct): keys S2703..S2854 with index mod 4 = K. Same rule as
# run24b.sh (wheelcheck18 verdict + occurrence module, modules in scratch). Optional 2nd arg: a pid to wait for first
# (worker 3 starts when the xcap test ends). Output results24b_w<K>.txt, then W<K>.DONE.
cd ${0:a:h}; K=$1
[ -n "$2" ] && while kill -0 $2 2>/dev/null; do python3 -c 'import time; time.sleep(60)'; done
M=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/mods24b; mkdir -p $M; OUT=results24b_w$K.txt; : > $OUT
n=$(grep -c . k1_studioD.txt)
for i in $(seq 2703 $((n-1))); do
  [ $((i % 4)) = $K ] || continue
  ns=$(printf 'S%04d' $i)
  sed -n "$((i+1))p" k1_studioD.txt > $M/$ns.in
  v=$(nice -n 19 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/reverent-cartwright-aa34d5/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/.lake/build/bin/wheelcheck18 $M/$ns.in 2>&1 | grep -o 'D=[a-z]*')
  if ! python3 gen_occ_key.py k1_studioD.txt $i $ns $M 2> $M/$ns.gen.err; then echo "$ns $v GENFAIL" >> $OUT; continue; fi
  (cd ..; /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/lk.sh $M/$ns.lean > $M/$ns.out 2>&1)
  e=$(grep -c ': error' $M/$ns.out); so=$(grep -c sorryAx $M/$ns.out)
  echo "$ns $(cut -d' ' -f1-2 $M/$ns.in) $v errors=$e sorry=$so" >> $OUT
  [ $e = 0 ] && rm -f $M/$ns.out
done
echo done > W$K.DONE
