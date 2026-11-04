"""s63: for every tight receiver row of sol_c (viol file: rows within 1e-5 of the cap), find the table entries whose un-killing raises that row's load.
usage: analyze.py VIOL OUT.pkl  <engine args...>   (engine args = the upperR2 flag set, sol=, f2b=, ...)"""
import sys, os, json, pickle, itertools, collections, time
ENG = os.path.join(os.environ['E63'], 'pcheck.py'); viol = sys.argv[1]; out = sys.argv[2]
sys.argv = [ENG, 'help'] + sys.argv[3:]
ns = {'__file__': ENG, '__name__': 'pcheck_s63'}
exec(compile(open(ENG).read(), ENG, 'exec'), ns)
OPT = ns['OPT']; Sj = json.load(open(OPT['sol'])); t = Sj['t']
ns['l3q_load'](); ns['kt_load']()
y = ns['np'].zeros(len(ns['ROOTS']))
for k, v in Sj['y'].items():
    u, rest = k.split('|'); y[ns['RIX'][ns['root'](list((int(u),) + tuple(int(c) for c in rest)), 0)]] = v
HV2 = {tuple(k): v for k, v in Sj['h']}; RV = {tuple(k): v for k, v in Sj.get('r', [])}; RRV = {tuple(k): v for k, v in Sj.get('rr', [])}
xd = {int(k): v for k, v in Sj.get('x', {}).items()}
ns['LQV'].clear(); ns['LQV'].update({tuple(k): v for k, v in Sj.get('lq', [])}); ns['LQQ'].clear(); ns['LQQ'].update({tuple(k): v for k, v in Sj.get('lQ', [])})
ns['RV'].clear(); ns['RV'].update(RV); ns['RRV'].clear(); ns['RRV'].update(RRV)
mc = {}
def MV2(sg):
    if sg not in mc:
        ks = ns['sig2_keys'](sg); mc[sg] = max(HV2.get(k, 0.0) for k in ks) if ks else None
    return mc[sg]
def val(k):
    if k[0] == 'y': return y[ns['RIX'][k[1]]]
    if k[0] == 'x': return xd.get(k[1], 0.0)
    if k[0] == 'M': v = MV2(k[1]); return 0.0 if v is None else v
    if k[0] == 'r': return RV.get(k[1], 0.0)
    if k[0] == 'rr': return RRV.get(k[1], 0.0)
    if k[0] == 'lq': return ns['LQV'].get(k[1], 0.0)
    if k[0] == 'lQ': return ns['l3q_Qeff'](*k[1]) if len(k[1]) == 3 else ns['l3q_QeffV'](*k[1])
    raise Exception('unsupported key %s' % (k,))
rcr = ns['recv_coef_R2']
def load(d, lk, sv): return sum(c * val(k) for k, c in rcr(d, lk, sv, True, None).items())
f2bm = ns['f2bm']; KT = ns['KT']; amask = ns['amask']; L3T = ns['L3T']
SKIP = set()
def firing(g, d, w, s, i):
    idx = f2bm._IDX[g]; sm1, s0 = s[(i - 1) % d], s[i]; res = []
    for key in ((sm1, s0), (sm1, None), (None, s0), (None, None)):
        for wr, sr, bit in idx.get(key, ()):
            if all(w[(i + o) % d] in al for o, al in wr) and all(s[(i + o) % d] == v for o, v in sr): res.append((wr, sr, bit))
    return res
_o6, _o7 = f2bm.extra6, f2bm.extra7
def mk(g_fmt):
    def f(d, w, s, i, *a):
        if not f2bm.ACTIVE: return 0
        g = g_fmt(d, *a); 
        ex = 0
        for wr, sr, bit in firing(g, d, w, s, i):
            if (g, wr, sr, bit) not in SKIP: ex |= bit
        return ex
    return f
