#!/usr/bin/env python3
"""Track A task 2 [exploratory]: anatomy of quarter-floor equality classes (F/N = 1/4) in the frame class, and a product test on all classes.

Per graph: picyc --full gives every class (size N, filled F) at every degree-5 hole (engine 1). Holes holding a class that is
small (N <= SMALL) or has N a power of two or has 4F = N are re-enumerated with kempe_py.Space (engine 2), and each such class gets:
  - the move graph: states, single whole-component Kempe swaps between distinct states (self-loops = renamings dropped);
    each edge is labelled by its CHAIN = the swapped component as a vertex set, made renaming-invariant by pairing it with its
    complement inside the {p,q}-subgraph (swapping K or the rest of the {p,q}-subgraph gives the same state up to renaming);
  - PRODUCT test ("product of k independent chain flips"): N = 2^k, every state has exactly k distinct neighbours, and there are
    k chain labels c_1..c_k such that each state has exactly one c_i-edge for every i and the coordinates x(t) = x(s) xor e_i along
    c_i-edges are consistent and bijective onto {0,1}^k (labels are matched up to renaming invariance: parallel edges must carry
    the SAME chain vertex set);
    also the weaker graph test: the move graph is isomorphic to the hypercube Q_k (labels ignored);
  - filled positions: is the filled set a subcube {x : x_i = a_i for i in S}? then F/N = 2^-|S|;
  - per unfilled state: repeat j (c(x_j) = c(x_{j+2})), lock1 = x_{j+3} in the {mu,A}-component of x_{j+1}, lock2 = x_{j+4} in the
    {mu,B}-component of x_{j+1} (picyc / NightLockBreaking definitions, link in rotation order), DL = both;
  - link word = degrees of x_0..x_4; colour word of each state on the link.
usage: anatomy.py OUT.jsonl LISTFILE... (picyc lines) [--faces JSON...]   (Pool(4))"""
import sys, os, json, itertools
from multiprocessing import Pool
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/common')
from kempe_py import Space
from tracka_lib import parse_line, rot_from_faces, G
from holes import picyc_holes
SMALL = 64

def pow2(n): return n > 0 and n & (n - 1) == 0

def locks(sp, s):
    L = sp.linki; c = [s[i] for i in L]
    if len(set(c)) <= 3: return None
    j = next(j for j in range(5) if c[j] == c[(j + 2) % 5])
    mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
    cm = sp.cmasks(s); m = 1 << L[(j + 1) % 5]
    l1 = bool(sp.flood(m, cm[mu] | cm[A]) >> L[(j + 3) % 5] & 1)
    l2 = bool(sp.flood(m, cm[mu] | cm[B]) >> L[(j + 4) % 5] & 1)
    return dict(j=j, lock1=l1, lock2=l2, DL=l1 and l2)

def word(sp, s):
    mp = {}; return ''.join('abcd'[mp.setdefault(s[i], len(mp))] for i in sp.linki)

