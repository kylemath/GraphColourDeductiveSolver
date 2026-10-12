#!/usr/bin/env python3
"""Census29 [exploratory]: summary of out/eval-N.jsonl (N = 22..max) + word / hitting-set statistics.
Words: Track B convention (capped at 8+, canonical over rotations and reflections), using TrackB/words.py functions.
usage: summarise.py N1 N2 > out/summary.txt"""
import sys, os, re, json, collections
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); WK = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(WK, 'TrackB'))
from words import load, graph_words, fmt, hitting
N1, N2 = int(sys.argv[1]), int(sys.argv[2])
O = os.path.join(ROOT, 'out')

def plantri_total(n):
    p = os.path.join(O, 'shards', str(n))
    if os.path.isdir(p):
        fs = [os.path.join(p, f) for f in os.listdir(p) if f.endswith('.plog')]
    else: fs = [os.path.join(O, 'plantri-%d.log' % n)]
    tot = 0
    for f in fs:
        m = re.search(r'(\d+) triangulations written', open(f).read())
        if not m: return None
        tot += int(m.group(1))
    return tot

R = {n: [json.loads(l) for l in open(os.path.join(O, 'eval-%d.jsonl' % n))] for n in range(N1, N2 + 1) if os.path.exists(os.path.join(O, 'eval-%d.jsonl' % n))}
print('# Census29 summary, orders %d-%d (plantri -m5 -c4, TrackB frame.c, picyc --full, f66 --lockparity, kempe_py sample)\n' % (N1, N2))
print('order | plantri graphs | frame | deg-5 vertices | PureClean | non-PC graphs | worst (floor) | #holes at 1/4 | #graphs at 1/4 | breaks <1/4 | min margin | LP states | LP fails | allDL cycles | errs | eng2 sample | eng2 class mism | eng2 LP states | eng2 LP fails | eng2 frame')
tot = collections.Counter()
for n, rs in R.items():
    e2 = [r['engine2'] for r in rs if 'engine2' in r]
    row = dict(pl=plantri_total(n), fr=len(rs), d5=sum(r['deg5'] for r in rs), pc=sum(r['npc'] for r in rs),
               nonpc=sum(1 for r in rs if r['nonpc']), worst=min(r['worst'] for r in rs), qh=sum(len(r['quarter_eq']) for r in rs),
               qg=sum(1 for r in rs if r['quarter_eq']), qb=sum(len(r['quarter_break']) for r in rs), mm=min(r['margin'] for r in rs),
               lp=sum(r['lp'][0] for r in rs), lpf=sum(sum(r['lp'][1:]) for r in rs), adl=sum(r['allDL'] for r in rs),
               errs=sum(len(r['errs']) for r in rs), e2n=len(e2), e2c=sum(1 for v in e2 if not v['classes_ok']),
               e2lp=sum(v['lp_unf'] for v in e2), e2lpf=sum(v['lp_bad'] for v in e2) + sum(1 for v in e2 if not v['lp_unf_ok']),
               e2fr=sum(1 for v in e2 if v['frame']))
    for k in ('fr', 'd5', 'pc', 'nonpc', 'qh', 'qg', 'qb', 'lp', 'lpf', 'adl', 'errs', 'e2n', 'e2c', 'e2lp', 'e2lpf', 'e2fr'): tot[k] += row[k]
    print('%d | %s | %d | %d | %d | %d | %.4f | %d | %d | %d | %.4f | %d | %d | %d | %d | %d | %d | %d | %d | %d' % (
        n, row['pl'], row['fr'], row['d5'], row['pc'], row['nonpc'], row['worst'], row['qh'], row['qg'], row['qb'], row['mm'],
        row['lp'], row['lpf'], row['adl'], row['errs'], row['e2n'], row['e2c'], row['e2lp'], row['e2lpf'], row['e2fr']))
print('total |  | %(fr)d | %(d5)d | %(pc)d | %(nonpc)d |  | %(qh)d | %(qg)d | %(qb)d |  | %(lp)d | %(lpf)d | %(adl)d | %(errs)d | %(e2n)d | %(e2c)d | %(e2lp)d | %(e2lpf)d | %(e2fr)d' % tot)

allr = [r for rs in R.values() for r in rs]
print('\n## Small classes (N <= 16) by (size, F): count of holes')
sc = collections.Counter((s, F) for r in allr for c in r['classes'].values() for s, F in c if s <= 16)
print(dict(sorted(sc.items())))
print('\n## Quarter-floor equality classes (4F = N) by (size, F) and order')
qe = collections.Counter((r['n'], s, F) for r in allr for c in r['classes'].values() for s, F in c if 4 * F == s)
print(dict(sorted(qe.items())))
print('max size of an equality class:', max((s for (_, s, _) in qe), default=None))
print('\n## Classes per hole: histogram'); print(dict(sorted(collections.Counter(len(c) for r in allr for c in r['classes'].values()).items())))
print('\n## Most marginal graphs (smallest margin = max over deg-5 v of min class F/size), 15 lowest')
for r in sorted(allr, key=lambda r: r['margin'])[:15]:
    print('  %-18s n=%d deg5=%d margin=%.4f worst=%.4f wordset=%s' % (r['name'], r['n'], r['deg5'], r['margin'], r['worst'], ','.join(r['wordset'])))
