# Independent D/C-reducibility check for the 7-wheel c7_5666567 (ring 13).
# Written from textbook definitions (Birkhoff/Heesch Kempe-chain D-closure, RSST C-reducibility);
# no repo C++/Lean consulted.
#
# Kempe formulation used:
#   For a ring colouring k and pair partition {a,b}|{c,d}, every ring vertex lies on exactly one
#   Kempe chain (ab-chain if k[v] in {a,b}, else cd-chain) of the outside graph.  The chains partition
#   the ring vertices into a NON-CROSSING partition whose blocks are type-monochromatic, and two
#   ring-adjacent vertices of the same type lie in the same chain.  Hence chains are unions of maximal
#   same-type runs ("blocks"); the runs alternate in type around the ring (2t runs).
#   k is good if for some pair partition, for EVERY admissible chain partition, some set of chains
#   (ab-chains swap a<->b, cd-chains swap c<->d) can be swapped to give a good colouring.
#   A finer partition offers a superset of swap options, so it suffices to check the maximal (coarsest)
#   admissible partitions: (pi, Kreweras(pi)) for pi a non-crossing partition of the t ab-runs, the
#   cd-runs grouped into the coarsest non-crossing partition compatible with pi.
#   With colours 0..3 and pairings x in {1,2,3} ({0,x}|{others}), any Kempe swap is XOR by x on the
#   swapped vertices.  Swapping a set S and its complement give the same colour class (global swap),
#   so we take nonempty S not containing block 0.
import itertools, sys, time
import numpy as np

T0 = time.time()
LINE = "c7_5666567 13 8 -;12,0;0,1,2;2,3,4;4,5,6;6,7;7,8,9;9,10,11,12 1,2,3,4,5,6,7;0,2,7;0,3,1;0,4,2;0,5,3;0,6,4;0,7,5;0,1,6"
name, rs, ms, ringpart, intpart = LINE.split()
n = int(rs); m = int(ms)
ringadj = [[] if s == '-' else [int(x) for x in s.split(',')] for s in ringpart.split(';')]
intadj = [[int(x) for x in s.split(',')] for s in intpart.split(';')]
assert len(ringadj) == m and len(intadj) == m
for j in range(m):
    for i in intadj[j]: assert j in intadj[i], (j, i)
# vertices: R0..R12 -> 0..12, Ij -> n+j
V = lambda j: n + j
edges = set()
for i in range(n): edges.add(frozenset((i, (i + 1) % n)))
for j in range(m):
    for r in ringadj[j]: edges.add(frozenset((r, V(j))))
    for i in intadj[j]: edges.add(frozenset((V(j), V(i))))
print(name, 'ring', n, 'interior', m, 'edges', len(edges))
print('interior degrees', [len(ringadj[j]) + len(intadj[j]) for j in range(m)])
# Euler check for near-triangulation of disc: E = 3V - 3 - r
print('E =', len(edges), ' 3V-3-r =', 3 * (n + m) - 3 - n)

# ---------- ring colourings ----------
reps = []
def rec(p):
    if len(p) == n:
        if p[-1] != p[0]: reps.append(tuple(p))
        return
    for c in range(min(4, max(p) + 2)):
        if c != p[-1]: rec(p + [c])
rec([0])
reps.sort()
N = len(reps)
print('ring colour classes', N)
K = np.array(reps, dtype=np.int64)              # N x n
pw = 4 ** np.arange(n, dtype=np.int64)
codes = K @ pw
canon = np.full(4 ** n, -1, dtype=np.int32)
for perm in itertools.permutations(range(4)):
    P = np.array(perm, dtype=np.int64)
    canon[P[K] @ pw] = np.arange(N, dtype=np.int32)

# ---------- extension ----------
def ring_sets_from_interior(eq_edges):
    """Enumerate interior colourings; eq_edges = set of X edges (contracted -> equal colours).
    Returns array (#distinct x n) of allowed-colour bitmasks per ring vertex."""
    out = set()
    for col in itertools.product(range(4), repeat=m):
        ok = True
        for j in range(m):
            for i in intadj[j]:
                if i > j:
                    e = frozenset((V(j), V(i)))
                    if (e in eq_edges) != (col[i] == col[j]): ok = False; break
            if not ok: break
        if not ok: continue
        allow = [15] * n
        for j in range(m):
            for r in ringadj[j]:
                if frozenset((r, V(j))) in eq_edges: allow[r] &= (1 << col[j])
                else: allow[r] &= ~(1 << col[j]) & 15
        if all(allow): out.add(tuple(allow))
    return np.array(sorted(out), dtype=np.int64)

def extendable(eq_edges):
    A = ring_sets_from_interior(eq_edges)
    res = np.zeros(N, dtype=bool)
    for row in A:
        res |= np.all((row[None, :] >> K) & 1, axis=1).astype(bool)
    return res, len(A)

