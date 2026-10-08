#!/usr/bin/env python3
"""Track H: anatomy of sigma (swap of K = K_{alpha mu}(x_{j+2})) along every all-DL pi-cycle of a hole.
usage: th_sigma.py GRAPHFILE NAME HOLE
Per cycle state: number of {a,m} and {A,B} components, triv (K = every a/m vertex, i.e. sigma = renaming),
|K|, the AB-component K' of x_{j+3} (size), the sigma-image locks (L1', L2'), inA', inB' at the image (D check),
and which link vertices / partition pieces the lock chains of the image use."""
import sys
from collections import Counter
from th_engine import read_graphs, Hole

def comps(H, col, pair):
    left = {v for v in H.V if col[v] in pair}; out = []
    while left:
        s = next(iter(left)); K = H.comp(col, s, pair); left -= K; out.append(K)
    return out

def main():
    gf, name, hole = sys.argv[1], sys.argv[2], int(sys.argv[3])
    H = Hole(read_graphs(gf)[name], hole).build(); info = H.info
    for ci, cyc in enumerate(H.allDL_cycles()):
        print(f'## {name} h{hole} cycle {ci} len {len(cyc)}')
        for t, i in enumerate(cyc):
            r = info[i]; col = H.col(i); j = r['j']; x = [H.X[(j + k) % 5] for k in range(5)]
            al, mu, A, B = r['roles']
            am = comps(H, col, (al, mu)); AB = comps(H, col, (A, B))
            K = H.comp(col, x[2], (al, mu)); Kp = H.comp(col, x[3], (A, B))
            triv = all(col[v] not in (al, mu) or v in K for v in H.V)
            s = info[r['sigma']]
            # which AB components touch K
            touchK = [L for L in AB if any(w in K for v in L for w in H.adj[v])]
            print(f"{t:2d} j={j} #am={len(am)} #AB={len(AB)} |K|={len(K)} triv={int(triv)} |K'|={len(Kp)} ABcompsTouchingK={len(touchK)} "
                  f"sigma->{s['kind']} L'={int(s.get('L1', 0))}{int(s.get('L2', 0))} in'={int(s.get('inA', 0))}{int(s.get('inB', 0))} D'ok={int(s.get('D1', 1) and s.get('D2', 1))}")

if __name__ == '__main__':
    main()
