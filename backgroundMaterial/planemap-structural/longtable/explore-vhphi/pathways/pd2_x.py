#!/usr/bin/env python3
"""pd2_x.py -- [exploratory, these graphs only] P-D afternoon pass. One process, stdlib.
A. re-check of the hand lemmas (lock criterion; lock2(s) => x_j not in K and lock1(F s)).
B. Variant X rules, T4's 26 radius-4 (hole,state) pairs first, then all states of T4, A_3 (all deg-5 holes), A_4 (all deg-5 holes).
C. shortest fills of the 26 radius-4 pairs in Tait terms.
D. candidate potentials: strict decrease along shortest fills / descent property.
States are canonical under colour renaming (first occurrence along sorted vertices); radius = pure Kempe distance to a
link with <= 3 colours (whole-component swaps in G-v)."""
import sys, time
from collections import Counter, defaultdict
sys.path.insert(0, '.')
from pd2_lib import *

t0 = time.process_time()
GS = list(graphs())

def info(g, col):
    """Tait data of an unfilled link-4 state"""
    d = g.lockdata(col); j = d['j']; L = g.L
    Z1, Z2 = set(d['Z1']), set(d['Z2'])
    Z1b, _ = g.ppath(col, j, {d['be'], d['ga']})            # other (beta,gamma) P-path (from e_j)
    Z2b, _ = g.ppath(col, (j + 1) % 5, {d['be'], d['de']})  # other (beta,delta) P-path (from e_{j+1})
    d['A1'] = len(g.side(L[(j + 2) % 5], Z1)); d['A2'] = len(g.side(L[j], Z2))
    d['B1'] = len(g.side(L[j], set(Z1b))); d['B2'] = len(g.side(L[(j + 2) % 5], set(Z2b)))
    d['len'] = len(Z1) + len(Z2)
    nodes = lambda Z: {x for e in Z for x in g.H[e]} - {'P'}
    d['shared'] = len(nodes(Z1) & nodes(Z2))
    k = 0
    for s in (1, 2, 3):
        k += sum(1 for c in components(g.H, {e: g.tc(col, e) for e in g.H}, {1, 2, 3} - {s}) if 'P' not in c)
    d['k'] = k
    d['gap'] = (j + 3) % 5
    Wp, _ = g.ppath(col, (j + 2) % 5, {d['ga'], d['de']})   # (gamma,delta) path joining the two odd edges
    d['lenW'] = len(Wp); d['C3'] = len(g.side(L[(j + 3) % 5], set(Wp)))
    x0, m, x2, a, b = roles(L, j)
    d['chains'] = len(comp(g.adj, col, m, {col[m], col[a]})) + len(comp(g.adj, col, m, {col[m], col[b]}))
    return d

def Kof(g, col):
    j = repeat_index(col, g.L); x0, m, x2, a, b = roles(g.L, j)
    return comp(g.adj, col, x2, {col[x0], col[a]})

def cutinfo(g, col, K):
    cut = {e for e in g.H if len(e & K) == 1}
    return ncomp_edges(cut, g.H), sorted(g.pidx[e] for e in cut if e in g.pidx), len(cut)

out = []
P = lambda *a: out.append(' '.join(str(x) for x in a))

# ------------------------------------------------------------------ data per graph
DATA = {}
for g in GS:
    st = g.all_states(); dist, byk, nbrs = dist_to_fill(g, st)
    DATA[g.name] = (g, dist, byk, nbrs)

# ------------------------------------------------------------------ A. hand-lemma re-checks
nA = bad1 = bad2 = bad3 = 0
for name, (g, dist, byk, nbrs) in DATA.items():
    for k, c in byk.items():
        if g.filled(c): continue
        d = g.lockdata(c); l = locks(g.adj, c, g.L)
        nA += 1; bad1 += (l != (d['lock1'], d['lock2']))
        if d['lock2']:
            j = d['j']; K = Kof(g, c)
            bad2 += (g.L[j] in K)
            Fs = F(g.adj, c, g.L); bad3 += (not locks(g.adj, Fs, g.L)[0])
P('[A] unfilled states', nA, '| lock criterion mismatches', bad1, '| lock2 & x_j in K', bad2, '| lock2(s) & not lock1(Fs)', bad3)

# ------------------------------------------------------------------ B. Variant X
def w_key(g, col):
    """radius-1 local Tait datum: for t = j..j+4 the relative Tait colours of the two outer edges of the dual node across e_t
    (roles beta,gamma,delta -> A,B,C), plus link degrees, rotated so j -> 0"""
    d = g.lockdata(col); j = d['j']; rn = {d['be']: 'A', d['ga']: 'B', d['de']: 'C'}
    s = []
    for i in range(5):
        t = (j + i) % 5; x, y = g.L[t], g.L[(t + 1) % 5]
        w = [u for u in g.adj[x] & g.adj[y] if u != 'v'][0]
        s.append(rn[col[x] ^ col[w]] + rn[col[y] ^ col[w]] + str(len(g.adj[x])))
    return ''.join(s)

