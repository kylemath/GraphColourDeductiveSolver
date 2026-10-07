#!/usr/bin/env python3
"""[exploratory] NightBudget: test the per-group budget B' of NightPostAW §3 (see SolvingFrameworkPlan/docs/working/NightBudget.md).

Engine: uv_lib.Hole (kempe_py.Space + escape.pi_of; all states of T - h up to renaming), either orientation.
Per hole with link degrees {5,5,5,5,6} (and {5,5,5,5,5} as a control) and per sigma-group and (sigma u sigma')-group g:
  lam-sum, |DD|, N0, E2, tau (exact identity checked), R (= R3-typed DD endpoints, type from w0, w3 as uv_lib.frame),
  R- (sigma-image not lockless: fixed / Lock1-only / Lock2-only / DL), N0f (lockless states of g not in sigma(R)),
  B' slack = 2 N0f + E2 + 3 tau - 2 |R-|  (= 2 N0 + E2 + 3 tau - 2 |R|),  DD loss = |DD| - 2|R|;
  the same with R_rho = rho(DD) (rho(d) = d if d is R3, else pi d if pi d is R3, else d), for which |DD| <= 2|R_rho| always.
U34 accounting: for every r in R with a failing image s = sigma r, the excursion of s (u, f) and what it puts on the right side of B'.
Usage: nightbudget.py [ncores]   (default 2)."""
import sys, os, json, time, itertools
from collections import Counter, defaultdict
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobuv', '../jobas', '../../common', '../../22-winding-escape'): sys.path.insert(0, os.path.join(HERE, d))
from uv_lib import Hole
from flipsearch import rotation as rot_of_faces
from kempe_py import plantri_ascii
PS = os.path.join(HERE, '../../../..')            # backgroundMaterial/planemap-structural
MAXSTATES = 400000

def sources():
    out = []
    for n in range(12, 23):
        fn = os.path.join(PS, 'triangulations-min5-%d.txt' % n)
        if not os.path.exists(fn): fn = os.path.join(PS, 'longtable/wp17-last-roots/triangulations-min5-%d.txt' % n)
        if not os.path.exists(fn): continue
        for i, l in enumerate(open(fn)):
            if l.strip(): out.append(('census', 'g%d#%d' % (n, i + 1), plantri_ascii(l), None))
    C = json.load(open(os.path.join(PS, 'longtable/wp13-generator/corpus.json')))['graphs']
    for g in C:
        if g['order'] <= 40: out.append(('wp13', g['id'], g['rotation'], None))
    R = HERE + '/..'
    for f in sorted(os.listdir(R + '/jobaw/hits')):
        out.append(('AW-hit', f[:-5], rot_of_faces([tuple(t) for t in json.load(open(R + '/jobaw/hits/' + f))['faces']]), 22))
    for f in sorted(os.listdir(R + '/jobas')):
        if f.startswith('best-') and f.endswith('.json'):
            out.append(('AS-construction', f[5:-5], rot_of_faces([tuple(t) for t in json.load(open(R + '/jobas/' + f))['faces']]), None))
    w = json.load(open(R + '/witness-sigC-p26-70869-h11.json')); out.append(('witness', 'p26#70869(sigmaC-fail)', w['rotation'], None))
    w = json.load(open(R + '/jobuv/jobu-p27-133619-h21.json')); out.append(('witness', 'p27#133619', w['plantri']['rotation_system'], None))
    w = json.load(open(R + '/jobuv/jobak-counterexample.json')); out.append(('witness', 'p25#668', w['rotation_system'], None))
    w = json.load(open(R + '/jobuv/jobal-Ldeath-counterexample.json')); out.append(('witness', 'jobal-Ldeath:' + str(w['graph']), w['rotation_system'], None))
    w = json.load(open(R + '/jobaz/jobaz-p26-87942-h22.json')); w = w[0] if isinstance(w, list) else w
    out.append(('witness', 'p26#87942', w['rotation'], None))
    return out

def holes_of(rot, allpat=False):
    for h, nb in enumerate(rot):
        if len(nb) != 5: continue
        d = sorted(len(rot[x]) for x in nb)
        if allpat or d in ([5, 5, 5, 5, 6], [5, 5, 5, 5, 5]): yield h, tuple(d)

