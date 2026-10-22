# Pair induction (canonical ordering) with the STEP-detrended level measure:
#   even #interior-odd : |t| <= 2 and tau_step <= 1, tau_step = min_j circumradius{H_i (i<=j), H_i - t (j<i<L)}
#   odd                : tau_step_odd <= 1, tau_step_odd = min_j circumradius{H_i (i<=j), 2q - H_i (j<i<L)}, q = (H_0+H_L)/2
#   (ODD_MODE = 'fp' instead uses the fixed-point radius max_i |H_i - q| <= 1 of pi.py)
# Even step solver: DFS over the free boundary colours along the walk (rotated so that the longest fixed run comes
# first), pruned by the necessary condition "prefix up to the last admissible cut has radius <= 1 and the suffix
# after it has radius <= 1" (no branching on t or on the cut), exact tau_step check on the closed walk, then the
# same SAT extension of the free interior vertices as pi.py.
import sys, itertools, time
sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import *
import ld

def eval_step(B, s, odd, col):
    H = walk(B, s, np.array([col[b] for b in B]))
    if H is None: return False, None, None
    if odd:
        ok, r, j = ld.tau_step_le(H, 1.0, True); return ok, r, None
    at = abs(H[-1] - H[0])
    if at > 2 + 1e-9: return False, None, at
    ok, r, j = ld.tau_step_le(H, 1.0, odd)
    return ok, r, at

def _hull(p2, cap):
    if len(p2) > cap:
        Z = np.array(p2)
        try: h = ConvexHull(np.stack([Z.real, Z.imag], 1)); return list(Z[h.vertices])
        except Exception: pass
    return p2

def maxrun(B, col):
    """longest cyclic block of consecutive boundary vertices using only two colours (counted in vertices)."""
    L = len(B); c = [col[b] for b in B]
    if L <= 2: return L
    best = 0
    for i in range(L):
        a, b = c[i], c[(i+1) % L]; r = 2
        while r < L and c[(i+r) % L] in (a, b): r += 1
        best = max(best, r)
        if best >= L: break
    return best

