# s86: k86GS20 (Lead 10 Nov 02:42Z: "the thin pool cost more than it saved") = GS16's FULL warm list + the GS16..GS19 own rows, 357 keys
# (449bf4dd), alone with its checks (GL lane stopped: t1 = -2/11 on payer-8 key files, diagnosis k86GLD1).  In-point FEAS20, else ST-94.  Older notes (GS16):
# s86: k86GS16 (Lead 9 Nov 20:30Z "(a)": move the upper to K3gB5n + 347 as soon as the 347-key tests pass) = k86GS15 moved to
# K3gB5n (1e1f35e8 = K3gB5m + P09 D f9_555557557_.....676., ST-91) with 347 keys p1r/cg_keys_r13w16_16fikpqrstw.txt (0a66b3c0 = 329
# 891077d7 + W6b-16t sel18 b9440d2d: payer 8 x10, payer 7 x8; payer-7 120 <= 192) on eng_p8.  Needs p8test/VERDICT_347 (P347OK).
# In-point: FEAS16, else ST-89's sol_k86MK1_in08__K3l5j_k260 (0.015523694 [E2] on K3l5j + 260; FEASIBLE on K3gB5m + 329 here).
# Warm = GS15's list + GS15's own rows.  Ladder checks K3gB5n, sub-check K3l5n; subchk rechecks each in-point on K3l5k (Lean-complete)
# and K3l5n.  macinject86p8b also picks sol_k86MK* Mac points.  Every lpdual_k86GS16_NN.json goes to from_opus/s86_k86GS16/.
# Refuses while k86GS15's solveR2 runs (stop GS15 + its helpers first; the GS15 copier loop self-matches 'tag=k86GS15 ').
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
[ -x $N/eng_p8/bin/jsepf_gk_k192 ] || { echo "launch_k86GS20: eng_p8/bin/jsepf_gk_k192 missing" >&2; exit 2; }
pgrep -f "pcheck.py solveR2.*tag=k86GS1[9] " > /dev/null && { echo "launch_k86GS20: k86GS19 still running" >&2; exit 3; }
pgrep -f "pcheck.py solveR2.*tag=k86GS2[0] " > /dev/null && { echo "launch_k86GS20: k86GS20 already running" >&2; exit 3; }
grep -q "^P357OK" $N/p8test/VERDICT_357 2>/dev/null || { echo "launch_k86GS20: 357 keys not validated (p8test/VERDICT_357)" >&2; exit 7; }
export E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt FEAS=${FEAS20:-$N/cand/sol_repK1MW_10__K3l5j_k260.json}
[ "$(md5sum < $ARGS | cut -c1-8)" = 1e1f35e8 ] || { echo "launch_k86GS20: K3gB5n args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $N/args_A97_F_W13K3l5n.txt | cut -c1-8)" = 47407139 ] || { echo "launch_k86GS20: K3l5n args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 449bf4dd ] || { echo "launch_k86GS20: 357-key file md5 mismatch" >&2; exit 5; }
[ -s $FEAS ] || { echo "launch_k86GS20: in-point $FEAS missing" >&2; exit 6; }
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p8/rows_k86GS19.txt $N/warm/rows_k86GS19_snap_GS20.txt
export WARM=$(cat $N/runK_k86GS16/warmlist.txt),$N/warm/rows_k86GS16_snap_GS17.txt,$N/warm/rows_k86GS17_snap_GS18.txt,$N/warm/rows_k86GS18_snap_GS19.txt,$N/warm/rows_k86GS19_snap_GS20.txt
nohup bash $N/p1r/runK86p8.sh 200 2 k86GS20 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_k86GS20.out 2>&1 &
sleep 5
cd $N && ENGD=eng_p8 nohup bash $N/watch86e.sh k86GS20 > $N/logs/watch86_k86GS20.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86GS20 > $N/logs/file86_k86GS20.out 2>&1 &
cd $N && REPL_INIT= TAG=k86GS20 LKEYS=$KEYS bash $N/relaunch_ladderYp8.sh $FEAS $ARGS $N/args_A97_F_W13K3l5n.txt X
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_k86GS20; mkdir -p $O; cp $KEYS $O/ && (cd $O && md5sum cg_keys_r13w16_16fikpqrstw.txt > MD5SUMS_keys)
cd $N && nohup bash -c "while pgrep -f 'pcheck.py solveR2.*tag=k86GS2[0] ' > /dev/null || [ \$(ls $N/eng_p8/lpdual_k86GS20_*.json 2>/dev/null | wc -l) -eq 0 ]; do for f in $N/eng_p8/lpdual_k86GS20_*.json; do b=\$(basename \$f); [ -e \$f ] && [ ! -e $O/\$b ] && [ \$(( \$(date +%s) - \$(stat -c %Y \$f) )) -gt 30 ] && cp \$f $O/\$b.tmp && mv $O/\$b.tmp $O/\$b && (cd $O && md5sum lpdual_k86GS20_*.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] \$b -> from_opus/s86_k86GS20\" >> $N/run.log; done; sleep 60; done" > /dev/null 2>&1 &
cd $N && ARGS=$ARGS KEYS=$KEYS nohup bash $N/macinject86p8c.sh k86GS20 > $N/logs/macinject_k86GS20.out 2>&1 &
sleep 120; cd $N && KEYS=$KEYS FAMS="K3gB5k" nohup bash $N/subchk86p8.sh k86GS20 > $N/logs/subchk_k86GS20.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GS20 (K3gB5n 1e1f35e8 + 357 keys 449bf4dd, eng_p8, lpdual, full warm + GS16-19 rows) from $(basename $FEAS); ladder checks K3gB5n, sub-check K3l5n; subchk K3gB5k" >> $N/run.log
