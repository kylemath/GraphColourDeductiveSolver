#!/usr/bin/env python3
"""[exploratory] NightBudget pass 2 (same sources/engine as nightbudget.py), (5,5,5,5,6) holes only, both orientations.
Per sigma-group and (sigma u sigma')-group:
  (a) the weighted budget B'_c: sum_{r in R-_rho} c(r) <= 2 N0f_rho + E2 + 3 tau, c(r) = #DD steps charged to r by rho (1 or 2);
  (b) one-hop payer flow: every r in R- (literal R) needs 2 units from suppliers (N0f state: 2, E2 start: 1, tau state: 3; shared capacities)
      lying in an excursion that contains a one-hop image of r: V1 = sigma(r) (if not fixed) and, on union groups, the sigma'-images of r;
      V2 = V1 plus r's own excursion (r's unfilled run and the filled run after it);
      V3 = cycle-level: any supplier on the pi-cycle of a one-hop image of r or on r's own pi-cycle.
U34 details for literal-R states with a failing image: whether r has the full R3 ring (R3At: w0..w4 = B,A,B,mu,A), k, kind, (f_prev, u, f).
Usage: nightbudget2.py [ncores]."""
import sys, os, json, time
from collections import Counter, defaultdict, deque
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nightbudget as NB
from uv_lib import Hole

def maxflow(cap, s, t):
    flow = 0; adj = defaultdict(set)
    for (u, v) in list(cap): adj[u].add(v); adj[v].add(u); cap.setdefault((v, u), 0)
    while True:
        par = {s: None}; q = deque([s])
        while q and t not in par:
            u = q.popleft()
            for v in adj[u]:
                if v not in par and cap[(u, v)] > 0: par[v] = u; q.append(v)
        if t not in par: return flow
        b = float('inf'); v = t
        while par[v] is not None: b = min(b, cap[(par[v], v)]); v = par[v]
        v = t
        while par[v] is not None: cap[(par[v], v)] -= b; cap[(v, par[v])] += b; v = par[v]
        flow += b

