"""Q1: numerical check of the disc Stokes formula
   12*S_a + 4*sum_{ring v, c(v)=a} t(v) = 3*E + 12*Psi_a(word)     for each colour a,
S_a = sum of spins of interior vertices of colour a, t(v)=fan turn (f-b) of ring vertex v,
E = sum over triangles of orientation sign, 12*Psi_a = sum_{b!=a} sgn(a,b,c,d) delta(c->d)."""
import sys, csv, random, collections
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, '/mnt/project-files/multiscale/spin_windows')
from spinlib import *

def cap_disc(n, seed, z0):
    rng = np.random.default_rng(seed); p = rng.normal(size=(n, 3)); p /= np.linalg.norm(p, axis=1)[:, None]
    h = ConvexHull(p); T = [t for t in h.simplices.tolist() if all(p[x][2] > z0 for x in t)]
    ecount = collections.Counter()
    for a, b, c in T:
        for e in ((a, b), (b, c), (a, c)): ecount[tuple(sorted(e))] += 1
    bd = [e for e, k in ecount.items() if k == 1]
    V = set(x for t in T for x in t)
    if len(V) - len(ecount) + len(T) != 1: return None
    nb = collections.defaultdict(list)
    for a, b in bd: nb[a].append(b); nb[b].append(a)
    if any(len(v) != 2 for v in nb.values()): return None
    cyc = [bd[0][0]]; prev = None
    while True:
        x = cyc[-1]; nx_ = [y for y in nb[x] if y != prev][0]
        if nx_ == cyc[0]: break
        prev = x; cyc.append(nx_)
    if len(cyc) != len(nb): return None
    order = cyc + sorted(V - set(cyc)); idx = {v: i for i, v in enumerate(order)}
    adj = [set() for _ in order]
    for e in ecount:
        a, b = idx[e[0]], idx[e[1]]; adj[a].add(b); adj[b].add(a)
    return adj, len(cyc)

