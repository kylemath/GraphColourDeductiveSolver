"""[exploratory] Line B: two-hole game at a Wernicke edge uv (deg u = 5, deg v in {5,6}); exact on T4, order14, A_3.
State: canonical 4-colouring of G-{u,v}. Moves: Kempe swap (whole component of G-{u,v}), cost 1.
Fill: colour u (or v) with any free colour (neighbours other than the other hole), cost 0, leaving a one-hole
state whose exact pure radius R is then paid. d2(S) = least total swaps to a full colouring.
Also: for every one-hole state at u (v coloured), D2 = d2(uncolour v) <= R (refilling v with its colour is an option)."""
import time
from collections import Counter, defaultdict
from pb2_lib import *
t0 = time.process_time()

def run(name, adj):
    deg = {u: len(adj[u]) for u in adj}
    Rt = {};
    for h in adj: Rt[h] = radius_table(adj, h)[0]
    edges = [(u, v) for u in adj for v in adj[u] if deg[u] == 5 and deg[v] in (5, 6) and (deg[v] == 6 or u < v)]
    print(f"== {name}: Wernicke edges 5-5: {sum(deg[v]==5 for u,v in edges)}, 5-6: {sum(deg[v]==6 for u,v in edges)}")
    agg = defaultdict(Counter); cmp = defaultdict(Counter); firstfill = defaultdict(Counter)
    best = {}  # (hole h, one-hole state key) -> least d2 over Wernicke partners o
    D2 = {}
    for u, v in edges:
        H = {u, v}; cols = colourings_H(adj, H); idx = {key(c): c for c in cols}
        nb = {k: [key(canon(swap(c, a, b, K))) for a, b, K in comps_H(adj, c, H)] for k, c in idx.items()}
        def fillcost(c):
            best = None; who = None
            for h, o in ((u, v), (v, u)):
                for col in free(adj, c, h):
                    n = dict(c); n[h] = col; r = Rt[o][key(canon(n))]
                    if best is None or r < best: best, who = r, h
            return best, who
        fc = {k: fillcost(c) for k, c in idx.items()}
        d2 = {k: (fc[k][0] if fc[k][0] is not None else 99) for k in idx}
        changed = True
        while changed:
            changed = False
            for k in idx:
                m = min(d2[n] for n in nb[k]) + 1 if nb[k] else 99
                if m < d2[k]: d2[k] = m; changed = True
        typ = f"5-{deg[v]}"
        agg[typ].update(d2.values())
        for k in idx:
            if fc[k][0] is not None and fc[k][0] == d2[k]:
                firstfill[typ]['u(deg5) first' if fc[k][1] == u else f'v(deg{deg[v]}) first'] += 1
            elif fc[k][0] is None: firstfill[typ]['neither fillable at start'] += 1
            else: firstfill[typ]['swap before fill'] += 1
        # compare with one-hole states at u and at v
        for h, o in ((u, v), (v, u)):
            for k, r in Rt[h].items():
                c = dict(k); c.pop(o); D = d2[key(canon(c))]
                cmp[(typ, f"hole deg{deg[h]}")][(r, D)] += 1
                if deg[h] == 5: best[(h, k)] = min(best.get((h, k), 99), D)
    for typ in sorted(agg):
        print(f"  {typ}: two-hole distance hist over all (edge,state): {dict(sorted(agg[typ].items()))}; best-first-fill: {dict(firstfill[typ])}")
    pb = Counter((Rt[h][k], d) for (h, k), d in best.items())
    print(f"  deg-5 one-hole states: (R, least d2 over the hole's Wernicke partners) -> count: {dict(sorted(pb.items()))}")
    for t in sorted(cmp):
        print(f"  {t}: (one-hole radius R, two-hole d2 after uncolouring the other end) -> count: {dict(sorted(cmp[t].items()))}")

for name, adj in graphs(): run(name, adj)
print("cpu", round(time.process_time() - t0, 1))
