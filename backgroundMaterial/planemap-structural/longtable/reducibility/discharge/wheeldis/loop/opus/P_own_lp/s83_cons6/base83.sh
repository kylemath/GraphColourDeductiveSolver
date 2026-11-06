# s83: c6le re-solve of the proof-stack base lowers (b77PF patched298 0.0210847 and b77UF unpatched 0.0263839, both [E2] in the equality model):
# same warm rows (s77 runL_b77b warmlist), FAM=base, ARGS=args_studio_full, nosep + conssep + c6le, then exact repair (L83.sh). Waits for xW_c6_ks.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; P=$B/s83_cons6
until [ -f $P/runL_xW_c6_ks/DONE ]; do sleep 60; done
W=$(cat $B/s77_k6patch/runL_b77b/warmlist.txt); echo "$W" | tr ',' '\n' > $P/warm/base83_warmlist.txt
( export STACK=s77 ARGS=$B/s77_k6patch/args/args_studio_full.txt FAM=base KS=0; bash $P/L83.sh b83PF "$W" "c6le conssep lpmax=45" )
( export STACK=s77 ARGS=$B/s77_k6patch/args/args_studio_full.txt FAM=base KS=0 KT=$B/s64_keep95p131f/tab/kill/kill6; bash $P/L83.sh b83UF "$W" "c6le conssep lpmax=45" )
echo "$(date -u +%H:%M:%SZ) [s83] BASE83 DONE" >> $P/run.log
