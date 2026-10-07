#!/usr/bin/env python3
"""[exploratory] Aggregate run*.jsonl: per family table, headline, smallest violating examples (re-verified independently)."""
import sys, json, glob, itertools
from fractions import Fraction
sys.path.insert(0, '../common'); sys.path.insert(0, '.')
from torus import *
from kempe_py import Space

fam = {}; ex = []
graphs = 0
for fn in sorted(glob.glob('run?.jsonl')):
    for line in open(fn):
        r = json.loads(line); graphs += 1
        d = fam.setdefault(r['family'], dict(graphs=0, holes=0, empty=0, skipped=0, classes=0, states=0, minfrac=Fraction(1), viol=0, targetless=0, minwhere=None, graphs_viol=0))
        d['graphs'] += 1; gv = False
        for h in r['holes']:
            if 'skipped' in h: d['skipped'] += 1; continue
            if not h['classes']: d['empty'] += 1; continue
            d['holes'] += 1; d['states'] += h['states']
            for size, fil in h['classes']:
                d['classes'] += 1; fr = Fraction(fil, size)
                if fr < d['minfrac']: d['minfrac'] = fr; d['minwhere'] = (size, fil)
                if fil == 0: d['targetless'] += 1
                if fr < Fraction(1, 4):
                    d['viol'] += 1; gv = True
                    ex.append((r['n'], size, fil, r, h['v']))
        d['graphs_viol'] += gv
print(f'graphs: {graphs}')
print('| family | graphs | deg-5 holes analysed (T-v colourable) | classes | states | min filled fraction (class size, filled) | classes < 1/4 | targetless classes | graphs with violation |')
print('|---|---|---|---|---|---|---|---|---|')
tot = dict(holes=0, classes=0, viol=0, targetless=0, graphs=0, gv=0); gmin = Fraction(1)
def key(k): a, b = k[2:-1].split(','); return (int(a) * int(b), int(a))
for k in sorted(fam, key=key):
    d = fam[k]; gmin = min(gmin, d['minfrac'])
    print(f"| {k} | {d['graphs']} | {d['holes']} | {d['classes']} | {d['states']} | {d['minfrac']} ({d['minwhere']}) | {d['viol']} | {d['targetless']} | {d['graphs_viol']} |")
    for a, b in [('holes','holes'),('classes','classes'),('viol','viol'),('targetless','targetless'),('graphs','graphs'),('gv','graphs_viol')]: tot[a] += d[b]
print('TOTAL', tot, 'global min fraction', gmin)
# first (smallest) violation, verified from scratch
ex.sort(key=lambda t: (t[0], t[1], t[2]))
if ex:
    n, size, fil, r, v = ex[0]
    F = set(frozenset(f) for f in r['faces']); assert validate(n, F) is None
    adj = adjacency(F, n); link = link_cycle(F, v); sp = Space(adj, v, link); sp.build_graph(); cl, ncl = sp.classes()
    cnt = {}
    for k in range(len(sp.states)): c = cl[k]; a = cnt.setdefault(c, [0, 0]); a[0] += 1; a[1] += sp.filled(k)
    assert [size, fil] in [list(x) for x in cnt.values()]
    c = next(c for c, x in cnt.items() if x == [size, fil])
    print('\nFIRST (smallest) VIOLATION, re-verified from the face list')
    print('n =', n, 'family', r['family'], 'degseq', r['degseq']); print('v =', v, 'link', link, 'deg', len(adj[v]))
    print('faces =', r['faces']); print(f'class size {size}, filled {fil}, fraction {Fraction(fil, size)}; T-v states {len(sp.states)}, classes {ncl}')
    if size <= 4:
        for k in range(len(sp.states)):
            if cl[k] == c: print(' state (vertex order', sp.order, ')', sp.states[k], 'link colours', [sp.states[k][i] for i in sp.linki], 'filled', sp.filled(k))
    # smallest targetless
    tl = [t for t in ex if t[2] == 0]; tl.sort(key=lambda t: (t[0], t[1]))
    print('number of violating (hole,class) pairs:', len(ex), ' targetless among them:', len(tl))
    if tl: print('smallest targetless: n=%d size=%d family=%s v=%d' % (tl[0][0], tl[0][1], tl[0][3]['family'], tl[0][4]))
    mn = min(ex, key=lambda t: Fraction(t[2], t[1])); print('lowest-fraction nonzero? see table; example with n,size,fil:', mn[:3])