def analyse_class(sp, members, hole_deg):
    idx = {k: i for i, k in enumerate(members)}; N = len(members)
    nb = [dict() for _ in range(N)]   # neighbour index -> set of chain labels
    for k in members:
        s = sp.states[k]; cm = sp.cmasks(s)
        for t, p, q, K in sp.moves(k):
            if t == k: continue
            rest = (cm[p] | cm[q]) & ~K
            lab = tuple(sorted((K, rest)))
            nb[idx[k]].setdefault(idx[t], set()).add(lab)
    deg = [len(x) for x in nb]
    fil = [sp.filled(k) for k in members]; F = sum(fil)
    rec = dict(N=N, F=F, degs=dict(Counter(deg)), edges=sum(deg) // 2)
    # graph hypercube test (labels ignored) and labelled product test
    k = N.bit_length() - 1
    rec['pow2'] = pow2(N); rec['k'] = k if pow2(N) else None
    cube = prod = False; coord = None
    if pow2(N) and all(d == k for d in deg):
        # labelled: each edge must carry exactly one label class shared by parallel edges
        lab0 = {}
        for t, labs in nb[0].items(): lab0[t] = labs
        gens = list(nb[0].keys())   # k neighbours of the root
        # assign labels: map each edge label set -> generator i via the root's edges, then propagate
        L2i = {}
        for i, t in enumerate(gens):
            for lab in nb[0][t]: L2i[lab] = i
        coord = [None] * N; coord[0] = 0; queue = [0]; ok = True
        for u in queue:
            for t, labs in nb[u].items():
                ii = {L2i[l] for l in labs if l in L2i}
                if len(ii) != 1: ok = False; break
                c = coord[u] ^ (1 << ii.pop())
                if coord[t] is None: coord[t] = c; queue.append(t)
                elif coord[t] != c: ok = False; break
            if not ok: break
        prod = ok and None not in coord and len(set(coord)) == N
        # unlabelled hypercube check: BFS coordinates via common-neighbour structure (brute force for k <= 5)
        if prod: cube = True
        else:
            cube = is_hypercube([set(x) for x in nb], k)
    rec['product'] = prod; rec['hypercube'] = cube
    if prod:
        fc = [coord[i] for i in range(N) if fil[i]]
        # subcube test
        sub = None
        for S in range(1 << k):
            vals = {c & S for c in fc}
            if len(vals) == 1 and len(fc) == N >> bin(S).count('1'):
                if sub is None or bin(S).count('1') < bin(sub[0]).count('1'): sub = (S, vals.pop())
        rec['filled_subcube'] = None if sub is None else dict(fixed_dims=bin(sub[0]).count('1'), mask=sub[0], val=sub[1])
        rec['filled_coords'] = sorted(fc)
        # chains: one representative label per generator
        ch = []
        for i, t in enumerate(gens):
            lab = sorted(nb[0][t])[0]; K, R = lab
            s0 = sp.states[members[0]]
            vs = lambda M: sp.mask_vertices(M)
            touch = lambda M: [x for x in sp.link if sp.idx[x] is not None and (M >> sp.idx[x]) & 1]
            ch.append(dict(dim=i, K=vs(K), rest=vs(R), K_link=touch(K), rest_link=touch(R), nlabels_root=len(nb[0][t])))
        rec['chains'] = ch
        # per-factor floor: fraction of filled along each dimension's pairs
        fac = []
        for i in range(k):
            pairs = [(a, a | 1 << i) for a in range(N) if not a >> i & 1]
            inv = {coord[j]: j for j in range(N)}
            fac.append(Counter((fil[inv[a]], fil[inv[b]]) for a, b in pairs))
        rec['factor_pairs'] = [{('%d%d' % kk): v for kk, v in f.items()} for f in fac]
    # cycle structure: connected 2-regular class -> list states in cyclic order with the edge (chain) between consecutive ones
    rec['cycle'] = None
    if all(d == 2 for d in deg) and N >= 3:
        order = [0]; prev = None
        while True:
            u = order[-1]; nxt = [t for t in nb[u] if t != prev]
            if prev is None: nxt = nxt[:1]
            t = nxt[0]
            if t == 0: break
            prev = u; order.append(t)
        rec['cycle_len'] = len(order); rec['is_single_cycle'] = len(order) == N
        if len(order) == N:
            cyc = []
            for a, u in enumerate(order):
                t = order[(a + 1) % N]; s = sp.states[members[u]]
                mp = {}
                for i in sp.linki:
                    if s[i] not in mp: mp[s[i]] = 'abcd'[len(mp)]
                labs = sorted(nb[u][t]); e = []
                for K, R in labs:
                    # colour pair of this swap in state s (letters of the link word; x = colour absent from link)
                    cols = sorted({s[i] for i in range(sp.N) if (K | R) >> i & 1})
                    e.append(dict(pair=''.join(sorted(mp.get(c, 'x') for c in cols)), K=len(sp.mask_vertices(K)), R=len(sp.mask_vertices(R)),
                                  K_link=[i for i, x in enumerate(sp.link) if K >> sp.idx[x] & 1], R_link=[i for i, x in enumerate(sp.link) if R >> sp.idx[x] & 1]))
                lk = locks(sp, s)
                cyc.append(dict(word=word(sp, s), filled=fil[u], lock=None if lk is None else ('DL' if lk['DL'] else 'L1' if lk['lock1'] else 'L2' if lk['lock2'] else 'N0'),
                                j=None if lk is None else lk['j'], edge_to_next=e))
            rec['cycle'] = cyc
            rec['filled_positions'] = [a for a, c in enumerate(cyc) if c['filled']]
    # states: word, filled, locks
    st = []
    for i, kk in enumerate(members):
        s = sp.states[kk]; lk = locks(sp, s)
        st.append(dict(coord=None if coord is None else coord[i], word=word(sp, s), filled=fil[i], **({} if lk is None else lk)))
    rec['states'] = st if N <= SMALL else None
    rec['unfilled_lock_hist'] = dict(Counter(('DL' if x.get('DL') else 'L1' if x.get('lock1') else 'L2' if x.get('lock2') else 'N0') for x in st if not x['filled']))
    return rec

def is_hypercube(adj, k):
    """adj: list of neighbour sets, N = 2^k, k-regular. Standard recognition: root 0, neighbours = basis; label vertices at
    distance d by the union of basis labels of their predecessors at distance d-1; check bijectivity and edges = single-bit."""
    N = len(adj); dist = [-1] * N; dist[0] = 0; q = [0]
    for u in q:
        for v in adj[u]:
            if dist[v] < 0: dist[v] = dist[u] + 1; q.append(v)
    if -1 in dist: return False
    lab = [0] * N; nbr0 = sorted(adj[0])
    for i, v in enumerate(nbr0): lab[v] = 1 << i
    for u in sorted(range(N), key=lambda x: dist[x]):
        if dist[u] >= 2:
            pre = [w for w in adj[u] if dist[w] == dist[u] - 1]
            x = 0
            for w in pre: x |= lab[w]
            lab[u] = x
            if bin(x).count('1') != dist[u] or len(pre) != dist[u]: return False
    if len(set(lab)) != N: return False
    return all(bin(lab[u] ^ lab[v]).count('1') == 1 for u in range(N) for v in adj[u])

def work(item):
    name, rot = item
    H = picyc_holes(rot, name)
    out = dict(name=name, n=len(rot), holes={}, allclasses=[])
    adj = {v: set(r) for v, r in enumerate(rot)}
    for h, cls in sorted(H.items()):
        ld = [len(rot[x]) for x in rot[h]]
        for (N, F) in cls: out['allclasses'].append((h, N, F))
        if not any(N <= SMALL or pow2(N) or 4 * F == N for N, F in cls): continue
        sp = Space(adj, h, link=rot[h]); sp.build_graph(); cl, nc = sp.classes()
        mem = [[] for _ in range(nc)]
        for kk, c in enumerate(cl): mem[c].append(kk)
        recs = []
        for m in mem:
            N = len(m); F = sum(sp.filled(kk) for kk in m)
            if N <= SMALL or pow2(N) or 4 * F == N:
                r = analyse_class(sp, m, ld); r['linkdeg'] = ld; recs.append(r)
            else: recs.append(dict(N=N, F=F, linkdeg=ld, skipped=True))
        # cross-check engine 1 vs engine 2 class multisets at this hole
        assert sorted((r['N'], r['F']) for r in recs) == sorted(cls), (name, h)
        out['holes'][str(h)] = recs
    return out

if __name__ == '__main__':
    out = sys.argv[1]; items = []; args = sys.argv[2:]
    if '--faces' in args:
        i = args.index('--faces'); lists, faces = args[:i], args[i + 1:]
    else: lists, faces = args, []
    for fn in lists:
        for l in open(fn):
            if l.strip(): items.append(parse_line(l))
    for fn in faces:
        d = json.load(open(fn))
        for k, r in enumerate(d if isinstance(d, list) else [d]):
            items.append((r['name'], rot_from_faces([tuple(t) for t in r['faces']])))
    with Pool(4) as P, open(out, 'w') as f:
        for r in P.imap_unordered(work, items):
            f.write(json.dumps(r) + '\n'); f.flush()
