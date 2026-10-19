# Round 51 part 2: binder census-survivor windows (win51.py), after part 1.  Ring <= 16 ones (at most 300), then the
# first 200 at ring 17 (ordered by more fives, more sixes), 600 s cap, 3 workers.
cd "$(dirname "$0")"
until [ -f R51B.DONE ]; do sleep 30; done
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
