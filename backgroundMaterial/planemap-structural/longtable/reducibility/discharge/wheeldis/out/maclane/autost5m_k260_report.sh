#!/bin/bash
# usage: autost_report.sh NN POINT : summarise ST-NN (main, tneg on K3l; main on K3l5) and commit out/job_STNN with md5 -r MD5SUMS
NN=$1; P=$2; W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd $W; J=out/job_ST$NN; L=/tmp/swarm-W17/logs
cat $L/${P}_tneg_zK3l5m_k260/viol_d*.txt 2>/dev/null | grep -v "^#" | sort -u > $J/tneg_receiver_violators.txt
for f in main tneg; do cp /tmp/swarm-W17/st${NN}_$f.out $J/; done
cp $L/${P}_zK3l5m_k260/summary.txt $J/summary_main.txt; cp $L/${P}_tneg_zK3l5m_k260/summary.txt $J/summary_tneg.txt; cp $L/${P}_tneg_zK3l5m_k260/p0.log $J/p0_tneg.log; 
cp out/maclane/autost5m_k260.sh $J/run_autost.sh
for f in main tneg; do echo "--$f"; grep -E "^RESULT|senderR2 rows|^  (five|nofive)|cons2 6-balance|patterns distinct|DP margin|Karp|exact violated [1-9]" /tmp/swarm-W17/st${NN}_$f.out | cut -c1-170; grep -o "nonzero amounts [0-9]* (sum [0-9.e-]*" /tmp/swarm-W17/st${NN}_$f.out | head -1; done
echo "--tneg receiver loads by d (count, load)"; awk '{print $1, $4}' $J/tneg_receiver_violators.txt | sort | uniq -c | sort -k2,2n -k3,3nr | awk '{print}' | head -12
echo "--top load rows per d"; for d in 7 8 9 10; do m=$(awk -v d=$d '$1==d{print $4}' $J/tneg_receiver_violators.txt | sort -nr | head -1); [ -n "$m" ] && awk -v d=$d -v m=$m '$1==d && $4==m' $J/tneg_receiver_violators.txt | head -8; done
cd $J; FL="run_autost.sh in/$P.json in/${P}_tneg.json st${NN}_main.out st${NN}_tneg.out summary_main.txt summary_tneg.txt p0_tneg.log tneg_receiver_violators.txt"
md5 -r $FL > MD5SUMS; echo "MD5SUMS md5 $(md5 -q MD5SUMS)"; cd $W
git add -f $(for f in $FL MD5SUMS; do echo $J/$f; done) && git commit -q -m "ST-$NN (auto, maclane point $P): W17 main + tneg on K3l5m + 260 keys

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && for i in 1 2 3 4 5; do git fetch -q origin main && git merge -q --no-edit origin/main && git push -q origin HEAD:main && { echo "commit $(git log -1 --format=%h --grep="ST-$NN (auto")"; break; }; sleep $((2**i)); done
