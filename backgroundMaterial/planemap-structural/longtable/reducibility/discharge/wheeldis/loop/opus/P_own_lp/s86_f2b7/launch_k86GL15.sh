# s86: k86GL15 = k86GL14 relaunched after the container restart of 9 Nov ~14:46Z (still building its warm cache). Same flags, family and warm rows.
# s86: k86GL15 = k86GL13 relaunched after the container restart of 9 Nov ~13:42Z (GL13 was still building its warm cache; new tag per relaunch). Same flags, family and warm rows.
# s86: k86GL15 (Lead 9 Nov 13:10Z: GL12 had two t1 = 0 passes with its d9-17 violations growing 6 -> 9-14, so restart now) = k86GL12
# moved to K3gB5l (5f88581e = K3l5l + 159 K3g-only kills), same 240 keys (3d996dbb) + p1r and XF, with Khi=900: the per-pass cap of
# separated rows per degree is 3x at d >= 9 (K=300 kept at d7/d8; prelay2.py option Khi, 145ea98b).  sepmax=3600 and sepord kept.
# Warm = GL12's warm list + all of GL12's own rows (2,987 R + 1,008 C, complete lines snapshotted to warm/rows_k86GL12_snap_GL13.txt).
# Its lower covers K3l5l and every subfamily (K3l5j, the sound upper's family).  Start only after k86GL12 has stopped (two LP runs at most).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
[ -x $N/eng_p1r/bin/jsepf_gk_k192 ] && [ -x $N/eng_p1r/bin/jsepf_gk_k192s ] || { echo "launch_k86GL15: eng_p1r/bin/jsepf_gk_k192(s) missing" >&2; exit 2; }
pgrep -f 'tag=k86GL12 ' > /dev/null && { echo "launch_k86GL15: k86GL12 still running" >&2; exit 3; }
pgrep -f 'tag=k86GL15 ' > /dev/null && { echo "launch_k86GL15: k86GL15 already running" >&2; exit 3; }
grep -q "OPT.get('Khi'" $N/eng_p1r/prelay2.py || { echo "launch_k86GL15: prelay2.py has no Khi option" >&2; exit 2; }
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5l.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r" KEYS=$N/p1r/cg_keys_r13w16_16fik.txt FEAS=$N/cand/sol_k85C_in03.json
[ "$(md5sum < $ARGS | cut -c1-8)" = 5f88581e ] || { echo "launch_k86GL15: K3gB5l args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 3d996dbb ] || { echo "launch_k86GL15: 240-key file md5 mismatch" >&2; exit 5; }
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p1r/rows_k86GL12.txt $N/warm/rows_k86GL12_snap_GL13.txt
export WARM=$(cat $N/runK_k86GL12/warmlist.txt),$N/warm/rows_k86GL12_snap_GL13.txt
nohup bash $N/p1r/runK86p.sh 200 2 k86GL15 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 sepmax=3600 sepord=17,16,15,14,13,12,11,10,9,7,8 Khi=900 warmcache=$N/warmcache > $N/logs/runK_k86GL15.out 2>&1 &
sleep 5
cd $N && nohup bash $N/p1r/watchL86p.sh k86GL15 > $N/logs/watchL86_k86GL15.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/p1r/dualwatch86p.sh k86GL15 > $N/logs/dualwatch86_k86GL15.out 2>&1 &
cd $N && nohup bash p1r/bindwatch86.sh k86GL15 > $N/logs/bindwatch86_k86GL15.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GL15 (K3gB5l 5f88581e + 240 keys 3d996dbb + p1r, lext, Khi=900 at d >= 9, sepmax 3600; warm = GL12 list + GL12 rows)" >> $N/run.log
