#!/usr/bin/env python3
"""[exploratory] Verify Intern C's cycle-7 cross-j collision (interns-2026-10-06/intern-C-cycle7.md).
T: v; y_0..y_4 (link); w_0..w_4; z_0..z_4; u. Edges: v-y_t; y_t y_{t+1}; y_t-w_{t-1}, y_t-w_t; w_t w_{t+1}; w_t-z_{t-1}, w_t-z_t;
z_t z_{t+1}; u-z_t. Colouring: v = X; y = (S,p,q,p,q); w = (q,S,X,S,p); z = (p,q,p,q,S); u = X.
Checks: triangulation (E = 3n-6, triangles = 2n-4), degrees, no separating triangle, isomorphism to a gentri order-17 graph,
properness, s1 (y_4 -> X) and s2 (y_1 -> X) and their repeat index, locks, and that Lemma A's phi sends both to t.
Builds the rotation system by hand (faces listed below) so the link order y_0..y_4 is the rotation at v."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common")); sys.path.insert(0, os.path.join(H, "..", "3-inert-disc"))
from kempe_py import Space, gentri_rotation, adj_from_rot
from qall_scan import vertex_orbits, dart_code
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")
v = 0; y = [1 + t for t in range(5)]; w = [6 + t for t in range(5)]; z = [11 + t for t in range(5)]; u = 16
E = set()
add = lambda a, b: E.add((min(a, b), max(a, b)))
for t in range(5):
    add(v, y[t]); add(y[t], y[(t + 1) % 5]); add(y[t], w[(t - 1) % 5]); add(y[t], w[t]); add(w[t], w[(t + 1) % 5])
    add(w[t], z[(t - 1) % 5]); add(w[t], z[t]); add(z[t], z[(t + 1) % 5]); add(u, z[t])
n = 17; adj = {i: set() for i in range(n)}
for a, b in E: adj[a].add(b); adj[b].add(a)
tri = sum(1 for a, b in E for c in adj[a] & adj[b] if c > b)
res = {"E": len(E), "triangles": tri, "triangulation_counts_ok": len(E) == 3 * n - 6 and tri == 2 * n - 4,
       "degrees": sorted(len(adj[i]) for i in range(n))}
# rotation system: every triangle is a face (no separating triangle), so each link is a cycle; walk it, then orient all
# vertices consistently (if c follows b around a, then a follows c around b), propagating from v with rot[v] = y_0..y_4.
def link_cycle(a):
    nb = adj[a]; cyc = [min(nb)]
    while len(cyc) < len(nb):
        cand = [x for x in adj[cyc[-1]] & nb if x not in cyc]; cyc.append(cand[0] if len(cyc) == 1 else cand[0])
    return cyc
rot = {v: y[:]}; queue = [v]
while queue:
    a = queue.pop()
    for k, b in enumerate(rot[a]):
        if b in rot: continue
        c = rot[a][(k + 1) % len(rot[a])]          # c follows b around a  =>  a follows c around b
        cyc = link_cycle(b); i = cyc.index(c)
        cyc = cyc[i:] + cyc[:i]                     # starts at c
        if cyc[1] != a: cyc = [cyc[0]] + cyc[1:][::-1]
        rot[b] = cyc[1:] + cyc[:1]; queue.append(b)
R = [rot[i] for i in range(n)]
nxt = {}
for a in range(n):
    for k, b in enumerate(R[a]): nxt[(a, b)] = R[a][(k + 1) % len(R[a])]
ok = all(nxt[(b, nxt[(a, b)])] == a for (a, b) in nxt)    # face (a, b, c) closes consistently
res["rotation_consistent"] = ok
_, code = vertex_orbits(R)
lines = [l for l in open(os.path.join(GENTRI, "tri17.txt")) if l.strip()]
res["gentri17_iso_index"] = [gi for gi, l in enumerate(lines) if vertex_orbits(gentri_rotation(l))[1] == code]
S_, p, q, X = 0, 1, 2, 3
col = {v: X, u: X}
for t, cc in enumerate((S_, p, q, p, q)): col[y[t]] = cc
for t, cc in enumerate((q, S_, X, S_, p)): col[w[t]] = cc
for t, cc in enumerate((p, q, p, q, S_)): col[z[t]] = cc
res["proper_on_T"] = all(col[a] != col[b] for a, b in E)
Sp = Space(adj, v, link=R[v]); Sp.build_graph(); cl, _ = Sp.classes(); dist = Sp.dist_to_filled()
tcol = {k: c for k, c in col.items() if k != v}
s1 = dict(tcol); s1[y[4]] = X; s2 = dict(tcol); s2[y[1]] = X
res["s1_proper"] = all(s1[a] != s1[b] for a, b in E if v not in (a, b)); res["s2_proper"] = all(s2[a] != s2[b] for a, b in E if v not in (a, b))
it, i1, i2 = Sp.state_of(tcol), Sp.state_of(s1), Sp.state_of(s2)
res["same_class"] = cl[it] == cl[i1] == cl[i2]


def phi(si):
    c = Sp.states[si]; cm = Sp.cmasks(c); L = Sp.linki; lc = [c[x] for x in L]
    j = [t for t in range(5) if lc[t] == lc[(t + 2) % 5]][0]; x = [L[(j + t) % 5] for t in range(5)]
    mu, A, B = lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
    l1 = bool(Sp.flood(1 << x[1], cm[mu] | cm[A]) >> x[3] & 1); l2 = bool(Sp.flood(1 << x[1], cm[mu] | cm[B]) >> x[4] & 1)
    if not l1: K = Sp.flood(1 << x[3], cm[mu] | cm[A]); return j, l1, l2, 1, Sp.index[Sp.swap(c, K, mu, A)]
    if not l2: K = Sp.flood(1 << x[4], cm[mu] | cm[B]); return j, l1, l2, 2, Sp.index[Sp.swap(c, K, mu, B)]
    return j, l1, l2, None, None


for name, si in (("s1", i1), ("s2", i2)):
    j, l1, l2, case, img = phi(si)
    res[name] = {"j": j, "lock1": l1, "lock2": l2, "case": case, "phi_is_t": img == it}
res["t_filled"] = dist[it] == 0
print(json.dumps(res, indent=1))
