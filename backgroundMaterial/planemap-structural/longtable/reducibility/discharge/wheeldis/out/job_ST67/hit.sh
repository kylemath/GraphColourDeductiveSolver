#!/bin/zsh
# ST-67 (Studio): hit.sh NN ID : second check; on PASS create + start the Lean job, mark rows dead, update skip, restart the screen (8 procs unless an ST check runs), commit
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; cd $W
NN=$1; ID=$2; J=out/job_ST67; C=$J/chk/h$NN
nice -n 10 python3 $J/k67chk.py $NN $ID 2>&1 | tail -9 | cut -c1-320
grep -q PASS $C/verdict.txt || { echo "VERDICT FAIL"; exit 1; }
python3 $J/after_hit.py $NN
JOB=$(ls -d out/job_H?K5P$NN | sed 's#out/job_##'); H=out/job_$JOB
nohup $H/drive.sh > $H/drive.log 2>&1 &
NP=8; pgrep -f "check.sh /tmp/swarm-W17/sol" > /dev/null && NP=4
bash $J/ctl.sh $NP; sleep 3; (cd $J; python3 status.py | tail -9)
L=($J/killed_rows.txt $J/skip_b2140.txt $J/hit.sh $J/results/res_K5_*.tsv(N) $C/report.md $C/verdict.txt $C/cfg.in $C/cfg.out $C/occ.txt $C/cfg.x(N) $C/extraC.tsv(N) $C/lean/CK5P*.lean(N) $C/lean/CK5P*.log(N) $C/lean/status.txt(N) $H/drive.sh $H/lean/run.sh $H/*.tsv(N) $H/lean/*.lean(N))
git add -f $L && git commit -q -m "ST-67: hit p$NN second check PASS; Lean $JOB started; rows dead, skip updated

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && for i in 1 2 3 4 5; do git fetch -q origin main && git merge -q --no-edit origin/main && git push -q origin HEAD:main && { echo "commit $(git log -1 --format=%h --grep="hit p$NN second")"; break; }; sleep $((2**i)); done
