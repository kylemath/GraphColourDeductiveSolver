#!/bin/bash
# usage: [SRC=json] autost5e.sh NN POINTNAME   (K3l5e variant: main + tneg on K3l5e + 240 keys, main on K3l)   (standing rule from coordinator 12:07Z): W17 check of a maclane upper point.
# copies outbox/upper/<POINT>.json to out/job_STNN/in and /tmp/swarm-W17/sol, makes the tneg (t - 5e-6, regex on the leading "t"),
# pauses ST-42, runs main + tneg on K3l and main on K3l5 + 240 keys, restarts ST-42 at 2 procs, writes /tmp/swarm-W17/stNN.done
NN=$1; P=$2; W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
J=$W/out/job_ST$NN; mkdir -p $J/in; S=/tmp/swarm-W17/sol
SRC=${SRC:-$HOME/maclane/maclane-k86/outbox/upper/$P.json}; cp $SRC $J/in/$P.json; cp $J/in/$P.json $S/
python3 -I - "$S/$P.json" "$S/${P}_tneg.json" <<'PY'
import re, sys
s = open(sys.argv[1]).read(); m = re.match(r'\{"t": ([0-9.eE+-]+)', s); t = float(m.group(1))
open(sys.argv[2], 'w').write('{"t": ' + repr(t - 5e-6) + s[m.end():]); print('t', t, 'tneg', t - 5e-6)
PY
cp $S/${P}_tneg.json $J/in/
pkill -f runk5.sh; pkill -f "mscreen.py famK5_r1516_0"; pkill -f "mscreen.py famK5_r1516_1"; sleep 2
for p in $(ps -Ao pid,ppid,command | awk '$2==1' | grep -E "loop/kc/kc|out/job52/dfast18|studio15/cfast" | grep -v -E "job_K5/chk|job_K3CHK|job_ST49/chk" | awk '{print $1}'); do kill $p; done
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json
AL=/tmp/swarm-W17/args_A97F_W13K3l_x_studio.txt; A5=/tmp/swarm-W17/args_A97F_W13K3l5_x_studio.txt
G=/tmp/swarm-W17/tab/cg_keys_r13w16.txt; G240=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt
A5E=/tmp/swarm-W17/args_A97F_W13K3l5e_x_studio.txt
GK=$G240 RPATN=$R F2BRULES=$F ARGSF=$A5E EXPECT_PAT=18142,704,158 TAG=${P}_zK3l5e_k240 bash /tmp/swarm-W17/check.sh $S/$P.json 8 > /tmp/swarm-W17/st${NN}_main.out 2>&1
GK=$G240 RPATN=$R F2BRULES=$F ARGSF=$A5E EXPECT_PAT=18142,704,158 TAG=${P}_tneg_zK3l5e_k240 bash /tmp/swarm-W17/check.sh $S/${P}_tneg.json 8 > /tmp/swarm-W17/st${NN}_tneg.out 2>&1
GK=$G RPATN=$R F2BRULES=$F ARGSF=$AL EXPECT_PAT=18136,694,158 TAG=${P}_zK3l_w16 bash /tmp/swarm-W17/check.sh $S/$P.json 8 > /tmp/swarm-W17/st${NN}_K3l.out 2>&1
echo DONE > /tmp/swarm-W17/st$NN.done
cd $W/out/job_K5; mv run.log run_pre_st$NN.log; SKIP=$PWD/skip_K5.txt KC=$W/loop/kc/kc DF18=$W/out/job52/dfast18 CF=$W/../studio15/cfast nohup bash runk5.sh 2 > run.log 2>&1 &
