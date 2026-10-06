#!/usr/bin/env python3
"""studiointel reducible_filters.py -- [exploratory] classical filters on hard graphs (imports no producer code):
 (a) Birkhoff diamond: adjacent degree-5 vertices a,b whose two common face-neighbours c,d also have degree 5;
 (b) separating 4-cycle: a 4-cycle whose removal disconnects T;
 (c) non-trivial separating 5-cycle: a 5-cycle whose removal leaves >= 2 components each with >= 2 vertices.
A minimal counterexample to 4CT contains none of these (Birkhoff 1913)."""
import sys, json, itertools
def load(p): return [tuple(f) for f in json.load(open(p))['faces']]
def analyse(F):
    adj = {}
    for f in F:
        for i in range(3): adj.setdefault(f[i], set()).add(f[(i + 1) % 3]); adj.setdefault(f[(i + 1) % 3], set()).add(f[i])
    deg = {u: len(a) for u, a in adj.items()}; V = sorted(adj)
    diamonds = []
    for a in V:
        for b in adj[a]:
            if b <= a or deg[a] != 5 or deg[b] != 5: continue
            cd = [c for c in adj[a] & adj[b]]
            if len(cd) == 2 and all(deg[c] == 5 for c in cd): diamonds.append((a, b, *cd))
    def comps(removed):
        rest = [u for u in V if u not in removed]; seen = set(); out = []
        for s in rest:
            if s in seen: continue
            st = [s]; seen.add(s); n = 0
            while st:
                u = st.pop(); n += 1
                for w in adj[u]:
                    if w not in removed and w not in seen: seen.add(w); st.append(w)
            out.append(n)
        return out
    def cycles(k):
        seen = set()
        for s in V:
            def dfs(path):
                u = path[-1]
                if len(path) == k:
                    if s in adj[u]:
                        key = frozenset(path)
                        if key not in seen: seen.add(key); yield tuple(path)
                    return
                for w in adj[u]:
                    if w > s and w not in path: yield from dfs(path + [w])
            yield from dfs([s])
    sep4 = [c for c in cycles(4) if len(comps(set(c))) >= 2]
    sep5 = [c for c in cycles(5) if sum(1 for x in comps(set(c)) if x >= 2) >= 2]
    return {'n': len(V), 'diamonds': len(diamonds), 'sep4': len(sep4), 'sep5_nontrivial': len(sep5),
            'example': {'diamond': diamonds[:1], 'sep4': sep4[:1], 'sep5': sep5[:1]}}
if __name__ == '__main__':
    surv = 0
    for p in sys.argv[1:]:
        r = analyse(load(p)); ok = r['diamonds'] == 0 and r['sep4'] == 0 and r['sep5_nontrivial'] == 0; surv += ok
        print(p.split('/')[-1][:24], json.dumps(r), 'SURVIVES' if ok else 'excluded', flush=True)
    print('survive all three filters: %d of %d' % (surv, len(sys.argv) - 1))
