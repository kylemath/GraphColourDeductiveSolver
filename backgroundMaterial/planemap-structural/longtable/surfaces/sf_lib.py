#!/usr/bin/env python3
"""Surfaces experiment helpers: engine pipe (sf_eng), graph defects, face-list complexes."""
import subprocess, json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'sf_eng')
CLSF = ['size', 'filled', 'DL', 'onCyc', 'n8', 'n9', 'n10p', 'lawFail', 'r7Fail', 'h3Fail', 'minK', 'maxK', 'nonDLunf', 'exc', 'h3imb', 'root']


class Engine:
    def __init__(self, allholes=False, hole=0, maxstates=60000):
        args = [ENG, '--maxstates', str(maxstates)] + (['--allholes'] if allholes else ['--hole', str(hole)])
        self.p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def run(self, line, nholes=1):
        self.p.stdin.write(line.strip() + '\n'); self.p.stdin.flush()
        return [json.loads(self.p.stdout.readline()) for _ in range(nholes)]

    def close(self):
        self.p.stdin.close(); self.p.wait()


def cls_dicts(js):
    return [dict(zip(CLSF, c)) for c in js.get('cls', [])]


def to_line(name, adj):
    return f"{name} {len(adj)} " + ';'.join(','.join(map(str, a)) for a in adj)


def parse_line(l):
    p = l.split()
    return p[0], [list(map(int, r.split(','))) if r else [] for r in p[2].split(';')]


def tri_counts(adj):
    S = [set(a) for a in adj]
    t = {}
    for u in range(len(adj)):
        for v in adj[u]:
            if v > u: t[(u, v)] = len(S[u] & S[v])
    return t


def link_components(adj, v):
    S = [set(a) for a in adj]; nb = S[v]; seen = set(); comps = 0
    for x in nb:
        if x in seen: continue
        comps += 1; st = [x]; seen.add(x)
        while st:
            y = st.pop()
            for z in S[y] & nb:
                if z not in seen: seen.add(z); st.append(z)
    return comps


def link_is_cycles(adj, v):
    S = [set(a) for a in adj]; nb = S[v]
    return all(len(S[x] & nb) == 2 for x in nb)


def defects(adj):
    """graph-level: edges not in exactly two triangles, sum |t-2|, vertices whose link is not 2-regular,
    vertices whose link is not a single cycle, sum (link comps - 1)."""
    t = tri_counts(adj)
    bad_e = sum(1 for x in t.values() if x != 2); dA = sum(abs(x - 2) for x in t.values())
    nonreg = sum(1 for v in range(len(adj)) if not link_is_cycles(adj, v))
    comps = [link_components(adj, v) for v in range(len(adj))]
    noncyc = sum(1 for v in range(len(adj)) if not (link_is_cycles(adj, v) and comps[v] == 1))
    return dict(edges=len(t), bad_edges=bad_e, dA=dA, nonreg_links=nonreg, noncycle_links=noncyc,
                extra_comps=sum(c - 1 for c in comps if c > 0), dB=dA + sum(c - 1 for c in comps if c > 0))


# ---------- face-list complexes ----------

def edges_of(F):
    E = defaultdict(list)
    for i, f in enumerate(F):
        a, b, c = f
        for e in ((a, b), (b, c), (a, c)):
            E[tuple(sorted(e))].append(i)
    return E


def is_pseudo(F):
    return all(len(x) == 2 for x in edges_of(F).values())


def vlinks(F):
    L = defaultdict(list)
    for a, b, c in F:
        L[a].append((b, c)); L[b].append((a, c)); L[c].append((a, b))
    return L


def link_cycles(F, v=None):
    """number of cycles in the link of each vertex (link edges = opposite edges of faces at v)."""
    L = vlinks(F); out = {}
    for x in (L if v is None else [v]):
        adj = defaultdict(list)
        for p, q in L[x]: adj[p].append(q); adj[q].append(p)
        seen = set(); k = 0
        for s in adj:
            if s in seen: continue
            k += 1; st = [s]; seen.add(s)
            while st:
                y = st.pop()
                for z in adj[y]:
                    if z not in seen: seen.add(z); st.append(z)
        out[x] = k
    return out


def link_order(F, v):
    """cyclic order of the link of v if it is one cycle, else None"""
    L = vlinks(F)[v]
    adj = defaultdict(list)
    for p, q in L: adj[p].append(q); adj[q].append(p)
    if any(len(a) != 2 for a in adj.values()): return None
    s = next(iter(adj)); order = [s]; prev = None; cur = s
    while True:
        nx = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        if nx == s: break
        order.append(nx); prev, cur = cur, nx
    return order if len(order) == len(adj) else None


def complex_to_adj(F):
    """relabel vertices 0..n-1; adjacency lists with cyclic order for single-cycle links"""
    V = sorted({x for f in F for x in f}); idx = {v: i for i, v in enumerate(V)}
    G = defaultdict(set)
    for a, b, c in F:
        for p, q in ((a, b), (b, c), (a, c)): G[p].add(q); G[q].add(p)
    adj = []
    for v in V:
        o = link_order(F, v)
        adj.append([idx[x] for x in (o if o is not None else sorted(G[v]))])
    return adj, idx


def euler(F):
    V = {x for f in F for x in f}
    return len(V) - len(edges_of(F)) + len(F)


def orientable(F):
    """orientability of a pseudo-surface via face orientation propagation"""
    E = edges_of(F); ori = [0] * len(F)
    def dir_edges(k):
        x, y, z = F[k]; d = [(x, y), (y, z), (z, x)]
        return d if ori[k] == 1 else [(b, a) for a, b in d]
    for s0 in range(len(F)):
        if ori[s0]: continue
        ori[s0] = 1; st = [s0]
        while st:
            i = st.pop()
            for p, q in dir_edges(i):
                for k in E[tuple(sorted((p, q)))]:
                    if k == i: continue
                    x, y, z = F[k]; nat = [(x, y), (y, z), (z, x)]
                    want = 1 if (q, p) in nat else -1
                    if ori[k] == 0: ori[k] = want; st.append(k)
                    elif ori[k] != want: return False
    return True
