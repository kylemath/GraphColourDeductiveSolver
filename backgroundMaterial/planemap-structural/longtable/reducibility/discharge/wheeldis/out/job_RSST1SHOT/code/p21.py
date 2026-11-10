#!/usr/bin/env python3
"""Coordinator 12:47Z: own proved kill P21 (C window fix_404d45e819) kills six d = 6 rows (link/sword).
Treated as a proved kill at d6: which of our d6 K582 states (fullworld d6 582 leaves, all killed only by 'none'
configs) does it remove?  A leaf (link, read apexes, unread apexes = 9+, read privates) stands for every row that
agrees on the read apexes; P21 removes the leaf only if every such row is a P21 row (i.e. no unread apex and the
leaf's apex word is a P21 sword).  Rows are compared up to rotation and reflection (link and sword together:
reflection sends w_i -> w_{-i}, s_i -> s_{-i-1}).  We also list leaves that P21 partially covers (some completion
rows are P21 rows).  Output results/P21_d6.tsv."""
import os, json, itertools
JOB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P21 = ['565668/575777', '565678/575755', '565678/575757', '565678/777757', '565778/577755', '565788/577755']
def orbit(link, sw):
    d = len(link); out = set()
    for r in range(d):
        L = link[r:] + link[:r]; S = sw[r:] + sw[:r]; out.add((L, S))
        Lr = tuple(L[(-i) % d] for i in range(d)); Sr = tuple(S[(-i - 1) % d] for i in range(d)); out.add((Lr, Sr))
    return out
P = {}
for x in P21:
    a, b = x.split('/');
    for o in orbit(tuple(map(int, a)), tuple(map(int, b))): P[o] = x
rows = []
with open(os.path.join(JOB, 'results', 'P21_d6.tsv'), 'w') as o:
    o.write('# P21 rows (coordinator 12:47Z) vs fullworld d6 K582 leaves (all killed only by none configs)\n')
    o.write('leaf_link\tleaf_filling\tneeds_none\tcompletion_rows\tP21_rows_among_them\tleaf_removed_by_P21\n')
    nfull = npart = 0; tot = 0
    for l in open(os.path.join(JOB, 'logs', 'fw_d6_582_0of1.jsonl')):
        x = json.loads(l)
        if 'summary' in x: continue
        tot += 1
        link = tuple(int(c) for c in x['link']); d = len(link)
        f = dict(t.split('=') for t in x['filling'].split()) if '=' in x['filling'] else {}
        known = {int(k[1:]): int(v) for k, v in f.items() if k.startswith('s')}
        # read apexes at 9 are not in the filling text; treat letters not listed as 9 if read, free if unread:
        # the leaf file does not distinguish, so be conservative: an apex absent from the text may be 9 or unread.
        free = [i for i in range(d) if i not in known]
        hits = []; ncomp = 0
        for combo in itertools.product((5, 6, 7, 8, 9), repeat=len(free)):
            S = [known.get(i, 0) for i in range(d)]
            for i, a in zip(free, combo): S[i] = a
            ncomp += 1
            if (link, tuple(S)) in P: hits.append(''.join(map(str, S)) + '=' + P[(link, tuple(S))])
        if hits:
            removed = (len(free) == 0)
            nfull += removed; npart += 1
            o.write('%s\t%s\t%s\t%d\t%s\t%s\n' % (x['link'], x['filling'], ','.join(x['needs_none']), ncomp, ' '.join(hits), removed))
    o.write('# leaves %d; leaves with some P21 completion row %d; leaves wholly removed by P21 %d\n' % (tot, npart, nfull))
print('leaves', tot, 'touching P21 rows', npart, 'wholly removed', nfull)
