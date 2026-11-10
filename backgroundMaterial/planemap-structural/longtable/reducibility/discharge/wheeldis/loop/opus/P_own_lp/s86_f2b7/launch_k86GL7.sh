# s86: k86GL7 = k86GL6 moved to K3gB5g (Lead 19:47Z 8 Nov): args_A97_F_W13K3gB5g.txt (6251f38a = K3gB + K5H01 + K5b + K5c V1-V8 + K5d B1
# + K5e B2 + K5f H05 + K5g B3), so its lower covers K3l5g (the sound upper's family); same 240 keys p1r/cg_keys_r13w16_16fik.txt (3d996dbb),
# same XF (c6le f2b7 rules c67fa1d1+A5 twins, rpatN3 + offc_K3g_2f4f0f02, p1r) and flags.  Warm = k86GL6's warm list + k86GL6's own rows
# (passes 0-4 separation rows, complete lines snapshotted to warm/rows_k86GL6_snap_GL7.txt); rows the bigger kill family no longer admits
# (killed labels) are dropped on admission.  Start only after k86GL6 has stopped (two LP runs at most).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
[ -x $N/eng_p1r/bin/jsepf_gk_k192 ] || { echo "launch_k86GL7: eng_p1r/bin/jsepf_gk_k192 missing" >&2; exit 2; }
pgrep -f 'tag=k86GL6 ' > /dev/null && { echo "launch_k86GL7: k86GL6 still running" >&2; exit 3; }
export STACK=s77 ARGS=${ARGS7:-$N/args_A97_F_W13K3gB5g.txt} XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r" KEYS=${KEYS7:-$N/p1r/cg_keys_r13w16_16fik.txt} FEAS=$N/cand/sol_k85C_in03.json
[ "$(md5sum < $ARGS | cut -c1-8)" = 6251f38a ] || [ -n "$ARGS7" ] || { echo "launch_k86GL7: K3gB5g args md5 mismatch" >&2; exit 4; }
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p1r/rows_k86GL6.txt $N/warm/rows_k86GL6_snap_GL7.txt
export WARM=$(cat $N/runK_k86GL6/warmlist.txt),$N/warm/rows_k86GL6_snap_GL7.txt
nohup bash $N/p1r/runK86p.sh 200 2 k86GL7 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 > $N/logs/runK_k86GL7.out 2>&1 &
sleep 5
cd $N && nohup bash $N/p1r/watchL86p.sh k86GL7 > $N/logs/watchL86_k86GL7.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/p1r/dualwatch86p.sh k86GL7 > $N/logs/dualwatch86_k86GL7.out 2>&1 &
