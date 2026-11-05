# s77 phase 2: once the sol_c upper control is done, start K b77K (FAM=base, 1 thread while L b77a runs) + its in-point watcher (held by HOLD_WATCH while an L runs)
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch; cd $N
until grep -q "s77U-ctl_solc" run.log; do sleep 15; done
grep -q "s77U-ctl_solc.*FEASIBLE at t = 0.041565" run.log || { echo "$(date -u +%H:%M:%SZ) [s77] sol_c control not FEASIBLE on the patched stack: K NOT started" >> run.log; exit 1; }
FAM=base nohup bash runK77.sh 200 1 b77K inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 feascols > logs/runK_b77K.out 2>&1 &
sleep 5; FAM=base nohup bash watch77.sh b77K > logs/watch_b77K.out 2>&1 &
