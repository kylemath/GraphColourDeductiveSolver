#!/usr/bin/env python3
"""Track L [data]: search for a monotone quantity along near-rigid two-steps.
A Phi-step is u -> c' = pi(u) -> u'' = pi(c') with u, u'' rigid and c' in-shape (all DL).  For each candidate
feature f of rigid states, tally sign(f(u'') - f(u)) over all Phi-steps found; a potential would show one sign only.
Also the in-shape analogue (c -> u -> c'' with c, c'' in-shape).
Features (rigid u, Tait frame of u): |X|, |Y| (F13 loops), |Xt|, |Yt| (F12 loops), position of the far ends of
e0/e1/e3 along H_u, l1, l2 (lock paths), |K|, |Kt|, colour-class sizes in role order, #inside chords.
usage: tl_phi.py GRAPHFILE STRIDE OFFSET MAXGRAPHS"""
import sys
from collections import Counter, deque
from tl_lib import HoleData, TaitState, read_graphs


def dist(hd, col, s, t, pair):
    prev = {s: None}; dq = deque([s])
    while dq:
        u = dq.popleft()
        for w in hd.Hh.adj[u]:
            if w not in prev and col[w] in pair: prev[w] = u; dq.append(w)
    k = 0; x = t
    while prev[x] is not None: x = prev[x]; k += 1
    return k


def feats(hd, i, rigid=True):
    r = hd.info[i]; col = hd.col[i]; x = r['x']; al, mu, A, B = r['roles']; Hh = hd.Hh
    ts = TaitState(hd, i)
    f = {}
    f['X'] = len(ts.X); f['Y'] = len(ts.Y); f['Xt'] = len(ts.Xt); f['Yt'] = len(ts.Yt)
    f['l1'] = dist(hd, col, x[1], x[3], (mu, A)); f['l2'] = dist(hd, col, x[1], x[4], (mu, B))
    f['K'] = len(Hh.comp(col, x[2], (al, A))); f['Kt'] = len(Hh.comp(col, x[0], (al, B)))
    for nm, cc in (('a', al), ('m', mu), ('A', A), ('B', B)):
        f['n' + nm] = sum(1 for v in Hh.V if col[v] == cc)
    if rigid:
        # position along H (from v via e2) of the far ends of e0, e1, e3
        T = ts.T
        path, _ = T.trail(ts.H, T.lab['e2'])
        pos = {}; xv = 0
        for k, q in enumerate(path):
            xv = T.other(q, xv); pos[xv] = k + 1
        for l in ('e0', 'e1', 'e3'):
            q = T.lab[l]; w = T.other(q, 0); f['p' + l] = pos.get(w, -1)
        f['H'] = len(path)
        f['d30'] = f['pe3'] - f['pe0']; f['d31'] = f['pe3'] - f['pe1']; f['d10'] = f['pe1'] - f['pe0']
        f['out'] = f['H'] - f['pe0'] + f['pe1']   # H-edges outside the (e0,e1) lens, i.e. not between the ends of e0, e1
    return f


def main():
    gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    T = Counter(); TI = Counter(); nphi = 0; nins = 0
    for name, rot in read_graphs(gf, stride, off, maxg):
        for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
            hd = HoleData(rot, h)
            for u in range(hd.S):
                if not hd.rigid(u): continue
                c = hd.info[u]['pi']
                if c is None or not hd.inshape(c): continue
                u2 = hd.info[c]['pi']
                if u2 is None or not hd.rigid(u2): continue
                nphi += 1
                f0 = feats(hd, u); f2 = feats(hd, u2)
                for k in f0:
                    d = f2[k] - f0[k]; T[(k, '+' if d > 0 else ('-' if d < 0 else '0'))] += 1
            for c in range(hd.S):
                if not hd.inshape(c): continue
                u = hd.info[c]['pi']; c2 = hd.info[u]['pi']
                if c2 is None or not hd.inshape(c2): continue
                nins += 1
                f0 = feats(hd, c, False); f2 = feats(hd, c2, False)
                for k in f0:
                    d = f2[k] - f0[k]; TI[(k, '+' if d > 0 else ('-' if d < 0 else '0'))] += 1
    print(gf, 'phi-steps', nphi)
    keys = sorted({k for k, s in T})
    for k in keys: print('   %-4s +%d -%d =%d' % (k, T[(k, '+')], T[(k, '-')], T[(k, '0')]))
    print(gf, 'inshape two-steps', nins)
    keys = sorted({k for k, s in TI})
    for k in keys: print('   %-4s +%d -%d =%d' % (k, TI[(k, '+')], TI[(k, '-')], TI[(k, '0')]))


if __name__ == '__main__':
    main()
