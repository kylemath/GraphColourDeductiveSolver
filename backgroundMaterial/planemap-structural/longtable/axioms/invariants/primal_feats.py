"""Primal (Kempe-chain) features along the real sphere NR runs (coordinator priority 3).
For each state of each run (tm_lib Hole, roles alpha, mu, A, B at x_j..x_{j+4} = (alpha, mu, alpha, A, B)):
  class sizes n_alpha, n_mu, n_A, n_B (vertices of T - h);
  chain counts per pair graph (am, aA, aB, mA, mB, AB) and sizes of the link chains;
  the swap chain K = K_{alpha A}(x_{j+2}) of pi: |K|, |K cap alpha|, |K cap A|;
  lock data L1, L2, lockSize, lockLen (tm_lib).
Identities checked against the matching-form features: |K| = aX, |K_{aA}(x_j)| = aY, |K_{mB}| = aO,
n_alpha + n_mu = hA (side of H_t), n_A + n_B = hB.
Usage: primal_feats.py GRAPHS HOLESPEC minlen out.jsonl"""
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/TrackM'))
from tm_lib import Hole

graphs = {}
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) >= 3: graphs[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
specs = [l.split()[0] for l in open(sys.argv[2]) if l.strip()]
minlen = int(sys.argv[3]); out = open(sys.argv[4], 'w')
pc = lambda m: bin(m).count('1')
for spec in specs:
    name, h = spec.rsplit(':', 1); h = int(h)
    Hl = Hole(graphs[name], h); sp = Hl.sp; li = sp.linki
    dl = {x for x in range(Hl.S) if not Hl.filled[x] and Hl.phi[x] == 2}
    nr = {x for x in dl if Hl.Nch[x] <= 9}
    for x in sorted(nr):
        p = Hl.pinv[x]
        if p is not None and p in nr and Hl.pi[p] == x: continue
        r = [x]; y = Hl.pi[x]
        while y is not None and y in nr and y not in r: r.append(y); y = Hl.pi[y]
        if len(r) < minlen: continue
        rows = []
        for k in r:
            s = sp.states[k]; cm = sp.cmasks(s); j = Hl.j[k]
            xs = [li[(j + t) % 5] for t in range(5)]
            c = [s[q] for q in xs]
            al, mu, A, B = c[0], c[1], c[3], c[4]
            role = {'a': al, 'm': mu, 'A': A, 'B': B}
            nc = {r_: pc(cm[col]) for r_, col in role.items()}
            chains = {}
            for p_, q_ in (('a', 'm'), ('a', 'A'), ('a', 'B'), ('m', 'A'), ('m', 'B'), ('A', 'B')):
                chains[p_ + q_] = len(sp.components(s, role[p_], role[q_], cm))
            fl = lambda v, a, b: sp.flood(1 << v, cm[a] | cm[b])
            K = fl(xs[2], al, A); K0 = fl(xs[0], al, A); KmB = fl(xs[1], mu, B)
            Kam = fl(xs[0], al, mu); KAB = fl(xs[3], A, B)
            rows.append(dict(state=k, j=j, Nch=Hl.Nch[k], n=nc, chains=chains,
                             K=pc(K), K_a=pc(K & cm[al]), K_A=pc(K & cm[A]), K0=pc(K0), K0_eq_K=int(K0 == K),
                             KmB=pc(KmB), Kam=pc(Kam), KAB=pc(KAB),
                             L1=Hl.L1[k], L2=Hl.L2[k], lsize=Hl.lsize[k], llen=Hl.llen[k], ell=Hl.ell[k]))
        out.write(json.dumps(dict(name=name, hole=h, R=len(r), rows=rows)) + '\n'); out.flush()
