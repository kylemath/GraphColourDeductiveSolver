"""Null configurations.

N1 (shape kept): each config keeps its embedded interior shape; its degree
    multiset is shuffled over its vertices (feasible: fully interior vertices
    keep deg == interior degree; others deg >= interior degree + gaps).
N2 (random shape): an induced disc patch with m vertices from a random
    triangulated torus (min degree 5, max 11, random flips), accepted only when
    its boundary walk length L matches the paired config (so the ring size is
    matched too, ring = sum(deg) - 6m + 6 + L), then the paired config's degree
    multiset is assigned feasibly at random.
"""
import random
from collections import defaultdict, deque


def feasible_assign(multiset, intdeg, gaps, rng, tries=300):
    m = len(intdeg)
    fixed = [v for v in range(m) if gaps[v] == 0]
    for _ in range(tries):
        ms = list(multiset)
        rng.shuffle(ms)
        deg = [None] * m
        ok = True
        # fixed vertices need exact values
        for v in fixed:
            if intdeg[v] in ms:
                ms.remove(intdeg[v])
                deg[v] = intdeg[v]
            else:
                ok = False
                break
        if not ok:
            return None
        free = [v for v in range(m) if gaps[v] > 0]
        rng.shuffle(free)
        for v, x in zip(free, ms):
            if x < intdeg[v] + gaps[v]:
                ok = False
                break
            deg[v] = x
        if ok:
            return deg
    return None


def n1(cfgs, rng):
    out = []
    for c in cfgs:
        intdeg = [len(r) for r in c['irot']]
        d = feasible_assign(c['deg'], intdeg, c['gaps'], rng)
        if d is None:
            d = list(c['deg'])
        out.append(dict(m=c['m'], deg=d, irot=c['irot'], gaps=c['gaps']))
    return out


class Torus:
    def __init__(self, W, H, rng, flips):
        self.rng = rng
        idx = lambda x, y: (x % W) + W * (y % H)
        self.n = W * H
        faces = set()
        for x in range(W):
            for y in range(H):
                a, b, c, d = idx(x, y), idx(x + 1, y), idx(x + 1, y + 1), idx(x, y + 1)
                faces.add((a, b, c))
                faces.add((a, c, d))
        # half-edge -> third vertex (face a,b,c ccw: he a->b has apex c)
        self.apex = {}
        for (a, b, c) in faces:
            self.apex[(a, b)] = c
            self.apex[(b, c)] = a
            self.apex[(c, a)] = b
        self.adj = defaultdict(set)
        for (a, b) in self.apex:
            self.adj[a].add(b)
        hes = list(self.apex)
        done = 0
        att = 0
        while done < flips and att < flips * 50:
            att += 1
            a, b = rng.choice(hes)
            if (a, b) not in self.apex:
                hes = list(self.apex)
                continue
            c = self.apex[(a, b)]
            d = self.apex[(b, a)]
            if c == d or d in self.adj[c]:
                continue
            if len(self.adj[a]) <= 5 or len(self.adj[b]) <= 5:
                continue
            if len(self.adj[c]) >= 11 or len(self.adj[d]) >= 11:
                continue
            # faces (a,b,c), (b,a,d) -> (c,a,d), (d,b,c)
            for he in [(a, b), (b, c), (c, a), (b, a), (a, d), (d, b)]:
                del self.apex[he]
            for (p, q, r) in [(c, a, d), (d, b, c)]:
                self.apex[(p, q)] = r
                self.apex[(q, r)] = p
                self.apex[(r, p)] = q
            self.adj[a].discard(b)
            self.adj[b].discard(a)
            self.adj[c].add(d)
            self.adj[d].add(c)
            done += 1
        # rotations
        self.rot = {}
        for v in range(self.n):
            succ = {}
            for w in self.adj[v]:
                succ[w] = self.apex[(v, w)]  # face v,w,apex ccw -> next nbr ccw after w is apex? use consistent order
            w0 = next(iter(self.adj[v]))
            seq = [w0]
            w = succ[w0]
            while w != w0:
                seq.append(w)
                w = succ[w]
            assert len(seq) == len(self.adj[v])
            self.rot[v] = seq

    def patch(self, m, rng):
        s = rng.randrange(self.n)
        S = [s]
        inS = {s}
        while len(S) < m:
            cand = defaultdict(int)
            for v in S:
                for w in self.adj[v]:
                    if w not in inS:
                        cand[w] += 1
            ws = list(cand)
            wt = [cand[w] ** 3 for w in ws]
            w = rng.choices(ws, wt)[0]
            S.append(w)
            inS.add(w)
        # complement connected (no holes): local check on ring + 2 layers
        ring = {w for v in S for w in self.adj[v] if w not in inS}
        start = next(iter(ring))
        seen = {start}
        q = deque([start])
        lim = set(ring)
        for w in list(ring):
            lim |= {x for x in self.adj[w] if x not in inS}
        lim2 = set(lim)
        for w in list(lim):
            lim2 |= {x for x in self.adj[w] if x not in inS}
        while q:
            v = q.popleft()
            for w in self.adj[v]:
                if w in lim2 and w not in inS and w not in seen:
                    seen.add(w)
                    q.append(w)
        if not ring <= seen:
            return None
        idx = {v: i for i, v in enumerate(S)}
        irot = [[idx[w] for w in self.rot[v] if w in inS] for v in S]
        gaps = []
        for v in S:
            st = ''.join('I' if w in inS else 'R' for w in self.rot[v])
            if 'R' not in st:
                gaps.append(0)
            else:
                gaps.append(sum(1 for i in range(len(st)) if st[i] == 'R' and st[i - 1] == 'I'))
        return dict(m=m, irot=irot, gaps=gaps)


def n2(cfgs, rng, host, maxtry=20000):
    out = []
    fail = 0
    for c in cfgs:
        L = sum(c['gaps'])
        got = None
        for _ in range(maxtry):
            p = host.patch(c['m'], rng)
            if p is None or sum(p['gaps']) != L:
                continue
            intdeg = [len(r) for r in p['irot']]
            d = feasible_assign(c['deg'], intdeg, p['gaps'], rng, tries=50)
            if d is None:
                continue
            p['deg'] = d
            got = p
            break
        if got is None:
            fail += 1
            continue
        out.append(got)
    return out, fail
