#!/bin/zsh
# Job 24b remainder, claim-based worker ID (18 Oct 17:2xZ, Long Table go): takes any key S2703..S2854 that no one has
# claimed (atomic mkdir in /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/claims24b), same rule as run24b.sh; output results24b_c<ID>.txt.
cd ${0:a:h}; ID=$1; CL=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/claims24b
M=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/mods24b; mkdir -p $M; OUT=results24b_c$ID.txt; touch $OUT
n=$(grep -c . k1_studioD.txt)
for i in $(seq 2703 $((n-1))); do
  ns=$(printf 'S%04d' $i)
  mkdir $CL/$ns 2>/dev/null || continue
  sed -n "$((i+1))p" k1_studioD.txt > $M/$ns.in
  v=$(nice -n 19 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/reverent-cartwright-aa34d5/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/.lake/build/bin/wheelcheck18 $M/$ns.in 2>&1 | grep -o 'D=[a-z]*')
  if ! python3 gen_occ_key.py k1_studioD.txt $i $ns $M 2> $M/$ns.gen.err; then echo "$ns $v GENFAIL" >> $OUT; continue; fi
  (cd ..; /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/lk.sh $M/$ns.lean > $M/$ns.out 2>&1)
  e=$(grep -c ': error' $M/$ns.out); so=$(grep -c sorryAx $M/$ns.out)
  echo "$ns $(cut -d' ' -f1-2 $M/$ns.in) $v errors=$e sorry=$so" >> $OUT
  [ $e = 0 ] && rm -f $M/$ns.out
done
echo done > C$ID.DONE
