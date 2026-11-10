#!/bin/bash
# coordinator 10:15Z: MK4 -> k86MK6 (r, 260 keys, eng_p1r), MK5 -> k86MK7 (r, eng_p8, 268 keys); each after its running checks (ST-106/107) finish. Detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
O=$R/outbox/upper; S=$W/out/maclane/setup_k5r; K260=cg_keys_r13w16_16fikp.txt; K268=cg_keys_r13w16_16fikp_p8bb.txt
log(){ echo "$(date -u +%H:%M:%SZ) $*"; }; abort(){ log "ABORT: $*"; echo MOVEABORT; exit 1; }
for j in HDK5P10 HDK5P15 HDK5P16; do grep -q GLUEDONE $W/out/job_$j/lean/status.txt || abort "$j not GLUEDONE"; done
grep -q 'SMOKE-FAM r: PASS' $S/smoke_fam_r.out || abort "smoke_fam r not PASS"
pick(){ fam=$1; keys=$2; eng=$3; for p in $(awk -v f=$fam '$4==f {print $2, $1}' $O/POINTS.txt | sort -g | head -3 | awk '{print $2}'); do
    log "recheck r ($keys ${eng:-eng_p1r}) on $p"; out=$(cd $R && env ${eng:+ENG=$eng} KEYS=$keys nice -n 10 bash recheck_fam.sh r $O/$p.json 2 2>&1 | tail -3); echo "$out" | sed 's/^/    /'
    echo "$out" | grep -q 'UPPER-R2: FEASIBLE' && { PICK=$p; return 0; }; done; return 1; }
# MK4 -> MK6 (wait for the ST-107 check of MK4's point)
while pgrep -f 'autost_mk4nz|autost5q_k260' > /dev/null; do sleep 60; done
pick K3l5q_k260 $K260 "" || abort "no MK4 point FEASIBLE on r + 260 keys"; P1=$PICK
log "stop k86MK4"; (cd $R && bash stop_fam.sh k86MK4 2>&1 | tail -3)
log "launch k86MK6 from $P1"; (cd $R && KEYS=$K260 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK6 PREV_TAG=k86MK4 FAM_SUFFIX=r LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P1.json > $S/launch_mk6.out 2>&1 < /dev/null); tail -2 $S/launch_mk6.out | cut -c1-200
# MK5 -> MK7 (wait for the ST-106 check of MK5's point)
while pgrep -f 'autost_mk5' > /dev/null; do sleep 60; done
pick K3l5q_k268 $K268 eng_p8 || abort "no MK5 point FEASIBLE on r + 268 keys"; P2=$PICK
log "stop k86MK5"; (cd $R && bash stop_fam.sh k86MK5 2>&1 | tail -3)
log "launch k86MK7 from $P2"; (cd $R && ENG=eng_p8 KEYS=$K268 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK7 PREV_TAG=k86MK5 FAM_SUFFIX=r LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P2.json > $S/launch_mk7.out 2>&1 < /dev/null); tail -2 $S/launch_mk7.out | cut -c1-200
(cd $R && bash status_fam.sh k86MK6 2>/dev/null | sed -n 3p; bash status_fam.sh k86MK7 2>/dev/null | sed -n 3p) | cut -c1-150
echo MOVEDONE
