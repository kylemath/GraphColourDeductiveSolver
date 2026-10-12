#!/usr/bin/env python3
"""Track F: nanotube fullerene families from spirals. Belt = min vertex cut (dual) between the two caps' pentagon sets."""
import sys, itertools; sys.path.insert(0, 'src'); import spiral
import networkx as nx
def belt(rot, A, B):
    G = nx.Graph(); n = len(rot)
    for u in range(n):
        for v in rot[u]: G.add_edge(u, v)
    G.add_node('s'); G.add_node('t')
    for a in A:
        for w in list(G.neighbors(a)): G.add_edge('s', w)
        G.remove_node(a)
    for b in B:
        for w in list(G.neighbors(b)): G.add_edge('t', w)
        G.remove_node(b)
    if G.has_edge('s', 't'): return 0
    try: return len(nx.minimum_node_cut(G, 's', 't'))
    except Exception: return -1
def build(f, pents):
    r = spiral.from_pentagons(f, pents)
    return None if r is None else r[0]
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'search':   # find cap pairs whose last cap can be shifted by d repeatedly
        d = int(sys.argv[2]); F0 = int(sys.argv[3]); M = int(sys.argv[4]); res = {}
        for first in itertools.combinations(range(M), 6):
            if first[0] != 0: continue
            for f in range(F0, F0 + 2 * d):
                last = [f - 1 - p for p in reversed(first)]
                if last[0] <= first[-1] + 1: continue
                ok = True; rots = []
                for k in range(3):
                    rr = build(f + d * k, list(first) + [x + d * k for x in last])
                    if rr is None: ok = False; break
                    rots.append(rr)
                if not ok: continue
                deg = [len(x) for x in rots[-1]]; p5 = [v for v in range(len(deg)) if deg[v] == 5]
                b = belt(rots[-1], p5[:6], p5[6:]) if len(p5) == 12 else -1
                key = (b,); print('found', 'd', d, 'f', f, 'first', [x + 1 for x in first], 'last', [x + 1 for x in last], 'natoms', 2 * (f - 2), 'belt', b, flush=True)
                break

def search_ipr(d, F0, M, want_belt):
    for first in itertools.combinations(range(M), 6):
        if any(first[i+1]-first[i] == 1 for i in range(5)): continue
        for f in range(F0, F0 + 3 * d):
            last = [f - 1 - p for p in reversed(first)]
            if last[0] <= first[-1] + 1: continue
            rots = []
            for k in range(3):
                rr = build(f + d * k, list(first) + [x + d * k for x in last])
                if rr is None: break
                rots.append(rr)
            if len(rots) < 3: continue
            r = rots[0]; deg = [len(x) for x in r]; p5 = [v for v in range(len(deg)) if deg[v] == 5]
            if any(deg[w] == 5 for v in p5 for w in r[v]): continue
            b = belt(rots[-1], p5[:6], [x + d * 2 for x in p5[6:]]) if False else belt(rots[-1], [v for v in range(len(rots[-1])) if len(rots[-1][v]) == 5][:6], [v for v in range(len(rots[-1])) if len(rots[-1][v]) == 5][6:])
            if b != want_belt: continue
            print('IPR d', d, 'f', f, 'first', [x + 1 for x in first], 'last', [x + 1 for x in last], 'natoms', 2 * (f - 2), 'belt', b, flush=True)
            return
