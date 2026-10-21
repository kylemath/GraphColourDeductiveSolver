# control: the s42a A78 upper re-run unchanged (no new options) on the s46c engine copy -> must match s42a/run_A78/upper.log apart from timings
. $(dirname $0)/env.sh; cd $E
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$SOL $A threads=1 work=$SC/P/wr46c_base > $O/upper_base.log 2>&1
sed 's/([^)]*s)//' $O/upper_base.log > $SC/s46c_b1.txt; sed 's/([^)]*s)//' $RD/upper.log > $SC/s46c_b2.txt
cmp $SC/s46c_b1.txt $SC/s46c_b2.txt && echo "CONTROL: identical to s42a/run_A78/upper.log (timings stripped)" > $O/upper_base_cmp.txt || diff $SC/s46c_b1.txt $SC/s46c_b2.txt > $O/upper_base_cmp.txt
echo "$(date -u +%H:%M:%SZ) [base] control upper: $(grep UPPER-R2 $O/upper_base.log); $(head -1 $O/upper_base_cmp.txt)" >> $O/s46c.log
rm -rf $SC/P/wr46c_base $SC/s46c_b1.txt $SC/s46c_b2.txt
