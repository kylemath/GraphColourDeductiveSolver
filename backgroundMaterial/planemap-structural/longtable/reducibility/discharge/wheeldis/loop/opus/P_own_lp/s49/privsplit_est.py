"""s49: private-split estimate (no solve).  For each receiver row (d, LINK, SWORD) and each big link vertex w_i (letter 7 or 8),
split the row by the letters (5..9; 9 = >=9, never exact) of w_i's privates p_{i,1} (next to s_{i-1}) .. p_{i,k} (next to s_i),
and test which configurations embed in the plane 2-ball once those privates are exact.  Embedding = node-induced subgraph
isomorphism onto exact vertices with equal degrees whose triangles all land on faces (s39o/offc_phys.py's matcher, reused).
Configurations: (a) every A83 registry entry (pat=/cpat=/rpat, 128 exname C held out), K re-derived from its own window by the
OFFC_SPEC section 2 rule (offc_phys.conf_from_entry); (b) explore's whole 2026 set nl51_kc.txt (8,200 two-engine D; rpatN3's
source); (c) the 14 kpriv v3 engine-kill windows (explore 5f4d62d1 loop/k60/kpriv_v3.txt, md5 2b824170).  RSST 2.126 / 8406.123 excluded by name.
usage: python3 privsplit_est.py ROWSFILE OUT.json   (ROWSFILE lines: w d LINK SWORD)"""
import sys, os, json, time, itertools, collections, pickle, hashlib
import networkx as nx
from networkx.algorithms import isomorphism as iso
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
SC = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'
M = SC + '/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
E = B + '/s44/eng'; Q = B + '/s33z/reg_A83'; H = os.path.dirname(os.path.abspath(__file__))
NL51 = SC + '/ex_A83/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/k51/nl51_kc.txt'
EXCL = ('2.126', '8406.123')

def window_graph(d, lk, sv, priv=None):
    """offc_phys.window_graph plus fixed private letters: priv = {i: [letter of p_{i,1}, .., p_{i,k}]} (9 = not exact)"""
    priv = priv or {}
    G = nx.Graph(); F = set()
    G.add_node('u', deg=d, exact=True)
    for i in range(d): G.add_node(('w', i), deg=lk[i], exact=lk[i] != 9); G.add_node(('s', i), deg=sv[i], exact=sv[i] != 9)
    arcs = {}
    for i in range(d):
        k = lk[i] - 5
        ps = [('p', i, j) for j in range(1, k + 1)]
        for j, p in enumerate(ps):
            if i in priv: G.add_node(p, deg=priv[i][j], exact=priv[i][j] != 9)
            else: G.add_node(p, deg=None, exact=False)
        arcs[i] = [('s', (i - 1) % d)] + ps + [('s', i)]
    for i in range(d):
        a, b = ('w', i), ('w', (i + 1) % d)
        G.add_edge('u', a); G.add_edge(a, b); F.add(frozenset(('u', a, b)))
        G.add_edge(a, ('s', i)); G.add_edge(b, ('s', i)); F.add(frozenset((a, b, ('s', i))))
        arc = arcs[i]
        for x, y in zip(arc, arc[1:]): G.add_edge(x, y); G.add_edge(a, x); G.add_edge(a, y); F.add(frozenset((a, x, y)))
    return G, F

def ringsize(K): return sum(K.nodes[x]['deg'] for x in K) - K.number_of_edges() - 3 * K.number_of_nodes() + 3

def conf_from_entry(src, nm, d0, P, r, m):
    ex = {sl: next(iter(S)) for sl, S in P if len(S) == 1 and 5 <= next(iter(S)) <= 8}
    for (t, i) in ex:
        if t == 's' and ('s', (i + 1) % d0) in ex and ('w', (i + 1) % d0) not in ex: return None
    lk = [ex.get(('w', i), 9) for i in range(d0)]; sv = [ex.get(('s', i), 9) for i in range(d0)]
    G, F = window_graph(d0, lk, sv)
    keep = ['u'] + sorted(ex)
    Ku = G.subgraph(keep).copy()
    if src in ('RPATN', 'RPAT') or r is None: return Ku if nx.is_connected(Ku) else None
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

def prep(K):
    return (K, collections.Counter(K.nodes[x]['deg'] for x in K), [t for t in nx.enumerate_all_cliques(K) if len(t) == 3])

def embeds(G, F, have, KK, want_map=False):
    K, need, tris = KK
    if any(have[k] < v for k, v in need.items()): return None
    GM = iso.GraphMatcher(G, K, node_match=lambda a, b: a['exact'] and a['deg'] == b['deg'])
    for mp in GM.subgraph_isomorphisms_iter():
        inv = {v: k for k, v in mp.items()}
        if all(frozenset(inv[x] for x in t) in F for t in tris): return mp
    return None

