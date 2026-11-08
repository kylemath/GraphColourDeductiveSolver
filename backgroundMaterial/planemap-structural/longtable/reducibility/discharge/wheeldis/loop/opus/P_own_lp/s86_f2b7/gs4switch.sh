# s86: move the upper slot from k86GS3 (K3g) to k86GS4 (K3gB = K3g + kill B): tighten GS3's in01 candidate on K3l first (it was skipped by watch86:
# the relaunched GS3 reuses old in-point names), then stop GS3 + its ladder, launch GS4 from the better point, restart repladder + tightwatch for GS4.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; cd $N
cp eng/sol_k86GS3_in01.json cand/sol_k86GS3b_in01.json
bash tighten.sh $N/cand/sol_k86GS3b_in01.json 0.003 >> logs/tightwatch_k86GS3.out 2>&1
P=sol_repS3W_06; grep -q "tighten k86GS3b_in01 .*UPPER-R2: FEASIBLE" run.log && P=sol_k86GS3b_in01_tight
echo "$(date -u +%H:%M:%SZ) [s86G] gs4switch: stopping GS3 (K3g); launching GS4 on K3gB from $P" >> run.log
pkill -f startrep.sh; pkill -f "repladder.py k86GS3"; pkill -f "tightwatch.sh k86GS3"; pkill -f "runK86.sh 200 2 k86GS3"; pkill -f "watch86.sh k86GS3"; pkill -f "file86.sh k86GS3"; sleep 2; pkill -f "tag=k86GS3 "; pkill -f "U86.sh REPk86GS3"; sleep 20
until [ $(free -m | awk 'NR==2{print $7}') -ge 4000 ]; do sleep 20; done
bash launch_k86GS4.sh $P
nohup bash tightwatch.sh k86GS4 >> logs/tightwatch_k86GS4.out 2>&1 &
REPL_FAM=W REPL_ARGS=$N/args_A97_F_W13K3gB.txt REPL_KEYS=$B/s85_edge56/keys/cg_keys_r13w16.txt REPL_ARGS2=$N/args_A97_F_W13K3l.txt REPL_K0=5 REPL_PAR=1 REPL_MINMEM=4500 nohup python3 repladder.py k86GS4 $N/cand/$P.json 60 >> logs/repladder_k86GS4.out 2>&1 &
echo "$(date -u +%H:%M:%SZ) [s86G] gs4switch: GS4 launched from $P; repladder k86GS4 (K3gB / ARGS2 K3l) and tightwatch k86GS4 started" >> run.log
