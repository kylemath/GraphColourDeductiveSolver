# s31: st24b-engine re-solve on Studio head 3cfd7f18 (argsA62, kill tables s31/f/kill). Recipe = s24d/cmd_st24r.sh run1
# (as s30h/cmd_resolve7a.sh): keeppen solve (cap 3 h), nosep L solve (cap 3 h), lowerR2, upperR2. Warm st24b_final + rows_s29.
# CPU gate (Long Table): before each stage, if the l3q solve (pcheck ... s28A60) runs: threads=1 when load1 < 4, else wait
# (5-min checks, bounded at 288 = 24 h); once l3q is gone: threads=2.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Q=$P/s31; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
A="root=$M args=$Q/argsA62.txt rpat=$P/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall"
CB=consbasis=$P/s21/cf/cons2basis_cls.json
WARM=$P/s24d/rows_st24b_final.txt,$P/s29/rows_s29.txt
tag=s31
gate(){ for i in $(seq 1 288); do
    if [ -f $P/s28q/done_s28A60.txt ] || { ! pgrep -f 'pcheck.py .*s28A60' > /dev/null && sleep 90 && ! pgrep -f 'pcheck.py .*s28A60' > /dev/null; }; then TH=2; echo "$(date -u +%H:%M:%SZ) gate $1: l3q gone, threads=2" >> gate.log; return; fi
    L1=$(cut -d' ' -f1 /proc/loadavg)
    if awk -v l=$L1 'BEGIN{exit !(l < 4)}'; then TH=1; echo "$(date -u +%H:%M:%SZ) gate $1: l3q running, load $L1, threads=1" >> gate.log; return; fi
    echo "$(date -u +%H:%M:%SZ) gate $1: l3q running, load $L1, wait" >> gate.log; sleep 300; done
  echo "gate $1 timed out" >> gate.log; exit 1; }
gate solve
date -u +%H:%M:%SZ > ${tag}_start.txt
timeout 10800 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 dcap=3 dpen=1e-3 threads=$TH work=$S/P/wr31_$tag > $tag.log 2>&1 || echo "solve exit $?" >> $tag.log
date -u +%H:%M:%SZ > ${tag}_end.txt
gate L
timeout 10800 python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 dcap=3 threads=$TH work=$S/P/wr31_${tag}L > ${tag}L.log 2>&1 || echo "solve exit $?" >> ${tag}L.log
date -u +%H:%M:%SZ > ${tag}L_end.txt
python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 dcap=3 $A work=$S/P/wr31_${tag}L > lower_${tag}L.log 2>&1
gate upper
python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json dcap=3 $A threads=$TH work=$S/P/wr31_${tag}u > upper_$tag.log 2>&1
md5sum sol_$tag.json sol_${tag}L.json cert_${tag}L.json rows_$tag.txt rows_${tag}L.txt > md5_out.txt 2>&1
echo DONE > done.txt
