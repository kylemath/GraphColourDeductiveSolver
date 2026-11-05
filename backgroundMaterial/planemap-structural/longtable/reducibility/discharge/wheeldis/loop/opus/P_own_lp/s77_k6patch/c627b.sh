# s77: c627.sh split into two parallel jobs after K b77K was stopped (coordinator 17:1xZ: its core goes to the 627-C lowers).  Same steps and flags as c627.sh.
# usage: nohup bash c627b.sh post <tag> <KT prefix> [pid to wait for] &   (post-process an L whose solveR2 already ran / is running)
#        nohup bash c627b.sh run  <tag> <KT prefix> &                     (full: L + post-processing)
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch
B=$(dirname $N); export ARGS=${ARGS:-$N/args/args_A97_plusStudioC_local.txt}; WARM=$(cat $N/runL_b77b/warmlist.txt)
MODE=$1; TAG=$2; export KT=$3; WPID=$4; . $N/env77.sh; RD=$N/runL_$TAG; mkdir -p $RD
log() { echo "$(date -u +%H:%M:%SZ) [s77C627] $*" >> $N/run.log; }
lowerchk() {  # <engdir> <cert> <log> [flags...]
  ED=$1; CE=$2; LG=$3; shift 3; WK=$S7/wr77c_$(basename $(dirname $LG))_$(basename $LG .log); mkdir -p $WK; cd $ED
  nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$CE xcap=3 $A work=$WK "$@" > $LG 2>&1; rm -rf $WK
  log "$TAG $(basename $LG): $(grep -o 'by kind {[^}]*}' $LG | head -1) | $(grep 'LOWER-R2' $LG | tail -1 | cut -c1-160)"; }
if [ "$MODE" = run ]; then WK=$S7/wr77L_$TAG; mkdir -p $WK; echo "$WARM" > $RD/warmlist.txt
  log "L $TAG start: FAM=base KT=$KT ARGS=$ARGS warm = runL_b77b/warmlist.txt, nosep lpmax=45, 1 thread"
  cd $N/eng; nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=$TAG $A $CB warm=$WARM K=300 xcap=3 threads=1 work=$WK lpmax=45 > $RD/L.log 2>&1; rm -rf $WK
elif [ -n "$WPID" ]; then while kill -0 $WPID 2>/dev/null; do sleep 30; done; rm -rf $S7/wr77L_$TAG; fi
cd $N/eng; cp sol_$TAG.json cert_$TAG.json $RD/ || { log "$TAG: no sol/cert from the L (see runL_$TAG/L.log)"; exit 1; }
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
else log "$TAG: exactbasis wrote no cert (see runL_$TAG/lower_exb.log)"; fi
echo DONE > $RD/DONE
