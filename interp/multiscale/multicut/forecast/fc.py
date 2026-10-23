# Remaining-holonomy forecast ("steering potential") for the vortex-restricted canonical induction.
# Model unchanged: ../unbounded/vr.py via ../scale/vrs.py (imported, not edited).  Output only in forecast/.
#
# Holonomy machinery (exact, combinatorial):
#   heights live on vertices (Kondev-Henley, Lambda = Z[w]); a face with ccw order (a,b,c) and sign sigma gives
#   h_b - h_a = sigma * e(col a ^ col b) for each ccw pair; adjacent faces have opposite sigma.
#   For a vertex set Q (a disc: Q and its complement Z connected, v1, v2 in Q, vn in Z) the faces straddling the cut
#   form one dual cycle through the outer face f0 = (v1, v2, vn).  Developing the Q-side heights along it from the
#   frame (h(v1) = 0, sigma(f0) = +1) gives the affine holonomy g = (eps, a): h -> eps*h + a  (eps = -1 iff Q
#   encloses an odd number of odd vertices; then g is the point reflection about a/2).  Only colours of Q are used.
#   For Q = the current prefix this is the walk holonomy of vr.py (t = a when even), checked at every step (chk=1).
# Forecast at a step (prefix region C, run colouring -> A = hol(C)):
#   ORACLE: a fixed proper colouring col* of the whole map (SAT or a completed run; colour-normalised so that
#   col*(v1, v2, v3) = (0, 1, 2) as in the run).  Q_r = C + every outside vertex within graph distance r of C (the
#   distance is measured in the outside graph, vn excluded), holes filled.  The near-outside holonomy in the frame
#   fixed by the cut is hol*(near) = hol*(C)^-1 o hol*(Q_r) (so it composes exactly the reflections of the outside
#   odd vertices within r, with col*'s developed centres, in frontier order).  Predicted total  T_r = A o hol*(near).
#   P_r = |translation of T_r| if T_r is a translation, 0 if it is a reflection (an odd number of vortices beyond r
#   remain to absorb it).  r = 0: P_0 = |t| (or 0 when odd).  r = all: P = |t - t*(C)| (even case).
#   LOCAL: centres unknown; vortex w at distance d_w from the boundary, nearest boundary vertex b_w, has its centre in
#   the Lipschitz disc |c_w - h(b_w)| <= d_w.  P_r^loc = min over centres (and both frontier orientations) of
#   |translation of A o rho_{c_1} o ... o rho_{c_m}| = max(0, |base| - 2 sum d_w) (continuous relaxation), 0 if the
#   composite is a reflection.  No near vortex: P = |t| (even) / 0 (odd).
# Steering (opt st=tie|soft, pot=orc|loc, r=<int>|all):  tie = among the admissible min-R candidates take min P_r
# (then fewest cuts, fewest recolourings);  soft = also solve at Rmin+1 and keep the lower P_r (ties: lower R).
# spec: map:oseed:pol:var[:k=v,...]   opts as vrs.py plus st, pot, r, orc=sat<k>|run, log=1, chk=1
import sys, os, json, time, random, collections, math
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/scale/'); sys.path.insert(0, '/mnt/project-files/multiscale/multicut/backtrack/')
import vrs, mc
from vrs import canon2, pick_face, VRInductor, FrontierVR, BIG
from pi import rotation, check_proper, signs, ball
FC = '/mnt/project-files/multiscale/multicut/forecast/'
STEP = mc.STEP

def vadd(p, q): return (p[0] + q[0], p[1] + q[1])
def vmul(e, p): return (e*p[0], e*p[1])
def comp(g1, g2): return (g1[0]*g2[0], vadd(g1[1], vmul(g1[0], g2[1])))
def inv(g): return (g[0], vmul(-g[0], g[1]))
def nrm(p): return abs(mc.cz(p))
def tr_norm(g): return nrm(g[1]) if g[0] == 1 else 0.0

