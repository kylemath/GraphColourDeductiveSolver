# s86: k86GS7 = k86GS6 + kill K5d B1 (D b9_u555557667_5..56...6, w13/pat_K5d_D.out c5c4c210, lead kills_K5d_0805.tsv 031bde25, [E2] ST-49 + K3CHK main d8950ae17): LP K3gB5d, ladder K3l5d.  (k86GS6:) k86GS5 with the K5c kills (V1-V8, w13/pat_K5c_C.cfast + pat_K5c_D.out, lead kills_K5c_0735.tsv b3efa2c5): LP on K3gB5d, ladder on K3l5d.  (k86GS5 header:) k86GS4's in-out upper solve on K3gB5b (= K3gB + K5H01 + K5b L1-L3/U1-U2, args 5e399535, all kills [E2]) with the 240-key file
# p1r/cg_keys_r13w16_16fik.txt (3d996dbb = r13w16 171 + W6b-16f/16i/16k 69) under the STANDARD key coefficients (no p1r flag: p1r is a
# relaxation, sound for lowers only).  89 payer-7 keys > 64, so it runs on the engine copy eng_p1r (jsepf_gk_k192; identical to eng without
# the p1r flag) via p1r/runK86p.sh, and every helper's upperR2 runs there too (E86OVR, env86.sh).  Points are rechecked on K3l5 (= K3l +
# K5H01 + K5b, args 2547de87; Lean HCK5H01 / HCK5b_* / HDK5b_L3 queued) + the same 240 keys; quote on K3l5 once its Lean lands.
# usage: bash launch_k86GS7.sh <in-point name in cand/, FEASIBLE on K3l5d + 240 keys: logs/upper_F_<name minus sol_>.log>
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
[ -x $N/eng_p1r/bin/jsepf_gk_k192 ] || { echo "launch_k86GS7: eng_p1r/bin/jsepf_gk_k192 missing" >&2; exit 2; }
P1=${1#sol_}; grep -q "^UPPER-R2: FEASIBLE" $N/logs/upper_F_$P1.log || { echo "launch_k86GS7: in-point $1 has no FEASIBLE logs/upper_F_$P1.log" >&2; exit 2; }
grep -q "args_A97_F_W13K3l5d.txt gkeys cg_keys_r13w16_16fik.txt" <(grep "\[s86U-F_$P1\]" $N/run.log | tail -1) || { echo "launch_k86GS7: last check of $1 is not on K3l5d + 16fik" >&2; exit 2; }
pgrep -f "tag=k86GS6 " > /dev/null && { echo "launch_k86GS7: k86GS6 still running (two LPs at most); stop it first" >&2; exit 3; }
export E86OVR=$N/eng_p1r STACK=s77 ARGS=$N/args_A97_F_W13K3gB5d.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$N/p1r/cg_keys_r13w16_16fik.txt FEAS=$N/cand/$1.json
export WARM=$(cat $N/runK_k86GS6/warmlist.txt)
if [ -s $N/eng_p1r/rows_k86GS6.txt ]; then cp $N/eng_p1r/rows_k86GS6.txt $N/warm/rows_k86GS6_snap_GS7.txt; WARM=$WARM,$N/warm/rows_k86GS6_snap_GS7.txt; fi
nohup bash $N/p1r/runK86p.sh 200 2 k86GS7 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 > $N/logs/runK_k86GS7.out 2>&1 &
sleep 5
cd $N && ENGD=eng_p1r nohup bash $N/watch86e.sh k86GS7 > $N/logs/watch86_k86GS7.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86GS7 > $N/logs/file86_k86GS7.out 2>&1 &
cd $N && ARGS=$N/args_A97_F_W13K3l5d.txt nohup bash $N/tightwatch.sh k86GS7 >> $N/logs/tightwatch_k86GS7.out 2>&1 &
cd $N && REPL_ENGD=eng_p1r REPL_FAM=W REPL_ARGS=$ARGS REPL_ARGS2=$N/args_A97_F_W13K3l5d.txt REPL_KEYS=$KEYS REPL_PAR=1 REPL_MINMEM=4500 nohup python3 $N/repladder_e.py k86GS7 $FEAS 60 >> $N/logs/repladder_k86GS7.out 2>&1 &
sleep 2; echo "$(date -u +%H:%M:%SZ) [s86G] launched k86GS7 (K3gB5d ec9d8dbb + 240 keys 3d996dbb, standard coefficients, eng_p1r) from $1; ladder rechecks on K3l5d 399cfc4c" >> $N/run.log
