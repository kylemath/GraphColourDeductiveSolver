#!/usr/bin/env python3
"""Studio copy (18 Oct) of loop/opus/B_rsst_rows/rsst_rows.py (Opus team, branch claude/project-thread-7uelj0);
only change: RSST_ONLYD=1 restricts pattern generation to RSST D configurations.
B_rsst_rows [exploratory]: which receiver rows (d, link w_0..w_{d-1}, shared s_0..s_{d-1}) contain an RSST
configuration (RSST appearance: interior G(K) maps injectively, exact degrees, induced, faces to faces)?

Row semantics (wlp3.py parse(), sep3.cpp): u has exact degree d; w_i is u's i-th link vertex; s_i is the apex of the
triangle w_i w_{i+1} s_i on the far side of edge w_i w_{i+1}.  A 5 at w_i has rotation (u, w_{i+1}, s_i, s_{i-1},
w_{i-1}).  Letters 5..8 are exact degrees, 9 means degree >= 9 (never exact).  A w_i of exact degree k has k-5
private neighbours between s_{i-1} and s_i, of unknown degree.

Known graph among {u, w, s} in an internally 6-connected triangulation: u ~ w_i; w_i ~ w_{i+1}; s_i ~ w_i, w_{i+1};
s_{i-1} ~ s_i iff w_i = 5; no other edges or identifications (each would give a separating cycle of length <= 4, or
a separating 5-cycle with >= 2 vertices on each side, or a degree-4 vertex).  Every triangle among them is a face.

Hosts (vertices an interior vertex of K may map to):
  strict  : u and the w_i with an exact letter (all their neighbours exist in the patch) -- the coordinator's rule.
  relaxed : also the s_i with an exact letter.  s_i's outer neighbours are unknown but they are only ring vertices
            of K, which RSST appearance does not constrain; so this is still a valid RSST appearance.
Usage: python3 rsst_rows.py rows   -> per-family counts for row files (out/rows_hits.txt)
       python3 rsst_rows.py generic D -> which RSST configs embed in some degree-D receiver patch (out/generic_D.txt)
"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SI = os.path.abspath(os.path.join(W, '..', '..', '..', '..', 'studiointel'))
sys.path.insert(0, os.path.join(SI, 'routeb')); import rsst_parse

CONFS = rsst_parse.parse(os.path.join(SI, 'routeb', 'rsst', 'unavoidable.conf'))
def prep(c):
    r, n = c['r'], c['n']; U = list(range(r + 1, n + 1))
    deg = {u: len(c['adj'][u]) for u in U}; E = {u: set(x for x in c['adj'][u] if x > r) for u in U}
    order = [max(U, key=lambda u: (deg[u], len(E[u])))]; seen = set(order)
    while len(order) < len(U):
        b = max((u for u in U if u not in seen), key=lambda u: (len(E[u] & seen), deg[u])); order.append(b); seen.add(b)
    faces = set()
    for u in U:
        L = c['adj'][u]
        for i in range(len(L)):
            a, b = L[i], L[(i + 1) % len(L)]
            if a > r and b > r: faces.add(frozenset((u, a, b)))
    return {'deg': deg, 'E': E, 'order': order, 'dm': collections.Counter(deg.values()), 'faces': faces,
            'ring': r, 'kind': 'C' if c['k_contract'] > 0 else 'D', 'name': c['name']}
P = [prep(c) for c in CONFS]

def target(d, w, s, mode):
    """hostable vertices -> allowed degree set; adjacency among them."""
    host = {}
    host['u'] = {d}
    if mode.endswith('fixed'):   # only slots some 5-sender's code reads (others are free in the LP row)
        fw = [w[i] == 5 or w[(i - 1) % d] == 5 or w[(i + 1) % d] == 5 for i in range(d)]
        fs = [w[i] == 5 or w[(i + 1) % d] == 5 for i in range(d)]
        w = [w[i] if fw[i] else None for i in range(d)]; s0 = s
        s = [s[i] if fs[i] else None for i in range(d)]
        mode = 'relaxed' if mode == 'fixed' else 'strict'
        wfull = [x if x is not None else 0 for x in w]
    else: wfull = w
    for i in range(d):
        if w[i] is not None and w[i] <= 8: host[('w', i)] = {w[i]} if isinstance(w[i], int) else w[i]
        if mode == 'relaxed' and s[i] is not None:
            sv = s[i]
            if isinstance(sv, int):
                if sv <= 8: host[('s', i)] = {sv}
            else: host[('s', i)] = sv
    adj = {v: set() for v in host}
    def e(a, b):
        if a in host and b in host: adj[a].add(b); adj[b].add(a)
    for i in range(d):
        j = (i + 1) % d
        e('u', ('w', i)); e(('w', i), ('w', j)); e(('s', i), ('w', i)); e(('s', i), ('w', j))
        if wfull[i] == 5: e(('s', (i - 1) % d), ('s', i))
    return host, adj

def contains(host, adj, p):
    order, deg, E = p['order'], p['deg'], p['E']; phi = {}; used = set()
    def rec(k):
        if k == len(order):
            for f in p['faces']:   # every triangle among {u,w,s} is a face of T, so only check it is a triangle
                a, b, c = (phi[x] for x in f)
                if not (b in adj[a] and c in adj[a] and c in adj[b]): return False
            return True
        x = order[k]; nb = [y for y in order[:k] if y in E[x]]
        cands = adj[phi[nb[0]]] if nb else host.keys()
        for t in cands:
            if t in used or deg[x] not in host[t]: continue
            if any((y in E[x]) != (phi[y] in adj[t]) for y in order[:k]): continue
            phi[x] = t; used.add(t)
            if rec(k + 1): return True
            del phi[x]; used.discard(t)
        return False
    return rec(0)

def hits(d, w, s, mode):
    host, adj = target(d, w, s, mode)
    # degree multiset prefilter (only for exact hosts)
    hc = collections.Counter()
    for v, S in host.items():
        for x in S: hc[x] += 1
    out = []
    for i, p in enumerate(P):
        if len(p['deg']) > len(host): continue
        if any(hc[x] < m for x, m in p['dm'].items()): continue
        if contains(host, adj, p): out.append(i)
    return out

def L(ch): return int(ch)
def read_rows(fn):
    rows = []
    for line in open(fn):
        f = line.split()
        if 'receiver' in line:
            d = int(f[1][2:]); rows.append((d, f[3], f[5]))
        elif len(f) >= 2 and f[0].isdigit() and f[1].isdigit() and len(f[0]) == len(f[1]):
            rows.append((len(f[0]), f[0], f[1]))
    return rows

def run_rows():
    fams = [('binders (loop/b7/binders.txt)', 'loop/b7/binders.txt'),
            ('binders_self (out/job28)', 'out/job28/binders_self.txt'),
            ('HARD28-like 49 (loop/lf/seeds.txt)', 'loop/lf/seeds.txt'),
            ('HARD28 round-12 (hard_12_tight)', 'out/job28/hard_12_tight.txt'),
            ('tight round 12 (tight_12)', 'out/job28/tight_12.txt'),
            ('tight round 13 (tight_13)', 'out/job28/tight_13.txt')]
    o = open(os.path.join(HERE, 'out', 'rows_hits.txt'), 'w')
    for nm, fn in fams:
        if fn.endswith('hard_12_tight.txt'):
            rows = []
            for line in open(os.path.join(W, fn)):
                f = line.split()
                if f and f[0] == 'HARD28': rows.append((int(f[1][2:]), f[3], f[5]))
        else: rows = read_rows(os.path.join(W, fn))
        rows = sorted(set(rows))
        res = {}
        for mode in ('strict', 'relaxed', 'strictfixed', 'fixed'):
            cnt = 0; byd = collections.Counter(); totd = collections.Counter()
            for d, lk, sv in rows:
                h = hits(d, [L(c) for c in lk], [L(c) for c in sv], mode); totd[d] += 1
                if h:
                    cnt += 1; byd[d] += 1
                    o.write('%s\t%s\td=%d %s %s\t%s\n' % (nm, mode, d, lk, sv,
                            ' '.join('%s(r%d,%s)' % (P[i]['name'], P[i]['ring'], P[i]['kind']) for i in h)))
            res[mode] = (cnt, dict(byd), dict(totd))
        line = '%-36s rows %5d %s | ' % (nm, len(rows), res['strict'][2]) + ' | '.join('%s: %d %s' % (m, res[m][0], res[m][1]) for m in res)
        print(line, flush=True); o.write('# ' + line + '\n')

def run_generic(D):
    """Every link word over {5,6,7,8,9} up to dihedral symmetry; s = any degree 5..8 (wildcard host) in relaxed."""
    seen = set(); words = []
    for wd in itertools.product((5, 6, 7, 8, 9), repeat=D):
        cand = []
        for r in range(D):
            x = wd[r:] + wd[:r]; cand += [x, x[::-1]]
        m = min(cand)
        if m not in seen: seen.add(m); words.append(m)
    o = open(os.path.join(HERE, 'out', 'generic_%d.txt' % D), 'w')
    for mode in ('strict', 'fixed', 'relaxed'):
        fit = collections.defaultdict(list)
        for wd in words:
            s = [{5, 6, 7, 8}] * D
            for i in hits(D, list(wd), s, mode): fit[i].append(''.join(map(str, wd)))
        rc = collections.Counter((P[i]['ring'], P[i]['kind']) for i in fit)
        line = 'd=%d %s: %d of 633 RSST configs embed in some receiver patch; by (ring,kind) %s' % (
            D, mode, len(fit), dict(sorted(rc.items())))
        print(line, flush=True); o.write('# ' + line + '\n')
        for i in sorted(fit, key=lambda i: P[i]['ring']):
            p = P[i]
            o.write('%s\t%s ring %d %s interior %d degs %s\twords %d e.g. %s\n' % (mode, p['name'], p['ring'], p['kind'],
                    len(p['deg']), ''.join(map(str, sorted(p['deg'].values()))), len(fit[i]), ','.join(fit[i][:4])))

# ---------------- pattern generation for sep3 (raw lines "d k pos mask ...") ----------------
LI = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
ONLYD = os.environ.get('RSST_ONLYD') == '1'
def allemb(host, adj, p, cap=50):
    order, deg, E = p['order'], p['deg'], p['E']; phi = {}; used = set(); outs = []
    def rec(k):
        if len(outs) >= cap: return
        if k == len(order):
            for f in p['faces']:
                a, b, c = (phi[x] for x in f)
                if not (b in adj[a] and c in adj[a] and c in adj[b]): return
            outs.append({x: (phi[x], deg[x]) for x in phi}); return
        x = order[k]; nb = [y for y in order[:k] if y in E[x]]
        for t in (adj[phi[nb[0]]] if nb else host.keys()):
            if t in used or deg[x] not in host[t]: continue
            if any((y in E[x]) != (phi[y] in adj[t]) for y in order[:k]): continue
            phi[x] = t; used.add(t); rec(k + 1); del phi[x]; used.discard(t)
    rec(0); return outs

def pattern_from(d, w, emb):
    I = {t: dg for t, dg in emb.values()}
    Q = set(i for (k, i) in [t for t in I if t != 'u'] if k == 'w' and w[i] == 5)
    need_non5 = set()
    for t in list(I):
        if t == 'u': continue
        k, i = t
        if k == 'w' and w[i] != 5:
            if not ({(i - 1) % d, (i + 1) % d} & Q):
                c = [j for j in ((i - 1) % d, (i + 1) % d) if w[j] == 5]
                if not c: return None
                Q.add(c[0])
        if k == 's':
            if not ({i, (i + 1) % d} & Q):
                c = [j for j in (i, (i + 1) % d) if w[j] == 5]
                if not c: return None
                Q.add(c[0])
    for i in range(d):   # s_{i-1}, s_i both images: w_i must be pinned
        if ('s', (i - 1) % d) in I and ('s', i) in I:
            if w[i] == 5: Q.add(i)
            elif ('w', i) not in I:
                if not ({(i - 1) % d, (i + 1) % d} & Q):
                    c = [j for j in ((i - 1) % d, (i + 1) % d) if w[j] == 5]
                    if not c: return None
                    Q.add(c[0])
                need_non5.add(i)
    P = []
    for q in sorted(Q):
        slots = [('w', (q + 1) % d), ('s', q), ('s', (q - 1) % d), ('w', (q - 1) % d)]; m = 0
        for t, v in enumerate(slots):
            if v in I: S = [I[v]]
            elif v[0] == 'w' and v[1] in Q: S = [5]
            elif v[0] == 'w' and v[1] in need_non5: S = [6, 7, 8, 9]
            else: S = [5, 6, 7, 8, 9]
            for x in S: m |= 1 << (5 * t + LI[x])
        P.append((q, m))
    # verify every image slot is pinned
    pinned = {('w', q) for q in Q}
    for q in Q: pinned |= {('w', (q + 1) % d), ('s', q), ('s', (q - 1) % d), ('w', (q - 1) % d)}
    assert all(t == 'u' or t in pinned for t in I)
    return (d, tuple(P))

def gen_patterns(rowfiles, outfn):
    pats = {}; nrows = 0; nk = 0
    for fn in rowfiles:
        for d, lk, sv in sorted(set(read_rows(fn))):
            w = [int(c) for c in lk]; s = [int(c) for c in sv]; nrows += 1
            host, adj = target(d, w, s, 'fixed'); got = False
            for i in hits(d, w, s, 'fixed'):
                if ONLYD and P[i]['kind'] != 'D': continue   # Studio: D only (Lean agreesRSST: checker D iff RSST D)
                for emb in allemb(host, adj, P[i]):
                    pt = pattern_from(d, w, emb)
                    if pt: pats.setdefault(pt, P[i]['name']); got = True
            nk += got
    with open(outfn, 'w') as o:
        for (d, PP), nm in sorted(pats.items()):
            o.write('%d %d %s # %s\n' % (d, len(PP), ' '.join('%d %d' % pm for pm in PP), nm))
    print('rows %d, rows with an encodable RSST pattern %d, distinct patterns %d -> %s' % (nrows, nk, len(pats), outfn))

if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    if sys.argv[1] == 'rows': run_rows()
    elif sys.argv[1] == 'pat': gen_patterns(sys.argv[3:], sys.argv[2])
    else: run_generic(int(sys.argv[2]))

