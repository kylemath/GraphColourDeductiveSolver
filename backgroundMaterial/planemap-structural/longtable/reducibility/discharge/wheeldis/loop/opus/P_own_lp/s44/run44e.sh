# s44e: A83 (240b5a08) nosep lower with fb OFF, s42a family (l3q lqcap=3 + rpatN3, xcap=3), 128 exname hold-outs; warm from run44c's A83 rows.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
Q=$S/reg_A83; A="root=$M args=$Q/args_A83.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
WQ=$SE/rows_q66.txt,$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
T=q44nfA83L; RD=$D/run_A83nf; mkdir -p $RD; cd $E
WARM=$D/run_A83/rows_q44fbA83.txt,$D/run_A78/rows_q44fbA78.txt,$B/s42a/run_A78/rows_q42aA78.txt,$N3/rows_q39n3A74.txt,$WQ
dfok; note "A83 fb-off nosep start ($FQ $X; nice 5 threads 2)"
nice -n 5 python3 pcheck.py solveR2 $FQ $X nosep tag=$T $A $CB warm=$WARM K=300 xcap=3 threads=2 work=$SC/P/wr44e > $RD/L.log 2>&1
cp sol_$T.json cert_$T.json $RD/; python3 $H/binder_keys.py $RD/cert_$T.json "Opus s44/run_A83nf/cert_$T.json (A83 240b5a08, l3q + rpatN3, fb off, 128 exname hold-outs)" > $RD/binders_canon.txt
note "A83 fb-off nosep: $(grep 'LP t\*' $RD/L.log | tail -1 | cut -c1-80)"
nice -n 5 python3 pcheck.py lowerR2 $FQ $X cert=$RD/cert_$T.json xcap=3 $A work=$SC/P/wr44e > $RD/lower.log 2>&1
md5sum $RD/*.json > $RD/md5.txt; date -u > $RD/ALL.done
note "A83 fb-off lower: $(grep 'LOWER-R2' $RD/lower.log | tail -1 | cut -c1-120)"