def n2_key(g, col):
    """fixed graph and hole: colours of all vertices at distance <= 2 from v, renamed by first occurrence"""
    N1 = set(g.L); N2 = set(N1)
    for x in N1: N2 |= g.adj[x]
    N2.discard('v'); mp = {}; ks = []
    for u in sorted(N2, key=str):
        if col[u] not in mp: mp[col[u]] = len(mp)
        ks.append(mp[col[u]])
    return (g.name, tuple(ks))

def test_rule(label, keyf, pool):
    """pool: list of (g, col). outcome = F s doubly locked. rule = outcome is a function of keyf."""
    grp = defaultdict(set); ex = {}
    for g, c in pool:
        o = doubly(g.adj, F(g.adj, c, g.L), g.L); kk = keyf(g, c); grp[kk].add(o); ex.setdefault((kk, o), (g.name, g.key(c)))
    clash = [kk for kk, v in grp.items() if len(v) == 2]
    P('[B] rule', label, ': keys', len(grp), 'clashing keys', len(clash),
      ('-> KILLED, e.g. key %r: F DL at %s, not DL at %s' % (clash[0], ex[(clash[0], True)], ex[(clash[0], False)])) if clash else '-> survives on this pool')
    return not clash

def rule1(g, c):  # X1: one Kempe cycle in the cut of F's chain
    return cutinfo(g, c, Kof(g, c))[0] == 1

def test_iff(label, pred, pool):
    tab = Counter()
    for g, c in pool:
        tab[(pred(g, c), doubly(g.adj, F(g.adj, c, g.L), g.L))] += 1
    P('[B] rule', label, ': (predicate, F s DL) counts', dict(tab), '-> KILLED' if tab[(True, False)] + tab[(False, True)] else '-> survives on this pool')

R4 = [(g, c) for (g, dist, byk, nbrs) in DATA.values() if g.name.startswith('T4') for k, c in byk.items() if dist[k] == 4]
DLT4 = [(g, c) for (g, dist, byk, nbrs) in DATA.values() if g.name.startswith('T4') for k, c in byk.items() if not g.filled(c) and doubly(g.adj, c, g.L)]
DLA = [(g, c) for (g, dist, byk, nbrs) in DATA.values() if not g.name.startswith('T4') for k, c in byk.items() if not g.filled(c) and doubly(g.adj, c, g.L)]
P('[B] pools: T4 radius-4 pairs', len(R4), '(all DL:', all(doubly(g.adj, c, g.L) for g, c in R4), ') | T4 DL states', len(DLT4), '| A_3+A_4 DL states', len(DLA))
for nm, pool in (('T4 radius-4', R4), ('T4 all DL', DLT4), ('A_3+A_4 all DL', DLA)):
    P('[B] pool', nm)
    test_rule('X0 (pairings of the 5 ends only; constant on DL states)', lambda g, c: 'const', pool)
    test_rule('X2 (pairings + radius-1 Tait datum + link degrees)', w_key, pool)
    test_rule('X3 (pairings + all colours within distance 2 of v, per graph and hole)', n2_key, pool)
    test_iff('X1 (F s DL <=> cut of F chain is ONE Kempe cycle)', rule1, pool)

# ------------------------------------------------------------------ C. shortest fills in Tait terms
def describe_swap(g, c, p, q, K, n):
    s = p ^ q; nc, pedges, ncut = cutinfo(g, c, K)
    a = g.roles(c); b = g.roles(n) if not g.filled(n) else None
    rel = lambda r, x: {r[1]: 'b', r[2]: 'g', r[3]: 'd'}[x]
    return dict(cls=rel(a, s), K=len(K), cyc=nc, P=tuple(pedges), cut=ncut,
                gap=(a[0] + 3) % 5, gap2=None if b is None else (b[0] + 3) % 5, filled=g.filled(n))

P('[C] radius-4 T4 states: every shortest-fill first step (class of the swap in Tait roles b/g/d = beta/gamma/delta of the state,')
P('    |K|, # Kempe cycles in the cut, P-edges in the cut, gap index (the lone beta edge between the odd edges) before->after)')
stepstats = Counter(); seqs = Counter()
def shortest_paths(g, dist, c, acc, path):
    if g.filled(c): seqs[tuple(path)] += 1; return
    for p, q, K, n in g.swaps(c):
        nn = g.canon(n)
        if dist[g.key(nn)] == dist[g.key(c)] - 1:
            dsc = describe_swap(g, c, p, q, K, n)
            stepstats[(dist[g.key(c)], dsc['cls'], dsc['cyc'], len(dsc['P']))] += 1
            shortest_paths(g, dist, nn, acc, path + [(dsc['cls'], dsc['cyc'], len(dsc['P']), (dsc['gap2'] - dsc['gap']) % 5 if dsc['gap2'] is not None else 'F')])
