# s86: k86GS10 = k86GS9's in-out upper LP moved to K3gB5k (4f3d8c05 = K3l5k + 159 K3g-only kills; K3l5k = K3l5i + K5j + P05) after the
# container restart of 9 Nov ~06:08Z, with flag lpdual (Lead 04:55Z: main-LP row duals lpdual_k86GS10_NN.json in the lextcert format,
# for W6b pricing against the upper; the first one is copied to from_opus/s86_k86GS10/).  In-point repS9X_01 (0.017896489769, FEASIBLE on
# K3gB5i, so on K3gB5k).  Points count once ST-69 (Lean for the 159 K3g-only kills) and HCK5P05 land.  Ladder: checks on K3gB5k, sub-check K3l5k.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
[ -x $N/eng_p1r/bin/jsepf_gk_k192 ] || { echo "launch_k86GS10: eng_p1r/bin/jsepf_gk_k192 missing" >&2; exit 2; }
pgrep -f "tag=k86GS9 " > /dev/null && { echo "launch_k86GS10: k86GS9 still running" >&2; exit 3; }
export E86OVR=$N/eng_p1r STACK=s77 ARGS=$N/args_A97_F_W13K3gB5k.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$N/p1r/cg_keys_r13w16_16fik.txt FEAS=$N/cand/sol_repS9X_01.json
[ "$(md5sum < $ARGS | cut -c1-8)" = 4f3d8c05 ] || { echo "launch_k86GS10: K3gB5k args md5 mismatch" >&2; exit 4; }
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p1r/rows_k86GS9.txt $N/warm/rows_k86GS9_snap_GS10.txt
export WARM=$(cat $N/runK_k86GS9/warmlist.txt),$N/warm/rows_k86GS9_snap_GS10.txt
nohup bash $N/p1r/runK86p.sh 200 2 k86GS10 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual > $N/logs/runK_k86GS10.out 2>&1 &
sleep 5
cd $N && ENGD=eng_p1r nohup bash $N/watch86e.sh k86GS10 > $N/logs/watch86_k86GS10.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86GS10 > $N/logs/file86_k86GS10.out 2>&1 &
cd $N && REPL_INIT= TAG=k86GS10 bash $N/relaunch_ladderX.sh $FEAS $ARGS $N/args_A97_F_W13K3l5k.txt X
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_k86GS10; mkdir -p $O
cd $N && nohup bash -c "until ls $N/eng_p1r/lpdual_k86GS10_00.json >/dev/null 2>&1; do sleep 60; done; sleep 5; cp $N/eng_p1r/lpdual_k86GS10_00.json $O/ && (cd $O && md5sum lpdual_k86GS10_00.json > MD5SUMS_lpdual) && echo \"\$(date -u +%H:%M:%SZ) [s86G] lpdual_k86GS10_00.json -> from_opus/s86_k86GS10\" >> $N/run.log" > /dev/null 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GS10 (K3gB5k 4f3d8c05 + 240 keys, standard coefficients, eng_p1r, lpdual) from sol_repS9X_01; ladder checks K3gB5k, sub-check K3l5k" >> $N/run.log
