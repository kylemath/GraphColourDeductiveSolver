# s48: stage-1 loads of the A78 cert receiverR2 rows at the upper solution, and their big neighbours' worst-case spare.
# Usage: python3 loads.py ENGINE_DIR SOL CERT OUT_JSON [mode=rows|nb] [flags...]
import sys, os, json, itertools, collections, time
ENG, SOLF, CERTF, OUTF, MODE = sys.argv[1:6]
sys.argv = [os.path.join(ENG, 'pcheck.py'), 'none'] + sys.argv[6:]
__file__ = sys.argv[0]
src = open(sys.argv[0]).read()
src = src[:src.rindex("{'pcellcheck'")]   # everything but the command dispatch
exec(compile(src, sys.argv[0], 'exec'))
load_patterns(); xon = 'xon' in FLAGS
Sj = json.load(open(SOLF)); t = Sj['t']
VAL = {('y', k): v for k, v in Sj['y'].items()}
for fam in ('g', 'h', 'z', 'zr', 'r', 'rr', 'lq', 'lQ', 'z6', 'Z6', 'q', 'f'):
    for k, v in Sj.get(fam, []): VAL[(fam, tuple(k))] = v
for k, v in Sj.get('D', []): VAL[('D', eval(k))] = v
for k, v in Sj.get('x', {}).items(): VAL[('x', int(k))] = v
HV2 = {tuple(k): v for k, v in Sj['h']}
LQV.clear(); LQV.update({tuple(k): v for k, v in Sj.get('lq', [])}); LQQ.clear(); LQQ.update({tuple(k): v for k, v in Sj.get('lQ', [])})
if L3Q: l3q_load()
assert not Sj.get('D') and not Sj.get('z') and not Sj.get('q') and not Sj.get('v') and not Sj.get('rr')
mc = {}
def val(k):
    if k[0] == 'y': return VAL.get(('y', rname(k[1])), 0.0)
    if k[0] == 'M':
        if k[1] not in mc: mc[k[1]] = max([HV2.get(tuple(h), 0.0) for h in sig2_keys(k[1])] or [0.0])
        return mc[k[1]]
    if k[0] == 'lQ': return l3q_Qeff(*k[1])   # as upperR2: Q = max(sol, max q over the mask)
    return VAL.get(k, 0.0)
STAGE1 = ('y', 'M', 'r')       # five -> big (direct y, through a 6 hat M, through a 5 hat r)
BIGBIG = ('x', 'lq', 'lQ')     # big <-> big (L2 tau, l3q)
def loads(d, lk, sv):
    cf = recv_coef_R2(d, lk, sv, xon); g = collections.defaultdict(float)
    for k, c in cf.items():
        if c: g[k[0]] += c * val(k)
    unk = set(g) - set(STAGE1) - set(BIGBIG)
    assert not any(abs(g[f]) > 1e-12 for f in unk), (d, lk, sv, dict(g))
    s1 = sum(g[f] for f in STAGE1); bb = sum(g[f] for f in BIGBIG)
    return (6 - d) + s1, (6 - d) + s1 + bb, dict(g)
C = json.load(open(CERTF)); R = sorted([c for c in C if c['row'][0] == 'receiverR2'], key=lambda c: c['w'])
out = {'t': t, 'rows': []}
if MODE == 'rows':
    for c in R:
        _, d, lk, sv = c['row']
        L1, Lf, g = loads(d, lk, sv)
        out['rows'].append(dict(w=c['w'], d=d, lk=lk, sv=sv, L1=L1, Lf=Lf, fam=g, adm=admissible(d, lk, sv)))
        print(d, lk, sv, 'L1 %.6f Lfull %.6f slack %.3g' % (L1, Lf, t - Lf), {k: round(v, 6) for k, v in g.items()}, flush=True)
