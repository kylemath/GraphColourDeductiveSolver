# s86 v2r copy of p1r/bindwatch86.sh (binding86v.py counts receiverV2 rows too).  For every dual export lext_<tag>/dual_rows_<tag>_p1_NN.json (written by dualwatch86p), write BINDING_<tag>_p1_NN.txt (binding86.py, top 80)
# and MROWS_<tag>_p1_NN.txt (mrowsum.py) and copy both to from_opus/s86_<tag>/ (Lead ask 8 Nov 03:59Z: every phase-1 cert, not only p1_00).
# usage: bash bindwatch86.sh <tag>
Z=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; TAG=$1
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_$TAG; mkdir -p $O
while true; do
  for D in $(ls $Z/lext_$TAG/dual_rows_${TAG}_p1_[0-9][0-9].json 2>/dev/null); do
    n=$(basename $D .json); n=${n##*_p1_}; Bf=$Z/lext_$TAG/BINDING_${TAG}_p1_$n.txt; Mf=$Z/lext_$TAG/MROWS_${TAG}_p1_$n.txt
    [ -s $Bf ] && continue
    grep -q '"stamp"' $D || continue   # dualwatch stamps the JSON last; wait for it
    python3 -I $Z/v2r/binding86v.py $D 80 > $Bf.tmp 2>&1 && mv $Bf.tmp $Bf
    python3 -I $Z/mrowsum.py $D 25 > $Mf 2>&1
    cp $Bf $Mf $O/; (cd $O && md5sum $(ls | grep -v MD5SUMS) > MD5SUMS)
    echo "$(date -u +%H:%M:%SZ) [s86DX-$TAG] p1_$n: BINDING + MROWS -> from_opus/s86_$TAG ($(sed -n 3p $Bf | cut -c3-90))" >> $Z/run.log
  done
  pgrep -f "tag=$TAG " > /dev/null || pgrep -f "dualwatch86v.sh $TAG" > /dev/null || exit 0
  sleep 60
done
