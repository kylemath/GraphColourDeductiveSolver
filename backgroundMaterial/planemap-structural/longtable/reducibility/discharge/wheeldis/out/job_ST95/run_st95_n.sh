#!/bin/bash
# ST-95: sol_k86GS20_in01 (aacc2ff6) with the 174 nonzero keys (c8349589) on code_gk8 (check8.sh); families in order, stop at the first FEASIBLE main, then tneg there.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/job_ST95; B=/tmp/swarm-W17; P=sol_k86GS20_in01
: cp $J/in/$P.json $B/sol/; python3 -I - "$B/sol/$P.json" "$B/sol/${P}_tneg.json" <<'PY'
import re, sys
s = open(sys.argv[1]).read(); m = re.match(r'\{"t": ([0-9.eE+-]+)', s); t = float(m.group(1))
open(sys.argv[2], 'w').write('{"t": ' + repr(t - 5e-6) + s[m.end():]); print('t', t, 'tneg', t - 5e-6)
PY
cp $B/sol/${P}_tneg.json $J/in/
C="GK=$B/tab/cg_keys_GS20_nonzero.txt RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json W17NICE=20"
for spec in K3gB5n:18237,781,158; do
  F=${spec%%:*}; E=${spec#*:}
  cd $B; env $C ARGSF=$B/args_A97F_W13${F}_x_studio.txt EXPECT_PAT=$E TAG=${P}_z${F}_gk8 nice -n 15 bash $B/check8.sh $B/sol/$P.json 6 > $J/main_$F.out 2>&1
  cat $B/logs/${P}_z${F}_gk8/viol_d*.txt 2>/dev/null | grep -v '^#' | sort -u > $J/main_${F}_receiver_violators.txt
  echo "$F main: $(grep -E '^RESULT' $J/main_$F.out | cut -c1-60)"
  if grep -q '^RESULT: FEASIBLE' $J/main_$F.out; then
    env $C ARGSF=$B/args_A97F_W13${F}_x_studio.txt EXPECT_PAT=$E TAG=${P}_tneg_z${F}_gk8 nice -n 15 bash $B/check8.sh $B/sol/${P}_tneg.json 6 > $J/tneg_$F.out 2>&1
    cat $B/logs/${P}_tneg_z${F}_gk8/viol_d*.txt 2>/dev/null | grep -v '^#' | sort -u > $J/tneg_${F}_receiver_violators.txt
    echo "$F tneg: $(grep -E '^RESULT' $J/tneg_$F.out | cut -c1-60)"; echo "FAMILY $F"; break
  fi
done
echo ST95DONE
