# s86: k86GS4 = k86GS3 + offc (off-centre kills, offc/offc_K3g_2f4f0f02.txt, 250 rpatN-format patterns, [E2] ST-32) loaded via rpatN=A,B.
# Start ONLY if k86GL3 (lower with offc) shows offc moves the floor; it replaces k86GS3 (2 LP runs fit in memory).
# In-point $1 must have a FEASIBLE recheck under the GS3 family (more kills only drop rows, so it stays feasible with offc).
# Repair ladder for GS4: REPL_RPATN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt REPL_FAM=O python3 repladder.py k86GS4 <in-point>
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3g.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt" KEYS=$Z/keys/cg_keys_r13w16.txt FEAS=$N/cand/$1.json
P1=${1#sol_}; grep -q "^UPPER-R2: FEASIBLE" $N/logs/upper_F_$P1.log || { echo "in-point $1 has no FEASIBLE recheck under the proof-stack family" >&2; exit 2; }
SN=$(ls -t $N/warm/rows_k86GS3_snap_it*.txt 2>/dev/null | head -1)
export WARM=$(cat $N/runK_k86B/warmlist.txt),$N/warm/rows_k86B_snap_it13.txt,$N/warm/rows_k86CS_snap_it1.txt,$N/warm/rows_k86FS_snap_it3.txt,$N/warm/rows_k86GS_snap_it3.txt,$N/warm/rows_k86GS2_snap_it5.txt${SN:+,$SN}
nohup bash $N/runK86.sh 200 2 k86GS4 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 > $N/logs/runK_k86GS4.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watch86.sh k86GS4 > $N/logs/watch86_k86GS4.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86GS4 > $N/logs/file86_k86GS4.out 2>&1 &
