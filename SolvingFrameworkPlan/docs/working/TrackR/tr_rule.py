#!/usr/bin/env python3
"""Track R: "local universal rule" test.  Restrict the price certificate of tr_lag.py to the form
    u_{t,e} = f( N(t), pattern_t(e) ),   pattern_t(e) = (name of e's pair/role at states t-r .. t+r)  (cyclic)
with ONE function f shared by all states of the cycle (rotation-equivariant) and, optionally, by several cycles.
Link edges get price 0.  Feasibility: sum_t f(N(t), pattern_t(e)) <= 1 for every ground edge e of every cycle.
Value of a cycle: sum_t sum_P MST_P(u_t) + 5.  We maximise min over cycles of (value - base) by Kelley cutting planes.
If the optimum is > 0 for every cycle, the rule f is a candidate universal certificate.
usage: tr_rule.py R MODE DATA.json [DATA.json ...]   MODE in {role, pair}+[K][T] (K: also flag 'e cut by K_s'; T: key includes absolute state t, i.e. no rotation sharing;
       A: key includes offset t - anchor, anchors given as DATA.json@a, shared across cycles)
       [--out F.json]"""
import sys, os, json, time, itertools, collections
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load, part_edges, mst, verify
sys.path.insert(0, os.path.join(HERE, '..', 'TrackQ'))
from tq_roles import roles


def names(c):
    j, (a, m, A, B) = roles(c); nm = {a: 'a', m: 'm', A: 'A', B: 'B'}
    return nm


def role_of(nm, cx, cy):
    s = ''.join(sorted(nm[cx] + nm[cy], key='amAB'.index))
    return s


ROLE = {'am': '1', 'AB': '1', 'aA': '2', 'mB': '2', 'aB': '3', 'mA': '3'}


def swapset(c, n):
    """K_t = component of the alpha-A pair graph containing x_{j+2} -- computed from the next state instead (vertices
    whose colour changes up to renaming); here: vertices v with c_t(v) in {alpha, A} that change colour at t+1 is
    not well defined up to renaming, so we use the role names: K = vertices that are alpha/A at t and A/alpha at t+1."""
    return None


def keys_for(D, r, mode, anchor=0):
    U = D['U']; cols = D['cols']; L = len(cols); n = D['n']
    nms = [names(c) for c in cols]
    # K_t: vertices whose role name goes a->A' ... we use: role name at t in {a,A} and at t+1 name differs in the
    # sense alpha<->A: under pi, roles (alpha,mu,A,B)_{t+1} = (alpha, B, mu, A) in t's colours; swapped vertices are
    # exactly those coloured alpha/A at t whose colour (as integer) changed between the two stored colourings after
    # renaming.  Stored colourings are canonical up to renaming, so we test membership by the role map.
    Ks = []
    for t in range(L):
        c, c2 = cols[t], cols[(t + 1) % L]
        j, (a, m, A, B) = roles(c); j2, (a2, m2, A2, B2) = roles(c2)
        # colour map t -> t+1 on unswapped vertices: alpha->alpha2, mu->A2 (mu becomes A), B->mu2 (B becomes mu), A->B2
        mp = {a: a2, m: A2, B: m2, A: B2}
        K = {v for v in range(1, n) if mp[c[v]] != c2[v]}
        assert all(c[v] in (a, A) for v in K), 'swap set not alpha/A'
        Ks.append(K)
    # universal part tags: pair name + frame-relative positions of the link vertices in the part ('Z' if none)
    ptag = []
    for t in range(L):
        c = cols[t]; j, _ = roles(c); nm = nms[t]; tg = {}
        for (tt, p, q, P) in D['parts']:
            if tt != t: continue
            pos = sorted((v - 1 - j) % 5 for v in P if 1 <= v <= 5)
            s_ = ''.join(map(str, pos)) or 'Z'
            for v in P: tg.setdefault(v, {})[(p, q)] = s_
        ptag.append(tg)
    keys = {}
    for t in range(L):
        for k, (x, y) in enumerate(U):
            if k in D['forced']: continue
            pat = []
            for s in range(t - r, t + r + 1):
                ss = s % L; nm = nms[ss]; pn = role_of(nm, cols[ss][x], cols[ss][y])
                tok = ROLE[pn] if mode.startswith('role') else pn
                if mode.startswith('part'): tok = pn + ':' + ptag[ss][x][tuple(sorted((cols[ss][x], cols[ss][y])))]
                if 'K' in mode: tok += '*' if ((x in Ks[ss]) != (y in Ks[ss])) else ''
                pat.append(tok)
            keys[(t, k)] = (D['Nprof'][t],) + tuple(pat) + ((t,) if 'T' in mode else ()) + ((('d', (t - anchor) % L),) if 'A' in mode else ()) + ((k,) if 'E' in mode else ())
    return keys


