#!/usr/bin/env python3
"""Track H: push a general-graph LPC counterexample towards the counting identities of closed triangulated surfaces
WITHOUT changing its Kempe class.
Moves that provably keep the class (and every component through the link, hence D, the locks and pi):
  add    u-v (non-edge, not at h, not a link chord) when at EVERY class state c(u) != c(v) and u, v lie in the same
         component of their pair graph (a 'neutral' edge: it only removes colourings outside the class);
  remove u-v (not at h, not a link edge) when at every class state u-v is not a bridge of its pair graph (components
         unchanged; new colourings with c(u) = c(v) cannot be reached from the class, since every swap of a class
         state is computed on unchanged components and is a proper colouring of the old graph).
Objective: per class state, the edge balance of Lemma H3 (E1 = E2 + 1 = E3 + 1 over the partitions) plus, with --P, the
parity identities P1-P3 (odd-G-degree counts of K_aA, K_aB, K_am at x_{j+2}).
usage: th_balance.py FILE NAME OUT [--P] [--seed S] [--iters K]"""
import sys, random
from th_engine import read_graphs, Hole

def main():
    f, name, out = sys.argv[1], sys.argv[2], sys.argv[3]
    useP = '--P' in sys.argv
    seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 1
    iters = int(sys.argv[sys.argv.index('--iters') + 1]) if '--iters' in sys.argv else 20000
    rng = random.Random(seed)
    g = read_graphs(f)[name]; n = len(g); H = Hole(g, 0).build()
    cyc = H.allDL_cycles()[0]; mem = H.class_members(cyc[0])
    assert all(H.info[i]['kind'] == 'DL' for i in mem)
    cols = [H.col(i) for i in mem]; roles = [H.info[i]['roles'] for i in mem]; js = [H.info[i]['j'] for i in mem]
    link = g[0]; L = set(link)
    adj = {v: set(g[v]) - {0} for v in range(1, n)}
    def part(c, r, u, v):
        al, mu, A, B = r; p = frozenset((c[u], c[v]))
        return 0 if p in (frozenset((al, mu)), frozenset((A, B))) else (1 if p in (frozenset((al, A)), frozenset((mu, B))) else 2)
    def comp(c, s, pair, skip=None):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if skip and {u, w} == skip: continue
                if w not in seen and c[w] in pair: seen.add(w); st.append(w)
        return seen
    def cost():
        tot = 0
        for c, r, j in zip(cols, roles, js):
            E = [0, 0, 0]
            for u in adj:
                for w in adj[u]:
                    if w > u: E[part(c, r, u, w)] += 1
            tot += abs(E[0] - E[1] - 1) + abs(E[1] - E[2])
            if useP:
                al, mu, A, B = r; x = [link[(j + t) % 5] for t in range(5)]
                deg = {v: len(adj[v]) + (1 if v in L else 0) for v in adj}
                for pr in ((al, A), (al, B), (al, mu)):
                    K = comp(c, x[2], pr); odd = sum(1 for v in K if deg[v] % 2) % 2
                    want = 1 if pr == (al, mu) else (0 if x[0] in K else 1)
                    tot += odd != want
        return tot
    def neutral(u, v):
        for c in cols:
            if c[u] == c[v]: return False
            if v not in comp(c, u, (c[u], c[v])): return False
        return True
    def removable(u, v):
        if u in L and v in L: return False
        for c in cols:
            if v not in comp(c, u, (c[u], c[v]), skip={u, v}): return False
        return True
    cur = cost(); best = cur; print('start cost', cur, 'edges', sum(len(a) for a in adj.values()) // 2, flush=True)
    T = 2.0
    for it in range(iters):
        u, v = rng.sample(range(1, n), 2)
        if u in L and v in L: continue
        if v in adj[u]:
            if not removable(u, v): continue
            adj[u].discard(v); adj[v].discard(u); c2 = cost()
            if c2 <= cur or rng.random() < pow(2.718, (cur - c2) / T): cur = c2
            else: adj[u].add(v); adj[v].add(u)
        else:
            if not neutral(u, v): continue
            adj[u].add(v); adj[v].add(u); c2 = cost()
            if c2 <= cur or rng.random() < pow(2.718, (cur - c2) / T): cur = c2
            else: adj[u].discard(v); adj[v].discard(u)
        T = max(0.05, T * 0.9995)
        if cur < best:
            best = cur; print('it', it, 'cost', cur, 'edges', sum(len(a) for a in adj.values()) // 2, flush=True)
        if cur == 0: break
    rot = [list(link)] + [sorted(adj[v] | ({0} if v in L else set())) for v in range(1, n)]
    with open(out, 'w') as fo: fo.write(f"{name}_bal {n} " + ';'.join(','.join(map(str, r)) for r in rot) + '\n')
    print('final cost', cur)

if __name__ == '__main__':
    main()
