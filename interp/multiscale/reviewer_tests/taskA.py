# Task A: forced-alignment 4-vortex merge.  U = A + B on ico20 (a_geom.py), vortex depth d from dU.
# Step 1: one SAT colouring of U with tau(dA) <= 1, tau(dB) <= 1 (each side level, one-lap tau, wk convention) and
#         |t_U|^2 >= 16 (so t_A, t_B have |t| = 2 and are aligned under the identity renaming).
# Step 2: colA = c|A, colB = c|B treated as independent level sides; for all 24 renamings: seam conflicts, exact min R
#         (proper_repair_at), |t_U| after repair, whether the repair zone meets a vortex.
# Step 3: for T in (1, 1.5, 2): min collar width w (exact SAT, ic.walk_int strip half-width) on the repaired colouring.
# Geometry: a_geom2.py (ico17, f_U != 0).  Usage: python taskA.py d [renamings: all|best]
import sys, json, time, math, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/reviewer_tests'); sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic')
from a_geom2 import build
from w2 import *
import ic
from pysat.solvers import Cadical153
OUT = '/mnt/project-files/multiscale/reviewer_tests/A_results.jsonl'

def colour_U(g, D, DA, DB, minT2=16.0):
    enc = ic.Enc(sorted(D.S))
    for u, w in D.edges: enc.neq(u, w)
    f = D.g.faces[next(iter(D.tris))]
    for j in range(3): enc.fix(f[j], j)
    def track(W, Dm, start0=False):
        Ls = enc.labels(W); s = W['s']; m = len(Ls); Ds = set(Dm)
        H = [{p: enc.new() for p in Dm} for _ in range(m+1)]
        for i in range(m):
            for p in Dm:
                for l in (1, 2, 3):
                    dd = INC[l]; q = (p[0]+s[i]*dd[0], p[1]+s[i]*dd[1])
                    enc.cls.append([-H[i][p], -Ls[i][l], H[i+1][q]] if q in Ds else [-H[i][p], -Ls[i][l]])
        if start0: enc.cls.append([H[0][(0, 0)]])
        else:
            enc.cls.append([H[0][p] for p in Dm])
            for p, q in itertools.combinations(Dm, 2): enc.cls.append([-H[0][p], -H[0][q]])
        return H, m
    for W in DA.pockets + DB.pockets: track(W, domain(1.0+1e-9))     # every pocket one-lap tau <= 1 (centre free)
    Db = domain(40.0); H, m = track(D.whole, Db, start0=True)
    for q in Db:
        if n2(q) < minT2-1e-9: enc.cls.append([-H[m][q]])
    s = Cadical153(bootstrap_with=enc.cls); ok = s.solve()
    if not ok: return None
    mod = set(l for l in s.get_model() if l > 0)
    return {v: next(c for c in range(4) if enc.x(v, c) in mod) for v in enc.V}

def min_w(g, D, c2, zone, T, wmax, dB):
    for w in range(wmax+1):
        fx = {v: c2[v] for v in D.S if dB[v] > w and v not in zone}
        if w == 0 and ic.tau_int(D.whole, c2) <= T+1e-9: return 0
        r = ic.sat_disc(D, [D.whole], T, fixed=fx, dmax=2, gcap=30)
        if r not in (None, 'UNK'): return w
    return '>%d' % wmax

if __name__ == '__main__':
    d = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else 'all'
    t0 = time.time(); g, c = build(d=d); A, B, U = c['A'], c['B'], c['U']
    D, DA, DB = Disc(g, U), Disc(g, A), Disc(g, B)
    vort = set(c['vort']); dBU = multi_bfs(g.adj, list(D.bset), D.S)
    col = colour_U(g, D, DA, DB)
    print('colour U', 'UNSAT' if col is None else 'SAT', round(time.time()-t0, 1), flush=True)
    if col is None: print(json.dumps(dict(d=d, status='UNSAT')), file=open(OUT, 'a')); sys.exit()
    colA = {v: col[v] for v in A}; colB = {v: col[v] for v in B}
    base = dict(d=d, nU=len(U), nA=len(A), nB=len(B), mU=len(D.whole['walk']), mA=len(DA.whole['walk']), mB=len(DB.whole['walk']),
                depths=sorted(dBU[o] for o in vort), tauA=[round(tau_walk(W, colA), 3) for W in DA.pockets], tauB=[round(tau_walk(W, colB), 3) for W in DB.pockets], fU=sum(D.whole['s']) % 3,
                tA=tvec(DA.whole, colA), tB=tvec(DB.whole, colB), tU_id=tvec(D.whole, col),
                tauU_onelap_id=round(tau_walk(D.whole, col), 3), tauU_strip_id=round(ic.tau_int(D.whole, col), 3))
    print(base, flush=True)
    seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]; base['seam'] = len(seam)
    rows = []
    for p in PERMS:
        cc = {v: colA[v] for v in A}; cc.update({v: p[colB[v]] for v in B})
        K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e)
        R = None
        for RR in range(4):
            r, c2 = (0, cc) if not K else proper_repair_at(g, D.S, cc, K, RR)
            if r is not None: R = RR; break
        row = dict(perm=''.join(map(str, p)), nconf=len(K), R=R)
        if R is not None:
            zone = set(v for v in D.S if c2[v] != cc[v])
            row.update(zone=len(zone), zone_vort=len(zone & vort), tU=tvec(D.whole, c2), tau_strip=round(ic.tau_int(D.whole, c2), 3),
                       tau_onelap=round(tau_walk(D.whole, c2), 3), zone_depth=min([dBU[v] for v in zone], default=None))
            row['_c2'] = c2; row['_zone'] = zone
        rows.append(row)
    okrows = [r for r in rows if r['R'] is not None]
    # w for: every renaming (mode all) or the identity-class + min-|t_U| renaming at min R (mode best)
    Rmin = min(r['R'] for r in okrows)
    sel = okrows if mode == 'all' else [r for r in okrows if r['R'] == Rmin or r['nconf'] == 0][:3] + sorted(okrows, key=lambda r: (r['tU'] if r['tU'] is not None else 99, r['R']))[:2]
    seen = set()
    for r in sel:
        if r['perm'] in seen: continue
        seen.add(r['perm'])
        for T in (1.0, 1.5, 2.0):
            t1 = time.time(); r['w_T%s' % T] = min_w(g, D, r['_c2'], r['_zone'], T, d+1, dBU); r['sec_T%s' % T] = round(time.time()-t1, 1)
        print({k: v for k, v in r.items() if not k.startswith('_')}, flush=True)
    for r in rows: r.pop('_c2', None); r.pop('_zone', None)
    base.update(rows=rows, sec=round(time.time()-t0, 1))
    open(OUT, 'a').write(json.dumps(base)+'\n')
    print('min |t_U| over renamings', min(r['tU'] for r in okrows if r['tU'] is not None), 'Rmin', Rmin, flush=True)
