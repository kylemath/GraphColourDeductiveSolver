"""[exploratory] NightA34Two: the two-run (exchange-pair) picture of an L = 20 Gamma-cycle at a (5,5,5,5,6) hole.
For each all-DL pi-cycle: anchor c = c_0 at an R3k4 state, run actual colourings; rho = colour permutation with
c_10 = rho c_0 on the 11 hole vertices; d = rho^{-1} c_10.  Checks: d = c on the hole; pi^10 d = rho c (exchange);
per step i: X_i = {v : c_i(v) != d_i(v)}, X_i cap hole, K_i^c vs K_i^d, J, breaks, pockets, |Pi(p)| at R3k4.
usage: pair.py orders [gentri-file-override]  -> prints summary, writes pair-<orders>.jsonl"""
import sys, json
from eng import *
from collections import Counter
NM = {(3, 4): 0, (1, 1): 1, (3, 3): 2, (1, 0): 3, (3, 2): 4, (1, 4): 5, (3, 1): 6, (1, 3): 7, (3, 0): 8, (1, 2): 9}
def pos(Hh, c):
    f = Hh.frame(c); return NM.get((f[1], f[2]))
def relabel(c, perm): return tuple(perm[x] for x in c)
def pocket(Hh, c):
    q = Hh.q; xp = Hh.X[(q + 1) % 5]; wp = Hh.W[(q + 1) % 5]; a, b = c[Hh.P], c[Hh.Mi]
    if c[xp] not in (a, b) or c[wp] not in (a, b): return None
    S = Hh.comp(c, wp, a, b, avoid=(Hh.P, xp))
    return S if Hh.Mi in S else set()
def run(Hh, c, n):
    seq = [c]; Ks = []
    for _ in range(n):
        c2, kind, K, pr = Hh.pi(seq[-1]); seq.append(c2); Ks.append((frozenset(K), tuple(sorted(pr)), kind))
    return seq, Ks
def graphs_file(fn):
    for i, l in enumerate(open(fn)):
        if l.startswith('G'): yield i, gentri_rotation(l)
if __name__ == '__main__':
    orders = [int(x) for x in sys.argv[1].split(',')]
    src = sys.argv[2] if len(sys.argv) > 2 else None
    out = open('pair-%s.jsonl' % sys.argv[1].replace(',', '_'), 'w'); st = Counter()
    for n in orders:
        it = graphs_file(src) if src else graphs(n)
        for gi, rot0 in it:
            for mirror in (0, 1):
                rot = [list(reversed(r)) for r in rot0] if mirror else rot0
                for h in holes6(rot):
                    Hh = H(rot, h); S = Hh.sp.states; idx = Hh.sp.index
                    DL = [Hh.DL(c) for c in S]
                    if not any(DL): continue
                    nxt = {}
                    for k, c in enumerate(S):
                        if DL[k]: nxt[k] = idx[Hh.canon(Hh.pi(c)[0])]
                    seen = set()
                    hole = set(Hh.X) | set(Hh.W) | {Hh.Mi}
                    for k0 in nxt:
                        if k0 in seen: continue
                        cyc = []; k = k0
                        while k in nxt and k not in seen and k not in cyc: cyc.append(k); k = nxt[k]
                        seen.update(cyc)
                        if k != k0 or not all(DL[x] for x in cyc): continue
                        L = len(cyc); st[('Gamma L', L)] += 1
                        a0 = next((x for x in cyc if pos(Hh, S[x]) == 0), None)
                        if a0 is None: st['no R3k4'] += 1; continue
                        c0 = S[a0]; seqc, Kc = run(Hh, c0, L)
                        if L != 20: continue
                        c10 = seqc[10]
                        rho = {}
                        for v in hole: rho.setdefault(c0[v], c10[v])
                        if len(rho) != 4: st['rho undetermined'] += 1; continue
                        assert all(rho[c0[v]] == c10[v] for v in hole)
                        rinv = {b: a for a, b in rho.items()}
                        d0 = relabel(c10, rinv)
                        seqd, Kd = run(Hh, d0, 10)
                        ok_exch = seqd[10] == relabel(c0, rho)
                        st[('exchange pi^10 d = rho c', ok_exch)] += 1
                        st[('c20 = rho^2 c', seqc[20] == relabel(c0, {a: rho[rho[a]] for a in rho}))] += 1
                        st[('L10 (c=d)', c0 == d0)] += 1
                        rec = dict(n=n, g=gi, mir=mirror, h=h, steps=[])
                        for i in range(10):
                            ci, di = seqc[i], seqd[i]
                            Xi = {v for v in range(len(ci)) if ci[v] != di[v]}
                            st[('hole-sync at pos %d' % i, not (Xi & hole))] += 1
                            Kci, Kdi = Kc[i][0], Kd[i][0]
                            st[('same pair+kind step %d' % i, Kc[i][1:] == Kd[i][1:])] += 1
                            st[('Kc==Kd step %d' % i, Kci == Kdi)] += 1
                            st[('Kc cap hole == Kd cap hole step %d' % i, (Kci & hole) == (Kdi & hole))] += 1
                            rec['steps'].append(dict(i=i, X=len(Xi), KcdDiff=len(Kci ^ Kdi), KcX=len(Kci & Xi), KdX=len(Kdi & Xi),
                                                     Jc=Hh.J(ci), Jd=Hh.J(di)))
                        Bc = Hh.J(seqc[8]) and not Hh.J(seqc[9]); Bd = Hh.J(seqd[8]) and not Hh.J(seqd[9])
                        st[('breaks (c,d)', Bc, Bd)] += 1
                        X9 = {v for v in range(len(c0)) if seqc[9][v] != seqd[9][v]}
                        for nm, s9, B in (('c', seqc[9], Bc), ('d', seqd[9], Bd)):
                            pk = pocket(Hh, s9)
                            if B: st[('pocket of breaking run meets X9', bool(pk & X9))] += 1
                        rec.update(Bc=Bc, Bd=Bd, X0=sorted(v for v in range(len(c0)) if c0[v] != d0[v]))
                        # Pi(p) at R3k4 of both runs
                        rec['Pi0'] = [len(Hh.comp(s, Hh.P, s[Hh.P], s[Hh.Mi])) for s in (c0, d0)]
                        out.write(json.dumps(rec) + '\n')
            print(n, gi, flush=True) if gi % 2000 == 0 else None
        print(n, dict(st), flush=True)
    for k in sorted(st, key=str): print(k, st[k])
