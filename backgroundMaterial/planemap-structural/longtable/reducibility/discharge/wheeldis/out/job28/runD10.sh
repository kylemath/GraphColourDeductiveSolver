#!/bin/zsh
# Job 28 one-off: rest of the lone-5-at-10 family (pairs.py 10 5, ring <= 16): dfast18 then cfast, nice 19
cd "$(dirname $0)"
for k in 0 1 2; do awk -v k=$k 'NR%3==k' D10k5_rest.txt > D10_$k; done
for k in 0 1 2; do (while IFS= read -r l; do print -r -- "$l" > D10_$k.x; nice -n 19 /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/dfast18 D10_$k.x; done < D10_$k > D10_$k.out 2>&1) & done; wait
cat D10_0.out D10_1.out D10_2.out > r_D10k5.out
awk 'NR==FNR{if(/D=true/)d[$1]=1;next} !($1 in d)' r_D10k5.out D10k5_rest.txt > D10_cin
for k in 0 1 2; do awk -v k=$k 'NR%3==k' D10_cin > D10c_$k; nice -n 19 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/studio15/cfast D10c_$k --search --limit 1 > D10c_$k.out 2>&1 & done; wait
cat D10c_0.out D10c_1.out D10c_2.out > r_D10k5.cfast; echo done > D10.DONE
