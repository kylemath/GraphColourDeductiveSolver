# Canonical-order induction with the bounded-cut invariant:  even: |t| <= 2 and tau_J <= 1;  odd: tau_J,odd <= 1.
# cutmode 'min': cuts anywhere (min over positions).  'att': cuts only on the edges carried from the previous step
# (still boundary edges) plus the two boundary edges at the new vertex v (new flux charged at the attachment).
# Optional run cap k0 (as localdetrend/pi_step.py).  Exact: DFS over free boundary colours with the exact DP frontier
# of mc.py as the prune, then the SAT extension of free interior vertices (pi.py).
import sys, itertools, time
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/'); sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import *
from pi_step import maxrun
import mc

class MCInductor(Inductor):
    J = 2; variant = 'nc'; tfree = False; k0 = None; cutmode = 'min'; carried = None; capfails = None; repair_d = None
    def H_of(self, B2, s, col):
        L = len(B2); lab = [col[B2[i]] ^ col[B2[(i+1) % L]] for i in range(L)]
        if 0 in lab: return None
        return mc.int_walk(lab, [int(x) for x in s])
    def allowed_edges(self, B2, pos, P, v):
        if self.cutmode == 'min': return None
        L = len(B2); al = [False]*L
        for (a, b) in (self.carried or []):
            if a in pos and b in pos and pos[b] == (pos[a] + 1) % L: al[pos[a]] = True
        al[pos[P[0]]] = True; al[pos[v]] = True
        return al
    def step(self, k):
        v = self.order[k]; P = self.paths[k]; B = self.B
        ip = B.index(P[0]); iq = B.index(P[-1]); assert iq == ip + len(P) - 1
        B2 = B[:ip+1] + [v] + B[iq:]
        self.present[v] = True; self.degp[v] = len(P)
        for w in P: self.degp[w] += 1
        for w in P[1:-1]:
            if len(self.adj[w]) % 2: self.nodd += 1
        s, odd = signs(B2, self.degp); assert odd == (self.nodd % 2 == 1)
        pos = {b: i for i, b in enumerate(B2)}
        if self.capfails is None: self.capfails = []
        self.al = self.allowed_edges(B2, pos, P, v); self.cap_on = self.k0
        for R in range(0, 2*self.Rmax+2):
            if R == self.Rmax + 1:
                if self.k0 is None: break
                self.capfails.append(dict(k=k, n=k+1, L=len(B2))); self.cap_on = None
            Rr = R - (self.Rmax + 1 if R > self.Rmax else 0)
            F = ball(self.nb, v, Rr)
            res = self.solve_step(v, B2, pos, s, odd, F, Rr)
            if res is not None:
                newcol, nc, ncand, nsat = res
                self.col.update(newcol); self.B = B2
                H = self.H_of(B2, s, self.col); t = mc.cz(H[-1])
                cuts = mc.cut_positions(H, odd, self.J, self.variant, 1.0, self.al)
                self.carried = [(B2[j], B2[(j+1) % len(B2)]) for j in cuts]
                rec = dict(n=k+1, L=len(B2), R=Rr, odd=odd, t=round(abs(t), 3), ncuts=len(cuts), nodd=self.nodd, run=maxrun(B2, self.col), capoff=R > self.Rmax)
                self.recs.append(rec); return rec
        self.fail = dict(k=k, v=v, P=P, B=B2, s=s.tolist(), odd=odd, col=dict(self.col), nodd=self.nodd, al=self.al)
        return None

    def solve_step(self, v, B2, pos, s, odd, F, R):
        col = self.col; L = len(B2); FBs = set(x for x in B2 if x in F); FI = [x for x in F if x not in pos]
        nbs = {x: self.nb(x) for x in F}
        fixed = [b not in FBs for b in B2]
        st = next(j for j in range(L) if not fixed[j]); best = (0, 0); cur = None
        for kk in range(1, L+1):
            idx = (st + kk) % L
            if fixed[idx]:
                if cur is None: cur = [idx, 1]
                else: cur[1] += 1
                if cur[1] > best[1]: best = tuple(cur)
            else: cur = None
        i0 = best[0] if best[1] > 0 else pos[v]
        Bv = B2[i0:] + B2[:i0]; sv = [int(x) for x in np.concatenate([s[i0:], (-1 if odd else 1)*s[:i0]])]
        alv = None if self.al is None else [self.al[(i + i0) % L] for i in range(L)]
        free = [x in FBs for x in Bv]
        allowed = {x: [c for c in range(4) if all(col[y] != c for y in nbs[x] if y not in F)] for x in FBs}
        for x in FBs:
            if x != v and col[x] in allowed[x]: allowed[x].remove(col[x]); allowed[x].insert(0, col[x])
        Fr = mc.Frontier(self.J, odd, self.variant, 1.0)
        fixedge = [not (free[i] or free[(i+1) % L]) for i in range(L)]
        runend = [0]*L; j = L
        for i in range(L-1, -1, -1):
            if not fixedge[i]: j = i
            runend[i] = j if fixedge[i] else i
        cands = []; nodes = [0]; assign = {}; ncap = self.node_cap; ccap = self.cand_cap
        def ae(i): return True if alv is None else alv[i]
        def stepH(H, i, cx, cy):
            d = mc.STEP[cx ^ cy]; g = sv[i]; return (H[0] + g*d[0], H[1] + g*d[1])
        def dfs(i, H, Fs):
            nodes[0] += 1
            if nodes[0] > ncap or len(cands) >= ccap: return
            if i == L:
                if not odd and not self.tfree and abs(mc.cz(H)) > 2 + 1e-9: return
                c = Fr.close(Fs, H, ae(L-1))
                if c is not None: cands.append((dict(assign), c))
                return
            x = Bv[i]; y = Bv[(i+1) % L]
            if fixedge[i]:
                jj = runend[i]; Hk = H
                for kk in range(i, jj):
                    Hk = stepH(Hk, kk, col[Bv[kk]], col[Bv[(kk+1) % L]])
                    if kk + 1 < L:
                        Fs = Fr.adv(Fs, Hk, ae(kk))
                        if not Fs: return
                dfs(jj, Hk, Fs); return
            if i == L-1: ys = [assign[y]] if y in FBs else [col[y]]
            elif y in FBs: ys = [c for c in allowed[y] if all(assign.get(z) != c for z in nbs[y] if z in FBs)]
            else: ys = [col[y]]
            cx = assign[x] if x in FBs else col[x]
            for cy in ys:
                if cy == cx: continue
                H2 = stepH(H, i, cx, cy); F2 = Fs
                if i+1 < L:
                    F2 = Fr.adv(Fs, H2, ae(i))
                    if not F2: continue
                newly = y in FBs and i+1 < L
                if newly: assign[y] = cy
                dfs(i+1, H2, F2)
                if newly: del assign[y]
        x0 = Bv[0]
        for c in (allowed[x0] if x0 in FBs else [col[x0]]):
            if x0 in FBs: assign[x0] = c
            dfs(0, (0, 0), Fr.start())
            if x0 in FBs: del assign[x0]
        if nodes[0] > ncap: raise RuntimeError('node cap R=%d |FB|=%d' % (R, len(FBs)))
        if not cands: return None
        ev = []
        for a, nc in cands:
            c2 = dict(col); c2.update(a); mr = maxrun(B2, c2)
            if self.cap_on is not None and mr > self.cap_on: continue
            ev.append((a, nc, mr))
        if not ev: return None
        ev.sort(key=lambda e: (e[1], sum(1 for x in FBs if x != v and e[0][x] != col[x])))
        if not FI:
            a, nc, _ = ev[0]; return a, nc, len(ev), 0
        ix = {x: i for i, x in enumerate(F)}; X = lambda x, c: 4*ix[x]+c+1; cls = []
        for x in F:
            cls.append([X(x, c) for c in range(4)])
            for a_, b_ in itertools.combinations(range(4), 2): cls.append([-X(x, a_), -X(x, b_)])
            for y in nbs[x]:
                if y in F:
                    if ix[y] > ix[x]:
                        for c in range(4): cls.append([-X(x, c), -X(y, c)])
                else: cls.append([-X(x, col[y])])
        S = Cadical153(bootstrap_with=cls); nsat = 0
        try:
            for a, nc, _ in ev:
                nsat += 1
                if S.solve(assumptions=[X(x, a[x]) for x in FBs]):
                    m = set(l for l in S.get_model() if l > 0)
                    out = {x: next(c for c in range(4) if X(x, c) in m) for x in F}
                    return out, nc, len(ev), nsat
            if len(cands) >= ccap: raise RuntimeError('cand cap with no extension')
            return None
        finally: S.delete()

