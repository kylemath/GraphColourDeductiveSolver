# s79: K b79F = b77F (patched-298 kill6 U7, FAM=full: rr+z+zr+q7) + B3 route-F D patterns (pat_B3_routeF.out) on the A97 stack.
# feas = b77F in02 (t 0.029906, FEASIBLE on nc); warm = b77F warmlist + rows_b77F snapshot + rows_q75B snapshot (q75B K stopped 19:2xZ to free its 2 threads).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch; S79=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s79_routeF
W=$(cat $N/runK_b77F/warmlist.txt),$S79/rows_b77F_snap1.txt,$S79/rows_q75B_snap4.txt
cd $N && ARGS=$S79/args_A97_F.txt FAM=full WARM=$W FEAS=$N/cand/sol_b77F_in02.json nohup bash runK77.sh 200 2 b79F inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_b79F.out 2>&1 &
sleep 5; cd $N && ARGS=$S79/args_A97_F.txt FAM=full nohup bash watch77.sh b79F > $N/logs/watch_b79F.out 2>&1 &
