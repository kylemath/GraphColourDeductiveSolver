# s86: k86GS15 (Lead 9 Nov 17:05Z + 17:29Z: fold W6b-16r and the W6b-16s payer-8/9 keys into GS15 at GS14's next natural restart, no restart
# just for this) = k86GS14 moved to K3gB5m (f9feb30c = K3l5m + 159 K3g-only kills; K3l5m = K3l5l + K5m D, Lean HDK5m) on the engine copy
# eng_p8 (payer-8/9 EDGE keys, PAYER8SPEC W5 OUT at d >= 8 in rows and WIN, d = 7 leaf payer masks up to 31) with 329 keys
# p1r/cg_keys_r13w16_16fikpqrs.txt (891077d7 = 305 aaeec172 + W6b-16s b8bcafba (24 payer 8/9); payer-7 112 <= 192).
# Needs eng_p8 validated first (p8test/run_tests*.sh: P8REFTEST, GKWINTEST, F2B-SELFTEST PASS and the gkoplant control FAIL).
# In-point: FEAS15, else the best Mac K3l5j point (FEASIBLE on any bigger family + more keys: new keys 0).  Warm = GS14's list + GS14's
# own rows.  Ladder checks K3gB5m, sub-check K3l5m; subchk86p8 rechecks each in-point on K3l5j (Lean-complete) then K3l5m (payer-8
# points need the Studio harness's W5 OUT for [E2]).  Every lpdual_k86GS15_NN.json goes to from_opus/s86_k86GS15/ for W6b.
# Refuses while k86GS14 runs (natural restart only).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
[ -x $N/eng_p8/bin/jsepf_gk_k192 ] || { echo "launch_k86GS15: eng_p8/bin/jsepf_gk_k192 missing" >&2; exit 2; }
pgrep -f "tag=k86GS14 " > /dev/null && { echo "launch_k86GS15: k86GS14 still running" >&2; exit 3; }
pgrep -f "tag=k86GS15 " > /dev/null && { echo "launch_k86GS15: k86GS15 already running" >&2; exit 3; }
grep -q "P8OK" $N/p8test/VERDICT 2>/dev/null || { echo "launch_k86GS15: eng_p8 not validated (p8test/VERDICT has no P8OK)" >&2; exit 7; }
export E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt FEAS=${FEAS15:-$N/cand/sol_repK1MW_04__K3l5j_k260.json}
[ "$(md5sum < $ARGS | cut -c1-8)" = f9feb30c ] || { echo "launch_k86GS15: K3gB5m args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $N/args_A97_F_W13K3l5m.txt | cut -c1-8)" = 6877de46 ] || { echo "launch_k86GS15: K3l5m args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 891077d7 ] || { echo "launch_k86GS15: 329-key file md5 mismatch" >&2; exit 5; }
[ -s $FEAS ] || { echo "launch_k86GS15: in-point $FEAS missing" >&2; exit 6; }
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p1r/rows_k86GS14.txt $N/warm/rows_k86GS14_snap_GS15.txt
export WARM=$(cat $N/runK_k86GS14/warmlist.txt),$N/warm/rows_k86GS14_snap_GS15.txt
nohup bash $N/p1r/runK86p8.sh 200 2 k86GS15 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_k86GS15.out 2>&1 &
sleep 5
cd $N && ENGD=eng_p8 nohup bash $N/watch86e.sh k86GS15 > $N/logs/watch86_k86GS15.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86GS15 > $N/logs/file86_k86GS15.out 2>&1 &
cd $N && REPL_INIT= TAG=k86GS15 LKEYS=$KEYS bash $N/relaunch_ladderYp8.sh $FEAS $ARGS $N/args_A97_F_W13K3l5m.txt X
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_k86GS15; mkdir -p $O; cp $KEYS $O/ && (cd $O && md5sum cg_keys_r13w16_16fikpqrs.txt > MD5SUMS_keys)
cd $N && nohup bash -c "while pgrep -f 'tag=k86GS15 ' > /dev/null || [ \$(ls $N/eng_p8/lpdual_k86GS15_*.json 2>/dev/null | wc -l) -eq 0 ]; do for f in $N/eng_p8/lpdual_k86GS15_*.json; do b=\$(basename \$f); [ -e \$f ] && [ ! -e $O/\$b ] && [ \$(( \$(date +%s) - \$(stat -c %Y \$f) )) -gt 30 ] && cp \$f $O/\$b.tmp && mv $O/\$b.tmp $O/\$b && (cd $O && md5sum lpdual_k86GS15_*.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] \$b -> from_opus/s86_k86GS15\" >> $N/run.log; done; sleep 60; done" > /dev/null 2>&1 &
cd $N && ARGS=$ARGS KEYS=$KEYS nohup bash $N/macinject86p8.sh k86GS15 > $N/logs/macinject_k86GS15.out 2>&1 &
sleep 120; cd $N && KEYS=$KEYS nohup bash $N/subchk86p8.sh k86GS15 > $N/logs/subchk_k86GS15.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GS15 (K3gB5m f9feb30c + 329 keys 891077d7 incl. 24 payer-8/9, eng_p8, lpdual) from $(basename $FEAS); ladder checks K3gB5m, sub-check K3l5m; subchk K3l5j K3l5m" >> $N/run.log
