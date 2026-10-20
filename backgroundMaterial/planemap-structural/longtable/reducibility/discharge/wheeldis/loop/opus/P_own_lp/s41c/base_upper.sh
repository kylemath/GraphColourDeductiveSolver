# control: the s39o n3 A74 upper re-run unchanged (no new options) -> must match run_n3_A74/upper.log apart from timings
. $(dirname $0)/env.sh; cd $E
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$SOL $A threads=1 work=$SC/P/wr41c_base > $O/upper_base.log 2>&1
sed 's/([^)]*s)//' $O/upper_base.log > $SC/b1.txt; sed 's/([^)]*s)//' $RD/upper.log > $SC/b2.txt
cmp $SC/b1.txt $SC/b2.txt && echo "CONTROL: identical to run_n3_A74/upper.log (timings stripped)" > $O/upper_base_cmp.txt || diff $SC/b1.txt $SC/b2.txt > $O/upper_base_cmp.txt
rm -rf $SC/P/wr41c_base
