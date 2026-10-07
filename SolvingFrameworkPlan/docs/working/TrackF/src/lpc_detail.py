#!/usr/bin/env python3
"""Track F [exploratory]: second engine (pure Python, independent of kclass.cpp/kclass2) for the LPC census,
plus per-state detail of targetless Kempe classes at a degree-5 hole.

For each Kempe class of 4-colourings of T - h (up to colour renaming; moves = swap any Kempe component, any pair):
  size, #filled (link uses <= 3 colours), #DL, #single-lock, #lock-parity violations.
Per unfilled state (link (alpha, mu, alpha, A, B) at x_j..x_{j+4}):
  L1 = x_{j+3} in K_{mu A}(x_{j+1}),  L2 = x_{j+4} in K_{mu B}(x_{j+1})
  eA = parity of #odd-degree (in T) vertices of K_{alpha A}(x_{j+2}),  eB likewise for K_{alpha B}(x_{j+2})
  inA = x_j in K_{alpha A}(x_{j+2}),  inB = x_j in K_{alpha B}(x_{j+2})
  lock parity (LP) holds iff eA == L2 and eB == L1;  Theorem P says eA == !inA, eB == !inB (checked here too);
  D2 fails iff L2 != !inA,  D1 fails iff L1 != !inB.
usage: lpc_detail.py FILE NAME HOLE [--detail]     (HOLE = vertex or 5 = all degree-5 holes)
Output: one JSON line per hole (same class tuple layout as kclass2), and with --detail one line per targetless class."""
import sys, json
from collections import Counter

def read(path, name):
    for l in open(path):
        p = l.split()
        if p and p[0] == name: return [list(map(int, r.split(','))) for r in p[2].split(';')]

def comp(adj, s, allowed):
    seen = {s}; st = [s]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen and w in allowed: seen.add(w); st.append(w)
    return seen