class Geo:
    def __init__(self, adj, rot):
        self.adj = adj; self.n = len(adj); self.nx = {}
        for w in range(self.n):
            r = rot[w]; d = len(r)
            for i, u in enumerate(r): self.nx[(u, w)] = r[(i+1) % d]
        for (u, w), x in list(self.nx.items())[:2000]:
            assert self.nx[(w, x)] == u and self.nx[(x, u)] == w
    def dev(self, inQ, col, v1, v2, vn, want_h=False):
        nx = self.nx
        if nx[(v1, v2)] == vn: f = (v1, v2, vn)
        else: assert nx[(v2, v1)] == vn; f = (v2, v1, vn)
        f0 = frozenset(f)
        def fill(face, h, sg):
            for _ in range(2):
                for p, q in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])):
                    if inQ[p] and inQ[q]:
                        st = STEP[col[p] ^ col[q]]
                        if p in h and q not in h: h[q] = vadd(h[p], vmul(sg, st))
                        elif q in h and p not in h: h[p] = vadd(h[q], vmul(-sg, st))
        h = {v1: (0, 0)}; sg = 1; fill(f, h, sg); h0 = dict(h); first = dict(h); seq = []
        face = f; it = 0
        while True:
            it += 1; assert it < 8*self.n
            ex = next((p, q) for p, q in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])) if inQ[p] and not inQ[q])
            p, q = ex; face = (q, p, nx[(q, p)]); sg = -sg; h = {p: h[p]}; fill(face, h, sg)
            if want_h:
                for x, y in h.items():
                    if x not in first: first[x] = y
                seq.append(p)
            if frozenset(face) == f0: break
        e = sg; a = vadd(h[v1], vmul(-e, h0[v1]))
        assert h[v2] == vadd(vmul(e, h0[v2]), a), 'holonomy inconsistent'
        return ((e, a), first, seq) if want_h else (e, a)

def sat_colouring(adj, seed):
    from pysat.solvers import Cadical153
    n = len(adj); rng = random.Random(seed); X = lambda x, c: 4*x + c + 1; cls = []
    for x in range(n):
        cls.append([X(x, c) for c in range(4)])
        for a in range(4):
            for b in range(a+1, 4): cls.append([-X(x, a), -X(x, b)])
        for y in adj[x]:
            if y > x:
                for c in range(4): cls.append([-X(x, c), -X(y, c)])
    S = Cadical153(bootstrap_with=cls)
    # random partial seeding (assumptions) for diversity; drop them if unsat
    asm = [X(x, rng.randrange(4)) for x in rng.sample(range(n), min(n, 40))]
    ok = S.solve(assumptions=asm) or S.solve()
    assert ok
    m = set(l for l in S.get_model() if l > 0); S.delete()
    return [next(c for c in range(4) if X(x, c) in m) for x in range(n)]

def normalise(colstar, v1, v2, v3):
    a, b, c = colstar[v1], colstar[v2], colstar[v3]; d = ({0, 1, 2, 3} - {a, b, c}).pop()
    pm = {a: 0, b: 1, c: 2, d: 3}; return [pm[x] for x in colstar]

RS = [0, 1, 2, 4, 8, 16, 'all']

class Ov:
    def __init__(s, base, top): s.b = base; s.t = top
    def __getitem__(s, x): return s.t[x] if x in s.t else s.b[x]

