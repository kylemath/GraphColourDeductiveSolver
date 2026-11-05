B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk; K=$B/s78_kstar
A97=$B/s33z/reg_A97/args_A97.txt; AF=$B/s79_routeF/args_A97_F.txt; EG=$K/eng/edgekeys_r4.txt
chk() { # engdir cert log STACK ARGS KS EGK [flags]
  local E=$1 CE=$2 LG=$3; shift 3; local ST=$1 AR=$2 KSv=$3 EGv=$4; shift 4
  ( export STACK=$ST ARGS=$AR FAM=full KS=$KSv; [ -n "$EGv" ] && export EGK=$EGv; . $K/env78.sh; WK=$SD/wr81x_$$; mkdir -p $WK; cd $E
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$CE xcap=3 $A work=$WK "$@" > $LG 2>&1; rm -rf $WK )
}
run() { # tag STACK ARGS KS EGK
  local T=$1 RD=$K/runL_$1 O=$R/exact_$1; mkdir -p $O
  python3 - $RD/cert_$T.json $O/cert_z.json > $O/zero.log 2>&1 <<'PY'
import json, sys
C = json.load(open(sys.argv[1])); n = 0
for c in C:
    w = float(c['w']); k = c['row'][0]
    if (k == 'senderR2' and w < 0) or ((k == 'receiverR2' or k.startswith('mrow')) and w > 0): c['w'] = 0.0; n += 1
json.dump(C, open(sys.argv[2], 'w'), indent=0); print('zeroed', n, 'wrong-sign of', len(C))
PY
  chk $R/eng_ks $O/cert_z.json $O/lower_exb.log $2 $3 $4 "$5" exactbasis exbmu=0 exbtol=1e-10
  if [ -s $O/cert_z_exb.json ]; then chk $K/eng $O/cert_z_exb.json $O/lower_recheck.log $2 $3 $4 "$5" norepair
    echo "$(date -u +%H:%M:%SZ) [s81x-$T] exb: $(grep LOWER-R2 $O/lower_exb.log | tail -1 | cut -c1-110) | recheck s78 eng norepair: $(grep LOWER-R2 $O/lower_recheck.log | tail -1 | cut -c1-140)" >> $R/run.log
  else echo "$(date -u +%H:%M:%SZ) [s81x-$T] exactbasis wrote no cert: $(tail -2 $O/lower_exb.log | tr '\n' ' ' | cut -c1-200)" >> $R/run.log; fi
}
run xPK_s77F_ksEG s77 $AF 1 $EG
echo "$(date -u +%H:%M:%SZ) [s81] EXACT2 DONE" >> $R/run.log