def analyse(H):
    S = H.S; pi = H.pi; pinv = H.pinv
    filled = [H.filled(k) for k in range(S)]
    DL = [not filled[k] and not filled[pi[k]] and not filled[pinv[k]] for k in range(S)]
    assert DL == list(H.DL), 'Lemma P (DL) mismatch'
    N0 = [not filled[k] and filled[pi[k]] and filled[pinv[k]] for k in range(S)]
    DD = [DL[k] and DL[pi[k]] for k in range(S)]
    DDE = [DD[k] or DD[pinv[k]] for k in range(S)]
    E2 = [filled[pinv[k]] and not filled[k] and not filled[pi[k]] and filled[pi[pi[k]]] for k in range(S)]
    TAU = [filled[k] and filled[pi[k]] for k in range(S)]
    fr = {}; sig = {}
    for k in range(S):
        if DL[k]: fr[k] = H.frame(k)
    R3 = [DL[k] and fr[k][1] == 3 for k in range(S)]
    for k in range(S):
        if DDE[k]: sig[k] = H.sigma(k)
    def sg(k):
        if k not in sig: sig[k] = H.sigma(k)
        return sig[k]
    # sigma is an involution on unfilled states (spot check on DD endpoints)
    for k in list(sig):
        assert sg(sig[k]) == k, 'sigma not an involution'
    Rlit = [R3[k] and DDE[k] for k in range(S)]
    Rrho = [False] * S
    for d in range(S):
        if DD[d]:
            r = d if R3[d] else (pi[d] if R3[pi[d]] else d); Rrho[r] = True
    # groups: union-find over pi-cycles
    nc = len(H.cycles); cyc = H.cyc
    def mkuf():
        up = list(range(nc))
        def f(x):
            while up[x] != x: up[x] = up[up[x]]; x = up[x]
            return x
        return up, f
    up1, f1 = mkuf(); up2, f2 = mkuf()
    linkmask = 0
    for i in H.sp.linki: linkmask |= 1 << i
    for k in range(S):
        if not DDE[k]: continue
        a, b = f1(cyc[k]), f1(cyc[sig[k]]); up1[a] = b
        a, b = f2(cyc[k]), f2(cyc[sig[k]]); up2[a] = b
        for t, p, q, K in H.sp.moves(k):
            if t == k or K & linkmask or DL[t]: continue
            a, b = f2(cyc[k]), f2(cyc[t]); up2[a] = b
    res = {}
    for gname, f in (('sigma', f1), ('union', f2)):
        G = defaultdict(list)
        for c in range(nc): G[f(c)].append(c)
        recs = []
        for root, cs in G.items():
            st = [k for c in cs for k in H.cycles[c]]; inS = set(st)
            lam = sum(H.lam[k] for k in st); nDD = sum(DD[k] for k in st); nN0 = sum(N0[k] for k in st)
            nE2 = sum(E2[k] for k in st); nT = sum(TAU[k] for k in st); F = sum(filled[k] for k in st)
            assert lam == nDD - 2 * nN0 - nE2 - 3 * nT, 'exact identity'
            assert lam == len(st) - 4 * F, 'Theorem W'
            rec = dict(size=len(st), ncyc=len(cs), lam=lam, DD=nDD, N0=nN0, E2=nE2, tau=nT, F=F,
                       ncyc_pos=sum(1 for c in cs if H.W[c] > 0), maxw=max(H.W[c] for c in cs))
            for tag, R in (('lit', Rlit), ('rho', Rrho)):
                Rs = [k for k in st if R[k]]
                img = {sg(r) for r in Rs}
                assert img <= inS, 'sigma image left the group'
                Rm = [r for r in Rs if not N0[sg(r)]]
                N0f = sum(1 for k in st if N0[k] and k not in img)
                assert len(Rm) - N0f == len(Rs) - nN0
                rec[tag] = dict(R=len(Rs), Rm=len(Rm), N0f=N0f, slack=2 * N0f + nE2 + 3 * nT - 2 * len(Rm), ddloss=nDD - 2 * len(Rs),
                                Rm_kinds=dict(Counter(('fixed' if sg(r) == r else 'DL' if DL[sg(r)] else 'L1' if filled[pinv[sg(r)]] is False and filled[pi[sg(r)]] else 'L2')
                                                      for r in Rm)))
            recs.append(rec)
        res[gname] = recs
    # U34 accounting: failing images of R (lit) by k = position of the degree-6 vertex relative to j
    u34 = Counter(); u34rhs = Counter()
    deg = [len(H.rot[x]) for x in H.L]
    for r in range(S):
        if not Rlit[r]: continue
        s = sg(r)
        if N0[s]: continue
        j = fr[r][0]; hi = [(t - j) % 5 for t in range(5) if deg[t] >= 6]; k = hi[0] if hi else None
        kind = 'fixed' if s == r else ('DL' if DL[s] else ('Lock2-only' if filled[pinv[s]] else 'Lock1-only'))
        if s == r: u34[(k, kind, None)] += 1; continue
        a = s; back = 0
        while not filled[pinv[a]] and back < 100000: a = pinv[a]; back += 1
        if back >= 100000: u34[(k, kind, 'Gamma')] += 1; continue
        u = 0; y = a; nR = 0; nDDr = 0
        while not filled[y]: nR += Rlit[y]; nDDr += DD[y]; u += 1; y = pi[y]
        ff = 0
        while filled[y]: ff += 1; y = pi[y]
        rhs = (2 if u == 1 else 0) + (1 if u == 2 else 0) + 3 * (ff - 1)
        u34[(k, kind, 'pos%d u%d f%d' % (back, u, ff))] += 1
        u34rhs[(k, kind, 'rhs %d, DD %d, R %d' % (rhs, nDDr, nR))] += 1
    return res, u34, u34rhs, deg

def job(args):
    src, name, rot, onlyhole = args
    out = []
    for h, pat in holes_of(rot, src == 'witness'):
        for mirror in (False, True):
            t = time.time()
            try:
                H = Hole(name, h, mirror, rot=[list(x) for x in rot])
            except Exception as e:
                out.append(dict(src=src, name=name, hole=h, mirror=mirror, error=repr(e))); continue
            if H.S > MAXSTATES: out.append(dict(src=src, name=name, hole=h, mirror=mirror, skipped=H.S)); continue
            res, u34, u34rhs, deg = analyse(H)
            out.append(dict(src=src, name=name, n=len(rot), hole=h, mirror=mirror, pattern=pat, linkdeg=deg, states=H.S, secs=round(time.time() - t, 1),
                            groups=res, u34={repr(k): v for k, v in u34.items()}, u34rhs={repr(k): v for k, v in u34rhs.items()}))
    return out

if __name__ == '__main__':
    nc = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    J = sources()
    print('graphs', len(J), Counter(s for s, *_ in J), flush=True)
    with open(os.path.join(HERE, 'nightbudget-records.jsonl'), 'w') as fo, Pool(nc) as P:
        for i, recs in enumerate(P.imap_unordered(job, J)):
            for r in recs: fo.write(json.dumps(r) + '\n')
            fo.flush()
            if i % 50 == 0: print(i, time.strftime('%H:%M:%S'), flush=True)
    print('done')