def load_confs():
    ck = H + '/confs_A83.pkl'
    if os.path.exists(ck): return pickle.load(open(ck, 'rb'))
    sv = sys.argv
    sys.argv = [E + '/pcheck.py', 'none', 'root=' + M, 'args=' + Q + '/args_A83.txt', 'rpat=' + B + '/rpatD.txt',
                'exname=' + B + '/s40f/exname_rm128.txt', 'work=' + SC + '/P/w49', 'offc']
    ns = {'__file__': sys.argv[0], '__name__': 'pcheck_lib'}
    exec(open(sys.argv[0]).read().replace("}.get(CMD, lambda: print(__doc__))()", "}.get(CMD, lambda: None)()"), ns)
    sys.argv = sv
    exec(open(E + '/offc.py').read(), ns); ns['offc_extend'] = lambda: None
    ns['load_patterns']()
    C = []; seen = {}; stat = collections.Counter()
    def add(src, nm, K):
        h = nx.weisfeiler_lehman_graph_hash(K, node_attr='degs')
        for j in seen.get(h, []):
            if nx.is_isomorphic(C[j][2], K, node_match=lambda a, b: a['deg'] == b['deg']): C[j][3].append((src, nm)); stat['dup'] += 1; return
        seen.setdefault(h, []).append(len(C)); C.append((src, nm, K, []))
    for src, nm, d0, P, r, m in ns['OFFREG']:
        if any(x in nm for x in EXCL): stat['excl'] += 1; continue
        K = conf_from_entry(src, nm, d0, P, r, m)
        if K is None: stat['skip ' + src] += 1; continue
        for x in K: K.nodes[x]['degs'] = str(K.nodes[x]['deg'])
        stat['acc ' + src] += 1; add(src, nm, K)
    for fn, tag in ((NL51, 'NL51'), (H + '/kpriv_kc.txt', 'KPRIV')):
        for l in open(fn):
            if not l.strip() or l.startswith('#'): continue
            K = conf_from_kc(l)
            for x in K: K.nodes[x]['degs'] = str(K.nodes[x]['deg'])
            stat['acc ' + tag] += 1; add(tag, l.split()[0], K)
    out = ([(s, n, K, al) for s, n, K, al in C], dict(stat))
    pickle.dump(out, open(ck, 'wb'))
    return out

def cells_of(lk, i):
    k = lk[i] - 5
    return [list(c) for c in itertools.product((5, 6, 7, 8, 9), repeat=k)]

if __name__ == '__main__':
    t0 = time.time()
    C, stat = load_confs()
    print('configurations: %d distinct; %s; %.0fs' % (len(C), stat, time.time() - t0), flush=True)
    PK = [prep(K) for _, _, K, _ in C]
    rows = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
    res = []
    for w, d, LK, SV in rows:
        d = int(d); lk = [int(c) for c in LK]; sv = [int(c) for c in SV]
        G, F = window_graph(d, lk, sv); have = collections.Counter(G.nodes[x]['deg'] for x in G if G.nodes[x]['exact'])
        base = [j for j, KK in enumerate(PK) if embeds(G, F, have, KK)]
        print('row %s %d %s/%s: %d configurations embed in the 1.5-ball (offc)' % (w, d, LK, SV, len(base)), [C[j][1] for j in base[:5]], flush=True)
        big = [i for i in range(d) if lk[i] in (7, 8)]
        rr = {'w': float(w), 'd': d, 'link': LK, 'sword': SV, 'base': [C[j][:2] for j in base], 'big': big, 'single': {}, 'joint': {}}
        killers = {}
        for i in big:
            out = {}
            for c in cells_of(lk, i):
                G2, F2 = window_graph(d, lk, sv, {i: c}); h2 = collections.Counter(G2.nodes[x]['deg'] for x in G2 if G2.nodes[x]['exact'])
                ks = []
                for j, KK in enumerate(PK):
                    if j in base: continue
                    mp = embeds(G2, F2, h2, KK)
                    if mp is not None:
                        ks.append((C[j][0], C[j][1], len(C[j][3]), sorted(str(x) for x in mp if x[0] == 'p')))
                        if len(ks) >= 3: break
                out[''.join(map(str, c))] = ks
            rr['single'][i] = out
            nk = sum(1 for v in out.values() if v)
            print('  w%d=%d: %d/%d cells killed; %.0fs' % (i, lk[i], nk, len(out), time.time() - t0), flush=True)
        # joint key over pairs of big vertices: a joint cell dies if a marginal dies, else test configurations needing both
        for i, j2 in itertools.combinations(big, 2):
            if os.environ.get('NOJOINT') or (lk[i] - 5) * (lk[j2] - 5) > 4: continue   # 7-7 pairs only (625 cells); 7-8 / 8-8 skipped for cost
            si, sj = rr['single'][i], rr['single'][j2]; extra = {}
            for a in si:
                if si[a]: continue
                for b in sj:
                    if sj[b]: continue
                    G2, F2 = window_graph(d, lk, sv, {i: [int(x) for x in a], j2: [int(x) for x in b]})
                    h2 = collections.Counter(G2.nodes[x]['deg'] for x in G2 if G2.nodes[x]['exact'])
                    for jj, KK in enumerate(PK):
                        if jj in base: continue
                        mp = embeds(G2, F2, h2, KK)
                        if mp is not None: extra[a + '|' + b] = (C[jj][0], C[jj][1], sorted(str(x) for x in mp if x[0] == 'p')); break
            nsurv = sum(1 for a in si if not si[a]) * sum(1 for b in sj if not sj[b])
            rr['joint']['%d,%d' % (i, j2)] = {'surv_marginal': nsurv, 'extra_killed': extra}
            print('  joint w%d,w%d: %d cells survive both marginals, %d more die jointly; %.0fs' % (i, j2, nsurv, len(extra), time.time() - t0), flush=True)
        res.append(rr)
        json.dump(res, open(sys.argv[2], 'w'), indent=1, default=str)
    print('done %.0fs' % (time.time() - t0))
