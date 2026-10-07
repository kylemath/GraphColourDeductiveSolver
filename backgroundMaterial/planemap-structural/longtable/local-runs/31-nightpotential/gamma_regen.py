"""[exploratory] Regenerate the 54 distinct (5,5,5,5,6) Gamma-cycles of jobak-66dump.json (rotation + pos-4 colouring) by iterating pi,
and record per-state potentials.  Output gamma54.json.  One core."""
import json, sys, os, itertools
from peng import Hole, key, NM, canon
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../27-studio-positive-config/jobuv/')
L2I = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
PAIRS = list(itertools.combinations(range(4), 2))
def state_rec(H, c):
    j, ty, k, (al, mu, A, B) = H.frame(c); X = H.L
    l1, l2, K1, K2 = H.locks(c)
    Ks = H.Ksig(c); Kst = H.comp(c, X[(j+2) % 5], al, A)
    rk = {pr: H.rank(c, *pr) for pr in PAIRS}; nc = {pr: H.ncomp(c, *pr) for pr in PAIRS}
    role = lambda a, b: rk[tuple(sorted((a, b)))]
    esc = sum(1 for u in (H.y, H.z) for t in H.nb[u] if c[t] in (al, mu) and t not in Ks)
    escy = sum(1 for t in H.nb[H.y] if c[t] in (al, mu) and t not in Ks); escz = esc - escy
    nAM = sum(1 for v in H.V if c[v] in (al, mu)); 
    r = dict(pos=NM.get((ty, k)), ty=ty, k=k, j=j, L1=len(K1), L2=len(K2), AB=role(A, B), muA=role(mu, A), muB=role(mu, B),
             alMu=role(al, mu), alA=role(al, A), alB=role(al, B), Ntot=sum(nc.values()), Rtot=sum(rk.values()),
             Ksig=len(Ks), Kst=len(Kst), KstL1=len(Kst & K1), KstL2=len(Kst & K2), esc=esc, escy=escy, escz=escz,
             J=H.J(c), Kyz=len(H.comp(c, H.y, c[H.y], c[H.z])), fixed=(len(Ks) == nAM),
             ex=(H.lockless_exit(c) if ty == 3 else None),
             ncol=[sum(nc[pr] for pr in PAIRS if a in pr) for a in range(4)], rkabs=[rk[pr] for pr in PAIRS], ncabs=[nc[pr] for pr in PAIRS], linkabs=H.lc(c),
             Kst_has=''.join(n for n, v in (('p', H.p), ('m', H.m), ('y', H.y), ('z', H.z)) if v in Kst))
    return r
def trace_cycle(H, c0, cap=400):
    seq = [c0]; c = c0
    for _ in range(cap):
        c, kind, K, pr = H.pi(c)
        if canon(c) == canon(c0): return seq
        seq.append(c)
    return None
if __name__ == '__main__':
    dump = json.load(open(D + 'jobak-66dump.json')); done = set(); out = []
    for r in dump:
        cid = (r['run'], r['name'], r['hole'], r['cycle'])
        if cid in done: continue
        done.add(cid)
        H = Hole(r['rotation'], r['hole'])
        c0 = {int(v): L2I[x] for v, x in r['colourings']['4'].items()}
        seq = trace_cycle(H, c0)
        assert seq is not None, cid
        assert all(H.DL(c) for c in seq), cid
        # check dump positions 5..8
        for q in range(5, 9):
            assert canon(seq[q - 4]) == canon({int(v): L2I[x] for v, x in r['colourings'][str(q)].items()}), (cid, q)
        rows = [state_rec(H, c) for c in seq]
        s0 = next(i for i, x in enumerate(rows) if x['pos'] == 0); rows = rows[s0:] + rows[:s0]
        assert all(x['pos'] == i % 10 for i, x in enumerate(rows)), cid
        out.append(dict(id=cid, L=len(rows), rows=rows)); print(cid, len(rows), flush=True)
    json.dump(out, open('gamma54.json', 'w'))
