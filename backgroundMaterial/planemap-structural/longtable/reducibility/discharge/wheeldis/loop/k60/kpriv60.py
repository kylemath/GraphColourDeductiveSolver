"""EXPLORE round 60 (Long Table 06:19Z ruling): build out/job30/kpriv.txt, the private-split kills, kept out of k3x.
Name form g<d>_<link>_<s>_w<k>:<pp>: the letters of the vertices the kill needs ('.' = not needed, so letter 9 never
appears), pp = the two privates of the link 7 w_k, p_k_1 (next to s_k) then p_k_2 (next to s_(k-1)) (the pair census
names priv<a><b>); a placement that avoids u is written g<d>_-<link>_... (cen53's g-name marker).
Two sources:
  engine kills (ENG file: tag row k ab evidence | kc line), named from my own window (pw60.py, u + exact link + s_(k-1),
  s_k + exact privates), checked isomorphic to the kc line the engines ran on, and checked against the registry and the
  2026 set (containment);
  containment kills (pair60 output files: the DEAD cells): every placement of the named configuration inside the
  cell's closed vertices, tagged C-reg (registry) or C-2026 (2026 set, two engines in round 54d), kept when no other
  kept pattern of the same row and w_k needs a subset of its letters.
usage: python3 kpriv60.py TD TC XKC ENG PAIR60OUT... > kpriv.txt"""
import sys, os, collections
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, '..', 'k59'))
A = list(sys.argv); sys.argv = A[:1] + ['x', 'x', 'x']
import pair60 as P, tw60, chain59 as C, grow
import networkx as nx
from networkx.algorithms import isomorphism as I
TD, TC, XKC, ENG = A[1:5]; OUTS = A[5:]
REG, miss = C.F.registry(TD, TC); XR = [grow.kcline(l, 'x') for l in open(XKC) if l.strip()]
BYN = {c[0]: (c, 'C-reg') for c in REG}; BYN.update({c[0]: (c, 'C-2026') for c in XR})

def case(row, k, a, b):
    lk, sv = row.split('/'); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]
    D, u, W, S = P.frame(LK, SV); p1, p2 = P.privates(D, W, S, k)
    for x, l in ((p1, a), (p2, b)):
        if l <= 8: assert D.close(x, l)
    return D, u, W, S, p1, p2, LK, SV

def pattern(D, u, W, S, p1, p2, k, img):
    d = len(W)
    lk = ''.join(str(D.deg[w]) if w in img else '.' for w in W)
    sv = ''.join(str(D.deg[s]) if s in img else '.' for s in S)
    pp = ''.join(str(D.deg[x]) if x in img else '.' for x in (p1, p2))
    assert all(v in set(W) | set(S) | {u, p1, p2} for v in img)
    return 'g%d_%s%s_%s_w%d:%s' % (d, '' if u in img else '-', lk, sv, k, pp)

def graph(line):
    f = line.split(); r, m = int(f[1]), int(f[2]); ra = f[3].split(';'); ia = f[4].split(';'); g = nx.Graph()
    for i in range(r): g.add_node(('r', i), t='ring'); g.add_edge(('r', i), ('r', (i + 1) % r))
    for v in range(m):
        for x in ([] if ra[v] == '-' else ra[v].split(',')): g.add_edge(('i', v), ('r', int(x)))
        for x in ([] if ia[v] == '-' else ia[v].split(',')): g.add_edge(('i', v), ('i', int(x)))
    for v in range(m): g.nodes[('i', v)]['t'] = g.degree(('i', v))
    return g

def inside(line, CONF):
    c = grow.kcline(line, 'w')
    return sorted({k[0] for k in CONF if len(k[2]) <= len(c[2]) and grow.embeddings(k, c[2], c[4], c[5], c[3])})

