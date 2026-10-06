"""nprove_skeleton.py: print the H-skeleton (triangles, regions, shared vertices, H-edges outside triangles, ring positions)
for c' or c'' of one disc line.  usage: file index c'|c''"""
import sys
from itertools import combinations
from nprove_lib import *
exec(open('nprove_regions.py').read().split("for i, line")[0].split("fn = sys.argv[1]")[1])
fn, which, nm = sys.argv[1], int(sys.argv[2]), sys.argv[3]
line = [l for l in open(fn) if 'DISC' in l][which]
col, E = parse(line); x, adj = build(col, E)
cp, cpp, K2, K0 = neighbours_cprime(adj, x, col + [0])
c0, apex = (cp, 0) if nm == "c'" else (cpp, 2)
Dset = [v for v in range(x) if c0[v] == c0[apex]]
R, loose = regions(adj, x, Dset); rem = set(Dset) | {x}
print("D' vertices", Dset, "degrees", [len(adj[v]) for v in Dset], "x-ring", list(range(5)))
print("colours of c0 (D,al,be,ga)=(0..3):", c0[:x])
tris = [t for t in combinations(range(len(adj)), 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]] and not (set(t) & rem)]
print("H triangles", tris)
print("regions", [sorted(r) for r in R])
Hv = [v for v in range(x) if v not in Dset]
He = [(u, w) for u in Hv for w in adj[u] if w in Hv and u < w]
intri = {e for t in tris for e in combinations(t, 2)}
print("H vertices", len(Hv), "H edges", len(He), "edges outside H-triangles:", [e for e in He if e not in intri])
mult = {v: sum(1 for r in R if v in r) for v in Hv}
print("vertices in >=2 regions:", {v: m for v, m in mult.items() if m > 1}, "ring positions u1..u4 =1..4; D' ring vertex u0 =0")