else:
    want = sys.argv[sys.argv.index('nbrow') + 1] if 'nbrow' in sys.argv else None
    y = np.zeros(len(ROOTS))
    for k, v in Sj['y'].items():
        u_, rest = k.split('|'); r_ = root(list((int(u_),) + tuple(int(ch) for ch in rest)), 0); y[RIX[r_]] = v
    xd = {int(k): v for k, v in Sj.get('x', {}).items()}
    RV.clear(); RV.update({tuple(k): v for k, v in Sj.get('r', [])}); RRV.clear()
    def MV2(sg):
        ks = sig2_keys(sg); return max(HV2.get(k, 0.0) for k in ks) if ks else None
    WT = {}
    def wtab(U):
        if U not in WT:
            Wf = window_table_R2(U, y, xd, MV2)
            g_ = globals(); sv_ = g_['L3Q']; g_['L3Q'] = False
            W1 = window_table_R2(U, y, {}, MV2); g_['L3Q'] = sv_
            WT[U] = (Wf.reshape(-1), W1.reshape(-1))
        return WT[U]
    def wsum(Wflat, Lidx, Tidx, dv):
        # Lidx: (n, dv) letter indices of link, Tidx: (n, dv) apex indices; window at i: a,b,c,e,f = L[i-2..i+2]; p,q,r,s = T[i-2..i+1]
        tot = np.zeros(Lidx.shape[0])
        for i in range(dv):
            ix = 0
            for o in (-2, -1, 0, 1, 2): ix = ix * 5 + Lidx[:, (i + o) % dv]
            for o in (-2, -1, 0, 1): ix = ix * 5 + Tidx[:, (i + o) % dv]
            tot += Wflat[ix]
        return tot
    rng = np.random.default_rng(48); chk = [0, 0, 0.0]
    def bb(dv, Lidx, Tidx, ws, which, sgn):
        """exact max (sgn=+1) or min (sgn=-1) of the load over admissible rows, using ws (window sums, exact or UB) to order"""
        fin = np.where(np.isfinite(ws))[0]; o = fin[np.argsort(-sgn * ws[fin], kind='stable')]; best = None; bestrow = None; nex = 0
        for k in o:
            if best is not None and sgn * ws[k] < sgn * best - 1e-12: break
            lks = ''.join(str(LET[v]) for v in Lidx[k]); svs = ''.join(str(LET[v]) for v in Tidx[k])
            nex += 1
            if admissible(dv, lks, svs) is not None: continue
            L1, Lf, g = loads(dv, lks, svs); v = (L1, Lf)[which]
            if best is None or sgn * v > sgn * best: best, bestrow = v, lks + '/' + svs
            if which == 0 or sgn > 0: pass
        return best, bestrow, nex
    for c in R:
        _, d, lk, sv = c['row']; w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
        if want and want != '%s/%s' % (lk, sv): continue
        for j in range(d):
            if w[j] < 7: continue
            dv = w[j]; W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]
            # v's link from u: (u, w_{j+1}, s_j, p_1..p_{dv-5}, s_{j-1}, w_{j-1}); apex t_m across (L_m, L_{m+1}) (Lemma 44.1)
            L = [d, W_(j + 1), S_(j)] + [None] * (dv - 5) + [S_(j - 1), W_(j - 1)]
            T = [None] * dv; T[0] = W_(j + 2); T[dv - 1] = W_(j - 2)
            if W_(j + 1) == 5: T[1] = S_(j + 1)
            if W_(j - 1) == 5: T[dv - 2] = S_(j - 2)
            fl = [i for i in range(dv) if L[i] is None]; ft = [i for i in range(dv) if T[i] is None]
            t0 = time.time()
            G = np.array(list(itertools.product(range(5), repeat=len(fl) + len(ft))), dtype=np.int64).reshape(-1, len(fl) + len(ft))
            n = G.shape[0]
            Lidx = np.tile(np.array([LI[x] if x is not None else 0 for x in L], dtype=np.int64), (n, 1))
            Tidx = np.tile(np.array([LI[x] if x is not None else 0 for x in T], dtype=np.int64), (n, 1))
            for q_, i in enumerate(fl): Lidx[:, i] = G[:, q_]
            for q_, i in enumerate(ft): Tidx[:, i] = G[:, len(fl) + q_]
            Wf, W1 = wtab(min(dv, 9))
            wf = wsum(Wf, Lidx, Tidx, dv) + (6 - dv); w1 = wsum(W1, Lidx, Tidx, dv) + (6 - dv)
            # spot check: window sums vs the exact Python load on random window-finite admissible rows
            fin = np.where(np.isfinite(w1))[0]
            for k in rng.choice(fin, min(300, len(fin)), replace=False):
                lks = ''.join(str(LET[v]) for v in Lidx[k]); svs = ''.join(str(LET[v]) for v in Tidx[k])
                if admissible(dv, lks, svs) is not None: continue
                L1, Lf, g = loads(dv, lks, svs); chk[0] += 1
                if abs(L1 - w1[k]) > 1e-9: chk[1] += 1
                chk[2] = max(chk[2], Lf - wf[k])   # must be <= 0 (window is exact or an upper bound)
            mx1 = bb(dv, Lidx, Tidx, w1, 0, 1); mn1 = bb(dv, Lidx, Tidx, w1, 0, -1)
            mxf = bb(dv, Lidx, Tidx, wf, 1, 1)
            rec = dict(row='%d %s/%s' % (d, lk, sv), j=j, dv=dv, link=''.join('?' if x is None else str(x) for x in L),
                       apex=''.join('?' if x is None else str(x) for x in T), n=n, nfin=int(np.isfinite(w1).sum()),
                       L1max=mx1, L1min=mn1, Lfmax=mxf, sec=round(time.time() - t0, 1))
            out['rows'].append(rec); print(json.dumps(rec), flush=True)
    out['check'] = chk; print('check: rows %d, |L1-window|>1e-9: %d, max(Lfull - window) %.3g' % tuple(chk))
json.dump(out, open(OUTF, 'w'), indent=1)
