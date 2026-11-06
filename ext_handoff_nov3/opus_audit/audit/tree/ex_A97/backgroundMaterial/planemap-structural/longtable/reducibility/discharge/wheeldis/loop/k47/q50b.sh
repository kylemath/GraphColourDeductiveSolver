# Round 50 follow-on: d = 7 7665566/6675666 at ring 15-16 (no kill at ring <= 14), after the d = 10 row.
cd "$(dirname "$0")"
until [ -f R50D.DONE ]; do sleep 30; done
W=win45_7_7665566_6675666_A16.txt
[ -f $W ] || python3 win45.py 16 7 7665566 6675666
date -u +%H:%MZ; wc -l < $W
STOP=0 NW=3 python3 drive45.py $W 600 > drive50_r7d16.log 2>&1
python3 minkill47.py $W 7665566 r7d16; date -u +%H:%MZ; cat r7d16_kills_min.txt
grep -c MISMATCH A_df.out A_cf.out KILL; touch R50E.DONE
