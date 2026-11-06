# start k83E when base83.sh (b83PF then b83UF) has finished, so 3 solves share the 4 cores
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s83_cons6
while pgrep -f "base83.sh" > /dev/null; do sleep 60; done
echo "$(date -u +%H:%M:%SZ) [s83] base83 done; launching k83E (W13 67 kills, c6le)" >> $P/run.log
bash $P/launch_k83E.sh
