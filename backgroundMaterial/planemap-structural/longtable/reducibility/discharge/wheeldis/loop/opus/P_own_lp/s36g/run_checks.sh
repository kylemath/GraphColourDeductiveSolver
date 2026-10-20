# s36g prototype checks (PRIVCELL_SPEC.md part 4). threads=1, no solve.  bash run_checks.sh
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SW=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s36g_work; mkdir -p $SW; echo '# empty' > $SW/empty.txt
S=$B/s36g; cd $S/eng
A="root=$M args=$B/s25/argsA59.txt rpat=$B/rpatD.txt threads=1 work=$SW"; F0="xon apexcls filt16 killtab=$B/s25/f/kill/kill6 hat5 consall"
# 1. amask over all 3 x 5^8 entries: with the q-names vs the s25c g7 flag formula; without names vs the plain table
(nice python3 pcheck.py pcellcheck $F0 g7ref pcell=$S/g7_q.txt $A; nice python3 pcheck.py pcellcheck $F0 $A) > $S/pcellcheck.log 2>&1
# 2. lowerR2 on cert_st24bL: names / no option / empty file
nice python3 pcheck.py lowerR2 $F0 pcell=$S/g7_q.txt cert=$B/s24d/cert_st24bL.json xcap=3 $A > $S/lower_st24bL_pcell.log 2>&1
nice python3 pcheck.py lowerR2 $F0 cert=$B/s24d/cert_st24bL.json xcap=3 $A > $S/lower_st24bL_off.log 2>&1
nice python3 pcheck.py lowerR2 $F0 pcell=$SW/empty.txt cert=$B/s24d/cert_st24bL.json xcap=3 $A > $S/lower_st24bL_empty.log 2>&1
# 3. l3q flag (s28q A60 setup, cert_s28A60L): no option / empty file / names
A6="root=$M args=$B/s29/argsA60.txt rpat=$B/rpatD.txt threads=1 work=$SW"; F="xon apexcls filt16 killtab=$B/s29/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab60_1.json,$B/s28q/tab60_-1.json lqcap=3"
nice python3 pcheck.py lowerR2 $F cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A6 > $S/lower_s28A60L_off.log 2>&1
nice python3 pcheck.py lowerR2 $F pcell=$SW/empty.txt cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A6 > $S/lower_s28A60L_empty.log 2>&1
nice python3 pcheck.py lowerR2 $F pcell=$S/g7_q.txt cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A6 > $S/lower_s28A60L_pcell.log 2>&1
