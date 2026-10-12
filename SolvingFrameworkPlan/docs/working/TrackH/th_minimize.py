#!/usr/bin/env python3
"""Track H: greedily shrink a general-graph LPC counterexample (hole = vertex 0, link = adj[0] in order) while keeping
'some class has an all-DL pi-cycle, filled = 0, no pi-path ends' (and, with --lp, no lock-parity violations).
Tries deleting vertices (not h / link), then deleting edges (not at h, not link edges).
usage: th_minimize.py FILE NAME OUT [--lp]"""
import sys, random
from th_gsearch import evaluate

def good(adj, n, lp):
    r = evaluate(adj, n, '/tmp/th_min.tmp' if False else OUTTMP, 0)
    if not r or r.get('states', 0) == 0: return False
    cls = r['cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]']
    return any(c[7] > 0 and c[1] == 0 and c[8] == 0 and (c[6] == 0 or not lp) for c in cls)

def main():
    global OUTTMP
    f, name, out = sys.argv[1], sys.argv[2], sys.argv[3]; lp = '--lp' in sys.argv
    OUTTMP = out + '.tmp'
    for l in open(f):
        p = l.split()
        if p and p[0] == name: adj = [list(map(int, r.split(','))) for r in p[2].split(';')]
    n = len(adj); assert good(adj, n, lp)
    rng = random.Random(1)
    changed = True
    while changed:
        changed = False
        for v in rng.sample(range(6, n), n - 6):
            if v >= n: continue
            keep = [u for u in range(n) if u != v]; mp = {u: i for i, u in enumerate(keep)}
            adj2 = [[mp[w] for w in adj[u] if w != v] for u in keep]
            if good(adj2, n - 1, lp):
                adj, n, changed = adj2, n - 1, True
        E = [(u, w) for u in range(1, n) for w in adj[u] if w > u and not (u <= 5 and w <= 5)]
        rng.shuffle(E)
        for (u, w) in E:
            adj2 = [list(a) for a in adj]; adj2[u].remove(w); adj2[w].remove(u)
            if good(adj2, n, lp):
                adj, changed = adj2, True
    with open(out, 'w') as fo:
        fo.write(f"{name}_min {n} " + ';'.join(','.join(map(str, a)) for a in adj) + '\n')
    print('n', n, 'edges', sum(len(a) for a in adj) // 2)

if __name__ == '__main__':
    main()
