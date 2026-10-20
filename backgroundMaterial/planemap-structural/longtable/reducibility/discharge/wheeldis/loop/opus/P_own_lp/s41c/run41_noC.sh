# s41c step 1-3: upper on sol_q39n3A74 with ALL C out (noC noCw + D-only kill6/l3q tables of prep_noC_A74.sh, s41c/noC),
# every violated receiver row to the vfile (vK=1e12); then ccover41.py (covers per row, sole set, greedy).
. $(dirname $0)/env.sh; cd $E
until [ -e $O/noC/prep_done.txt ]; do sleep 30; done
a=$(df -BG --output=avail $SC | tail -1 | tr -dc 0-9); [ "$a" -gt 10 ] || { echo "df ${a}G" > $O/run41_noC.err; exit 5; }
VF=$SC/s41c_vrows_A74.txt; : > $VF
echo "$(date -u +%H:%M:%SZ) noC upper start" >> $O/s41c.log
timeout 14400 nice -n 10 python3 pcheck.py upperR2 $(fq $O/noC) $X noC noCw nomax vK=1e12 vfile=$VF sol=$SOL $A threads=1 work=$SC/P/wr41c_nc > $O/upper_noC.log 2>&1 || echo "upper exit $?" >> $O/upper_noC.log
{ wc -l < $VF; md5sum $VF; } > $O/vrows_count.txt
echo "$(date -u +%H:%M:%SZ) noC upper: $(grep UPPER-R2 $O/upper_noC.log) ; vrows $(head -1 $O/vrows_count.txt)" >> $O/s41c.log
nice -n 10 python3 -I $O/ccover41.py $VF $Q/args_A74.txt $M $S/m89/CGLUE-XRING-ENTRIES_27964810.txt $O/cc $O/lean_CXRing_entries.txt,$O/lean_CXInt_entries.txt > $O/ccover41.log 2>&1
echo "$(date -u +%H:%M:%SZ) ccover: $(grep -E '^sole-cover set' $O/cc/ccover_summary.txt)" >> $O/s41c.log
rm -rf $SC/P/wr41c_nc; echo DONE > $O/run41_noC.done
