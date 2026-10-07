#!/usr/bin/env python3
"""Independent Python check of the B' slack (NightBudget §1): sigma u sigma' groups from DD endpoints; N0 = unfilled with filled pi-neighbours on both sides;
E2 = start of an unfilled run of length exactly 2; tau = filled with filled successor; DD = DL with DL successor; R_rho = {rho(d)} (d if Studio-R3, else pi d if R3, else d);
slack = 2 N0 + E2 + 3 tau - 2 |R|; identity sum lambda = |DD| - 2 N0 - E2 - 3 tau."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobuv', '../jobas'): sys.path.insert(0, os.path.join(HERE, d))
from uv_lib import Hole
from flipsearch import rotation
def check(faces, hole, mirror):
    H = Hole('g', hole, mirror, rot=rotation([tuple(t) for t in faces])); S = H.S; pi = H.pi; pinv = H.pinv; DL = H.DL
    fil = [H.filled(k) for k in range(S)]; lm = 0
    for i in H.sp.linki: lm |= 1 << i
    n = len(H.cycles); up = list(range(n))
    def f(u):
        while up[u] != u: up[u] = up[up[u]]; u = up[u]
        return u
    for k in range(S):
        if not (DL[k] and (DL[pi[k]] or DL[pinv[k]])): continue
        s = H.sigma(k); up[f(H.cyc[k])] = f(H.cyc[s])
        for t, p, q, K in H.sp.moves(k):
            if t == k or K & lm or DL[t]: continue
            up[f(H.cyc[k])] = f(H.cyc[t])
    R3 = lambda k: H.frame(k)[1] == 3
    G = {}
    Rset = set()
    for k in range(S):
        g = G.setdefault(f(H.cyc[k]), dict(N0=0, E2=0, tau=0, DD=0, R=0, lam=0, pos=0)); g['lam'] += H.lam[k]
        if not fil[k] and fil[pi[k]] and fil[pinv[k]]: g['N0'] += 1
        if not fil[k] and fil[pinv[k]] and not fil[pi[k]] and fil[pi[pi[k]]]: g['E2'] += 1
        if fil[k] and fil[pi[k]]: g['tau'] += 1
        if DL[k] and DL[pi[k]]:
            g['DD'] += 1; Rset.add(k if R3(k) else (pi[k] if R3(pi[k]) else k))
    for r in Rset: G[f(H.cyc[r])]['R'] += 1
    for c in range(n):
        if H.W[c] > 0: G[f(c)]['pos'] = 1
    out = []
    for g in G.values():
        sl = 2 * g['N0'] + g['E2'] + 3 * g['tau'] - 2 * g['R']; idok = g['lam'] == g['DD'] - 2 * g['N0'] - g['E2'] - 3 * g['tau']
        out.append(dict(slack=sl, identity=idok, **g))
    return out
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); out = check(d['faces'], int(sys.argv[2]), sys.argv[3] == 'mirror')
    neg = sorted([g for g in out if g['slack'] < 0], key=lambda g: g['slack'])
    print('groups', len(out), 'identity fails', sum(not g['identity'] for g in out), 'negative slack groups', len(neg), 'min slack', min(g['slack'] for g in out))
    for g in neg: print('   ', g)
