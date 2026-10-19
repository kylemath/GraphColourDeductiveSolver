#!/bin/bash
# usage: round.sh K WARMLIST FORBIDFILE TLIMIT_S
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s27o/env.sh
cd $S; k=$1; WARM=$2; FB=forbid=$3; TL=$4; tag=r$k
date -u +%H:%M:%SZ > ${tag}_start.txt
# quick lower bound: previous rows only, forbidden ones removed by admissible()
( python3 pcheck.py solveR2 $F0 nosep tag=${tag}pre $A $CB $FB warm=$WARM K=300 xcap=3 dcap=3 threads=1 work=$WK/${tag}pre > ${tag}pre.log 2>&1
  python3 pcheck.py lowerR2 $F0 $FB cert=cert_${tag}pre.json xcap=3 dcap=3 $A work=$WK/${tag}pre > lower_${tag}pre.log 2>&1 ) &
PRE=$!
python3 pcheck.py solveR2 $F0 keeppen tag=$tag $A $CB $FB warm=$WARM K=300 xcap=3 xpen=1e-3 dcap=3 dpen=1e-3 threads=4 tlimit=$TL work=$WK/$tag > $tag.log 2>&1 || echo "solve exit $?" >> $tag.log
date -u +%H:%M:%SZ > ${tag}_end.txt
python3 pcheck.py solveR2 $F0 nosep tag=${tag}L $A $CB $FB warm=rows_$tag.txt,$WARM K=300 xcap=3 dcap=3 threads=4 work=$WK/${tag}L > ${tag}L.log 2>&1
python3 pcheck.py lowerR2 $F0 $FB cert=cert_${tag}L.json xcap=3 dcap=3 $A work=$WK/${tag}L > lower_${tag}L.log 2>&1
( python3 pcheck.py upperR2 $F0 $FB nomax sol=sol_$tag.json dcap=3 $A threads=4 work=$WK/${tag}u > upper_$tag.log 2>&1; date -u +%H:%M:%SZ > ${tag}_udone.txt ) > /dev/null 2>&1 &
date -u +%H:%M:%SZ > ${tag}_Ldone.txt
wait $PRE
