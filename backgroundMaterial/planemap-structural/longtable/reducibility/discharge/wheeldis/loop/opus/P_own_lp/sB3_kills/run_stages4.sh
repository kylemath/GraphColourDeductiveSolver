#!/bin/bash
# B3 sequential driver v4 (1 core, nice 15): replaces v3 after the F stage (PID 1290) so that targets_v2's new rows go first.
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/sB3_kills
while kill -0 1290 2>/dev/null; do sleep 20; done
cd scripts
nice -n 15 python3 famB3.py ../rows_v2new.txt 14 ../windows/famV2_R14.tsv QKFPT > ../logs/gen_V2.log 2>&1
nice -n 15 python3 famB3.py ../rows_r02.txt 14 ../windows/famQr02_R14.tsv Q > ../logs/gen_Qr02.log 2>&1
cd ..
# family list: every tag in famV2, rows in rows_v2new order; within a row Q, K, F, P, T
python3 - <<'PY'
import collections
rows=[l.split()[1]+'/'+l.split()[2] for l in open('rows_v2new.txt') if l.strip() and not l.startswith('#')]
tags=collections.OrderedDict()
for l in open('windows/famV2_R14.tsv'): tags[l.split('\t')[4]]=1
pri={'Q':0,'K':1,'F':2,'P':3,'T':4}
def key(t):
    r=t.split(':')[1]; return (rows.index(r) if r in rows else 99, pri.get(t[0],9), t)
open('flist_V2.tags','w').write('\n'.join(sorted(tags,key=key))+'\n')
PY
MINSC=12:2,13:2 nice -n 15 python3 scripts/scrB3.py results/res_V2.tsv 13 windows/famV2_R14.tsv flist_V2.tags > logs/scr_V2.log 2>&1
echo V2_13_DONE >> logs/scr_V2.log
nice -n 15 python3 scripts/scrB3.py results/res_T1PT.tsv 13 windows/famT1_R14.tsv flist_T1_PT.tags > logs/scr_T1PT.log 2>&1
echo STAGES13_DONE >> logs/scr_T1PT.log
grep -o '^Q:[^	]*' /dev/null; cut -f5 windows/famQr02_R14.tsv | sort -u > flist_Qr02.tags
nice -n 15 python3 scripts/scrB3.py results/res_Qr02_14.tsv 14 windows/famQr02_R14.tsv flist_Qr02.tags > logs/scr_Qr02_14.log 2>&1
nice -n 15 python3 scripts/scrB3.py results/res_T1s1b.tsv 14 windows/famT1_R14.tsv flist_T1_stage1.tags > logs/scr_T1s1b.log 2>&1
MINSC=12:2,13:2,14:3 nice -n 15 python3 scripts/scrB3.py results/res_V2_14.tsv 14 windows/famV2_R14.tsv flist_V2.tags > logs/scr_V2_14.log 2>&1
MINSC=12:2,13:2,14:3 nice -n 15 python3 scripts/scrB3.py results/res_T1F14.tsv 14 windows/famT1_R14.tsv flist_T1_F.tags > logs/scr_T1F14.log 2>&1
echo STAGES_DONE >> logs/scr_T1F14.log
