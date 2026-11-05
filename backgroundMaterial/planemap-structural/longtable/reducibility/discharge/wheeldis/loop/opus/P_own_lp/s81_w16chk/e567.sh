B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk; N=$B/s80_k6A
one() { # tag F2BXfile
  local TG=$1 OD=$R/e567_$1; mkdir -p $OD
  ( export FAM=full; [ -n "$2" ] && export F2BX=$2; . $N/env80.sh; WK=$S8/wr81e_$TG; mkdir -p $WK; cd $ENG
    nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=e$TG $A $CB warm=$R/rows_x567_recv.txt K=300 xcap=3 threads=1 work=$WK > $OD/L.log 2>&1
    mv sol_e$TG.json cert_e$TG.json $OD/; rm -f rows_e$TG.txt
    python3 - $OD/cert_e$TG.json $OD/cert_z.json > $OD/zero.log 2>&1 <<'PY'
import json, sys
C = json.load(open(sys.argv[1])); n = 0
for c in C:
    w = float(c['w']); k = c['row'][0]
    if (k == 'senderR2' and w < 0) or ((k == 'receiverR2' or k.startswith('mrow')) and w > 0): c['w'] = 0.0; n += 1
json.dump(C, open(sys.argv[2], 'w'), indent=0); print('zeroed', n, 'wrong-sign of', len(C))
PY
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$OD/cert_z.json xcap=3 $A work=$WK exactbasis exbmu=0 exbtol=1e-10 > $OD/lower_exb.log 2>&1
    [ -s $OD/cert_z_exb.json ] && nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$OD/cert_z_exb.json xcap=3 $A work=$WK norepair > $OD/lower_recheck.log 2>&1
    rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s81e-$TG] s80 eng FAM=full patched298+F F2BX=$(basename ${2:-none}): $(grep '^nosep' $OD/L.log | cut -c1-80) | $(grep LOWER-R2 $OD/lower_recheck.log 2>/dev/null | tail -1 | cut -c1-140)" >> $R/run.log )
}
one ctl ""
one ApLp $N/rules/rules_ApLp.json
echo "$(date -u +%H:%M:%SZ) [s81] E567 DONE" >> $R/run.log
