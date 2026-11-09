#!/bin/bash
# usage: [SRC=json] autost5i.sh NN POINTNAME   (K3l5n variant: main + tneg on K3l5e + 240 keys, main on K3l)   (standing rule from coordinator 12:07Z): W17 check of a maclane upper point.
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
[ -f $W/out/job_ST67/run.log ] && ! grep -q ALLDONE $W/out/job_ST67/run.log && bash $W/out/job_ST67/ctl.sh 4
cd /tmp/swarm-W17
R=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt; F=/tmp/swarm-W17/tab/rules_A5final_2db75746.json
AL=/tmp/swarm-W17/args_A97F_W13K3l_x_studio.txt; A5=/tmp/swarm-W17/args_A97F_W13K3l5_x_studio.txt
G=/tmp/swarm-W17/tab/cg_keys_r13w16.txt; G240=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt
A5E=/tmp/swarm-W17/args_A97F_W13K3l5n_x_studio.txt
GK=$G240 RPATN=$R F2BRULES=$F ARGSF=$A5E EXPECT_PAT=18147,712,158 TAG=${P}_zK3l5n_k240 bash /tmp/swarm-W17/check.sh $S/$P.json 8 > /tmp/swarm-W17/st${NN}_main.out 2>&1
GK=$G240 RPATN=$R F2BRULES=$F ARGSF=$A5E EXPECT_PAT=18147,712,158 TAG=${P}_tneg_zK3l5n_k240 bash /tmp/swarm-W17/check.sh $S/${P}_tneg.json 8 > /tmp/swarm-W17/st${NN}_tneg.out 2>&1
# (K3l main dropped from 15:21Z, coordinator: MS2 points depend on K3l5e kills + 240 keys)
echo DONE > /tmp/swarm-W17/st$NN.done
[ -f $W/out/job_ST67/run.log ] && ! grep -q ALLDONE $W/out/job_ST67/run.log && bash $W/out/job_ST67/ctl.sh 8
