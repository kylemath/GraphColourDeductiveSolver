#!/bin/bash
# s86 launch21.sh (10 Nov 06:50Z): GS20 already stopped by swap21.sh at iter 2, but its HATBB f2bself tests were OOM-killed beside GS20,
# so swap21 fell back to k86GS21x (stopped).  This waits for the rerun tests, then for our upperR2 verdict on GS20 in03 (0.014094436):
# FEASIBLE -> GS21 starts there, else from MK1 in23 (0.014164305, ST-96 [E2]).  Rest as swap21.sh.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
L=$N/run.log
until [ -s $N/hatbb/tests_f2b.out ]; do sleep 30; done
OK=0; grep -q "^hbf2bself: .*F2B-SELFTEST: PASS" $N/hatbb/tests_f2b.out && grep -q "^hbf2bplant: .*F2B-SELFTEST: FAIL" $N/hatbb/tests_f2b.out && grep -q "^hbf2bself: .* 0 tracebacks" $N/hatbb/tests_f2b.out && OK=1
t0=$(date +%s); until grep -q "\[s86U-sol_k86GS20_in03\] STACK" $L || [ $(( $(date +%s) - t0 )) -ge 3600 ]; do sleep 30; done
if grep "\[s86U-sol_k86GS20_in03\] STACK" $L | tail -1 | grep -q "UPPER-R2: FEASIBLE"; then FE=$N/cand/sol_k86GS20_in03.json; else FE=$N/cand/sol_k86MK1_in23__K3l5j_k260.json; fi
TIN=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['t'])" $FE)
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt FEAS=$FE
XF0="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export WARM=$(cat $N/runK_k86GS20/warmlist.txt),$N/warm/rows_k86GS20_snap_GS21.txt
if [ $OK = 1 ]; then
  T=k86GS21; ENG=eng_p8h; RUN=$N/p1r/runK86p8h.sh; export XF="$XF0 hatbb hbkeys=$N/hatbb/cg_keys_w6b16x_hatbb.txt"
else
  T=k86GS21y; ENG=eng_p8; RUN=$N/p1r/runK86p8.sh; export XF="$XF0"
  echo "$(date -u +%H:%M:%SZ) [s86SW21] HATBB tests NOT clean ($(tr '\n' ' ' < $N/hatbb/tests_f2b.out | cut -c1-300)): relaunching the GS20 lineage without HATBB as $T" >> $L
fi
cd $N && nohup bash $RUN 200 2 $T inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_$T.out 2>&1 &
sleep 10
cd $N && ENGD=$ENG E86OVR=$N/$ENG nohup bash $N/watch86e.sh $T > $N/logs/watch86_$T.out 2>&1 &
cd $N && nohup bash $N/file86.sh $T > $N/logs/file86_$T.out 2>&1 &
cd $N && nohup bash $N/rowsnap.sh $ENG $T > $N/logs/rowsnap_$T.out 2>&1 &
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_$T; mkdir -p $O; cp $KEYS $O/; [ $OK = 1 ] && cp $N/hatbb/cg_keys_w6b16x_hatbb.txt $O/; (cd $O && md5sum cg_keys_* > MD5SUMS_keys)
P="${T%?}[${T: -1}]"
cd $N && nohup bash -c "while pgrep -f 'pcheck.py solveR2.*tag=$P ' > /dev/null; do for f in $N/$ENG/lpdual_${T}_*.json; do b=\$(basename \$f); [ -e \$f ] && [ ! -e $O/\$b ] && [ \$(( \$(date +%s) - \$(stat -c %Y \$f) )) -gt 30 ] && cp \$f $O/\$b.tmp && mv $O/\$b.tmp $O/\$b && (cd $O && md5sum lpdual_${T}_*.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] \$b -> from_opus/s86_$T\" >> $L; done; sleep 60; done" > /dev/null 2>&1 &
echo "$(date -u +%H:%M:%SZ) [s86G] launched $T on $ENG (K3gB5n 1e1f35e8 + 357 keys 449bf4dd$([ $OK = 1 ] && echo ' + 14 HATBB columns b9ff66bd'), lpdual, GS20 warm + GS20 rows) from $(basename $FEAS) t $TIN; gate (Lead 06:15Z): LP t >= 1.5e-4 below GS20's last LP t after 2 iterations, or a checked point < 0.014164305" >> $L
