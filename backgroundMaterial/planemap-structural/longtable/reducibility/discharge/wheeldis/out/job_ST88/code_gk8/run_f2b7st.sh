#!/bin/bash
# W17 round 5: one Python-step run of code_gk7 on a solution (no separator search jobs), for the f2b7 tests.
# usage: SOL=... TAG=... [GKF=keys] [ARGSF=... EXPECT_PAT=...] [env for the tests] bash run_f2b7st.sh  (log to stdout)
# round 6 (macpack): ARGSF / EXPECT_PAT may be set by the caller (default: the A97F studio args, 18101,598,158)
B=/tmp/swarm-W17
: ${SOL:?SOL=} ${TAG:?TAG=}
T=$(python3 -I -c "import json,sys; print(repr(json.load(open(sys.argv[1]))['t']))" $SOL)
env C6LE=1 NOCLAMP=1 GK=${GKF:-$B/tab/A97F_111keys.txt} ARGSF=${ARGSF:-$B/args_A97F_x_studio.txt} EXPECT_PAT=${EXPECT_PAT:-18101,598,158} EXNAME=$B/tab/exname_keep95p131f.txt \
  DMAXP=26 KILLDIR=$B/kill/patched298 EXPECT_T=$T W17CODE=$B/code_gk7 bash $B/code_gk7/run17.sh
