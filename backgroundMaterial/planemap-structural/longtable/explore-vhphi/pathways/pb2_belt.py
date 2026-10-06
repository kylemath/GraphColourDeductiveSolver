"""[exploratory] Coordinator's extra input: holes of the audit's 12:40 lemma class (degree-5 vertex with <= 1
neighbour of degree >= 12). Exact max pure radius at those holes on T4, order14, A_3 (all degree-5 holes qualify:
max degree 6) and on the belt G_n (TwoPoleBelt: poles 0,1 of degree n; u_i ~ pole 0, v_i ~ pole 1; edges
u_i u_{i+1}, v_i v_{i+1}, u_i v_i, u_i v_{i-1}; same adjacency as audit/team-a-belt-check.py). G_6 = order14.
Belt holes are all equivalent under the dihedral/swap symmetry, so one belt hole u_0 is computed; the pole too."""
import time
from collections import Counter
from pb2_lib import *
t0 = time.process_time()

def belt(n):
    adj = {i: set() for i in range(2 + 2 * n)}
    u = lambda i: 2 + i % n; v = lambda i: 2 + n + i % n
    def e(x, y): adj[x].add(y); adj[y].add(x)
    for i in range(n):
        for x, y in [(0, u(i)), (1, v(i)), (u(i), u(i + 1)), (v(i), v(i + 1)), (u(i), v(i)), (u(i), v(i - 1))]: e(x, y)
    return adj

def qualifying(adj):
    deg = {x: len(adj[x]) for x in adj}
    return [x for x in adj if deg[x] == 5 and sum(deg[w] >= 12 for w in adj[x]) <= 1]

for name, adj in graphs():
    q = qualifying(adj)
    mx = {h: max(radius_table(adj, h)[0].values()) for h in q}
    print(f"[exploratory] {name}: qualifying holes {len(q)} of {sum(len(adj[x])==5 for x in adj)} deg-5; max radius hist {dict(Counter(mx.values()))}")
for n in range(5, 15):
    t1 = time.process_time(); adj = belt(n)
    q = qualifying(adj)
    dist, idx, nb = radius_table(adj, 2)
    hb = Counter(dist.values())
    dp, ip, _ = radius_table(adj, 0)
    print(f"[exploratory] belt G_{n} (order {2*n+2}, pole degree {n}): qualifying {len(q)}/{2*n} belt holes; "
          f"belt hole u_0: {len(idx)} states, radius hist {dict(sorted(hb.items()))}; pole hole: {len(ip)} states, max radius {max(dp.values())}; "
          f"cpu {round(time.process_time()-t1,1)}", flush=True)
    if time.process_time() - t0 > 240: print("stopping: time budget"); break
print("cpu", round(time.process_time() - t0, 1))
