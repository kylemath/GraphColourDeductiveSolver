# W2 check: for every node of a hierarchy/weak run (children at each merge + the merged U), the monodromy norm |t_Q| of
# every connected sub-union Q of pockets (all subtrees when <= 12 pockets, else all subtrees of size <= 4 plus the whole).
# W2(b) holds iff max |t_Q| <= 2 over even sub-unions.  Usage: python w2check.py name seed L [vor]
import sys, os, json, time, collections, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy/weak'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof'); sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof/witness')
import wk
from wk import Disc, tau_walk
from mp import tvec
from w2 import tau_star, tau_strip
from e1_hier import make

def pocket_tris(D):
    g = D.g; ch = set(D.chords); par = {i: i for i in D.tris}
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i in D.tris:
        f = g.faces[i]
        for j in range(3):
            u, w = f[j], f[(j+1) % 3]; o = g.face[(w, u)]
            if o in D.tris and (min(u, w), max(u, w)) not in ch: par[find(i)] = find(o)
    comp = collections.defaultdict(set)
    for i in D.tris: comp[find(i)].add(i)
    P = list(comp.values()); idx = {}
    for a, T in enumerate(P):
        for i in T: idx[i] = a
    adj = collections.defaultdict(set)
    for (u, w) in D.chords:
        a, b = idx[g.face[(u, w)]], idx[g.face[(w, u)]]; adj[a].add(b); adj[b].add(a)
    return P, adj

def subtrees(k, adj, maxsize=None):
    """connected vertex subsets of a tree on 0..k-1 (all, or of size <= maxsize)."""
    out = set()
    def grow(S, frontier):
        out.add(S)
        if maxsize and len(S) >= maxsize: return
        for v in sorted(frontier):
            if v < min(S) and False: pass
            S2 = S | {v}
            if S2 in out: continue
            grow(frozenset(S2), (frontier | adj[v]) - S2)
    for r in range(k): grow(frozenset([r]), set(adj[r]))
    return out

def w2stats(D, col):
    P, adj = pocket_tris(D); k = len(P)
    subs = subtrees(k, adj) if k <= 12 else subtrees(k, adj, 4) | {frozenset(range(k))}
    mx = 0.0; nE = 0; bad = 0; mxtau = 0.0
    for S in subs:
        if len(S) == 1: continue
        T = set().union(*[P[a] for a in S]); W = D.walk_of(T)
        if W['odd']: continue
        nE += 1; t = tvec(W, col)
        if t is None: continue
        mx = max(mx, t); bad += t > 2+1e-9
    return dict(pockets=k, subunions=len(subs), even_subunions=nE, max_tQ=round(mx, 3), bad_subunions=bad,
                max_pocket_tau_star=round(max(tau_star(W, col) for W in D.pockets), 3), max_pocket_tau_strip=round(max(tau_strip(W, col) for W in D.pockets), 3), max_pocket_tau=round(max(tau_walk(W, col) for W in D.pockets), 3), tU=tvec(D.whole, col))

orig = wk.do_merge
def do_merge(g, D, A, B, col, *a, **kw):
    sa = w2stats(Disc(g, A), col); sb = w2stats(Disc(g, B), col)
    rec = orig(g, D, A, B, col, *a, **kw)
    rec['w2_A'] = sa; rec['w2_B'] = sb; rec['w2_U'] = w2stats(D, col)
    return rec
wk.do_merge = do_merge

if __name__ == '__main__':
    name, seed, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    log = open('/mnt/project-files/multiscale/merge_proof/witness/w2check_%s_s%d_L%d.jsonl' % (name, seed, L), 'w')
    res = wk.run(name, make(name), seed=seed, L=L, log=log)
    recs = res.pop('recs'); res.pop('leaves')
    allst = [r[k] for r in recs for k in ('w2_A', 'w2_B', 'w2_U')]
    summ = dict(name=name, seed=seed, L=L, merges=len(recs), nodes_checked=len(allst), bad_nodes=sum(1 for s in allst if s['bad_subunions']),
                max_tQ=max(s['max_tQ'] for s in allst), max_pockets=max(s['pockets'] for s in allst),
                tQ_hist=dict(collections.Counter(s['max_tQ'] for s in allst)), tau_strip_hist=dict(collections.Counter(s['max_pocket_tau_strip'] for s in allst)), tau_hist=dict(collections.Counter(s['max_pocket_tau'] for s in allst)), R_final=res.get('R_final'), sec=res.get('sec'))
    print(json.dumps(summ)); open('/mnt/project-files/multiscale/merge_proof/witness/w2check_summary.jsonl', 'a').write(json.dumps(summ)+'\n')
