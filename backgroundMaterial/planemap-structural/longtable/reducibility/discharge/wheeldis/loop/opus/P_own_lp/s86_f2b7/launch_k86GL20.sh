# s86: k86GL20 (Lead 10 Nov 03:40Z) = GL19 setup with flag consempty (eng_p8l patched: empty cons2 rows kept as t >= 0, W6r-GLD),
# warm += GL19 rows; beside GS20; GL has priority over GS20 checks (Lead).  Older notes (GL19):
# s86: k86GL19 (10 Nov 01:05Z) = k86GL18 relaunched after the ~00:58Z container restart; warm += GL18's own rows (warm/rows_k86GL18_snap_GL19.txt).
# s86: k86GL18 (Lead 9 Nov 22:59Z option A: restart the GL lane beside the trimmed GS17) = k86GL17 with 357 keys (449bf4dd,
# p8test/VERDICT_357), warm = GL lineage (62k) + GL17's own rows (warm/rows_k86GL17_snap_swap.txt, stopped 22:57Z at it 15).  glguard2.sh
# (10 s poll) stops GL18 before a check can be OOM-killed.  Older notes (GL17):
# s86: k86GL17 (Lead 9 Nov 20:30Z: one floor block on K3gB5n + 347 + p1r, warm from GL16's rows, without starving GS16's checks)
# = k86GL16 moved to K3gB5n (1e1f35e8) + 347 keys (0a66b3c0, p8test/VERDICT_347) on eng_p8l, same flags (sepord d7/d8 first, K=300,
# Khi9=900, Khi=150 at d >= 10, sepmax 3600, lext).  MEMORY: warm = the GL lineage row snapshots only (warm/warmlist_GL17_lineage.txt:
# GL..GL15 + k86L + k85CL, 62,484 distinct rows) instead of the 50-file pool (289k rows), so the LP fits next to GS16 + one check.
# GL16 had no own rows (stopped in setup).  gl17guard.sh stops GL17 (rows snapshotted) if a GS16 check waits > 20 min for memory.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
grep -q '^P357OK' $N/p8test/VERDICT_357 2>/dev/null || { echo "launch_k86GL20: 357 keys not validated" >&2; exit 2; }
grep -q '^P1ROK' $N/p8test/VERDICT_P1R 2>/dev/null || { echo "launch_k86GL20: eng_p8l not validated" >&2; exit 2; }
pgrep -f 'pcheck.py solveR2.*tag=k86GL(19|20) ' > /dev/null && { echo "launch_k86GL20: GL19/GL20 running" >&2; exit 3; }
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r" KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt FEAS=$N/cand/sol_k85C_in03.json
[ "$(md5sum < $ARGS | cut -c1-8)" = 1e1f35e8 ] || { echo "launch_k86GL20: K3gB5n args md5 mismatch" >&2; exit 4; }
[ "$(md5sum < $KEYS | cut -c1-8)" = 449bf4dd ] || { echo "launch_k86GL20: 357-key file md5 mismatch" >&2; exit 5; }
python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p8l/rows_k86GL19.txt $N/warm/rows_k86GL19_snap_GL20.txt
export WARM=$(cat $N/warm/warmlist_GL17_lineage.txt),$N/warm/rows_k86GL17_snap_swap.txt,$N/warm/rows_k86GL18_snap_GL19.txt,$N/warm/rows_k86GL19_snap_GL20.txt
nohup bash $N/p1r/runK86p8l.sh 200 2 k86GL20 lext lextcert consempty q7pen=1e-3 consk=20 consfrac=0.25 sepmax=3600 sepord=7,8,9,10,11,12,13,14,15,16,17 K=300 Khi9=900 Khi=150 warmcache=$N/warmcache > $N/logs/runK_k86GL20.out 2>&1 &
sleep 5
cd $N && nohup bash $N/p1r/watchL86p8l.sh k86GL20 > $N/logs/watchL86_k86GL20.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/p1r/dualwatch86p8l.sh k86GL20 > $N/logs/dualwatch86_k86GL20.out 2>&1 &
cd $N && nohup bash p1r/bindwatch86.sh k86GL20 > $N/logs/bindwatch86_k86GL20.out 2>&1 &
cd $N && nohup bash $N/rowsnap.sh eng_p8l k86GL20 > /dev/null 2>&1 &   # no glguard: GL20 has priority over GS20 checks (Lead 03:40Z)
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GL20 (K3gB5n 1e1f35e8 + 357 keys 449bf4dd + p1r on eng_p8l, lext; consempty; warm GL lineage + GL17-19 rows; priority over GS20 checks)" >> $N/run.log
