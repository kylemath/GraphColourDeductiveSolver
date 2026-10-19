# Round 51 queue after part 1 (replaces q51b/q51c.sh; Long Table 02:08Z and 02:36Z): the two s18r relay binders, each ring <= 14 then
# ring 15-16 only if no kill, then part 2 (survivor windows of the binder 7665566/6675666).  3 workers.
cd "$(dirname "$0")"
until [ -f R51B.DONE ]; do sleep 30; done
row() {   # D LK SV PREFIX
  for R in 14 16; do
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
row 10 6565656565 6655666666 r10b; touch R51D.DONE
row 7 7655667 6756656 r7g; touch R51E.DONE
# s19c secondary binders (Long Table 02:36Z; 7666566/5656656 is 7665666/6566565 mirrored, dead at ring 12, not rerun)
row 9 655566556 757656565 r9e; touch R51F.DONE
row 7 7676556 7759565 r7h; touch R51G.DONE
row 7 7655566 6759676 r7i; touch R51H.DONE
grep -c MISMATCH A_df.out A_cf.out KILL
date -u +%H:%MZ
[ -f win51_A17.txt ] || python3 win51.py 17
python3 - <<'PY'
L = [l for l in open('win51_A17.txt') if l.strip()]
a = [l for l in L if int(l.split()[1]) <= 16][:300]; b = [l for l in L if int(l.split()[1]) == 17][:200]
open('win51_run.txt', 'w').write(''.join(a + b))
print('ring <= 16: %d run of %d; ring 17: %d run of %d' % (len(a), sum(1 for l in L if int(l.split()[1]) <= 16), len(b), sum(1 for l in L if int(l.split()[1]) == 17)))
PY
date -u +%H:%MZ
STOP=0 NW=3 python3 drive45.py win51_run.txt 600 > drive51_b.log 2>&1
date -u +%H:%MZ; touch R51C.DONE
grep '^b7_' KILL; grep -c MISMATCH A_df.out A_cf.out KILL
