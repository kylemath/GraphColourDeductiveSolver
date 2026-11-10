#!/bin/bash
# coordinator 08:54Z: when HDK5P10 is GLUEDONE (sorryAx 0) and the fam-q smokes passed: MK2 -> k86MK4 (q, 260 keys), MK3 -> k86MK5 (q, eng_p8, 268 keys). Detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
O=$R/outbox/upper; S=$W/out/maclane/setup_k5q; K260=cg_keys_r13w16_16fikp.txt; K268=cg_keys_r13w16_16fikp_p8bb.txt
log(){ echo "$(date -u +%H:%M:%SZ) $*"; }; abort(){ log "ABORT: $*"; echo MOVEABORT; exit 1; }
J=$W/out/job_HDK5P10; until grep -q GLUEDONE $J/lean/status.txt 2>/dev/null; do sleep 120; done
n=$(grep -l sorryAx $J/lean/*.log 2>/dev/null | wc -l | tr -d ' '); [ "$n" = 0 ] || abort "HDK5P10 sorryAx in $n logs"
bad=$(grep -vE ' exit=0 .*sorry=0 error=0|ALLDONE|GLUEDONE| exit=143 ' $J/lean/status.txt | head -3); [ -z "$bad" ] || abort "HDK5P10 status: $bad"
log "glue: HDK5P10 GLUEDONE, sorryAx 0"
until grep -q 'SMOKE-FAM q:' $S/smoke_fam_q.out 2>/dev/null; do sleep 60; done
[ "$(grep -c '^RESULT: FEASIBLE' $S/smoke_K3l5q_k240.out $S/smoke_K3gB5q_k240.out | awk -F: '{s+=$2} END{print s}')" = 2 ] || abort "q harness smoke not FEASIBLE on both"
grep -q 'D 18152 (spec 15,497), C 712' $S/smoke_K3l5q_k240.out || abort "K3l5q patterns"; grep -q 'D 18242 (spec 15,497), C 781' $S/smoke_K3gB5q_k240.out || abort "K3gB5q patterns"
grep -q 'SMOKE-FAM q: PASS' $S/smoke_fam_q.out || abort "smoke_fam q not PASS"
log "q smokes: harness 18152/712/158 and 18242/781/158 FEASIBLE; smoke_fam q PASS"
pick(){ fam=$1; re=$2; keys=$3; eng=$4; for p in $(awk -v f=$fam -v r="$re" '$4==f && $1 ~ r {print $2, $1}' $O/POINTS.txt | sort -g | head -3 | awk '{print $2}'); do
    log "recheck q ($keys ${eng:-eng_p1r}) on $p"; out=$(cd $R && env ${eng:+ENG=$eng} KEYS=$keys nice -n 10 bash recheck_fam.sh q $O/$p.json 2 2>&1 | tail -3); echo "$out" | sed 's/^/    /'
    echo "$out" | grep -q 'UPPER-R2: FEASIBLE' && { PICK=$p; return 0; }; done; return 1; }
# MK2 -> MK4
while pgrep -f 'autost5n_k260|autost5q_k260' > /dev/null; do sleep 60; done
pick K3l5n_k260 '(k86MK2_in|repK2MW_)' $K260 "" || abort "no MK2 point FEASIBLE on q + 260 keys"; P1=$PICK
log "stop k86MK2"; (cd $R && bash stop_fam.sh k86MK2 2>&1 | tail -3)
log "launch k86MK4 from $P1"; (cd $R && KEYS=$K260 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK4 PREV_TAG=k86MK2 FAM_SUFFIX=q LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P1.json > $S/launch_mk4.out 2>&1 < /dev/null); tail -2 $S/launch_mk4.out | cut -c1-200
# MK3 -> MK5
while pgrep -f 'autost_mk3|autost_mk5' > /dev/null; do sleep 60; done
pick K3l5n_k268 '.' $K268 eng_p8 || abort "no MK3 point FEASIBLE on q + 268 keys"; P2=$PICK
log "stop k86MK3"; (cd $R && bash stop_fam.sh k86MK3 2>&1 | tail -3)
log "launch k86MK5 from $P2"; (cd $R && ENG=eng_p8 KEYS=$K268 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK5 PREV_TAG=k86MK3 FAM_SUFFIX=q LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P2.json > $S/launch_mk5.out 2>&1 < /dev/null); tail -2 $S/launch_mk5.out | cut -c1-200
(cd $R && bash status_fam.sh k86MK4 2>/dev/null | sed -n 3p; bash status_fam.sh k86MK5 2>/dev/null | sed -n 3p) | cut -c1-150
echo MOVEDONE
