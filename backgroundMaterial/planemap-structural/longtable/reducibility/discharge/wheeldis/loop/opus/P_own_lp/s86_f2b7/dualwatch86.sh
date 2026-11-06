# s86: for every phase-1 cert lext_<tag>/cert_p1_NN_<md5>.json (copied there by watchL86s), run dualexport with the run's flags ($XF, $KEYS,
# $ARGS) and dualsplit, then copy cert + dual_rows + dual_split to from_opus/s86_<tag>/ (for swarm pricing; the exact VALID cert follows from
# watchL86s).  usage: [STACK ARGS KEYS XF] bash dualwatch86.sh <tag>
Z=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; S85=$Z/../s85_edge56; TAG=$1
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_$TAG; mkdir -p $O
while true; do
  for c in $(ls $Z/lext_$TAG/cert_p1_[0-9][0-9]_*.json 2>/dev/null | grep -v _exb); do
    b=$(basename $c .json); n=${b#cert_p1_}; n=${n%%_*}; D=$Z/lext_$TAG/dual_rows_${TAG}_p1_$n.json
    [ -e $D ] && continue
    PYTHONINTMAXSTRDIGITS=0 bash $Z/wtest86.sh dx_${TAG}_p1_$n dualexport cert=$c out=$D gkeys=$KEYS gkwin gkleaf $XF
    python3 -I $S85/dualsplit.py $c 30 > $Z/lext_$TAG/dual_split_${TAG}_p1_$n.txt 2>&1
    cp $c $D $Z/lext_$TAG/dual_split_${TAG}_p1_$n.txt $O/; (cd $O && md5sum $(ls | grep -v MD5SUMS) > MD5SUMS)
    echo "$(date -u +%H:%M:%SZ) [s86DX-$TAG] $(basename $c): dual export + split -> from_opus/s86_$TAG ($(grep -o 'DUALEXPORT: [0-9]* rows' $Z/logs/dx_${TAG}_p1_$n.log))" >> $Z/run.log
  done
  pgrep -f "tag=$TAG " > /dev/null || { sleep 300; [ -z "$(ls $Z/lext_$TAG/cert_p1_*.json 2>/dev/null | grep -v _exb | while read c; do b=$(basename $c .json); n=${b#cert_p1_}; n=${n%%_*}; [ -e $Z/lext_$TAG/dual_rows_${TAG}_p1_$n.json ] || echo x; done)" ] && exit 0; }
  sleep 120
done
