#!/usr/bin/env python3
"""Track A library [exploratory]: faithful frame-class filter for R* (FrameF3.RStarFrame).

Frame class = connected spherical triangulation, min degree >= 5, NoSep (every triangle facial),
no Occ of DiamondM / DiamondP / C2122M / C2122P.  The Occ rotation facts and degree vectors are PARSED
from the Lean files (StudioMathLean/.../PlaneMap/*Occ.lean), so this is the Lean definition, not a proxy.

Graph format: rotation lists rot[v] = neighbours of v in cyclic order (picyc input line: "name n r0;r1;...").
Convention: Nx T u a b  <=>  b follows a in rot[u].  The mirror convention is covered automatically because
each configuration is checked in both orientations (M and P are mirror images: verified in selftest()).

Also computed (for cross-checks only): Appears (Lean AppearsOcc.Appears: injective interior inducing K4-e with
the degree vector) and TipsClean (every common neighbour of the two tips is a centre).
"""
import os, re, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(HERE, '../StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/')
CONFIGS = ('DiamondM', 'DiamondP', 'C2122M', 'C2122P')


def _parse(t):
    m = re.match(r'(ring|int) (\d+)', t.strip('() '))
    return (m.group(1), int(m.group(2)))


def load_occ(ns):
    src = open(LEAN + ns + 'Occ.lean').read().split('structure Occ')[1].split('\ntheorem')[0]
    facts = [tuple(_parse(x) for x in re.findall(r'\((?:ring|int) \d+\)', l)) for l in src.splitlines() if ': Nx T' in l]
    degs = [int(x) for x in re.search(r'!\[([\d, ]+)\]', src.split('deg :')[1]).group(1).split(',')]
    assert 'ring_inj : Function.Injective ring' in src and 'int_inj : Function.Injective int' in src and 'disj : ∀ t a, ring t ≠ int a' in src
    other = [l for l in src.splitlines()[1:] if l.strip() and ': Nx T' not in l and not any(k in l for k in ('ring_inj', 'int_inj', 'disj', 'deg :'))]
    assert not other, other  # no other fields: the structure is exactly injectivity + degrees + Nx facts
    R = 1 + max(i for f in facts for k, i in f if k == 'ring')
    return dict(ns=ns, facts=facts, degs=degs, R=R, I=len(degs))


OCC = {ns: load_occ(ns) for ns in CONFIGS}
GAMMA = {'Diamond': [5, 5, 5, 5], 'C2122': [6, 5, 5, 5]}


def parse_line(line):
    name, n, r = line.split(' ', 2)
    rot = [[int(x) for x in s.split(',')] for s in r.strip().split(';')]
    assert len(rot) == int(n)
    return name, rot


def rot_line(name, rot):
    return '%s %d %s' % (name, len(rot), ';'.join(','.join(map(str, r)) for r in rot))


def rot_from_faces(F):
    """oriented faces (a,b,c) -> rotation lists, relabelled 0..n-1 by sorted label (same as jobas/flipsearch.rotation)."""
    labels = sorted({x for t in F for x in t}); m = {u: i for i, u in enumerate(labels)}; nxt = {}
    for t in F:
        for i in range(3): nxt.setdefault(m[t[i]], {})[m[t[(i + 1) % 3]]] = m[t[(i + 2) % 3]]
    rot = []
    for v in range(len(labels)):
        s = min(nxt[v]); r = [s]
        while nxt[v][r[-1]] != s: r.append(nxt[v][r[-1]])
        rot.append(r[::-1])
    return rot


def faces_from_rot(rot):
    F = set()
    for v, r in enumerate(rot):
        for i in range(len(r)):
            t = (v, r[(i + 1) % len(r)], r[i]); k = min(range(3), key=lambda s: t[s]); F.add(t[k:] + t[:k])
    return sorted(F)