class RepairInductor(MCInductor):
    """after every step: while two consecutive cuts lie within boundary distance d, try to recolour the union of the
    radius-rr balls around the boundary vertices between them so that the walk needs one cut fewer (invariant kept)."""
    rep_d = 8; rep_r = 2; nrep = 0; nrep_try = 0
    def step(self, k):
        rec = MCInductor.step(self, k)
        if rec is None: return None
        for it in range(3):
            if not self.try_repair(): break
        if self.recs: self.recs[-1]['ncuts_after'] = len(self.carried)
        return rec
    def try_repair(self):
        B2 = self.B; L = len(B2); pos = {b: i for i, b in enumerate(B2)}
        cuts = sorted(pos[a] for a, b in self.carried)
        if len(cuts) < 2: return False
        s, odd = signs(B2, self.degp)
        prs = []
        for i in range(len(cuts)):
            a, b = cuts[i], cuts[(i+1) % len(cuts)]
            dist = (b - a) % L
            if 0 < dist <= self.rep_d: prs.append((dist, a, b))
        for dist, a, b in sorted(prs):
            seg = [B2[(a + j) % L] for j in range(dist + 2)]
            F = {}
            for x in seg: F.update(ball(self.nb, x, self.rep_r))
            Jsave = self.J; self.J = len(cuts) - 1; alsave = self.al; self.al = None; cap = self.cap_on; self.cap_on = self.k0
            self.nrep_try += 1
            try: res = self.solve_step(seg[0], B2, pos, s, odd, F, -1)
            except RuntimeError: res = None
            finally: self.J = Jsave; self.al = alsave; self.cap_on = cap
            if res is None: continue
            newcol, nc, _, _ = res
            self.col.update(newcol); H = self.H_of(B2, s, self.col)
            c2 = mc.cut_positions(H, odd, self.J, self.variant, 1.0, None)
            self.carried = [(B2[j], B2[(j+1) % L]) for j in c2]; self.nrep += 1
            return True
        return False
