#!/usr/bin/env python3
"""Which RSST configs already have a Lean job on main under another name (Opus, 10 Nov 2026).
Matches every RSST kc literal (rsst_closure/inputs/rsst.txt f561ac13) up to isomorphism (ring cycle kept, mirror allowed) against
every kc literal listed in a Lean job input on origin/main (wheeldis/out/job_H*/ and lean*/ *.tsv / *.txt; copies in leanlists/).
A listing is not a build result: the Studio confirms the module status.  usage: python3 -I leaniso.py <out tsv>"""
import sys, os, re, glob, collections
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
RSST = '/mnt/project-files/swarm/round6/W6r-replay/rsst_closure/inputs/rsst.txt'
LIT = re.compile(r'^(\S+)\t(\d+) (\d+) ([-0-9,;]+) ([-0-9,;]+)')
def graph(r, n, rn, inn):
    G = nx.Graph()
    for i in range(r): G.add_node(('R', i), ring=1); G.add_edge(('R', i), ('R', (i + 1) % r))
    rl = rn.split(';'); il = inn.split(';'); assert len(rl) == n and len(il) == n, (r, n, rn, inn)
    for k in range(n):
        G.add_node(('I', k), ring=0)
        if rl[k] != '-':
            for x in rl[k].split(','): G.add_edge(('I', k), ('R', int(x)))
        if il[k] != '-':
            for x in il[k].split(','): G.add_edge(('I', k), ('I', int(x)))
    return G
def key(G): return nx.weisfeiler_lehman_graph_hash(G, node_attr='ring', iterations=4)
lean = collections.defaultdict(list); nl = 0
for fn in sorted(glob.glob(os.path.join(HERE, 'leanlists', '*'))):
    if fn.endswith('files.txt'): continue
    for line in open(fn, errors='replace'):
        m = LIT.match(line)
        if not m: continue
        nm, r, n, rn, inn = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4), m.group(5)
        try: G = graph(r, n, rn, inn)
        except (AssertionError, ValueError): continue
        nl += 1; lean[(r, n, key(G))].append((nm, os.path.basename(fn), G))
print('lean literals', nl, 'buckets', len(lean))
nm_ = nx.algorithms.isomorphism.categorical_node_match('ring', 0)
with open(sys.argv[1], 'w') as g:
    g.write('# RSST config vs Lean job inputs on origin/main (isomorphism of kc literals); listing != build status\nrsst_id\tlean_matches\n')
    hit = 0
    for line in open(RSST):
        f = line.split()
        if len(f) < 5 or not f[0].startswith('rsst'): continue
        r, n = int(f[1]), int(f[2]); G = graph(r, n, f[3], f[4])
        ms = sorted(set('%s@%s' % (a, b) for a, b, H in lean.get((r, n, key(G)), []) if nx.is_isomorphic(G, H, node_match=nm_)))
        hit += bool(ms); g.write('%s\t%s\n' % (f[0], ','.join(ms) if ms else '-'))
print('rsst configs with a Lean-job listing', hit)