class G:
    def __init__(self, rot):
        self.rot = rot; self.n = len(rot)
        self.adj = [set(r) for r in rot]; self.deg = [len(r) for r in rot]
        self.nxt = {}; self.prv = {}
        for u, r in enumerate(rot):
            d = len(r)
            for i in range(d):
                self.nxt[(u, r[i])] = r[(i + 1) % d]; self.prv[(u, r[(i + 1) % d])] = r[i]

    # ---- basic class checks
    def is_triangulation(self):
        n = self.n
        if any(len(set(r)) != len(r) or u in r for u, r in enumerate(self.rot)): return False
        if any(u not in self.adj[w] for u in range(n) for w in self.adj[u]): return False
        E = sum(self.deg) // 2
        if E != 3 * n - 6: return False
        # every consecutive pair (w, x) at u closes a triangle with one global orientation:
        # A: at w, u follows x; at x, w follows u.   B (mirror): at w, x follows u; at x, u follows w.
        okA = okB = True
        for u in range(n):
            for w in self.rot[u]:
                x = self.nxt[(u, w)]
                if x not in self.adj[w]: return False
                okA = okA and self.nxt[(w, x)] == u and self.nxt[(x, u)] == w
                okB = okB and self.nxt[(w, u)] == x and self.nxt[(x, w)] == u
        if not (okA or okB): return False
        if len(self.faces()) != 2 * n - 4: return False
        return self.connected()

    def connected(self):
        seen = {0}; st = [0]
        while st:
            u = st.pop()
            for w in self.adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        return len(seen) == self.n

    def faces(self):
        return {frozenset((u, w, self.nxt[(u, w)])) for u in range(self.n) for w in self.rot[u]}

    def nosep(self):
        F = self.faces()
        for a in range(self.n):
            for b in self.adj[a]:
                if b <= a: continue
                for c in self.adj[a] & self.adj[b]:
                    if c > b and frozenset((a, b, c)) not in F: return False
        return True

    def n_sep_triangles(self):
        F = self.faces(); k = 0
        for a in range(self.n):
            for b in self.adj[a]:
                if b <= a: continue
                for c in self.adj[a] & self.adj[b]:
                    if c > b and frozenset((a, b, c)) not in F: k += 1
        return k

    # ---- Occ (Lean definition)
    def occ(self, ns, limit=10 ** 9):
        C = OCC[ns]; facts = C['facts']; degs = C['degs']; R, I = C['R'], C['I']
        found = []
        for i0 in range(self.n):
            if self.deg[i0] != degs[0]: continue
            for i1 in self.rot[i0]:
                if self.deg[i1] != degs[1]: continue
                asg = {('int', 0): i0, ('int', 1): i1}; ch = True; bad = False
                while ch and not bad:
                    ch = False
                    for (x, y, z) in facts:
                        if x in asg and y in asg and z not in asg:
                            if (asg[x], asg[y]) not in self.nxt: bad = True; break
                            asg[z] = self.nxt[(asg[x], asg[y])]; ch = True
                        elif x in asg and z in asg and y not in asg:
                            if (asg[x], asg[z]) not in self.prv: bad = True; break
                            asg[y] = self.prv[(asg[x], asg[z])]; ch = True
                if bad or len(asg) < R + I: continue
                if not all(self.nxt.get((asg[x], asg[y])) == asg[z] for x, y, z in facts): continue
                vals = list(asg.values())
                if len(set(vals)) != len(vals): continue
                if not all(self.deg[asg[('int', a)]] == degs[a] for a in range(I)): continue
                found.append(([asg[('ring', t)] for t in range(R)], [asg[('int', a)] for a in range(I)]))
                if len(found) >= limit: return found
        return found

    def occ_counts(self, limit=10 ** 9):
        return {ns: len(self.occ(ns, limit)) for ns in CONFIGS}

    # ---- Appears (Lean AppearsOcc.Appears) + TipsClean
    def appears(self, kind):
        g = GAMMA[kind]; out = []
        for i0 in range(self.n):
            if self.deg[i0] != g[0]: continue
            for i2 in self.adj[i0]:
                if self.deg[i2] != g[2]: continue
                com = [x for x in self.adj[i0] & self.adj[i2] if self.deg[x] == 5]
                for i1, i3 in itertools.permutations(com, 2):
                    if i3 in self.adj[i1]: continue
                    tc = (self.adj[i1] & self.adj[i3]) <= {i0, i2}
                    out.append(((i0, i1, i2, i3), tc))
        return out

    def summary(self):
        oc = self.occ_counts()
        ap = {k: self.appears(k) for k in GAMMA}
        d = dict(n=self.n, mindeg=min(self.deg), maxdeg=max(self.deg), deg5=self.deg.count(5),
                 tri=self.is_triangulation(), nosep=self.nosep(), occ=oc,
                 app={k: len(v) for k, v in ap.items()}, app_notipsclean={k: sum(1 for _, t in v if not t) for k, v in ap.items()})
        d['diamond_free'] = oc['DiamondM'] == 0 and oc['DiamondP'] == 0
        d['c2122_free'] = oc['C2122M'] == 0 and oc['C2122P'] == 0
        d['frame'] = d['tri'] and d['mindeg'] >= 5 and d['nosep'] and d['diamond_free'] and d['c2122_free']
        d['appears_free'] = all(v == 0 for v in d['app'].values())
        return d


def quick_frame(rot):
    """fast frame test for census sweeps: min degree, NoSep, then Occ only if an appearance exists (Occ => Appears)."""
    g = G(rot)
    if min(g.deg) < 5: return False, g, 'mindeg'
    if not g.nosep(): return False, g, 'sep'
    if not any(g.appears(k) for k in GAMMA): return True, g, 'noappear'
    oc = g.occ_counts(limit=1)
    return (all(v == 0 for v in oc.values())), g, 'occ' if any(oc.values()) else 'appear_noocc'


def selftest():
    # M and P mirror: P facts = M facts with reversed rotation (Nx u a b -> Nx u b a)
    for k in ('Diamond', 'C2122'):
        m = sorted(OCC[k + 'M']['facts']); p = sorted((x, z, y) for x, y, z in OCC[k + 'P']['facts'])
        assert m == p, k
    return True


if __name__ == '__main__':
    print('selftest', selftest(), {k: (v['R'], v['I'], v['degs'], len(v['facts'])) for k, v in OCC.items()})
