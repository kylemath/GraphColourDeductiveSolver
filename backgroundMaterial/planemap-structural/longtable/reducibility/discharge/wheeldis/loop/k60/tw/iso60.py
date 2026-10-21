"""Round 60: are two kc lines the same configuration?  Graph = ring cycle + interior, interior vertices coloured by degree,
ring vertices marked; compared with networkx isomorphism (data read only, never run)."""
import sys, networkx as nx
from networkx.algorithms import isomorphism as I
def G(line):
    f = line.split(); r, m = int(f[1]), int(f[2]); ra = f[3].split(';'); ia = f[4].split(';')
    g = nx.Graph()
    for i in range(r): g.add_node(('r', i), t='ring'); 
    for i in range(r): g.add_edge(('r', i), ('r', (i + 1) % r))
    for v in range(m):
        for x in ra[v].split(','):
            if x != '-': g.add_edge(('i', v), ('r', int(x)))
        for x in ia[v].split(','):
            if x != '-': g.add_edge(('i', v), ('i', int(x)))
    for v in range(m): g.nodes[('i', v)]['t'] = 'd%d' % g.degree(('i', v))
    return f[0], g
A = [G(l) for l in open(sys.argv[1]) if l.strip()]; B = [G(l) for l in open(sys.argv[2]) if l.strip()]
for na, ga in A:
    hits = [nb for nb, gb in B if ga.number_of_nodes() == gb.number_of_nodes() and
            I.GraphMatcher(ga, gb, node_match=lambda a, b: a['t'] == b['t']).is_isomorphic()]
    print(na, ga.number_of_nodes(), sorted(d['t'] for _, d in ga.nodes(data=True) if d['t'] != 'ring'), '->', hits or 'no match')
