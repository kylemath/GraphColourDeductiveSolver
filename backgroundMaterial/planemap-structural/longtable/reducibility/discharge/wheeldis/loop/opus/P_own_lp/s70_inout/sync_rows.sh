# s70 Team A: copy the K checkpoint eng/rows_<tag>.txt to the W12 shared folder whenever it changes (poll 60 s).  usage: nohup bash sync_rows.sh <tag> &
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s70_inout
D=/mnt/project-files/swarm/round6/W12-studio-K/from_opus; TAG=$1; F=$N/eng/rows_$TAG.txt; last=""
while true; do
  if [ -s $F ]; then m=$(stat -c %Y:%s $F); if [ "$m" != "$last" ]; then cp $F $D/rows_$TAG.txt.tmp && mv $D/rows_$TAG.txt.tmp $D/rows_$TAG.txt; last=$m; echo "$(date +%H:%M:%S) synced $(wc -l < $F) rows" >> $N/logs/sync_$TAG.log; fi; fi
  pgrep -f "tag=$TAG " > /dev/null || { sleep 90; [ -s $F ] && cp $F $D/rows_$TAG.txt; echo "$(date +%H:%M:%S) run gone, final sync, exit" >> $N/logs/sync_$TAG.log; exit 0; }
  sleep 60
done
