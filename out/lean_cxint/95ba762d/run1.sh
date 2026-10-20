#!/bin/zsh
# one CXInt entry: compile CXIkkk.lean (hC_k by native_decide) into the 2a4bc4cf build, nice 15; log, time, exit
k=$1; mkdir "/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/out/lean_cxint/95ba762d/lock_$k" 2>/dev/null || exit 0
SP=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad; W=$SP/glue_2a4bc4cf_build; L=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/out/lean_cxint/95ba762d
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$W/cxr:$W/cxi:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
cd $SP/cxi_src; t0=$(date +%s)
/usr/bin/time -l nice -n 15 env LEAN_PATH="$LP" $TC/bin/lean -o $W/cxi/CXI$k.olean -i $W/cxi/CXI$k.ilean CXI$k.lean > $L/CXI$k.log 2>$L/CXI$k.time
e=$?; echo "$k exit=$e wall=$(($(date +%s)-t0))s sorry=$(grep -c sorry $L/CXI$k.log) error=$(grep -c 'error' $L/CXI$k.log) rss=$(awk '/maximum resident/{print int($1/1048576)"MB"}' $L/CXI$k.time) $(date -u +%H:%M)" >> $L/status.txt
