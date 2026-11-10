# s86 9 Nov 20:12Z: K3l5n (= K3l5m + P09 D f9_555557557_.....676.) kills the 3 ST-89 d9 top-binder labels in our engine (rowR2
# admissible= names the killer); control: the first label on K3l5m (not killed).  Through T86.sh (gated, FIFO), sol = ST-89 in08.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export E86OVR=$N/eng_p8 STACK=s77 KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt T86CMD=rowR2; SOL=$N/cand/sol_k86MK1_in08__K3l5j_k260.json
ARGS=$N/args_A97_F_W13K3l5m.txt bash $N/T86.sh k5nCTL $SOL 1 $XF d=9 lk=555557557 sv=588586768
for L in 555557557:588586768 555575575:885867685 555755755:858676858; do
  ARGS=$N/args_A97_F_W13K3l5n.txt bash $N/T86.sh k5n_${L%%:*} $SOL 1 $XF d=9 lk=${L%%:*} sv=${L##*:}
done
for f in k5nCTL k5n_555557557 k5n_555575575 k5n_555755755; do echo "$f: $(grep -o 'row d=9.*' $N/logs/t86_$f.log | cut -c1-200)"; done > $N/p8test/k5n_rows.out
echo "$(date -u +%H:%M:%SZ) [s86P8] K3l5n label test done: $(grep -c 'admissible=None' $N/p8test/k5n_rows.out) of 4 rows admissible=None (control should be the only one)" >> $N/run.log
