"""print the PM digraph D of every class at small n (anatomy).  usage: show_small.py n [maxclasses]"""
import sys, json
from r0lib import G5, analyse
n = int(sys.argv[1]); mx = int(sys.argv[2]) if len(sys.argv) > 2 else 99
for ci, l in enumerate(open(f'out/census_n{n}_p.jsonl')):
    if ci >= mx: break
    r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
    A = analyse(g)
    name = {}
    for e, (a, b) in enumerate(g.E):
        name[e] = f'f{g.fidx[e]}' if e in g.fidx else f'{a}-{b}'
    print(f'class {ci}: chords', [g.E[e] for e in range(g.m) if e not in g.fidx and abs(g.E[e][0]-g.E[e][1]) != 1],
          'v-ends', {f'f{s}': g.other(g.fv[s], 0) for s in range(5)})
    P = A['P']
    for i, M in enumerate(P):
        es = [name[e] for e in range(g.m) if M >> e & 1]
        outs = [j for (a, j) in A['arcs'] if a == i]
        print(f'   M{i} k={A["ks"][i]} {es}  ->', ['M%d%s' % (j, '*' if (i, j) in A['ham'] else '') for j in outs])
