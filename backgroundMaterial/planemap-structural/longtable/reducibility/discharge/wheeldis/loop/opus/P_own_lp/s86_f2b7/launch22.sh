#!/bin/bash
# s86 launch22.sh (10 Nov 10:25Z, Lead 10:14Z "GS22 is a go"): after the HATBB gate control logs its line, start k86GS22 on eng_p8h with
# HATBB on family q (K3gB5q d07d3cce, Lean-complete 09:38Z), from GS21 in02 (0.013963963) if our check passed (else in01), keys 365
# (357 + 8 bb, 2485a27d) if p8test/VERDICT_365 is P365OK (else 357).  Warm = GS20 lineage + GS20 rows + GS21 rows.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
L=$N/run.log
until grep -qE "\[s86C21\] (HATBB GATE|k86GS21n died)" $L; do sleep 30; done
sleep 30; pgrep -f 'pcheck.py solveR2.*tag=k86GS2[12]n? ' > /dev/null && { echo "$(date -u +%H:%M:%SZ) [s86G] launch22: a GS21/GS22 solve still runs; not starting" >> $L; exit 3; }
if grep "\[s86U-sol_k86GS21_in02\] STACK" $L | tail -1 | grep -q "UPPER-R2: FEASIBLE"; then FE=$N/cand/sol_k86GS21_in02.json; else FE=$N/cand/sol_k86GS21_in01.json; fi
if head -1 $N/p8test/VERDICT_365 2>/dev/null | grep -q '^P365OK'; then KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstwb.txt; KN=365; else KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt; KN=357; fi
case $FE in *in02*) NOTE='HATBB kept: in02 passed our check below ST-102 0.014021370 (Lead 10:14Z)';; *) NOTE='in02 did NOT pass our check: started from in01 (0.014028473)';; esac
TIN=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['t'])" $FE)
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5q.txt KEYS FEAS=$FE
[ "$(md5sum < $ARGS | cut -c1-8)" = d07d3cce ] || { echo "launch22: K3gB5q args md5 mismatch" >> $L; exit 4; }
cp $N/eng_p8h/rows_k86GS21.txt $N/warm/rows_k86GS21_snap_GS22.txt
XF0="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export WARM=$(cat $N/runK_k86GS20/warmlist.txt),$N/warm/rows_k86GS20_snap_GS21.txt,$N/warm/rows_k86GS21_snap_GS22.txt
OK=1; T=k86GS22; ENG=eng_p8h; RUN=$N/p1r/runK86p8h.sh; export XF="$XF0 hatbb hbkeys=$N/hatbb/cg_keys_w6b16x_hatbb.txt"
cd $N && nohup bash $RUN 200 2 $T inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_$T.out 2>&1 &
sleep 10
cd $N && ENGD=$ENG E86OVR=$N/$ENG nohup bash $N/watch86e.sh $T > $N/logs/watch86_$T.out 2>&1 &
cd $N && nohup bash $N/file86.sh $T > $N/logs/file86_$T.out 2>&1 &
cd $N && nohup bash $N/rowsnap.sh $ENG $T > $N/logs/rowsnap_$T.out 2>&1 &
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_$T; mkdir -p $O; cp $KEYS $O/; [ $OK = 1 ] && cp $N/hatbb/cg_keys_w6b16x_hatbb.txt $O/; (cd $O && md5sum cg_keys_* > MD5SUMS_keys)
P="${T%?}[${T: -1}]"
cd $N && nohup bash -c "while pgrep -f 'pcheck.py solveR2.*tag=$P ' > /dev/null; do for f in $N/$ENG/lpdual_${T}_*.json; do b=\$(basename \$f); [ -e \$f ] && [ ! -e $O/\$b ] && [ \$(( \$(date +%s) - \$(stat -c %Y \$f) )) -gt 30 ] && cp \$f $O/\$b.tmp && mv $O/\$b.tmp $O/\$b && (cd $O && md5sum lpdual_${T}_*.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] \$b -> from_opus/s86_$T\" >> $L; done; sleep 60; done" > /dev/null 2>&1 &
echo "$(date -u +%H:%M:%SZ) [s86G] launched $T on $ENG (K3gB5q d07d3cce + $KN keys $(md5sum < $KEYS | cut -c1-8) + 14 HATBB columns b9ff66bd, lpdual, GS20 warm + GS20/GS21 rows) from $(basename $FEAS) t $TIN; $NOTE" >> $L
