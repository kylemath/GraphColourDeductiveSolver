# s86 p1r copy of ../watchL86s.sh: the run writes its phase-1 cert in eng_p1r (ENG), and lowerR2 runs on eng_p1r (p1r/wtest86p.sh).
# s86 (f2b7 engine; watchL86s = watchL86 with the run's $XF flags, so f2b= overrides reach lowerR2): when a lext run writes (or rewrites) eng/cert_<tag>_p1.json (phase-1 cert, t1 > 0), check it: lowerR2 exactbasis (exbmu=0 exbtol=1e-10),
# then norepair recheck of the exact cert (both inside lowerR2); copy VALID certs to from_opus/s85_<tag>/.  usage: [STACK ARGS KEYS] bash watchL85.sh <tag>
Z=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; TAG=$1; ENG=$Z/eng_p1r
O=/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_$TAG; mkdir -p $O $Z/lext_$TAG; last=""
while true; do
  f=$ENG/cert_${TAG}_p1.json
  if [ -s $f ]; then
    m=$(md5sum $f | cut -c1-8)
    if [ "$m" != "$last" ]; then
      last=$m; n=$(ls $Z/lext_$TAG | grep -c '^cert_p1_' ); c=$Z/lext_$TAG/cert_p1_$(printf %02d $n)_$m.json; cp $f $c; cp $ENG/sol_${TAG}_p1.json $Z/lext_$TAG/sol_p1_$(printf %02d $n)_$m.json 2>/dev/null
      echo "$(date -u +%H:%M:%SZ) [s86LX-$TAG] phase-1 cert $(basename $c) -> lowerR2 exactbasis" >> $Z/run.log
      PYTHONINTMAXSTRDIGITS=0 bash $Z/p1r/wtest86p.sh lx_${TAG}_$n lowerR2 cert=$c xcap=3 gkeys=$KEYS gkwin gkleaf $XF exactbasis exbmu=0 exbtol=1e-10
      L=$Z/logs/lx_${TAG}_$n.log; v=$(grep LOWER-R2 $L | tail -1 | cut -c1-200)
      echo "$(date -u +%H:%M:%SZ) [s86LX-$TAG] $(basename $c): $v" >> $Z/run.log
      if echo "$v" | grep -q VALID && ! echo "$v" | grep -q INVALID; then cp ${c%.json}_exb.json $L $O/ 2>/dev/null; (cd $O && md5sum $(ls | grep -v MD5SUMS) > MD5SUMS); fi
    fi
  fi
  pgrep -f "tag=$TAG " > /dev/null || { sleep 30; exit 0; }
  sleep 120
done
