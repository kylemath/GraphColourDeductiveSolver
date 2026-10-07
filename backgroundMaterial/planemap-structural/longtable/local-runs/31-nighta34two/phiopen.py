"""[exploratory] NightA34Two §6: test of the one-period form 'B(u) => Phi(u_0) > Phi(u_10)' of the antisymmetry
principle on OPEN DL runs (gentri orders given), where u_0 is the R3k4 state 8 steps before a step-8 break and u_10 the
next R3k4 (the failing one).  Phi candidates at an R3k4 colouring s: Kpm = |K_{c(p),c(m)}(p)|, Jy = |K_J(y)|, Jz = |K_J(z)|.
A candidate with 0 exceptions would, on an L = 20 Gamma-cycle (u_20 = rho^2 u_0), forbid two breaks."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../30-nighta34'))
from eng import *
from collections import Counter
NM = {(3, 4): 0, (1, 1): 1, (3, 3): 2, (1, 0): 3, (3, 2): 4, (1, 4): 5, (3, 1): 6, (1, 3): 7, (3, 0): 8, (1, 2): 9}
def pos(Hh, c):
    f = Hh.frame(c); return NM.get((f[1], f[2])) if f else None
def feats(Hh, s):
    Kpm = len(Hh.comp(s, Hh.P, s[Hh.P], s[Hh.Mi])); Jy = len(Hh.comp(s, Hh.Y, s[Hh.Y], s[Hh.Z])); Jz = len(Hh.comp(s, Hh.Z, s[Hh.Y], s[Hh.Z]))
    return dict(Kpm=Kpm, Jy=Jy, Jz=Jz, KpmMinusJz=Kpm - Jz, KpmPlusJyMinusJz=Kpm + Jy - Jz)
st = Counter(); ex = []
for n in [int(x) for x in sys.argv[1].split(',')]:
    for gi, rot0 in graphs(n):
        for mirror in (0, 1):
            rot = [list(reversed(r)) for r in rot0] if mirror else rot0
            for h in holes6(rot):
                Hh = H(rot, h); S = Hh.sp.states; idx = Hh.sp.index
                DL = [Hh.DL(c) for c in S]
                if not any(DL): continue
                nxt = {k: idx[Hh.canon(Hh.pi(S[k])[0])] for k in range(len(S)) if DL[k]}
                prevDL = set(nxt.values())
                for k0 in nxt:
                    if k0 in prevDL: continue          # open runs only (start without DL predecessor)
                    seq = [S[k0]]; kk = k0
                    while DL[kk] and len(seq) < 400:
                        c2 = Hh.pi(seq[-1])[0]; kk = idx[Hh.canon(c2)]; seq.append(c2)
                    seq = seq[:-1] if not DL[kk] else seq
                    P = [pos(Hh, x) for x in seq]
                    for i in range(8, len(seq) - 2):
                        if P[i] == 8 and P[i - 8] == 0 and Hh.J(seq[i]) and not Hh.J(seq[i + 1]):
                            f0 = feats(Hh, seq[i - 8]); f1 = feats(Hh, seq[i + 2])
                            prevfail = not Hh.J(seq[i - 8])
                            st[('breaks tested', 'u0 fails' if prevfail else 'u0 ok')] += 1
                            for key in f0:
                                ok = f1[key] > f0[key]       # failing R3k4 has the larger value
                                st[(key, 'u0 fails' if prevfail else 'u0 ok', ok)] += 1
                                if not ok and len(ex) < 30: ex.append((n, gi, mirror, h, i, key, f0[key], f1[key], prevfail))
    print(n, flush=True)
for k in sorted(st, key=str): print(st[k], k)
for e in ex[:15]: print('ex', e)
