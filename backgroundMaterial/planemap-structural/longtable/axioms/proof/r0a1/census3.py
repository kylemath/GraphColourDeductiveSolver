"""Chunked planar census WITHOUT isomorphism reduction (every chord diagram analysed): counts diagrams whose
PM digraph D has a directed cycle, and Ham arcs inside an SCC.  usage: census3.py n chunk nchunks"""
import sys, json, time, itertools
import networkx as nx
from r0lib import planar_normal_forms, digraph
n, ch, nch = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
t0 = time.time(); nd = 0; cyc = 0; bad = 0; maxpm = 0
import r0lib
orig = itertools.permutations
cnt = [0]
def perm_chunk(it, r):
    for i, x in enumerate(orig(it, r)):
        if i % nch == ch: yield x
r0lib.itertools = type('M', (), {'permutations': staticmethod(perm_chunk)})
for g, pm, vch in planar_normal_forms(n):
    nd += 1
    P, ks, arcs, ham = digraph(g)
    maxpm = max(maxpm, len(P))
    D = nx.DiGraph(); D.add_nodes_from(range(len(P))); D.add_edges_from(arcs)
    if not nx.is_directed_acyclic_graph(D):
        cyc += 1
        comp = {}
        for ci, c in enumerate(nx.strongly_connected_components(D)):
            for x in c: comp[x] = ci
        bad += any(comp[i] == comp[j] for i, j in ham)
print(json.dumps(dict(n=n, chunk=ch, nchunks=nch, diagrams=nd, cyclicD=cyc, R0_violations=bad, maxPM=maxpm,
                      sec=round(time.time() - t0, 1))), flush=True)
