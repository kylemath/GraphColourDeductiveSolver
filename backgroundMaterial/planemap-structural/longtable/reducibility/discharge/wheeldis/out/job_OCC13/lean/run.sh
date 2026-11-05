#!/bin/zsh
# compile one OCC13 module into /Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1/occ13 (COccBridge into dc), nice 15; logs wall/user/sys/RSS
m=$1; src=${2:-/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_OCC13/lean/$m.lean}; out=${3:-/Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1/occ13}; W=/Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1; L=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_OCC13/lean
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$W/occ13:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
mkdir -p $out; cd $L; t0=$(date +%s)
/usr/bin/time -l nice -n 15 env LEAN_PATH="$LP" $TC/bin/lean -o $out/$m.olean -i $out/$m.ilean $src > $L/$m.log 2>$L/$m.time
e=$?; echo "$m exit=$e wall=$(($(date +%s)-t0))s user=$(awk '/ user /{print $3}' $L/$m.time) sorry=$(grep -c sorry $L/$m.log) error=$(grep -c 'error' $L/$m.log) rss=$(awk '/maximum resident/{print int($1/1048576)"MB"}' $L/$m.time) $(date -u +%H:%M)" >> $L/status.txt
