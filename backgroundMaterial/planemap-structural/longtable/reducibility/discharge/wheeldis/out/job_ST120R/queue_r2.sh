#!/bin/zsh
# ST-120 R queue v2: build once, then two workers claiming modules by lock dir (largest ring, W2p first).
# Worker 1 starts at once (with HCK5P22 still running this keeps 3 Lean jobs); worker 2 starts when HCK5P22 is ALLDONE.
O=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
cd $O/..; grep -q RSCHKDONE $O/job_ST120R/chk.log || exit 1
python3 out/job_ST120R/build_r.py || { echo BUILDFAIL; exit 1; }
(cd $O/job_HDRS403/lean && ./run.sh HDRS403); (cd $O/job_HCRS403/lean && ./run.sh CKRS403)
tail -1 $O/job_HCRS403/lean/status.txt | grep -q "^CKRS403 exit=0" || { echo "CKRS403 FAILED"; exit 1; }
L=$O/job_ST120R/locks; mkdir -p $L
worker(){ while read j m r; do mkdir $L/$m 2>/dev/null || continue; (cd $O/$j/lean && ./run.sh $m); done < $O/job_ST120R/queue_order.txt; }
worker & W1=$!
( until grep -q ALLDONE $O/job_HCK5P22/lean/status.txt 2>/dev/null; do sleep 120; done; echo "worker 2 start $(date -u +%H:%MZ)"; worker ) & W2=$!
wait $W1 $W2
(cd $O/job_HDRS403/lean && ./run.sh HDRS403All; echo ALLDONE >> status.txt)
(cd $O/job_HCRS403/lean && ./run.sh RS403VAll; echo ALLDONE >> status.txt)
echo "QDONE $(date -u +%H:%MZ)"
