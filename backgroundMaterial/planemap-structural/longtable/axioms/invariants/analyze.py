"""Monotonicity scan over runs (INVARIANTS-1).  Usage: analyze.py data/passN
For every numeric feature f and run kind, along each run:
  step-2 differences d = f(t+2) - f(t), split by the parity class of t (H = w[t]==1 Hamiltonian state,
  N = w[t]==2), and 1-step differences.  Reports, per (kind, feature, class), the share of runs whose
  differences are all >= 0, all <= 0, all > 0, all < 0, all == 0 (runs with >= 1 difference)."""
import sys, json, gzip
from collections import defaultdict

pref = sys.argv[1]
rows = [json.loads(l) for l in gzip.open(pref + '_feat.jsonl.gz', 'rt')]
runs = defaultdict(list)
for r in rows: runs[r['run']].append(r)
for k in runs: runs[k].sort(key=lambda r: r['t'])
FEATS = ['k', 'a5', 'nX', 'nY', 'xx', 'yy', 'xy', 'pX', 'pY', 'vcross', 'xycross', 'f8planar', 'YYn', 'XXn', 'D',
         'XYn', 'YXn', 'h_ncross', 'h_comp', 'h_bip', 'h_bip_rot', 'h_oddc', 'h_e0', 'h_e1', 'h_e3', 'h_e0x',
         'h_e1x', 'h_e3x', 'h_bipdef', 'aX', 'aY', 'aO', 'hA', 'hB']


def cls(r):
    w = r.get('w')
    return 'H' if w == 1 else ('N' if w == 2 else '?')


def diffs(seq, f, step, closed):
    R = len(seq); out = defaultdict(list)
    rng = range(R) if closed else range(R - step)
    for t in rng:
        a = seq[t].get(f); b = seq[(t + step) % R].get(f)
        if a is None or b is None: continue
        out[cls(seq[t])].append(b - a)
    return out


res = {}
kinds = sorted(set(r['kind'] for r in rows))
for kind in kinds:
    rr = [s for s in runs.values() if s[0]['kind'] == kind]
    for f in FEATS:
        for step in (1, 2):
            agg = defaultdict(lambda: defaultdict(int))
            vals = defaultdict(list)
            for s in rr:
                D = diffs(s, f, step, s[0]['closed'])
                for c, d in D.items():
                    if not d: continue
                    a = agg[c]; a['runs'] += 1
                    a['ge'] += all(x >= 0 for x in d); a['le'] += all(x <= 0 for x in d)
                    a['gt'] += all(x > 0 for x in d); a['lt'] += all(x < 0 for x in d)
                    a['eq'] += all(x == 0 for x in d)
                    vals[c] += d
            for c, a in agg.items():
                v = vals[c]
                res[(kind, f, step, c)] = dict(a, ndiff=len(v), mean=round(sum(v) / len(v), 3),
                                               pos=sum(1 for x in v if x > 0), neg=sum(1 for x in v if x < 0),
                                               zero=sum(1 for x in v if x == 0))
# print the interesting lines: any class where (gt or lt or eq or ge or le) covers all runs, or strong bias
out = open(pref + '_monotone.txt', 'w')
def pr(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
pr('kind feature step class | runs all>=0 all<=0 all>0 all<0 all==0 | diffs pos neg zero mean')
for key in sorted(res):
    kind, f, step, c = key; a = res[key]
    flag = ''
    if a['runs'] >= 3:
        for nm in ('eq', 'gt', 'lt', 'ge', 'le'):
            if a[nm] == a['runs']: flag = '<== ' + nm; break
    pr(kind, f, step, c, '|', a['runs'], a['ge'], a['le'], a['gt'], a['lt'], a['eq'], '|', a['ndiff'], a['pos'], a['neg'], a['zero'], a['mean'], flag)
