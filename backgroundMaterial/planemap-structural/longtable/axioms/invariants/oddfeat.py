"""Features that are ODD under time-reversal + mirror (the only kind that can be monotone, see report).
sX = 2 pX - (nX - 1): signed offset of v's partner along X (from the f_{k-1} end).
sE = h_e0 + h_e1 - (n - 2): signed offset of the e0/e1 far ends around the circle centre (Hamiltonian states).
dE = h_e0 - h_e1.  Reports sign patterns of 1- and 2-step changes per kind."""
import sys, json, gzip
from collections import defaultdict, Counter
pref = sys.argv[1]
runs = defaultdict(list)
for l in gzip.open(pref + '_feat.jsonl.gz', 'rt'):
    r = json.loads(l); runs[r['run']].append(r)
def feats(r):
    o = {}
    if r['pX'] >= 0: o['sX'] = 2 * r['pX'] - (r['nX'] - 1)
    if r['pY'] >= 0: o['sY'] = 2 * r['pY'] - (r['nY'] - 1)
    if 'h_e0' in r:
        o['sE'] = r['h_e0'] + r['h_e1'] - (r['n'] - 2); o['dE'] = r['h_e0'] - r['h_e1']
        o['s3'] = 2 * r['h_e3'] - (r['n'] - 2)
    return o
for kind in ('a5', 'planar', 'free', 't1'):
    for f in ('sX', 'sY', 'sE', 'dE', 's3'):
        for step in (1, 2):
            runsign = Counter(); vals = Counter()
            for rid, s in runs.items():
                if s[0]['kind'] != kind: continue
                s.sort(key=lambda r: r['t']); F = [feats(r) for r in s]
                R = len(s); closed = s[0]['closed']
                d = []
                for t in (range(R) if closed else range(R - step)):
                    a = F[t].get(f); b = F[(t + step) % R].get(f)
                    if a is not None and b is not None: d.append(b - a)
                if not d: continue
                runsign['all>0' if all(x > 0 for x in d) else 'all<0' if all(x < 0 for x in d) else 'all>=0' if all(x >= 0 for x in d) else 'all<=0' if all(x <= 0 for x in d) else 'mixed'] += 1
                for x in d: vals['+' if x > 0 else '-' if x < 0 else '0'] += 1
            if runsign: print(kind, f, step, dict(runsign), dict(vals))