print('# kpriv.txt: private-split kills (Long Table 06:19Z), out of k3x; the LP reads them only through a split row key.')
print('# name g<d>_<link>_<s>_w<k>:<pp>: letters of the vertices the kill needs, "." = not needed (letter 9 never appears);')
print('# pp = w_k\'s privates, p_k_1 (next to s_k) then p_k_2 (next to s_(k-1)); "_-" before the link = placement avoids u.')
print('# tags: D2 / C2 = window two-engine D / C (engines and commits in ev=); C-reg / C-2026 = a configuration of the')
print('# registry (main 7cd777a3 k3x + RSST 582) / of the 2026 set (two engines, round 54d) inside the needed vertices.')
print('# cont= containment of the window itself (registry, 2026 set); cells= pair-census cells (row w<k> priv<a><b>) covered.')
print('# Built by explore loop/k60/kpriv60.py on branch claude/project-thread-nh6pv2.')
rows = []
for l in open(ENG):
    if not l.strip() or l.startswith('#'): continue
    head, kcl = l.split(' | ', 1); f = head.split(); tag, row, k, ab, ev = f[0], f[1], int(f[2]), f[3], ' '.join(f[4:])
    a, b = int(ab[0]), int(ab[1]); D, u, W, S, p1, p2, LK, SV = case(row, k, a, b)
    I0 = [u] + [w for w in W if w in D.deg] + [s for s in (S[k - 1], S[k]) if s in D.deg] + [x for x in (p1, p2) if x in D.deg]
    nm = kcl.split()[0]                      # pw60x.py's grown window: its apex letters add those apexes
    if nm.startswith('x60_'): I0 += [S[i] for i, c in enumerate(nm.split('_')[-1]) if c != '.' and S[i] not in I0]
    mine, il, rl = tw60.window(D, I0, 'mine')
    iso = I.GraphMatcher(graph(mine), graph(kcl), node_match=lambda x, y: x['t'] == y['t']).is_isomorphic()
    assert iso, (row, k, ab)
    cr, cx = inside(kcl, REG), inside(kcl, XR)
    rows.append('%s r=%s tag=%s | ev=%s | iso=mine | cont=registry:%s,2026:%s | cells=%s w%d priv%s | %s' % (
        pattern(D, u, W, S, p1, p2, k, set(I0)), kcl.split()[1], tag, ev, '+'.join(cr) or 'none', '+'.join(cx) or 'none',
        row, k, ab, kcl.strip()))
print('## engine kills (%d)' % len(rows)); print('\n'.join(rows))
found = collections.defaultdict(set); src = {}
for fn in OUTS:
    for l in open(fn):
        if ': DEAD,' not in l: continue
        row, wk, pv = l.split()[:3]; k = int(wk[1:]); ab = pv.rstrip(':')[4:]; a, b = int(ab[0]), int(ab[1])
        names = l.split('inside: ')[1].split(' (')[0].split()
        D, u, W, S, p1, p2, LK, SV = case(row, k, a, b)
        Pv = list(range(D.n)); pa = {v: set(D.adj[v]) for v in Pv}; pf = set(D.tris); fd = dict(D.deg)
        for nm in names:
            c, tag = BYN[nm]
            for e in grow.embeddings(c, Pv, pa, pf, fd):
                img = {v for x, v in e}
                if any(v not in fd for v in img): continue
                pt = pattern(D, u, W, S, p1, p2, k, img); found[(row, k, pt, nm, tag)].add('priv' + ab); src[(row, k)] = 1
def sub(p, q):                               # p needs a subset of q's letters
    return len(p) == len(q) and all(x == '.' or x == y for x, y in zip(p, q))
keys = sorted(found); keep = []
for key in keys:
    row, k, pt = key[:3]
    if any(o != key and o[0] == row and o[1] == k and sub(o[2], pt) and (not sub(pt, o[2]) or o < key) for o in keys): continue
    keep.append(key)
print('## containment kills (%d kept of %d placements patterns)' % (len(keep), len(keys)))
for row, k, pt, nm, tag in keep:
    print('%s r=- tag=%s | ev=%s inside (two engines) | cells=%s w%d %s' % (pt, tag, nm, row, k, ' '.join(sorted(found[(row, k, pt, nm, tag)]))))
