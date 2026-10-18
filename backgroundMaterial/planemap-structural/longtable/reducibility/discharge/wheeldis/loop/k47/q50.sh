# Round 50 queue (after round 49): relay-class receivers at ring <= 14, one row at a time, 3 workers.
cd "$(dirname "$0")"
until [ -f ../k46/grow49_66669.txt ] && [ -f ../k46/grow49_56696.txt ]; do sleep 20; done; sleep 10
row() {   # d LK SV PREFIX
  W=win45_$1_$2_$3_A14.txt
  [ -f $W ] || python3 win45.py 14 $1 $2 $3
  python3 - $W <<'PY'
import sys
w = [l.split()[0] for l in open(sys.argv[1]) if l.strip()]
done = {l.split()[0] for l in open('A_kcc.out') if l[:1] == 'a'}; k = {l.split()[0] for l in open('KILL')}
print('%s: %d windows, %d already run, %d already two-engine kills' % (sys.argv[1], len(w), sum(x in done for x in w), sum(x in k for x in w)))
PY
  date -u +%H:%MZ
  STOP=0 NW=3 python3 drive45.py $W 600 > drive50_$4.log 2>&1
  python3 minkill47.py $W $2 $4; date -u +%H:%MZ; cat $4_kills_min.txt
}
row 7 7665566 6675666 r7d; touch R50A.DONE
STOP=0 NW=3 python3 drive45.py win45_9_656565665_665666566_A14.txt 600 > drive47B2.log 2>&1; touch B14.DONE; date -u +%H:%MZ
sleep 60
row 9 656656665 665555555 r9d; touch R50C.DONE
row 10 6556656556 6665656665 r10a; touch R50D.DONE
grep -c MISMATCH A_df.out A_cf.out KILL
