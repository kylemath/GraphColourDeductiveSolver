#!/usr/bin/env python3
"""Track Q: where is the extra chain Z at each 9-state of a law R-cycle (alpha-mu = sigma-type, or AB)?
Also the cycle ranks of the six pair graphs (role order) at the state and at its rigid predecessor.
usage: tq_ztype.py FILE [FILE ...]"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tn_lib import Engine
from tn_forest import parse_dump, cycles_in_R_law, components
from tq_roles import roles
ed = Engine(dump=True, maxstates=200000); agg = collections.Counter()
def pairdata(n, E, c):
    j, (a, m, A, B) = roles(c); link = set(range(1, 6)); out = []
    for (p, q) in ((a, m), (A, B), (a, A), (m, B), (a, B), (m, A)):
        V = [v for v in range(1, n) if c[v] in (p, q)]; Es = [e for e in E if c[e[0]] in (p, q) and c[e[1]] in (p, q)]
        cs = components(V, Es); free = sum(1 for C in cs if not (C & link))
        out.append((len(cs), len(Es) - len(V) + len(cs), free))
    return out
for f in sys.argv[1:]:
    for l in open(f):
        if l.startswith('{'):
            d = json.loads(l)
            if 'graph' not in d or d.get('ev', 'example') != 'example': continue
            l = d['graph']
        p = l.split()
        if len(p) < 3: continue
        rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        n = len(rot); E = sorted({tuple(sorted((u, v))) for u in range(1, n) for v in rot[u] if v != 0})
        js, tn, dump = ed.run(l)
        if tn is None: continue
        S = parse_dump(dump)
        for C in cycles_in_R_law(S):
            z = []
            for i, x in enumerate(C):
                if S[x]['N'] != 9: continue
                # Lemma Q-S identity with the rigid predecessor u = C[i-1] (roles in each state's own frame)
                cu = [-1 if ch == '-' else int(ch) for ch in S[C[i - 1]]['col']]
                pu = pairdata(n, E, cu); pc = pairdata(n, E, [-1 if ch == '-' else int(ch) for ch in S[x]['col']])
                lhs = pc[2][1] + pc[1][1]; rhs = pc[1][0] + pu[0][1] + pu[5][1]
                agg['QS'] += 1; agg['QS_fail'] += int(lhs != rhs)
                # mirror identity with the rigid successor u' = C[i+1]: beta_c(aB)+beta_c(AB) = #AB + beta_u'(am) + beta_u'(mB)
                cw = [-1 if ch == '-' else int(ch) for ch in S[C[(i + 1) % len(C)]]['col']]; pw = pairdata(n, E, cw)
                lhs2 = pc[4][1] + pc[1][1]; rhs2 = pc[1][0] + pw[0][1] + pw[3][1]
                agg['QSm'] += 1; agg['QSm_fail'] += int(lhs2 != rhs2)
                c = [-1 if ch == '-' else int(ch) for ch in S[x]['col']]
                pd = pairdata(n, E, c)
                where = [nm for nm, (k, b, fr) in zip(('am', 'AB', 'aA', 'mB', 'aB', 'mA'), pd) if fr > 0]
                z.append('+'.join(where)); agg[tuple(where)] += 1
            print(p[0], len(E) - (3 * (n - 1) - 8), ' '.join(z), flush=True)
print(json.dumps({str(k): v for k, v in agg.items()}))
