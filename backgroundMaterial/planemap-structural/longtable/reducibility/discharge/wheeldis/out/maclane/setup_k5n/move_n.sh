#!/bin/bash
# Coordinator 22:42Z: when HCK5P07 and HDK5P08 are GLUEDONE (sorryAx 0) and the K3l5n/K3gB5n harness smoke passes:
# move MK1 -> k86MK2 (family n, 260 keys) after any running MK1 check; then MS6 -> k86MS7 (family n, 240 keys). Run detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
O=$R/outbox/upper; S=$W/out/maclane/setup_k5n; K260=cg_keys_r13w16_16fikp.txt
log(){ echo "$(date -u +%H:%M:%SZ) $*"; }
abort(){ log "ABORT: $*"; echo MOVEABORT; exit 1; }
# 1. glue
for j in HCK5P07 HDK5P08; do until grep -q GLUEDONE $W/out/job_$j/lean/status.txt 2>/dev/null; do sleep 120; done; done
for j in HCK5P07 HDK5P08; do
  n=$(grep -l sorryAx $W/out/job_$j/lean/*.log 2>/dev/null | wc -l | tr -d ' '); [ "$n" = 0 ] || abort "$j sorryAx in $n logs"
  bad=$(grep -vE ' exit=0 .*sorry=0 error=0|ALLDONE|GLUEDONE| exit=143 ' $W/out/job_$j/lean/status.txt | head -3); [ -z "$bad" ] || abort "$j status: $bad"
done
log "glue: HCK5P07 and HDK5P08 GLUEDONE, sorryAx 0"
# 2. harness smoke
until grep -q SMOKEDONE $S/smoke_harness.log 2>/dev/null; do sleep 60; done
[ "$(grep -c '^RESULT: FEASIBLE' $S/smoke_K3l5n_k240.out $S/smoke_K3gB5n_k240.out | awk -F: '{s+=$2} END{print s}')" = 2 ] || abort "harness smoke not FEASIBLE on both"
grep -q 'D 18147 (spec 15,497), C 712' $S/smoke_K3l5n_k240.out || abort "K3l5n patterns"
grep -q 'D 18237 (spec 15,497), C 781' $S/smoke_K3gB5n_k240.out || abort "K3gB5n patterns"
log "harness smoke: K3l5n 18147/712/158 and K3gB5n 18237/781/158 FEASIBLE"
# pick: lowest filed point of a family that rechecks FEASIBLE on n with the given keys (at most 3 tries)
pick(){ fam=$1; keys=$2; for p in $(awk -v f=$fam '$4==f{print $2, $1}' $O/POINTS.txt | sort -g | head -3 | awk '{print $2}'); do
    log "recheck n ($keys) on $p"; out=$(cd $R && KEYS=$keys nice -n 10 bash recheck_fam.sh n $O/$p.json 2 2>&1 | tail -3); echo "$out" | sed 's/^/    /'
    echo "$out" | grep -q 'UPPER-R2: FEASIBLE' && { PICK=$p; return 0; }; done; return 1; }
# 3. MK1 -> MK2
while pgrep -f 'autost5j_k260|autost5n_k260' > /dev/null; do sleep 60; done
pick K3l5j_k260 $K260 || abort "no MK1 point FEASIBLE on n + 260 keys"; P1=$PICK
log "stop k86MK1"; (cd $R && bash stop_fam.sh k86MK1 2>&1 | tail -4)
log "launch k86MK2 from $P1"; (cd $R && KEYS=$K260 PARALLEL=1 UPPER_THREADS=2 TAG=k86MK2 PREV_TAG=k86MK1 FAM_SUFFIX=n LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P1.json > $S/launch_mk2.out 2>&1 < /dev/null); tail -3 $S/launch_mk2.out | cut -c1-200
# 4. MS6 -> MS7
while pgrep -f 'autost5j.sh|autost5j_report|autost5n.sh|autost5n_report' > /dev/null; do sleep 60; done
pick K3l5j cg_keys_r13w16_16fik.txt || abort "no MS6 point FEASIBLE on n + 240 keys"; P2=$PICK
log "stop k86MS6"; (cd $R && bash stop_fam.sh k86MS6 2>&1 | tail -4)
log "launch k86MS7 from $P2"; (cd $R && PARALLEL=1 UPPER_THREADS=2 TAG=k86MS7 PREV_TAG=k86MS6 FAM_SUFFIX=n LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $O/$P2.json > $S/launch_ms7.out 2>&1 < /dev/null); tail -3 $S/launch_ms7.out | cut -c1-200
(cd $R && bash status_fam.sh k86MK2 2>/dev/null | sed -n 3p; bash status_fam.sh k86MS7 2>/dev/null | sed -n 3p) | cut -c1-150
echo MOVEDONE
