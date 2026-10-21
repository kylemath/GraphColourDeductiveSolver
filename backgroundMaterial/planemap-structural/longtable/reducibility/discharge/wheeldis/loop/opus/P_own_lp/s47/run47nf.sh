# s47nf: A84 (517b0129) nosep lower with fb OFF: l3q + l3qV=7,8 + rpatN3 (lqcap 3, xcap 3), 128 exname; warm from run44d's A84 rows.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
E=$B/s47/eng; RD=$B/s47/run_A84nf; TV=$B/s47/tabV8_A84; mkdir -p $RD
Q=$S/reg_A84; A="root=$M args=$Q/args_A84.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$TV/tabV8_1.json,$TV/tabV8_-1.json"
WQ=$SE/rows_q66.txt,$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
T=q47nfA84L; cd $E
WARM=$B/s47/run_A84/rows_q47A84.txt,$D/run_A83/rows_q44fbA83.txt,$B/s42a/run_A78/rows_q42aA78.txt,$WQ
note() { echo "$(date -u +%H:%M:%SZ) [s47nf] $*" >> $B/s47/run.log; }
note "A84 fb-off nosep start ($FQ $X; nice 10 threads 1)"
nice -n 10 python3 pcheck.py solveR2 $FQ $X nosep tag=$T $A $CB warm=$WARM K=300 xcap=3 threads=1 work=$SC/P/wr47nf > $RD/L.log 2>&1
cp sol_$T.json cert_$T.json $RD/; python3 $H/binder_keys.py $RD/cert_$T.json "Opus s47/run_A84nf/cert_$T.json (A84 517b0129, l3q + l3qV=7,8 + rpatN3, fb off, 128 exname)" > $RD/binders_canon.txt
note "A84 fb-off nosep: $(grep 'LP t\*' $RD/L.log | tail -1 | cut -c1-80)"
nice -n 10 python3 pcheck.py lowerR2 $FQ $X cert=$RD/cert_$T.json xcap=3 $A work=$SC/P/wr47nf > $RD/lower.log 2>&1
md5sum $RD/*.json > $RD/md5.txt; date -u > $RD/ALL.done
note "A84 fb-off lower: $(grep 'LOWER-R2' $RD/lower.log | tail -1 | cut -c1-120)"
