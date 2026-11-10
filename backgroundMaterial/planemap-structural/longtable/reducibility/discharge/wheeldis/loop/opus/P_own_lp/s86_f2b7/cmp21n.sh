#!/bin/bash
# s86 cmp21n.sh (10 Nov 09:15Z, Lead 09:05Z "comparable rows"): the HATBB gate's control.  After GS21 ends iteration 1 (its 2nd gate
# iteration), stop GS21 (rows + in-point snapshotted by rowsnap / file86), then run k86GS21n = GS21's exact setup WITHOUT hatbb on GS21's
# iteration-1 LP rows (GS21 warm + warm/rows_k86GS21_snap_it1LP.txt = GS21's 337 iteration-0 rows), same FEAS (GS20 in03), same engine
# (eng_p8h, HBON off = eng_p8 code).  Its iteration-0 LP t (B) vs GS21's iteration-1 LP t (A): keep HATBB iff A <= B - 1.5e-4.
# k86GS21n is stopped as soon as its "q7rc it 0: t=" line is out (only the LP value is needed).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
L=$N/run.log; K=$N/runK_k86GS21/K.log
until grep -q '^iter 1 t=' $K; do pgrep -f 'pcheck.py solveR2.*tag=k86GS2[1] ' > /dev/null || { echo "$(date -u +%H:%M:%SZ) [s86C21] GS21 gone before iter 1 end; no control run" >> $L; exit 1; }; sleep 30; done
A=$(grep -o 'q7rc it 1: t=[0-9.]*' $K | tail -1 | cut -d= -f2)
sleep 60   # let file86 / rowsnap pick up the iteration-1 point and rows
cp $N/eng_p8h/rows_k86GS21.txt $N/warm/rows_k86GS21_snap_it2.txt
PID=$(pgrep -f 'pcheck.py solveR2.*tag=k86GS2[1] '); RP=$(pgrep -f 'runK86p8h.sh 200 2 k86GS21 ')
[ -n "$PID" ] && kill $PID; [ -n "$RP" ] && kill $RP
echo "$(date -u +%H:%M:%SZ) [s86C21] GS21 stopped after iter 1 (gate LP t A = $A; $(grep '^iter 1 t=' $K | cut -c1-120)); starting k86GS21n control (no hatbb, GS21 iteration-1 rows)" >> $L
sleep 20
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt FEAS=$N/cand/sol_k86GS20_in03.json
export XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export WARM=$(cat $N/runK_k86GS20/warmlist.txt),$N/warm/rows_k86GS20_snap_GS21.txt,$N/warm/rows_k86GS21_snap_it1LP.txt
T=k86GS21n
cd $N && nohup bash $N/p1r/runK86p8h.sh 200 2 $T inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25 lpdual warmcache=$N/warmcache > $N/logs/runK_$T.out 2>&1 &
until grep -q 'q7rc it 0: t=' $N/runK_$T/K.log 2>/dev/null; do pgrep -f "pcheck.py solveR2.*tag=k86GS21[n] " > /dev/null || [ $(( $(date +%s) - $(stat -c %Y $N/logs/runK_$T.out) )) -lt 600 ] || { echo "$(date -u +%H:%M:%SZ) [s86C21] k86GS21n died before its LP" >> $L; exit 2; }; sleep 30; done
B=$(grep -o 'q7rc it 0: t=[0-9.]*' $N/runK_$T/K.log | head -1 | cut -d= -f2)
PID=$(pgrep -f 'pcheck.py solveR2.*tag=k86GS21[n] '); RP=$(pgrep -f "runK86p8h.sh 200 2 $T ")
[ -n "$PID" ] && kill $PID; [ -n "$RP" ] && kill $RP
V=$(python3 -c "import sys; a, b = float(sys.argv[1]), float(sys.argv[2]); print('KEEP' if a <= b - 1.5e-4 else 'DROP', '%.3e' % (b - a))" $A $B)
echo "$(date -u +%H:%M:%SZ) [s86C21] HATBB GATE: A (GS21 it-1 LP, with HATBB) = $A, B (same rows, no HATBB) = $B, B - A = ${V#* } -> ${V%% *}" >> $L
