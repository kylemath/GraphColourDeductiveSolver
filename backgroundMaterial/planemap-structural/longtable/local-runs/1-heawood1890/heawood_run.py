#!/usr/bin/env python3
"""[exploratory] Local compute item 1: Heawood's 1890 map graph (25 vertices, 69 edges).
- C++ (../common/krad, derived from studio-explore kclass.cpp) and the existing ../common/kclass (kclass.cpp unchanged):
  kappa(T), and at every degree-5 hole kappa(T - v), targetless classes, rho, per-class radius.
- Python (../common/kempe_py.py, independent plain BFS): the same numbers at every degree-5 hole, as a cross-check.
- Heawood's own failing colouring at hole V: its class size, class radius, its distance to the filled set, and one shortest
  filling swap sequence replayed on the concrete colouring (colour letters r, b, y, g as Heawood's).
usage: python3 heawood_run.py > heawood-results.json"""
import json, os, subprocess, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, adj_from_rot
from collections import deque

d = json.load(open(os.path.join(H, "..", "..", "historical-traps", "heawood1890.json")))
names, rot, E = d["vertex_names"], d["rotation"], d["edges"]
adj = adj_from_rot(rot); n = len(rot)
assert sum(len(r) for r in rot) == 2 * len(E) == 138
with tempfile.NamedTemporaryFile("w", suffix=".el", delete=False) as fh:
    fh.write("%d %d\n" % (n, len(E)) + "".join("%d %d\n" % tuple(e) for e in E)); EL = fh.name
cpp = lambda exe, *a: json.loads(subprocess.run([os.path.join(H, "..", "common", exe), EL, *map(str, a)], capture_output=True, text=True).stdout)

out = {"graph": "heawood1890.json", "n": n, "edges": len(E)}
out["kappa_T_cpp_krad"] = cpp("krad", -1)["n_classes"]; out["kappa_T_cpp_kclass"] = cpp("kclass", -1)["n_classes"]
ST = Space(adj, None); ST.build_graph(); out["kappa_T_python"] = ST.classes()[1]; out["states_T"] = len(ST.states)
holes = []
for v in range(n):
    if len(rot[v]) != 5: continue
    a = cpp("krad", v); b = cpp("kclass", v)
    S = Space(adj, v, link=rot[v]); S.build_graph(); cl, ncl = S.classes(); dist = S.dist_to_filled()
    tl = [k for k in range(ncl) if not any(dist[s] == 0 for s in range(len(dist)) if cl[s] == k)]
    rho_py = -1 if tl else max(dist)
    rec = {"hole": v, "name": names[v], "link": [names[x] for x in rot[v]],
           "kappa_T_minus_v": a["n_classes"], "targetless": a["targetless_classes"], "rho": a["rho"], "states": a["n_states"],
           "filled": a["n_filled"], "classes_cpp": a["classes"],
           "python": {"kappa": ncl, "targetless": len(tl), "rho": rho_py, "states": len(S.states)},
           "kclass_cpp": {"kappa": b["n_classes"], "targetless": b["targetless_classes"], "states": b["n_states"]}}
    rec["agree"] = (a["n_classes"] == ncl == b["n_classes"] and a["targetless_classes"] == len(tl) == b["targetless_classes"]
                    and a["rho"] == rho_py and a["n_states"] == len(S.states) == b["n_states"])
    holes.append(rec)
out["degree5_holes"] = holes

# Heawood's colouring at V
V = d["kempe_failing_colouring"]["hole_index"]; letters = d["kempe_failing_colouring"]["colours_by_name"]
L = "rbyg"; conc = {i: L.index(letters[names[i]]) for i in range(n) if i != V}
for u in conc:
    assert all(conc[u] != conc[w] for w in adj[u] if w != V), "not proper"
S = Space(adj, V, link=rot[V]); S.build_graph(); cl, ncl = S.classes(); dist = S.dist_to_filled()
s0 = S.state_of(conc)
with tempfile.NamedTemporaryFile("w", suffix=".q", delete=False) as fh:
    fh.write("".join("%d %d\n" % (u, c) for u, c in conc.items())); QF = fh.name
q = cpp("krad", V, QF)["query"]
cls = [s for s in range(len(S.states)) if cl[s] == cl[s0]]
h = {"hole": names[V], "link_colours": "".join(L[conc[x]] for x in rot[V]),
     "class_size": len(cls), "class_filled": sum(dist[s] == 0 for s in cls), "class_radius": max(dist[s] for s in cls),
     "dist_from_heawood_colouring": dist[s0], "cpp_query": q}
# one shortest filling sequence, replayed on the concrete colouring
seq, cur, c = [], s0, dict(conc)
while dist[cur] > 0:
    for t, p, qq, K in S.moves(cur):
        if dist[t] == dist[cur] - 1: break
    vs = S.mask_vertices(K)
    # p, qq are canonical labels of state cur; translate to the concrete colours via any vertex
    canon2conc = {S.states[cur][S.idx[u]]: c[u] for u in S.order}
    P, Q = canon2conc[p], canon2conc[qq]
    before = ["%s:%s" % (names[u], L[c[u]]) for u in vs]
    for u in vs: c[u] = Q if c[u] == P else P
    assert S.state_of(c) == t
    seq.append({"pair": L[P] + L[Q], "component": [names[u] for u in vs], "component_current_colours": before, "link_after": "".join(L[c[x]] for x in rot[V]), "dist_after": dist[t]})
    cur = t
for u in c:
    assert all(c[u] != c[w] for w in adj[u] if w != V)
h["shortest_filling_sequence"] = seq
# all first moves on shortest sequences, for the record
firsts = []
for t, p, qq, K in S.moves(s0):
    if dist[t] == dist[s0] - 1:
        canon2conc = {S.states[s0][S.idx[u]]: conc[u] for u in S.order}
        firsts.append({"pair": L[canon2conc[p]] + L[canon2conc[qq]], "component": [names[u] for u in S.mask_vertices(K)]})
h["all_shortest_first_moves"] = firsts
out["heawood_colouring_at_V"] = h
os.unlink(EL); os.unlink(QF)
print(json.dumps(out, indent=1))
