# Multi-front, turn-taking version of the vortex-restricted uncapped-cut induction (../unbounded/vr.py model).
# m seed faces (farthest-point, pairwise far apart); each seed = a "tag" (front). Tags take turns adding one uncoloured
# vertex adjacent to their own cell (equal speed => graph-Voronoi cells). The invariant is kept on EVERY boundary walk
# of the coloured region (one walk per complement component; walks may be pinched; annuli = two walks):
#   circumradius <= 1 of the lifted walk after cuts with jumps in 2*Lambda (variant 'any'), |t| free,
#   cut positions persistent darts; new positions only at vortex steps (dn new interior odd vertices), departed
#   positions re-assigned to the darts at v; budget of non-carried cuts NB = #departed + dn, POOLED over the new walks.
# Boundary structure is computed locally from the rotation system: dart (a->u) is a boundary dart iff a, u coloured and
# the cw-successor of a around u is uncoloured; succ(a->u) = (u->c), c the next coloured neighbour cw after a.
# Gauge flip at a corner (a->u->c) = parity of #edges strictly between c and a on the region side (deg-2-gap);
# for a simple corner this is degp-2, as in pi.signs.
# Step: choose v among the top-K candidates of the tag (most coloured neighbours first), minimal R (ball in the present
# graph, boundary vertices of OTHER walks frozen), then (cuts, sum|t|, #recoloured). Exact multi-walk DFS with the DP
# frontier of mc.py, SAT extension of free interior vertices.
import sys, os, json, time, random, pickle, collections, itertools, math
sys.dont_write_bytecode = True
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/unbounded/')
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/')
import vr, mc
from vr import FrontierVR, BIG
from pi import make, rotation, check_proper, ball
from pysat.solvers import Cadical153
L18 = '/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'
OUT = '/mnt/project-files/multiscale/multicut/multifront/'

def mkmap(name):
    if name == 'L18': return [set(a) for a in json.load(open(L18))['adj']]
    if name.startswith('rigid_'): return [set(a) for a in json.load(open('/mnt/project-files/multiscale/opus_attack/control/rigid/maps/%s.json' % name[6:]))['adj']]
    return make(name)

class FP(FrontierVR):
    """FrontierVR with an instance budget NB; close2 returns (min new-cut count, cuts) or None."""
    def __init__(self, J, odd, variant, T, NB):
        FrontierVR.__init__(self, J, odd, variant, T); self.NB = NB
    def adv(self, F, p, allow=True):
        s = FrontierVR.NB; FrontierVR.NB = self.NB
        try: return FrontierVR.adv(self, F, p, allow)
        finally: FrontierVR.NB = s
    def close2(self, F, HL, allow=True):
        best = None; NB = self.NB
        allow = 1 if allow is True else (0 if allow is False or allow is None else allow)
        for (a, ph, x, y, m, cn), c in F.items():
            for use in (0, 1):
                if use and not allow: continue
                cn2 = cn + (1 if (use and allow == 2) else 0)
                if cn2 > NB: continue
                if not self.odd:
                    if ph != 0: continue
                    dx, dy = x - HL[0], y - HL[1]
                    if not use:
                        if (dx, dy) != (0, 0): continue
                        cc = c
                    else:
                        if not ((-dx, -dy) in mc.UI and self._jump_ok(m, mc.UI[(-dx, -dy)])): continue
                        cc = c + 1
                else:
                    if ph == 0:
                        if not use: continue
                        cc = c + 1
                    else:
                        dx, dy = x - HL[0], y - HL[1]
                        if not use:
                            if (dx, dy) != (0, 0): continue
                            cc = c
                        else:
                            if not ((dx, dy) in mc.UI and self._jump_ok(m, mc.UI[(dx, dy)])): continue
                            cc = c + 1
                key = (cn2, cc)
                if best is None or key < best: best = key
        return best

