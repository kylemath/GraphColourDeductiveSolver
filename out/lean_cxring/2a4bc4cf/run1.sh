#!/bin/zsh
# one CXRing entry: compile CXRkk.lean (hC_k by native_decide) into the 2a4bc4cf build, nice 15; log, time, exit
k=$1; mkdir "/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/out/lean_cxring/2a4bc4cf/lock_$k" 2>/dev/null || exit 0   # one run per entry across worker pools
SP=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad; W=$SP/glue_2a4bc4cf_build; L=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/out/lean_cxring/2a4bc4cf
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$W/cxr:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
cd $SP/cxr_src; t0=$(date +%s)
/usr/bin/time -l nice -n 15 env LEAN_PATH="$LP" $TC/bin/lean -o $W/cxr/CXR$k.olean -i $W/cxr/CXR$k.ilean CXR$k.lean > $L/CXR$k.log 2>$L/CXR$k.time
e=$?; echo "$k exit=$e wall=$(($(date +%s)-t0))s sorry=$(grep -c sorry $L/CXR$k.log) error=$(grep -c 'error' $L/CXR$k.log) rss=$(awk '/maximum resident/{print int($1/1048576)"MB"}' $L/CXR$k.time) $(date -u +%H:%M)" >> $L/status.txt
