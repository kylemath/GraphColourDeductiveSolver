# s77: lower bounds on the Studio 627-C stack (coordinator 16:3xZ): args = args_A97 + the 42 Studio cpat files (local copy args/studio_C627, md5-checked
# against from_opus/studio_C627/MD5SUMS), exname unchanged.  Same warm rows as L b77b (runL_b77b/warmlist.txt), base families, nosep L lpmax=45,
# then: wrong-sign float duals -> 0, lowerR2 exactbasis exbmu=0 exbtol=1e-10 (eng/, opt-in), recheck on the UNMODIFIED engine copy eng_orig/ with norepair.
# Order: (0) replay the two A97 exact certs on this stack, (1) unpatched (s64 kill6) tag b77U6, (2) patched-298 tag b77P6.   usage: nohup bash c627.sh [start step] &
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch
B=$(dirname $N); export ARGS=$N/args/args_A97_plusStudioC_local.txt; WARM=$(cat $N/runL_b77b/warmlist.txt); STEP=${1:-0}
log() { echo "$(date -u +%H:%M:%SZ) [s77C627] $*" >> $N/run.log; }
lowerchk() {  # <engdir> <cert> <log> [flags...]
  ED=$1; CE=$2; LG=$3; shift 3; WK=$S7/wr77c_$(basename $LG .log); mkdir -p $WK; cd $ED
  nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$CE xcap=3 $A work=$WK "$@" > $LG 2>&1; rm -rf $WK
  log "$(basename $LG): $(grep -o 'by kind {[^}]*}' $LG | head -1) | $(grep 'LOWER-R2' $LG | tail -1 | cut -c1-160)"; }
runone() {  # <tag> <KT prefix>
  TAG=$1; export KT=$2; . $N/env77.sh; RD=$N/runL_$TAG; WK=$S7/wr77L_$TAG; mkdir -p $RD $WK; echo "$WARM" > $RD/warmlist.txt
  log "L $TAG start: FAM=base KT=$KT ARGS=$ARGS (C627) warm = runL_b77b/warmlist.txt, nosep lpmax=45, 1 thread"
  cd $N/eng; nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=$TAG $A $CB warm=$WARM K=300 xcap=3 threads=1 work=$WK lpmax=45 > $RD/L.log 2>&1
  cp sol_$TAG.json cert_$TAG.json $RD/; rm -rf $WK
  log "L $TAG [M]: $(grep '^nosep' $RD/L.log | cut -c1-100) ; $(grep -o 'by kind {[^}]*}' $RD/L.log | head -1); cert md5 $(md5sum < $RD/cert_$TAG.json | cut -c1-32)"
  lowerchk $N/eng $RD/cert_$TAG.json $RD/lower.log
  python3 - $RD/cert_$TAG.json $RD/cert_${TAG}_z.json >> $RD/zero.log 2>&1 <<'EOF'
import json, sys
C = json.load(open(sys.argv[1])); n = 0
for c in C:
    w = float(c['w']); k = c['row'][0]
    if (k == 'senderR2' and w < 0) or ((k == 'receiverR2' or k.startswith('mrow')) and w > 0): c['w'] = 0.0; n += 1
json.dump(C, open(sys.argv[2], 'w'), indent=0); print('zeroed', n, 'wrong-sign of', len(C))
EOF
  lowerchk $N/eng $RD/cert_${TAG}_z.json $RD/lower_exb.log exactbasis exbmu=0 exbtol=1e-10
  if [ -s $RD/cert_${TAG}_z_exb.json ]; then cp $RD/cert_${TAG}_z_exb.json $RD/cert_${TAG}_exact.json
    lowerchk $N/eng_orig $RD/cert_${TAG}_exact.json $RD/lower_exact_origengine.log norepair
    log "*** $TAG exact cert runL_$TAG/cert_${TAG}_exact.json md5 $(md5sum < $RD/cert_${TAG}_exact.json | cut -c1-32) ***"
  else log "$TAG: exactbasis wrote no cert (see runL_$TAG/lower_exb.log)"; fi; }
. $N/env77.sh
if [ $STEP -le 0 ]; then log "step 0: replay of the A97 exact certs on the C627 stack (eng_orig, norepair)"
  export KT=$B/s64_keep95p131f/tab/kill/kill6; . $N/env77.sh; lowerchk $N/eng_orig $N/runL_b77b/cert_unpatched_exact.json $N/runL_b77b/lower_C627_unpatchedcert.log norepair
  export KT=$N/tab/kill/kill6; . $N/env77.sh; lowerchk $N/eng_orig $N/runL_b77b/cert_b77b_exact.json $N/runL_b77b/lower_C627_patchedcert.log norepair; fi
[ $STEP -le 1 ] && runone b77U6 $B/s64_keep95p131f/tab/kill/kill6
[ $STEP -le 2 ] && runone b77P6 $N/tab/kill/kill6
log "c627.sh done"; echo DONE > $N/c627.DONE
