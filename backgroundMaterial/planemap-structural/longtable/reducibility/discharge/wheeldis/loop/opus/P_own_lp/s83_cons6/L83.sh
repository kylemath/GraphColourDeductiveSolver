# usage: [STACK ARGS FAM KS EGK] bash L83.sh <tag> <warm csv> "<extra flags>"   nosep L + conssep, then zero wrong signs, exactbasis, recheck norepair (all with the same extra flags)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s83_cons6/env83.sh
TG=$1; WARM=$2; XF=$3; RD=$P/runL_$TG; WK=$SD/wr83_$TG; mkdir -p $RD $WK; cd $E83
echo "$(date -u +%H:%M:%SZ) [s83L-$TG] start STACK=$STACK ARGS=$(basename $ARGS) FAM=$FAM KS=$KS EGK=${EGK:+$(basename $EGK)} warm $(basename $WARM) flags: $XF" >> $P/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=$TG $A $CB warm=$WARM K=300 xcap=3 threads=1 work=$WK $XF > $RD/L.log 2>&1
cp sol_$TG.json cert_$TG.json $RD/ && rm -f sol_$TG.json cert_$TG.json rows_$TG.txt
python3 - $RD/cert_$TG.json $RD/cert_z.json "$XF" > $RD/zero.log 2>&1 <<'PY'
import json, sys
C = json.load(open(sys.argv[1])); n = 0; c6 = 'c6le' in sys.argv[3].split()
for c in C:
    w = float(c['w']); k = c['row'][0]
    if (k == 'senderR2' and w < 0) or ((k == 'receiverR2' or k.startswith('mrow') or (c6 and k == 'cons2')) and w > 0): c['w'] = 0.0; n += 1
json.dump(C, open(sys.argv[2], 'w'), indent=0); print('zeroed', n, 'wrong-sign of', len(C))
PY
nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$RD/cert_z.json xcap=3 $A work=$WK $XF exactbasis exbmu=0 exbtol=1e-10 > $RD/lower_exb.log 2>&1
[ -s $RD/cert_z_exb.json ] && nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$RD/cert_z_exb.json xcap=3 $A work=$WK $XF norepair > $RD/lower_recheck.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s83L-$TG] $(grep '^nosep' $RD/L.log | cut -c1-70) conssep rounds $(grep -c 'conssep it' $RD/L.log) ; exb: $(grep LOWER-R2 $RD/lower_exb.log | tail -1 | cut -c1-110) ; recheck: $(grep LOWER-R2 $RD/lower_recheck.log 2>/dev/null | tail -1 | cut -c1-120)" >> $P/run.log
rm -rf $WK; echo DONE > $RD/DONE
