#!/bin/bash
# ST-108: sol_k86GS21_in02 (2d6c1779) on gk9 (check9.sh) + K3gB5n (8430a441), 186 nonzero keys (19 payer-8, 4 HATBB), main + tneg
J=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_ST108/point; B=/tmp/swarm-W17; P=sol_k86GS21_in02
python3 -I - "$B/sol/$P.json" "$B/sol/${P}_tneg.json" <<'PY'
import re, sys
s = open(sys.argv[1]).read(); m = re.match(r'\{"t": ([0-9.eE+-]+)', s); t = float(m.group(1))
open(sys.argv[2], 'w').write('{"t": ' + repr(t - 5e-6) + s[m.end():]); print('t', t, 'tneg', t - 5e-6)
PY
C="GK=$B/tab/cg_keys_GS21_nonzero.txt RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json W17NICE=20 ARGSF=$B/args_A97F_W13K3gB5n_x_studio.txt EXPECT_PAT=18237,781,158"
cd $B; env $C TAG=${P}_zK3gB5n_gk9 nice -n 15 bash $B/check9.sh $B/sol/$P.json 4 > $J/main_K3gB5n.out 2>&1
echo "main: $(grep -E '^RESULT' $J/main_K3gB5n.out | cut -c1-70)"
env $C TAG=${P}_tneg_zK3gB5n_gk9 nice -n 15 bash $B/check9.sh $B/sol/${P}_tneg.json 4 > $J/tneg_K3gB5n.out 2>&1
cat $B/logs/${P}_tneg_zK3gB5n_gk9/viol_d*.txt 2>/dev/null | grep -v '^#' | sort -u > $J/tneg_K3gB5n_receiver_violators.txt
echo "tneg: $(grep -E '^RESULT' $J/tneg_K3gB5n.out | cut -c1-70)"; echo GS21DONE
