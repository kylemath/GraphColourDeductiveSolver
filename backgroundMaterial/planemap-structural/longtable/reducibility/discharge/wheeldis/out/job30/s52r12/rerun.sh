#!/bin/zsh
# Studio re-run of untraced s52r1/s52r2 f-names on both engines (light, nice 19): kc -C; kc D -> dfast18; kc X -> cfast --fixed X.
# usage: rerun.sh PART K   (takes lines with index % K == PART of untraced.txt)
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$W/out/job30/s52r12; P=$1; K=$2; i=0
while IFS= read -r l; do
  if (( i % K == P )); then
    echo "$l" > $S/w$P.in
    o=$(nice -n 19 $W/loop/kc/kc -C -s 60 -t 600 $S/w$P.in 2>&1); echo "$o" >> $S/kc_p$P.out
    if echo "$o" | grep -q 'D=true'; then nice -n 19 $W/out/job52/dfast18 $S/w$P.in >> $S/df_p$P.out 2>&1
    else x=$(echo "$o" | sed -n 's/.*C-REDUCIBLE X={\([^}]*\)}.*/\1/p' | head -1)
      [ -n "$x" ] && nice -n 19 $W/../studio15/cfast $S/w$P.in --fixed "$x" >> $S/cf_p$P.cfast 2>&1; fi
  fi; i=$((i+1))
done < $S/${3:-untraced.txt}
echo DONE > $S/DONE_p$P
