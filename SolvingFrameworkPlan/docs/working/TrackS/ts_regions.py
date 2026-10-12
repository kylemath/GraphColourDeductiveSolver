#!/usr/bin/env python3
"""Track S experiment 2: region incidence of consecutive figure-eights along R-runs.

At every state t of a near-rigid run, Q_t := F13(t) = E \\ M2(t) is a connected figure-eight X_t u Y_t through v; its three
regions are the P2 chains of t (primal vertex sets): RX = K_{aA}(x_{j+2}) (inside X), RY = K_{aA}(x_j) (inside Y),
RO = K_{mB} (the rest).  Also P1 chains (regions of S^2 - H_t) and P3 chains (regions of F12 = Q_{t-1}).
For consecutive / two-apart states we tabulate |R_a(t) cap R_b(t+d)| and report which entries are ALWAYS zero.
usage: ts_regions.py GRAPHFILE name:hole ...   (or GRAPHFILE --notable FILE minrun)"""
import sys, json
from collections import Counter, defaultdict
from ts_lib import load_graphs, HoleData, runs, pair_components


def regions(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']
    P2 = {}
    for K in pair_components(hd, col, (al, A)):
        if x[2] in K: P2['X'] = frozenset(K)
        elif x[0] in K: P2['Y'] = frozenset(K)
        else: P2.setdefault('Xextra', []).append(K)
    mB = pair_components(hd, col, (mu, B))
    P2['O'] = frozenset(set().union(*mB))
    P1 = {}
    for K in pair_components(hd, col, (al, mu)):
        if x[0] in K: P1['am'] = frozenset(K)
        else: P1['Z'] = frozenset(K)
    ab = pair_components(hd, col, (A, B))
    P1['AB'] = frozenset(set().union(*ab))
    return dict(P2=P2, P1=P1)


def main():
    args = sys.argv[1:]
    G = load_graphs(args[0])
    specs = []
    if args[1] == '--notable':
        minrun = int(args[3]); seen = set()
        for l in open(args[2]):
            d = json.loads(l)
            if d['Rrun'] >= minrun and d['name'] in G and (d['name'], d['hole']) not in seen:
                seen.add((d['name'], d['hole'])); specs.append((d['name'], d['hole']))
    else:
        for s in args[1:]:
            nm, h = s.rsplit(':', 1); specs.append((nm, int(h)))
    tab = {d: defaultdict(Counter) for d in (1, 2)}   # d -> key -> Counter over 'type' (rigid->inshape etc)
    nonzero = {d: defaultdict(int) for d in (1, 2)}
    total = {d: defaultdict(int) for d in (1, 2)}
    nsteps = 0
    for nm, h in specs:
        hd = HoleData(G[nm], h)
        for run, cyc in runs(hd):
            if len(run) < 3: continue
            R = [regions(hd, i) for i in run]
            kinds = ['r' if hd.rigid(i) else ('s' if hd.inshape(i) else 'o') for i in run]
            for d in (1, 2):
                for t in range(len(run) - d):
                    if 'o' in (kinds[t], kinds[t + d]): continue
                    key = kinds[t] + kinds[t + d]
                    total[d][key] += 1
                    for a in ('X', 'Y', 'O'):
                        for b in ('X', 'Y', 'O'):
                            if R[t]['P2'][a] & R[t + d]['P2'][b]: nonzero[d][(key, a, b)] += 1
                    for a in ('am', 'AB'):
                        for b in ('X', 'Y', 'O'):
                            if R[t]['P1'][a] & R[t + d]['P2'][b]: nonzero[d][(key, 'P1' + a, b)] += 1
                    if d == 1: nsteps += 1
        print(nm, h, 'done', flush=True)
    for d in (1, 2):
        print('=== offset', d, dict(total[d]))
        for key in sorted(total[d]):
            line = []
            for a in ('X', 'Y', 'O', 'P1am', 'P1AB'):
                row = []
                for b in ('X', 'Y', 'O'):
                    row.append('%s>%s:%d' % (a, b, nonzero[d][(key, a, b)]))
                line.append(' '.join(row))
            print(key, total[d][key]); print('   ' + '\n   '.join(line))


if __name__ == '__main__':
    main()
