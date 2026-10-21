#!/bin/zsh
# compile one CCover2 module (CCover2 / CC2Vkk / CC2All) into the 2a4bc4cf build (Lean dcheck sources identical at b6dc7610), nice 15
m=$1; SP=/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad; W=$SP/glue_2a4bc4cf_build; L=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/out/lean_ccover2/f2acc3e7
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$W/cc2:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
cd $SP/cc2_src; t0=$(date +%s)
/usr/bin/time -l nice -n 15 env LEAN_PATH="$LP" $TC/bin/lean -o $W/cc2/$m.olean -i $W/cc2/$m.ilean $m.lean > $L/$m.log 2>$L/$m.time
e=$?; echo "$m exit=$e wall=$(($(date +%s)-t0))s sorry=$(grep -c sorry $L/$m.log) error=$(grep -c 'error' $L/$m.log) rss=$(awk '/maximum resident/{print int($1/1048576)"MB"}' $L/$m.time) $(date -u +%H:%M)" >> $L/status.txt
