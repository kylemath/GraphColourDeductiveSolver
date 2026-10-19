# Round 51 part 1: the binder's two 7-sender rows, ring <= 14 first, ring 15-16 only if no kill.  3 workers.
cd "$(dirname "$0")"
row() {   # LK SV PREFIX
  for R in 14 16; do
    W=win45_7_$1_$2_A$R.txt
    [ -f $W ] || python3 win45.py $R 7 $1 $2
    python3 - $W <<'PY'
import sys
w = [l.split()[0] for l in open(sys.argv[1]) if l.strip()]
done = {l.split()[0] for l in open('A_kcc.out') if l[:1] == 'a'}; k = {l.split()[0] for l in open('KILL')}
print('%s: %d windows, %d already run, %d already two-engine kills' % (sys.argv[1], len(w), sum(x in done for x in w), sum(x in k for x in w)))
PY
    date -u +%H:%MZ
    STOP=0 NW=3 python3 drive45.py $W 600 > drive51_$3_$R.log 2>&1
    python3 minkill47.py $W $1 $3; date -u +%H:%MZ; cat $3_kills_min.txt
    [ -s $3_kills.txt ] && break
  done
}
row 7665666 6566565 r7e; touch R51A.DONE
row 7655666 6756666 r7f; touch R51B.DONE
grep -c MISMATCH A_df.out A_cf.out KILL