class StepInductor(Inductor):
    k0 = None          # cap on two-colour runs (vertices); None = no cap
    cutmode = 'min'    # 'min': invariant = min over cuts; 'att': transition charges the flux at the attachment of v
    cut = None         # current flux edge (b, b_next) on the boundary, carried as state in 'att' mode
    capfails = None    # steps where no colouring within Rmax met the cap
    def step(self, k):
        # identical to Inductor.step but records tau_step and uses solve_even for even boundaries
        v = self.order[k]; P = self.paths[k]; B = self.B
        ip = B.index(P[0]); iq = B.index(P[-1]); assert iq == ip + len(P) - 1, (ip, iq, len(P))
        B2 = B[:ip+1] + [v] + B[iq:]
        self.present[v] = True; self.degp[v] = len(P)
        for w in P: self.degp[w] += 1
        for w in P[1:-1]:
            assert self.degp[w] == len(self.adj[w])
            if len(self.adj[w]) % 2: self.nodd += 1
        s, odd = signs(B2, self.degp); assert odd == (self.nodd % 2 == 1), 'parity'
        pos = {b: i for i, b in enumerate(B2)}
        if self.capfails is None: self.capfails = []
        self.Ratt = None; self.Rmin = None
        # admissible cut edges in 'att' mode: the old flux edge (if still a boundary edge) and the two edges at v
        att = []
        L2 = len(B2)
        if self.cut is not None and self.cut[0] in pos and self.cut[1] in pos and pos[self.cut[1]] == (pos[self.cut[0]] + 1) % L2: att.append(pos[self.cut[0]])
        att += [pos[P[0]], pos[v]]
        self.attcuts = sorted(set(att))
        self.cap_on = self.k0
        for R in range(0, 2*self.Rmax+2):
            if R == self.Rmax + 1:
                if self.k0 is None: break
                # cap not restorable within Rmax: record, fall back to the pair alone (best run among min-R colourings)
                pre = maxrun(B[:ip+1] + B[iq:], self.col)
                self.capfails.append(dict(k=k, n=k+1, L=len(B2), inherited=pre > self.k0, prerun=pre)); self.cap_on = None
            F = ball(self.nb, v, R - (self.Rmax + 1 if R > self.Rmax else 0)); t0 = time.time()
            res = self.solve_step(v, B2, pos, s, odd, F, R)
            if self.verbose: print('   R', R, '|F|', len(F), '|FB|', sum(1 for x in F if x in pos), 'ok' if res else 'no', round(time.time()-t0, 2), self.dbg, flush=True)
            if res is not None:
                newcol, (ok, tau, at), ncand, nsat = res
                nch = sum(1 for x in F if x != v and newcol[x] != self.col[x])
                self.col.update(newcol); self.B = B2
                if R > self.Rmax: R -= self.Rmax + 1; self.capfails[-1]['R'] = R; self.capfails[-1]['run'] = maxrun(B2, self.col)
                H = walk(B2, s, np.array([self.col[b] for b in B2])); tmin, jmin = ld.tau_step_full(H, odd); tatt, jatt = ld.tau_step_cuts(H, odd, self.attcuts)
                self.cut = (B2[jatt], B2[(jatt+1) % len(B2)]) if (jatt is not None and (odd or abs(H[-1]-H[0]) > 1e-9)) else None
                rec = dict(k=k, n=k+1, L=len(B2), R=R, odd=odd, run=maxrun(B2, self.col), tau_min=round(float(tmin), 4), tau_att=round(float(tatt), 4), Rmin=self.Rmin, Ratt=self.Ratt, tau=round(float(tau), 4), t=None if at is None else round(float(at), 3),
                           degv=len(self.adj[v]), plen=len(P), nchanged=nch, ncand=ncand, nsat=nsat)
                self.recs.append(rec); return rec
        self.fail = dict(k=k, v=v, P=P, B=B2, s=s.tolist(), odd=odd, col=dict(self.col), nodd=self.nodd)
        return None

    def solve_step(self, v, B2, pos, s, odd, F, R):
        col = self.col; L = len(B2); FBs = set(x for x in B2 if x in F); FI = [x for x in F if x not in pos]
        nbs = {x: self.nb(x) for x in F}
        # rotate so that the longest cyclic run of fixed vertices starts at index 0
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
        Bv = B2[i0:] + B2[:i0]; sv = np.concatenate([s[i0:], (-1 if odd else 1)*s[:i0]])
        free = [x in FBs for x in Bv]
        allowed = {x: [c for c in range(4) if all(col[y] != c for y in nbs[x] if y not in F)] for x in FBs}
        for x in FBs:
            if x != v and col[x] in allowed[x]: allowed[x].remove(col[x]); allowed[x].insert(0, col[x])
        cands = []; nodes = [0]; ncap = self.node_cap; ccap = self.cand_cap; assign = {}
        fixedge = [not (free[i] or free[(i+1) % L]) for i in range(L)]
        inc = np.zeros(L, dtype=complex)
        for i in range(L):
            if fixedge[i]: inc[i] = sv[i]*EV[col[Bv[i]] ^ col[Bv[(i+1) % L]]]
        Cf = np.concatenate([[0], np.cumsum(inc)])
        runend = [0]*L; j = L
        for i in range(L-1, -1, -1):
            if not fixedge[i]: j = i
            runend[i] = j if fixedge[i] else i
        # prune state: (phase, pts, circ). phase 0: all points so far within radius 1 (pts = hull of H_0..H_i);
        # phase 1: prefix exceeded at some point, pts = points after the last admissible cut; circ = their mec.
        def add_points(state, newpts):
            phase, pts, circ = state
            for p in newpts:
                if abs(p - circ[0]) <= circ[1] + 1e-9: continue
                p2 = _hull(pts + [p], 12); c2 = mecc(np.array(p2))
                if c2[1] <= 1 + 1e-9: pts, circ = p2, c2; continue
                if phase == 1: return None
                phase, pts, circ = 1, [p], (p, 0.0)
            return (phase, pts, circ)
        def dfs(i, H, state):
            nodes[0] += 1
            if nodes[0] > ncap or len(cands) >= ccap: return
            if i == L:
                if odd or abs(H - 0j) <= 2 + 1e-9: cands.append(dict(assign))
                return
            x = Bv[i]; y = Bv[(i+1) % L]
            if fixedge[i]:
                j = runend[i]; ks = np.arange(i+1, j+1); Hk = H + (Cf[ks] - Cf[i])
                st2 = add_points(state, list(Hk[ks < L]))
                if st2 is None: return
                dfs(j, Hk[-1], st2); return
            if i == L-1: ys = [assign[y]] if y in FBs else [col[y]]
            elif y in FBs: ys = [c for c in allowed[y] if all(assign.get(z) != c for z in nbs[y] if z in FBs)]
            else: ys = [col[y]]
            for cy in ys:
                cx = assign[x] if x in FBs else col[x]
                if cy == cx: continue
                H2 = H + sv[i]*EV[cx ^ cy]
                st2 = state
                if i+1 < L:
                    st2 = add_points(state, [H2])
                    if st2 is None: continue
                newly = y in FBs and i+1 < L
                if newly: assign[y] = cy
                dfs(i+1, H2, st2)
                if newly: del assign[y]
        x0 = Bv[0]
        for c in (allowed[x0] if x0 in FBs else [col[x0]]):
            if x0 in FBs: assign[x0] = c
            dfs(0, 0j, (0, [0j], (0j, 0.0)))
            if x0 in FBs: del assign[x0]
        self.dbg = ('cands', len(cands), 'nodes', nodes[0])
        if nodes[0] > ncap: raise RuntimeError('node cap R=%d |FB|=%d' % (R, len(FBs)))
        if not cands: return None
        ev = []
        for a in cands:
            c2 = dict(col); c2.update(a); r = eval_step(B2, s, odd, c2)
            if r[0]:
                if self.Rmin is None: self.Rmin = R
                if self.cutmode == 'att':
                    H = walk(B2, s, np.array([c2[b] for b in B2])); ta, ja = ld.tau_step_cuts(H, odd, self.attcuts)
                    if ta is None or ta > 1 + 1e-9: continue
                    r = (True, ta, r[2])
                if self.Ratt is None: self.Ratt = R
                mr = maxrun(B2, c2)
                if self.cap_on is not None and mr > self.cap_on: continue
                ev.append((a, r, mr))
        self.dbg = self.dbg + ('exact', len(ev))
        if not ev: return None
        if self.policy == 'keep': ev.sort(key=lambda e: (e[2] if self.k0 is not None else 0, sum(1 for x in FBs if x != v and e[0][x] != col[x])))
        elif self.policy == 'rand': self.rng.shuffle(ev)
        else: ev.sort(key=lambda e: self.score(e[1]))
        ev = [(a, r) for a, r, mr in ev]
        if not FI:
            a, r = ev[0]; return a, r, len(ev), 0
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
            for a, r in ev:
                nsat += 1
                if S.solve(assumptions=[X(x, a[x]) for x in FBs]):
                    m = set(l for l in S.get_model() if l > 0)
                    out = {x: next(c for c in range(4) if X(x, c) in m) for x in F}
                    return out, r, len(ev), nsat
            if len(cands) >= ccap: raise RuntimeError('cand cap with no extension')
            return None
        finally: S.delete()
