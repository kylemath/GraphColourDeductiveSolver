# s86: k86GS19 (10 Nov 01:25Z) = k86GS18 relaunched after the disk filled at 01:13Z (sD work dirs; sdclean.sh now prunes them).  Warm adds GS18's own rows.
# s86: k86GS18 (10 Nov 01:05Z) = k86GS17 relaunched after the ~00:58Z container restart (no new tag reuse): same family/keys/flags, trimmed
# warm rebuilt with GS17's lpduals + GS17's own rows (warm/rows_k86GS17_snap_GS18.txt).  In-point FEAS18, else the ST-94 point.  Older notes (GS17):
# s86: k86GS17 (Lead 9 Nov 22:59Z option A, at GS16's next natural restart) = k86GS16 with 357 keys p1r/cg_keys_r13w16_16fikpqrstw.txt
# (449bf4dd = 347 0a66b3c0 + W6b-16w 32b2adae: payer 7 x4, payer 8 x6, W5) on K3gB5n (1e1f35e8), eng_p8, and a TRIMMED warm pool so a
# GL run + one check fit beside it: mkwarmtrim.py = dual support of every lpdual_k86GS15/16_*.json + the GS-lineage own-row snapshots
# (k85B/k85L finals, k85C/k85CL, k86B/CS/FS, k86GS..GS16) only; the s44..s79 pools are dropped (~106k lines vs 375k; aim <= 5 GB).
# If the in-point trend is worse than GS16's after one ladder round, tell the Lead (fallback (B): fixed GL block overnight).
# Needs p8test/VERDICT_357 (P357OK).  In-point FEAS17, else GS16's current in-point.  Refuses while k86GS16's solveR2 runs.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
[ -x $N/eng_p8/bin/jsepf_gk_k192 ] || { echo "launch_k86GS19: eng_p8/bin/jsepf_gk_k192 missing" >&2; exit 2; }
pgrep -f "pcheck.py solveR2.*tag=k86GS1[8] " > /dev/null && { echo "launch_k86GS19: k86GS18 still running" >&2; exit 3; }
pgrep -f "pcheck.py solveR2.*tag=k86GS1[9] " > /dev/null && { echo "launch_k86GS19: k86GS19 already running" >&2; exit 3; }
grep -q "^P357OK" $N/p8test/VERDICT_357 2>/dev/null || { echo "launch_k86GS19: 357 keys not validated (p8test/VERDICT_357)" >&2; exit 7; }
export E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt FEAS=${FEAS19:-$N/cand/sol_repK1MW_10__K3l5j_k260.json}
[ "$(md5sum < $ARGS | cut -c1-8)" = 1e1f35e8 ] || { echo "launch_k86GS19: K3gB5n args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $N/args_A97_F_W13K3l5n.txt | cut -c1-8)" = 47407139 ] || { echo "launch_k86GS19: K3l5n args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 449bf4dd ] || { echo "launch_k86GS19: 357-key file md5 mismatch" >&2; exit 5; }
[ -s $FEAS ] || { echo "launch_k86GS19: in-point $FEAS missing" >&2; exit 6; }
cp $FEAS $N/cand/sol_k86GS19_from.json; FEAS=$N/cand/sol_k86GS19_from.json
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p8/rows_k86GS18.txt $N/warm/rows_k86GS18_snap_GS19.txt
W=$N/warm; RF=$(ls $W/rows_k86GS*_snap*.txt $W/rows_k86B_snap_it13.txt $W/rows_k86CS_snap_it1.txt $W/rows_k86FS_snap_it3.txt $W/rows_k85C_snap_it3.txt $W/rows_k85CL_snap_it1.txt $B/s85_edge56/runK_k85B/rows_k85B_final.txt $B/s85_edge56/runK_k85L/rows_k85L_final.txt | tr '\n' ',')
python3 -I $N/mkwarmtrim.py $W/rows_GS19_trim.txt --dual $(ls $N/eng_p8/lpdual_k86GS1[5678]_*.json | tr '\n' ',') --rows $RF >> $N/run.log 2>&1 || exit 8
export WARM=$W/rows_GS19_trim.txt
nohup bash $N/p1r/runK86p8.sh 200 2 k86GS19 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_k86GS19.out 2>&1 &
sleep 5
cd $N && ENGD=eng_p8 nohup bash $N/watch86e.sh k86GS19 > $N/logs/watch86_k86GS19.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86GS19 > $N/logs/file86_k86GS19.out 2>&1 &
cd $N && REPL_INIT= TAG=k86GS19 LKEYS=$KEYS bash $N/relaunch_ladderYp8.sh $FEAS $ARGS $N/args_A97_F_W13K3l5n.txt X
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_k86GS19; mkdir -p $O; cp $KEYS $O/ && (cd $O && md5sum cg_keys_r13w16_16fikpqrstw.txt > MD5SUMS_keys)
cd $N && nohup bash -c "while pgrep -f 'pcheck.py solveR2.*tag=k86GS1[9] ' > /dev/null || [ \$(ls $N/eng_p8/lpdual_k86GS19_*.json 2>/dev/null | wc -l) -eq 0 ]; do for f in $N/eng_p8/lpdual_k86GS19_*.json; do b=\$(basename \$f); [ -e \$f ] && [ ! -e $O/\$b ] && [ \$(( \$(date +%s) - \$(stat -c %Y \$f) )) -gt 30 ] && cp \$f $O/\$b.tmp && mv $O/\$b.tmp $O/\$b && (cd $O && md5sum lpdual_k86GS19_*.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] \$b -> from_opus/s86_k86GS19\" >> $N/run.log; done; sleep 60; done" > /dev/null 2>&1 &
cd $N && ARGS=$ARGS KEYS=$KEYS nohup bash $N/macinject86p8c.sh k86GS19 > $N/logs/macinject_k86GS19.out 2>&1 &
sleep 120; cd $N && KEYS=$KEYS FAMS="K3gB5k" nohup bash $N/subchk86p8.sh k86GS19 > $N/logs/subchk_k86GS19.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GS19 (K3gB5n 1e1f35e8 + 357 keys 449bf4dd, eng_p8, lpdual, trimmed warm $(wc -l < $W/rows_GS19_trim.txt) lines) from $(basename $FEAS); ladder checks K3gB5n, sub-check K3l5n; subchk K3gB5k" >> $N/run.log
