#!/usr/bin/env python3
"""Track U: for graphs in an eval JSONL: planarity, 3-connectivity, and whether the cyclic order f0..f4 at v agrees
(up to reversal) with v's rotation in a planar embedding (unique if 3-connected), and WL-hash isomorphism class.
usage: tu_planarcheck.py EVAL.jsonl"""
import sys, json, networkx as nx
res = []
for l in open(sys.argv[1]):
    d = json.loads(l)
    if d['event'] != 'graph': continue
    E = d['edges']; fv = d['fv']
    G = nx.Graph(); G.add_edges_from(E)
    pl, emb = nx.check_planarity(G)
    r = dict(gi=d['gi'], n=d['n'], planar=pl)
    if pl:
        r['conn'] = nx.node_connectivity(G)
        nb = [E[e][1] if E[e][0] == 0 else E[e][0] for e in fv]
        cw = list(emb.neighbors_cw_order(0))
        i = cw.index(nb[0]); rot = cw[i:] + cw[:i]
        rev = [rot[0]] + rot[1:][::-1]
        r['v_rotation_planar'] = (nb == rot) or (nb == rev)
    r['wl'] = nx.weisfeiler_lehman_graph_hash(G, iterations=4)[:10]
    res.append(r); print(json.dumps(r))