class FCI(VRInductor):
    PCAP = 400; st = None; pot = 'orc'; rr = 'all'; logon = False; chk = False
    def fc_setup(self, geo, colstar, oddtot):
        self.geo = geo; self.colstar = colstar; self.oddtot = oddtot
        self.v1, self.v2 = self.order[0], self.order[1]
        self.vn = self.order[-1]; self.flog = []; self.nchk = 0; self.nchkfail = 0; self.stepR = []
        self._stepcache = None
    # ---- per-step forecast data (depends on the prefix, not on the candidate) ----
    def outside_bfs(self):
        pres = self.present; n = len(pres); vn = self.vn; dist = {}; src = {}; dq = collections.deque()
        for b in self.Bcur:
            for y in self.adj[b]:
                if not pres[y] and y != vn and y not in dist: dist[y] = 1; src[y] = b; dq.append(y)
        while dq:
            x = dq.popleft()
            for y in self.adj[x]:
                if not pres[y] and y != vn and y not in dist: dist[y] = dist[x] + 1; src[y] = src[x]; dq.append(y)
        return dist, src
    def Qr(self, dist, r):
        """Q_r = prefix + outside vertices within distance r, holes filled; the far region (distance > r) is joined
        to vn by thin corridors (shortest absent paths, avoiding odd vertices) so that the frame face f0 = (v1, v2, vn)
        lies on the cut; Q-pieces cut off from the prefix by a corridor are moved to the far side."""
        pres = self.present; n = len(pres); adj = self.adj; vn = self.vn
        if r == 'all': far = set()
        else: far = set(y for y, d in dist.items() if d > r)
        Z = {vn}; rem = set(far)
        import heapq
        while True:
            # grow Z by the far components already touching it
            dq = collections.deque(Z); 
            while dq:
                x = dq.popleft()
                for y in adj[x]:
                    if y in rem: rem.discard(y); Z.add(y); dq.append(y)
            if not rem: break
            # corridor: cheapest absent path from Z to rem (odd vertices cost 50, others 1)
            dd = {x: 0 for x in Z}; par = {}; hq = [(0, x) for x in Z]; hit = None
            while hq:
                c, x = heapq.heappop(hq)
                if c > dd.get(x, 1e18): continue
                if x in rem: hit = x; break
                for y in adj[x]:
                    if pres[y] or y in Z: continue
                    c2 = c + (50 if len(adj[y]) % 2 else 1)
                    if c2 < dd.get(y, 1e18): dd[y] = c2; par[y] = x; heapq.heappush(hq, (c2, y))
            if hit is None: break
            x = par.get(hit)
            while x is not None and x not in Z: Z.add(x); x = par.get(x)
        inQ = [x not in Z for x in range(n)]
        # keep only the component of Q containing v1 (prefix is connected); the rest goes to the far side
        seen = {self.v1}; dq = collections.deque([self.v1])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if inQ[y] and y not in seen: seen.add(y); dq.append(y)
        return [x in seen for x in range(n)]
    def step_data(self, B2, rs):
        key = (tuple(B2), len(self.recs))
        if self._stepcache and self._stepcache[0] == key and all(r in self._stepcache[1] for r in rs): return self._stepcache[1], self._stepcache[2]
        self.Bcur = B2; dist, src = self.outside_bfs(); M = {}
        cs = self.colstar; g = self.geo
        Bst = g.dev(self.present, cs, self.v1, self.v2, self.vn)
        for r in rs:
            if r == 0: M[r] = (1, (0, 0)); continue
            Q = self.Qr(dist, r); M[r] = comp(inv(Bst), g.dev(Q, cs, self.v1, self.v2, self.vn))
        odd_out = [(w, d, src[w]) for w, d in dist.items() if len(self.adj[w]) % 2]
        extra = dict(dist=dist, src=src, odd_out=odd_out, Bst=Bst)
        self._stepcache = (key, M, extra); return M, extra
    # ---- candidate holonomy: direct development of the outside loop of the prefix (boundary odd vertices count
    #      as enclosed here; vr.py counts them as outside -> parity/t differ only while an odd vertex is ON the boundary)
    def A_dev(self, colov):
        (e, a), first, seq = self.geo.dev(self.present, colov, self.v1, self.v2, self.vn, want_h=True)
        return (e, a), first
    def P_orc(self, A, M): return tr_norm(comp(A, M))
    def P_loc(self, A, hts, B2, extra, r):
        pos = {b: i for i, b in enumerate(B2)}
        near = [(pos[b], d) for (w, d, b) in extra['odd_out'] if (r == 'all' or d <= r)]
        if not near: return tr_norm(A)
        e = A[0] * (-1)**len(near)
        if e == -1: return 0.0
        near.sort(); best = None; S = 2*sum(d for _, d in near)
        for seqn in (near, near[::-1]):
            g = A
            for i, d in seqn: g = comp(g, (-1, vmul(2, hts[B2[i]])))     # rho_c: h -> -h + 2c
            v = max(0.0, nrm(g[1]) - S)
            best = v if best is None else min(best, v)
        return best
    # ---- hook into the vrs candidate ordering (called before the SAT extension) ----
    def _lyap_hook(self, ev, B2, s, odd, FBs):
        self._ly = None
        if not self.st or not ev or self.present[self.vn]: return ev
        r = self.rr; col = self.col; v = self.order[len(self.recs) + 3]
        M, extra = self.step_data(B2, [r] if self.pot == 'orc' else [0])
        Ps = []
        for i, (a, nc, mr) in enumerate(ev):
            if i >= self.PCAP: Ps.append(1e9); continue
            Ps.append(self.P_of_col(a, B2, M, extra))
        idx = sorted(range(len(ev)), key=lambda i: (round(Ps[i], 6), ev[i][1], sum(1 for x in FBs if x != v and ev[i][0][x] != col[x])))
        return [ev[i] for i in idx]
    def P_of_col(self, newcol, B2, M=None, extra=None):
        if M is None: M, extra = self.step_data(B2, [self.rr] if self.pot == 'orc' else [0])
        A, hts = self.A_dev(Ov(self.col, newcol))
        return self.P_orc(A, M[self.rr]) if self.pot == 'orc' else self.P_loc(A, hts, B2, extra, self.rr)
    def solve_step(self, v, B2, pos, s, odd, F, R):
        res = VRInductor.solve_step(self, v, B2, pos, s, odd, F, R)
        if res is None or self.st != 'soft' or R + 1 > self.Rmax or R < 0 or self.present[self.vn]:
            if res is not None: self._Ruse = R
            return res
        P1 = self.P_of_col(res[0], B2)
        if P1 > 1e-9:
            try: res2 = VRInductor.solve_step(self, v, B2, pos, s, odd, ball(self.nb, v, R + 1), R + 1)
            except RuntimeError: res2 = None
            if res2 is not None and self.P_of_col(res2[0], B2) < P1 - 1e-9:
                self._Ruse = R + 1; return res2
        self._Ruse = R; return res
    # ---- passive log after each committed step ----
    def log_step(self):
        B2 = self.B; s, odd = signs(B2, self.degp); H = self.H_of(B2, s, self.col)
        A, hts = self.A_dev(self.col)
        nob = sum(1 for b in B2 if len(self.adj[b]) % 2)
        if self.chk:
            self.nchk += 1
            bad = (A[0] == -1) != (odd != (nob % 2 == 1))
            if nob == 0 and not odd: bad = bad or round(abs(mc.cz(H[-1])), 3) != round(nrm(A[1]), 3)
            self.nchkfail += bad
        M, extra = self.step_data(B2, RS)
        rec = dict(n=len(self.recs) + 3, eps=A[0], a=A[1], nodd=self.nodd, nob=nob, todd=odd, t=round(abs(mc.cz(H[-1])), 3),
                   Po={str(r): round(self.P_orc(A, M[r]), 3) for r in RS},
                   Pl={str(r): round(self.P_loc(A, hts, B2, extra, r), 3) for r in RS},
                   fr={str(r): M[r] for r in RS},
                   nout=len(extra['odd_out']), dmin=min([d for _, d, _ in extra['odd_out']], default=None))
        self.flog.append(rec)

