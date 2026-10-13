"""R0* on other graph collections: every graph in the given jsonl / line files (TrackU annealing records,
seeds, random graphs) that is planar with its rotation at v: does D have a cycle, does G have a Hamiltonian arc,
and are both ever true at once (an R0* counterexample)?  Graphs with more than PMCAP perfect matchings are
skipped and counted.  usage: star_files.py PMCAP file1 [file2 ...]"""
import sys, json, time
import networkx as nx
from r0lib import G5, digraph
PMCAP = int(sys.argv[1])
seen = set(); stats = dict(graphs=0, planar=0, skipped=0, cyc=0, ham=0, both=0, cyc_ham_inside=0)
t0 = time.time()
for path in sys.argv[2:]:
    for line in open(path):
        line = line.strip()
        if not line: continue
        if line.startswith('{'):
            d = json.loads(line)
            if 'edges' not in d: continue
            n, E, fv = d['n'], [tuple(e) for e in d['edges']], d['fv']
        else:
            t = list(map(int, line.split())); n, m = t[0], t[1]
            E = [(t[2 + 2 * i], t[3 + 2 * i]) for i in range(m)]; fv = t[2 + 2 * m: 7 + 2 * m]
        key = (n, tuple(sorted(tuple(sorted(e)) for e in E)), tuple(fv))
        if key in seen: continue
        seen.add(key); stats['graphs'] += 1
        a, b = E[fv[0]]; c, dd = E[fv[1]]; v = a if a in (c, dd) else b
        perm = {x: x for x in range(n)}; perm[v] = 0; perm[0] = v
        try:
            g = G5(n, [(perm[x], perm[y]) for x, y in E], fv)
        except AssertionError:
            continue
        if not g.planar_rot(): continue
        stats['planar'] += 1
        P = g.pms()
        if len(P) > PMCAP: stats['skipped'] += 1; continue
        P_, ks, arcs, ham = digraph(g)
        D = nx.DiGraph(); D.add_nodes_from(range(len(P_))); D.add_edges_from(arcs)
        cyc = not nx.is_directed_acyclic_graph(D)
        stats['cyc'] += cyc; stats['ham'] += bool(ham); stats['both'] += (cyc and bool(ham))
        print('planar:', path.split('/')[-1], 'n', n, '#PM', len(P_), 'cyclicD', cyc, '#Ham arcs', len(ham), flush=True)
        if cyc and ham:
            comp = {}
            for ci, cc in enumerate(nx.strongly_connected_components(D)):
                for x in cc: comp[x] = ci
            stats['cyc_ham_inside'] += any(comp[i] == comp[j] for i, j in ham)
            print('R0* COUNTEREXAMPLE CANDIDATE', path.split('/')[-1], n, flush=True)
print(json.dumps(stats), f'{time.time()-t0:.0f}s', flush=True)
