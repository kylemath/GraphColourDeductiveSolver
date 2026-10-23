# Non-vacuity of the vortex-restricted invariant along actual induction runs.  Every 25 steps (L >= 12), with the
# boundary's real gauge signs s and the current persistent positions held fixed (no new cuts):
#   glob : random proper 4-colourings of the boundary cycle  -> fraction accepted
#   arc  : the real colouring with a random contiguous arc of 8 boundary vertices recoloured at random (proper on the
#          cycle)                                              -> fraction accepted
# compared with the same number of cuts placed anywhere (J = npos) and with uncapped cuts anywhere.
import sys, json, random, time
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/unbounded/')
import vr, mc
from pi import make, rotation, canonical, signs
def acc(H, odd, var, al, J):
    vr.FrontierVR.NB = 0 if al is not None else vr.BIG
    return mc.ncuts(H, odd, J, var, 1.0, al) is not None
def rand_cycle(L, rng, base=None, arc=None):
    """sequential sampling: each recoloured vertex differs from its predecessor; the last one also from its successor."""
    c = list(base) if base else [rng.randrange(4)] + [None]*(L-1)
    idx = list(range(1, L)) if arc is None else arc
    for t, i in enumerate(idx):
        bad = {c[(i-1) % L]}
        if t == len(idx) - 1: bad.add(c[(i+1) % L])
        c[i] = rng.choice([x for x in range(4) if x not in bad])
    assert all(c[i] != c[(i+1) % L] for i in range(L))
    return c
def run(spec, nsamp=60):
    name, oseed, pol, var = spec.split(':'); oseed = int(oseed)
    adj = make(name); rot, emb = rotation(adj); rng = random.Random(oseed)
    u = rng.randrange(len(adj)); w = rot[u][rng.randrange(len(rot[u]))]; f = tuple(emb.traverse_face(u, w))
    order, paths = canonical(adj, rot, f, pol, rng=rng)
    I = vr.VRInductor(adj, order, paths, Rmax=4, policy='keep', seed=oseed); I.node_cap = 400000; I.variant = var; I.init_vr()
    R = random.Random(11); tot = dict(n=0, glob_pos=0, glob_J=0, glob_inf=0, arc_pos=0, arc_J=0, arc_inf=0, real_ok=0)
    for k in range(3, len(order)):
        if I.step(k) is None: break
        B = I.B; L = len(B)
        if k % 25 or L < 12: continue
        s, odd = signs(B, I.degp); s = [int(x) for x in s]; pos = {b: i for i, b in enumerate(B)}
        al = [0]*L
        for (a, b) in I.posn:
            if a in pos and b in pos and pos[b] == (pos[a]+1) % L: al[pos[a]] = 1
        J = sum(al); real = [I.col[b] for b in B]
        def H_of(c): return mc.int_walk([c[i] ^ c[(i+1) % L] for i in range(L)], s)
        tot['real_ok'] += acc(H_of(real), odd, var, al, vr.BIG)
        for t in range(nsamp):
            c = rand_cycle(L, R); H = H_of(c); tot['n'] += 1
            tot['glob_pos'] += acc(H, odd, var, al, vr.BIG); tot['glob_J'] += acc(H, odd, var, None, J); tot['glob_inf'] += acc(H, odd, var, None, vr.BIG)
            i0 = R.randrange(L); arc = [(i0 + j) % L for j in range(min(8, L - 2))]
            c = rand_cycle(L, R, real, arc); H = H_of(c)
            tot['arc_pos'] += acc(H, odd, var, al, vr.BIG); tot['arc_J'] += acc(H, odd, var, None, J); tot['arc_inf'] += acc(H, odd, var, None, vr.BIG)
    tot['probes'] = tot['n'] // nsamp; tot['spec'] = spec; tot['last_n'] = len(I.recs) + 3
    return tot
if __name__ == '__main__':
    from multiprocessing import Pool
    with Pool(4) as P, open(sys.argv[1], 'a') as fo:
        for r in P.imap_unordered(run, sys.argv[2:]):
            fo.write(json.dumps(r) + '\n'); fo.flush(); print(r, flush=True)
