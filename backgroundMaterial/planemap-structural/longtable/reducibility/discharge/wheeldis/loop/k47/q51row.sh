# Round 51: one binder row (ring <= 14, then 15-16 only if no kill), as a task that fits the 2-hour limit.
# usage: sh q51row.sh RINGS D LK SV PREFIX [D LK SV PREFIX ...]   -> touches R51_<PREFIX>.DONE per row
# RINGS = "14 16" (full kill line) or "14" (face rows, Long Table 07:02Z: ring <= 14 only)
cd "$(dirname "$0")"
row() {   # D LK SV PREFIX
  for R in $RINGS; do
    W=win45_$1_$2_$3_A$R.txt
    [ -f $W ] || python3 win45.py $R $1 $2 $3
    python3 - $W <<'PY'
import sys
w = [l.split()[0] for l in open(sys.argv[1]) if l.strip()]
done = {l.split()[0] for l in open('A_kcc.out') if l[:1] == 'a'}; k = {l.split()[0] for l in open('KILL')}
print('%s: %d windows, %d already run, %d already two-engine kills' % (sys.argv[1], len(w), sum(x in done for x in w), sum(x in k for x in w)))
PY
    date -u +%H:%MZ
    STOP=0 NW=3 python3 drive45.py $W 600 > drive51_$4_$R.log 2>&1
    python3 minkill47.py $W $2 $4; date -u +%H:%MZ; cat $4_kills_min.txt
    [ -s $4_kills.txt ] && break
  done
}
RINGS=$1; shift
while [ $# -ge 4 ]; do row $1 $2 $3 $4; touch R51_$4.DONE; shift 4; done
grep -c MISMATCH A_df.out A_cf.out KILL