class MF:
    def __init__(self, adj, m, seed, K=5, Rmax=4, variant='any', ren=False, D=None, mb=0, tz=False):
        self.adj = adj; n = len(adj); self.n = n
        rot, emb = rotation(adj); self.rot = rot
        self.ix = [{w: i for i, w in enumerate(rot[u])} for u in range(n)]
        self.rng = random.Random(seed); self.K = K; self.Rmax = Rmax; self.variant = variant; self.ren = ren; self.mb = mb; self.tz = tz
        self.present = [False]*n; self.col = {}; self.unc = [len(adj[u]) for u in range(n)]
        self.tag = [-1]*n; self.posn = set(); self.nodd = 0
        self.node_cap = int(os.environ.get('NCAP', '300000')); self.cand_cap = int(os.environ.get('CCAP', '20000'))
        # seeds: farthest-point sampling
        def bfs(srcs):
            d = [-1]*n; q = collections.deque(srcs)
            for s in srcs: d[s] = 0
            while q:
                x = q.popleft()
                for y in adj[x]:
                    if d[y] < 0: d[y] = d[x]+1; q.append(y)
            return d
        s0 = self.rng.randrange(n); d0 = bfs([s0]); far = max(range(n), key=lambda x: d0[x])
        self.diam = max(bfs([far]))
        seeds = [self.rng.randrange(n)]
        while len(seeds) < m:
            d = bfs(seeds); best = max(d); seeds.append(self.rng.choice([x for x in range(n) if d[x] == best]))
        faces = []; used = set()
        for s in seeds:
            opts_ = [(s, rot[s][i], rot[s][(i+1) % len(rot[s])]) for i in range(len(rot[s]))]
            good = [f for f in opts_ if not any(x in used or (adj[x] & used) for x in f)]
            if not good: raise RuntimeError('seed faces collide')
            f = good[0]; faces.append(f); used |= set(f)
        self.mind = min([bfs([f[0]])[g[0]] for f, g in itertools.combinations(faces, 2)], default=None)
        # seed faces must be pairwise disjoint and non-adjacent
        for i, f in enumerate(faces):
            for j, x in enumerate(f):
                assert not self.present[x]; self.present[x] = True; self.col[x] = j; self.tag[x] = i
        for f in faces:
            for x in f:
                for y in adj[x]: self.unc[y] -= 1
        for f in faces:
            for x in f:
                for y in adj[x]:
                    if self.present[y]: assert self.tag[y] == self.tag[x], 'seeds adjacent'
        self.m = m; self.uf = list(range(m)); self.recs = []; self.events = []; self.holes = []
        self.front = [set(y for x in f for y in adj[x] if not self.present[y]) for f in faces]

    def find(self, a):
        while self.uf[a] != a: self.uf[a] = self.uf[self.uf[a]]; a = self.uf[a]
        return a
    def nb(self, x): return [y for y in self.adj[x] if self.present[y]]
    # ---------- boundary structure ----------
    def is_bd(self, a, u):
        r = self.rot[u]; return self.present[a] and self.present[u] and not self.present[r[(self.ix[u][a] + 1) % len(r)]]
    def succ(self, a, u):
        r = self.rot[u]; d = len(r); i = self.ix[u][a]
        for k in range(1, d+1):
            c = r[(i + k) % d]
            if self.present[c]: return c, k - 1          # gap size
        raise RuntimeError('isolated')
    def trace(self, a, u):
        """walk starting with dart (a->u): returns B (vertex list; edge j = B[j]->B[j+1]) and flips per vertex."""
        B = [a]; start = (a, u); cur = (a, u); fl = []
        while True:
            x, y = cur; c, g = self.succ(x, y)
            B.append(y); fl.append((len(self.rot[y]) - 2 - g) % 2)
            cur = (y, c)
            if cur == start: break
            if len(B) > 4*self.n: raise RuntimeError('trace loop')
        # B = [a, u, ..., ] where B[-1] is the vertex before a; fl[i] is the flip at B[i+1]
        B = B[:-1] if False else B
        # rotate representation: vertices V[0..L-1] with V[0] = u ... V[L-1] = a
        V = B[1:]; F = fl                                 # V[i] has flip F[i]; edges V[i] -> V[i+1], V[L-1] -> V[0]
        return V, F
    def walks_at(self, v):
        """all walks through v (v present): list of (V, flips), deduplicated by dart sets."""
        r = self.rot[v]; d = len(r); out = []; seen = set()
        for i in range(d):
            a = r[i]
            if self.present[a] and not self.present[r[(i+1) % d]]:
                if (a, v) in seen: continue
                V, Fl = self.trace(a, v)
                L = len(V); ds = set((V[j], V[(j+1) % L]) for j in range(L))
                seen |= ds; out.append((V, Fl))
        return out
    @staticmethod
    def signs(Fl):
        s = [1];
        for f in Fl[1:]: s.append(s[-1] * (-1 if f else 1))
        closing = s[-1] * (-1 if Fl[0] else 1)
        return s, closing != 1
    def H_of(self, V, s, col):
        L = len(V); lab = [col[V[i]] ^ col[V[(i+1) % L]] for i in range(L)]
        if 0 in lab: return None
        return mc.int_walk(lab, s)
    # ---------- tentative step ----------
    def arcs(self, v):
        r = self.rot[v]; d = len(r); pres = [self.present[x] for x in r]
        if all(pres): return 'close', 1
        if not any(pres): return None, 0
        i0 = next(i for i in range(d) if not pres[i]); runs = []; cur = 0
        for k in range(1, d+1):
            if pres[(i0+k) % d]: cur += 1
            else:
                if cur: runs.append(cur)
                cur = 0
        if len(runs) == 1 and runs[0] < 2: return None, 0
        return ('grow' if len(runs) == 1 else 'multi'), len(runs)
    def setup(self, v):
        """mark v present (caller must undo with unsetup); returns step context."""
        dep = [p for p in self.posn if self.rot[p[1]][(self.ix[p[1]][p[0]] + 1) % len(self.rot[p[1]])] == v]
        self.present[v] = True
        for y in self.adj[v]: self.unc[y] -= 1
        dnv = [y for y in self.adj[v] if self.present[y] and self.unc[y] == 0 and len(self.adj[y]) % 2]
        if self.unc[v] == 0 and len(self.adj[v]) % 2: dnv.append(v)
        W = []
        for V, Fl in self.walks_at(v):
            s, odd = self.signs(Fl); W.append(dict(V=V, s=s, odd=odd, flat=(self.tz and not odd and self.is_flat(V))))
        dn = len(dnv); NB = len(dep) + dn
        ncomp = len(set(self.find(self.tag[y]) for y in self.adj[v] if self.present[y] and y != v))
        mrg = self.mb if ncomp >= 2 else 0; NB += mrg
        depset = set(dep)
        for w in W:
            V = w['V']; L = len(V); al = [0]*L
            for j in range(L):
                if (V[j], V[(j+1) % L]) in self.posn and (V[j], V[(j+1) % L]) not in depset: al[j] = 1
            new = set()
            for j in range(L):
                if V[j] == v:
                    if dep or mrg: new |= {(j-1) % L, j}
                    if dn: new |= {(j-1) % L, j, (j+1) % L}
            for j in new:
                if al[j] == 0: al[j] = 2
            w['al'] = al
        return dict(v=v, W=W, dep=dep, dn=dn, NB=NB, dnv=dnv, mrg=mrg)
    def is_flat(self, V):
        """no odd-degree vertex on the walk nor in the uncoloured component on its gap side (early exit)."""
        adj = self.adj
        if any(len(adj[x]) % 2 for x in V): return False
        L = len(V); st = None
        for j in range(L):
            a, u = V[(j-1) % L], V[j]; ru = self.rot[u]; z = ru[(self.ix[u][a] + 1) % len(ru)]
            if not self.present[z]: st = z; break
        if st is None: return False
        seen = {st}; q = [st]
        while q:
            x = q.pop()
            if len(adj[x]) % 2: return False
            for y in adj[x]:
                if not self.present[y] and y not in seen: seen.add(y); q.append(y)
        return True
    def unsetup(self, v):
        self.present[v] = False
        for y in self.adj[v]: self.unc[y] += 1
    # ---------- exact multi-walk solver ----------
    def solve(self, ctx, R):
        v = ctx['v']; W = ctx['W']; col = self.col; NB = ctx['NB']
        onw = set(x for w in W for x in w['V'])
        F0 = ball(self.nb, v, R)
        F = [x for x in F0 if x == v or x in onw or self.unc[x] == 0]       # freeze boundary vertices of other walks
        Fs = set(F); FBs = set(x for x in onw if x in Fs); FI = [x for x in F if x not in onw]
        nbs = {x: self.nb(x) for x in F}
        allowed = {}
        for x in FBs:
            a = [c for c in range(4) if all(col[y] != c for y in nbs[x] if y not in Fs)]
            if x in col and col[x] in a: a.remove(col[x]); a.insert(0, col[x])
            allowed[x] = a
        WS = []
        for w in W:
            V = w['V']; L = len(V); s = w['s']; odd = w['odd']; al = w['al']
            fixed = [b not in FBs for b in V]
            if all(fixed): i0 = 0
            else:
                st = next(j for j in range(L) if not fixed[j]); best = (0, 0); cur = None
                for kk in range(1, L+1):
                    idx = (st + kk) % L
                    if fixed[idx]:
                        if cur is None: cur = [idx, 1]
                        else: cur[1] += 1
                        if cur[1] > best[1]: best = tuple(cur)
                    else: cur = None
                i0 = best[0] if best[1] > 0 else 0
            Bv = V[i0:] + V[:i0]; sv = s[i0:] + [(-1 if odd else 1)*x for x in s[:i0]]
            alv = al[i0:] + al[:i0]; free = [x in FBs for x in Bv]
            fixedge = [not (free[i] or free[(i+1) % L]) for i in range(L)]
            runend = [0]*L; j = L
            for i in range(L-1, -1, -1):
                if not fixedge[i]: j = i
                runend[i] = j if fixedge[i] else i
            WS.append(dict(Bv=Bv, sv=sv, alv=alv, L=L, odd=odd, flat=w['flat'], fixedge=fixedge, runend=runend))
        cands = []; nodes = [0]; assign = {}; ncap = self.node_cap; ccap = self.cand_cap
        def colof(x): return assign[x] if x in assign else col[x]
        def opts(y):
            if y in assign: return [assign[y]]
            if y in FBs: return [c for c in allowed[y] if all(assign.get(z) != c for z in nbs[y])]
            return [col[y]]
        def walkdfs(wi, budget, cuts, ts):
            if nodes[0] > ncap or len(cands) >= ccap: return
            if wi == len(WS): cands.append((dict(assign), cuts, ts)); return
            w = WS[wi]; Fr = FP(BIG, w['odd'], self.variant, 1.0, budget); x0 = w['Bv'][0]
            for c in opts(x0):
                newly = x0 in FBs and x0 not in assign
                if newly: assign[x0] = c
                dfs(wi, w, Fr, 0, (0, 0), Fr.start(), budget, cuts, ts)
                if newly: del assign[x0]
        def dfs(wi, w, Fr, i, H, Fst, budget, cuts, ts):
            nodes[0] += 1
            if nodes[0] > ncap or len(cands) >= ccap: return
            L = w['L']; Bv = w['Bv']; sv = w['sv']; alv = w['alv']
            if i == L:
                if w['flat'] and tuple(H) != (0, 0): return
                r = Fr.close2(Fst, H, alv[L-1])
                if r is None: return
                walkdfs(wi+1, budget - r[0], cuts + r[1], ts + abs(mc.cz(H))); return
            if w['fixedge'][i]:
                jj = w['runend'][i]; Hk = H
                for kk in range(i, jj):
                    d = mc.STEP[col[Bv[kk]] ^ col[Bv[(kk+1) % L]]]; g = sv[kk]; Hk = (Hk[0] + g*d[0], Hk[1] + g*d[1])
                    if kk + 1 < L:
                        Fst = Fr.adv(Fst, Hk, alv[kk])
                        if not Fst: return
                dfs(wi, w, Fr, jj, Hk, Fst, budget, cuts, ts); return
            x = Bv[i]; y = Bv[(i+1) % L]; cx = colof(x)
            for cy in opts(y):
                if cy == cx: continue
                d = mc.STEP[cx ^ cy]; g = sv[i]; H2 = (H[0] + g*d[0], H[1] + g*d[1]); F2 = Fst
                if i+1 < L:
                    F2 = Fr.adv(Fst, H2, alv[i])
                    if not F2: continue
                newly = y in FBs and y not in assign
                if newly: assign[y] = cy
                dfs(wi, w, Fr, i+1, H2, F2, budget, cuts, ts)
                if newly: del assign[y]
        walkdfs(0, NB, 0, 0.0)
        if nodes[0] > ncap: raise RuntimeError('node cap R=%d |FB|=%d' % (R, len(FBs)))
        if not cands: return None
        cands.sort(key=lambda e: (e[1], round(e[2], 6), sum(1 for x in FBs if x != v and e[0][x] != col.get(x))))
        if not FI: a, nc, ts = cands[0]; return a, nc, ts
        ix = {x: i for i, x in enumerate(F)}; X = lambda x, c: 4*ix[x]+c+1; cls = []
        for x in F:
            cls.append([X(x, c) for c in range(4)])
            for a_, b_ in itertools.combinations(range(4), 2): cls.append([-X(x, a_), -X(x, b_)])
            for y in nbs[x]:
                if y in Fs:
                    if ix[y] > ix[x]:
                        for c in range(4): cls.append([-X(x, c), -X(y, c)])
                else: cls.append([-X(x, col[y])])
        S = Cadical153(bootstrap_with=cls)
        try:
            for a, nc, ts in cands:
                if S.solve(assumptions=[X(x, a[x]) for x in FBs]):
                    mm = set(l for l in S.get_model() if l > 0)
                    out = {x: next(c for c in range(4) if X(x, c) in mm) for x in F}
                    return out, nc, ts
            if len(cands) >= ccap: raise RuntimeError('cand cap with no extension')
            return None
        finally: S.delete()
    # ---------- commit ----------
    def commit(self, ctx, newcol, tagv):
        v = ctx['v']; self.col.update(newcol); self.tag[v] = tagv   # v already present (setup)
        self.nodd += ctx['dn']
        newpos = set(self.posn) - set(ctx['dep'])
        # recompute positions on the new walks: carried + used new darts (pooled budget), plus dormant slots
        W = ctx['W']; NB = ctx['NB']; used = 0; info = []; overrun = 0
        for w in W:
            V = w['V']; L = len(V); H = self.H_of(V, w['s'], self.col); assert H is not None
            for j in range(L): newpos.discard((V[j], V[(j+1) % L]))
            FrontierVR.NB = max(0, NB - used)
            cuts = mc.cut_positions(H, w['odd'], BIG, self.variant, 1.0, w['al'])
            if cuts is None:
                FrontierVR.NB = BIG; cuts = mc.cut_positions(H, w['odd'], BIG, self.variant, 1.0, w['al']); overrun += 1
            un = [j for j in cuts if w['al'][j] == 2]; used += len(un)
            for j in cuts: newpos.add((V[j], V[(j+1) % L]))
            w['cuts'] = cuts; w['t'] = abs(mc.cz(H[-1])); w['H'] = H
            info.append((L, len(cuts), round(w['t'], 3), int(w['odd'])))
        slots = NB - used
        for w in W:
            V = w['V']; L = len(V)
            for j in range(L):
                if slots <= 0: break
                e = (V[j], V[(j+1) % L])
                if w['al'][j] == 2 and e not in newpos: newpos.add(e); slots -= 1
        self.posn = newpos
        for y in self.adj[v]:
            if not self.present[y]: self.front[tagv].add(y)
        return info, overrun

    def candidates(self, tg):
        fr = self.front[tg]; out = []
        for x in list(fr):
            if self.present[x]: fr.discard(x); continue
            kind, na = self.arcs(x)
            if kind is None: continue
            nc = sum(1 for y in self.adj[x] if self.present[y])
            out.append((-nc, self.rng.random(), x, kind))
        out.sort(); return out

    def try_v(self, v, R):
        ctx = self.setup(v)
        try: res = self.solve(ctx, R)
        except RuntimeError as e: self.unsetup(v); raise
        if res is None: self.unsetup(v); return None, ctx
        return res, ctx

    def turn(self, tg, k):
        cs = self.candidates(tg)[:self.K]
        if not cs: return 'none'
        for R in range(0, self.Rmax + 1):
            best = None
            for _, _, v, kind in cs:
                comps = set(self.find(self.tag[y]) for y in self.adj[v] if self.present[y])
                perms = [None]
                if self.ren and len(comps) == 2 and R == 0:
                    other = [c for c in comps if c != self.find(tg)]
                    if other: perms = [None] + [p for p in itertools.permutations(range(4)) if p != (0, 1, 2, 3)]
                for p in perms:
                    saved = None
                    if p is not None:
                        oc = other[0]; saved = {x: c for x, c in self.col.items() if self.find(self.tag[x]) == oc}
                        for x, c in saved.items(): self.col[x] = p[c]
                    res, ctx = self.try_v(v, R)
                    if res is not None:
                        key = (res[1], round(res[2], 6))
                        if best is None or key < best[0]: best = (key, v, res, ctx, p, kind, comps)
                        self.unsetup(v)
                    if saved is not None: self.col.update(saved)
            if best is not None:
                key, v, res, ctx, p, kind, comps = best
                if p is not None:
                    oc = [c for c in comps if c != self.find(tg)][0]
                    for x in [x for x in self.col if self.find(self.tag[x]) == oc]: self.col[x] = p[self.col[x]]
                ctx = self.setup(v)   # recompute context in the final colouring state
                # re-solve to get a consistent colouring (deterministic)
                res2 = self.solve(ctx, R)
                assert res2 is not None
                ntags = set(self.tag[y] for y in self.adj[v] if self.present[y] and y != v)
                pre_hole = None
                if kind == 'close':
                    # the hole walk before closing: link of v
                    self.unsetup(v); r = self.rot[v]
                    a = r[0]; Vh, Fh = self.trace(r[1], a) if False else self.trace_link(v)
                    s_, odd_ = self.signs(Fh); Hh = self.H_of(Vh, s_, self.col)
                    pre_hole = dict(L=len(Vh), t=None if Hh is None else round(abs(mc.cz(Hh[-1])), 3), odd=odd_, tags=len(set(self.tag[x] for x in Vh)))
                    self.present[v] = True
                    for y in self.adj[v]: self.unc[y] -= 1
                info, overrun = self.commit(ctx, res2[0], tg)
                for c in comps:
                    self.uf[self.find(c)] = self.find(tg)
                ev = 'merge' if len(comps) >= 2 else ('close' if kind == 'close' else ('split' if len(info) >= 2 else 'grow'))
                rec = dict(k=k, tag=tg, v=v, R=R, ev=ev, ntags=len(ntags), comps=len(comps), W=info, dn=ctx['dn'], dep=len(ctx['dep']),
                           npos=len(self.posn), nodd=self.nodd, ren=p is not None and p != tuple(range(4)), ov=overrun)
                if pre_hole: rec['hole'] = pre_hole
                if ev == 'split':
                    rec['split'] = [self.comp_size(w) for w in ctx['W']]
                self.recs.append(rec); return rec
        return None

    def trace_link(self, v):
        """with v absent and all its neighbours present: the walk around the 1-vertex hole {v}."""
        r = self.rot[v]; a = r[0]; u = r[1]
        # find the dart (x->y) on the link with cw-next(x around y) == v
        for y in r:
            ry = self.rot[y]; i = self.ix[y][v]; x = ry[(i - 1) % len(ry)]
            if self.present[x]: return self.trace(x, y)
        raise RuntimeError('link')
    def comp_size(self, w):
        """size and #odd of the uncoloured component on the gap side of walk w."""
        V = w['V']; L = len(V); start = None
        for j in range(L):
            a, u = V[(j-1) % L], V[j]; ru = self.rot[u]; z = ru[(self.ix[u][a] + 1) % len(ru)]
            if not self.present[z]: start = z; break
        if start is None: return (0, 0)
        seen = {start}; q = [start]
        while q:
            x = q.pop()
            for y in self.adj[x]:
                if not self.present[y] and y not in seen: seen.add(y); q.append(y)
        return (len(seen), sum(1 for x in seen if len(self.adj[x]) % 2))

