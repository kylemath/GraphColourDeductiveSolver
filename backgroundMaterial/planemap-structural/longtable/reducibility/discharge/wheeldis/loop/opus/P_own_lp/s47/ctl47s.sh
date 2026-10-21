# s47 smoke solve (s1): solveR2 l3qV=7,8 (full reg_A78 V = 8 table), warm = the first 3000 rows of s42a's rows_q42aA78.txt,
# 3 LP rounds (2 separation rounds at d = 7..17 through jsep7 at d = 7, 8), then lowerR2 on its cert.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s47/env47.sh
TV=$D/tabV8_A78; CB=consbasis=$B/s21/cf/cons2basis_cls.json
until [ -e $D/ctl47f.done ]; do sleep 20; done
V8F="l3qV=7,8 l3qtab8=$TV/tabV8_1.json,$TV/tabV8_-1.json"; O=$D/ctl_s1; cd $E
head -3000 $B/s42a/run_A78/rows_q42aA78.txt > $O/warm3000.txt; note "smoke solve s1 start"
nice -n 10 python3 pcheck.py solveR2 $FQ $X $V8F tag=s47s1 $A $CB warm=$O/warm3000.txt K=300 xcap=3 maxit=3 threads=1 work=$SC/P/wr47_s1 > $O/solve.log 2>&1
mv sol_s47s1.json cert_s47s1.json rows_s47s1.txt $O/
nice -n 10 python3 pcheck.py lowerR2 $FQ $X $V8F cert=$O/cert_s47s1.json xcap=3 $A work=$SC/P/wr47_s1 > $O/lower.log 2>&1
python3 -c "
import json; S = json.load(open('$O/sol_s47s1.json')); C = json.load(open('$O/cert_s47s1.json'))
print('sol: V = 8 lq > 0:', [k for k in S['lq'] if len(k[0]) == 4], '; V = 8 lQ > 0:', [k for k in S['lQ'] if len(k[0]) == 4])
print('cert: V = 8 mrowL rows', sum(1 for c in C if c['row'][0] == 'mrowL' and len(c['row'][1]) == 4), 'of', sum(1 for c in C if c['row'][0] == 'mrowL'))" > $O/v8summary.txt
note "smoke s1: $(grep '^iter' $O/solve.log | tail -1 | cut -c1-70) | $(grep LOWER-R2 $O/lower.log | tail -1) | $(head -1 $O/v8summary.txt | cut -c1-120)"
echo DONE > $D/ctl47s.done
