# validation step 2 queue: restricted LPs on the GL5 p1_00 cert, one at a time (each memory gated by v2r_run.sh)
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N
CERT=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_k86GL5/cert_p1_00_def2afcc.json
while pgrep -f "v2rtest v2r cert=" > /dev/null; do sleep 10; done
for m in ${MODES:-mask p1r v2p1rkeys v2 v2curkeys}; do
  bash v2r/v2r_run.sh rlp_$m v2restricted cert=$CERT xcap=3 v2mode=$m v2seed=$N/eng_p1r/sol_k86GL5_p1.json v2json=$N/v2r/rlp/rlp_$m.json v2out=$N/v2r/rlp/cert_rlp_$m.json
done
echo "$(date -u +%H:%M:%SZ) rlp_queue done" >> $N/v2r/logs/runs.txt