def job(spec):
    # map:m:seed[:opts]  opts: K=,ren=1,Rmax=
    parts = spec.split(':'); name, m, seed = parts[0], int(parts[1]), int(parts[2])
    opts = dict(kv.split('=') for kv in parts[3].split(',')) if len(parts) > 3 and parts[3] else {}
    t0 = time.time(); adj = mkmap(name); n = len(adj)
    try: I = MF(adj, m, seed, K=int(opts.get('K', '5')), Rmax=int(opts.get('Rmax', '4')), ren=opts.get('ren') == '1', mb=int(opts.get('mb', '0')), tz=opts.get('tz') == '1')
    except RuntimeError as e: return dict(spec=spec, n=n, m=m, status='BADSEED', err=str(e), recs=[], fails=[], nskip=0, maxR=0, mind=None, diam=None, steps=0, colored=0, Rhist={}, sec=0)
    status = 'ok'; err = None; k = sum(I.present); fails = []; TL = int(os.environ.get('TLIM', '3000'))
    try:
        while k < n:
            prog = False; failed_round = []
            for tg in range(m):
                if k >= n: break
                r = I.turn(tg, k)
                if r == 'none': continue
                if r is None:
                    failed_round.append(tg); fails.append(dict(k=k, tag=tg, nodd=I.nodd, cands=[(c[2], c[3]) for c in I.candidates(tg)[:I.K]],
                                                            ntags=[len(set(I.tag[y] for y in adj[c[2]] if I.present[y])) for c in I.candidates(tg)[:I.K]]))
                    continue
                prog = True; k += 1
            if not prog:
                status = 'FAIL' if failed_round else 'STUCK'; break
            if time.time() - t0 > TL: status = 'timeout'; break
    except RuntimeError as e: status = 'UNK'; err = str(e)
    rs = I.recs
    out = dict(spec=spec, n=n, m=m, diam=I.diam, mind=I.mind, status=status, err=err, steps=len(rs), colored=sum(I.present),
               maxR=max([r['R'] for r in rs], default=0), Rhist=dict(collections.Counter(r['R'] for r in rs)),
               nskip=len(fails), fails=fails[:20], sec=round(time.time()-t0))
    if status == 'ok': out['proper'] = check_proper(adj, I.col)
    out['recs'] = [[r['k'], r['tag'], r['R'], r['ev'], r['ntags'], r['comps'], r['W'], r['dn'], r['npos'], r['nodd'], r.get('hole'), r.get('split'), r['ren'], r['ov']] for r in rs]
    # Voronoi / Delaunay-like dual of the cells
    E = set(); T = set()
    for u in range(n):
        for w in adj[u]:
            if I.tag[u] >= 0 and I.tag[w] >= 0 and I.tag[u] != I.tag[w]: E.add(tuple(sorted((I.tag[u], I.tag[w]))))
        r = I.rot[u]
        for i in range(len(r)):
            tr = {I.tag[u], I.tag[r[i]], I.tag[r[(i+1) % len(r)]]}
            if len(tr) == 3 and -1 not in tr: T.add(tuple(sorted(tr)))
    out['dual'] = dict(edges=sorted(E), triangles=sorted(T), cellsize=collections.Counter(I.tag).most_common())
    if os.environ.get('SAVECOL') == '1': out['tag'] = I.tag; out['col'] = I.col
    return out

if __name__ == '__main__':
    from multiprocessing import Pool
    with Pool(int(os.environ.get('NP', '4')), maxtasksperchild=1) as Pp, open(sys.argv[1], 'a') as fo:
        for r in Pp.imap_unordered(job, sys.argv[2:]):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print({k: r[k] for k in ('spec', 'n', 'diam', 'mind', 'status', 'err', 'steps', 'colored', 'maxR', 'Rhist', 'nskip', 'sec')}, flush=True)
