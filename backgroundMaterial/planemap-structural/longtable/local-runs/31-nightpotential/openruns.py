"""[exploratory] NightPotential: all maximal DL runs (length >= 10) at (5,5,5,5,6) holes of gentri order N, both orientations.
Per run: positions, J, fixed (R3 k<=2), Rtot = sum over the six pairs of cycle ranks (= #Kempe components - 8), lock status of the
predecessor / leaving state.  Usage: python3 openruns.py N out.jsonl"""
import sys, json, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../30-nighta34'))
from eng import H as EH, graphs, holes6
from collections import Counter
NM = {(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
PAIRS = list(itertools.combinations(range(4), 2))
def ncomp(Hh, c, a, b):
    seen = set(); n = 0
    for v in range(Hh.N):
        if c[v] in (a, b) and v not in seen: seen |= Hh.comp(c, v, a, b); n += 1
    return n
def Rtot(Hh, c): return sum(ncomp(Hh, c, a, b) for a, b in PAIRS) - 8
def ranks(Hh, c):
    f = Hh.frame(c); j, ty, k, (al, mu, A, B) = f
    # role ranks via duality at DL states is not assumed: compute directly
    E = [(u, v) for u in range(Hh.N) for v in Hh.nb[u] if u < v]
    def rk(a, b): return sum(1 for u, v in E if c[u] in (a, b) and c[v] in (a, b)) - sum(1 for v in range(Hh.N) if c[v] in (a, b)) + ncomp(Hh, c, a, b)
    return dict(AB=rk(A, B), muA=rk(mu, A), muB=rk(mu, B), alMu=rk(al, mu), alA=rk(al, A), alB=rk(al, B))
def lockstat(Hh, c):
    if len(set(c[x] for x in Hh.X)) <= 3: return 'F'
    l = Hh.locks(c); return 'L%d%d' % (l[0], l[1])
if __name__ == '__main__':
    n = int(sys.argv[1]); out = open(sys.argv[2], 'w'); st = Counter()
    for gi, rot0 in graphs(n):
        for mirror in (0, 1):
            rot = [list(reversed(r)) for r in rot0] if mirror else rot0
            for h in holes6(rot):
                Hh = EH(rot, h); S = Hh.sp.states; idx = Hh.sp.index
                DL = [Hh.DL(c) for c in S]
                if not any(DL): continue
                nxt = {}
                for k, c in enumerate(S):
                    if DL[k]: nxt[k] = idx[Hh.canon(Hh.pi(c)[0])]
                hasDLpred = set(t for k, t in nxt.items())
                pred = {t: k for k, t in nxt.items()}
                for k0 in nxt:
                    if k0 in hasDLpred: continue
                    seq = []; kk = k0; c = S[k0]
                    while DL[kk] and len(seq) < 400:
                        seq.append(c); c = Hh.pi(c)[0]; kk = idx[Hh.canon(c)]
                    st['runs'] += 1
                    if len(seq) < 10: continue
                    P = []; Jv = []; Fx = []; Rt = []; RK = []
                    for x in seq:
                        f = Hh.frame(x); P.append(NM.get((f[1], f[2]))); Jv.append(Hh.J(x)); Rt.append(Rtot(Hh, x)); RK.append(ranks(Hh, x))
                        Fx.append(f[1] == 3 and f[2] <= 2 and len(Hh.comp(x, Hh.X[(f[0]+1) % 5], f[3][0], f[3][1])) == sum(1 for v in range(Hh.N) if x[v] in f[3][:2]))
                    # predecessor of run start (any move kind): search all states whose pi is k0 is expensive; record pi-inverse via DL-free scan skipped
                    rec = dict(n=n, g=gi, mir=mirror, h=h, L=len(seq), pos=P, J=Jv, fixed=Fx, Rtot=Rt, ranks=RK,
                               leave=lockstat(Hh, c), leaveRtot=Rtot(Hh, c), lastframe=Hh.frame(seq[-1])[:3])
                    out.write(json.dumps(rec) + '\n'); st['runs>=10'] += 1
        if gi % 2000 == 0: print(n, gi, dict(st), flush=True)
    print(n, 'done', dict(st), flush=True)
