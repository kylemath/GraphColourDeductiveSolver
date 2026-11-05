# s78 test 4 (method of s75_teamA/symchk): jsepf at d = 7 with rotation symmetry on (argv[4] = 1) and off (0), mode 0, K = 200000,
# threshold lowered by LOWER (default 0.003), on the tables of a KEEPWK upper78 run (default: t5_plant_in09 = in09 + K1 0.125, K* firing).
# usage: bash symchk78.sh [workdir] [lower] [K, default 200000: must exceed the nosym row count]   -> logs/symchk/out7_{sym,nosym}.txt, err7_*.txt, cmp_result.txt
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar
WK=${1:-/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sD/wr78u_t5_plant_in09}; LOW=${2:-0.003}; KK=${3:-200000}; O=$N/logs/symchk; mkdir -p $O; cd $O
H=$WK/hdr_7_m0.txt; [ -s $H ] || { echo "no $H"; exit 2; }
read d thr K mode < <(head -1 $H)
nt=$(python3 -c "print('%.15f' % ($thr - $LOW))")
{ echo "7 $nt $KK 0"; tail -n +2 $H; } > $O/hdr_7_sym.txt
BON=$( [ -s $WK/bonus7.txt ] && echo $WK/bonus7.txt || echo none ); Q7M=$( [ -s $WK/q7m_d7.bin ] && echo $WK/q7m_d7.bin || echo none ); L8=$( [ -s $WK/l3q8.bin ] && echo $WK/l3q8.bin || echo none )
KSF=$( [ -s $WK/kstar_d7.bin ] && echo $WK/kstar_d7.bin || echo none ); EGF=$( [ -s $WK/edge_d7.bin ] && echo $WK/edge_d7.bin || echo none )
echo "thr $thr -> $nt; edge $EGF; bonus $BON q7m $Q7M l3q8 $L8 kstar $WK/kstar_d7.bin" > $O/args.txt
for sy in 1 0; do
  m=$([ $sy = 1 ] && echo sym || echo nosym)
  T0=$SECONDS; nice -n 15 $N/eng/bin/jsepf $O/hdr_7_sym.txt $WK/win_d7.bin 1 $sy none $BON $WK/l3q.bin none $L8 $WK/f2b_d7.bin none $Q7M $KSF $EGF > $O/out7_$m.txt 2> $O/err7_$m.txt; echo "exit $? $((SECONDS - T0)) s" >> $O/err7_$m.txt
  echo "$m: $(tail -1 $O/out7_$m.txt) $(grep -v '^P tasks' $O/err7_$m.txt | tr '\n' ' ')" >> $O/args.txt
done
python3 - <<'EOF' > $O/cmp_result.txt
import collections
def canon(w, s):
    d = len(w); P = list(zip(w, s)); return min(tuple(P[k:] + P[:k]) for k in range(d))
res = {}
for m in ('sym', 'nosym'):
    L = [l.split() for l in open('out7_%s.txt' % m) if l.startswith('V ')]
    D = {}
    for _, tot, w, s in L: D.setdefault(canon(w, s), set()).add(round(float(tot), 9))
    end = [l.strip() for l in open('out7_%s.txt' % m) if l.startswith('END')]
    errs = [l.strip() for l in open('err7_%s.txt' % m) if not l.startswith('P tasks')]
    res[m] = D; print('d=7 %s: %d rows, %d classes, totals consistent per class: %s, %s, %s' % (m, len(L), len(D), all(len(v) == 1 for v in D.values()), end[0] if end else 'NO END', errs))
a, b = set(res['sym']), set(res['nosym'])
ok = (a == b) and all(res['sym'][k] == res['nosym'][k] for k in a) and len(a) > 0
print('d=7 classes only in sym %d, only in nosym %d, totals equal on common: %s' % (len(a - b), len(b - a), all(res['sym'][k] == res['nosym'][k] for k in a & b)))
print('SYM-TEST: %s' % ('PASS' if ok else 'FAIL'))
EOF
cat $O/cmp_result.txt
