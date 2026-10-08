#!/usr/bin/env python3
"""Track P: prescan surface triangulations (all degree-5 holes) with tn_eng and rank holes as seeds for law-respecting
R-cycle annealing.  Score per hole: P1 = best all-DL pi-cycle law penalty (bc[1][0]) if any, and win[1] (best 10-window
law penalty).  Output: seed lines 'name n rot hole' sorted by (P1, win1), plus a jsonl of the per-hole stats.
usage: tp_prescan.py IN.txt OUTPREFIX [TOP]"""
import sys, json, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
inp, pref = sys.argv[1], sys.argv[2]; top = int(sys.argv[3]) if len(sys.argv) > 3 else 60
lines = [l.strip() for l in open(inp) if l.strip()]
p = subprocess.Popen([os.path.join(HERE, 'tn_eng'), '--allholes', '--maxstates', '60000'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
rows = []
for l in lines:
    rot = [list(map(int, r.split(','))) for r in l.split()[2].split(';')]
    holes = [v for v in range(len(rot)) if len(rot[v]) == 5]
    p.stdin.write(l + '\n'); p.stdin.flush()
    for h in holes:
        tn = json.loads(p.stdout.readline())
        if 'err' in tn: continue
        js = json.loads(p.stdout.readline())
        bc1 = tn['bc'][1][0] if 'bc' in tn else 99
        rows.append(dict(name=l.split()[0], hole=h, states=js['states'], run0=tn['run'][0], run1=tn['run'][1], win1=tn['win'][1], bc1=bc1,
                         prof=tn['bc'][1][8] if 'bc' in tn else '', ncyc=js['ncyc'], line=l))
p.stdin.close(); p.wait()
rows.sort(key=lambda r: (min(r['bc1'], (r['win1'] if r['win1'] >= 0 else 99) + 3), r['win1'] if r['win1'] >= 0 else 99, -r['run0']))
with open(pref + '_stats.jsonl', 'w') as f:
    for r in rows: f.write(json.dumps({k: v for k, v in r.items() if k != 'line'}) + '\n')
with open(pref + '_seeds.txt', 'w') as f:
    for r in rows[:top]: f.write(f"{r['line']} {r['hole']}\n")
print(len(lines), 'graphs', len(rows), 'holes; best:', [(r['name'], r['hole'], r['bc1'], r['win1'], r['run0'], r['prof']) for r in rows[:8]])
