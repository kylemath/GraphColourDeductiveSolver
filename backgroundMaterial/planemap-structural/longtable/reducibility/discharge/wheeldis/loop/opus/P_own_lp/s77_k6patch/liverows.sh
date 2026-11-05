# s77: keep warm/rows_<K>_live.txt = complete lines of eng/rows_<K>.txt (atomic), until runL_<L>/L.log shows the warm admission is done.  usage: bash liverows.sh <Ktag> <Ltag>
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch; K=$1; L=$2; F=$N/eng/rows_$K.txt; O=$N/warm/rows_${K}_live_$L.txt
while ! grep -q "warm rows admitted" $N/runL_$L/L.log 2>/dev/null; do
  n=$(wc -l < $F); head -n $n $F > $O.tmp && mv $O.tmp $O; sleep 60
done
echo "$(date -u +%H:%M:%SZ) [s77] L $L admitted; $O frozen at $(wc -l < $O) K rows (md5 $(md5sum < $O | cut -c1-32))" >> $N/run.log
