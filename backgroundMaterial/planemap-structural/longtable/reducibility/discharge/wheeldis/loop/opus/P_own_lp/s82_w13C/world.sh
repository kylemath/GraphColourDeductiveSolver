B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s82_w13C; K=$B/s78_kstar; S81=$B/s81_w16chk
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
while kill -0 585 2>/dev/null; do sleep 30; done
echo "$(date -u +%H:%M:%SZ) [s82] world F: $(cat $R/gen_F.log | tr '\n' ' ') rows $(wc -l < $R/rows567_F.txt)" >> $R/run.log
cd $K/eng && python3 $R/filtC3.py $PWD $R/rows567_F.txt $R/rows567_FC3.txt root=$M args=$R/args_C3only.txt >> $R/run.log 2>&1
AF=$B/s79_routeF/args_A97_F.txt; AC=$R/args_A97_F_C3.txt; EG=$K/eng/edgekeys_r4.txt
cd $K && STACK=s77 ARGS=$AF FAM=full KS=1 EGK=$EG NOLOWER=1 bash runL78.sh w567full_F_ksEG $R/rows567_F.txt 1
cd $K && STACK=s77 ARGS=$AC FAM=full KS=1 EGK=$EG NOLOWER=1 bash runL78.sh w567full_FC3_ksEG $R/rows567_FC3.txt 1
echo "$(date -u +%H:%M:%SZ) [s82] L done: $(grep 's78L-w567full' $K/run.log | grep nosep | cut -c1-200 | tr '\n' ' ')" >> $R/run.log
# exact: reuse s81 exact.sh run() via a small driver
sed -n '1,/^run w567_s75_full/p' $S81/exact.sh | grep -v "^run w567" > $R/exactw.sh
echo 'run w567full_F_ksEG s77 $AF 1 $EG' >> $R/exactw.sh
echo "AF=$AC; run w567full_FC3_ksEG s77 \$AF 1 \$EG" >> $R/exactw.sh
bash $R/exactw.sh
echo "$(date -u +%H:%M:%SZ) [s82] WORLD DONE" >> $R/run.log
