# s86: k86GL11 = k86GL10 relaunched after the container restart of 9 Nov ~07:50Z (GL10 was still loading warm rows). Same flags and warm rows.
# s86: k86GL11 = k86GL9 with the capped separation the Lead asked for (9 Nov 06:14Z): sepmax=3600 (each pass stops at ~60 min, counted
# from the pass start; the rows found so far, including those of a separator stopped by SIGTERM via bin/jsepf_gk_k192s, are added and
# the LP is re-solved; a pass that finds nothing within the cap finishes uncapped, so 'added 0' is still a complete pass) and
# sepord=17,...,9,7,8 (largest violations first). Same family K3gB5k (4f3d8c05), keys, XF and warm rows as k86GL9 (stopped while loading).
# s86: k86GL9 = k86GL8 (container restart 9 Nov ~06:08Z killed it in its first separation) moved to K3gB5k (4f3d8c05 = K3gB5i + K5j + P05; Lead 02:59Z: k at the next natural restart). Was: k86GL8 = k86GL7 (crashed 23:54Z at it 1: LP noise -9e-9 in a key amount hit the gkin assert; prelay2 now zeroes (-1e-7, 0) for separation) moved to K3gB5i (c240d5ec = K3gB5g + P01-P04; Lead 21:46Z: switch at the next natural restart). Was: k86GL7 = k86GL6 moved to K3gB5g (Lead 19:47Z 8 Nov): args_A97_F_W13K3gB5g.txt (6251f38a = K3gB + K5H01 + K5b + K5c V1-V8 + K5d B1
# + K5e B2 + K5f H05 + K5g B3), so its lower covers K3l5g (the sound upper's family); same 240 keys p1r/cg_keys_r13w16_16fik.txt (3d996dbb),
# same XF (c6le f2b7 rules c67fa1d1+A5 twins, rpatN3 + offc_K3g_2f4f0f02, p1r) and flags.  Warm = k86GL6's warm list + k86GL6's own rows
# (passes 0-4 separation rows, complete lines snapshotted to warm/rows_k86GL6_snap_GL7.txt); rows the bigger kill family no longer admits
# (killed labels) are dropped on admission.  Start only after k86GL6 has stopped (two LP runs at most).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
[ -x $N/eng_p1r/bin/jsepf_gk_k192 ] || { echo "launch_k86GL11: eng_p1r/bin/jsepf_gk_k192 missing" >&2; exit 2; }
pgrep -f 'tag=k86GL10 ' > /dev/null && { echo "launch_k86GL11: k86GL11 still running" >&2; exit 3; }
[ -x $N/eng_p1r/bin/jsepf_gk_k192s ] || { echo "launch_k86GL11: eng_p1r/bin/jsepf_gk_k192s missing" >&2; exit 2; }
export STACK=s77 ARGS=${ARGS7:-$N/args_A97_F_W13K3gB5k.txt} XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r" KEYS=${KEYS7:-$N/p1r/cg_keys_r13w16_16fik.txt} FEAS=$N/cand/sol_k85C_in03.json
[ "$(md5sum < $ARGS | cut -c1-8)" = 4f3d8c05 ] || [ -n "$ARGS7" ] || { echo "launch_k86GL11: K3gB5k args md5 mismatch" >&2; exit 4; }
export WARM=$(cat $N/runK_k86GL10/warmlist.txt)
nohup bash $N/p1r/runK86p.sh 200 2 k86GL11 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 sepmax=3600 sepord=17,16,15,14,13,12,11,10,9,7,8 > $N/logs/runK_k86GL11.out 2>&1 &
sleep 5
cd $N && nohup bash $N/p1r/watchL86p.sh k86GL11 > $N/logs/watchL86_k86GL11.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/p1r/dualwatch86p.sh k86GL11 > $N/logs/dualwatch86_k86GL11.out 2>&1 &
