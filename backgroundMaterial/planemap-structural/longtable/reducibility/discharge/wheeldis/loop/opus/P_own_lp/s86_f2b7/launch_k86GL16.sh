# s86: k86GL16 (Lead 9 Nov 19:42Z "go on (a)") = the floor run on K3gB5m (f9feb30c) + the 329 keys (891077d7, incl. the 24 W6b-16s
# payer-8/9 keys) + p1r, on engine eng_p8l (eng_p8 + p1r with d8 OUT = the exact sure count for payer-8/9 keys; validated
# p8test/VERDICT_P1R).  Lead's cheap alternative to the payer-8 p1r rewrite: d7/d8 first in sepord, and a lower cap of separated rows at
# d >= 10 (Khi=150; Khi9=900 keeps GL15's cap at d = 9; K=300 at d7/d8).  Same XF, lext flags and sepmax as GL15.
# Warm = GL15's warm list (GL12 list + GL12 rows) + GL15's own rows (warm/rows_k86GL15_snap_GL16.txt, 7,252).
# Its lower covers K3gB5m and every subfamily (K3l5j/k/l/m with the 329 keys or any subset).  Start only after k86GL15 has stopped.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
grep -q '^P1ROK' $N/p8test/VERDICT_P1R 2>/dev/null || { echo "launch_k86GL16: eng_p8l not validated (p8test/VERDICT_P1R)" >&2; exit 2; }
[ -x $N/eng_p8l/bin/jsepf_gk_k192 ] && [ -x $N/eng_p8l/bin/jsepf_gk_k192s ] || { echo "launch_k86GL16: eng_p8l/bin/jsepf_gk_k192(s) missing" >&2; exit 2; }
pgrep -f 'tag=k86GL15 ' > /dev/null && { echo "launch_k86GL16: k86GL15 still running" >&2; exit 3; }
pgrep -f 'tag=k86GL16 ' > /dev/null && { echo "launch_k86GL16: k86GL16 already running" >&2; exit 3; }
grep -q "OPT.get('Khi9'" $N/eng_p8l/prelay2.py || { echo "launch_k86GL16: prelay2.py has no Khi9 option" >&2; exit 2; }
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r" KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt FEAS=$N/cand/sol_k85C_in03.json
[ "$(md5sum < $ARGS | cut -c1-8)" = f9feb30c ] || { echo "launch_k86GL16: K3gB5m args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 891077d7 ] || { echo "launch_k86GL16: 329-key file md5 mismatch" >&2; exit 5; }
[ -s $N/warm/rows_k86GL15_snap_GL16.txt ] || { echo "launch_k86GL16: GL15 rows snapshot missing" >&2; exit 6; }
export WARM=$(cat $N/runK_k86GL15/warmlist.txt),$N/warm/rows_k86GL15_snap_GL16.txt
nohup bash $N/p1r/runK86p8l.sh 200 2 k86GL16 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 sepmax=3600 sepord=7,8,9,10,11,12,13,14,15,16,17 K=300 Khi9=900 Khi=150 warmcache=$N/warmcache > $N/logs/runK_k86GL16.out 2>&1 &
sleep 5
cd $N && nohup bash $N/p1r/watchL86p8l.sh k86GL16 > $N/logs/watchL86_k86GL16.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/p1r/dualwatch86p8l.sh k86GL16 > $N/logs/dualwatch86_k86GL16.out 2>&1 &
cd $N && nohup bash p1r/bindwatch86.sh k86GL16 > $N/logs/bindwatch86_k86GL16.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GL16 (K3gB5m f9feb30c + 329 keys 891077d7 + p1r on eng_p8l, lext; sepord d7/d8 first, K=300, Khi9=900, Khi=150 at d >= 10, sepmax 3600; warm = GL15 list + GL15 rows)" >> $N/run.log
