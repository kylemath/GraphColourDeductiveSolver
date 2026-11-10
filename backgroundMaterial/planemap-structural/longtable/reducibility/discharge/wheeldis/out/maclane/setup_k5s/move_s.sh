#!/bin/bash
# coordinator 11:22Z: when HCK5P17 is GLUEDONE and the s smokes pass: MK6 -> k86MK8 (s, 260 keys, eng_p1r), MK7 -> k86MK9 (s, eng_p8, 268 keys). Detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
O=$R/outbox/upper; S=$W/out/maclane/setup_k5s; K260=cg_keys_r13w16_16fikp.txt; K268=cg_keys_r13w16_16fikp_p8bb.txt
log(){ echo "$(date -u +%H:%M:%SZ) $*"; }; abort(){ log "ABORT: $*"; echo MOVEABORT; exit 1; }
for j in HCK5P17; do until grep -q GLUEDONE $W/out/job_$j/lean/status.txt 2>/dev/null; do sleep 120; done; grep -q GLUEDONE $W/out/job_$j/lean/status.txt || abort "$j not GLUEDONE"; done
until grep -q 'SMOKE-FAM s:' $S/smoke_fam_s.out 2>/dev/null; do sleep 60; done; grep -q 'SMOKE-FAM s: PASS' $S/smoke_fam_s.out || abort 'smoke_fam s not PASS'; [ "$(grep -c '^RESULT: FEASIBLE' $S/smoke_K3l5s_k240.out $S/smoke_K3gB5s_k240.out | awk -F: '{s+=$2} END{print s}')" = 2 ] || abort 'harness smoke s'
pick(){ fam=$1; keys=$2; eng=$3; for p in $(awk -v f=$fam '$4==f {print $2, $1}' $O/POINTS.txt | sort -g | head -3 | awk '{print $2}'); do
    log "recheck s ($keys ${eng:-eng_p1r}) on $p"; out=$(cd $R && env ${eng:+ENG=$eng} KEYS=$keys nice -n 10 bash recheck_fam.sh s $O/$p.json 2 2>&1 | tail -3); echo "$out" | sed 's/^/    /'
    echo "$out" | grep -q 'UPPER-R2: FEASIBLE' && { PICK=$p; return 0; }; done; return 1; }
# MK4 -> MK6 (wait for the ST-107 check of MK4's point)
while pgrep -f 'autost_mk6nz' > /dev/null; do sleep 60; done
pick K3l5r_k260 $K260 "" || abort "no MK4 point FEASIBLE on r + 260 keys"; P1=$PICK
log "stop k86MK6"; (cd $R && bash stop_fam.sh k86MK6 2>&1 | tail -3)
log "launch k86MK8 from $P1"; (cd $R && KEYS=$K260 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK8 PREV_TAG=k86MK6 FAM_SUFFIX=s LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P1.json > $S/launch_mk8.out 2>&1 < /dev/null); tail -2 $S/launch_mk8.out | cut -c1-200
# MK5 -> MK7 (wait for the ST-106 check of MK5's point)
while pgrep -f 'autost_mk7' > /dev/null; do sleep 60; done
pick K3l5r_k268 $K268 eng_p8 || abort "no MK5 point FEASIBLE on r + 268 keys"; P2=$PICK
log "stop k86MK7"; (cd $R && bash stop_fam.sh k86MK7 2>&1 | tail -3)
log "launch k86MK9 from $P2"; (cd $R && ENG=eng_p8 KEYS=$K268 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK9 PREV_TAG=k86MK7 FAM_SUFFIX=s LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P2.json > $S/launch_mk9.out 2>&1 < /dev/null); tail -2 $S/launch_mk9.out | cut -c1-200
(cd $R && bash status_fam.sh k86MK8 2>/dev/null | sed -n 3p; bash status_fam.sh k86MK9 2>/dev/null | sed -n 3p) | cut -c1-150
echo MOVEDONE