def analyse2(H):
    S = H.S; pi = H.pi; pinv = H.pinv
    filled = [H.filled(k) for k in range(S)]
    DL = list(H.DL)
    N0 = [not filled[k] and filled[pi[k]] and filled[pinv[k]] for k in range(S)]
    DD = [DL[k] and DL[pi[k]] for k in range(S)]
    DDE = [DD[k] or DD[pinv[k]] for k in range(S)]
    E2 = [filled[pinv[k]] and not filled[k] and not filled[pi[k]] and filled[pi[pi[k]]] for k in range(S)]
    TAU = [filled[k] and filled[pi[k]] for k in range(S)]
    fr = {k: H.frame(k) for k in range(S) if DL[k]}
    R3 = [DL[k] and fr[k][1] == 3 for k in range(S)]
    sig = {}
    def sg(k):
        if k not in sig: sig[k] = H.sigma(k)
        return sig[k]
    Rlit = [R3[k] and DDE[k] for k in range(S)]
    c = Counter()
    for d in range(S):
        if DD[d]: c[d if R3[d] else (pi[d] if R3[pi[d]] else d)] += 1
    deg = [len(H.rot[x]) for x in H.L]
    def fullring(k):
        j, ty, hi, (al, mu, A, B) = fr[k]
        w = [H.col(k, H.w[(j + t) % 5]) for t in range(5)]
        return w == [B, A, B, mu, A]
    # excursion id of a state: (start of its unfilled run) for unfilled states and for filled states (the run before them)
    exc = {}
    def exc_of(k):
        if k in exc: return exc[k]
        a = k; n = 0
        while filled[a] and n < S: a = pinv[a]; n += 1
        if n >= S: exc[k] = ('allfilled', H.cyc[k]); return exc[k]
        n = 0
        while not filled[pinv[a]] and n < S: a = pinv[a]; n += 1
        exc[k] = ('gamma', H.cyc[k]) if n >= S else a
        return exc[k]
    members = {}
    def exc_members(e):
        if e in members: return members[e]
        if isinstance(e, tuple): members[e] = []; return []
        out = []; y = e
        while not filled[y]: out.append(y); y = pi[y]
        while filled[y]: out.append(y); y = pi[y]
        members[e] = out; return out
    linkmask = 0
    for i in H.sp.linki: linkmask |= 1 << i
    nc = len(H.cycles); cyc = H.cyc
    up1 = list(range(nc)); up2 = list(range(nc))
    def f(up, x):
        while up[x] != x: up[x] = up[up[x]]; x = up[x]
        return x
    sigp = defaultdict(list)
    for k in range(S):
        if not DDE[k]: continue
        a, b = f(up1, cyc[k]), f(up1, cyc[sg(k)]); up1[a] = b
        a, b = f(up2, cyc[k]), f(up2, cyc[sg(k)]); up2[a] = b
        for t, p, q, K in H.sp.moves(k):
            if t == k or K & linkmask or DL[t]: continue
            sigp[k].append(t); a, b = f(up2, cyc[k]), f(up2, cyc[t]); up2[a] = b
    res = {}
    for gk, up in (('sigma', up1), ('union', up2)):
        G = defaultdict(list)
        for cc in range(nc): G[f(up, cc)].append(cc)
        recs = []
        for root, cs in G.items():
            st = [k for cc in cs for k in H.cycles[cc]]
            if not any(DD[k] for k in st): continue
            nE2 = sum(E2[k] for k in st); nT = sum(TAU[k] for k in st)
            lam = sum(H.lam[k] for k in st)
            Rr = [k for k in st if c[k]]; img = {sg(r) for r in Rr}
            N0f_r = sum(1 for k in st if N0[k] and k not in img)
            Rm_r = [r for r in Rr if not N0[sg(r)]]
            slack_c = 2 * N0f_r + nE2 + 3 * nT - sum(c[r] for r in Rm_r)
            Rl = [k for k in st if Rlit[k]]; imgl = {sg(r) for r in Rl}
            Rm = [r for r in Rl if not N0[sg(r)]]
            rec = dict(size=len(st), lam=lam, slack_c=slack_c, Rm=len(Rm))
            if Rm:
                for V in ('V1', 'V2'):
                    cap = {}
                    for r in Rm:
                        cap[('S', ('r', r))] = 2
                        imgs = [] if sg(r) == r else [sg(r)]
                        if gk == 'union': imgs += sigp.get(r, [])
                        E = {exc_of(t) for t in imgs}
                        if V == 'V2': E.add(exc_of(r))
                        for e in E:
                            for y in exc_members(e):
                                if N0[y] and y not in imgl: cap[(('r', r), ('y', y))] = 2; cap[(('y', y), 'T')] = 2
                                elif E2[y]: cap[(('r', r), ('y', y))] = 1; cap[(('y', y), 'T')] = 1
                                elif TAU[y]: cap[(('r', r), ('y', y))] = 3; cap[(('y', y), 'T')] = 3
                    rec[V] = maxflow(cap, 'S', 'T') >= 2 * len(Rm)
                # V3: cycle-level payers; cycle Z supplies 2 N0f(Z) + E2(Z) + 3 tau(Z); r may use the cycles of its one-hop images and its own cycle
                cap = {}
                for r in Rm:
                    cap[('S', ('r', r))] = 2
                    imgs = [] if sg(r) == r else [sg(r)]
                    if gk == 'union': imgs += sigp.get(r, [])
                    for z in {cyc[t] for t in imgs} | {cyc[r]}:
                        sup = sum(2 if (N0[y] and y not in imgl) else 1 if E2[y] else 3 if TAU[y] else 0 for y in H.cycles[z])
                        if sup: cap[(('r', r), ('z', z))] = 2; cap[(('z', z), 'T')] = sup
                rec['V3'] = maxflow(cap, 'S', 'T') >= 2 * len(Rm)
            recs.append(rec)
        res[gk] = recs
    det = Counter()
    for r in range(S):
        if not Rlit[r]: continue
        s = sg(r)
        if N0[s]: continue
        j = fr[r][0]; hi = [(t - j) % 5 for t in range(5) if deg[t] >= 6]; k = hi[0] if hi else None
        kind = 'fixed' if s == r else ('DL' if DL[s] else ('Lock2-only' if filled[pinv[s]] else 'Lock1-only'))
        if s == r or kind == 'DL': det[(k, kind, fullring(r), None)] += 1; continue
        a = s; back = 0
        while not filled[pinv[a]]: a = pinv[a]; back += 1
        u = 0; y = a
        while not filled[y]: u += 1; y = pi[y]
        ff = 0
        while filled[y]: ff += 1; y = pi[y]
        fp = 0; y = pinv[a]
        while filled[y]: fp += 1; y = pinv[y]
        det[(k, kind, fullring(r), 'fprev%d u%d f%d' % (fp, u, ff))] += 1
    return res, det

def job(args):
    src, name, rot, _ = args; out = []
    for h, pat in NB.holes_of(rot):
        if pat != (5, 5, 5, 5, 6): continue
        for mirror in (False, True):
            H = Hole(name, h, mirror, rot=[list(x) for x in rot])
            res, det = analyse2(H)
            out.append(dict(src=src, name=name, hole=h, mirror=mirror, groups=res, det={repr(k): v for k, v in det.items()}))
    return out

if __name__ == '__main__':
    nc = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    J = NB.sources()
    with open(os.path.join(HERE, 'nightbudget2-records.jsonl'), 'w') as fo, Pool(nc) as P:
        for i, recs in enumerate(P.imap_unordered(job, J)):
            for r in recs: fo.write(json.dumps(r) + '\n')
            if i % 100 == 0: print(i, time.strftime('%H:%M:%S'), flush=True)
    print('done', flush=True)