ext, nA = extendable(set())
print('extendable classes', int(ext.sum()), '(distinct interior ring-constraint patterns %d)' % nA)

# ---------- Kempe structures ----------
def set_partitions(lst):
    if not lst: yield []; return
    f, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
        yield [[f]] + p
        for i in range(len(p)):
            yield p[:i] + [[f] + p[i]] + p[i + 1:]
def crossing(P):
    for A, B in itertools.combinations(P, 2):
        for a1, a2 in itertools.combinations(sorted(A), 2):
            for b1, b2 in itertools.combinations(sorted(B), 2):
                if a1 < b1 < a2 < b2 or b1 < a1 < b2 < a2: return True
    return False
def maximal_partitions(t):
    """runs 0..2t-1, ab runs even, cd runs odd. Returns list of block-lists (run indices)."""
    res = []
    for pi in set_partitions(list(range(t))):
        if crossing(pi): continue
        ab = [[2 * i for i in B] for B in pi]
        def sep(x, y):  # does some ab block separate cd positions x<y ?
            for B in ab:
                ins = any(x < b < y for b in B); outs = any(b < x or b > y for b in B)
                if ins and outs: return True
            return False
        cdpts = [2 * i + 1 for i in range(t)]
        par = {c: c for c in cdpts}
        def fnd(c):
            while par[c] != c: c = par[c]
            return c
        for x, y in itertools.combinations(cdpts, 2):
            if not sep(x, y): par[fnd(x)] = fnd(y)
        cdb = {}
        for c in cdpts: cdb.setdefault(fnd(c), []).append(c)
        blocks = ab + list(cdb.values())
        assert len(blocks) == t + 1
        assert not crossing(blocks)
        res.append(blocks)
    return res
MAXP = {t: maximal_partitions(t) for t in range(1, 7)}
print('maximal partitions per t', {t: len(v) for t, v in MAXP.items()})
# run-bitmask matrix per t: (P, S, 2t) indicator
IND = {}
for t, Ps in MAXP.items():
    mats = []
    for blocks in Ps:
        b0 = blocks[0] if 0 in blocks[0] else next(B for B in blocks if 0 in B)
        others = [B for B in blocks if B is not b0]
        rows = []
        for r in range(1, len(others) + 1):
            for S in itertools.combinations(others, r):
                v = np.zeros(2 * t, dtype=np.int64)
                for B in S:
                    for x in B: v[x] = 1
                rows.append(v)
        mats.append(rows)
    IND[t] = np.array(mats, dtype=np.int64)  # P x (2^t-1) x 2t
    assert IND[t].shape[1] == 2 ** t - 1

# group (k, x) by t; compute run-delta codes
groups = {t: ([], []) for t in range(1, 7)}  # t -> (ids, rundeltas)
for idx, k in enumerate(reps):
    for x in (1, 2, 3):
        typ = [min(c, c ^ x) for c in k]  # 0 if colour in {0,x} else 1
        starts = [i for i in range(n) if typ[i] != typ[i - 1]]
        s0 = next(i for i in starts if typ[i] == 0)
        si = starts.index(s0)
        starts = starts[si:] + starts[:si]
        t = len(starts) // 2
        rd = []
        for q in range(2 * t):
            a = starts[q]; b = starts[(q + 1) % (2 * t)]
            d = 0; i = a
            while True:
                d += x * 4 ** i
                i = (i + 1) % n
                if i == b: break
            rd.append(d)
        groups[t][0].append(idx * 3 + (x - 1))
        groups[t][1].append(rd)