print('\n## Graphs with the most holes at exactly 1/4 (top 10)')
for r in sorted(allr, key=lambda r: -len(r['quarter_eq']))[:10]:
    print('  %-18s n=%d holes at 1/4: %d of %d' % (r['name'], r['n'], len(r['quarter_eq']), r['deg5']))
print('\n## Smallest class fractions strictly above 1/4 (closest approach to the floor without equality), 10 lowest')
nf = sorted(((F / s, s, F, r['name']) for r in allr for c in r['classes'].values() for s, F in c if 4 * F > s))[:10]
for x in nf: print('  F/N=%.4f (N=%d, F=%d) %s' % x)

# ---- words
print('\n## Link words (cap 8+) per order')
files = {n: os.path.join(O, 'frame-%d.txt' % n) for n in range(22, N2 + 1)}
G = {n: load([f]) for n, f in files.items() if os.path.exists(f)}
seen = set(); sets_by_n = {}
for n in sorted(G):
    sets = [frozenset(graph_words(rot, 8)) for _, _, rot in G[n]]; sets_by_n[n] = sets
    U = set().union(*sets) if sets else set(); new = U - seen; seen |= U
    mono = sorted({fmt(next(iter(s)), 8) for s in sets if len(s) == 1})
    print('n=%d graphs=%d distinct words=%d new=%d %s monotype=%s' % (n, len(sets), len(U), len(new), sorted(fmt(w, 8) for w in new), mono))
print('cumulative distinct words in census:', len(seen))
freq = collections.Counter(w for n in sets_by_n for s in sets_by_n[n] for w in s)
print('graphs containing each word (all census orders):', ', '.join('%s %d' % (fmt(w, 8), c) for w, c in freq.most_common()))

def reduce_sets(sets):
    S = sorted(set(sets), key=len); keep = []
    for s in S:
        if not any(k <= s for k in keep): keep.append(s)
    return keep

def packing(sets):
    X = reduce_sets(sets); U = sorted(set().union(*X)); A = np.zeros((len(U), len(X)))
    for j, s in enumerate(X):
        for w in s: A[U.index(w), j] = 1
    res = milp(c=-np.ones(len(X)), constraints=LinearConstraint(A, -np.inf, 1), integrality=np.ones(len(X)), bounds=Bounds(0, 1))
    return [X[j] for j in range(len(X)) if res.x[j] > 0.5]

print('\n## Hitting sets (exact MILP over inclusion-minimal word sets)')
cum = []
for n in sorted(sets_by_n):
    cum += sets_by_n[n]; X = reduce_sets(cum); g, E = hitting(X, set().union(*X))
    print('census 22..%d: %d graphs, %d minimal word-sets, min hitting set %d: %s' % (n, len(cum), len(X), len(E), sorted(fmt(w, 8) for w in E)))
ext = {k: os.path.join(WK, 'TrackB/out', f) for k, f in (('ipr', 'frame-ext-ipr.txt'), ('bigsample', 'frame-ext-bigsample.txt'), ('witness', 'witness-cap8.txt'))}
xs = [frozenset(graph_words(rot, 8)) for f in ext.values() for _, _, rot in load([f])]
base = [s for n in sets_by_n if n <= 28 for s in sets_by_n[n]]
for lab, S0 in (('census 22..28 + TrackB extras (IPR, bigsample, 325 witnesses)', base + xs), ('census 22..%d + TrackB extras' % max(sets_by_n), cum + xs)):
    X = reduce_sets(S0); g, E = hitting(X, set().union(*X)); pk = packing(S0)
    print('%s: min hitting set %d: %s | disjoint packing lower bound %d' % (lab, len(E), sorted(fmt(w, 8) for w in E), len(pk)))
# does the old 13-word set from Track B's last round still hit every census graph?
S13 = {'55666', '55668+', '55677', '55757', '55758+', '55767', '56657', '56658+', '56666', '56667', '56757', '56758+', '66666'}
miss = [(n, i) for n in sets_by_n for i, s in enumerate(sets_by_n[n]) if not {fmt(w, 8) for w in s} & S13]
print("Track B's final-round 13-set misses %d census graphs" % len(miss), [(n, G[n][i][0]) for n, i in miss[:10]])
pk = packing(cum)
print('census-only disjoint packing lower bound: %d' % len(pk))
for s in pk: print('   ', sorted(fmt(w, 8) for w in s))
