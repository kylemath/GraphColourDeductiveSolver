#!/bin/bash
# s86 launch23.sh (11 Nov 02:12Z): k86GS23 = k86GS22 relaunched after the 02:06Z container restart killed it (seed first: same family,
# no new rung). eng_p8h, K3gB5r b0ce409f + 365 keys 2485a27d + 14 HATBB b9ff66bd, same flags as launch22r.sh. Starts from GS22 in07
# (0.013237894) if our U86 check passes, else from in06 (0.013249702, FEASIBLE 01:00Z). Warm = GS22's warm list + GS22's own rows.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
L=$N/run.log
until grep -q "\[s86U-sol_k86GS22_in07\] STACK" $L; do sleep 30; done; while pgrep -f "pcheck.py upperR2.*sol_k86GS22_in07" > /dev/null; do sleep 30; done
pgrep -f 'pcheck.py solveR2.*tag=k86GS2[23] ' > /dev/null && { echo "$(date -u +%H:%M:%SZ) [s86G] launch23: a GS22/GS23 solve still runs; not starting" >> $L; exit 3; }
if grep "\[s86U-sol_k86GS22_in07\] STACK" $L | tail -1 | grep -q "UPPER-R2: FEASIBLE"; then FE=$N/cand/sol_k86GS22_in07.json; else FE=$N/cand/sol_k86GS22_in06.json; fi
KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstwb.txt; KN=365
TIN=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['t'])" $FE)
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5r.txt KEYS FEAS=$FE
[ "$(md5sum < $ARGS | cut -c1-8)" = b0ce409f ] || { echo "launch23: K3gB5r args md5 mismatch" >> $L; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 2485a27d ] || { echo "launch23: 365-key md5 mismatch" >> $L; exit 5; }
XF0="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export WARM=$(cat $N/runK_k86GS22/warmlist.txt),$N/warm/rows_k86GS22_snap_GS23.txt
OK=1; T=k86GS23; ENG=eng_p8h; RUN=$N/p1r/runK86p8h.sh; export XF="$XF0 hatbb hbkeys=$N/hatbb/cg_keys_w6b16x_hatbb.txt"
cd $N && nohup bash $RUN 200 2 $T inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_$T.out 2>&1 &
sleep 10
cd $N && ENGD=$ENG E86OVR=$N/$ENG nohup bash $N/watch86e.sh $T > $N/logs/watch86_$T.out 2>&1 &
cd $N && nohup bash $N/file86.sh $T > $N/logs/file86_$T.out 2>&1 &
cd $N && nohup bash $N/rowsnap.sh $ENG $T > $N/logs/rowsnap_$T.out 2>&1 &
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_$T; mkdir -p $O; cp $KEYS $O/; [ $OK = 1 ] && cp $N/hatbb/cg_keys_w6b16x_hatbb.txt $O/; (cd $O && md5sum cg_keys_* > MD5SUMS_keys)
P="${T%?}[${T: -1}]"
cd $N && nohup bash -c "while pgrep -f 'pcheck.py solveR2.*tag=$P ' > /dev/null; do for f in $N/$ENG/lpdual_${T}_*.json; do b=\$(basename \$f); [ -e \$f ] && [ ! -e $O/\$b ] && [ \$(( \$(date +%s) - \$(stat -c %Y \$f) )) -gt 30 ] && cp \$f $O/\$b.tmp && mv $O/\$b.tmp $O/\$b && (cd $O && md5sum lpdual_${T}_*.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] \$b -> from_opus/s86_$T\" >> $L; done; sleep 60; done" > /dev/null 2>&1 &
echo "$(date -u +%H:%M:%SZ) [s86G] launched $T on $ENG (K3gB5r b0ce409f + $KN keys $(md5sum < $KEYS | cut -c1-8) + 14 HATBB columns b9ff66bd, lpdual, GS22 warm list + GS22 rows) from $(basename $FEAS) t $TIN; GS22 relaunched after the 02:06Z container restart" >> $L
