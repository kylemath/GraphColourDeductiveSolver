#!/bin/bash
# coordinator 12:59Z: when HCK5P17-P20 and HCK5P22 are GLUEDONE and the v smokes pass: upper lanes -> family v (= u + P22).
# 260-key lane -> k86MK14 (v, eng_p1r), 268-key lane -> k86MK15 (v, eng_p8). Sources: the newest finished move (u MK12/13, t MK10/11,
# s MK8/9), else MK6/MK7; a pending move that has not started moving is killed (skipped). Detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
O=$R/outbox/upper; S=$W/out/maclane/setup_k5v; MU=$W/out/maclane/setup_k5u/move_u.log; MS=$W/out/maclane/setup_k5s/move_s.log; MT=$W/out/maclane/setup_k5t/move_t.log; K260=cg_keys_r13w16_16fikp.txt; K268=cg_keys_r13w16_16fikp_p8bb.txt
log(){ echo "$(date -u +%H:%M:%SZ) $*"; }; abort(){ log "ABORT: $*"; echo MOVEABORT; exit 1; }
for j in HCK5P17 HCK5P18 HCK5P19 HCK5P20 HCK5P22; do until grep -q GLUEDONE $W/out/job_$j/lean/status.txt 2>/dev/null; do sleep 120; done; log "$j GLUEDONE"; done
until grep -q 'SMOKE-FAM v:' $S/smoke_fam_v.out 2>/dev/null; do sleep 60; done; grep -q 'SMOKE-FAM v: PASS' $S/smoke_fam_v.out || abort 'smoke_fam v not PASS'
[ "$(grep -c '^RESULT: FEASIBLE' $S/smoke_K3l5v_k240.out $S/smoke_K3gB5v_k240.out | awk -F: '{s+=$2} END{print s}')" = 2 ] || abort 'v harness smokes not both FEASIBLE'
grep -qE 'exact violated [1-9]' $S/smoke_K3l5v_k240.out $S/smoke_K3gB5v_k240.out && abort 'v harness smoke violators'
log "gate passed (5 GLUEDONE, smoke_fam v PASS, harness v 2/2 FEASIBLE)"
# which lanes are the sources
for L in $MU $MT $MS; do if grep -qE 'launch k86MK(8|10|12)' $L 2>/dev/null; then until grep -qE 'MOVEDONE|MOVEABORT' $L; do sleep 60; done; fi; done
if grep -q MOVEDONE $MU 2>/dev/null; then A=k86MK12; FA=K3l5u; B=k86MK13; FB=K3l5u; AA=autost_mk12nz; AB=autost_mk13
else
  pkill -f 'setup_k5u/move_u.sh' && log "move_u had not moved: killed (skip u)"
  if grep -q MOVEDONE $MT 2>/dev/null; then A=k86MK10; FA=K3l5t; B=k86MK11; FB=K3l5t; AA=autost_mk10nz; AB=autost_mk11
  else
    pkill -f 'setup_k5t/move_t.sh' && log "move_t had not moved: killed (skip t)"
    if grep -q MOVEDONE $MS 2>/dev/null; then A=k86MK8; FA=K3l5s; B=k86MK9; FB=K3l5s; AA=autost_mk8nz; AB=autost_mk9
    else pkill -f 'setup_k5s/move_s.sh' && log "move_s had not moved: killed (skip s)"; A=k86MK6; FA=K3l5r; B=k86MK7; FB=K3l5r; AA=autost_mk6nz; AB=autost_mk7; fi
  fi
fi
log "sources: $A ($FA) -> k86MK14, $B ($FB) -> k86MK15"
pick(){ fam=$1; keys=$2; eng=$3; for p in $(awk -v f=$fam '$4==f {print $2, $1}' $O/POINTS.txt | sort -g | head -3 | awk '{print $2}'); do
    log "recheck v ($keys ${eng:-eng_p1r}) on $p"; out=$(cd $R && env ${eng:+ENG=$eng} KEYS=$keys nice -n 10 bash recheck_fam.sh v $O/$p.json 2 2>&1 | tail -3); echo "$out" | sed 's/^/    /'
    echo "$out" | grep -q 'UPPER-R2: FEASIBLE' && { PICK=$p; return 0; }; done; return 1; }
while pgrep -f "$AA" > /dev/null; do sleep 60; done
pick ${FA}_k260 $K260 "" || abort "no $A point FEASIBLE on v + 260 keys"; P1=$PICK
log "stop $A"; (cd $R && bash stop_fam.sh $A 2>&1 | tail -3)
log "launch k86MK14 from $P1"; (cd $R && KEYS=$K260 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK14 PREV_TAG=$A FAM_SUFFIX=v LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P1.json > $S/launch_mk14.out 2>&1 < /dev/null); tail -2 $S/launch_mk14.out | cut -c1-200
while pgrep -f "$AB" > /dev/null; do sleep 60; done
pick ${FB}_k268 $K268 eng_p8 || abort "no $B point FEASIBLE on v + 268 keys"; P2=$PICK
log "stop $B"; (cd $R && bash stop_fam.sh $B 2>&1 | tail -3)
log "launch k86MK15 from $P2"; (cd $R && ENG=eng_p8 KEYS=$K268 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK15 PREV_TAG=$B FAM_SUFFIX=v LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P2.json > $S/launch_mk15.out 2>&1 < /dev/null); tail -2 $S/launch_mk15.out | cut -c1-200
(cd $R && bash status_fam.sh k86MK14 2>/dev/null | sed -n 3p; bash status_fam.sh k86MK15 2>/dev/null | sed -n 3p) | cut -c1-150
echo MOVEDONE
