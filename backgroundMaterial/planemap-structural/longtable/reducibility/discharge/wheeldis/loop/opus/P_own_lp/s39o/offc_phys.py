"""s39o control (c): physical test of offc against an independent networkx matcher (OFFC_SPEC 6).
For every sampled row window (d, LINK, SWORD) the actual plane graph of its 2-ball is built with networkx: u; w_0..w_{d-1};
ring 2 = s_{i-1}, p_{i,1}, .., p_{i,k}, s_i around each w_i (k = w_i - 5 privates, a 9 counted as 9); edges u-w_i, w_i-w_{i+1},
the ring-2 cycle, w_i to its ring-2 arc; faces u w_i w_{i+1}, w_i w_{i+1} s_i, w_i x y for consecutive x, y of w_i's arc.
Exact vertices: u (degree d) and every w_i, s_i whose letter is not 9; privates are never exact.
Each registry configuration is re-derived here from its own name window (networkx graph of the name's degree-d0 window, induced
subgraph on the exact slots and u; u dropped iff m = #exact; skipped when ambiguous or (r, m) not reproduced -- the spec's rule),
the rpatN configurations come straight from the kc file (row55_hits_kc.txt), and a configuration K embeds in the row iff networkx
finds a node-induced subgraph isomorphism onto exact vertices with equal degrees whose triangles all land on faces.
Engine side: offc.offc_embed(K, d) patterns (the ones offc adds to PATS) tested on the row over the 2d rotations/reflections.
Compared per (row, K).  usage: python3 offc_phys.py NROWS SEED [broken] -> mismatches"""
import sys, os, random, itertools, collections, time
import networkx as nx
from networkx.algorithms import isomorphism as iso
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import offc_lib
NR, SEED = int(sys.argv[1]), int(sys.argv[2]); BROKEN = 'broken' in sys.argv[3:]
B = os.path.dirname(H); M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
Q = B + '/s33z/reg_A67'
ns = offc_lib.load(['root=' + M, 'args=' + Q + '/args_A67.txt', 'rpat=' + B + '/rpatD.txt', 'rpatN=' + H + '/rpatN.txt',
                    'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/w39', 'offc'] + (['offcbroken'] if BROKEN else []))
exec(open(os.path.join(H, 'eng', 'offc.py')).read(), ns)
ns['offc_extend'] = lambda: None          # only OFFREG is needed here
ns['load_patterns']()

def window_graph(d, lk, sv):
    """networkx plane 2-ball of a window; lk/sv letter lists (5..9); returns G (node attrs deg, exact), faces"""
    G = nx.Graph(); F = set()
    G.add_node('u', deg=d, exact=True)
    for i in range(d): G.add_node(('w', i), deg=lk[i], exact=lk[i] != 9); G.add_node(('s', i), deg=sv[i], exact=sv[i] != 9)
    arcs = {}
    for i in range(d):
        k = lk[i] - 5
        ps = [('p', i, j) for j in range(1, k + 1)]
        for p in ps: G.add_node(p, deg=None, exact=False)
        arcs[i] = [('s', (i - 1) % d)] + ps + [('s', i)]
    for i in range(d):
        a, b = ('w', i), ('w', (i + 1) % d)
        G.add_edge('u', a); G.add_edge(a, b); F.add(frozenset(('u', a, b)))
        G.add_edge(a, ('s', i)); G.add_edge(b, ('s', i)); F.add(frozenset((a, b, ('s', i))))
        arc = arcs[i]
        for x, y in zip(arc, arc[1:]): G.add_edge(x, y); G.add_edge(a, x); G.add_edge(a, y); F.add(frozenset((a, x, y)))
    return G, F

def conf_from_entry(src, nm, d0, P, r, m):
    """independent re-derivation of K from the entry's own window (networkx), the spec's acceptance rule"""
    ex = {sl: next(iter(S)) for sl, S in P if len(S) == 1 and 5 <= next(iter(S)) <= 8}
    for (t, i) in ex:
        if t == 's' and ('s', (i + 1) % d0) in ex and ('w', (i + 1) % d0) not in ex: return None
    lk = [ex.get(('w', i), 9) for i in range(d0)]; sv = [ex.get(('s', i), 9) for i in range(d0)]
    G, F = window_graph(d0, lk, sv)
    keep = ['u'] + sorted(ex)
    def ringsize(K):
        return sum(K.nodes[x]['deg'] for x in K) - K.number_of_edges() - 3 * K.number_of_nodes() + 3
    Ku = G.subgraph(keep).copy()
    if src == 'RPATN' or r is None: return Ku if nx.is_connected(Ku) else None
    if m == len(keep) and nx.is_connected(Ku) and ringsize(Ku) == r: return Ku
    K0 = G.subgraph(keep[1:]).copy()
    if m == len(keep) - 1 and nx.is_connected(K0) and ringsize(K0) == r: return K0
    return None

