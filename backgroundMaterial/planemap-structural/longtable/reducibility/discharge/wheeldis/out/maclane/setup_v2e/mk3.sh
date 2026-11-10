#!/bin/bash
# coordinator 07:45Z: SMOKE-V2E PASS -> stop k86MS7; MK2's best K3l5n_k260 point; recheck on n + 268 keys (eng_p8); launch k86MK3 (family n). Detached.
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
S=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/maclane/setup_v2e
K=cg_keys_r13w16_16fikp_p8bb.txt; log(){ echo "$(date -u +%H:%M:%SZ) $*"; }
log "stop k86MS7"; (cd $R && bash stop_fam.sh k86MS7 2>&1 | tail -4)
for p in $(awk '$4=="K3l5n_k260" && $1 ~ /(k86MK2_in|repK2MW_)/ {print $2, $1}' $R/outbox/upper/POINTS.txt | sort -g | head -3 | awk '{print $2}'); do
  log "recheck n (268 keys, eng_p8) on $p"; out=$(cd $R && ENG=eng_p8 KEYS=$K nice -n 10 bash recheck_fam.sh n $R/outbox/upper/$p.json 2 2>&1 | tail -3); echo "$out" | sed 's/^/    /'
  echo "$out" | grep -q 'UPPER-R2: FEASIBLE' && { P=$p; break; }
done
[ -n "$P" ] || { log "ABORT: no MK2 point FEASIBLE on n + 268 keys"; echo MK3ABORT; exit 1; }
log "launch k86MK3 from $P"; (cd $R && ENG=eng_p8 KEYS=$K PARALLEL=1 TAG=k86MK3 PREV_TAG=k86MK2 FAM_SUFFIX=n LP_ON_CHECK=1 nohup bash $N/launch_msfam.sh $R/outbox/upper/$P.json > $S/launch_mk3.out 2>&1 < /dev/null); tail -3 $S/launch_mk3.out | cut -c1-200
(cd $R && bash status_fam.sh k86MK3 2>/dev/null | sed -n 3p; bash status_fam.sh k86MK2 2>/dev/null | sed -n 3p) | cut -c1-150
echo MK3DONE
