#!/bin/zsh
# compile one ST-120 B5 module against the rsst118 build into out_st120b5, nice 15 (copy of b4/run.sh; LEAN_PATH adds out_st114 (B3/B1), out_st120b2 (B2), out_st120b4 (B4) and out_st120b5; the source path is absolute so that include_str resolves)
m=$1; W=/Users/kylemathewson/studio_lean_builds/rsst118_fb35d2d1; L=$(cd $(dirname $0) && pwd)
B=$HOME/mathlib4-planemap-build; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc3
LP=$W:$W/dc:$W/out_st114:$W/out_st120b2:$W/out_st120b4:$W/out_st120b5:$(ls -d $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
mkdir -p $W/out_st120b5; cd $L; t0=$(date +%s)
/usr/bin/time -l nice -n 15 env LEAN_PATH="$LP" $TC/bin/lean -o $W/out_st120b5/$m.olean -i $W/out_st120b5/$m.ilean $L/$m.lean > $L/$m.log 2>$L/$m.time
e=$?; echo "$m exit=$e wall=$(($(date +%s)-t0))s sorry=$(grep -c 'declaration uses .sorry' $L/$m.log) error=$(grep -c 'error' $L/$m.log) rss=$(awk '/maximum resident/{print int($1/1048576)"MB"}' $L/$m.time) $(date -u +%H:%M)" >> $L/status.txt
