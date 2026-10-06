#!/usr/bin/env python3
"""Rigid labelled states WITH a ring chord (excluded by disc_gen2 by design): are any of them
locked at every legal admitting fan? Audit code; uses only rigid_census.py and case_walk_check.py.
usage: chord_states.py PLANTRI_FILE [SHARD NSHARDS]   (shard: graphs with index % NSHARDS == SHARD)"""
import sys, json
from rigid_census import parse_plantri, census_graph
from case_walk_check import separable

out = {'chord_states': 0, 'locked_at_all_legal_admitting': 0, 'no_legal_admitting_fan': 0, 'examples': []}
shard, nsh = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 1)
out['shard'] = [shard, nsh]
for gi, line in enumerate(open(sys.argv[1])):
    if not line.strip() or gi % nsh != shard: continue
    rot = parse_plantri(line)
    adj, found = census_graph(rot)
    for (x, ring, col, legal) in found:
        if legal: continue
        out['chord_states'] += 1
        c = [col.get(v, -1) for v in range(len(rot))]
        # relabel nothing: separable() needs ring at indices; work with actual vertex ids
        legal_fans = []
        for k in (1, 3, 4):                                   # admitting fans: singleton apexes
            a = ring[k]
            if ring[(k + 2) % 5] in adj[a] or ring[(k + 3) % 5] in adj[a]: continue
            legal_fans.append(k)
        if not legal_fans:
            out['no_legal_admitting_fan'] += 1; continue
        locks = {k: separable(adj, c, x, ring[k])[0] for k in legal_fans}
        if not any(locks.values()):
            out['locked_at_all_legal_admitting'] += 1
            if len(out['examples']) < 10: out['examples'].append(dict(graph=gi, x=x, ring=ring, legal=legal_fans))
print(json.dumps(out))