for g, c in R4:
    shortest_paths(g, DATA[g.name][1], c, None, [])
P('[C] step counts keyed (radius before, swap class, #cut cycles, #P-edges in cut):')
for k, v in sorted(stepstats.items(), key=str): P('     ', k, v)
P('[C] distinct shortest-path step patterns (class,#cyc,#P-edges,gap shift or F=fill) over all 26 pairs:', len(seqs))
for k, v in seqs.most_common(8): P('     ', v, k)

# ------------------------------------------------------------------ D. potentials
FEAT = ['nDL', '-nDL', 'lenW', 'C3', '-C3', 'chains', '-chains', 'max(A1,A2)', 'A1', 'A2', 'A1+A2', 'min(A1,A2)', 'B1+B2', 'A1+A2+B1+B2', 'len', 'shared', 'k', '|K|', '-(A1+A2)', '-len']
def phi(g, c, name):
    d = info(g, c)
    nDL = sum(1 for (_, _, _, n) in g.swaps(c) if not g.filled(n) and doubly(g.adj, n, g.L))
    v = {'nDL': nDL, '-nDL': -nDL, 'A1': d['A1'], 'A2': d['A2'], 'A1+A2': d['A1'] + d['A2'], 'min(A1,A2)': min(d['A1'], d['A2']), 'B1+B2': d['B1'] + d['B2'],
         'A1+A2+B1+B2': d['A1'] + d['A2'] + d['B1'] + d['B2'], 'len': d['len'], 'shared': d['shared'], 'k': d['k'],
         '|K|': len(Kof(g, c)), 'lenW': d['lenW'], 'C3': d['C3'], '-C3': -d['C3'], 'chains': d['chains'], '-chains': -d['chains'], 'max(A1,A2)': max(d['A1'], d['A2']), '-(A1+A2)': -d['A1'] - d['A2'], '-len': -d['len']}
    return v[name]
cache = {}
def ph(g, c):
    kk = (g.name, g.key(c))
    if kk not in cache: cache[kk] = {f: phi(g, c, f) for f in FEAT}
    return cache[kk]
P('[D] potentials on DL states (radius >= 2). "every": strictly decreases along EVERY shortest-fill step between DL states;')
P('    "some": every DL state of radius >= 3 has a shortest-fill successor (DL) with strictly smaller value;')
P('    "descent": every DL state has SOME swap to a non-DL/filled state or to a DL state with strictly smaller value (no use of radius).')
for grp in ('T4', 'A_3', 'A_4'):
    res = {f: [0, 0, 0, 0, 0, 0] for f in FEAT}   # every-viol, every-tot, some-viol, some-tot, descent-viol, descent-tot
    for name, (g, dist, byk, nbrs) in DATA.items():
        if not name.startswith(grp): continue
        for k, c in byk.items():
            if g.filled(c) or not doubly(g.adj, c, g.L): continue
            pc = ph(g, c); succ = []; anynon = False; nbrph = []
            for p, q, K, n in g.swaps(c):
                nn = g.canon(n)
                if g.filled(nn) or not doubly(g.adj, nn, g.L): anynon = True; continue
                pn = ph(g, nn); nbrph.append(pn)
                if dist[g.key(nn)] == dist[k] - 1: succ.append(pn)
            for f in FEAT:
                for pn in succ:
                    res[f][1] += 1; res[f][0] += (pn[f] >= pc[f])
                if dist[k] >= 3:
                    res[f][3] += 1; res[f][2] += (not any(pn[f] < pc[f] for pn in succ))
                res[f][5] += 1; res[f][4] += (not anynon and not any(pn[f] < pc[f] for pn in nbrph))
    P('[D]', grp)
    for f in FEAT:
        r = res[f]; P('     %-12s every: %d/%d violations | some: %d/%d states fail | descent: %d/%d states fail' % (f, r[0], r[1], r[2], r[3], r[4], r[5]))

# radius vs A1+A2 table
for grp in ('T4', 'A_3', 'A_4'):
    tab = defaultdict(Counter)
    for name, (g, dist, byk, nbrs) in DATA.items():
        if not name.startswith(grp): continue
        for k, c in byk.items():
            if g.filled(c) or not doubly(g.adj, c, g.L): continue
            p = ph(g, c); tab[dist[k]][(p['A1'], p['A2'])] += 1
    P('[D] %s: radius -> histogram of (A1,A2) on DL states:' % grp, {r: dict(sorted(v.items())) for r, v in sorted(tab.items())})

P('cpu %.1f s' % (time.process_time() - t0))
print('\n'.join(out))
