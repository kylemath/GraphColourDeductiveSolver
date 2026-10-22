# Is the translation monodromy t of an even cluster forced nonzero? (two 5-vertices in a dome; 5-7 pairs)
import json
from lev import *
from e1_survey import graph
def sat_t(cl, maxt2, K2=16.0):
    # boundary walk within radius K, with |H_m - H_0|^2 <= maxt2 (in plane units)
    m = cl.m
    def extra(add, x, new):
        pass
    # re-implement closure via domain trick: rebuild with an extra constraint using sat_level internals
    import lev
    D = domain(K2)
    # reuse sat_level by monkeypatching: simplest is to build here
    V = cl.verts; ix = cl.idx; nv = len(V); X = lambda v, c: 4*ix[v]+c+1
    top = [4*nv]; cls = []
    def nw(): top[0] += 1; return top[0]
    for v in V:
        cls.append([X(v, c) for c in range(4)])
        for a, b in itertools.combinations(range(4), 2): cls.append([-X(v, a), -X(v, b)])
    for u, w in cl.edges:
        for c in range(4): cls.append([-X(u, c), -X(w, c)])
    Ds = set(D); H = [{p: nw() for p in D} for _ in range(m+1)]
    for i in range(m):
        u, w = cl.walk[i], cl.walk[(i+1) % m]; L = {l: nw() for l in (1, 2, 3)}
        for a in range(4):
            for b in range(4):
                if a != b: cls.append([-X(u, a), -X(w, b), L[a ^ b]])
        for p in D:
            for l in (1, 2, 3):
                d = INC[l]; q = (p[0]+cl.s[i]*d[0], p[1]+cl.s[i]*d[1])
                cls.append([-H[i][p], -L[l], H[i+1][q]] if q in Ds else [-H[i][p], -L[l]])
    cls.append([H[0][(0, 0)]])
    for p0 in D:
        if p0 != (0, 0): cls.append([-H[0][p0]])
    for p in D:
        if n2(p) > maxt2+1e-9: cls.append([-H[m][p]])
    s = Cadical153(bootstrap_with=cls); ok = s.solve(); s.delete(); return ok
for l in open('e1_survey.jsonl'):
    r = json.loads(l)
    if r.get('nodd') in (2, 4) and r['name'].startswith('ico'):
        T = graph(r['name']); cl = Cluster(T, bfs(T.adj, r['c'], r['r']))
        print(r['name'], r['r'], 'nodd', r['nodd'], 'spacing', r['odd_spacing'], 't=0 possible:', sat_t(cl, 0.0), flush=True)
