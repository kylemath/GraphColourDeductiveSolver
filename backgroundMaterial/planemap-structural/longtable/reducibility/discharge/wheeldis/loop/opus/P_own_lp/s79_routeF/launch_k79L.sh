# s79: K k79L = k79K restarted after the 6 Nov 00:00Z container restart: same stack (s78 engine, K* + EDGE r4, FAM=full, patched298, args_A97_F), in-point k79K in05 (0.023317 FEASIBLE), warm += k79K's 813 rows.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; S79=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s79_routeF; cd $N && . ./env78.sh
W=$W7POOL,$WX75,$WK75,$N/warm/rows_q75B_snap78.txt,$N/warm/rows_b77F_snap78.txt,$N/tests/t6/pool_W6support_floor.txt,$N/tests/t6/pool_b77U6dual_floor.txt,$S79/rows_b77F_final.txt,$S79/rows_q75B_snap4.txt,$N/warm/rows_k79K_final_restart.txt
export ARGS=$S79/args_A97_F.txt STACK=s77 FAM=full KS=1 EGK=$N/eng/edgekeys_r4.txt
WARM=$W FEAS=$N/cand/sol_k79K_in05.json nohup bash runK78.sh 200 1 k79L inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > logs/runK_k79L.out 2>&1 &
sleep 20; nohup bash watch78.sh k79L > logs/watch_k79L.out 2>&1 &
