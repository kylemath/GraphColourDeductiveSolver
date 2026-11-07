#!/bin/zsh
# compile one HDC502 module into /Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1/out_hdk3, nice 15; logs wall, user+sys CPU and peak RSS
m=$1; W=/Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1; L=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_HDK3/lean
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$W/out_hdk3:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
mkdir -p $W/out_hdk3; cd $L; t0=$(date +%s)
/usr/bin/time -l nice -n 20 env LEAN_PATH="$LP" $TC/bin/lean -o $W/out_hdk3/$m.olean -i $W/out_hdk3/$m.ilean $m.lean > $L/$m.log 2>$L/$m.time
e=$?; echo "$m exit=$e wall=$(($(date +%s)-t0))s user=$(awk '/ user /{print $3}' $L/$m.time) sys=$(awk '/ sys/{print $5}' $L/$m.time) sorry=$(grep -c sorry $L/$m.log) error=$(grep -c 'error' $L/$m.log) rss=$(awk '/maximum resident/{print int($1/1048576)"MB"}' $L/$m.time) $(date -u +%H:%M)" >> $L/status.txt
