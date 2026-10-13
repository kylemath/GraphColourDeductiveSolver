"""Per-class anatomy at small n (census classes): chords, #PM, #arcs, #Ham arcs, longest D-walk through a Ham
arc (as v-frame word, Ham arc marked by |), and the pairing at v of E - M at the two dead ends (type B =
{k+1,k+2}{k+3,k+4}; A = {k+2,k+3}{k+1,k+4}).  usage: anatomy.py n"""
import sys, json
import networkx as nx
from r0lib import G5, analyse
from depth import loop_partner   # noqa (depth.py runs on import only with argv; guarded below)
n = int(sys.argv[1])
def ptype(g, M, k):
    p = loop_partner(g, M, (k + 2) % 5)
    return 'A' if p == (k + 3) % 5 else ('B' if p == (k + 1) % 5 else 'X')
for ci, l in enumerate(open(f'out/census_n{n}_p.jsonl')):
    r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
    A = analyse(g); D = A['D']; P = A['P']; ks = A['ks']
    back = {}; fwd = {}; bp = {}; fp = {}
    order = list(nx.topological_sort(D))
    for x in order:
        preds = list(D.predecessors(x))
        back[x] = max([back[p] + 1 for p in preds], default=0)
        bp[x] = max(preds, key=lambda p: back[p]) if preds else None
    for x in reversed(order):
        su = list(D.successors(x))
        fwd[x] = max([fwd[s] + 1 for s in su], default=0)
        fp[x] = max(su, key=lambda s: fwd[s]) if su else None
    best = max(A['ham'], key=lambda a: back[a[0]] + fwd[a[1]]) if A['ham'] else None
    chords = sorted(tuple(g.E[e]) for e in range(g.m) if e not in g.fidx and abs(g.E[e][0] - g.E[e][1]) != 1)
    vends = {s: g.other(g.fv[s], 0) for s in (1, 3, 4)}
    line = f'| {ci} | {chords} f1,f3,f4->{vends[1]},{vends[3]},{vends[4]} | {len(P)} | {len(A["arcs"])} | {len(A["ham"])} |'
    if best:
        i0, i1 = best; left = []; x = i0
        while bp[x] is not None: x = bp[x]; left.append(x)
        right = []; x = i1
        while fp[x] is not None: x = fp[x]; right.append(x)
        word = ''.join(str(ks[x]) for x in reversed(left)) + str(ks[i0]) + '|' + str(ks[i1]) + ''.join(str(ks[x]) for x in right)
        start = (list(reversed(left)) + [i0])[0]; end = ([i1] + right)[-1]
        line += f' {back[i0] + 1 + fwd[i1]} | {word} | source: no in-arc ({ptype(g, P[start], ks[start])}), sink: {ptype(g, P[end], ks[end])} |'
    print(line)
