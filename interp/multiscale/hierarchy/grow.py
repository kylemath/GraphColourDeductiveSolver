# Growth (lopsided) chordless hierarchy: D_0 = a face; D_{k+1} = D_k + B_k with B_k a face (or two adjacent faces)
# outside D_k, every D_k a chordless disc (boundary induced in G).  Stops when the complement V - D is a chordless
# disc of size <= Lroot (root split).  Incremental chordless test: O(|boundary|) per candidate.
import sys, random, collections, time
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
from hier import G, check

class Grower:
    def __init__(self, g, seed_face):
        self.g = g; self.inD = [False]*g.n; self.bd = {}; self.inF = set()
        for v in g.faces[seed_face]: self.inD[v] = True
        self.inF.add(seed_face); f = g.faces[seed_face]
        for j in range(3): self.bd[f[j]] = f[(j+1) % 3]
        self.size = 3
    def try_add(self, B):
        g = self.g; inD = self.inD; Bs = set(B)
        inU = lambda x: inD[x] or x in Bs
        aff = set(Bs)
        for b in Bs:
            for w in g.adj[b]:
                if inD[w]: aff.add(w)
        newF = set(i for v in Bs for i in g.vf[v] if all(inU(x) for x in g.faces[i]))
        Fu = lambda i: i in self.inF or i in newF
        nbd = {u: w for u, w in self.bd.items() if u not in aff}
        for u in aff:
            for i in g.vf[u]:
                if not Fu(i): continue
                f = g.faces[i]; j = f.index(u); w = f[(j+1) % 3]
                if not Fu(g.face[(w, u)]):
                    if u in nbd: return None
                    nbd[u] = w
        for b in Bs:
            if not any(Fu(i) for i in g.vf[b]): return None
        # Euler characteristic change dV - dE + dF must be 0 (E = edges of G[U])
        dE = sum(1 for b in Bs for w in g.adj[b] if inD[w]) + sum(1 for b in Bs for w in g.adj[b] if w in Bs)//2
        if len(Bs) - dE + len(newF) != 0: return None
        start = next(iter(nbd)); x = nbd[start]; k = 1
        while x != start:
            if x not in nbd: return None
            x = nbd[x]; k += 1
            if k > len(nbd): return None
        if k != len(nbd): return None
        for x in aff:   # induced: changed boundary vertices see exactly 2 boundary vertices
            if x in nbd and sum(1 for w in g.adj[x] if w in nbd) != 2: return None
        return nbd, newF
    def commit(self, B, res):
        nbd, newF = res
        for b in B: self.inD[b] = True
        self.inF |= newF; self.bd = nbd; self.size += len(B)

def grow(g, seed=0, Lroot=40, maxB=4, rule='fill', wheels=True):
    rng = random.Random(seed); n = g.n
    S = Grower(g, rng.randrange(len(g.faces))); leaves = [3]
    if wheels:   # seed with a closed neighbourhood
        v0 = rng.randrange(n); S = Grower(g, g.vf[v0][0]); B0 = (g.adj[v0] | {v0}) - set(g.faces[g.vf[v0][0]]); r = S.try_add(B0)
        if r: S.commit(B0, r); leaves = [len(g.adj[v0])+1]; t = time.time(); best_root = None
    while True:
        W = n - S.size
        if W <= Lroot:
            Wset = set(v for v in range(n) if not S.inD[v])
            if W >= 3 and check(g, Wset)[0] == 'ok':
                return dict(ok=True, steps=len(leaves), leaves=dict(collections.Counter(leaves)), root=(S.size, W), sec=round(time.time()-t, 1))
        cand = {}
        for u in S.bd:
            for i in g.vf[u]:
                for x in g.faces[i]:
                    for k in g.vf[x]:
                        f = g.faces[k]
                        if not any(S.inD[y] for y in f):
                            key = frozenset(f)
                            if key not in cand: cand[key] = sum(1 for y in f for w in g.adj[y] if S.inD[w])
        if maxB >= 4:
            for key in list(cand):
                for x in key:
                    for k in g.vf[x]:
                        f = frozenset(g.faces[k])
                        if f in cand and len(f & key) == 2:
                            k2 = f | key
                            if k2 not in cand: cand[k2] = sum(1 for y in k2 for w in g.adj[y] if S.inD[w])
        if wheels:
            near = set(w for u in S.bd for w in g.adj[u] if not S.inD[w])
            near2 = near | set(x for w in near for x in g.adj[w] if not S.inD[x])
            for v in near2:
                Bv = frozenset(x for x in g.adj[v] | {v} if not S.inD[x])
                if Bv not in cand and len(Bv) >= 3 and check(g, set(Bv))[0] == 'ok':
                    cand[Bv] = sum(1 for y in Bv for w in g.adj[y] if S.inD[w])
        if rule == 'fill': order = sorted(cand, key=lambda B: (-cand[B]/len(B), rng.random()))
        else: order = sorted(cand, key=lambda B: rng.random())
        done = False
        for B in order:
            r = S.try_add(B)
            if r is not None:
                S.commit(B, r); leaves.append(len(B)); done = True; break
        if not done:
            return dict(ok=False, steps=len(leaves), stuck_at=(S.size, n-S.size), sec=round(time.time()-t, 1))
