import sys, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
def G_(r, m, rs, is_):
    m = int(m); R = rs.split(';'); I = is_.split(';'); G = nx.Graph()
    for i in range(m):
        G.add_node(i)
        for j in I[i].split(','):
            if j: G.add_edge(i, int(j))
    for i in range(m): G.nodes[i]['deg'] = G.degree(i) + (0 if R[i] in ('-', '') else len(R[i].split(',')))
    return G
names = [l.split()[0] for l in open(sys.argv[1]) if l.strip()]
stored = {l.split()[0]: l.split() for l in open(sys.argv[2]) if l.strip()}
reb = [l.split() for l in open(sys.argv[3]) if l.strip()]
dfast = {}
for fn in sys.argv[4:]:
    for l in open(fn):
        f = l.split()
        if f and f[0] in names: dfast[f[0]] = ' '.join(x for x in f[1:] if x[:2] in ('r=', 'm=', 'D='))
for nm, rb in zip(names, reb):
    Gr = G_(*rb[1:5]); st = stored.get(nm)
    iso = GraphMatcher(Gr, G_(*st[1:5]), node_match=lambda a, b: a['deg'] == b['deg']).is_isomorphic() if st else None
    print(nm, 'rebuilt r=%s m=%s' % (rb[1], rb[2]), '| stored kc: %s' % ('none' if not st else 'r=%s m=%s iso=%s same_line=%s' % (st[1], st[2], iso, st[1:5] == rb[1:5])), '| dfast:', dfast.get(nm))
