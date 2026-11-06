# s85: after dual85.sh <tag> finishes: dualexport (every dual row + key coefficients) and dualsplit -> from_opus/s85_k85B/.  usage: bash postdual85.sh <tag>
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; TG=$1; RD=$Z/run_$TG
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s85_k85B
until [ -e $RD/DONE ]; do sleep 60; done
[ -e $RD/cert_$TG.json ] || { echo "$(date -u +%H:%M:%SZ) [s85P-$TG] no cert" >> $Z/run.log; exit 1; }
STACK=s77 ARGS=$B/s79_routeF/args_A97_F.txt bash $Z/wtest.sh dx_$TG dualexport cert=$RD/cert_$TG.json out=$RD/dual_rows_$TG.json gkeys=$Z/keys/A97F_111keys.txt gkwin gkleaf c6le
python3 -I $Z/dualsplit.py $RD/cert_$TG.json 30 > $RD/dual_split_$TG.txt 2>&1
cp $RD/dual_rows_$TG.json $RD/dual_split_$TG.txt $RD/cert_$TG.json $O/; cp $RD/L.log $O/L_$TG.log
cd $O && md5sum A97F_111keys.txt sol_k85B_in*.json upper_sol_k85B_in*.log POINTS.txt DUAL_EXPORT.md dual_rows_*.json dual_split_*.txt cert_*.json L_*.log > MD5SUMS
echo "$(date -u +%H:%M:%SZ) [s85P-$TG] dual export + split copied to from_opus/s85_k85B ($(grep -c . $RD/dual_split_$TG.txt) split lines)" >> $Z/run.log