def conf_from_kc(line):
    f = line.split(); mm = int(f[2]); rp = f[3].split(';'); ip = f[4].split(';')
    K = nx.Graph()
    for v in range(mm): K.add_node(v, deg=(0 if ip[v] == '-' else len(ip[v].split(','))) + (0 if rp[v] == '-' else len(rp[v].split(','))))
    for v in range(mm):
        if ip[v] != '-':
            for x in ip[v].split(','): K.add_edge(v, int(x))
    return K

def nx_embeds(G, F, K):
    need = collections.Counter(K.nodes[x]['deg'] for x in K)
    have = collections.Counter(G.nodes[x]['deg'] for x in G if G.nodes[x]['exact'])
    if any(have[k] < v for k, v in need.items()): return False
    tris = [t for t in nx.enumerate_all_cliques(K) if len(t) == 3]
    GM = iso.GraphMatcher(G, K, node_match=lambda a, b: a['exact'] and a['deg'] == b['deg'])
    for mp in GM.subgraph_isomorphisms_iter():   # node-induced
        inv = {v: k for k, v in mp.items()}
        if all(frozenset(inv[x] for x in t) in F for t in tris): return True
    return False

# engine-side configurations (offc_conf) keyed like the nx ones
ENG = {}; NXK = {}
kcl = {l.split()[0]: l for l in open(os.path.join(H, 'k55', 'row55_hits_kc.txt')) if l.strip()}
for src, nm, d0, P, r, m in ns['OFFREG']:
    K, why = ns['offc_conf'](src, nm, d0, P, r, m)
    if src == 'RPATN': key = nm.split()[0]
    else: key = (src, nm, d0)
    if key in ENG: continue
    Kx = conf_from_kc(kcl[key]) if src == 'RPATN' else conf_from_entry(src, nm, d0, P, r, m)
    if (K is None) != (Kx is None): print('ACCEPTANCE DIFFERS', key)
    if K is None or Kx is None: continue
    ENG[key] = K; NXK[key] = Kx
# distinct configurations only (by the engine's key), to keep the test affordable
dk = {}
for key, K in ENG.items():
    VV, g, A, T = K; k2 = (tuple(sorted((x, g[x]) for x in VV)), key[2] if (('u',) in VV and key[0] != 'RPATN') else 0, key[0] == 'RPATN')
    dk.setdefault(k2, key)
KEYS = list(dk.values()) + [k for k in ENG if not isinstance(k, tuple) or k[0] == 'RPATN']
KEYS = list(dict.fromkeys(KEYS))
print('configurations: %d accepted entries, %d distinct tested (rpatN from the kc file)' % (len(ENG), len(KEYS)), flush=True)

rng = random.Random(SEED)
rows = [(12, '555555555555', '757575757575')]
rows += [(int(l.split()[1]), l.split()[2], l.split()[3]) for l in open(os.path.join(H, 'k55', 'rows45_A67.txt')) if l.strip() and not l.startswith('#')]
LW = [5] * 12 + [6] * 4 + [7] * 3 + [8] + [9]
while len(rows) < NR:
    d = rng.choice([7, 7, 7, 8, 8, 9, 10, 11, 12, 13])
    rows.append((d, ''.join(str(rng.choice(LW)) for _ in range(d)), ''.join(str(rng.choice(LW)) for _ in range(d))))
rows = rows[:max(NR, 1)]
pcache = {}
def eng_hits(key, d, lk, sv):
    if (key, d) not in pcache: pcache[(key, d)] = ns['offc_embed'](ENG[key], d)
    for pat in pcache[(key, d)]:
        for r in range(d):
            for refl in (0, 1):
                ok = True
                for (t, i), S in pat:
                    j = (i + r) % d if not refl else ((r - i) % d if t == 'w' else (r - i - 1) % d)
                    if int(lk[j] if t == 'w' else sv[j]) not in S: ok = False; break
                if ok: return True
    return False
t0 = time.time(); tot = collections.Counter(); bad = []
for n, (d, lk, sv) in enumerate(rows):
    G, F = window_graph(d, [int(c) for c in lk], [int(c) for c in sv]); kr = 0
    for key in KEYS:
        a = eng_hits(key, d, lk, sv); b = nx_embeds(G, F, NXK[key])
        tot['pairs'] += 1; tot['both hit'] += a and b; kr += b
        if a != b:
            tot['MISMATCH'] += 1
            if len(bad) < 15: bad.append((d, lk, sv, key, 'engine' if a else 'networkx'))
    tot['rows killed (networkx)'] += kr > 0
    if n % 10 == 0: print('  row %d/%d d%d %s/%s: %d configurations embed; %.0fs' % (n, len(rows), d, lk, sv, kr, time.time() - t0), flush=True)
for x in bad: print('  MISMATCH d%d %s/%s %s only %s' % (x[0], x[1], x[2], x[3], x[4]))
print('offc physical test%s: %d rows x %d configurations = %d pairs, %d both hit, %d rows killed, %d mismatches (%.0fs)' % (
    ' (BROKEN CONTROL: s-s always adjacent)' if BROKEN else '', len(rows), len(KEYS), tot['pairs'], tot['both hit'], tot['rows killed (networkx)'], tot['MISMATCH'], time.time() - t0))
