# s86: k86GS14 = k86GS13 relaunched after the container restart of 9 Nov ~14:46Z (GS13 was still building its warm cache; new tag per relaunch); in-point default = Mac MS6 sol_repS6MW_04__K3l5j (cbf8dcee, 0.016520036 [E2] ST-83 on K3l5j + 240, so on K3gB5l + 280).
# s86: k86GS14 (Lead 9 Nov 12:10Z: fold W6b-16q into the upper at GS12's next natural restart, do not force one) = k86GS12 moved to
# K3gB5l (5f88581e = K3l5l + 159 K3g-only kills; K3l5l = K3l5k + P06 D, P07 C, P08 D) with 280 keys p1r/cg_keys_r13w16_16fikpq.txt
# (7ad4bf1f = 260 0470c459 + W6b-16q 315416ff, payer 5/6/7 = 88/93/99 <= 192 for jsepf_gk_k192).  In-point: FEAS14, else the Mac MS6
# point sol_repS6MW_01__K3l5j (45d6c79b, 0.016910200 [E2] ST-80 on K3l5j + 240; FEASIBLE here on K3gB5k + 260) -- pass a newer ladder
# in-point if one exists.  Warm = GS12's list + GS12's own rows.  Ladder checks K3gB5l, sub-check K3l5l.  Every lpdual_k86GS14_NN.json is
# copied to from_opus/s86_k86GS14/ for W6b.  Refuses while k86GS12 runs (stop it first: the restart is the natural one, never forced).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
[ -x $N/eng_p1r/bin/jsepf_gk_k192 ] || { echo "launch_k86GS14: eng_p1r/bin/jsepf_gk_k192 missing" >&2; exit 2; }
pgrep -f "tag=k86GS13 " > /dev/null && { echo "launch_k86GS14: k86GS13 still running" >&2; exit 3; }
pgrep -f "tag=k86GS12 " > /dev/null && { echo "launch_k86GS14: k86GS12 still running" >&2; exit 3; }
pgrep -f "tag=k86GS14 " > /dev/null && { echo "launch_k86GS14: k86GS14 already running" >&2; exit 3; }
export E86OVR=$N/eng_p1r STACK=s77 ARGS=$N/args_A97_F_W13K3gB5l.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$N/p1r/cg_keys_r13w16_16fikpq.txt FEAS=${FEAS14:-$N/cand/sol_repS6MW_04__K3l5j.json}
[ "$(md5sum < $ARGS | cut -c1-8)" = 5f88581e ] || { echo "launch_k86GS14: K3gB5l args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $N/args_A97_F_W13K3l5l.txt | cut -c1-8)" = 13088367 ] || { echo "launch_k86GS14: K3l5l args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 7ad4bf1f ] || { echo "launch_k86GS14: 280-key file md5 mismatch" >&2; exit 5; }
[ -s $FEAS ] || { echo "launch_k86GS14: in-point $FEAS missing" >&2; exit 6; }
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p1r/rows_k86GS12.txt $N/warm/rows_k86GS12_snap_GS13.txt
export WARM=$(cat $N/runK_k86GS12/warmlist.txt),$N/warm/rows_k86GS12_snap_GS13.txt
nohup bash $N/p1r/runK86p.sh 200 2 k86GS14 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_k86GS14.out 2>&1 &
sleep 5
cd $N && ENGD=eng_p1r nohup bash $N/watch86e.sh k86GS14 > $N/logs/watch86_k86GS14.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86GS14 > $N/logs/file86_k86GS14.out 2>&1 &
cd $N && REPL_INIT= TAG=k86GS14 LKEYS=$KEYS bash $N/relaunch_ladderY.sh $FEAS $ARGS $N/args_A97_F_W13K3l5l.txt X
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_k86GS14; mkdir -p $O; cp $KEYS $O/ && (cd $O && md5sum cg_keys_r13w16_16fikpq.txt > MD5SUMS_keys)
cd $N && nohup bash -c "while pgrep -f 'tag=k86GS14 ' > /dev/null || [ \$(ls $N/eng_p1r/lpdual_k86GS14_*.json 2>/dev/null | wc -l) -eq 0 ]; do for f in $N/eng_p1r/lpdual_k86GS14_*.json; do b=\$(basename \$f); [ -e \$f ] && [ ! -e $O/\$b ] && [ \$(( \$(date +%s) - \$(stat -c %Y \$f) )) -gt 30 ] && cp \$f $O/\$b.tmp && mv $O/\$b.tmp $O/\$b && (cd $O && md5sum lpdual_k86GS14_*.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] \$b -> from_opus/s86_k86GS14\" >> $N/run.log; done; sleep 60; done" > /dev/null 2>&1 &
cd $N && ARGS=$ARGS KEYS=$KEYS nohup bash $N/macinject86.sh k86GS14 > $N/logs/macinject_k86GS14.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GS14 (K3gB5l 5f88581e + 280 keys 7ad4bf1f, eng_p1r, lpdual) from $(basename $FEAS); ladder checks K3gB5l, sub-check K3l5l" >> $N/run.log