def analyse(rot, h, detail):
    n = len(rot); X = rot[h]; V = [v for v in range(n) if v != h]
    adj = {v: [w for w in rot[v] if w != h] for v in V}
    odd = {v for v in V if len(rot[v]) % 2}
    # BFS order from the link, colour by backtracking, keep first-occurrence normal forms
    order = list(X); seen = set(X) | {h}
    for u in order:
        for w in adj[u]:
            if w not in seen: seen.add(w); order.append(w)
    assert len(order) == n - 1
    pos = {v: i for i, v in enumerate(order)}
    def norm(c):
        mp = {}
        return tuple(mp.setdefault(c[v], len(mp)) for v in order)
    states = []; c = {}
    def rec(i, used):
        if i == len(order): states.append(tuple(c[v] for v in order)); return
        v = order[i]; forb = {c[w] for w in adj[v] if w in c}
        for a in range(min(used + 1, 4)):
            if a not in forb: c[v] = a; rec(i + 1, max(used, a + 1)); del c[v]
    rec(0, 0)
    idx = {s: i for i, s in enumerate(states)}; S = len(states)
    par = list(range(S))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    info = [None] * S; kdeg = [0] * S; pid_bad = [0, 0, 0]
    for i, st in enumerate(states):
        col = {v: st[pos[v]] for v in V}
        lk = [col[x] for x in X]
        if len(set(lk)) <= 3: info[i] = dict(kind='F')
        else:
            j = next(t for t in range(5) if lk[t] == lk[(t + 2) % 5])
            x = [X[(j + t) % 5] for t in range(5)]
            al, mu, A, B = col[x[0]], col[x[1]], col[x[3]], col[x[4]]
            cls = lambda S2: {v for v in V if col[v] in S2}
            L1 = x[3] in comp(adj, x[1], cls({mu, A})); L2 = x[4] in comp(adj, x[1], cls({mu, B}))
            KA = comp(adj, x[2], cls({al, A})); KB = comp(adj, x[2], cls({al, B})); KM = comp(adj, x[2], cls({al, mu}))
            eA = len(KA & odd) % 2; eB = len(KB & odd) % 2; eM = len(KM & odd) % 2
            inA = x[0] in KA; inB = x[0] in KB
            pid_bad[0] += eA != (not inA); pid_bad[1] += eB != (not inB); pid_bad[2] += eM != 1
            pi = None
            if not inA:   # pi = R+3: swap K_{alpha A}(x_{j+2}); defined (link-changing) iff x_j not in it
                d = dict(col)
                for v in KA: d[v] = A if col[v] == al else al
                pi = norm(d)
            info[i] = dict(kind='DL' if (L1 and L2) else 'S', j=j, pi=pi, L1=L1, L2=L2, eA=eA, eB=eB, inA=inA, inB=inB,
                           viol=(eA != L2) or (eB != L1), D2fail=(L2 != (not inA)), D1fail=(L1 != (not inB)),
                           KA=len(KA), KB=len(KB), KAodd=sorted(KA & odd), KBodd=sorted(KB & odd))
        nb = set()
        for p in range(4):
            for q in range(p + 1, 4):
                left = {v for v in V if col[v] in (p, q)}
                while left:
                    s = next(iter(left)); K = comp(adj, s, left); left -= K
                    d = dict(col)
                    for v in K: d[v] = q if col[v] == p else p
                    k = idx[norm(d)]
                    if k != i: nb.add(k)
                    a, b = f(i), f(k)
                    if a != b: par[a] = b
        kdeg[i] = len(nb)
    for i in range(S):
        if info[i]['kind'] != 'F': info[i]['pi'] = idx[info[i]['pi']] if info[i]['pi'] is not None else None
    # all-DL pi-cycles over all states (independent of kclass3)
    oncyc = set(); cyclens = []
    for i in range(S):
        if info[i]['kind'] != 'DL' or i in oncyc: continue
        path = []; k = i; pos2 = {}
        while k is not None and info[k]['kind'] == 'DL' and k not in pos2 and k not in oncyc:
            pos2[k] = len(path); path.append(k); k = info[k]['pi']
        if k is not None and k in pos2:
            cyc = path[pos2[k]:]; oncyc.update(cyc); cyclens.append(len(cyc))
    groups = {}
    for i in range(S): groups.setdefault(f(i), []).append(i)
    cl = []; det = []; piinfo = []
    for r in sorted(groups, key=lambda r: min(groups[r])):
        g = groups[r]; kinds = Counter(info[i]['kind'] for i in g)
        viol = sum(1 for i in g if info[i]['kind'] != 'F' and info[i]['viol'])
        t = [len(g), kinds['F'], kinds['DL'], kinds['S'], min(kdeg[i] for i in g), max(kdeg[i] for i in g), viol]
        cl.append(t)
        if kinds['F'] == 0:
            # pi-orbit structure of a targetless class: partial injection; violators = ends of non-cyclic orbits
            gs = set(g); pre = {}
            for i in g:
                t2 = info[i]['pi']
                if t2 is not None:
                    assert t2 in gs and t2 not in pre; pre[t2] = i
            seen = set(); cyc = []; paths = []
            for i in g:
                if i in pre or i in seen: continue
                L = 0; k = i
                while k is not None and k not in seen: seen.add(k); L += 1; k = info[k]['pi']
                paths.append(L)
            for i in g:
                if i in seen: continue
                L = 0; k = i
                while k not in seen: seen.add(k); L += 1; k = info[k]['pi']
                cyc.append(L)
            ends = {i for i in g if i not in pre} | {i for i in g if info[i]['pi'] is None}
            vset = {i for i in g if info[i]['viol']}
            piinfo.append(dict(size=len(g), viol=viol, paths=sorted(paths), cycles=sorted(cyc), ends_eq_viol=(ends == vset)))
        if detail and kinds['F'] == 0:
            vs = [i for i in g if info[i]['viol']]
            det.append(dict(cls=t, states=[dict(state=''.join(map(str, states[i])), kdeg=kdeg[i], **info[i]) for i in g],
                            viol_types=Counter(('D1' if info[i]['D1fail'] else '') + ('D2' if info[i]['D2fail'] else '') for i in vs)))
    return dict(hole=h, pid_bad=pid_bad, states=S, classes=len(cl), cls=sorted(cl), pi=piinfo, allDLcyc=sorted(cyclens),
                cycClasses=sorted([sum(1 for i in groups[r] if i in oncyc), sum(1 for i in groups[r] if info[i]['kind'] == 'F')]
                                  for r in groups if any(i in oncyc for i in groups[r]))), det

if __name__ == '__main__':
    path, name, hole = sys.argv[1], sys.argv[2], sys.argv[3]; detail = '--detail' in sys.argv
    rot = read(path, name)
    holes = [v for v in range(len(rot)) if len(rot[v]) == 5] if hole == '5' else [int(hole)]
    for h in holes:
        res, det = analyse(rot, h, detail)
        print(json.dumps(dict(graph=name, **res)), flush=True)
        for d in det:
            for st in d['states']: st.pop('pi', None)
            print(json.dumps(d, default=list), flush=True)
