#!/usr/bin/env python3
"""compare.py N: check val-N.jsonl (picyc --full on the gentri list) against run 23 (out-N.jsonl) and run 26 (small-N.jsonl)."""
import sys, json
from collections import Counter, defaultdict
n = int(sys.argv[1]); mine = [json.loads(l) for l in open('val-%d.jsonl' % n)]
gh = defaultdict(Counter); hole = {}
for r in mine:
    if r['kind'] != 'hole': continue
    gi = int(r['name'].split('#')[1]); hole[(gi, r['hole'])] = r
    for w, L, c in r['hist']: gh[gi][(w, L)] += c
# run 23
r23g = {}; r23c = []
for l in open('../23-positive-cycles/out-%d.jsonl' % n):
    r = json.loads(l)
    if r['kind'] == 'graph': r23g[r['gentri']] = Counter({(w, L): c for w, L, c in r['hist']})
    else: r23c.append(r)
bad = [gi for gi in r23g if r23g[gi] != gh.get(gi, Counter())]
print('run 23 graph histograms: %d graphs, mismatches %d' % (len(r23g), len(bad)), bad[:5])
mypos = {(gi, h): r for (gi, h), r in hole.items() if r['npos']}
r23pos = {}
for r in r23c: r23pos.setdefault((r['gentri'], r['hole']), []).append(r)
print('positive (graph,hole): run23 %d mine %d, same set %s' % (len(r23pos), len(mypos), set(r23pos) == set(mypos)))
mm = 0
for key, recs in r23pos.items():
    m = mypos.get(key)
    if not m: mm += 1; continue
    cw = sorted((c['w'], c['L'], c['minnb']) for rec in recs for c in rec['cycles']); mw = sorted((p['w'], p['L'], p['minnb']) for p in m['pos'])
    if cw != mw: mm += 1; print('  cycle mismatch', key, cw, mw)
    for rec in recs:
        cl = [p['class'] for p in m['pos'] if True]
        if not any(c['states'] == rec['states'] and c['ncyc'] == rec['ncyc'] for c in cl): mm += 1; print('  class mismatch', key, rec['states'], rec['ncyc'], [(c['states'], c['ncyc']) for c in cl])
print('run 23 positive-cycle records mismatches', mm)
# run 26
try:
    r26 = [json.loads(l) for l in open('../26-transport-adversarial/small-%d.jsonl' % n)]
except FileNotFoundError:
    r26 = []
mm = 0; nchk = 0
for rec in r26:
    key = (rec['tag']['gentri'], rec['tag']['hole']); m = mypos.get(key)
    if not m: mm += 1; print('  missing', key); continue
    # transport: run 26 is per class; mine per bipartite component. Compare the hall ratios on the component holding the same posW.
    for v in ['a_DL_allpairs', 'b_DL_otherpair', 'c_anystate', 'd_DL_lockbreaking', 'e_DL_otherpair_lockbreaking']:
        t26 = rec['transport'][v]; cands = [t for t in m['transport'] if sorted(t['posW'], reverse=True) == rec['posW']]
        if not cands: mm += 1; print('  no comp', key, rec['posW'], [t['posW'] for t in m['transport']]); break
        t = cands[0][v]; nchk += 1
        if t['ok'] != t26['ok'] or t['flow'] != t26['flow'] or t['capreach'] != t26['capreach'] or (t26['hall_ratio'] is not None and abs(t['hall_ratio'] - t26['hall_ratio']) > 1e-3):
            mm += 1; print('  transport mismatch', key, v, t26, t)
    lb26 = sorted((x['w'], x['L'], x['nDL'], x['exits_DL'], x['exits_lockbreaking'], x['exits_to_neg'], x['exits_to_neg_lockbreaking']) for x in rec['lockbreak'])
    lbm = sorted((p['w'], p['L'], p['nDL'], p['exits_DL'], p['exits_lockbreaking'], p['exits_to_neg'], p['exits_to_neg_lockbreaking']) for p in m['pos'] if any(p['w'] == x['w'] and p['L'] == x['L'] for x in rec['lockbreak']))
    if lb26 != lbm: mm += 1; print('  lockbreak mismatch', key, lb26, lbm)
print('run 26: %d class records, %d transport checks, mismatches %d' % (len(r26), nchk, mm))
