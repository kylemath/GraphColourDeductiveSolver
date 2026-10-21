# control: the s44 A83 upper (run44c.sh U stage) re-run unchanged (no new options) on the s52c engine copy -> must match s44/run_A83/upper.log apart from timings
. $(dirname $0)/env.sh; cd $E
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$SOL $A threads=1 work=$SC/P/wr52c_base > $O/upper_base.log 2>&1
sed 's/([^)]*s)//' $O/upper_base.log > $SC/s52c_b1.txt; sed 's/([^)]*s)//' $RD/upper.log > $SC/s52c_b2.txt
cmp $SC/s52c_b1.txt $SC/s52c_b2.txt && echo "CONTROL: identical to s44/run_A83/upper.log (timings stripped)" > $O/upper_base_cmp.txt || diff $SC/s52c_b1.txt $SC/s52c_b2.txt > $O/upper_base_cmp.txt
echo "$(date -u +%H:%M:%SZ) [base] control upper: $(grep UPPER-R2 $O/upper_base.log); $(head -1 $O/upper_base_cmp.txt)" >> $O/s52c.log
rm -rf $SC/P/wr52c_base $SC/s52c_b1.txt $SC/s52c_b2.txt
