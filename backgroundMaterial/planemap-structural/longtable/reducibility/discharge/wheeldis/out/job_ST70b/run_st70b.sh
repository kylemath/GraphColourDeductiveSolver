#!/bin/bash
# ST-70b: main only, W17, sol_repS4MW_01__K3l5i (e88e0e16) on K3l5g (1bd9a34b, 18142/706/158) + 240 keys
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
P=sol_repS4MW_01__K3l5i; J=$W/out/job_ST70b; S=/tmp/swarm-W17/sol; mkdir -p $J/in
cp $HOME/maclane/maclane-k86/outbox/upper/$P.json $J/in/; cmp $J/in/$P.json $S/$P.json || exit 3
[ "$(md5 -q $J/in/$P.json | cut -c1-8)" = e88e0e16 ] || exit 4
A=/tmp/swarm-W17/args_A97F_W13K3l5g_x_studio.txt; [ "$(md5 -q $A | cut -c1-8)" = 1bd9a34b ] || exit 5
bash $W/out/job_ST67/ctl.sh 4
cd /tmp/swarm-W17
GK=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt F2BRULES=/tmp/swarm-W17/tab/rules_A5final_2db75746.json ARGSF=$A EXPECT_PAT=18142,706,158 TAG=${P}_zK3l5g_k240 bash /tmp/swarm-W17/check.sh $S/$P.json 8 > $J/st70b_main.out 2>&1
echo "check exit $?"
L=/tmp/swarm-W17/logs/${P}_zK3l5g_k240
cat $L/viol_d*.txt 2>/dev/null | grep -v "^#" | sort -u > $J/main_receiver_violators.txt
cp $L/summary.txt $J/summary_main.txt; cp $L/p0.log $J/p0_main.log; cp $0 $J/run_st70b.sh
grep -q ALLDONE $W/out/job_ST67/run.log || bash $W/out/job_ST67/ctl.sh 8
cd $J; FL="run_st70b.sh in/$P.json st70b_main.out summary_main.txt p0_main.log main_receiver_violators.txt"
md5 -r $FL > MD5SUMS; echo "MD5SUMS md5 $(md5 -q MD5SUMS)"
grep -E "^RESULT|senderR2 rows|^  (five|nofive)|cons2 6-balance|patterns distinct|DP margin|Karp|exact violated [1-9]" st70b_main.out | cut -c1-170; grep -o "nonzero amounts [0-9]* (sum [0-9.e-]*" st70b_main.out | head -1
awk '{print $1,$4}' main_receiver_violators.txt | sort | uniq -c; head -40 main_receiver_violators.txt
cd $W; git add -f $(for f in $FL MD5SUMS; do echo out/job_ST70b/$f; done) && git commit -q -m "ST-70b: sol_repS4MW_01__K3l5i main on K3l5g + 240 keys

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && for i in 1 2 3 4 5; do git fetch -q origin main && git merge -q --no-edit origin/main && git push -q origin HEAD:main && { git log -1 --format=%h --grep="ST-70b"; break; }; sleep $((2**i)); done
