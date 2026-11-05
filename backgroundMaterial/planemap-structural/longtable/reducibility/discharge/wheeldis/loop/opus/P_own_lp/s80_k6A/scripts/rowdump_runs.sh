# s80 Team E: test (a) row coefficients eng_orig vs eng (no f2bx) and the f2bx row changes (sample + B3 target rows), 1 process, nice 15
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s80_k6A
FAM=full; . $N/env80.sh; WK=$S8/wr80_rowdump; mkdir -p $WK $N/tests/out; O=$N/tests/out; SOL=$N/sol_b77F_in02.json
R() { nice -n 15 python3 $N/scripts/rowdump.py "$@"; }
R $N/eng_orig $N/tests/rows_sample1000.txt $O/s1000_orig.jsonl sol=$SOL -- $F $X $A work=$WK
R $N/eng $N/tests/rows_sample1000.txt $O/s1000_eng.jsonl sol=$SOL -- $F $X $A work=$WK
python3 $N/scripts/rowcmp.py $O/s1000_orig.jsonl $O/s1000_eng.jsonl
R $N/eng $N/tests/rows_sample1000.txt $O/s1000_f2bx.jsonl sol=$SOL -- $F $X $A work=$WK f2bx=$N/rules/rules_ApLp.json
python3 $N/scripts/rowcmp.py $O/s1000_f2bx.jsonl
R $N/eng $N/tests/rows_B3targets.txt $O/b3t_f2bx.jsonl sol=$SOL -- $F $X $A work=$WK f2bx=$N/rules/rules_ApLp.json
python3 $N/scripts/rowcmp.py $O/b3t_f2bx.jsonl
