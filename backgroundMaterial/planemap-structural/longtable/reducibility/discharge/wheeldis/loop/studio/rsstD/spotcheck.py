"""Studio spot-check of the RSST-D pattern mapping with an independent matcher.
For sampled (row, RSST D config) hits from rsst_rows.py's 'fixed' mode:
- build the row's two-ring patch with gen.py's `build` (u, link, second ring as a cycle);
- label the pinned slots with their exact degrees (u = d; pinned w_i, s_i <= 8);
- ask networkx (GraphMatcher, induced subgraph isomorphism, node match on degree) whether the configuration's
  interior graph G(K) embeds.
Agreement on every sample = a pass. Usage: python3 spotcheck.py ROWFILE [n=8] [seed=1] [all]   ('all': every D configuration on every row, prints embeddings)"""
import sys, os, random, re
import networkx as nx
from networkx.algorithms import isomorphism as iso
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.argv, ARGV = [sys.argv[0], 'none'], sys.argv[1:]
src = open(os.path.join(HERE, 'rsst_rows.py')).read(); exec(src[:src.index("if __name__ == '__main__':")])
gsrc = open(os.path.join(W, 'gen.py')).read(); gsrc = gsrc[:gsrc.index('arrs = []')].replace('os.path.dirname(os.path.abspath(__file__))', repr(W))
sys.argv = ['gen.py', '/dev/null', '30']; exec(gsrc)
N = int(next((a[2:] for a in ARGV if a.startswith('n=')), '8')); random.seed(int(next((a[5:] for a in ARGV if a.startswith('seed=')), '1')))
ALLC = 'all' in ARGV   # negative control: try every D configuration on every row
rows = sorted(set(read_rows(os.path.join(W, ARGV[0]))))
pairs = []
for d, lk, sv in rows:
    w = [int(c) for c in lk]; s = [int(c) for c in sv]
    for i in (range(len(P)) if ALLC else hits(d, w, s, 'fixed')):
        if P[i]['kind'] == 'D': pairs.append((d, lk, sv, i))
print('D hits (row, config):', len(pairs))
ok = bad = 0
for d, lk, sv, i in (pairs if ALLC else random.sample(pairs, min(N, len(pairs)))):
    w = [int(c) for c in lk]; s = [int(c) for c in sv]
    adj, name = build(d, w, {})
    fw = [w[k] == 5 or w[(k - 1) % d] == 5 or w[(k + 1) % d] == 5 for k in range(d)]
    fs = [w[k] == 5 or w[(k + 1) % d] == 5 for k in range(d)]
    H = nx.Graph()
    for v, nb in adj.items():
        for x in nb: H.add_edge(v, x)
    lab = {}
    for v, nm in name.items():
        if nm == ('u',): lab[v] = d
        elif nm[0] == 'w' and fw[nm[1]] and w[nm[1]] <= 8: lab[v] = w[nm[1]]
        elif nm[0] == 's' and fs[nm[1]] and s[nm[1]] <= 8: lab[v] = s[nm[1]]
    Hl = H.subgraph(list(lab)).copy(); nx.set_node_attributes(Hl, lab, 'deg')
    c = CONFS[i]; r = c['r']; U = [x for x in range(r + 1, c['n'] + 1)]
    K = nx.Graph(); K.add_nodes_from(U)
    for x in U:
        for y in c['adj'][x]:
            if y > r: K.add_edge(x, y)
    nx.set_node_attributes(K, {x: len(c['adj'][x]) for x in U}, 'deg')
    GM = iso.GraphMatcher(Hl, K, node_match=lambda a, b: a['deg'] == b['deg'])
    got = GM.subgraph_is_isomorphic()   # induced
    if got or not ALLC: print('d=%d %s %s  RSST %s (ring %d, D): networkx %s' % (d, lk, sv, c['name'], r, 'embeds' if got else 'NO EMBEDDING'))
    ok += got; bad += not got
print('spot-check: %d agree, %d disagree' % (ok, bad))
