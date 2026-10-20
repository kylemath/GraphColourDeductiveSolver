# e87 re-pricing against the stacked cert (coordinator/Long Table: price first, re-solve only if some key prices < 0 with projected
# gain >= 0.002; K2 relief on 8666655 is the one that matters). Waits for the main L stage (run_TAG/L.done), threads=1.
# Masks: s38e mask38.py copy (mask38s.py) on the cert's d = 7 receiver rows with a letter >= 8, registry TAG (ex_TAG + k3x_TAG).
# Pricer: s38e pricer38.py copy (pricer38s.py) on the s33z engine with the main stacked flags (+ pcell k3p #1).
TAG=${1:-A67}
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; Q=$S/reg_$TAG; RD=$S/run_$TAG; O=$S/e87/$TAG; mkdir -p $O
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
until [ -e $RD/L.done ]; do sleep 60; done
export OMP_NUM_THREADS=1
python3 -c "
import json; C=json.load(open('$RD/cert_s33L.json'))
rs=sorted({'%d/%s/%s'%(r['row'][1],r['row'][2],r['row'][3]) for r in C if r['row'][0]=='receiverR2' and r['row'][1]==7 and max(r['row'][2])>='8'})
open('$O/mask_rows.txt','w').write(' '.join(rs)); print(len(rs))" > $O/mask_rows_count.txt
EX=$SC/ex_$TAG TD=$Q/k3x_D_$TAG.out TC=$Q/k3x_C_$TAG.cfast nice -n 5 python3 $S/e87/mask38s.py $O/masks38.json $(cat $O/mask_rows.txt) > $O/mask38.log 2>&1
TARGET=$(grep -o "t >= [0-9/]*" $RD/lower_s33L.log | head -1 | cut -c6-)
ENGARGS="root=$M args=$Q/args_$TAG.txt rpat=$B/rpatD.txt xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt xcap=3 work=$SC/P/wr_${TAG}e87" \
CERT=$RD/cert_s33L.json TARGET=$TARGET OUTDIR=$O nice -n 5 python3 $S/e87/pricer38s.py > $O/pricer.out 2>&1
echo "$(date -u +%H:%M:%SZ) [$TAG] e87 pricing done: $(grep -c . $O/pricer38.log) lines" >> $S/wait.log
echo DONE > $O/done.txt
