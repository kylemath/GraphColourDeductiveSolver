#!/bin/bash
# B3 sequential driver v5 (1 core, nice 15), after the coordinator's 18:10Z order (C link family, B pattern supersets, then
# targets_v2 mates of B and E). Waits for the running F stage (PID 1290).
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/sB3_kills
while kill -0 1290 2>/dev/null; do sleep 20; done
DONLY=1 nice -n 15 python3 scripts/scrB3.py results/res_CB.tsv 13 windows/famCB_R14.tsv flist_CB.tags > logs/scr_CB.log 2>&1
echo CB13_DONE >> logs/scr_CB.log
cd scripts
nice -n 15 python3 famB3.py ../rows_v2new.txt 14 ../windows/famV2_R14.tsv QKFPT > ../logs/gen_V2.log 2>&1
cd ..
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
# V2 rings <= 12 first (B and E mates lead the list), then CB ring 14, then V2 ring 13
MINSC=12:2 nice -n 15 python3 scripts/scrB3.py results/res_V2.tsv 12 windows/famV2_R14.tsv flist_V2.tags > logs/scr_V2.log 2>&1
echo V2_12_DONE >> logs/scr_V2.log
DONLY=1 TO=2400 nice -n 15 python3 scripts/scrB3.py results/res_CB14.tsv 14 windows/famCB_R14.tsv flist_CB.tags > logs/scr_CB14.log 2>&1
echo CB14_DONE >> logs/scr_CB14.log
MINSC=12:2,13:2 nice -n 15 python3 scripts/scrB3.py results/res_V2_13.tsv 13 windows/famV2_R14.tsv flist_V2.tags > logs/scr_V2_13.log 2>&1
echo V2_13_DONE >> logs/scr_V2_13.log
nice -n 15 python3 scripts/scrB3.py results/res_T1PT.tsv 13 windows/famT1_R14.tsv flist_T1_PT.tags > logs/scr_T1PT.log 2>&1
echo STAGES13_DONE >> logs/scr_T1PT.log
nice -n 15 python3 scripts/scrB3.py results/res_T1s1b.tsv 14 windows/famT1_R14.tsv flist_T1_stage1.tags > logs/scr_T1s1b.log 2>&1
echo STAGES_DONE >> logs/scr_T1s1b.log
