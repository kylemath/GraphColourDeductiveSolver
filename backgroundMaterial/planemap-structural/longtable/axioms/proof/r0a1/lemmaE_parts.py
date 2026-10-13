"""Check the two intermediate claims of Lemma E on every arc (M_t, M_{t+1}) of the planar census that has a
successor: in E - M_{t+1}, sum of sigma_t over every v-free (M_t,R_t)-cycle is 0 mod 4, and over the odd loop
X minus v it is 2 mod 4.  usage: lemmaE_parts.py n"""
import sys, json, collections
import networkx as nx
from r0lib import G5, analyse
from sigsum import ccw_rot
n = int(sys.argv[1]); cz = collections.Counter(); cx = collections.Counter()
for l in open(f'out/census_n{n}_p.jsonl'):
    r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
    A = analyse(g); rot = ccw_rot(g); P = A['P']
    for (i, j) in A['arcs']:
        if A['D'].out_degree(j) == 0: continue
        Mt, Mt1 = P[i], P[j]
        def sig(w):
            a = next(e for e in g.inc[w] if Mt >> e & 1); b = next(e for e in g.inc[w] if Mt1 >> e & 1)
            return 1 if (rot[w].index(b) - rot[w].index(a)) % 3 == 1 else -1
        Q = nx.Graph(); Q.add_nodes_from(range(g.n))
        Q.add_edges_from(g.E[e] for e in range(g.m) if not (Mt1 >> e & 1))
        k = g.k(Mt)
        for comp in nx.connected_components(Q):
            if 0 not in comp:
                cz[sum(sig(w) for w in comp) % 4] += 1
            else:
                # X = loop through f_{k-1}
                e = g.fv[(k - 1) % 5]; x = g.other(e, 0); last = e; tot = 0
                while x != 0:
                    tot += sig(x)
                    nxt = [f for f in g.inc[x] if not (Mt1 >> f & 1) and f != last][0]
                    last = nxt; x = g.other(nxt, x)
                assert g.fidx[last] == (k + 2) % 5
                cx[tot % 4] += 1
print(f'n={n}: v-free cycles: sum sigma mod 4 = {dict(cz)};  odd loop X - v: sum sigma mod 4 = {dict(cx)}')
