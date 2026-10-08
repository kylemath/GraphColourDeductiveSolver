#!/usr/bin/env python3
"""Track H: LPC on pseudo-surfaces built by pinching a surface test bed.
For a seed (graph, hole) with an all-DL pi-cycle: candidate pinch pairs (u, v) = non-adjacent vertices off N[h] with
disjoint neighbourhoods and c(u) = c(v) in every state of the cycle (so the cycle colourings survive the identification).
Each single pinch (and, with --pairs, each pair of compatible pinches) is evaluated by kclass4 at the hole; the pinched
complex keeps faces = triangles, each edge in exactly two faces, the star of h untouched, so (F1)-(F3) and Theorem P hold.
Logs every result with a cycle class: [size, filled, DL, nonDL, minK, maxK, LPviol, onCycles, pathEnds].
usage: th_pinch.py GRAPHFILE NAME HOLE OUT.jsonl [--pairs]"""
import sys, json, itertools
from th_engine import read_graphs, Hole
from th_gsearch import evaluate

def pinch(rot, h, pairs):
    n = len(rot); rep = {}
    for u, v in pairs: rep[v] = u
    keep = [x for x in range(n) if x not in rep]; mp = {x: i for i, x in enumerate(keep)}
    f = lambda x: mp[rep.get(x, x)]
    adj = [[] for _ in keep]
    for x in range(n):
        for y in rot[x]:
            a, b = f(x), f(y)
            if b not in adj[a]: adj[a].append(b)
    adj[f(h)] = [f(x) for x in rot[h]]
    return adj, len(keep), f(h)

def main():
    gf, name, hole, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    rot = read_graphs(gf)[name]; H = Hole(rot, hole).build()
    cycs = H.allDL_cycles(); n = len(rot)
    Nh = set(rot[hole]) | {hole}; S = [set(r) for r in rot]
    fo = open(out, 'a'); tmp = out + '.tmp'
    for ci, cyc in enumerate(cycs):
        cols = [H.col(i) for i in cyc]
        cand = [(u, v) for u in range(n) for v in range(u + 1, n) if u not in Nh and v not in Nh and v not in S[u]
                and not (S[u] & S[v]) and all(c[u] == c[v] for c in cols)]
        print(f'{name} h{hole} cycle {ci}: {len(cand)} single pinch candidates', flush=True)
        sets = [[p] for p in cand]
        if '--pairs' in sys.argv:
            for p, q in itertools.combinations(cand, 2):
                if len({p[0], p[1], q[0], q[1]}) == 4 and not ((S[p[0]] | S[p[1]]) & (S[q[0]] | S[q[1]])) \
                        and not ({p[0], p[1]} & (S[q[0]] | S[q[1]])):
                    sets.append([p, q])
        best = None
        for ps in sets:
            adj, n2, h2 = pinch(rot, hole, ps)
            r = evaluate(adj, n2, tmp, h2)
            if not r or not r.get('states'): continue
            cls = r['cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]']
            cc = [c for c in cls if c[7] > 0]
            if cc:
                b = min(cc, key=lambda c: (c[1], c[8], c[0]))
                rec = dict(seed=name, hole=hole, cycle=ci, pinches=ps, n=n2, h=h2, cyc=cc, pid_bad=r['pid_bad'], dual_bad=r['dual_bad'],
                           graph=f"{name}_P{'_'.join(f'{u}-{v}' for u, v in ps)} {n2} " + ';'.join(','.join(map(str, a)) for a in adj))
                fo.write(json.dumps(rec) + '\n'); fo.flush()
                if best is None or (b[1], b[8]) < (best[1], best[8]): best = b
        print(f'   evaluated {len(sets)} pinch sets; best cycle class {best}', flush=True)

if __name__ == '__main__':
    main()