TAB = {}
for t, (ids, rds) in groups.items():
    if not ids: continue
    ids = np.array(ids); RD = np.array(rds, dtype=np.int64)  # G x 2t
    P, S, _ = IND[t].shape
    out = np.empty((len(ids), P, S), dtype=np.int32)
    flatI = IND[t].reshape(P * S, 2 * t).T  # 2t x PS
    base = codes[ids // 3]
    CH = 4096
    for s in range(0, len(ids), CH):
        D = RD[s:s + CH] @ flatI  # each run used at most once -> sum == xor of disjoint masks
        newc = base[s:s + CH, None] ^ D
        cl = canon[newc]
        assert (cl >= 0).all()
        out[s:s + CH] = cl.reshape(-1, P, S)
    TAB[t] = (ids, out)
    print(' t=%d: %d (colouring,pairing) x %d partitions x %d swaps' % (t, len(ids), P, S))
print('precompute done %.1fs' % (time.time() - T0)); sys.stdout.flush()

def step(good):
    ok3 = np.zeros(3 * N, dtype=bool)
    for t, (ids, out) in TAB.items():
        g = good[out]                      # G x P x S
        ok3[ids] = g.any(axis=2).all(axis=1)
    return ok3.reshape(N, 3).any(axis=1)

good = ext.copy()
it = 0
while True:
    it += 1
    new = step(good) & ~good
    print('iter', it, 'new', int(new.sum())); sys.stdout.flush()
    if not new.any(): break
    good |= new
print('D-closure: good', int(good.sum()), 'bad', int(N - good.sum()))
print('D-reducible:', bool(good.all()))

# ---------- sanity check against brute-force enumeration of ALL admissible chain partitions ----------
def ncp_mono(seq):  # all non-crossing partitions of run positions with monochromatic blocks
    L = len(seq)
    def gen(pts):
        if not pts: yield []; return
        f, rest = pts[0], pts[1:]
        same = [i for i, p in enumerate(rest) if seq[p] == seq[f]]
        for r in range(len(same) + 1):
            for comb in itertools.combinations(same, r):
                blk = [f] + [rest[i] for i in comb]
                cut = [-1] + list(comb) + [len(rest)]
                gaps = [rest[cut[j] + 1:cut[j + 1]] for j in range(len(cut) - 1)]
                def rg(gs):
                    if not gs: yield []; return
                    for p in gen(gs[0]):
                        for q in rg(gs[1:]): yield p + q
                for p in rg(gaps): yield [blk] + p
    return list(gen(list(range(L))))
def brute_good_step(k, good):
    for x in (1, 2, 3):
        typ = [min(c, c ^ x) for c in k]
        # vertex-level partitions: blocks are unions of runs
        starts = [i for i in range(n) if typ[i] != typ[i - 1]]
        runs = []
        for q in range(len(starts)):
            a = starts[q]; b = starts[(q + 1) % len(starts)]
            vs = []; i = a
            while True:
                vs.append(i); i = (i + 1) % n
                if i == b: break
            runs.append(vs)
        allok = True
        for P in ncp_mono([typ[r[0]] for r in runs]):
            found = False
            for mask in range(1, 1 << len(P)):
                k2 = list(k)
                for j, B in enumerate(P):
                    if mask >> j & 1:
                        for rr in B:
                            for v in runs[rr]: k2[v] ^= x
                if good[canon[np.dot(k2, pw)]]: found = True; break
            if not found: allok = False; break
        if allok: return True
    return False
rng = np.random.default_rng(1)
# check fixpoint property on a sample: bad classes must fail brute step; also check early-iteration agreement
sample = rng.choice(N, 300, replace=False)
mism = 0
for i in sample:
    b = brute_good_step(reps[i], good)
    if (not good[i]) and b: mism += 1
st1 = step(ext)
samp2 = rng.choice(np.nonzero(~ext)[0], 300, replace=False)
mism2 = sum(brute_good_step(reps[i], ext) != st1[i] for i in samp2)
print('brute cross-check: fixpoint violations in 300 samples:', mism, '; iter-1 disagreements in 300 samples:', mism2)

# ---------- C-reducibility ----------
def parseX(spec):
    def v(s): return int(s[1:]) if s[0] == 'R' else V(int(s[1:]))
    return set(frozenset((v(a), v(b))) for a, b in (e.split('-') for e in spec))
def creduce(spec):
    X = parseX(spec)
    print('\nX =', spec, 'size', len(X))
    assert all(e in edges for e in X), 'X edge not in configuration'
    par = list(range(n + m))
    def f(a):
        while par[a] != a: a = par[a]
        return a
    for e in X:
        a, b = tuple(e); par[f(a)] = f(b)
    loops = [tuple(sorted(e)) for e in edges if e not in X and f(min(e)) == f(max(e))]
    cls = {}
    for v in range(n + m): cls.setdefault(f(v), []).append(v)
    nm = lambda v: 'R%d' % v if v < n else 'I%d' % (v - n)
    print(' identified classes:', [[nm(v) for v in c] for c in cls.values() if len(c) > 1])
    print(' loops (non-X edge inside a class):', [(nm(a), nm(b)) for a, b in loops])
    admissible = (not loops) and len(X) <= 4
    cext, nA = extendable(X)
    bad_in = int((cext & ~good).sum())
    print(' admissible:', admissible, '| classes extending to contracted config:', int(cext.sum()),
          '| of which bad:', bad_in)
    print(' C-reducible with this X:', admissible and bad_in == 0)
    return cext
c3 = creduce(['I0-I1', 'I0-I3', 'R2-I3'])
c4 = creduce(['I0-I1', 'I0-I3', 'R0-I2', 'R2-I3'])
print('\ncontracted-extendable sets of the two X identical:', bool((c3 == c4).all()))
print('\ntotal runtime %.1fs' % (time.time() - T0))
