"""EXPLORATORY independent check (lead) of the D1-hand claims on the 8 SEP-bad states of 17:0, 17:1.
For each SEP-bad state: class sizes in T-x, component and cyclomatic numbers of the six pair
subgraphs of T-x, whether all six are forests, and the ring word."""
import itertools, json, subprocess, sys
from collections import Counter
P = sys.argv[1]
d = json.load(open('../wp20/regression-m5-17.json'))
lines = subprocess.run([P, '-m5', '17', '-a'], capture_output=True, text=True).stdout.splitlines()
for w in d['witnesses']['sep_bad']:
    gi, x, st = w['index'], w['x'], w['state']
    n = 17
    rot = [[ord(c) - 97 for c in r] for r in lines[gi].split()[1].split(',')]
    adj = [set(r) for r in rot]
    sizes = Counter(st[v] for v in range(n) if v != x)
    vec = {}; forests = True
    for p, q in itertools.combinations(range(4), 2):
        V = [v for v in range(n) if v != x and st[v] in (p, q)]
        E = sum(1 for v in V for u in adj[v] if u > v and u != x and st[u] in (p, q))
        seen = set(); comps = 0
        for s in V:
            if s in seen: continue
            comps += 1; stack = [s]; seen.add(s)
            while stack:
                u = stack.pop()
                for t in adj[u]:
                    if t != x and t not in seen and st[t] in (p, q): seen.add(t); stack.append(t)
        cyc = E - len(V) + comps
        vec[(p, q)] = (comps, cyc); forests &= (cyc == 0)
    ring = [st[v] for v in rot[x]]
    print(f"17:{gi} x={x} ring={ring} sizes={sorted(sizes.values())} comps/cyc per pair={[vec[k] for k in sorted(vec)]} all forests={forests} sum(V-E)={sum(c-y for c,y in vec.values())}")
