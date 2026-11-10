#!/bin/bash
# coordinator 11:46Z: when HCK5P17, HCK5P18 and HCK5P19 are GLUEDONE and the t smokes pass: upper lanes -> family t.
# 260-key lane -> k86MK10 (t, eng_p1r), 268-key lane -> k86MK11 (t, eng_p8). Source lanes: MK8/MK9 if move_s finished (MOVEDONE),
# else MK6/MK7 (move_s skipped: killed if it has not started moving). Detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
O=$R/outbox/upper; S=$W/out/maclane/setup_k5t; MS=$W/out/maclane/setup_k5s/move_s.log; K260=cg_keys_r13w16_16fikp.txt; K268=cg_keys_r13w16_16fikp_p8bb.txt
log(){ echo "$(date -u +%H:%M:%SZ) $*"; }; abort(){ log "ABORT: $*"; echo MOVEABORT; exit 1; }
for j in HCK5P17 HCK5P18 HCK5P19; do until grep -q GLUEDONE $W/out/job_$j/lean/status.txt 2>/dev/null; do sleep 120; done; log "$j GLUEDONE"; done
until grep -q 'SMOKE-FAM t:' $S/smoke_fam_t.out 2>/dev/null; do sleep 60; done; grep -q 'SMOKE-FAM t: PASS' $S/smoke_fam_t.out || abort 'smoke_fam t not PASS'
[ "$(grep -c '^RESULT: FEASIBLE' $S/smoke_K3l5t_k240.out $S/smoke_K3gB5t_k240.out | awk -F: '{s+=$2} END{print s}')" = 2 ] || abort 't harness smokes not both FEASIBLE'
grep -qE 'exact violated [1-9]' $S/smoke_K3l5t_k240.out $S/smoke_K3gB5t_k240.out && abort 't harness smoke violators'
log "gate passed (3 GLUEDONE, smoke_fam t PASS, harness t 2/2 FEASIBLE)"
# which lanes are the sources
if grep -q 'launch k86MK8' $MS 2>/dev/null; then until grep -qE 'MOVEDONE|MOVEABORT' $MS; do sleep 60; done; fi
if grep -q MOVEDONE $MS 2>/dev/null; then A=k86MK8; FA=K3l5s; B=k86MK9; FB=K3l5s; AA=autost_mk8nz; AB=autost_mk9
else
  pkill -f 'setup_k5s/move_s.sh' && log "move_s had not moved: killed (skip s)"; A=k86MK6; FA=K3l5r; B=k86MK7; FB=K3l5r; AA=autost_mk6nz; AB=autost_mk7
fi
log "sources: $A ($FA) -> k86MK10, $B ($FB) -> k86MK11"
pick(){ fam=$1; keys=$2; eng=$3; for p in $(awk -v f=$fam '$4==f {print $2, $1}' $O/POINTS.txt | sort -g | head -3 | awk '{print $2}'); do
    log "recheck t ($keys ${eng:-eng_p1r}) on $p"; out=$(cd $R && env ${eng:+ENG=$eng} KEYS=$keys nice -n 10 bash recheck_fam.sh t $O/$p.json 2 2>&1 | tail -3); echo "$out" | sed 's/^/    /'
    echo "$out" | grep -q 'UPPER-R2: FEASIBLE' && { PICK=$p; return 0; }; done; return 1; }
while pgrep -f "$AA" > /dev/null; do sleep 60; done
pick ${FA}_k260 $K260 "" || abort "no $A point FEASIBLE on t + 260 keys"; P1=$PICK
log "stop $A"; (cd $R && bash stop_fam.sh $A 2>&1 | tail -3)
log "launch k86MK10 from $P1"; (cd $R && KEYS=$K260 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK10 PREV_TAG=$A FAM_SUFFIX=t LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P1.json > $S/launch_mk10.out 2>&1 < /dev/null); tail -2 $S/launch_mk10.out | cut -c1-200
while pgrep -f "$AB" > /dev/null; do sleep 60; done
pick ${FB}_k268 $K268 eng_p8 || abort "no $B point FEASIBLE on t + 268 keys"; P2=$PICK
log "stop $B"; (cd $R && bash stop_fam.sh $B 2>&1 | tail -3)
log "launch k86MK11 from $P2"; (cd $R && ENG=eng_p8 KEYS=$K268 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK11 PREV_TAG=$B FAM_SUFFIX=t LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P2.json > $S/launch_mk11.out 2>&1 < /dev/null); tail -2 $S/launch_mk11.out | cut -c1-200
(cd $R && bash status_fam.sh k86MK10 2>/dev/null | sed -n 3p; bash status_fam.sh k86MK11 2>/dev/null | sed -n 3p) | cut -c1-150
echo MOVEDONE