def ex6(d, w, s, i): return 0 if d > 9 or d < 7 else _ex('d%d_w6' % d, d, w, s, i)
def ex7(d, w, s, i, sg): return 0 if d not in (7, 8) else _ex('d%d_w7_%d' % (d, sg), d, w, s, i)
def _ex(g, d, w, s, i):
    ex = 0
    for wr, sr, bit in firing(g, d, w, s, i):
        if (g, wr, sr) not in SKIP: ex |= bit
    return ex
f2bm.extra6 = ex6; f2bm.extra7 = ex7
rows = [l.split() for l in open(viol)]
t0 = time.time(); res = {}; nbad = 0; ents_all = collections.Counter(); maxdiff = 0
EPSD = 1e-9
for n, (d, ld, ex_, lk, sv) in enumerate(rows):
    d = int(d); w = [int(c) for c in lk]; s = [int(c) for c in sv]; U = min(d, 9)
    L0 = load(d, lk, sv); maxdiff = max(maxdiff, abs(L0 - float(ld)))
    ents = {}
    for j in range(d):
        if w[j] == 6:
            idx = (w[(j - 2) % d] - 5, w[(j - 1) % d] - 5, w[(j + 1) % d] - 5, w[(j + 2) % d] - 5, s[(j - 2) % d] - 5, s[(j - 1) % d] - 5, s[j] - 5, s[(j + 1) % d] - 5)
            km = int(KT[U][idx])
            for b in range(5):
                if (km >> b) & 1:
                    KT[U][idx] = km & ~(1 << b)
                    dl = load(d, lk, sv) - L0
                    KT[U][idx] = km
                    if dl > EPSD: ents[('KT', U, idx, 5 + b)] = dl
            if d <= 9:
                for gr in firing('d%d_w6' % d, d, w, s, j):
                    k_ = ('d%d_w6' % d, gr[0], gr[1])
                    SKIP.add(k_); dl = load(d, lk, sv) - L0; SKIP.discard(k_)
                    if dl > EPSD: ents[('RULE', 'd%d_w6' % d, gr[0], gr[1], 5 + gr[2].bit_length() - 1)] = dl
        if w[j] == 7 and d in (7, 8) and ns['L3Q']:
            for sg in (1, -1):
                c, a, a2, w4 = (w[(j + k * sg) % d] for k in (1, 2, 3, 4))
                ap_, o = (s[j], s[(j - 1) % d]) if sg == 1 else (s[(j - 1) % d], s[j])
                if c > 6 or ap_ > 6: continue
                key = (sg, c, a, a2, w4, ap_, o)
                T = L3T if d == 7 else ns['l3q_loadV'](8)
                if d == 8: key = (sg, c, a, a2, w4, ap_, o)
                m = T[key]
                for b in range(5):
                    if not (m >> b) & 1:
                        T[key] = m | (1 << b); dl = load(d, lk, sv) - L0; T[key] = m
                        if dl > EPSD: ents[('L3Q', d, key, 5 + b)] = dl
                for gr in firing('d%d_w7_%d' % (d, sg), d, w, s, j):
                    k_ = ('d%d_w7_%d' % (d, sg), gr[0], gr[1]); SKIP.add(k_); dl = load(d, lk, sv) - L0; SKIP.discard(k_)
                    if dl > EPSD: ents[('RULE', 'd%d_w7_%d' % (d, sg), gr[0], gr[1], 5 + gr[2].bit_length() - 1)] = dl
    res[(d, lk, sv)] = (L0, ents)
    for e in ents: ents_all[e] += 1
    if n % 1000 == 0: print(n, len(rows), '%.0fs' % (time.time() - t0), 'entries so far', len(ents_all), flush=True)
print('rows', len(rows), 'max |load - viol-file load|', maxdiff, 'rows with >=1 binding entry', sum(1 for v in res.values() if v[1]), 'distinct entries', len(ents_all))
pickle.dump({'res': res, 'ents': ents_all}, open(out, 'wb'))
