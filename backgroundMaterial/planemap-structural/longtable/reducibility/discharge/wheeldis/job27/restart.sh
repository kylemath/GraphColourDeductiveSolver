#!/bin/zsh
cd "$(dirname $0)"
nice -n 10 ../../studio15/cfast k2a2 --search --limit 1 >> k2a.cfast 2>&1 &
nice -n 10 ../../studio15/cfast k2b2 --search --limit 1 >> k2b.cfast 2>&1 &
nice -n 10 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/reverent-cartwright-aa34d5/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/.lake/build/bin/wheelcheck16 c8r.txt >> c_lean_D8_k3.out 2>&1 &
nice -n 10 /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/reverent-cartwright-aa34d5/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/.lake/build/bin/wheelcheck16 c9r.txt >> c_lean_D9_k4.out 2>&1 &
nice -n 10 /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/dfast18 b2.txt >> b_dfast18.out 2>&1 &
wait; echo done > restart.DONE
