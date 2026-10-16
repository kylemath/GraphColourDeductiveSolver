#!/bin/zsh
cd "$(dirname $0)"
awk 'NR%3==0' big_sample.txt > s0; awk 'NR%3==1' big_sample.txt > s1; awk 'NR%3==2' big_sample.txt > s2
for k in 0 1 2; do nice -n 19 /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/dfast18 s$k > s$k.out 2>&1 & done; wait
cat s0.out s1.out s2.out > big_sample.dfast
awk 'NR==FNR{if(/D=true/)d[$1]=1;next} !($1 in d)' big_sample.dfast big_sample.txt > cin
awk 'NR%3==0' cin > c0; awk 'NR%3==1' cin > c1; awk 'NR%3==2' cin > c2
for k in 0 1 2; do nice -n 19 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/studio15/cfast c$k --search --limit 1 > c$k.out 2>&1 & done; wait
cat c0.out c1.out c2.out > big_sample.cfast; echo done > DONE
