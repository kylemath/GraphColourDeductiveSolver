# s86: file every upperR2-FEASIBLE k85B in-point (cand/ + logs/upper_*.log) into from_opus/s85_<tag>/ with POINTS.txt (t, md5, NEG6) and MD5SUMS
Z=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
TAG=${1:-k85B}; O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_$TAG; mkdir -p $O
while true; do
  for f in $Z/cand/sol_${TAG}_in[0-9][0-9].json; do
    b=$(basename $f .json); L=$Z/logs/upper_$b.log
    [ -e $O/$b.json ] && continue; [ -e $L ] || continue
    grep -q "^UPPER-R2: FEASIBLE" $L || continue
    t=$(grep -o "^UPPER-R2: FEASIBLE at t = [0-9.]*" $L | awk '{print $NF}'); m=$(md5sum $f | cut -c1-8)
    N=$(grep -h "some 6 ends below" $L | sed 's/.*below 0: \([0-9]*\) (lowest in - out \([-0-9.e]*\)).*/\1 (\2)/')
    cp $f $L $O/; echo "$b    $t    $m  $N" >> $O/POINTS.txt
    (cd $O && md5sum $(ls | grep -v MD5SUMS) > MD5SUMS)
    echo "$(date -u +%H:%M:%SZ) [s86F-$b] filed to from_opus/s86_$TAG (t = $t, md5 $m, NEG6 $N)" >> $Z/run.log
  done
  sleep 120
done
