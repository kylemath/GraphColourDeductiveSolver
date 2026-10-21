# control: the s53 early A97 upper (s53/u53.sh) re-run unchanged (no new options) on the s53c engine copy -> must match s53/run_A97/upper_early.log apart from timings
. $(dirname $0)/env.sh; cd $E
until grep -q UPPER-R2 $RD/upper_early.log 2>/dev/null; do sleep 30; done
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$SOL $A threads=1 work=$SC/P/wr53c_base > $O/upper_base.log 2>&1
sed 's/([^)]*s)//' $O/upper_base.log > $SC/s53c_b1.txt; sed 's/([^)]*s)//' $RD/upper_early.log > $SC/s53c_b2.txt
cmp $SC/s53c_b1.txt $SC/s53c_b2.txt && echo "CONTROL: identical to s53/run_A97/upper_early.log (timings stripped)" > $O/upper_base_cmp.txt || diff $SC/s53c_b1.txt $SC/s53c_b2.txt > $O/upper_base_cmp.txt
echo "$(date -u +%H:%M:%SZ) [base] control upper: $(grep UPPER-R2 $O/upper_base.log); $(head -1 $O/upper_base_cmp.txt)" >> $O/s53c.log
rm -rf $SC/P/wr53c_base $SC/s53c_b1.txt $SC/s53c_b2.txt; echo DONE > $O/base.done
