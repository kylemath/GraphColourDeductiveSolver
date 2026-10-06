#!/usr/bin/env python3
"""[exploratory] Sage QA run 1: for each new Kempe class created by deleting an edge e (edge-new-classes.jsonl), walk the whole
class in T - e from its representative (whole-component two-colour swaps, states up to colour renaming) and, per state, count
the colour pairs {p,q} whose bichromatic subgraph is connected (0..6; 6 = frozen: every swap is a renaming)."""
import json, itertools, sys
from collections import Counter

def canon(c, order):
    mp = {}; return tuple(mp.setdefault(c[v], len(mp)) for v in order)

def comps(adj, verts):
    seen, out = set(), []
    for s in verts:
        if s in seen: continue
        comp, st = {s}, [s]; seen.add(s)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y in verts and y not in seen: seen.add(y); comp.add(y); st.append(y)
        out.append(comp)
    return out

for line in open(sys.argv[1] if len(sys.argv) > 1 else "edge-new-classes.jsonl"):
    r = json.loads(line)
    rot = [[ord(ch) - 97 for ch in x] for x in r["plantri_ascii"].split()[1].split(",")]
    u, w = r["edge"]
    adj = {v: set(nb) for v, nb in enumerate(rot)}; adj[u].discard(w); adj[w].discard(u)
    order = list(range(len(rot)))
    for k, cls in enumerate(r["new_classes"]):
        c0 = {int(a): b for a, b in cls["colouring"].items()}
        start = canon(c0, order); seen = {start}; todo = [start]; prof = []
        while todo:
            s = todo.pop(); c = dict(zip(order, s)); conn = 0
            for p, q in itertools.combinations(range(4), 2):
                V = {v for v in order if c[v] in (p, q)}
                cs = comps(adj, V); conn += len(cs) <= 1
                for K in cs:
                    d = dict(c)
                    for v in K: d[v] = q if c[v] == p else p
                    t = canon(d, order)
                    if t not in seen: seen.add(t); todo.append(t)
            prof.append(conn)
        print(json.dumps({"order": r["order"], "index": r["plantri_index"], "edge": r["edge"], "degs": r["endpoint_degrees"], "class": k,
                          "states": len(seen), "expected_size": cls["size"], "connected_pairs_per_state": dict(Counter(prof)),
                          "frozen_states": prof.count(6), "same_colour_at_e_all": all(dict(zip(order, s))[u] == dict(zip(order, s))[w] for s in seen)}))