def main():
    a = sys.argv[1:]; out = None; only = None
    if '--states' in a: i = a.index('--states'); only = {int(z) for z in a[i + 1].split(',')}; del a[i:i + 2]
    if '--out' in a: i = a.index('--out'); out = a[i + 1]; del a[i:i + 2]
    r = int(a[0]); mode = a[1]; files = a[2:]
    anc = [int(f.split('@')[1]) if '@' in f else 0 for f in files]; files = [f.split('@')[0] for f in files]
    Ds = [load(f) for f in files]
    KS = [keys_for(D, r, mode, a_) for D, a_ in zip(Ds, anc)]
    if only is not None: KS = [{tk: v for tk, v in K.items() if tk[0] in only} for K in KS]
    allkeys = sorted({v for K in KS for v in K.values()})
    kid = {k: i for i, k in enumerate(allkeys)}; nf = len(allkeys)
    print('cycles', len(Ds), 'keys', nf, flush=True)
    # variables: f_key (nf), w_{c,i} per part, z
    PEs = [part_edges(D['U'], D['parts']) for D in Ds]
    woff = []; o = nf
    for D in Ds: woff.append(o); o += len(D['parts'])
    zi = o; nvar = o + 1
    rows = []  # (cols list, vals list, rhs)  A x <= b
    # column sum per edge: sum_t f(key(t,e)) <= 1  (aggregate duplicates)
    seenrow = set()
    for D, K in zip(Ds, KS):
        L = len(D['cols'])
        for k in range(len(D['U'])):
            if k in D['forced']: continue
            cnt = collections.Counter(kid[K[(t, k)]] for t in range(L) if (t, k) in K)
            if not cnt: continue
            key = tuple(sorted(cnt.items()))
            if key in seenrow: continue
            seenrow.add(key); rows.append(([i for i, _ in key], [float(v) for _, v in key], 1.0))
    base_rows = list(rows)
    # value rows: z - sum_i w_{c,i} <= 5 - base_c     (value_c = sum w + 5 ; want value_c - base_c >= z)
    for ci, D in enumerate(Ds):
        base = 3 * (D['n'] - 1) - 8
        idx = [zi] + [woff[ci] + i for i in range(len(D['parts']))]
        base_rows.append((idx, [1.0] + [-1.0] * len(D['parts']), 5.0 - base))
    cuts = []; seen = set()
    def price(ci, x, t, k):
        D = Ds[ci]
        if k in D['forced'] or (t, k) not in KS[ci]: return 0.0
        return x[kid[KS[ci][(t, k)]]]
    def addcut(ci, i, T):
        key = (ci, i, tuple(sorted(T)))
        if key in seen: return 0
        seen.add(key); cuts.append(key); return 1
    for ci, D in enumerate(Ds):
        for i, (t, p, q, P) in enumerate(D['parts']):
            addcut(ci, i, mst(P, D['U'], PEs[ci][i], {k: 0 for k in PEs[ci][i]})[1])
    c = np.zeros(nvar); c[zi] = -1.0
    bounds = [(0, 1)] * nf + [(None, None)] * (nvar - nf - 1) + [(None, None)]
    t0 = time.time(); it = 0
    while True:
        it += 1
        ri, rj, rv, bb = [], [], [], []; nr = 0
        for (idx, vals, rhs) in base_rows:
            ri += [nr] * len(idx); rj += idx; rv += vals; bb.append(rhs); nr += 1
        for (ci, i, T) in cuts:
            D = Ds[ci]; t = D['parts'][i][0]
            cnt = collections.Counter(kid[KS[ci][(t, k)]] for k in T if k not in D['forced'] and (t, k) in KS[ci])
            ri.append(nr); rj.append(woff[ci] + i); rv.append(1.0)
            for j, v in cnt.items(): ri.append(nr); rj.append(j); rv.append(-float(v))
            bb.append(0.0); nr += 1
        A = coo_matrix((rv, (ri, rj)), shape=(nr, nvar)).tocsr()
        res = linprog(c, A_ub=A, b_ub=np.array(bb), bounds=bounds, method='highs')
        assert res.status == 0, res.message
        x = res.x; new = 0; vals = []
        for ci, D in enumerate(Ds):
            base = 3 * (D['n'] - 1) - 8; tot = 5.0
            for i, (t, p, q, P) in enumerate(D['parts']):
                w = {k: price(ci, x, t, k) for k in PEs[ci][i]}
                v, T = mst(P, D['U'], PEs[ci][i], w); tot += v
                if v < x[woff[ci] + i] - 1e-7: new += addcut(ci, i, T)
            vals.append(tot - base)
        if it % 10 == 0 or new == 0:
            print('  it %d cuts %d UB(z) %.5f  true min excess %.5f  per-cycle %s %.0fs' % (it, len(cuts), x[zi], min(vals), [round(v, 3) for v in vals], time.time() - t0), flush=True)
        if new == 0: break
    f = {allkeys[i]: x[i] for i in range(nf) if x[i] > 1e-7}
    fq = {kk: Fraction(v).limit_denominator(60) for kk, v in f.items()}
    exact = []
    for ci, D in enumerate(Ds):
        u = {(t, k): fq[KS[ci][(t, k)]] for (t, k) in KS[ci] if KS[ci][(t, k)] in fq}
        try: exact.append(str(verify(D, u) - (3 * (D['n'] - 1) - 8)))
        except AssertionError as er: exact.append('verify-failed')
    print('EXACT rational excess bound per cycle', exact)
    print('RESULT r=%d mode=%s keys=%d min excess bound %.5f per-cycle %s' % (r, mode, nf, min(vals), [round(v, 4) for v in vals]))
    for kk, v in sorted(f.items(), key=lambda z: -z[1])[:40]: print('   f%s = %.4f' % (kk, v))
    if out: json.dump(dict(r=r, mode=mode, files=files, vals=vals, f=[[list(k), v] for k, v in f.items()]), open(out, 'w'))


if __name__ == '__main__':
    main()
