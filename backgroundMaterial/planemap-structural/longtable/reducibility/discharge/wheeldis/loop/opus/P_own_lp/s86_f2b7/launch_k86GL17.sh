# s86: k86GL17 (Lead 9 Nov 20:30Z: one floor block on K3gB5n + 347 + p1r, warm from GL16's rows, without starving GS16's checks)
# = k86GL16 moved to K3gB5n (1e1f35e8) + 347 keys (0a66b3c0, p8test/VERDICT_347) on eng_p8l, same flags (sepord d7/d8 first, K=300,
# Khi9=900, Khi=150 at d >= 10, sepmax 3600, lext).  MEMORY: warm = the GL lineage row snapshots only (warm/warmlist_GL17_lineage.txt:
# GL..GL15 + k86L + k85CL, 62,484 distinct rows) instead of the 50-file pool (289k rows), so the LP fits next to GS16 + one check.
# GL16 had no own rows (stopped in setup).  gl17guard.sh stops GL17 (rows snapshotted) if a GS16 check waits > 20 min for memory.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
grep -q '^P347OK' $N/p8test/VERDICT_347 2>/dev/null || { echo "launch_k86GL17: 347 keys not validated" >&2; exit 2; }
grep -q '^P1ROK' $N/p8test/VERDICT_P1R 2>/dev/null || { echo "launch_k86GL17: eng_p8l not validated" >&2; exit 2; }
pgrep -f 'pcheck.py solveR2.*tag=k86GL1[67] ' > /dev/null && { echo "launch_k86GL17: GL16/GL17 running" >&2; exit 3; }
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r" KEYS=$N/p1r/cg_keys_r13w16_16fikpqrst.txt FEAS=$N/cand/sol_k85C_in03.json
[ "$(md5sum < $ARGS | cut -c1-8)" = 1e1f35e8 ] || { echo "launch_k86GL17: K3gB5n args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 0a66b3c0 ] || { echo "launch_k86GL17: 347-key file md5 mismatch" >&2; exit 5; }
export WARM=$(cat $N/warm/warmlist_GL17_lineage.txt)
nohup bash $N/p1r/runK86p8l.sh 200 2 k86GL17 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 sepmax=3600 sepord=7,8,9,10,11,12,13,14,15,16,17 K=300 Khi9=900 Khi=150 warmcache=$N/warmcache > $N/logs/runK_k86GL17.out 2>&1 &
sleep 5
cd $N && nohup bash $N/p1r/watchL86p8l.sh k86GL17 > $N/logs/watchL86_k86GL17.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/p1r/dualwatch86p8l.sh k86GL17 > $N/logs/dualwatch86_k86GL17.out 2>&1 &
cd $N && nohup bash p1r/bindwatch86.sh k86GL17 > $N/logs/bindwatch86_k86GL17.out 2>&1 &
cd $N && nohup bash $N/gl17guard.sh > $N/logs/gl17guard.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GL17 (K3gB5n 1e1f35e8 + 347 keys 0a66b3c0 + p1r on eng_p8l, lext; GL lineage warm rows only (62k) to fit next to GS16; gl17guard yields to GS16 checks)" >> $N/run.log
