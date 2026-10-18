#!/bin/zsh
# Job 24b completion (18 Oct): keys S2702..S2854, cut off by the 17 Oct 18:58 MDT outage. Same rule as run24b.sh
# (wheelcheck18 verdict + occurrence module, modules compiled in scratch, not committed), nice 19, one core;
# appended to results24b.txt, DONE written at the end.
cd ${0:a:h}
M=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/mods24b; mkdir -p $M
n=$(grep -c . k1_studioD.txt)
for i in $(seq 2702 $((n-1))); do
  ns=$(printf 'S%04d' $i)
  sed -n "$((i+1))p" k1_studioD.txt > $M/$ns.in
  v=$(nice -n 19 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/reverent-cartwright-aa34d5/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/.lake/build/bin/wheelcheck18 $M/$ns.in 2>&1 | grep -o 'D=[a-z]*')
  if ! python3 gen_occ_key.py k1_studioD.txt $i $ns $M 2> $M/$ns.gen.err; then echo "$ns $v GENFAIL" >> results24b.txt; continue; fi
  (cd ..; /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/lk.sh $M/$ns.lean > $M/$ns.out 2>&1)
  e=$(grep -c ': error' $M/$ns.out); so=$(grep -c sorryAx $M/$ns.out)
  echo "$ns $(cut -d' ' -f1-2 $M/$ns.in) $v errors=$e sorry=$so" >> results24b.txt
  [ $e = 0 ] && rm -f $M/$ns.out
done
echo DONE >> results24b.txt