ORC = {}
def get_orc(name, adj, how):
    fn = FC + 'orc_%s_%s.json' % (name, how)
    if os.path.exists(fn): return json.load(open(fn))
    if how.startswith('sat'): c = sat_colouring(adj, int(how[3:] or 0))
    else: raise ValueError(how)
    json.dump(c, open(fn, 'w')); return c

TLIM = int(os.environ.get('TLIM', '3000'))
def job(spec):
    parts = spec.split(':'); name, oseed, pol, var = parts[:4]; oseed = int(oseed)
    opts = dict(kv.split('=') for kv in parts[4].split(',')) if len(parts) > 4 and parts[4] else {}
    face = opts.get('face', 'rand'); Rmax = int(opts.get('Rmax', '4'))
    vrs.TZ[0] = False; mc.U[:] = vrs.U6; mc.UI.clear(); mc.UI.update({u: d for d, u in enumerate(mc.U)})
    t0 = time.time(); adj = vrs.mkmap(name); rot, emb = rotation(adj); rng = random.Random(oseed); n = len(adj)
    f = pick_face(adj, rot, emb, rng, face)
    order, paths = canon2(adj, rot, f, pol, rng)
    oddtot = sum(1 for x in range(n) if len(adj[x]) % 2)
    geo = Geo(adj, rot)
    cs = opts.get('orc', 'sat0')
    if cs == 'file': colstar = json.load(open(FC + 'cols/' + opts['orcfile']))
    elif cs == 'self':      # a completed colouring of the SAME map and ordering (from another variant), if any
        import glob
        fs = sorted(glob.glob(FC + 'cols/col_%s_%d_%s_%s*.json' % (name, oseed, pol, var)))
        fs = [x for x in fs if '_st' not in x] or fs
        if not fs: return dict(spec=spec, status='noorc', name=name, n=n)
        colstar = json.load(open(fs[0]))
    else: colstar = get_orc(name, adj, cs)
    assert all(colstar[x] != colstar[y] for x in range(n) for y in adj[x])
    colstar = normalise(colstar, order[0], order[1], order[2])
    I = FCI(adj, order, paths, Rmax=Rmax, policy='keep', seed=oseed)
    I.node_cap = int(os.environ.get('NCAP', '400000')); I.cand_cap = int(os.environ.get('CCAP', '20000')); I.variant = var; I.slide = 0; I.init_vr()
    I.greedy = False
    I.st = opts.get('st'); I.pot = opts.get('pot', 'orc'); r = opts.get('r', 'all'); I.rr = r if r == 'all' else int(r)
    I.logon = opts.get('log') == '1'; I.chk = opts.get('chk') == '1'
    I.fc_setup(geo, colstar, oddtot)
    status = 'ok'; err = None; tstar_full = None; Ruse = []
    try:
        for k in range(3, n):
            if opts.get('tz') == '1':
                nxt = I.nodd + sum(1 for w in paths[k][1:-1] if len(adj[w]) % 2); vrs.TZ[0] = (nxt == oddtot)
            I._Ruse = None
            if I.step(k) is None: status = 'FAIL'; break
            Ruse.append(I._Ruse if I._Ruse is not None else I.recs[-1]['R'])
            if I.logon and k < n - 1: I.log_step()
            if time.time() - t0 > TLIM: status = 'timeout'; break
    except RuntimeError as e: status = 'UNK'; err = str(e)
    rs = I.recs; full = [x for x in rs if x['nodd'] == oddtot]
    out = dict(spec=spec, name=name, n=n, oddtot=oddtot, status=status, err=err, steps=len(rs), failn=len(rs) + 4 if status == 'FAIL' else None,
               faillast=(status == 'FAIL' and len(rs) + 3 == n - 1), maxR=max(Ruse, default=0),
               peakcuts=max([x['ncuts'] for x in rs], default=0), peakt=max([x['t'] for x in rs], default=0),
               full_n=full[0]['n'] if full else None, t_at_full=full[0]['t'] if full else None,
               nchk=I.nchk, nchkfail=I.nchkfail, sec=round(time.time() - t0),
               fail_dn=(I.dn if status == 'FAIL' else None), fail_nodd=(I.nodd if status == 'FAIL' else None))
    if I.logon:
        out['flog'] = [dict(n=x['n'], eps=x['eps'], a=x['a'], nodd=x['nodd'], nob=x['nob'], todd=x['todd'], t=x['t'], Po=x['Po'], Pl=x['Pl'], nout=x['nout'], dmin=x['dmin'],
                            fr={k_: [v_[0], v_[1]] for k_, v_ in x['fr'].items()}) for x in I.flog]
        out['walkt'] = [(x['n'], x['nodd'], x['t'], x['dn']) for x in rs]
    if status == 'ok':
        out['proper'] = check_proper(adj, I.col)
        if opts.get('dump') == '1': json.dump([I.col[x] for x in range(n)], open(FC + 'cols/col_%s.json' % spec.replace(':', '_').replace(',', '_').replace('=', ''), 'w'))
    return out

if __name__ == '__main__':
    from multiprocessing import Pool
    specs = sys.argv[2:]
    if len(specs) == 1 and os.path.exists(specs[0]): specs = open(specs[0]).read().split()
    with Pool(int(os.environ.get('NP', '4')), maxtasksperchild=1) as Pp, open(sys.argv[1], 'a') as fo:
        for r in Pp.imap_unordered(job, specs):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print(r['spec'], r['status'], r['steps'], 'failn', r['failn'], 'last', r['faillast'], 'pc', r['peakcuts'], 'pt', r['peakt'],
                  'tfull', r['t_at_full'], 'R', r['maxR'], 'chk', r['nchk'], r['nchkfail'], r['err'], r['sec'], 's', flush=True)
