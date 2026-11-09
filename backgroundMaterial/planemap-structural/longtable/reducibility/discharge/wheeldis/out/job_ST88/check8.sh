#!/bin/bash
# check8.sh (9 Nov 2026): check.sh with code_gk8 (payer-8/9 GK keys, PAYER8SPEC W5) and bin/sep3r_gk8; everything else identical.
# W17 macpack: one full second-engine upper check (code_gk7) of one point at NPROC processes, on the proof stack's family by default.
# usage: bash /tmp/swarm-W17/check.sh POINT [NPROC]
#   POINT = a path to the sol.json Opus names FEASIBLE on the corrected rules + W13 + 151 keys (copy it into sol/), or in10 / in11
#           (sol/sol_k86B_in1x.json: made on the unsound f7s family; in the pack for the smoke test and timing, not as targets)
#   NPROC = parallel separator processes (default 8, at most 16)
# The run is restartable: it always runs with RESUME=1, so after a crash or reboot rerun the same line; it keeps the Python step
# (same solution md5, code, args) and every finished separator part, and reruns only the rest. A fresh TAG starts from scratch.
# env:
#   STACK = W13 (default: W13 args bfca4bc4 + full q7 + c6le + GK 151 keys fe8a97a7 + F2B7, rule file
#           tab/rules_zcons_minus_W18rejects.json (2b362955, 6,016 rules: Studio zcons e6c496a1 minus W18's 274 strict rejects);
#           EXPECT_PAT 18128,686,158)
#         | A97F (the older stack without W13's 115 kill patterns, 140 keys: args_A97F_x_studio.txt, 18101,598,158; comparison only)
#   TAG (default <point>_zW13, or <point>_zA97F), DLIST (default 7..26, written out: macOS seq differs; e.g. DLIST=7,8 for the f2b7 degrees first: give it its
#   own TAG), PARTS, W17NICE (separator nice, default 20), GK / ARGSF / EXPECT_PAT / F2BRULES (override the stack's files;
#   tab/rules_zcons.json e6c496a1, tab/rules_studio_keep95p131f_f7s.json 704c371f and ext/k95f/tab 45a4c6d1: comparison only).
B=/tmp/swarm-W17; P=${1:?usage: bash check.sh POINT.json [NPROC]}; NP=${2:-8}
case $P in
  in10|in11) SOL=$B/sol/sol_k86B_$P.json; PT=$P;;
  *) SOL=$P; PT=$(basename "$P" .json);;
esac
[ -f "$SOL" ] || { echo "no solution file $SOL"; exit 2; }
case ${STACK:-W13} in
  W13)  D_GK=$B/tab/cg_keys_r13.txt; D_ARGS=$B/args_A97F_W13_x_studio.txt; D_PAT=18128,686,158; D_TAG=${PT}_zW13;;
  A97F) D_GK=$B/tab/cg_keys_r12.txt; D_ARGS=$B/args_A97F_x_studio.txt;     D_PAT=18101,598,158; D_TAG=${PT}_zA97F;;
  *) echo "STACK must be W13 or A97F"; exit 2;;
esac
TAG=${TAG:-$D_TAG}
export PATH=$B/macshim:$PATH W17NICE=${W17NICE:-20}
mkdir -p $B/logs
echo "check.sh: point $SOL ($(md5sum < "$SOL" | cut -c1-8)), stack ${STACK:-W13}, rules ${F2BRULES:-$B/tab/rules_zcons_minus_W18rejects.json}, tag $TAG, $NP processes (log: $B/logs/${TAG}_run.out; resumes if $B/logs/$TAG exists)"
cd $B && env RESUME=1 C6LE=1 NOCLAMP=1 F2B7=1 F2BRULES=${F2BRULES:-$B/tab/rules_zcons_minus_W18rejects.json} GK=${GK:-$D_GK} \
  ARGSF=${ARGSF:-$D_ARGS} EXPECT_PAT=${EXPECT_PAT:-$D_PAT} EXNAME=$B/tab/exname_keep95p131f.txt NPROC=$NP NPROCMAX=16 DMAXP=26 \
  DLIST=${DLIST:-7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26} PARTS=${PARTS:-7:4,8:12,9:24,10:9,11:6,12:3,13:2} \
  W17CODE=$B/code_gk8 SEPBIN=${SEPBIN:-sep3r_gk8} bash $B/code_gk8/w17_upper.sh "$SOL" $B/kill/patched298 $TAG 2>&1 | tee -a $B/logs/${TAG}_run.out
echo "summary: $B/logs/$TAG/summary.txt"
